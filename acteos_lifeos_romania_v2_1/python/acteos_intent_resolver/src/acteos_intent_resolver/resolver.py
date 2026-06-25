"""Deterministic Intent Resolver pipeline (docs/03A §7-§9, 10A).

Pipeline: validate length/language -> normalize -> exact title/alias -> prefix
/ token lexical ranking -> availability/jurisdiction/production hard filters ->
negative-alias penalties -> dedupe -> max 3 candidates -> confidence thresholds
-> always require user confirmation.

The resolver only selects published canonical IDs; it never decides acts,
eligibility or deadlines. Semantic fallback is OFF by default and not part of
this pure core (it would only re-rank catalog IDs through the same gate).

Note on the jurisdiction bonus (docs/03A §9 "disponibil în jurisdicție +0.10"):
it is a *differentiator*, applied only when the caller supplies a jurisdiction
availability set AND the candidate is available there. When no jurisdiction
context is given we apply no bonus, so scores are not uniformly inflated and the
confidence thresholds stay meaningful.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

from .catalog import IntentCatalog, IntentRecord
from .normalize import NORMALIZATION_VERSION, RomanianNormalizer
from .ranking import RankingConfig

RESOLVER_VERSION = "2.1.0"

# resolution_state values surfaced to the API layer
HIGH = "high"
AMBIGUOUS = "ambiguous"
LOW = "low"
NO_RESULT = "no_result"
TOO_SHORT = "too_short"

# match_mode values (mirror OpenAPI IntentCandidate.match_mode)
MATCH_EXACT_TITLE = "exact_title"
MATCH_EXACT_ALIAS = "exact_alias"
MATCH_PREFIX = "prefix"
MATCH_LEXICAL = "lexical"


@dataclass(frozen=True)
class Candidate:
    intent_type_id: str
    title_ro: str
    outcome_ro: str
    category_id: str
    score: float
    match_mode: str
    matched_alias: str | None = None
    signals: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ResolveResult:
    resolution_state: str
    candidates: list[Candidate]
    resolver_version: str
    normalization_version: str
    catalog_version: str
    index_version: str
    needs_confirmation: bool = True
    fallback_used: bool = False
    error_code: str | None = None
    request_id: str | None = None


def _round(x: float) -> float:
    return round(x, 4)


class IntentResolver:
    def __init__(self, catalog: IntentCatalog, config: RankingConfig | None = None):
        self.catalog = catalog
        self.config = config or RankingConfig()
        self.normalizer: RomanianNormalizer = catalog.normalizer

    # -- scoring -----------------------------------------------------------
    def _score(
        self,
        record: IntentRecord,
        query_key: str,
        query_tokens: frozenset[str],
        *,
        category_hint: str | None,
        jurisdiction_available: bool,
        recent: bool,
        popularity: float,
    ) -> tuple[float, dict, str, str | None]:
        w = self.config
        signals: dict = {}
        base = 0.0
        match_mode = ""
        matched_alias: str | None = None

        if query_key and record.norm_title == query_key:
            base = w.exact_title
            match_mode = MATCH_EXACT_TITLE
            signals["exact_title"] = w.exact_title
        elif query_key and query_key in record.norm_aliases:
            base = w.exact_alias
            match_mode = MATCH_EXACT_ALIAS
            idx = record.norm_aliases.index(query_key)
            if idx < len(record.aliases_ro):
                matched_alias = record.aliases_ro[idx]
            signals["exact_alias"] = w.exact_alias
        else:
            coverage = 0.0
            if query_tokens:
                coverage = len(query_tokens & record.token_set) / len(query_tokens)
            lexical = w.lexical_token_coverage * coverage
            if coverage:
                signals["lexical_token_coverage"] = _round(lexical)
                match_mode = MATCH_LEXICAL
            prefix_hit = len(query_key) >= 2 and any(
                k != query_key and k.startswith(query_key)
                for k in (record.norm_title, *record.norm_aliases)
                if k
            )
            base = lexical
            if prefix_hit:
                base = max(base, w.prefix_title_or_alias)
                match_mode = MATCH_PREFIX
                signals["prefix_title_or_alias"] = w.prefix_title_or_alias

        bonus = 0.0
        if category_hint and category_hint == record.category_id:
            bonus += w.category_hint_bonus
            signals["category_hint_bonus"] = w.category_hint_bonus
        if jurisdiction_available:
            bonus += w.jurisdiction_available_bonus
            signals["jurisdiction_available_bonus"] = w.jurisdiction_available_bonus
        if recent:
            bonus += w.local_recent_or_favorite_max_bonus
            signals["local_recent_or_favorite_bonus"] = w.local_recent_or_favorite_max_bonus
        if popularity:
            pop = min(max(popularity, 0.0), w.aggregate_popularity_max_bonus)
            bonus += pop
            signals["aggregate_popularity_bonus"] = _round(pop)

        penalty = 0.0
        for nk, ntoks in zip(record.neg_keys, record.neg_token_sets):
            if (query_key and query_key == nk) or (ntoks and ntoks.issubset(query_tokens)):
                penalty = w.negative_alias_penalty
                signals["negative_alias_penalty"] = w.negative_alias_penalty
                break

        score = max(0.0, base * record.search_boost + bonus + penalty)
        return _round(score), signals, match_mode, matched_alias

    # -- state classification ---------------------------------------------
    def _classify(self, scored: Sequence[Candidate]) -> str:
        w = self.config
        if not scored:
            return NO_RESULT
        top = scored[0].score
        second = scored[1].score if len(scored) > 1 else 0.0
        margin = top - second
        if top < w.no_result_below:
            return NO_RESULT
        if top >= w.high_min_score and margin >= w.high_min_margin:
            return HIGH
        strong = [c for c in scored if c.score >= w.ambiguous_min_score]
        if len(strong) >= 2 and margin < w.high_min_margin:
            return AMBIGUOUS
        if top < w.ambiguous_min_score:
            return LOW
        # single decent match in [ambiguous_min_score, high_min_score): user must
        # still confirm; treat as low-confidence single suggestion.
        return LOW

    # -- public API --------------------------------------------------------
    def resolve(
        self,
        query: str,
        *,
        category_hint: str | None = None,
        jurisdiction_available_ids: set[str] | None = None,
        recent_ids: Sequence[str] = (),
        favorite_ids: Sequence[str] = (),
        popularity: Mapping[str, float] | None = None,
        apply_hard_filters: bool = True,
        allow_semantic_fallback: bool = False,
        request_id: str | None = None,
    ) -> ResolveResult:
        nz = self.normalizer
        meta = dict(
            resolver_version=RESOLVER_VERSION,
            normalization_version=NORMALIZATION_VERSION,
            catalog_version=self.catalog.catalog_version,
            index_version=self.catalog.index_version,
            request_id=request_id,
        )
        if nz.is_too_short(query):
            return ResolveResult(resolution_state=TOO_SHORT, candidates=[], error_code="INTENT_QUERY_TOO_SHORT", **meta)

        query_key = nz.key(query)
        query_tokens = nz.token_set(query)
        recent = set(recent_ids) | set(favorite_ids)
        pop = popularity or {}
        juris_known = jurisdiction_available_ids is not None

        scored: list[Candidate] = []
        for record in self.catalog.records:
            if apply_hard_filters and not record.is_active:
                continue
            in_jurisdiction = (not juris_known) or record.id in jurisdiction_available_ids
            if apply_hard_filters and juris_known and not in_jurisdiction:
                continue
            score, signals, match_mode, matched_alias = self._score(
                record,
                query_key,
                query_tokens,
                category_hint=category_hint,
                # bonus only when jurisdiction is actually known AND available
                jurisdiction_available=juris_known and in_jurisdiction,
                recent=record.id in recent,
                popularity=float(pop.get(record.id, 0.0)),
            )
            if score <= 0.0 or not match_mode:
                continue
            scored.append(
                Candidate(
                    intent_type_id=record.id,
                    title_ro=record.title_ro,
                    outcome_ro=record.outcome_ro,
                    category_id=record.category_id,
                    score=score,
                    match_mode=match_mode,
                    matched_alias=matched_alias,
                    signals=signals,
                )
            )

        scored.sort(key=lambda c: (-c.score, c.intent_type_id))
        top = scored[: self.config.max_candidates]
        state = self._classify(top)
        if state == NO_RESULT:
            return ResolveResult(resolution_state=NO_RESULT, candidates=[], error_code="INTENT_NOT_FOUND", **meta)
        return ResolveResult(
            resolution_state=state,
            candidates=top,
            needs_confirmation=True,
            fallback_used=False,
            **meta,
        )
