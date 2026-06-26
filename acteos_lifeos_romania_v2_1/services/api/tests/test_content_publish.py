"""Unit tests for the content publish adapter (no live database)."""

from __future__ import annotations

import pytest

from acteos_api.content_publish import (
    ContentPublishError,
    SqlAlchemyContentRepository,
    build_event_type_statements,
    build_publish_statements,
    build_requirement_template_statements,
    build_step_template_statements,
    compiled_requirement_template_sql,
    compiled_sql,
    compiled_step_template_sql,
    missing_event_types,
    validate_content_rows,
)
from acteos_rule_engine.authoring.event_types import compile_event_types
from acteos_rule_engine.authoring.publish import PublishError, compile_bundle
from acteos_rule_engine.authoring.templates import compile_templates

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

_TEMPLATES_DOC = {
    "step_templates": [
        {"id": "apply_x", "title_ro": "Depune", "instruction_ro": "Mergi la ghiseu."}
    ],
    "requirement_templates": [
        {
            "id": "req.x",
            "title_ro": "Certificat",
            "obligation": "mandatory",
            "timing": "now",
        }
    ],
}


def _event_records():
    return compile_event_types(_CATALOG, scope=("R1",))


def _compiled_templates():
    batch = {
        "batch_dir": "ro.life.test",
        "ruleset": {"batch_id": "ro.life.test", "rules": []},
        "fixtures": {},
        "claims": None,
        "templates": _TEMPLATES_DOC,
    }
    return compile_templates([batch])


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


def _rule(rule_id="rule.x", *, effective_from="2021-03-12"):
    rule = {
        "id": rule_id,
        "canonical_rule_id": f"ro.life.test.{rule_id}",
        "event_type_id": "life.test",
        "jurisdiction_ids": ["RO"],
        "authority_level": "national_normative",
        "severity": "operational",
        "when": {"op": "const", "value": True},
        "effects": [{"type": "include_step", "step_id": "s1"}],
        "source_claim_ids": ["claim.x"],
        "override_rule_ids": [],
        "status": "draft",
    }
    if effective_from is not None:
        rule["effective_from"] = effective_from
    return rule


def _batch(rules, claims=None, batch_id="ro.life.test"):
    return {
        "batch_dir": batch_id,
        "ruleset": {"batch_id": batch_id, "event_type_id": "life.test", "rules": rules},
        "fixtures": {},
        "claims": {"batch_id": batch_id, "claims": claims if claims is not None else [_claim()]},
    }


class _FakeConn:
    def __init__(self) -> None:
        self.executed: list = []

    def execute(self, stmt):
        self.executed.append(stmt)
        return None


class _FakeBegin:
    def __init__(self, conn: _FakeConn) -> None:
        self._conn = conn

    def __enter__(self) -> _FakeConn:
        return self._conn

    def __exit__(self, *exc) -> bool:
        return False


class _FakeEngine:
    def __init__(self) -> None:
        self.conn = _FakeConn()

    def begin(self) -> _FakeBegin:
        return _FakeBegin(self.conn)


def test_build_three_statements():
    bundle = compile_bundle([_batch([_rule()])])
    statements = build_publish_statements(bundle)
    assert [s.table.name for s in statements] == [
        "rule_sets",
        "rule_revisions",
        "rule_set_members",
    ]


def test_compiled_sql_targets_content_tables():
    bundle = compile_bundle([_batch([_rule()])])
    joined = "\n".join(compiled_sql(bundle)).upper()
    assert "CONTENT.RULE_SETS" in joined
    assert "CONTENT.RULE_REVISIONS" in joined
    assert "CONTENT.RULE_SET_MEMBERS" in joined
    assert "ON CONFLICT" in joined


def test_validate_flags_missing_not_null():
    bundle = compile_bundle([_batch([_rule()])])
    rows = bundle.as_content_rows()
    rows["content.rule_revisions"][0]["authority_level"] = None
    violations = validate_content_rows(rows)
    assert any(value.endswith(":authority_level") for value in violations)


def test_publish_executes_in_fk_order_with_fake_engine():
    bundle = compile_bundle([_batch([_rule()])])
    engine = _FakeEngine()
    repo = SqlAlchemyContentRepository(engine)
    result = repo.publish(bundle)
    assert (
        result.rule_set_count,
        result.rule_revision_count,
        result.rule_set_member_count,
    ) == (1, 1, 1)
    assert [s.table.name for s in engine.conn.executed] == [
        "rule_sets",
        "rule_revisions",
        "rule_set_members",
    ]
    assert result.manifest_sha256 == bundle.manifest_sha256


