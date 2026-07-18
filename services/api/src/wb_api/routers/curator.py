"""Curator (governed) endpoints.

Source registry, snapshot fetch, draft creation, rule review,
bundle publish and rollback. All endpoints require curator auth
with the appropriate OAuth scope.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Header, Query, Response, status
from fastapi.responses import JSONResponse

from ..deps import IdempotencyKeyHeader, ServicesDep
from ..errors import NotFoundError, ValidationProblem
from ..schemas import (
    BundlePublication,
    CreateSourceRequest,
    PublishBundleRequest,
    RollbackBundleRequest,
    RuleVersionReview,
    RuleVersionStatus,
    Source,
)

router = APIRouter(prefix="/v1/curator", tags=["curator"])


# --- auth dependency (placeholder — will be OIDC in production) --------------

@dataclass
class CuratorAuth:
    """Authenticated curator context."""
    curator_id: str
    scopes: set[str]


def get_curator_auth(
    authorization: Annotated[str | None, Header()] = None,
) -> CuratorAuth:
    """Extract curator identity and scopes from the Authorization header.

    In production this validates an OIDC JWT. For now we accept a
    Bearer token with the format: ``Bearer <curator_id>:<scope1,scope2>``.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise ValidationProblem(
            "Authorization header with Bearer token is required.",
            code="unauthorized",
        )
    token = authorization.removeprefix("Bearer ").strip()
    parts = token.split(":", 1)
    curator_id = parts[0]
    scopes = set(parts[1].split(",")) if len(parts) > 1 else set()
    return CuratorAuth(curator_id=curator_id, scopes=scopes)


def require_scope(scope: str):
    """Dependency factory that requires a specific curator scope."""
    def checker(auth: Annotated[CuratorAuth, Depends(get_curator_auth)]) -> CuratorAuth:
        if scope not in auth.scopes:
            raise ValidationProblem(
                f"Scope '{scope}' is required.",
                code="insufficient_scope",
            )
        return auth
    return checker


# --- source registry ---------------------------------------------------------

@router.get("/sources")
def list_sources(
    services: ServicesDep,
    auth: Annotated[CuratorAuth, Depends(require_scope("sources:read"))],
    status_filter: Annotated[str | None, Query(alias="status")] = None,
    stale_only: Annotated[bool, Query()] = False,
) -> dict:
    """List source registry entries."""
    # TODO: wire to source-ingestion registry via services layer
    return {"items": []}


@router.post("/sources", status_code=status.HTTP_201_CREATED)
def create_source(
    body: CreateSourceRequest,
    services: ServicesDep,
    auth: Annotated[CuratorAuth, Depends(require_scope("sources:write"))],
    idempotency_key: IdempotencyKeyHeader = None,
) -> Response:
    """Register a new source."""
    # TODO: wire to source-ingestion registry
    source_id = str(uuid.uuid4())
    source = Source(
        id=source_id,
        canonical_url=body.canonical_url,
        publisher=body.publisher,
        authority_level=body.authority_level,
        jurisdiction_id=body.jurisdiction_id,
        status="active",
        freshness_class=body.freshness_class,
        review_interval_days=body.review_interval_days,
        last_verified_at=None,
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=json.loads(source.model_dump_json()),
    )


@router.post("/sources/{source_id}/fetch", status_code=status.HTTP_202_ACCEPTED)
def fetch_source(
    source_id: str,
    services: ServicesDep,
    auth: Annotated[CuratorAuth, Depends(require_scope("sources:write"))],
    idempotency_key: IdempotencyKeyHeader = None,
) -> dict:
    """Trigger a fetch job for a source."""
    job_id = str(uuid.uuid4())
    return {"job_id": job_id, "status": "queued"}


# --- draft creation ----------------------------------------------------------

@router.post("/source-snapshots/{snapshot_id}/draft", status_code=status.HTTP_202_ACCEPTED)
def create_draft_from_snapshot(
    snapshot_id: str,
    services: ServicesDep,
    auth: Annotated[CuratorAuth, Depends(require_scope("rules:write"))],
    idempotency_key: IdempotencyKeyHeader = None,
) -> dict:
    """Create a rule draft from a snapshot (optionally AI-assisted)."""
    draft_id = str(uuid.uuid4())
    return {"draft_id": draft_id, "status": "draft"}


# --- rule review -------------------------------------------------------------

@router.post("/rule-versions/{rule_version_id}/review")
def review_rule_version(
    rule_version_id: str,
    body: RuleVersionReview,
    services: ServicesDep,
    auth: Annotated[CuratorAuth, Depends(require_scope("rules:review"))],
    idempotency_key: IdempotencyKeyHeader = None,
) -> RuleVersionStatus:
    """Submit a review for a rule version."""
    return RuleVersionStatus(
        rule_version_id=rule_version_id,
        status="in_review",
        reviews_required=2,
        reviews_received=1,
    )


# --- bundle publish / rollback ------------------------------------------------

@router.post("/bundles/{bundle_id}/publish")
def publish_bundle(
    bundle_id: str,
    body: PublishBundleRequest,
    services: ServicesDep,
    auth: Annotated[CuratorAuth, Depends(require_scope("rules:publish"))],
    idempotency_key: IdempotencyKeyHeader = None,
) -> BundlePublication:
    """Publish a rule bundle atomically."""
    return BundlePublication(
        publication_id=str(uuid.uuid4()),
        bundle_id=bundle_id,
        bundle_hash=f"sha256:{'0' * 64}",
        channel=body.channel,
        published_at=datetime.now(UTC),
    )


@router.post("/bundles/{bundle_id}/rollback")
def rollback_bundle(
    bundle_id: str,
    body: RollbackBundleRequest,
    services: ServicesDep,
    auth: Annotated[CuratorAuth, Depends(require_scope("rules:publish"))],
    idempotency_key: IdempotencyKeyHeader = None,
) -> BundlePublication:
    """Rollback to a previous bundle publication."""
    return BundlePublication(
        publication_id=str(uuid.uuid4()),
        bundle_id=bundle_id,
        bundle_hash=f"sha256:{'0' * 64}",
        channel="production",
        published_at=datetime.now(UTC),
    )
