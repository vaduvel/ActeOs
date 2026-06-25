"""ActeOS deterministic Intent Resolver (discovery layer).

Implements the pipeline described in docs/03A_DISCOVERY_INTENT_ATLAS.md (§7-§9)
and the weights/thresholds in contracts/intent_ranking.yaml. The core is pure:
no network, DB, clock or LLM. The optional semantic fallback is OFF by default
and can only return catalog IDs (not implemented in this core package).
"""
from __future__ import annotations

RESOLVER_VERSION = "2.1.0"

from .catalog import IntentCatalog, IntentRecord
from .normalize import NORMALIZATION_VERSION, RomanianNormalizer
from .ranking import RankingConfig
from .resolver import Candidate, IntentResolver, ResolveResult

__all__ = [
    "RESOLVER_VERSION",
    "NORMALIZATION_VERSION",
    "RomanianNormalizer",
    "RankingConfig",
    "IntentCatalog",
    "IntentRecord",
    "IntentResolver",
    "ResolveResult",
    "Candidate",
]
