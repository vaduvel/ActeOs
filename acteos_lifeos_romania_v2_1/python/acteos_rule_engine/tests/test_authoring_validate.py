import pytest

pytest.importorskip("jsonschema")
pytest.importorskip("referencing")

from acteos_rule_engine.authoring.validate import (
    CLAIM_SCHEMA,
    PREDICATE_SCHEMA,
    REQUIREMENT_TEMPLATE_SCHEMA,
    RULE_SCHEMA,
    STEP_TEMPLATE_SCHEMA,
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
STEP = {
    "$id": "https://acteos/schemas/step_template.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["id"],
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "semantic_key": {"type": "string"},
        "title_ro": {"type": "string"},
        "instruction_ro": {"type": "string"},
        "sequence_hint": {"type": "integer", "minimum": 0},
        "completion_evidence_ro": {"type": "array", "items": {"type": "string"}},
        "recovery_actions_ro": {"type": "array", "items": {"type": "string"}},
        "status": {"type": "string"},
    },
    "additionalProperties": False,
}
REQ = {
    "$id": "https://acteos/schemas/requirement_template.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["id"],
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "title_ro": {"type": "string"},
        "description_ro": {"type": "string"},
        "obligation": {"type": "string", "enum": ["mandatory", "conditional", "optional"]},
        "timing": {"type": "string", "enum": ["now", "later"]},
        "accepted_forms": {"type": "array", "items": {"type": "string"}},
        "validity": {"type": "object"},
        "readiness_checks": {"type": "array", "items": {"type": "string"}},
        "status": {"type": "string"},
    },
    "additionalProperties": False,
}
SCHEMAS = {RULE_SCHEMA: RULE, CLAIM_SCHEMA: CLAIM, PREDICATE_SCHEMA: PRED}
SCHEMAS_T = {
    RULE_SCHEMA: RULE,
    CLAIM_SCHEMA: CLAIM,
    PREDICATE_SCHEMA: PRED,
    STEP_TEMPLATE_SCHEMA: STEP,
    REQUIREMENT_TEMPLATE_SCHEMA: REQ,
}


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


def test_valid_templates_pass():
    batch = {
        "ruleset": {"batch_id": "T", "rules": []},
        "claims": {"claims": []},
        "templates": {
            "step_templates": [{"id": "apply_x", "title_ro": "Depune", "instruction_ro": "Mergi."}],
            "requirement_templates": [
                {"id": "req.x", "title_ro": "Cert", "obligation": "mandatory", "timing": "now"}
            ],
        },
    }
    report = validate_batch(batch, SCHEMAS_T)
    assert report.ok, report.errors


def test_invalid_obligation_enum_flagged():
    batch = {
        "ruleset": {"batch_id": "T", "rules": []},
        "claims": {"claims": []},
        "templates": {
            "requirement_templates": [{"id": "req.x", "obligation": "maybe", "timing": "now"}]
        },
    }
    report = validate_batch(batch, SCHEMAS_T)
    assert not report.ok
    assert any("requirement_template req.x" in e for e in report.errors)


def test_unknown_step_field_flagged():
    batch = {
        "ruleset": {"batch_id": "T", "rules": []},
        "claims": {"claims": []},
        "templates": {"step_templates": [{"id": "s", "typo_field": 1}]},
    }
    report = validate_batch(batch, SCHEMAS_T)
    assert not report.ok
    assert any("step_template s" in e for e in report.errors)


def test_templates_skipped_when_schema_absent():
    # SCHEMAS has no template schemas -> structurally bad templates are ignored.
    batch = {
        "ruleset": {"batch_id": "T", "rules": []},
        "claims": {"claims": []},
        "templates": {"step_templates": [{"id": "s", "bogus": True}]},
    }
    report = validate_batch(batch, SCHEMAS)
    assert report.ok, report.errors
