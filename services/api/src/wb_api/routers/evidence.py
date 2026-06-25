"""Evidence endpoint: resolve a source claim to its underlying source.

This is how the client renders "why" behind every requirement: each claim id
attached to a step/requirement can be expanded into the citable source.
"""
from __future__ import annotations

from fastapi import APIRouter

from ..deps import DeviceIdDep, ServicesDep
from ..schemas import SourceClaim

router = APIRouter(prefix="/v1/evidence", tags=["evidence"])


@router.get("/{claim_id}", response_model=SourceClaim)
def get_claim(claim_id: str, services: ServicesDep, device_id: DeviceIdDep) -> SourceClaim:
    return services.evidence.get_claim(claim_id)
