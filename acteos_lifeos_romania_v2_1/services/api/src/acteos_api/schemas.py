"""Pydantic v2 response/request models for the discovery slice.

Mirror the component schemas in contracts/openapi.yaml. Field names and required
flags are kept faithful so the generated contract and the implementation agree.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

MatchMode = Literal["exact_title", "exact_alias", "prefix", "lexical", "semantic_fallback"]
ResolutionState = Literal["high", "ambiguous", "low", "no_result"]
IntentKind = Literal["direct_goal", "bundle_goal"]


class ErrorBody(BaseModel):
    code: str
    message: str
    details: dict | None = None
    request_id: str
    retryable: bool = False


class ErrorResponse(BaseModel):
    error: ErrorBody


class MessageResponse(BaseModel):
    message: str


class PageInfo(BaseModel):
    next_cursor: str | None = None
    has_more: bool


class CategorySummary(BaseModel):
    id: str
    title_ro: str
    icon_key: str | None = None
    intent_count: int = Field(ge=0)
    order: int = 0


class CategoryListResponse(BaseModel):
    items: list[CategorySummary]
    catalog_version: str


class IntentSummary(BaseModel):
    id: str
    category_id: str
    kind: IntentKind
    title_ro: str
    outcome_ro: str
    production_status: str
    available: bool
    availability_message_ro: str | None = None
    release_wave: str | None = None


class IntentListResponse(BaseModel):
    items: list[IntentSummary]
    page: PageInfo | None = None
    catalog_version: str


class ResolveIntentQueryRequest(BaseModel):
    query: str = Field(min_length=2, max_length=200)
    locale: Literal["ro-RO"]
    jurisdiction_hint: str | None = None
    category_hint: str | None = None
    client_catalog_version: str | None = None
    allow_semantic_fallback: bool = False


class IntentCandidate(BaseModel):
    intent: IntentSummary
    score: float = Field(ge=0)
    match_mode: MatchMode
    requires_confirmation: Literal[True] = True
    matched_alias: str | None = None


class ResolveIntentQueryResponse(BaseModel):
    resolution_state: ResolutionState
    candidates: list[IntentCandidate] = Field(max_length=3)
    catalog_version: str
    resolver_version: str
    normalization_version: str
    fallback_used: bool
    request_id: str


class DiscoveryHomeResponse(BaseModel):
    headline_ro: str
    search_placeholder_ro: str
    quick_actions: list[IntentSummary] = Field(max_length=8)
    categories: list[CategorySummary]
    catalog_version: str
    resolver_version: str | None = None
