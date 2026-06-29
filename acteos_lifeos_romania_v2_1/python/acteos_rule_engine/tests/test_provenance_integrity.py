"""Tests for the provenance integrity gate (certification) and the
source_provenance schema wiring (validate).

These run on in-memory batch dicts shaped like ``loader.load_batch`` output and
do not touch the filesystem. They lock in the deterministic DB-constraint gates
added for the M3 provenance chain.
"""

from __future__ import annotations

import pytest

from acteos_rule_engine.authoring.certification import (
    VERDICT_GO,
    VERDICT_NO_GO,
    certify_batches,
)


_SOURCE = {
    "id": "src.a",
    "canonical_url": "https://legislatie.just.ro/a",
    "publisher": "Monitorul Oficial",
    "authority_level": "national_normative",
    "fetch_mode": "manual",
    "allowed_to_fetch": False,
}
_SNAPSHOT = {
    "id": "snap.a_2026",
    "source_id": "src.a",
    "captured_at": "2026-06-01T10:00:00Z",
    "sha256": "a" * 64,
}


def _claim(cid="claim.a", *, source_id="src.a", snapshot_id="snap.a_2026"):
    return {
        "id": cid,
        "source_id": source_id,
        "snapshot_id": snapshot_id,
        "statement": "...",
        "url": "https://legislatie.just.ro/a",
        "publisher": "Monitorul Oficial",
        "authority_level": "national_normative",
        "confidence": "verified",
        "status": "active",
    }


def _rule(rule_id="rule.a", *, source_claim_ids=("claim.a",)):
    return {
        "id": rule_id,
        "canonical_rule_id": f"ro.life.test.{rule_id}",
        "event_type_id": "life.test",
        "jurisdiction_ids": ["RO"],
        "severity": "operational",
        "when": {"op": "const", "value": True},
        "effects": [{"type": "include_step", "step_id": "s1"}],
        "source_claim_ids": list(source_claim_ids),
        "status": "draft",
        "effective_from": "2021-03-12",
    }


def _batch(*, sources, snapshots, claims=None, rules=None, batch_id="ro.life.test"):
    return {
        "batch_dir": batch_id,
        "ruleset": {
            "batch_id": batch_id,
            "event_type_id": "life.test",
            "rules": rules if rules is not None else [_rule()],
        },
        "fixtures": {},
        "claims": {"batch_id": batch_id, "claims": claims if claims is not None else [_claim()]},
        "provenance": {"sources": sources, "snapshots": snapshots},
    }


def _codes(report):
    return {f.code for f in report.findings}


def test_clean_provenance_batch_is_go():
    report = certify_batches([_batch(sources=[_SOURCE], snapshots=[_SNAPSHOT])])
    assert report.verdict == VERDICT_GO
    assert not any(c.startswith("PROVENANCE_") for c in _codes(report))


def test_duplicate_canonical_url_within_batch_blocks():
    # Mirrors the real ro.life.criminal_record_certificate defect: two distinct
    # source ids share one canonical_url -> would break content.sources UNIQUE.
    dup = {**_SOURCE, "id": "src.b"}  # same canonical_url, different id
    report = certify_batches([_batch(sources=[_SOURCE, dup], snapshots=[_SNAPSHOT])])
    assert report.verdict == VERDICT_NO_GO
    assert "PROVENANCE_CANONICAL_URL_COLLISION" in _codes(report)


def test_duplicate_canonical_url_across_batches_blocks():
    src2 = {**_SOURCE, "id": "src.b"}
    snap2 = {**_SNAPSHOT, "id": "snap.b_2026", "source_id": "src.b", "sha256": "b" * 64}
    b1 = _batch(sources=[_SOURCE], snapshots=[_SNAPSHOT], batch_id="ro.life.b1")
    b2 = _batch(
        sources=[src2],
        snapshots=[snap2],
        claims=[_claim(cid="claim.b", source_id="src.b", snapshot_id="snap.b_2026")],
        rules=[_rule(rule_id="rule.b", source_claim_ids=("claim.b",))],
        batch_id="ro.life.b2",
    )
    report = certify_batches([b1, b2])
    assert "PROVENANCE_CANONICAL_URL_COLLISION" in _codes(report)


def test_same_source_id_reused_is_not_a_collision():
    # Re-declaring the SAME id is de-duplicated, not a collision.
    b1 = _batch(sources=[_SOURCE], snapshots=[_SNAPSHOT], batch_id="ro.life.b1")
    b2 = _batch(sources=[_SOURCE], snapshots=[_SNAPSHOT], batch_id="ro.life.b2")
    report = certify_batches([b1, b2])
    assert "PROVENANCE_CANONICAL_URL_COLLISION" not in _codes(report)


def test_bad_sha256_blocks():
    bad = {**_SNAPSHOT, "sha256": "NOTAHEXDIGEST"}
    report = certify_batches([_batch(sources=[_SOURCE], snapshots=[bad])])
    assert report.verdict == VERDICT_NO_GO
    assert "PROVENANCE_SNAPSHOT_SHA256_INVALID" in _codes(report)


def test_uppercase_sha256_blocks():
    bad = {**_SNAPSHOT, "sha256": "A" * 64}  # uppercase is not allowed
    report = certify_batches([_batch(sources=[_SOURCE], snapshots=[bad])])
    assert "PROVENANCE_SNAPSHOT_SHA256_INVALID" in _codes(report)


