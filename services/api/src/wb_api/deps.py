"""FastAPI request dependencies and wiring.

One database session is created per request and committed on success / rolled
back on error. The session factory, cipher keyring, and engine are process
singletons. ``X-Device-Id`` is a required header for citizen endpoints; it is
validated as a UUID and the device row is touched on every request so we have a
pseudonymous last-seen without storing PII.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from functools import lru_cache
from typing import Annotated, Any, Callable, Iterator

from fastapi import Depends, Header, Query
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from .bundles import BundleProvider
from .canonical import sha256_hex
from .config import Settings, get_settings
from .crypto import FieldCipher
from .db import make_engine, make_session_factory
from .errors import ValidationProblem
from .repositories import (
    AuditRepo,
    CatalogRepo,
    ContentBundleRepo,
    DeviceRepo,
    EvidenceRepo,
    FeedbackRepo,
    IdempotencyRepo,
    JourneyRepo,
)
from .services import (
    CatalogService,
    EvidenceService,
    FeedbackService,
    JourneyService,
    RouteResolver,
)


@lru_cache(maxsize=1)
def _session_factory():
    s = get_settings()
    engine = make_engine(
        s.database_url,
        pool_size=s.db_pool_size,
        max_overflow=s.db_max_overflow,
        pool_pre_ping=True,
        connect_args={"options": f"-c statement_timeout={s.db_statement_timeout_ms}"},
    )
    return make_session_factory(engine)


@lru_cache(maxsize=1)
def _cipher() -> FieldCipher:
    return FieldCipher.from_env()


def get_db() -> Iterator[Session]:
    session = _session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def check_db(session: Session) -> bool:
    try:
        session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


@dataclass
class Services:
    settings: Settings
    session: Session
    devices: DeviceRepo
    idempotency: IdempotencyRepo
    audit: AuditRepo
    catalog: CatalogService
    resolver: RouteResolver
    journeys: JourneyService
    evidence: EvidenceService
    feedback: FeedbackService


def get_services(session: Annotated[Session, Depends(get_db)]) -> Services:
    settings = get_settings()
    cipher = _cipher()
    catalog_repo = CatalogRepo(session)
    journey_repo = JourneyRepo(session, cipher)
    content_repo = ContentBundleRepo(session)
    provider = BundleProvider(content_repo=content_repo, bundle_dir=settings.bundle_dir)
    resolver = RouteResolver(catalog_repo, provider, fail_closed=settings.fail_closed_on_stale)
    audit = AuditRepo(session)
    return Services(
        settings=settings,
        session=session,
        devices=DeviceRepo(session),
        idempotency=IdempotencyRepo(session),
        audit=audit,
        catalog=CatalogService(catalog_repo),
        resolver=resolver,
        journeys=JourneyService(catalog=catalog_repo, journeys=journey_repo, resolver=resolver, audit=audit),
        evidence=EvidenceService(EvidenceRepo(session)),
        feedback=FeedbackService(feedback=FeedbackRepo(session, cipher), journeys=journey_repo, audit=audit),
    )


ServicesDep = Annotated[Services, Depends(get_services)]


def get_device_id(
    services: ServicesDep,
    x_device_id: Annotated[str | None, Header(alias="X-Device-Id")] = None,
) -> str:
    if not x_device_id:
        raise ValidationProblem("X-Device-Id header is required.", code="missing_device_id")
    try:
        normalized = str(uuid.UUID(x_device_id))
    except (ValueError, AttributeError):
        raise ValidationProblem("X-Device-Id must be a UUID.", code="invalid_device_id")
    services.devices.touch(normalized)
    return normalized


DeviceIdDep = Annotated[str, Depends(get_device_id)]


@dataclass
class Page:
    limit: int
    offset: int


def pagination(
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Page:
    cap = get_settings().max_page_size
    return Page(limit=min(limit, cap), offset=offset)


PageDep = Annotated[Page, Depends(pagination)]


def run_idempotent(
    services: Services,
    *,
    scope: str,
    key: str | None,
    payload: dict[str, Any],
    producer: Callable[[], BaseModel],
    success_status: int,
) -> tuple[dict, int, bool]:
    """Execute ``producer`` at most once per (scope, Idempotency-Key).

    Returns (json_body, status_code, replayed). When no key is supplied the
    producer simply runs (the caller accepts at-least-once semantics).
    """
    if not key:
        model = producer()
        return json.loads(model.model_dump_json()), success_status, False
    request_hash = sha256_hex({"scope": scope, "payload": payload})
    services.idempotency.lock(scope, key)
    existing = services.idempotency.find(scope, key, request_hash)
    if existing is not None:
        return existing.response_body or {}, existing.response_status, True
    model = producer()
    body = json.loads(model.model_dump_json())
    services.idempotency.store(
        scope, key, request_hash=request_hash, status=success_status,
        body=body, ttl_seconds=services.settings.idempotency_ttl_seconds,
    )
    return body, success_status, False


IdempotencyKeyHeader = Annotated[str | None, Header(alias="Idempotency-Key", min_length=16, max_length=128)]
