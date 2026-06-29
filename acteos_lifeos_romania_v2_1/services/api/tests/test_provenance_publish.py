"""Provenance publish-adapter tests (no live database).

Verifies the gated provenance chain wiring in content_publish.py / publish_db.py:
- no statements when no sources/snapshots are authored (today's inbox);
- FK-ordered, idempotent INSERTs when real provenance is authored;
- NOT NULL validation of provenance rows;
- dry-run statement ordering keeps the chain FK-safe.
"""

from __future__ import annotations

from acteos_api.content_publish import (
    build_provenance_statements,
    compiled_provenance_sql,
    validate_content_rows,
)
from acteos_api.publish_db import build_dry_run
from acteos_rule_engine.authoring.publish import compile_bundle


def _claim() -> dict:
    return {
        "id": "claim.x",
        "source_id": "src.x",
        "snapshot_id": "snap.x.2026",
        "statement": "Documentul expira la 6 luni.",
        "evidence_excerpt": "art. 1 alin. (2)",
        "locator": "art.1(2)",
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


_SOURCES = [
    {
        "id": "src.x",
        "canonical_url": "https://legislatie.just.ro/example",
        "publisher": "Monitorul Oficial",
        "authority_level": "national_normative",
        "legal_rank": "LEGE",
        "territory_ids": ["RO"],
        "fetch_mode": "manual",
        "allowed_to_fetch": False,
    }
]
_SNAPSHOTS = [
    {
        "id": "snap.x.2026",
        "source_id": "src.x",
        "captured_at": "2026-06-01T10:00:00Z",
        "sha256": "a" * 64,
        "http_status": 200,
        "content_type": "text/html",
    }
]


def _batch(*, sources=None, snapshots=None) -> dict:
    doc: dict = {"batch_id": "ro.life.test", "claims": [_claim()]}
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


_CATALOG = {
    "schema_version": "2.0.0",
    "waves": {
        "R1A": [
            {
                "id": "life.test",
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


def test_no_provenance_authored_yields_no_statements():
    bundle = compile_bundle([_batch()])
    assert build_provenance_statements(bundle) == []
    assert compiled_provenance_sql(bundle) == []


def test_provenance_statements_target_tables_in_fk_order():
    bundle = compile_bundle([_batch(sources=_SOURCES, snapshots=_SNAPSHOTS)])
    statements = build_provenance_statements(bundle)
    assert [s.table.name for s in statements] == [
        "sources",
        "source_snapshots",
        "source_claims",
    ]
    joined = "\n".join(compiled_provenance_sql(bundle)).upper()
    assert "CONTENT.SOURCES" in joined
    assert "CONTENT.SOURCE_SNAPSHOTS" in joined
    assert "CONTENT.SOURCE_CLAIMS" in joined
    assert "ON CONFLICT" in joined


def test_provenance_rows_validate_not_null():
    bundle = compile_bundle([_batch(sources=_SOURCES, snapshots=_SNAPSHOTS)])
    rows = bundle.as_provenance_rows()
    assert validate_content_rows(rows) == []
    # Break a NOT NULL invariant -> validation flags it by table:identity:column.
    rows["content.source_claims"][0]["statement"] = None
    violations = validate_content_rows(rows)
    assert any(v.endswith(":statement") for v in violations)


def test_dry_run_includes_provenance_sql_in_fk_order():
    plan = build_dry_run(_CATALOG, [_batch(sources=_SOURCES, snapshots=_SNAPSHOTS)])
    assert plan.source_count == 1
    assert plan.source_snapshot_count == 1
    assert plan.source_claim_count == 1
    joined = "\n".join(plan.statements_sql).upper()
    assert joined.index("CONTENT.LIFE_EVENT_TYPES") < joined.index("CONTENT.SOURCES")
    assert joined.index("CONTENT.SOURCES") < joined.index("CONTENT.SOURCE_SNAPSHOTS")
    assert joined.index("CONTENT.SOURCE_SNAPSHOTS") < joined.index("CONTENT.SOURCE_CLAIMS")
    assert joined.index("CONTENT.SOURCE_CLAIMS") < joined.index("CONTENT.RULE_SETS")


def test_dry_run_without_provenance_emits_no_chain():
    plan = build_dry_run(_CATALOG, [_batch()])
    assert plan.source_count == 0
    assert plan.source_snapshot_count == 0
    assert plan.source_claim_count == 0
    assert plan.provenance_sql == []
