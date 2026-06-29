"""Provenance chain compile tests (content.sources/source_snapshots/claims).

These exercise the gated provenance pipeline in authoring/publish.py:
- with today's inbox shape (claims only, no sources/snapshots) nothing is
  emitted, yet the rule bundle stays FK-safe;
- with real sources + snapshots authored, the full FK-linked chain is emitted
  using deterministic uuids;
- a claim whose snapshot is not authored is deferred (not emitted);
- authoring provenance never perturbs the rule-bundle manifest hash.
"""

from __future__ import annotations

from acteos_rule_engine.authoring.publish import compile_bundle, mint_uuid


def _claim(cid: str = "claim.x", *, source_id: str = "src.x", snapshot_id: str = "snap.x.2026") -> dict:
    return {
        "id": cid,
        "source_id": source_id,
        "snapshot_id": snapshot_id,
        "statement": "Documentul expira la 6 luni.",
        "evidence_excerpt": "art. 1 alin. (2)",
        "locator": "art.1(2)",
        "url": "https://legislatie.just.ro/example",
        "publisher": "Monitorul Oficial",
        "authority_level": "national_normative",
        "confidence": "verified",
        "freshness_class": "operational",
        "status": "active",
        "accessed_at": "2026-06-01",
    }


def _rule() -> dict:
    return {
        "id": "rule.x",
        "canonical_rule_id": "ro.life.test.rule.x",
        "event_type_id": "life.test",
        "jurisdiction_ids": ["RO"],
        "authority_level": "national_normative",
        "severity": "operational",
        "when": {"op": "const", "value": True},
        "effects": [{"type": "include_step", "step_id": "s1"}],
        "source_claim_ids": ["claim.x"],
        "override_rule_ids": [],
        "status": "draft",
        "effective_from": "2021-03-12",
    }


def _batch(*, claims: list[dict], sources: list[dict] | None = None, snapshots: list[dict] | None = None) -> dict:
    doc: dict = {"batch_id": "ro.life.test", "claims": claims}
    if sources is not None:
        doc["sources"] = sources
    if snapshots is not None:
        doc["snapshots"] = snapshots
    return {
        "batch_dir": "ro.life.test",
        "ruleset": {
            "batch_id": "ro.life.test",
            "event_type_id": "life.test",
            "rules": [_rule()],
        },
        "fixtures": {},
        "claims": doc,
    }


_SOURCE = {
    "id": "src.x",
    "canonical_url": "https://legislatie.just.ro/example",
    "publisher": "Monitorul Oficial",
    "authority_level": "national_normative",
    "legal_rank": "LEGE",
    "territory_ids": ["RO"],
    "fetch_mode": "manual",
    "allowed_to_fetch": False,
}
_SNAPSHOT = {
    "id": "snap.x.2026",
    "source_id": "src.x",
    "captured_at": "2026-06-01T10:00:00Z",
    "sha256": "a" * 64,
    "http_status": 200,
    "content_type": "text/html",
}


def test_no_provenance_authored_emits_no_rows():
    # Today's inbox shape: claims only, no sources/snapshots authored.
    bundle = compile_bundle([_batch(claims=[_claim()])])
    rows = bundle.as_provenance_rows()
    assert rows["content.sources"] == []
    assert rows["content.source_snapshots"] == []
    assert rows["content.source_claims"] == []
    # The rule bundle is still FK-safe and emittable, keyset unchanged.
    assert set(bundle.as_content_rows()) == {
        "content.rule_sets",
        "content.rule_revisions",
        "content.rule_set_members",
    }


def test_full_chain_emits_fk_safe_rows_when_authored():
    bundle = compile_bundle(
        [_batch(claims=[_claim()], sources=[_SOURCE], snapshots=[_SNAPSHOT])]
    )
    rows = bundle.as_provenance_rows()
    assert len(rows["content.sources"]) == 1
    assert len(rows["content.source_snapshots"]) == 1
    assert len(rows["content.source_claims"]) == 1

    src_row = rows["content.sources"][0]
    snap_row = rows["content.source_snapshots"][0]
    claim_row = rows["content.source_claims"][0]

    # Deterministic, FK-consistent minting across the chain.
    assert src_row["id"] == mint_uuid("source", "src.x")
    assert snap_row["id"] == mint_uuid("snapshot", "snap.x.2026")
    assert snap_row["source_id"] == src_row["id"]
    assert claim_row["source_id"] == src_row["id"]
    assert claim_row["snapshot_id"] == snap_row["id"]
    assert claim_row["id"] == mint_uuid("claim", "claim.x")
    assert claim_row["stable_key"] == "claim.x"
    assert len(snap_row["sha256"]) == 64


def test_claim_without_resolved_snapshot_is_deferred():
    # Source authored, but the claim's snapshot is not -> claim is not emitted.
    bundle = compile_bundle(
        [_batch(claims=[_claim(snapshot_id="snap.missing")], sources=[_SOURCE])]
    )
    rows = bundle.as_provenance_rows()
    assert len(rows["content.sources"]) == 1
    assert rows["content.source_snapshots"] == []
    assert rows["content.source_claims"] == []


def test_snapshot_without_resolved_source_is_deferred():
    # Snapshot points at an unauthored source -> snapshot (and claim) deferred.
    bundle = compile_bundle(
        [_batch(claims=[_claim()], snapshots=[_SNAPSHOT])]
    )
    rows = bundle.as_provenance_rows()
    assert rows["content.sources"] == []
    assert rows["content.source_snapshots"] == []
    assert rows["content.source_claims"] == []


def test_manifest_sha256_is_stable_regardless_of_provenance():
    # Authoring sources/snapshots must NOT change the rule-bundle manifest hash.
    base = compile_bundle([_batch(claims=[_claim()])])
    with_prov = compile_bundle(
        [_batch(claims=[_claim()], sources=[_SOURCE], snapshots=[_SNAPSHOT])]
    )
    assert base.manifest_sha256 == with_prov.manifest_sha256
    assert base.version == with_prov.version
