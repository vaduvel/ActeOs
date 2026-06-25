"""Aggregate all API routers in spec order."""
from __future__ import annotations

from fastapi import APIRouter

from . import catalog, evidence, feedback, journeys, routes, system

api_router = APIRouter()
api_router.include_router(system.router)
api_router.include_router(catalog.router)
api_router.include_router(routes.router)
api_router.include_router(journeys.router)
api_router.include_router(evidence.router)
api_router.include_router(feedback.router)

__all__ = ["api_router"]
