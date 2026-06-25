"""In-memory discovery catalog built from data/intent_taxonomy.yaml.

The catalog is derived from the published taxonomy and pre-normalizes titles,
aliases and negative aliases against a versioned normalizer so the resolver does
no per-query normalization of catalog data. It is not a source of truth: it can
be rebuilt deterministically from the signed/published catalog.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

from .normalize import RomanianNormalizer


@dataclass(frozen=True)
class IntentRecord:
    id: str
    category_id: str
    kind: str
    title_ro: str
    outcome_ro: str
    aliases_ro: tuple[str, ...] = ()
    negative_aliases_ro: tuple[str, ...] = ()
    linked_event_ids: tuple[str, ...] = ()
    journey_template_id: str | None = None
    jurisdiction_scope: str = "mixed"
    release_wave: str | None = None
    research_status: str | None = None
    production_status: str = "not_available"
    availability_policy: str | None = None
    withdrawn: bool = False
    search_boost: float = 1.0
    catalog_version: str | None = None
    # pre-normalized lookup fields
    norm_title: str = ""
    norm_aliases: tuple[str, ...] = ()
    token_set: frozenset[str] = field(default_factory=frozenset)
    neg_keys: tuple[str, ...] = ()
    neg_token_sets: tuple[frozenset[str], ...] = ()

    @property
    def is_active(self) -> bool:
        return self.production_status == "active" and not self.withdrawn


def _build_record(raw: Mapping[str, Any], normalizer: RomanianNormalizer) -> IntentRecord:
    aliases = tuple(raw.get("aliases_ro", []) or [])
    negatives = tuple(raw.get("negative_aliases_ro", []) or [])
    title = raw.get("title_ro", "")
    token_set = normalizer.token_set(title)
    for alias in aliases:
        token_set |= normalizer.token_set(alias)
    return IntentRecord(
        id=raw["id"],
        category_id=raw.get("category_id", ""),
        kind=raw.get("kind", "direct_goal"),
        title_ro=title,
        outcome_ro=raw.get("outcome_ro", ""),
        aliases_ro=aliases,
        negative_aliases_ro=negatives,
        linked_event_ids=tuple(raw.get("linked_event_ids", []) or []),
        journey_template_id=raw.get("journey_template_id"),
        jurisdiction_scope=raw.get("jurisdiction_scope", "mixed"),
        release_wave=raw.get("release_wave"),
        research_status=raw.get("research_status"),
        production_status=raw.get("production_status", "not_available"),
        availability_policy=raw.get("availability_policy"),
        withdrawn=bool(raw.get("withdrawn", False)),
        search_boost=float(raw.get("search_boost", 1.0)),
        catalog_version=raw.get("catalog_version"),
        norm_title=normalizer.key(title),
        norm_aliases=tuple(normalizer.key(a) for a in aliases),
        token_set=token_set,
        neg_keys=tuple(normalizer.key(n) for n in negatives),
        neg_token_sets=tuple(normalizer.token_set(n) for n in negatives),
    )


@dataclass
class IntentCatalog:
    records: list[IntentRecord]
    catalog_version: str
    index_version: str
    normalizer: RomanianNormalizer

    @classmethod
    def from_taxonomy(
        cls,
        data: Mapping[str, Any],
        *,
        normalizer: RomanianNormalizer | None = None,
        index_version: str = "1",
        catalog_version: str | None = None,
    ) -> "IntentCatalog":
        nz = normalizer or RomanianNormalizer()
        records = [_build_record(raw, nz) for raw in data.get("intents", [])]
        version = catalog_version or data.get("schema_version") or "unknown"
        return cls(records=records, catalog_version=version, index_version=index_version, normalizer=nz)

    @classmethod
    def from_records(
        cls,
        records: Iterable[Mapping[str, Any]],
        *,
        normalizer: RomanianNormalizer | None = None,
        index_version: str = "1",
        catalog_version: str = "test",
    ) -> "IntentCatalog":
        nz = normalizer or RomanianNormalizer()
        built = [_build_record(r, nz) for r in records]
        return cls(records=built, catalog_version=catalog_version, index_version=index_version, normalizer=nz)

    def active(self) -> Sequence[IntentRecord]:
        return [r for r in self.records if r.is_active]
