"""Journey lifecycle endpoints.

Journeys are device-scoped, encrypted-at-rest records of a citizen's progress
through a bureaucratic route. Sensitive writes (create, recalculate, document
analysis) honour the Idempotency-Key header so retries never duplicate work.
Ownership is enforced in the service layer via a device-scoped lookup that does
not distinguish "not found" from "not yours" (anti-IDOR).
"""
from __future__ import annotations

import json

from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from ..deps import (
    DeviceIdDep,
    IdempotencyKeyHeader,
    PageDep,
    ServicesDep,
    run_idempotent,
)
from ..schemas import (
    CreateJourneyRequest,
    DocumentAnalysis,
    DocumentAnalysisInput,
    FactsPatch,
    Journey,
    JourneySummary,
    RecalculateRequest,
    RecalculationResult,
    RequirementState,
    RequirementUpdate,
)

router = APIRouter(prefix="/v1/journeys", tags=["journeys"])


@router.post("", response_model=Journey, status_code=status.HTTP_201_CREATED)
def create_journey(
    body: CreateJourneyRequest,
    services: ServicesDep,
    device_id: DeviceIdDep,
    idempotency_key: IdempotencyKeyHeader = None,
) -> Response:
    payload = {"device": device_id, "body": json.loads(body.model_dump_json())}
    out, code, _ = run_idempotent(
        services, scope="journey.create", key=idempotency_key, payload=payload,
        producer=lambda: services.journeys.create(device_id=device_id, req=body),
        success_status=status.HTTP_201_CREATED,
    )
    return JSONResponse(status_code=code, content=out)


@router.get("", response_model=list[JourneySummary])
def list_journeys(services: ServicesDep, device_id: DeviceIdDep, page: PageDep) -> list[JourneySummary]:
    return services.journeys.list(device_id=device_id, limit=page.limit, offset=page.offset)


@router.get("/{journey_id}", response_model=Journey)
def get_journey(journey_id: str, services: ServicesDep, device_id: DeviceIdDep) -> Journey:
    return services.journeys.get(device_id=device_id, journey_id=journey_id)


@router.delete("/{journey_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_journey(journey_id: str, services: ServicesDep, device_id: DeviceIdDep) -> Response:
    services.journeys.delete(device_id=device_id, journey_id=journey_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{journey_id}/facts", response_model=Journey)
def patch_facts(journey_id: str, body: FactsPatch, services: ServicesDep, device_id: DeviceIdDep) -> Journey:
    return services.journeys.patch_facts(device_id=device_id, journey_id=journey_id, facts=body.facts)


@router.post("/{journey_id}/recalculate", response_model=RecalculationResult)
def recalculate(
    journey_id: str,
    body: RecalculateRequest,
    services: ServicesDep,
    device_id: DeviceIdDep,
    idempotency_key: IdempotencyKeyHeader = None,
) -> Response:
    payload = {"device": device_id, "journey": journey_id, "body": json.loads(body.model_dump_json())}
    out, code, _ = run_idempotent(
        services, scope="journey.recalculate", key=idempotency_key, payload=payload,
        producer=lambda: services.journeys.recalculate(device_id=device_id, journey_id=journey_id, req=body),
        success_status=status.HTTP_200_OK,
    )
    return JSONResponse(status_code=code, content=out)


@router.patch("/{journey_id}/requirements/{requirement_id}", response_model=RequirementState)
def update_requirement(
    journey_id: str,
    requirement_id: str,
    body: RequirementUpdate,
    services: ServicesDep,
    device_id: DeviceIdDep,
) -> RequirementState:
    return services.journeys.update_requirement(
        device_id=device_id, journey_id=journey_id, requirement_id=requirement_id, body=body,
    )


@router.post("/{journey_id}/document-analyses", response_model=DocumentAnalysis, status_code=status.HTTP_201_CREATED)
def add_document_analysis(
    journey_id: str,
    body: DocumentAnalysisInput,
    services: ServicesDep,
    device_id: DeviceIdDep,
    idempotency_key: IdempotencyKeyHeader = None,
) -> Response:
    payload = {"device": device_id, "journey": journey_id, "body": json.loads(body.model_dump_json())}
    out, code, _ = run_idempotent(
        services, scope="document.analysis", key=idempotency_key, payload=payload,
        producer=lambda: services.journeys.add_document_analysis(device_id=device_id, journey_id=journey_id, body=body),
        success_status=status.HTTP_201_CREATED,
    )
    return JSONResponse(status_code=code, content=out)
