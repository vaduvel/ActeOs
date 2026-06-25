import pytest

pytest.importorskip("jsonschema")
pytest.importorskip("referencing")

from wb_rule_engine.authoring.validate import (
    CLAIM_SCHEMA,
    PREDICATE_SCHEMA,
    RULE_SCHEMA,
    validate_batch,
)

PRED = {
    "$id": "https://acteos/schemas/predicate.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["op"],
    "properties": {"op": {"type": "string"}},
}
RULE = {
    "$id": "https://acteos/schemas/rule.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["id", "when"],
    "properties": {
        "id": {"type": "string"},
        "when": {"$ref": "predicate.schema.json"},
        "source_claim_ids": {"type": "array", "items": {"type": "string"}},
    },
    "additionalProperties": True,
}
CLAIM = {
    "$id": "https://acteos/schemas/source_claim.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["id"],
    "properties": {"id": {"type": "string"}},
    "additionalProperties": True,
}
SCHEMAS = {RULE_SCHEMA: RULE, CLAIM_SCHEMA: CLAIM, PREDICATE_SCHEMA: PRED}


def test_valid_batch_has_no_errors():
    batch = {
        "ruleset": {"batch_id": "T", "rules": [{"id": "r1", "when": {"op": "const"}, "source_claim_ids": ["c1"]}]},
        "claims": {"claims": [{"id": "c1"}]},
    }
    report = validate_batch(batch, SCHEMAS)
    assert report.ok, report.errors


def test_invalid_predicate_via_ref_is_flagged():
    batch = {
        "ruleset": {"batch_id": "T", "rules": [{"id": "r1", "when": {}, "source_claim_ids": []}]},
        "claims": {"claims": []},
    }
    report = validate_batch(batch, SCHEMAS)
    assert not report.ok


def test_dangling_source_claim_id_flagged():
    batch = {
        "ruleset": {"batch_id": "T", "rules": [{"id": "r1", "when": {"op": "const"}, "source_claim_ids": ["missing"]}]},
        "claims": {"claims": []},
    }
    report = validate_batch(batch, SCHEMAS)
    assert any("not found" in e for e in report.errors)