def test_duplicate_source_id_within_batch_blocks():
    dup = {**_SOURCE, "canonical_url": "https://legislatie.just.ro/other"}  # same id
    report = certify_batches([_batch(sources=[_SOURCE, dup], snapshots=[_SNAPSHOT])])
    assert "PROVENANCE_DUPLICATE_SOURCE_ID" in _codes(report)


def test_duplicate_snapshot_id_within_batch_blocks():
    dup = {**_SNAPSHOT, "sha256": "c" * 64}  # same id snap.a_2026
    report = certify_batches([_batch(sources=[_SOURCE], snapshots=[_SNAPSHOT, dup])])
    assert "PROVENANCE_DUPLICATE_SNAPSHOT_ID" in _codes(report)


def test_snapshot_digest_collision_blocks():
    # Distinct snapshot ids that share (source_id, sha256) -> source_snapshots
    # (source_id, sha256) UNIQUE would fail at insert.
    snap2 = {**_SNAPSHOT, "id": "snap.a_dup_2026"}
    report = certify_batches([_batch(sources=[_SOURCE], snapshots=[_SNAPSHOT, snap2])])
    assert "PROVENANCE_SNAPSHOT_DIGEST_COLLISION" in _codes(report)


def test_distinct_sources_same_sha_is_not_a_digest_collision():
    # Same sha256 but DIFFERENT source_id is allowed (mirrors the real
    # criminal_record snapshots, which share a digest across distinct sources):
    # only the canonical_url collision should fire there, not a digest one.
    src2 = {**_SOURCE, "id": "src.b", "canonical_url": "https://legislatie.just.ro/b"}
    snap2 = {**_SNAPSHOT, "id": "snap.b_2026", "source_id": "src.b"}  # same sha, diff source
    report = certify_batches([_batch(sources=[_SOURCE, src2], snapshots=[_SNAPSHOT, snap2])])
    assert "PROVENANCE_SNAPSHOT_DIGEST_COLLISION" not in _codes(report)


def test_batch_without_provenance_is_unaffected():
    batch = {
        "batch_dir": "ro.life.test",
        "ruleset": {"batch_id": "ro.life.test", "event_type_id": "life.test", "rules": [_rule()]},
        "fixtures": {},
        "claims": {"batch_id": "ro.life.test", "claims": [_claim()]},
    }
    report = certify_batches([batch])
    assert report.verdict == VERDICT_GO
    assert not any(c.startswith("PROVENANCE_") for c in _codes(report))


# --- validate.py: source_provenance schema wiring -------------------------

pytest.importorskip("jsonschema")
pytest.importorskip("referencing")

from acteos_rule_engine.authoring.validate import (  # noqa: E402
    CLAIM_SCHEMA,
    PREDICATE_SCHEMA,
    RULE_SCHEMA,
    SOURCE_PROVENANCE_SCHEMA,
    validate_batch,
)

_PRED = {
    "$id": "https://acteos/schemas/predicate.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["op"],
    "properties": {"op": {"type": "string"}},
}
_RULE = {
    "$id": "https://acteos/schemas/rule.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["id"],
    "properties": {"id": {"type": "string"}, "source_claim_ids": {"type": "array"}},
    "additionalProperties": True,
}
_CLAIM = {
    "$id": "https://acteos/schemas/source_claim.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["id"],
    "properties": {"id": {"type": "string"}},
    "additionalProperties": True,
}
_PROV = {
    "$id": "https://acteos/schemas/source_provenance.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["sources", "snapshots"],
    "properties": {
        "sources": {"type": "array"},
        "snapshots": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}},
            },
        },
    },
}
_MIN = {RULE_SCHEMA: _RULE, CLAIM_SCHEMA: _CLAIM, PREDICATE_SCHEMA: _PRED}


def test_provenance_doc_schema_violation_flagged():
    batch = {
        "ruleset": {"batch_id": "T", "rules": []},
        "claims": {"claims": []},
        "provenance": {"sources": [], "snapshots": [{"id": "s", "sha256": "NOTHEX"}]},
    }
    report = validate_batch(batch, {**_MIN, SOURCE_PROVENANCE_SCHEMA: _PROV})
    assert not report.ok
    assert any("provenance" in e for e in report.errors)


def test_provenance_doc_valid_passes():
    batch = {
        "ruleset": {"batch_id": "T", "rules": []},
        "claims": {"claims": []},
        "provenance": {"sources": [], "snapshots": [{"id": "s", "sha256": "a" * 64}]},
    }
    report = validate_batch(batch, {**_MIN, SOURCE_PROVENANCE_SCHEMA: _PROV})
    assert report.ok, report.errors


def test_provenance_schema_absent_skips_validation():
    # No provenance schema in the set -> a structurally bad provenance doc is
    # ignored (guarded, like template validation).
    batch = {
        "ruleset": {"batch_id": "T", "rules": []},
        "claims": {"claims": []},
        "provenance": {"snapshots": [{"id": "s", "sha256": "NOTHEX"}]},
    }
    report = validate_batch(batch, _MIN)
    assert report.ok, report.errors
