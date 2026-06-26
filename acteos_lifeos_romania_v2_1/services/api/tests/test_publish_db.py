"""Unit tests for the publish_to_db CLI (pure, no filesystem, no database)."""

from __future__ import annotations

import pytest

from acteos_api.publish_db import DryRunPlan, build_dry_run, main
from acteos_rule_engine.authoring.publish import PublishError

_CATALOG = {
    "schema_version": "2.0.0",
    "waves": {
        "R1A": [
            {
                "id": "ro.life.test",
                "category_id": "identity_documents",
                "title_ro": "Test",
                "trigger_phrases_ro": ["test"],
                "release_wave": "R1A",
                "research_status": "required",
                "production_status": "not_available",
            }
        ]
    },
}

_EMPTY_CATALOG = {"schema_version": "2.0.0", "waves": {}}

_TEMPLATES_DOC = {
    "step_templates": [
        {"id": "apply_x", "title_ro": "Depune", "instruction_ro": "Mergi la ghiseu."}
    ],
    "requirement_templates": [
        {"id": "req.x", "title_ro": "Certificat", "obligation": "mandatory", "timing": "now"}
    ],
}


def _claim(cid="claim.x"):
    return {
        "id": cid,
        "source_id": "src.x",
        "snapshot_id": "snap-1",
        "statement": "...",
        "evidence_excerpt": "...",
        "locator": "art. 1",
        "authority_level": "national_normative",
        "confidence": "verified",
        "freshness_class": "operational",
        "status": "active",
        "accessed_at": "2026-06-01",
    }


def _rule(rule_id="rule.x", *, effective_from="2021-03-12", effects=None,
          source_claim_ids=("claim.x",), severity="operational"):
    rule = {
        "id": rule_id,
        "canonical_rule_id": f"ro.life.test.{rule_id}",
        "event_type_id": "life.test",
        "jurisdiction_ids": ["RO"],
        "authority_level": "national_normative",
        "severity": severity,
        "when": {"op": "const", "value": True},
        "effects": effects if effects is not None else [{"type": "include_step", "step_id": "s1"}],
        "source_claim_ids": list(source_claim_ids),
        "override_rule_ids": [],
        "status": "draft",
    }
    if effective_from is not None:
        rule["effective_from"] = effective_from
    return rule


def _rule_with_refs():
    return _rule(
        rule_id="refs",
        effects=[
            {"type": "include_step", "step_id": "apply_x"},
            {"type": "include_requirement", "requirement_id": "req.x"},
        ],
    )


def _batch(rules, claims=None, templates=None, batch_id="ro.life.test"):
    return {
        "batch_dir": batch_id,
        "ruleset": {"batch_id": batch_id, "event_type_id": "life.test", "rules": rules},
        "fixtures": {},
        "claims": {"batch_id": batch_id, "claims": claims if claims is not None else [_claim()]},
        "templates": templates,
    }


def test_build_dry_run_emits_fk_ordered_sql():
    plan = build_dry_run(_CATALOG, [_batch([_rule()])])
    assert isinstance(plan, DryRunPlan)
    joined = "\n".join(plan.statements_sql).upper()
    assert joined.index("CONTENT.LIFE_EVENT_TYPES") < joined.index("CONTENT.RULE_SETS")
    assert joined.index("CONTENT.RULE_SETS") < joined.index("CONTENT.RULE_REVISIONS")
    assert joined.index("CONTENT.RULE_REVISIONS") < joined.index("CONTENT.RULE_SET_MEMBERS")
    assert "ON CONFLICT" in joined


def test_build_dry_run_summary_counts():
    plan = build_dry_run(_CATALOG, [_batch([_rule()])])
    assert plan.event_type_count == 1
    assert plan.summary["rule_revision_count"] == 1
    assert plan.summary["publishable_rule_count"] == 1
    assert plan.missing_event_types == []
    assert plan.deferred_rule_ids == []
    assert plan.version.startswith("r1-")
    assert len(plan.manifest_sha256) == 64
    assert plan.summary["certification_verdict"] == "go"


def test_build_dry_run_reports_missing_event_types():
    plan = build_dry_run(_EMPTY_CATALOG, [_batch([_rule()])])
    assert plan.event_type_count == 0
    assert plan.event_type_sql == []
    assert plan.missing_event_types == ["life.test"]


def test_build_dry_run_non_strict_defers_rules_without_effective_from():
    advisory = _rule(
        rule_id="adv",
        effective_from=None,
        severity="explanatory",
        effects=[{"type": "emit_advice", "message_ro": "x", "tag": "t"}],
        source_claim_ids=(),
    )
    plan = build_dry_run(_CATALOG, [_batch([advisory])], strict=False)
    assert plan.deferred_rule_ids == ["ro.life.test.adv"]
    assert plan.summary["publishable_rule_count"] == 0
    joined = "\n".join(plan.publish_sql).upper()
    assert "CONTENT.RULE_REVISIONS" not in joined


def test_build_dry_run_strict_refuses_deferred_rules():
    advisory = _rule(
        rule_id="adv",
        effective_from=None,
        severity="explanatory",
        effects=[{"type": "emit_advice", "message_ro": "x", "tag": "t"}],
        source_claim_ids=(),
    )
    with pytest.raises(PublishError):
        build_dry_run(_CATALOG, [_batch([advisory])], strict=True)


def test_build_dry_run_no_go_bundle_propagates():
    with pytest.raises(PublishError) as exc:
        build_dry_run(_CATALOG, [_batch([_rule(source_claim_ids=())])])
    assert exc.value.report is not None
    assert exc.value.report.verdict == "no_go"


def test_build_dry_run_includes_template_sql_when_authored():
    plan = build_dry_run(_CATALOG, [_batch([_rule_with_refs()], templates=_TEMPLATES_DOC)])
    assert plan.step_template_count == 1
    assert plan.requirement_template_count == 1
    assert plan.missing_steps == []
    assert plan.missing_requirements == []
    joined = "\n".join(plan.statements_sql).upper()
    assert joined.index("CONTENT.LIFE_EVENT_TYPES") < joined.index("CONTENT.STEP_TEMPLATES")
    assert joined.index("CONTENT.STEP_TEMPLATES") < joined.index("CONTENT.REQUIREMENT_TEMPLATES")
    assert joined.index("CONTENT.REQUIREMENT_TEMPLATES") < joined.index("CONTENT.RULE_SETS")


def test_build_dry_run_reports_template_coverage_gap():
    plan = build_dry_run(_CATALOG, [_batch([_rule_with_refs()], templates=None)])
    assert plan.step_template_count == 0
    assert plan.requirement_template_count == 0
    assert plan.missing_steps == ["apply_x"]
    assert plan.missing_requirements == ["req.x"]


def test_main_returns_1_when_catalog_missing(tmp_path):
    code = main([
        "--catalog", str(tmp_path / "nope.yaml"),
        "--inbox", str(tmp_path / "inbox"),
    ])
    assert code == 1
