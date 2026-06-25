from wb_rule_engine.authoring.golden import run_fixtures
from wb_rule_engine.authoring.ruleset import evaluate_ruleset

RULESET = {
    "event_type_id": "life.demo",
    "required_facts": ["reason", "is_owner"],
    "rules": [
        {
            "id": "r.base",
            "canonical_rule_id": "demo.base",
            "jurisdiction_ids": ["ro.tm.timisoara"],
            "effective_from": "2000-01-01",
            "when": {"op": "const", "value": True},
            "effects": [
                {"type": "include_step", "step_id": "do_it"},
                {"type": "include_requirement", "requirement_id": "req.id"},
                {"type": "attach_channel", "channel_id": "ch.local"},
                {"type": "emit_advice", "message_ro": "x", "tag": "base_advice"},
            ],
        },
        {
            "id": "r.death",
            "canonical_rule_id": "demo.death_path",
            "jurisdiction_ids": ["ro.tm.timisoara"],
            "effective_from": "2000-01-01",
            "when": {"op": "eq", "field": "reason", "value": "death"},
            "effects": [
                {"type": "include_requirement", "requirement_id": "req.death_cert"},
                {"type": "require_confirmation", "message_ro": "confirm"},
            ],
        },
    ],
}

TM_PATH = ["eu", "ro", "ro.tm", "ro.tm.timisoara"]


def test_evaluate_ruleset_basic():
    r = evaluate_ruleset(RULESET, {"reason": "purchase", "is_owner": True}, jurisdiction_path=TM_PATH, reference_date="2026-06-25")
    assert r.status == "ok"
    assert "do_it" in r.included_steps
    assert "ch.local" in r.channels
    assert "base_advice" in r.advice_tags
    assert "req.death_cert" not in r.requirements


def test_death_path_requirement_and_confirmation():
    r = evaluate_ruleset(RULESET, {"reason": "death", "is_owner": True}, jurisdiction_path=TM_PATH, reference_date="2026-06-25")
    assert "req.death_cert" in r.requirements
    assert "death_path" in r.confirmations


def test_missing_facts_status_and_order():
    r = evaluate_ruleset(RULESET, {}, jurisdiction_path=TM_PATH, reference_date="2026-06-25")
    assert r.status == "needs_facts"
    assert r.missing_facts == ["reason", "is_owner"]


def test_jurisdiction_excludes_local_rules():
    r = evaluate_ruleset(RULESET, {"reason": "purchase", "is_owner": True}, jurisdiction_path=["eu", "ro", "ro.cj", "ro.cj.cluj"], reference_date="2026-06-25")
    assert r.channels == []
    assert r.included_steps == []


def test_run_fixtures_pass_and_fail():
    defaults = {"jurisdiction_path": TM_PATH, "reference_date": "2026-06-25"}
    good = {
        "batch_id": "DEMO",
        "defaults": defaults,
        "fixtures": [
            {"id": "D01", "facts": {"reason": "purchase", "is_owner": True}, "expect": {"status": "ok", "included_steps": ["do_it"], "advice_tags": ["base_advice"], "requirements_absent": ["req.death_cert"]}},
            {"id": "D02", "facts": {}, "expect": {"status": "needs_facts", "missing_facts": ["reason", "is_owner"]}},
            {"id": "D03", "facts": {"reason": "death", "is_owner": True}, "expect": {"status": "ok", "needs_confirmation": ["death_path"]}},
        ],
    }
    report = run_fixtures({"ruleset": RULESET, "fixtures": good})
    assert report.ok, report.failures
    assert report.passed == 3

    bad = {
        "batch_id": "BAD",
        "defaults": defaults,
        "fixtures": [{"id": "X", "facts": {"reason": "purchase", "is_owner": True}, "expect": {"channels": ["ch.nonexistent"]}}],
    }
    rbad = run_fixtures({"ruleset": RULESET, "fixtures": bad})
    assert not rbad.ok
    assert rbad.failures[0].fixture_id == "X"
