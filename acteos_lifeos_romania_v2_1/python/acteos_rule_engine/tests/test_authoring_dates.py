"""Rich-contract engine tests: date anchors, deadlines/overdue, conflicts,
overrides and status precedence."""
from datetime import date

from acteos_rule_engine.authoring.ast import EvalContext, evaluate, resolve_date_token
from acteos_rule_engine.authoring.ruleset import evaluate_ruleset
from acteos_rule_engine.trivalent import Tri

CTX = EvalContext(reference_date=date(2026, 6, 25))


def test_resolve_date_token_variants():
    assert resolve_date_token("2026-06-25", {}, CTX) == date(2026, 6, 25)
    assert resolve_date_token("reference_date", {}, CTX) == date(2026, 6, 25)
    assert resolve_date_token("move_date", {"move_date": "2026-06-22"}, CTX) == date(2026, 6, 22)
    assert resolve_date_token("move_date_plus_15d", {"move_date": "2026-06-22"}, CTX) == date(2026, 7, 7)
    assert resolve_date_token("expiry_date_minus_180d", {"expiry_date": "2026-12-22"}, CTX) == date(2026, 6, 25)
    assert resolve_date_token("reference_date_minus_10d", {}, CTX) == date(2026, 6, 15)
    assert resolve_date_token("unknown_fact", {}, CTX) is None


def test_within_window_uses_reference_date_and_anchors():
    pred = {"op": "within_window", "field": "reference_date", "values": ["expiry_date_minus_180d", "expiry_date_minus_15d"]}
    assert evaluate(pred, {"expiry_date": "2026-08-24"}, CTX) is Tri.TRUE
    # missing expiry_date -> cannot resolve window -> unknown (never silently false)
    assert evaluate(pred, {}, CTX) is Tri.UNKNOWN
    # reference far before the window
    early = EvalContext(reference_date=date(2025, 1, 1))
    assert evaluate(pred, {"expiry_date": "2026-08-24"}, early) is Tri.FALSE


def _deadline_ruleset(value):
    return {
        "event_type_id": "life.demo",
        "required_facts": [],
        "rules": [
            {
                "id": "r1",
                "canonical_rule_id": "demo.deadline",
                "jurisdiction_ids": ["ro"],
                "effective_from": "2000-01-01",
                "when": {"op": "const", "value": True},
                "effects": [
                    {"type": "include_step", "step_id": "do_it"},
                    {"type": "set_deadline", "step_id": "do_it", "value": value},
                ],
            }
        ],
    }


def test_deadline_calendar_days_and_overdue():
    rs = _deadline_ruleset({"kind": "relative_calendar_days", "anchor": "move_date", "days": 15})
    r = evaluate_ruleset(rs, {"move_date": "2026-06-22"}, jurisdiction_path=["ro"], reference_date="2026-06-25")
    assert r.deadline_dates["do_it"] == "2026-07-07"
    assert r.overdue_steps == []
    overdue = evaluate_ruleset(rs, {"move_date": "2026-05-01"}, jurisdiction_path=["ro"], reference_date="2026-06-25")
    assert overdue.deadline_dates["do_it"] == "2026-05-16"
    assert overdue.overdue_steps == ["do_it"]


def test_deadline_relative_hours():
    rs = _deadline_ruleset({"kind": "relative_hours", "anchor": "event_date", "hours": 24})
    r = evaluate_ruleset(rs, {"event_date": "2026-06-24"}, jurisdiction_path=["ro"], reference_date="2026-06-25")
    assert r.deadlines["do_it"]["hours"] == 24
    assert r.deadline_dates["do_it"] == "2026-06-25"


def test_deadline_window():
    rs = _deadline_ruleset({"kind": "window", "from": "expiry_date_minus_180d", "to": "expiry_date_minus_15d"})
    r = evaluate_ruleset(rs, {"expiry_date": "2026-12-22"}, jurisdiction_path=["ro"], reference_date="2026-06-25")
    assert r.deadlines["do_it"]["from"] == "2026-06-25"
    assert r.deadlines["do_it"]["to"] == "2026-12-07"


def test_flag_conflict_sets_conflicting_status():
    rs = {
        "event_type_id": "life.demo",
        "required_facts": [],
        "rules": [
            {
                "id": "r.conflict",
                "canonical_rule_id": "demo.sanction",
                "jurisdiction_ids": ["ro"],
                "effective_from": "2000-01-01",
                "when": {"op": "const", "value": True},
                "effects": [
                    {"type": "flag_conflict", "tag": "sanction_amount", "blocked_effect": "sanction_amount_display", "message_ro": "conflict"},
                ],
            }
        ],
    }
    r = evaluate_ruleset(rs, {}, jurisdiction_path=["ro"], reference_date="2026-06-25")
    assert r.status == "conflicting"
    assert r.conflicts == ["sanction_amount"]
    assert r.blocked_effects == ["sanction_amount_display"]


def test_missing_facts_outranks_conflict():
    rs = {
        "event_type_id": "life.demo",
        "required_facts": ["expiry_date"],
        "rules": [
            {
                "id": "r.conflict",
                "canonical_rule_id": "demo.sanction",
                "jurisdiction_ids": ["ro"],
                "effective_from": "2000-01-01",
                "when": {"op": "const", "value": True},
                "effects": [{"type": "flag_conflict", "tag": "sanction_amount"}],
            }
        ],
    }
    r = evaluate_ruleset(rs, {}, jurisdiction_path=["ro"], reference_date="2026-06-25")
    assert r.status == "needs_facts"
    assert r.missing_facts == ["expiry_date"]


def test_override_rule_excludes_target():
    rs = {
        "event_type_id": "life.demo",
        "required_facts": [],
        "rules": [
            {
                "id": "r.base",
                "canonical_rule_id": "demo.base",
                "jurisdiction_ids": ["ro"],
                "effective_from": "2000-01-01",
                "when": {"op": "eq", "field": "change_type", "value": "domiciliu"},
                "effects": [{"type": "include_step", "step_id": "renew_card"}],
            },
            {
                "id": "r.cei",
                "canonical_rule_id": "demo.cei",
                "jurisdiction_ids": ["ro"],
                "effective_from": "2000-01-01",
                "when": {"op": "all", "args": [{"op": "eq", "field": "id_card_type", "value": "cei"}, {"op": "eq", "field": "change_type", "value": "domiciliu"}]},
                "effects": [{"type": "override_rule", "rule_id": "r.base"}, {"type": "emit_warning", "tag": "cei_no_new_doc", "message_ro": "x"}],
            },
        ],
    }
    cei = evaluate_ruleset(rs, {"id_card_type": "cei", "change_type": "domiciliu"}, jurisdiction_path=["ro"], reference_date="2026-06-25")
    assert cei.overridden_rules == ["r.base"]
    assert "renew_card" not in cei.included_steps
    assert "cei_no_new_doc" in cei.warning_tags
    plain = evaluate_ruleset(rs, {"id_card_type": "ci_simpla", "change_type": "domiciliu"}, jurisdiction_path=["ro"], reference_date="2026-06-25")
    assert plain.overridden_rules == []
    assert "renew_card" in plain.included_steps
