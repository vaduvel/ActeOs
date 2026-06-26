"""Tests for the deterministic resolution projection (authoring.resolution)."""
from __future__ import annotations

from acteos_rule_engine import ENGINE_VERSION
from acteos_rule_engine.authoring.orchestrator import resolve_event
from acteos_rule_engine.authoring.resolution import (
    aggregate_status,
    build_resolution,
    facts_hash,
)


def _ruleset(event_id, rules):
    return {"event_type_id": event_id, "status": "draft", "rules": rules}


PARENT = _ruleset(
    "life.parent",
    [
        {
            "id": "rule.p.base",
            "canonical_rule_id": "parent.base",
            "event_type_id": "life.parent",
            "when": {"op": "const", "value": True},
            "effects": [
                {"type": "include_step", "step_id": "step_a"},
                {"type": "include_requirement", "requirement_id": "req_a"},
                {"type": "trigger_child_event", "event_type_id": "life.child"},
            ],
        },
        {
            "id": "rule.p.adult_only",
            "canonical_rule_id": "parent.adult_only",
            "event_type_id": "life.parent",
            "when": {"op": "gte", "field": "age", "value": 18},
            "effects": [{"type": "emit_advice", "message_ro": "ok", "tag": "adult"}],
        },
    ],
)

CHILD = _ruleset(
    "life.child",
    [
        {
            "id": "rule.c.base",
            "canonical_rule_id": "child.base",
            "event_type_id": "life.child",
            "when": {"op": "const", "value": True},
            "effects": [{"type": "include_step", "step_id": "step_c"}],
        }
    ],
)

RULESETS = {"life.parent": PARENT, "life.child": CHILD}


def test_facts_hash_is_order_independent():
    assert facts_hash({"a": 1, "b": 2}) == facts_hash({"b": 2, "a": 1})
    assert len(facts_hash({})) == 64


def test_aggregate_status_picks_most_severe():
    assert aggregate_status(["resolved", "needs_facts", "blocked"]) == "needs_facts"
    assert aggregate_status(["resolved", "resolved"]) == "resolved"
    assert aggregate_status([]) == "resolved"


def test_build_resolution_aggregates_tree():
    facts = {"age": 30}
    node = resolve_event("life.parent", RULESETS, facts)
    res = build_resolution(
        node,
        RULESETS,
        facts,
        ruleset_version="test-1",
        intent_type_id="ro.intent.x",
        reference_date="2026-06-25",
    )

    assert res["status"] == "resolved"
    assert res["engine_version"] == ENGINE_VERSION
    assert [e["event_type_id"] for e in res["events"]] == ["life.parent", "life.child"]

    trace = res["resolution_trace"]
    assert trace["included_rule_ids"] == sorted(["rule.p.base", "rule.p.adult_only", "rule.c.base"])
    assert trace["excluded_rule_ids"] == []
    assert trace["engine_version"] == ENGINE_VERSION
    assert trace["root_event_type_id"] == "life.parent"
    assert trace["event_type_ids"] == ["life.parent", "life.child"]
    assert trace["intent_type_id"] == "ro.intent.x"
    assert trace["reference_date"] == "2026-06-25"
    assert trace["has_unknown_events"] is False


def test_build_resolution_excludes_unfired_rules():
    facts = {"age": 10}
    node = resolve_event("life.parent", RULESETS, facts)
    res = build_resolution(node, RULESETS, facts, ruleset_version="test-1")
    trace = res["resolution_trace"]
    assert "rule.p.adult_only" not in trace["included_rule_ids"]
    assert "rule.p.adult_only" in trace["excluded_rule_ids"]
    assert "rule.p.base" in trace["included_rule_ids"]


def test_build_resolution_needs_facts_when_required_fact_missing():
    node = resolve_event("life.parent", RULESETS, {})
    res = build_resolution(node, RULESETS, {}, ruleset_version="test-1")
    assert res["status"] == "needs_facts"
    parent = res["events"][0]
    assert "age" in parent["missing_facts"]
