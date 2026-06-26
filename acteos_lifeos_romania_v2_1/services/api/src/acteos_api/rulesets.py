"""Ruleset repository: load governed rulesets keyed by event_type_id.

The deterministic engine (acteos_rule_engine) consumes rulesets keyed by
event_type_id. Discovery intents reference events as ``ro.life.<event>`` while
the governed rules.yaml carry the engine-internal ``life.<event>`` id, and the
research pack stores each batch under a ``ro.life.<event>/`` directory. This
repository loads every batch's rules.yaml once and indexes it under all of those
aliases so a case can be resolved from any of those id forms.

Loading the research inbox directly is the pre-publication path. The published
path (signed content.rule_sets compiled from approved rule_revisions) is a later
slice; this repository is the seam where that swap happens.
"""
from __future__ import annotations

import hashlib
import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

import yaml

_PACK_ROOT = Path(__file__).resolve().parents[4]


def event_id_aliases(event_id: str) -> set[str]:
    """All id forms an event may be referenced by (``ro.life.x`` <-> ``life.x``)."""
    aliases = {event_id}
    if event_id.startswith("ro.life."):
        aliases.add("life." + event_id[len("ro.life.") :])
    elif event_id.startswith("life."):
        aliases.add("ro.life." + event_id[len("life.") :])
    elif event_id.startswith("ro."):
        aliases.add(event_id[len("ro.") :])
    return aliases


class RulesetRepository:
    """Indexes governed rulesets by every alias of their event_type_id."""

    def __init__(self, rulesets_by_event: Mapping[str, Mapping[str, Any]]):
        self._canonical_rulesets: dict[str, Mapping[str, Any]] = dict(rulesets_by_event)
        self._alias_to_canonical: dict[str, str] = {}
        self._engine_map: dict[str, Mapping[str, Any]] = {}
        for canonical, ruleset in self._canonical_rulesets.items():
            for alias in event_id_aliases(canonical):
                self._alias_to_canonical[alias] = canonical
                self._engine_map[alias] = ruleset

    @classmethod
    def from_mapping(cls, rulesets_by_event: Mapping[str, Mapping[str, Any]]) -> "RulesetRepository":
        return cls(rulesets_by_event)

    @classmethod
    def from_inbox(cls, inbox_dir: str | os.PathLike[str]) -> "RulesetRepository":
        base = Path(inbox_dir)
        rulesets: dict[str, Mapping[str, Any]] = {}
        if base.is_dir():
            for child in sorted(base.iterdir()):
                rules_path = child / "rules.yaml"
                if not (child.is_dir() and rules_path.exists()):
                    continue
                ruleset = yaml.safe_load(rules_path.read_text(encoding="utf-8")) or {}
                event_id = ruleset.get("event_type_id") or child.name
                rulesets[event_id] = ruleset
        return cls(rulesets)

    def canonical(self, event_id: str) -> str | None:
        return self._alias_to_canonical.get(event_id)

    def has(self, event_id: str) -> bool:
        return event_id in self._alias_to_canonical

    @property
    def engine_map(self) -> Mapping[str, Mapping[str, Any]]:
        return self._engine_map

    def content_version(self) -> str:
        """Deterministic version tag derived from the loaded ruleset content."""
        canonical = json.dumps(
            {k: self._canonical_rulesets[k] for k in sorted(self._canonical_rulesets)},
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=str,
        )
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:12]
        return f"inbox+{digest}"


def _inbox_path() -> str:
    return os.environ.get("ACTEOS_RESEARCH_INBOX", str(_PACK_ROOT / "research" / "inbox"))


@lru_cache(maxsize=1)
def get_ruleset_repository() -> RulesetRepository:
    return RulesetRepository.from_inbox(_inbox_path())