def test_deferred_bundle_strict_refuses():
    advisory = {
        "id": "adv",
        "canonical_rule_id": "ro.life.test.adv",
        "event_type_id": "life.test",
        "jurisdiction_ids": ["RO"],
        "authority_level": "national_normative",
        "severity": "explanatory",
        "when": {"op": "const", "value": True},
        "effects": [{"type": "emit_advice", "message_ro": "x", "tag": "t"}],
        "source_claim_ids": [],
        "override_rule_ids": [],
        "status": "draft",
    }
    bundle = compile_bundle([_batch([advisory])])
    with pytest.raises(PublishError):
        build_publish_statements(bundle, strict=True)


def test_content_publish_error_is_runtimeerror():
    assert issubclass(ContentPublishError, RuntimeError)


def test_event_type_statement_targets_life_event_types():
    statements = build_event_type_statements(_event_records())
    assert [s.table.name for s in statements] == ["life_event_types"]


def test_publish_release_inserts_event_types_first():
    bundle = compile_bundle([_batch([_rule()])])
    engine = _FakeEngine()
    repo = SqlAlchemyContentRepository(engine)
    result = repo.publish_release(bundle, _event_records())
    assert [s.table.name for s in engine.conn.executed] == [
        "life_event_types",
        "rule_sets",
        "rule_revisions",
        "rule_set_members",
    ]
    assert result.event_type_count == 1
    assert result.rule_revision_count == 1


def test_publish_release_refuses_uncovered_event_type():
    bundle = compile_bundle([_batch([_rule()])])
    repo = SqlAlchemyContentRepository(_FakeEngine())
    assert missing_event_types(bundle, []) == ["life.test"]
    with pytest.raises(ContentPublishError):
        repo.publish_release(bundle, [])


def test_event_type_validation_flags_missing_title():
    rows = {"content.life_event_types": [{"id": "life.x", "title_ro": None}]}
    violations = validate_content_rows(rows)
    assert any(value.endswith(":title_ro") for value in violations)


def test_step_template_statement_targets_table():
    ct = _compiled_templates()
    statements = build_step_template_statements(ct.step_templates)
    assert [s.table.name for s in statements] == ["step_templates"]


def test_requirement_template_statement_targets_table():
    ct = _compiled_templates()
    statements = build_requirement_template_statements(ct.requirement_templates)
    assert [s.table.name for s in statements] == ["requirement_templates"]


def test_compiled_template_sql_targets_content_tables():
    ct = _compiled_templates()
    joined = "\n".join(
        compiled_step_template_sql(ct.step_templates)
        + compiled_requirement_template_sql(ct.requirement_templates)
    ).upper()
    assert "CONTENT.STEP_TEMPLATES" in joined
    assert "CONTENT.REQUIREMENT_TEMPLATES" in joined
    assert "ON CONFLICT" in joined


def test_step_template_validation_flags_missing_instruction():
    rows = {
        "content.step_templates": [
            {
                "id": "s",
                "semantic_key": "s",
                "title_ro": "t",
                "instruction_ro": None,
                "sequence_hint": 100,
                "status": "draft",
            }
        ]
    }
    violations = validate_content_rows(rows)
    assert any(value.endswith(":instruction_ro") for value in violations)


def test_requirement_template_validation_flags_missing_obligation():
    rows = {
        "content.requirement_templates": [
            {"id": "r", "title_ro": "t", "obligation": None, "timing": "now", "status": "draft"}
        ]
    }
    violations = validate_content_rows(rows)
    assert any(value.endswith(":obligation") for value in violations)


def test_publish_release_inserts_templates_between_event_types_and_rules():
    bundle = compile_bundle([_batch([_rule()])])
    ct = _compiled_templates()
    engine = _FakeEngine()
    repo = SqlAlchemyContentRepository(engine)
    result = repo.publish_release(
        bundle, _event_records(), ct.step_templates, ct.requirement_templates
    )
    assert [s.table.name for s in engine.conn.executed] == [
        "life_event_types",
        "step_templates",
        "requirement_templates",
        "rule_sets",
        "rule_revisions",
        "rule_set_members",
    ]
    assert result.step_template_count == 1
    assert result.requirement_template_count == 1
