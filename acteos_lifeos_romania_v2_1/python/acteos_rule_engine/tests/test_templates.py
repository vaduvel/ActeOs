"""Unit tests for the step/requirement template compiler (in-memory batches)."""

from __future__ import annotations

from acteos_rule_engine.authoring.templates import (
    CompiledTemplates,
    compile_templates,
    template_coverage,
)

_STEP = {
    "id": "apply_minor_passport",
    "title_ro": "Depune cererea de pasaport",
    "instruction_ro": "Prezinta-te la ghiseul SPCEEPS cu documentele si dovada platii.",
    "completion_evidence_ro": ["Bon de programare"],
    "recovery_actions_ro": ["Reprogrameaza online"],
    "sequence_hint": 10,
}

_REQ = {
    "id": "req.minor_birth_certificate",
    "title_ro": "Certificat de nastere al minorului",
    "description_ro": "In original.",
    "obligation": "mandatory",
    "timing": "now",
    "accepted_forms": ["original"],
    "validity": {"max_age_days": None},
    "readiness_checks": ["is_original"],
}


def _batch(steps=None, requirements=None, batch_id="ro.life.test"):
    return {
        "batch_dir": batch_id,
        "ruleset": {"batch_id": batch_id, "rules": []},
        "fixtures": {},
        "claims": None,
        "templates": {
            "step_templates": steps or [],
            "requirement_templates": requirements or [],
        },
    }


def test_compile_step_template_row_shape():
    compiled = compile_templates([_batch(steps=[_STEP])])
    assert isinstance(compiled, CompiledTemplates)
    assert len(compiled.step_templates) == 1
    row = compiled.step_templates[0].as_content_row()
    assert set(row) == {
        "id",
        "semantic_key",
        "title_ro",
        "instruction_ro",
        "sequence_hint",
        "completion_evidence_ro",
        "recovery_actions_ro",
        "status",
    }
    assert row["id"] == "apply_minor_passport"
    assert row["semantic_key"] == "apply_minor_passport"
    assert row["sequence_hint"] == 10
    assert row["completion_evidence_ro"] == ["Bon de programare"]
    assert row["status"] == "draft"


def test_compile_requirement_template_row_shape():
    compiled = compile_templates([_batch(requirements=[_REQ])])
    assert len(compiled.requirement_templates) == 1
    row = compiled.requirement_templates[0].as_content_row()
    assert set(row) == {
        "id",
        "title_ro",
        "description_ro",
        "obligation",
        "timing",
        "accepted_forms",
        "validity",
        "readiness_checks",
        "status",
    }
    assert row["obligation"] == "mandatory"
    assert row["timing"] == "now"
    assert row["accepted_forms"] == ["original"]
    assert row["validity"] == {"max_age_days": None}


def test_semantic_key_defaults_to_id_and_sequence_default():
    step = {k: v for k, v in _STEP.items() if k not in ("sequence_hint",)}
    step.pop("semantic_key", None)
    compiled = compile_templates([_batch(steps=[step])])
    rec = compiled.step_templates[0]
    assert rec.semantic_key == rec.id
    assert rec.sequence_hint == 100


def test_step_missing_instruction_is_deferred():
    bad = {"id": "s.bad", "title_ro": "x"}
    compiled = compile_templates([_batch(steps=[bad])])
    assert compiled.step_templates == []
    assert "step:s.bad:missing_instruction_ro" in compiled.deferred


def test_requirement_invalid_obligation_is_deferred():
    bad = {"id": "r.bad", "title_ro": "x", "obligation": "nope", "timing": "now"}
    compiled = compile_templates([_batch(requirements=[bad])])
    assert compiled.requirement_templates == []
    assert "requirement:r.bad:invalid_obligation" in compiled.deferred


def test_requirement_invalid_timing_is_deferred():
    bad = {"id": "r.bad2", "title_ro": "x", "obligation": "optional", "timing": "soon"}
    compiled = compile_templates([_batch(requirements=[bad])])
    assert compiled.requirement_templates == []
    assert "requirement:r.bad2:invalid_timing" in compiled.deferred


def test_duplicate_step_keeps_first_and_defers():
    dup = {**_STEP, "title_ro": "Alt titlu"}
    compiled = compile_templates([_batch(steps=[_STEP]), _batch(steps=[dup])])
    assert len(compiled.step_templates) == 1
    assert compiled.step_templates[0].title_ro == "Depune cererea de pasaport"
    assert "step:apply_minor_passport:duplicate" in compiled.deferred


def test_compile_is_sorted_and_deterministic():
    extra = {"id": "a_first", "title_ro": "A", "instruction_ro": "i"}
    a = compile_templates([_batch(steps=[_STEP, extra])])
    b = compile_templates([_batch(steps=[extra, _STEP])])
    ids_a = [s.id for s in a.step_templates]
    assert ids_a == sorted(ids_a)
    assert ids_a == [s.id for s in b.step_templates]


def test_template_coverage_reports_missing():
    compiled = compile_templates([_batch(steps=[_STEP], requirements=[_REQ])])
    cov = template_coverage(
        referenced_step_ids=["apply_minor_passport", "ghost_step"],
        referenced_requirement_ids=["req.minor_birth_certificate", "req.ghost"],
        compiled=compiled,
    )
    assert cov.missing_steps == ["ghost_step"]
    assert cov.missing_requirements == ["req.ghost"]
    assert cov.ok is False


def test_template_coverage_ok_when_all_present():
    compiled = compile_templates([_batch(steps=[_STEP])])
    cov = template_coverage(
        referenced_step_ids=["apply_minor_passport"],
        referenced_requirement_ids=[],
        compiled=compiled,
    )
    assert cov.ok is True
