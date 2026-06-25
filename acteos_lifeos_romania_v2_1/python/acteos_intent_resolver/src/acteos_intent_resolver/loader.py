"""File loaders for the taxonomy and ranking config (PyYAML, lazy).

Kept out of the package __init__ so the pure pipeline imports without any
third-party dependency. Install the ``yaml`` extra to use these.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .catalog import IntentCatalog
from .normalize import RomanianNormalizer
from .ranking import RankingConfig

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "PyYAML is required for the resolver loaders: pip install 'acteos-intent-resolver[yaml]'"
    ) from exc


def _load_yaml(path: Any) -> Any:
    with Path(path).open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_ranking_config(path: Any) -> RankingConfig:
    return RankingConfig.from_dict(_load_yaml(path) or {})


def build_normalizer(ranking_path: Any | None = None) -> RomanianNormalizer:
    if ranking_path is None:
        return RomanianNormalizer()
    data = _load_yaml(ranking_path) or {}
    norm = data.get("normalization", {}) or {}
    kwargs: dict[str, Any] = {}
    if "min_query_chars" in norm:
        kwargs["min_query_chars"] = int(norm["min_query_chars"])
    approved = norm.get("approved_short_tokens")
    if approved:
        base = set(RomanianNormalizer().approved_short_tokens)
        kwargs["approved_short_tokens"] = frozenset(base | {str(t).casefold() for t in approved})
    return RomanianNormalizer(**kwargs)


def load_catalog(
    taxonomy_path: Any,
    *,
    ranking_path: Any | None = None,
    index_version: str = "1",
) -> IntentCatalog:
    normalizer = build_normalizer(ranking_path)
    return IntentCatalog.from_taxonomy(_load_yaml(taxonomy_path) or {}, normalizer=normalizer, index_version=index_version)
