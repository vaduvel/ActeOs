"""Pure tests for the case persistence layer (no live database).

Mirrors the content-publish test style: exercise prepare_rows / validation /
compiled SQL without a real engine. The save/get round-trip against Postgres is
covered by integration tests when a database is available.
"""
from __future__ import annotations

from datetime import date

import pytest

from acteos_api.case_store import (
    CasePersistenceError,
    build_case_statements,
    compiled_case_sql,
    compiled_latest_journey_sql,
    prepare_rows,
    validate_case_row,
    validate_journey_row,
    validate_resolution_snapshot,
)

_RULE_SET_ID = "11111111-1111-1111-1111-111111111111"


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
        "events": [{"event_type_id": "life.identity_card_expired", "status": "resolved"}],
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
    # the snapshot is the lossless case aggregate
    snapshot = journey_row["resolution_snapshot"]
    assert snapshot["id"] == case_row["id"]
    assert snapshot["events"] == _case()["events"]
    assert snapshot["resolution_trace"] == _case()["resolution_trace"]


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
