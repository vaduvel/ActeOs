"""Unit tests for the content publish adapter (no live database)."""

from __future__ import annotations

import pytest

from acteos_api.content_publish import (
    ContentPublishError,
    SqlAlchemyContentRepository,
    build_event_type_statements,
    build_publish_statements,
    compiled_sql,
    missing_event_types,
    validate_content_rows,
)
from acteos_rule_engine.authoring.event_types import compile_event_types
from acteos_rule_engine.authoring.publish import PublishError, compile_bundle

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


def _event_records():
    return compile_event_types(_CATALOG, scope=("R1",))


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
