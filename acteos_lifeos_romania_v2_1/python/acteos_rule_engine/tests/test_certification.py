"""Unit tests for the release certification gate.

These run entirely on in-memory batch dictionaries shaped like the output of
``acteos_rule_engine.authoring.loader.load_batch`` so they need no filesystem.
"""

from __future__ import annotations

from acteos_rule_engine.authoring.certification import (
    ADVISORY_EFFECT_TYPES,
    NORMATIVE_EFFECT_TYPES,
    VERDICT_CONDITIONAL,
    VERDICT_GO,
    VERDICT_NO_GO,
    certify_batch,
    certify_batches,
)
from acteos_rule_engine.authoring.effects import EFFECT_TYPES


def _claim(cid="claim.x", *, confidence="verified", status="active", snapshot_id="snap-1"):
    return {
        "id": cid,
        "source_id": "src.x",
        "snapshot_id": snapshot_id,
        "statement": "...",
        "url": "https://example.ro",
        "publisher": "Pub",
        "authority_level": "national_normative",
        "confidence": confidence,
        "status": status,
    }


def _rule(
    rule_id="rule.x",
    *,
    severity="operational",
    effects=None,
    source_claim_ids=("claim.x",),
    effective_from="2021-03-12",
):
    rule = {
        "id": rule_id,
        "canonical_rule_id": f"ro.life.test.{rule_id}",
        "event_type_id": "life.test",
        "jurisdiction_ids": ["RO"],
        "severity": severity,
        "when": {"op": "const", "value": True},
        "effects": effects if effects is not None else [{"type": "include_step", "step_id": "s1"}],
        "source_claim_ids": list(source_claim_ids),
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


def _codes(findings):
    return {f.code for f in findings}


def test_effect_partition_is_total_and_disjoint():
    assert not (NORMATIVE_EFFECT_TYPES & ADVISORY_EFFECT_TYPES)
    assert NORMATIVE_EFFECT_TYPES | ADVISORY_EFFECT_TYPES == frozenset(EFFECT_TYPES)


def test_clean_batch_is_go():
    report = certify_batches([_batch([_rule()])])
    assert report.verdict == VERDICT_GO
    assert report.blockers == []
    assert report.warnings == []


def test_normative_rule_without_claim_blocks():
    findings = certify_batch(_batch([_rule(source_claim_ids=())]))
    assert "NORMATIVE_RULE_WITHOUT_CLAIM" in _codes(findings)


def test_normative_rule_without_effective_from_blocks():
    findings = certify_batch(_batch([_rule(effective_from=None)]))
    assert "NORMATIVE_RULE_WITHOUT_EFFECTIVE_FROM" in _codes(findings)


def test_dangling_claim_reference_blocks():
    findings = certify_batch(_batch([_rule(source_claim_ids=("claim.missing",))]))
    assert "DANGLING_CLAIM_REFERENCE" in _codes(findings)


def test_critical_rule_with_expired_claim_blocks():
    batch = _batch(
        [_rule(severity="critical")],
        claims=[_claim(confidence="expired")],
    )
    findings = certify_batch(batch)
    assert "CRITICAL_CLAIM_BAD_CONFIDENCE" in _codes(findings)
    assert certify_batches([batch]).verdict == VERDICT_NO_GO


def test_critical_rule_with_needs_confirmation_claim_blocks():
    batch = _batch(
        [_rule(severity="critical")],
        claims=[_claim(confidence="needs_confirmation")],
    )
    findings = certify_batch(batch)
    assert "CRITICAL_CLAIM_UNVERIFIED" in _codes(findings)


def test_advisory_only_rule_without_claim_is_go():
    rule = _rule(
        effects=[{"type": "emit_advice", "message_ro": "x", "tag": "t"}],
        source_claim_ids=(),
        effective_from=None,
    )
    report = certify_batches([_batch([rule])])
    assert report.verdict == VERDICT_GO


def test_pending_snapshot_on_normative_is_conditional_warning():
    batch = _batch([_rule()], claims=[_claim(snapshot_id="pending")])
    report = certify_batches([batch])
    assert report.verdict == VERDICT_CONDITIONAL
    assert "PROVENANCE_NOT_SNAPSHOTTED" in _codes(report.warnings)


def test_unknown_effect_type_blocks():
    findings = certify_batch(_batch([_rule(effects=[{"type": "nuke_everything"}])]))
    assert "UNKNOWN_EFFECT_TYPE" in _codes(findings)


def test_is_releasable_respects_allow_conditional():
    batch = _batch([_rule()], claims=[_claim(snapshot_id="pending")])
    report = certify_batches([batch])
    assert report.verdict == VERDICT_CONDITIONAL
    assert report.is_releasable(allow_conditional=False) is False
    assert report.is_releasable(allow_conditional=True) is True
