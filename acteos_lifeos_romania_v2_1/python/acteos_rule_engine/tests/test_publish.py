"""Unit tests for the publish/compile pipeline (in-memory batches)."""

from __future__ import annotations

import pytest

from acteos_rule_engine.authoring.publish import (
    PublishError,
    PublishedBundle,
    compile_bundle,
    mint_uuid,
)


def _claim(cid="claim.x", *, confidence="verified", status="active", snapshot_id="snap-1",
           freshness_class="operational"):
    return {
        "id": cid,
        "source_id": "src.x",
        "snapshot_id": snapshot_id,
        "statement": "...",
        "evidence_excerpt": "...",
        "locator": "art. 1",
        "url": "https://example.ro",
        "publisher": "Pub",
        "authority_level": "national_normative",
        "confidence": confidence,
        "freshness_class": freshness_class,
        "status": status,
        "accessed_at": "2026-06-01",
    }


def _rule(rule_id="rule.x", *, severity="operational", effects=None,
          source_claim_ids=("claim.x",), effective_from="2021-03-12",
          override_rule_ids=()):
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
        "override_rule_ids": list(override_rule_ids),
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


def test_compile_clean_batch_is_deterministic():
    batch = _batch([_rule()])
    a = compile_bundle([batch])
    b = compile_bundle([batch])
    assert isinstance(a, PublishedBundle)
    assert a.manifest_sha256 == b.manifest_sha256
    assert len(a.manifest_sha256) == 64
    assert a.version == b.version
    assert a.version.startswith("r1-")
    assert len(a.rule_revisions) == 1
    assert a.certification.verdict == "go"


def test_source_claim_ids_mapped_to_minted_uuids():
    bundle = compile_bundle([_batch([_rule()])])
    rev = bundle.rule_revisions[0]
    assert rev.source_claim_ids == [mint_uuid("claim", "claim.x")]
    assert bundle.source_claims[0].id == mint_uuid("claim", "claim.x")
    assert "life.test" in bundle.required_event_type_ids
    assert "s1" in bundle.referenced_step_ids


def test_no_go_batch_refuses_to_compile():
    # normative rule without claim -> certification no_go
    batch = _batch([_rule(source_claim_ids=())])
    with pytest.raises(PublishError) as exc:
        compile_bundle([batch])
    assert exc.value.report is not None
    assert exc.value.report.verdict == "no_go"


def test_conditional_requires_allow_flag():
    batch = _batch([_rule()], claims=[_claim(snapshot_id="pending")])
    with pytest.raises(PublishError):
        compile_bundle([batch])
    bundle = compile_bundle([batch], allow_conditional=True)
    assert bundle.certification.verdict == "conditional_go"
    assert "claim.x" in bundle.provenance_pending


def test_content_rows_shapes_are_fk_safe():
    bundle = compile_bundle([_batch([_rule()])])
    rows = bundle.as_content_rows()
    assert set(rows) == {
        "content.rule_sets",
        "content.rule_revisions",
        "content.rule_set_members",
    }
    rule_set = rows["content.rule_sets"][0]
    assert rule_set["manifest_sha256"] == bundle.manifest_sha256
    assert len(rule_set["manifest_sha256"]) == 64
    assert rule_set["status"] == "draft"
    assert rule_set["approved_by"] == []
    member = rows["content.rule_set_members"][0]
    assert member["rule_set_id"] == bundle.rule_set_id
    assert member["rule_revision_id"] == bundle.rule_revisions[0].id
    rev = rows["content.rule_revisions"][0]
    assert rev["event_type_id"] == "life.test"
    assert rev["severity"] == "operational"
    assert rev["effective_from"] == "2021-03-12"


def test_rule_without_effective_from_is_deferred():
    advisory = _rule(
        effects=[{"type": "emit_advice", "message_ro": "x", "tag": "t"}],
        source_claim_ids=(),
        effective_from=None,
    )
    bundle = compile_bundle([_batch([advisory])])
    assert len(bundle.rule_revisions) == 1
    assert bundle.publishable_revisions() == []
    assert len(bundle.deferred_revisions()) == 1
    # strict refuses, non-strict emits an empty rule_revisions set
    with pytest.raises(PublishError):
        bundle.as_content_rows(strict=True)
    rows = bundle.as_content_rows(strict=False)
    assert rows["content.rule_revisions"] == []
    assert rows["content.rule_set_members"] == []


def test_override_rule_ids_resolve_to_uuids():
    rule_a = _rule(rule_id="a")
    rule_b = _rule(rule_id="b", override_rule_ids=("a",))
    bundle = compile_bundle([_batch([rule_a, rule_b], claims=[_claim()])])
    by_canon = {r.canonical_rule_id: r for r in bundle.rule_revisions}
    rev_b = by_canon["ro.life.test.b"]
    assert rev_b.override_rule_ids == [mint_uuid("rule", "ro.life.test.a", "1")]


def test_unresolved_override_is_flagged():
    rule = _rule(override_rule_ids=("ghost",))
    bundle = compile_bundle([_batch([rule])])
    assert any(i.startswith("OVERRIDE_TARGET_UNRESOLVED:ghost") for i in bundle.issues)


def test_missing_freshness_class_is_flagged():
    batch = _batch([_rule()], claims=[_claim(freshness_class=None)])
    bundle = compile_bundle([batch])
    assert any(i.startswith("CLAIM_FRESHNESS_MISSING:claim.x") for i in bundle.issues)
    assert bundle.source_claims[0].freshness_class is None


def test_manifest_changes_when_content_changes():
    a = compile_bundle([_batch([_rule()])])
    b = compile_bundle([_batch([_rule(effective_from="2018-07-20")])])
    assert a.manifest_sha256 != b.manifest_sha256


def test_to_manifest_roundtrips_core_fields():
    bundle = compile_bundle([_batch([_rule()])])
    manifest = bundle.to_manifest()
    assert manifest["manifest_sha256"] == bundle.manifest_sha256
    assert manifest["version"] == bundle.version
    assert manifest["rule_set_id"] == bundle.rule_set_id
    assert len(manifest["rule_revisions"]) == 1
