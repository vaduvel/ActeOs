"""Ranking signals and thresholds (contracts/intent_ranking.yaml, docs/03A §9).

Defaults below MUST stay in sync with contracts/intent_ranking.yaml. The
``from_dict`` loader lets callers hydrate the config straight from that file so
the contract remains the single source of truth at runtime.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class RankingConfig:
    # signal weights
    exact_title: float = 1.0
    exact_alias: float = 0.96
    prefix_title_or_alias: float = 0.82
    lexical_token_coverage: float = 0.55
    category_hint_bonus: float = 0.12
    jurisdiction_available_bonus: float = 0.1
    local_recent_or_favorite_max_bonus: float = 0.06
    aggregate_popularity_max_bonus: float = 0.04
    negative_alias_penalty: float = -0.4
    # thresholds
    high_min_score: float = 0.82
    high_min_margin: float = 0.08
    ambiguous_min_score: float = 0.55
    no_result_below: float = 0.35
    max_candidates: int = 3
    always_require_user_confirmation: bool = True

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "RankingConfig":
        signals = data.get("signals", {}) or {}
        thresholds = data.get("thresholds", {}) or {}
        merged: dict[str, Any] = {}
        for f in (
            "exact_title",
            "exact_alias",
            "prefix_title_or_alias",
            "lexical_token_coverage",
            "category_hint_bonus",
            "jurisdiction_available_bonus",
            "local_recent_or_favorite_max_bonus",
            "aggregate_popularity_max_bonus",
            "negative_alias_penalty",
        ):
            if f in signals:
                merged[f] = signals[f]
        for f in (
            "high_min_score",
            "high_min_margin",
            "ambiguous_min_score",
            "no_result_below",
            "max_candidates",
            "always_require_user_confirmation",
        ):
            if f in thresholds:
                merged[f] = thresholds[f]
        return cls(**merged)
