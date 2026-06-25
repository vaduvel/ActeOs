import pytest

from wb_rule_engine.authoring.orchestrator import resolve_event

PARENT = {
    "event_type_id": "ro.life.child_born",
    "required_facts": [],
    "rules": [
        {
            "id": "r.parent",
            "canonical_rule_id": "child_born.root",
            "jurisdiction_ids": ["ro"],
            "effective_from": "2000-01-01",
            "when": {"op": "const", "value": True},
            "effects": [
                {"type": "include_step", "step_id": "start"},
                {"type": "trigger_child_event", "event_type_id": "ro.civil.birth.register"},
                {"type": "trigger_child_event", "event_type_id": "ro.benefits.state_allowance.request"},
            ],
        }
    ],
}
CHILD_REGISTER = {
    "event_type_id": "ro.civil.birth.register",
    "rules": [
        {
            "id": "r.register",
            "canonical_rule_id": "birth_register.root",
            "jurisdiction_ids": ["ro"],
            "effective_from": "2000-01-01",
            "when": {"op": "const", "value": True},
            "effects": [{"type": "include_step", "step_id": "register_birth"}],
        }
    ],
}

RULESETS = {
    "ro.life.child_born": PARENT,
    "ro.civil.birth.register": CHILD_REGISTER,
}


def test_resolves_root_and_children():
    node = resolve_event("ro.life.child_born", RULESETS, {}, jurisdiction_path=["ro"], reference_date="2026-06-25")
    assert node.event_type_id == "ro.life.child_born"
    assert "start" in node.route.included_steps
    ids = node.event_ids()
    assert "ro.civil.birth.register" in ids
    # allowance ruleset is not provided -> recorded as unknown_event child
    assert "ro.benefits.state_allowance.request" in ids
    unknown = [n for n in node.flatten() if n.event_type_id == "ro.benefits.state_allowance.request"][0]
    assert unknown.route.status == "unknown_event"


def test_child_route_is_evaluated():
    node = resolve_event("ro.life.child_born", RULESETS, {}, jurisdiction_path=["ro"], reference_date="2026-06-25")
    child = [n for n in node.flatten() if n.event_type_id == "ro.civil.birth.register"][0]
    assert "register_birth" in child.route.included_steps


def test_missing_root_raises():
    with pytest.raises(KeyError):
        resolve_event("ro.life.nonexistent", RULESETS, {}, jurisdiction_path=["ro"])


def test_cycle_is_guarded():
    a = {"event_type_id": "ev.a", "rules": [{"id": "ra", "canonical_rule_id": "a.root", "jurisdiction_ids": ["ro"], "effective_from": "2000-01-01", "when": {"op": "const", "value": True}, "effects": [{"type": "trigger_child_event", "event_type_id": "ev.b"}]}]}
    b = {"event_type_id": "ev.b", "rules": [{"id": "rb", "canonical_rule_id": "b.root", "jurisdiction_ids": ["ro"], "effective_from": "2000-01-01", "when": {"op": "const", "value": True}, "effects": [{"type": "trigger_child_event", "event_type_id": "ev.a"}]}]}
    node = resolve_event("ev.a", {"ev.a": a, "ev.b": b}, {}, jurisdiction_path=["ro"], reference_date="2026-06-25")
    # cycle terminates: a -> b -> a (not re-expanded)
    assert node.event_ids().count("ev.a") >= 1
    assert "ev.b" in node.event_ids()
