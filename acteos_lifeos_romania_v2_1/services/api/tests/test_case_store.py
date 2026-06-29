"""Pure tests for the case persistence layer (no live database).

Mirrors the content-publish test style: exercise prepare_rows / validation /
compiled SQL without a real engine. The save/get round-trip against Postgres is
covered by integration tests when a database is available.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import date

import pytest

from acteos_api.case_store import (
    CasePersistenceError,
    build_case_statements,
    compiled_case_sql,
    compiled_latest_journey_sql,
    prepare_projection_rows,
    prepare_rows,
    validate_case_row,
    validate_journey_row,
    validate_requirement_row,
    validate_resolution_snapshot,
    validate_step_row,
)

_RULE_SET_ID = "11111111-1111-1111-1111-111111111111"
_UUID_1 = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
_UUID_2 = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"


def _case(**overrides) -> dict:
    base = {
        "id": "22222222-2222-2222-2222-222222222222",
        "intent_type_id": "ro.intent.identity.renew_expired_id",
        "event_type_id": "life.identity_card_expired",
        "reference_date": "2026-06-26",
        "timezone": "Europe/Bucharest",
        "jurisdiction_path": ["ro", "ro.tm.timisoara"],
        "subject_ref": None,
        "installation_id": "33333333-3333-3333-3333-333333333333",
        "status": "resolved",
        "version": 1,
        "facts_hash": "a" * 64,
        "engine_version": "engine-1",
        "ruleset_version": "rs-1",
        "trust_state": "trusted",
        "events": [
            {
                "event_type_id": "life.identity_card_expired",
                "status": "resolved",
                "included_steps": ["apply_identity_card_expired"],
                "requirements": ["req.identity_photo"],
            }
        ],
        "resolution_trace": {
            "facts_hash": "a" * 64,
            "engine_version": "engine-1",
            "ruleset_version": "rs-1",
        },
        "created_at": "2026-06-26T09:00:00+00:00",
    }
    base.update(overrides)
    return base


def test_prepare_rows_projects_both_tables():
    case_row, journey_row = prepare_rows(_case(), _RULE_SET_ID)
    assert case_row["id"] == "22222222-2222-2222-2222-222222222222"
    assert case_row["reference_date"] == date(2026, 6, 26)
    assert case_row["jurisdiction_path"] == ["ro", "ro.tm.timisoara"]
    assert "created_at" not in case_row  # DB default now()
    assert journey_row["rule_set_id"] == _RULE_SET_ID
    assert journey_row["revision"] == 1
    assert journey_row["reference_date"] == date(2026, 6, 26)
    snapshot = journey_row["resolution_snapshot"]
    assert snapshot["id"] == case_row["id"]
    assert snapshot["events"] == _case()["events"]
    assert snapshot["resolution_trace"] == _case()["resolution_trace"]


def test_prepare_projection_rows_support_string_steps_and_requirements():
    step_rows, requirement_specs = prepare_projection_rows(_case(), "journey-1")
    assert [row["semantic_key"] for row in step_rows] == ["apply_identity_card_expired"]
    assert step_rows[0]["journey_id"] == "journey-1"
    assert step_rows[0]["title_ro"] == "apply_identity_card_expired"
    assert step_rows[0]["instruction_ro"] == "apply_identity_card_expired"
    assert step_rows[0]["status"] == "available"
    assert [row["semantic_key"] for row in requirement_specs] == ["req.identity_photo"]
    assert requirement_specs[0]["journey_step_semantic_key"] == "apply_identity_card_expired"
    assert requirement_specs[0]["title_ro"] == "req.identity_photo"
    assert requirement_specs[0]["obligation"] == "mandatory"
    assert requirement_specs[0]["timing"] == "now"


def test_prepare_projection_rows_preserves_rich_step_and_requirement_objects():
    snapshot = _case(
        events=[
            {
                "event_type_id": "life.identity_card_expired",
                "status": "needs_confirmation",
                "included_steps": [
                    {
                        "id": "apply_identity_card_expired",
                        "template_id": "tmpl.step.identity",
                        "title_ro": "Depune cererea",
                        "instruction_ro": "Mergi la ghi\u0219eu cu actele.",
                        "sequence": 7,
                        "status": "needs_confirmation",
                        "completion_evidence_ro": ["Bon de programare"],
                        "recovery_actions_ro": ["Reprogrameaz\u0103"],
                        "source_claim_ids": [_UUID_1],
                        "requirements": [
                            {
                                "id": "req.identity_photo",
                                "template_id": "tmpl.req.identity_photo",
                                "title_ro": "Fotografie recent\u0103",
                                "description_ro": "Tip pa\u0219aport.",
                                "obligation": "mandatory",
                                "timing": "later",
                                "accepted_forms": ["original"],
                                "readiness_checks": ["is_recent"],
                                "source_claim_ids": [_UUID_2],
                                "status": "ready",
                            }
                        ],
                    }
                ],
            }
        ]
    )
    step_rows, requirement_specs = prepare_projection_rows(snapshot, "journey-2")
    assert step_rows == [
        {
            "journey_id": "journey-2",
            "template_id": "tmpl.step.identity",
            "semantic_key": "apply_identity_card_expired",
            "title_ro": "Depune cererea",
            "instruction_ro": "Mergi la ghi\u0219eu cu actele.",
            "sequence": 7,
            "status": "needs_confirmation",
            "deadline": None,
            "completion_evidence_ro": ["Bon de programare"],
            "recovery_actions_ro": ["Reprogrameaz\u0103"],
            "source_claim_ids": [_UUID_1],
            "version": 1,
        }
    ]
    assert requirement_specs == [
        {
            "journey_step_semantic_key": "apply_identity_card_expired",
            "template_id": "tmpl.req.identity_photo",
            "semantic_key": "req.identity_photo",
                "title_ro": "Fotografie recent\u0103",
                "description_ro": "Tip pa\u0219aport.",
                "obligation": "mandatory",
                "timing": "later",
                "accepted_forms": ["original"],
                "validity": {},
                "readiness_checks": ["is_recent"],
                "source_claim_ids": [_UUID_2],
                "status": "ready",
            "version": 1,
        }
    ]


def test_prepare_projection_rows_adds_synthetic_step_when_event_has_only_requirements():
    snapshot = _case(
        events=[
            {
                "event_type_id": "life.identity_card_expired",
                "status": "resolved",
                "included_steps": [],
                "requirements": ["req.identity_photo"],
            }
        ]
    )
    step_rows, requirement_specs = prepare_projection_rows(snapshot, "journey-3")
    assert [row["semantic_key"] for row in step_rows] == ["life.identity_card_expired::requirements"]
    assert requirement_specs[0]["journey_step_semantic_key"] == "life.identity_card_expired::requirements"


def test_prepare_projection_rows_coerces_invalid_requirement_obligation_and_timing():
    snapshot = _case(
        events=[
            {
                "event_type_id": "life.identity_card_expired",
                "status": "resolved",
                "included_steps": ["apply_identity_card_expired"],
                "requirements": [
                    {
                        "id": "req.identity_photo",
                        "obligation": "derived_from_snapshot",
                        "timing": "derived_from_snapshot",
                    }
                ],
            }
        ]
    )
    _, requirement_specs = prepare_projection_rows(snapshot, "journey-1")
    assert requirement_specs[0]["obligation"] == "mandatory"
    assert requirement_specs[0]["timing"] == "now"


def test_prepare_projection_rows_does_not_mutate_authoritative_snapshot():
    snapshot = _case()
    original = deepcopy(snapshot)
    prepare_projection_rows(snapshot, "journey-4")
    assert snapshot == original


def test_valid_rows_have_no_violations():
    case_row, journey_row = prepare_rows(_case(), _RULE_SET_ID)
    assert validate_case_row(case_row) == []
    assert validate_journey_row(journey_row) == []


def test_missing_identity_is_a_violation():
    case_row, _ = prepare_rows(_case(installation_id=None, user_id=None), _RULE_SET_ID)
    violations = validate_case_row(case_row)
    assert any("identity" in v for v in violations)


def test_user_id_satisfies_identity():
    case_row, _ = prepare_rows(
        _case(installation_id=None, user_id="44444444-4444-4444-4444-444444444444"),
        _RULE_SET_ID,
    )
    assert validate_case_row(case_row) == []


def test_unknown_status_is_a_violation():
    case_row, _ = prepare_rows(_case(status="not_a_status"), _RULE_SET_ID)
    assert any("status_enum" in v for v in validate_case_row(case_row))


def test_bad_facts_hash_length_is_a_violation():
    _, journey_row = prepare_rows(_case(facts_hash="short"), _RULE_SET_ID)
    assert any("facts_hash_len" in v for v in validate_journey_row(journey_row))


def test_resolution_snapshot_header_must_match_journey_header():
    _, journey_row = prepare_rows(_case(), _RULE_SET_ID)
    journey_row["resolution_snapshot"] = {
        **journey_row["resolution_snapshot"],
        "facts_hash": "b" * 64,
    }
    violations = validate_resolution_snapshot(journey_row)
    assert any("snapshot_facts_hash_mismatch" in v for v in violations)


def test_resolution_snapshot_trace_must_match_snapshot_header():
    _, journey_row = prepare_rows(_case(), _RULE_SET_ID)
    journey_row["resolution_snapshot"] = {
        **journey_row["resolution_snapshot"],
        "resolution_trace": {
            **journey_row["resolution_snapshot"]["resolution_trace"],
            "engine_version": "different-engine",
        },
    }
    violations = validate_journey_row(journey_row)
    assert any("trace_engine_version_mismatch" in v for v in violations)


def test_resolution_snapshot_must_keep_events_array_for_replay():
    _, journey_row = prepare_rows(_case(), _RULE_SET_ID)
    journey_row["resolution_snapshot"] = {**journey_row["resolution_snapshot"], "events": None}
    violations = validate_journey_row(journey_row)
    assert any("snapshot_events_array" in v for v in violations)


def test_validate_step_row_catches_missing_columns_and_bad_status():
    step_row = prepare_projection_rows(_case(), "journey-1")[0][0]
    broken = {**step_row, "instruction_ro": None, "status": "not_a_step_status"}
    violations = validate_step_row(broken)
    assert any(":instruction_ro" in v for v in violations)
    assert any("status_enum" in v for v in violations)


def test_validate_requirement_row_catches_missing_columns_and_bad_status():
    requirement_spec = prepare_projection_rows(_case(), "journey-1")[1][0]
    requirement_row = {
        "journey_step_id": "step-1",
        "template_id": requirement_spec["template_id"],
        "semantic_key": requirement_spec["semantic_key"],
        "title_ro": requirement_spec["title_ro"],
        "description_ro": requirement_spec["description_ro"],
        "obligation": None,
        "timing": requirement_spec["timing"],
        "accepted_forms": requirement_spec["accepted_forms"],
        "validity": requirement_spec["validity"],
        "readiness_checks": requirement_spec["readiness_checks"],
        "source_claim_ids": requirement_spec["source_claim_ids"],
        "status": "not_a_requirement_status",
        "version": requirement_spec["version"],
    }
    violations = validate_requirement_row(requirement_row)
    assert any(":obligation" in v for v in violations)
    assert any("status_enum" in v for v in violations)


def test_build_statements_rejects_invalid_rows():
    case_row, journey_row = prepare_rows(_case(installation_id=None, user_id=None), _RULE_SET_ID)
    with pytest.raises(CasePersistenceError):
        build_case_statements(case_row, journey_row)


def test_compiled_sql_targets_both_tables():
    case_row, journey_row = prepare_rows(_case(), _RULE_SET_ID)
    sql = " ".join(compiled_case_sql(case_row, journey_row)).lower()
    assert "app.cases" in sql
    assert "app.journeys" in sql
    assert "on conflict" in sql


def test_compiled_writes_are_append_only_not_update_in_place():
    case_row, journey_row = prepare_rows(_case(), _RULE_SET_ID)
    sql = " ".join(compiled_case_sql(case_row, journey_row)).lower()
    assert "on conflict" in sql
    assert "do nothing" in sql
    assert "do update" not in sql
    assert "update app.cases" not in sql
    assert "update app.journeys" not in sql


def test_compiled_replay_query_uses_latest_journey_snapshot():
    sql = compiled_latest_journey_sql("22222222-2222-2222-2222-222222222222").lower()
    assert "select app.journeys.resolution_snapshot" in sql
    assert "where app.journeys.case_id" in sql
    assert "order by app.journeys.revision desc" in sql
    assert "limit" in sql


def test_prepare_rows_persists_intent_discovery_columns():
    case_row, _ = prepare_rows(
        _case(discovery_source="intent_search", event_context_ids=["life.identity_card_expired"]),
        _RULE_SET_ID,
    )
    assert case_row["intent_type_id"] == "ro.intent.identity.renew_expired_id"
    assert case_row["event_context_ids"] == ["life.identity_card_expired"]
    assert case_row["discovery_source"] == "intent_search"


def test_prepare_rows_defaults_event_context_ids_to_empty_list():
    case_row, _ = prepare_rows(_case(), _RULE_SET_ID)
    assert case_row["event_context_ids"] == []
    assert case_row["discovery_source"] is None


def test_intent_only_case_without_legacy_event_is_valid():
    case_row, _ = prepare_rows(_case(event_type_id=None), _RULE_SET_ID)
    assert case_row["event_type_id"] is None
    assert case_row["intent_type_id"] == "ro.intent.identity.renew_expired_id"
    assert validate_case_row(case_row) == []


def test_case_without_intent_or_event_is_a_violation():
    case_row, _ = prepare_rows(_case(event_type_id=None, intent_type_id=None), _RULE_SET_ID)
    assert any("intent_or_event" in v for v in validate_case_row(case_row))
