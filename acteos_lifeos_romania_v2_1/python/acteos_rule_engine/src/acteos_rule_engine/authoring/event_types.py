"""Compile the governed life-event catalog into content.life_event_types rows.

The catalog (``data/r1_event_catalog.yaml`` shape) is a mapping with a top-level
``schema_version`` and a ``waves`` mapping of ``wave -> [event dict]``. Each event
is the FK parent that ``content.rule_revisions.event_type_id`` points at.

Id canonicalization: the catalog keys events as ``ro.life.<event>`` while the
governed ``rules.yaml`` (and therefore ``content.rule_revisions.event_type_id``)
use the engine-internal ``life.<event>`` form. We canonicalize to the
engine-internal form so the foreign key resolves.

Honesty: no data is fabricated. ``description_ro`` and ``parent_event_id`` are
left ``None`` when the catalog does not define them, and an event without a
``title_ro`` is skipped because that column is ``NOT NULL`` in the schema.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

CATALOG_SCHEMA_DEFAULT = "2.0.0"


def canonical_event_type_id(event_id: str) -> str:
    """Canonicalize a catalog event id to the engine-internal ``life.<x>`` form."""

    if event_id.startswith("ro.life."):
        return "life." + event_id[len("ro.life.") :]
    return event_id


@dataclass(frozen=True)
class EventTypeRecord:
    id: str
    category_id: str | None
    title_ro: str
    description_ro: str | None
    trigger_phrases_ro: list[str]
    parent_event_id: str | None
    release_wave: str | None
    research_status: str | None
    production_status: str | None
    schema_version: str

    def as_content_row(self) -> dict[str, Any]:
        # Exact column mapping for content.life_event_types.
        return {
            "id": self.id,
            "category_id": self.category_id,
            "title_ro": self.title_ro,
            "description_ro": self.description_ro,
            "trigger_phrases_ro": list(self.trigger_phrases_ro),
            "parent_event_id": self.parent_event_id,
            "release_wave": self.release_wave,
            "research_status": self.research_status,
            "production_status": self.production_status,
            "schema_version": self.schema_version,
        }


def _wave_in_scope(wave: str, scope: tuple[str, ...]) -> bool:
    if not scope:
        return True
    return any(wave == s or wave.startswith(s) for s in scope)


def compile_event_types(
    catalog: Mapping[str, Any],
    *,
    scope: Iterable[str] = ("R1",),
) -> list[EventTypeRecord]:
    """Compile the catalog into deterministic, scope-filtered event records."""

    scope_t = tuple(s for s in scope if isinstance(s, str))
    schema_version = str(catalog.get("schema_version") or CATALOG_SCHEMA_DEFAULT)
    waves = catalog.get("waves")

    items: list[tuple[str, Mapping[str, Any]]] = []
    if isinstance(waves, Mapping):
        for wave_name, events in waves.items():
            if not isinstance(events, list):
                continue
            for event in events:
                if isinstance(event, Mapping):
                    items.append((str(wave_name), event))

    records: dict[str, EventTypeRecord] = {}
    for wave_name, event in items:
        wave = str(event.get("release_wave") or wave_name)
        if not _wave_in_scope(wave, scope_t):
            continue
        raw_id = event.get("id")
        if not isinstance(raw_id, str):
            continue
        title = event.get("title_ro")
        if not isinstance(title, str) or not title:
            # title_ro is NOT NULL in content.life_event_types; skip unusable rows.
            continue
        canonical_id = canonical_event_type_id(raw_id)
        triggers = [t for t in (event.get("trigger_phrases_ro") or []) if isinstance(t, str)]
        records[canonical_id] = EventTypeRecord(
            id=canonical_id,
            category_id=event.get("category_id"),
            title_ro=title,
            description_ro=event.get("description_ro"),
            trigger_phrases_ro=triggers,
            parent_event_id=event.get("parent_event_id"),
            release_wave=wave,
            research_status=event.get("research_status"),
            production_status=event.get("production_status"),
            schema_version=schema_version,
        )
    return sorted(records.values(), key=lambda r: r.id)
