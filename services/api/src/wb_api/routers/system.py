"""System endpoints: liveness and readiness probes.

Liveness answers "is the process up" (no dependencies). Readiness answers "can
it serve traffic" and therefore checks the database. Paths match the spec
exactly: ``/health/live`` and ``/health/ready`` (unversioned).
"""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Response

from ..config import get_settings
from ..deps import ServicesDep, check_db
from ..schemas import HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health/live", response_model=HealthResponse)
def live() -> HealthResponse:
    return HealthResponse(status="ok", version=get_settings().service_version, timestamp=datetime.now(timezone.utc))


@router.get("/health/ready", response_model=HealthResponse)
def ready(services: ServicesDep, response: Response) -> HealthResponse:
    db_ok = check_db(services.session)
    status = "ok" if db_ok else "degraded"
    if not db_ok:
        response.status_code = 503
    return HealthResponse(
        status=status, version=get_settings().service_version,
        timestamp=datetime.now(timezone.utc), checks={"database": "ok" if db_ok else "down"},
    )
