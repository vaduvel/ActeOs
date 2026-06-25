"""Feedback endpoint: queue a citizen-reported issue for human review.

Feedback bodies may contain free text, which is encrypted at rest. The endpoint
is idempotent and returns 202 (accepted, queued for review) because incidents
are triaged by curators out of band.
"""
from __future__ import annotations

import json

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..deps import (
    DeviceIdDep,
    IdempotencyKeyHeader,
    ServicesDep,
    run_idempotent,
)
from ..schemas import FeedbackAccepted, FeedbackInput

router = APIRouter(prefix="/v1/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackAccepted, status_code=status.HTTP_202_ACCEPTED)
def submit_feedback(
    body: FeedbackInput,
    services: ServicesDep,
    device_id: DeviceIdDep,
    idempotency_key: IdempotencyKeyHeader = None,
) -> JSONResponse:
    payload = {"device": device_id, "body": json.loads(body.model_dump_json())}
    out, code, _ = run_idempotent(
        services, scope="feedback.submit", key=idempotency_key, payload=payload,
        producer=lambda: services.feedback.submit(device_id=device_id, body=body),
        success_status=status.HTTP_202_ACCEPTED,
    )
    return JSONResponse(status_code=code, content=out)
