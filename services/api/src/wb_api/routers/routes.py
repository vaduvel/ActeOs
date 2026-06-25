"""Stateless route resolution endpoint.

POST /v1/routes/resolve evaluates a route without persisting anything, so a
client can preview the outcome of a set of facts. It still requires a device
header for rate-attribution and consistency with the rest of the API.
"""
from __future__ import annotations

from fastapi import APIRouter

from ..deps import DeviceIdDep, ServicesDep
from ..schemas import RouteResolution, RouteResolveRequest

router = APIRouter(prefix="/v1/routes", tags=["routes"])


@router.post("/resolve", response_model=RouteResolution)
def resolve_route(
    body: RouteResolveRequest,
    services: ServicesDep,
    device_id: DeviceIdDep,
) -> RouteResolution:
    return services.resolver.resolve(body)
