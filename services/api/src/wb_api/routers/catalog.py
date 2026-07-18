"""Catalog endpoints: discoverable intents and jurisdictions."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query

from ..deps import ServicesDep
from ..schemas import IntentSummary, Jurisdiction

router = APIRouter(prefix="/v1/catalog", tags=["catalog"])


@router.get("/intents")
def list_intents(
    services: ServicesDep,
    include_preview: Annotated[bool, Query()] = False,
) -> dict[str, list[IntentSummary]]:
    return {"items": services.catalog.list_intents(include_preview=include_preview)}


@router.get("/jurisdictions")
def list_jurisdictions(
    services: ServicesDep,
    type: Annotated[str | None, Query()] = None,
    parent_id: Annotated[str | None, Query()] = None,
    q: Annotated[str | None, Query(min_length=1, max_length=120)] = None,
) -> dict[str, list[Jurisdiction]]:
    return {"items": services.catalog.list_jurisdictions(kind=type, parent_id=parent_id, query=q)}
