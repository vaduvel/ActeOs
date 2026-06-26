"""Project a resolved EventNode tree into the journey resolution_trace contract.

Pure and deterministic (no IO, clock, or network). Consumes the EventNode tree
produced by ``orchestrator.resolve_event`` plus the rulesets it was evaluated
against, and produces:

  * a stable ``facts_hash`` over the citizen facts,
  * the ``resolution_trace`` required by
    contracts/jsonschema/journey.schema.json (facts_hash, engine_version,
    included_rule_ids, excluded_rule_ids), and
  * a per-event structural projection of everything the engine computed
    (steps, requirements, obligations, channels, advice, warnings,
    confirmations, conflicts, blocks, deadlines, child events, missing facts).

It deliberately does NOT materialize step/requirement *content* (title_ro,
instruction_ro): that requires published step_templates / requirement_templates
(content.step_templates / content.requirement_templates), which are a separate
content concern. This projection is faithful to exactly what the governed
ruleset encodes -- semantic ids plus authored messages -- and nothing more.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable, Mapping

from .. import ENGINE_VERSION
from ..dates import parse_date
from .orchestrator import EventNode

# Aggregate status precedence across the event tree (most severe first), aligned
# with ruleset.evaluate_ruleset's single-event precedence.
_STATUS_PRECEDENCE = (
    "needs_facts",
    "conflicting",
    "blocked",
    "needs_confirmation",
    "resolved",
)
_STATUS_RANK = {status: index for index, status in enumerate(_STATUS_PRECEDENCE)}


def facts_hash(facts: Mapping[str, Any]) -> str:
    """Stable SHA-256 over the citizen facts.

    Canonicalized with sorted keys and compact separators so identical facts
    always hash identically regardless of input ordering. Non-JSON-native
    values (dates, Decimals) fall back to their string form.
    """
    canonical = json.dumps(
        facts,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _rule_ids(ruleset: Mapping[str, Any] | None) -> list[str]:
    if not ruleset:
        return []
    return [r.get("id") for r in ruleset.get("rules", []) if r.get("id")]


def _event_projection(node: EventNode, ruleset: Mapping[str, Any] | None) -> dict:
    route = node.route
    fired = list(route.fired_rule_ids)
    fired_set = set(fired)
    excluded = [rid for rid in _rule_ids(ruleset) if rid not in fired_set]
    return {
        "event_type_id": node.event_type_id,
        "status": route.status,
        "included_steps": list(route.included_steps),
        "requirements": list(route.requirements),
        "obligations": dict(route.obligations),
        "channels": list(route.channels),
        "advice": [dict(a) for a in route.advice],
        "warnings": [dict(w) for w in route.warnings],
        "confirmations": list(route.confirmations),
        "conflicts": list(route.conflicts),
        "blocks": [dict(b) for b in route.blocks],
        "deadlines": {k: dict(v) for k, v in route.deadlines.items()},
        "overdue_steps": list(route.overdue_steps),
        "child_events": list(route.child_events),
        "missing_facts": list(route.missing_facts),
        "overridden_rules": list(route.overridden_rules),
        "fired_rule_ids": fired,
        "excluded_rule_ids": excluded,
    }


def aggregate_status(statuses: Iterable[str]) -> str:
    """Most severe status across an event tree, defaulting to ``resolved``."""
    ranked = [_STATUS_RANK[s] for s in statuses if s in _STATUS_RANK]
    if not ranked:
        return "resolved"
    return _STATUS_PRECEDENCE[min(ranked)]


def build_resolution(
    root: EventNode,
    rulesets_by_event: Mapping[str, Any],
    facts: Mapping[str, Any],
    *,
    ruleset_version: str,
    intent_type_id: str | None = None,
    reference_date: Any = None,
) -> dict:
    """Build the contract-shaped resolution for a resolved EventNode tree."""
    nodes = root.flatten()
    events = [
        _event_projection(node, rulesets_by_event.get(node.event_type_id)) for node in nodes
    ]

    included: list[str] = []
    for event in events:
        for rid in event["fired_rule_ids"]:
            if rid not in included:
                included.append(rid)
    fired_global = set(included)

    excluded: list[str] = []
    for event in events:
        for rid in event["excluded_rule_ids"]:
            if rid not in fired_global and rid not in excluded:
                excluded.append(rid)

    ref = parse_date(reference_date)
    status = aggregate_status(event["status"] for event in events)
    fh = facts_hash(facts)

    trace: dict[str, Any] = {
        "facts_hash": fh,
        "engine_version": ENGINE_VERSION,
        "included_rule_ids": sorted(included),
        "excluded_rule_ids": sorted(excluded),
        "ruleset_version": ruleset_version,
        "reference_date": ref.isoformat() if ref is not None else None,
        "root_event_type_id": root.event_type_id,
        "event_type_ids": root.event_ids(),
        "has_unknown_events": any(e["status"] == "unknown_event" for e in events),
    }
    if intent_type_id:
        trace["intent_type_id"] = intent_type_id

    return {
        "status": status,
        "facts_hash": fh,
        "engine_version": ENGINE_VERSION,
        "ruleset_version": ruleset_version,
        "events": events,
        "resolution_trace": trace,
    }
