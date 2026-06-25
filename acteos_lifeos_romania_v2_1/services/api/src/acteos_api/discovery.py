"""Discovery service + router: wires the deterministic Intent Resolver.

The service is read-only and stateless beyond the loaded catalog. It serves only
published intents (production_status == active). Jurisdiction-scoped availability
beyond the catalog is a future data concern; jurisdiction_hint is accepted but
not yet mapped to per-intent availability sets.
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

import yaml
from fastapi import APIRouter, Depends, Query, Request

from acteos_intent_resolver import IntentCatalog, IntentResolver, RankingConfig, RomanianNormalizer
from acteos_intent_resolver.catalog import IntentRecord
from acteos_intent_resolver.resolver import RESOLVER_VERSION, Candidate, TOO_SHORT

from .schemas import (
    CategoryListResponse,
    CategorySummary,
    DiscoveryHomeResponse,
    IntentCandidate,
    IntentListResponse,
    IntentSummary,
    PageInfo,
    ResolveIntentQueryRequest,
    ResolveIntentQueryResponse,
)

_PACK_ROOT = Path(__file__).resolve().parents[4]
_AVAILABILITY_MESSAGE = "Acest traseu este în pregătire și nu este încă disponibil."


class DiscoveryError(Exception):
    """Domain error mapped to an ErrorResponse by the app exception handler."""

    def __init__(self, status_code: int, code: str, message: str, retryable: bool = False):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.retryable = retryable


def _taxonomy_path() -> str:
    return os.environ.get("ACTEOS_TAXONOMY_PATH", str(_PACK_ROOT / "data" / "intent_taxonomy.yaml"))


def _ranking_path() -> str:
    return os.environ.get("ACTEOS_RANKING_PATH", str(_PACK_ROOT / "contracts" / "intent_ranking.yaml"))


def _normalizer_from_ranking(raw: Mapping[str, Any]) -> RomanianNormalizer:
    norm = (raw or {}).get("normalization", {}) or {}
    kwargs: dict[str, Any] = {}
    if "min_query_chars" in norm:
        kwargs["min_query_chars"] = int(norm["min_query_chars"])
    approved = norm.get("approved_short_tokens")
    if approved:
        base = set(RomanianNormalizer().approved_short_tokens)
        kwargs["approved_short_tokens"] = frozenset(base | {str(t).casefold() for t in approved})
    return RomanianNormalizer(**kwargs)


class DiscoveryService:
    def __init__(
        self,
        taxonomy: Mapping[str, Any],
        config: RankingConfig,
        normalizer: RomanianNormalizer,
    ) -> None:
        index_version = str(taxonomy.get("schema_version", "1"))
        self.catalog = IntentCatalog.from_taxonomy(
            taxonomy, normalizer=normalizer, index_version=index_version
        )
        self.resolver = IntentResolver(self.catalog, config)
        self.normalizer = normalizer
        self.categories_raw = list(taxonomy.get("categories", []) or [])
        self.catalog_version = self.catalog.catalog_version
        self._by_id: dict[str, IntentRecord] = {r.id: r for r in self.catalog.records}

    @classmethod
    def from_paths(cls, taxonomy_path: str, ranking_path: str) -> "DiscoveryService":
        taxonomy = yaml.safe_load(Path(taxonomy_path).read_text(encoding="utf-8")) or {}
        ranking_raw = yaml.safe_load(Path(ranking_path).read_text(encoding="utf-8")) or {}
        return cls(taxonomy, RankingConfig.from_dict(ranking_raw), _normalizer_from_ranking(ranking_raw))

    # -- mapping -----------------------------------------------------------
    def _summary(self, record: IntentRecord) -> IntentSummary:
        available = record.is_active
        return IntentSummary(
            id=record.id,
            category_id=record.category_id,
            kind=record.kind,  # type: ignore[arg-type]
            title_ro=record.title_ro,
            outcome_ro=record.outcome_ro,
            production_status=record.production_status,
            available=available,
            availability_message_ro=None if available else _AVAILABILITY_MESSAGE,
            release_wave=record.release_wave,
        )

    def _candidate(self, c: Candidate) -> IntentCandidate:
        return IntentCandidate(
            intent=self._summary(self._by_id[c.intent_type_id]),
            score=c.score,
            match_mode=c.match_mode,  # type: ignore[arg-type]
            requires_confirmation=True,
            matched_alias=c.matched_alias,
        )

    # -- endpoints ---------------------------------------------------------
    def _active_category_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for r in self.catalog.records:
            if r.is_active:
                counts[r.category_id] = counts.get(r.category_id, 0) + 1
        return counts

    def categories(self, jurisdiction_id: str | None = None) -> CategoryListResponse:
        counts = self._active_category_counts()
        items: list[CategorySummary] = []
        for c in sorted(self.categories_raw, key=lambda x: x.get("order", 0)):
            cid = c.get("id", "")
            count = counts.get(cid, 0)
            if count <= 0:
                continue  # only categories with >=1 available intent (openapi/03A)
            items.append(
                CategorySummary(
                    id=cid,
                    title_ro=c.get("title_ro", cid),
                    icon_key=c.get("icon_key"),
                    intent_count=count,
                    order=int(c.get("order", 0)),
                )
            )
        return CategoryListResponse(items=items, catalog_version=self.catalog_version)

    def home(self, jurisdiction_id: str | None = None) -> DiscoveryHomeResponse:
        quick = [self._summary(r) for r in self.catalog.records if r.is_active][:8]
        return DiscoveryHomeResponse(
            headline_ro="Ce vrei să rezolvi?",
            search_placeholder_ro="Caută: buletin, mașină, pașaport, certificat…",
            quick_actions=quick,
            categories=self.categories(jurisdiction_id).items,
            catalog_version=self.catalog_version,
            resolver_version=RESOLVER_VERSION,
        )

    def list_intents(
        self,
        *,
        query: str | None = None,
        category_id: str | None = None,
        jurisdiction_id: str | None = None,
        cursor: str | None = None,
        limit: int = 20,
    ) -> IntentListResponse:
        records = [r for r in self.catalog.records if r.is_active]
        if category_id:
            records = [r for r in records if r.category_id == category_id]
        if query and query.strip():
            records = self._search(records, query)
        else:
            records = sorted(records, key=lambda r: r.id)
        offset = int(cursor) if cursor and cursor.isdigit() else 0
        window = records[offset : offset + limit]
        has_more = offset + limit < len(records)
        return IntentListResponse(
            items=[self._summary(r) for r in window],
            page=PageInfo(next_cursor=str(offset + limit) if has_more else None, has_more=has_more),
            catalog_version=self.catalog_version,
        )

    def _search(self, records: list[IntentRecord], query: str) -> list[IntentRecord]:
        qkey = self.normalizer.key(query)
        qtok = self.normalizer.token_set(query)
        scored: list[tuple[float, IntentRecord]] = []
        for r in records:
            if qkey and (r.norm_title == qkey or qkey in r.norm_aliases):
                s = 2.0
            elif qkey and any(k.startswith(qkey) for k in (r.norm_title, *r.norm_aliases) if k):
                s = 1.5
            elif qtok and (qtok & r.token_set):
                s = len(qtok & r.token_set) / len(qtok)
            else:
                s = 0.0
            if s > 0:
                scored.append((s, r))
        scored.sort(key=lambda x: (-x[0], x[1].id))
        return [r for _, r in scored]

    def resolve(self, req: ResolveIntentQueryRequest, request_id: str) -> ResolveIntentQueryResponse:
        result = self.resolver.resolve(
            req.query,
            category_hint=req.category_hint,
            allow_semantic_fallback=req.allow_semantic_fallback,
            request_id=request_id,
        )
        if result.resolution_state == TOO_SHORT:
            raise DiscoveryError(422, "INTENT_QUERY_TOO_SHORT", "Query prea scurt pentru căutare.")
        return ResolveIntentQueryResponse(
            resolution_state=result.resolution_state,  # type: ignore[arg-type]
            candidates=[self._candidate(c) for c in result.candidates],
            catalog_version=result.catalog_version,
            resolver_version=result.resolver_version,
            normalization_version=result.normalization_version,
            fallback_used=result.fallback_used,
            request_id=request_id,
        )

    def get_intent(self, intent_type_id: str, jurisdiction_id: str | None = None) -> IntentSummary:
        record = self._by_id.get(intent_type_id)
        if record is None:
            raise DiscoveryError(404, "INTENT_NOT_FOUND", "Intentul nu există în catalog.")
        return self._summary(record)


@lru_cache(maxsize=1)
def get_discovery_service() -> DiscoveryService:
    return DiscoveryService.from_paths(_taxonomy_path(), _ranking_path())


router = APIRouter(prefix="/v1", tags=["Discovery"])


@router.get("/discovery/home", response_model=DiscoveryHomeResponse)
def discovery_home(
    jurisdiction_id: str | None = None,
    svc: DiscoveryService = Depends(get_discovery_service),
) -> DiscoveryHomeResponse:
    return svc.home(jurisdiction_id)


@router.get("/categories", response_model=CategoryListResponse)
def list_categories(
    jurisdiction_id: str | None = None,
    svc: DiscoveryService = Depends(get_discovery_service),
) -> CategoryListResponse:
    return svc.categories(jurisdiction_id)


@router.get("/intents", response_model=IntentListResponse)
def list_intents(
    query: str | None = Query(default=None, max_length=200),
    category_id: str | None = None,
    jurisdiction_id: str | None = None,
    cursor: str | None = None,
    limit: int = Query(default=20, ge=1, le=50),
    svc: DiscoveryService = Depends(get_discovery_service),
) -> IntentListResponse:
    return svc.list_intents(
        query=query,
        category_id=category_id,
        jurisdiction_id=jurisdiction_id,
        cursor=cursor,
        limit=limit,
    )


@router.post("/intents/resolve-query", response_model=ResolveIntentQueryResponse)
def resolve_intent_query(
    req: ResolveIntentQueryRequest,
    request: Request,
    svc: DiscoveryService = Depends(get_discovery_service),
) -> ResolveIntentQueryResponse:
    request_id = getattr(request.state, "request_id", "")
    return svc.resolve(req, request_id)


@router.get("/intents/{intent_type_id}", response_model=IntentSummary)
def get_intent(
    intent_type_id: str,
    jurisdiction_id: str | None = None,
    svc: DiscoveryService = Depends(get_discovery_service),
) -> IntentSummary:
    return svc.get_intent(intent_type_id, jurisdiction_id)
