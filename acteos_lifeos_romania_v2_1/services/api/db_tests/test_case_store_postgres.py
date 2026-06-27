"""Opt-in Postgres integration tests for DB-backed case replay.

These tests exercise the real ``SqlAlchemyCaseRepository`` against PostgreSQL,
including migrations, FK-backed seed rows, append-only journey revisions, and
latest-snapshot replay. They are intentionally outside ``tests/`` so the fast
``make api-test`` suite remains DB-free.

Safety guard: the test resets ``app``, ``content`` and ``audit`` schemas before
applying migrations. It only runs when both environment variables are set:

* ``ACTEOS_DATABASE_URL`` -- disposable/local Postgres URL
* ``ACTEOS_DB_TEST_RESET=1`` -- explicit acknowledgement that the target DB may
  be reset
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from acteos_api.case_store import CasePersistenceError, SqlAlchemyCaseRepository

PACK_ROOT = Path(__file__).resolve().parents[3]
MIGRATIONS = [PACK_ROOT / "db" / "0001_init.sql", PACK_ROOT / "db" / "0002_case_resolution_snapshot.sql"]

DATABASE_URL = os.environ.get("ACTEOS_DATABASE_URL")
ALLOW_RESET = os.environ.get("ACTEOS_DB_TEST_RESET") == "1"

pytestmark = pytest.mark.skipif(
    not DATABASE_URL or not ALLOW_RESET,
    reason="requires ACTEOS_DATABASE_URL and ACTEOS_DB_TEST_RESET=1 for a disposable Postgres DB",
)

INSTALLATION_ID = "33333333-3333-3333-3333-333333333333"
CASE_ID = "22222222-2222-2222-2222-222222222222"
EVENT_TYPE_ID = "life.identity_card_expired"
RULESET_VERSION = "rs-it-1"


@pytest.fixture(scope="module")
def engine() -> Engine:
    assert DATABASE_URL is not None
    engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)
    _reset_and_migrate(engine)
    _seed_minimal_content(engine)
    yield engine
    engine.dispose()


def _reset_and_migrate(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.exec_driver_sql("drop schema if exists audit cascade")
        conn.exec_driver_sql("drop schema if exists app cascade")
        conn.exec_driver_sql("drop schema if exists content cascade")
        for migration_path in MIGRATIONS:
            sql = migration_path.read_text(encoding="utf-8")
            for statement in _split_sql(sql):
                conn.exec_driver_sql(statement)


def _split_sql(sql: str) -> list[str]:
    """Split the current plain-SQL migrations into executable statements.

    The current migration files contain no dollar-quoted functions/procedures, so
    semicolon splitting is sufficient and keeps the integration test independent
    from a local ``psql`` binary.
    """

    return [statement.strip() for statement in sql.split(";") if statement.strip()]


def _seed_minimal_content(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                insert into app.installations (id, anonymous_subject_hash, platform, app_version)
                values (:id, 'integration-subject-hash', 'android', 'it')
                """
            ),
            {"id": INSTALLATION_ID},
        )
        conn.execute(
            text(
                """
                insert into content.life_event_types (
                    id, category_id, title_ro, trigger_phrases_ro, release_wave,
                    research_status, production_status, schema_version
                ) values (
                    :id, 'identity_documents', 'Îmi expiră cartea de identitate', '[]'::jsonb,
                    'R1A', 'required', 'not_available', '2.1.0'
                )
                """
            ),
            {"id": EVENT_TYPE_ID},
        )
        conn.execute(
            text(
                """
                insert into content.rule_sets (
                    version, scope, schema_version, engine_compatibility,
                    manifest_sha256, status, approved_by
                ) values (
                    :version, ARRAY['R1A'], '2.1.0', '2.1.0', :manifest_sha256,
                    'active', ARRAY[]::uuid[]
                )
                """
            ),
            {"version": RULESET_VERSION, "manifest_sha256": "c" * 64},
        )


def _case(**overrides: Any) -> dict[str, Any]:
    version = overrides.get("version", 1)
    facts_hash = overrides.get("facts_hash", "a" * 64)
    engine_version = overrides.get("engine_version", "engine-it-1")
    base: dict[str, Any] = {
        "id": CASE_ID,
        "intent_type_id": "ro.intent.identity.renew_expired_id",
        "event_type_id": EVENT_TYPE_ID,
        "reference_date": "2026-06-27",
        "timezone": "Europe/Bucharest",
        "jurisdiction_path": ["ro", "ro.tm.timisoara"],
        "subject_ref": None,
        "installation_id": INSTALLATION_ID,
        "status": "resolved",
        "version": version,
        "facts_hash": facts_hash,
        "engine_version": engine_version,
        "ruleset_version": RULESET_VERSION,
        "trust_state": "trusted",
        "events": [
            {
                "event_type_id": EVENT_TYPE_ID,
                "status": "resolved",
                "included_steps": ["apply_identity_card_expired"],
                "requirements": ["req.identity_photo"],
            }
        ],
        "resolution_trace": {
            "facts_hash": facts_hash,
            "engine_version": engine_version,
            "ruleset_version": RULESET_VERSION,
            "included_rule_ids": ["rule.exp.docs"],
            "excluded_rule_ids": [],
            "root_event_type_id": EVENT_TYPE_ID,
            "event_type_ids": [EVENT_TYPE_ID],
            "intent_type_id": "ro.intent.identity.renew_expired_id",
        },
        "created_at": "2026-06-27T10:00:00+00:00",
    }
    base.update(overrides)
    return base


def test_sqlalchemy_case_repository_persists_and_replays_latest_snapshot(engine: Engine):
    repo = SqlAlchemyCaseRepository(engine)

    saved_v1 = repo.save(_case())
    assert saved_v1["version"] == 1

    saved_v2 = repo.save(
        _case(
            version=2,
            facts_hash="b" * 64,
            engine_version="engine-it-2",
            events=[
                {
                    "event_type_id": EVENT_TYPE_ID,
                    "status": "needs_confirmation",
                    "included_steps": ["apply_identity_card_expired"],
                    "requirements": ["req.identity_photo", "req.address_proof"],
                }
            ],
            status="needs_confirmation",
            trust_state="needs_review",
        )
    )
    assert saved_v2["version"] == 2

    replayed = repo.get(CASE_ID)
    assert replayed is not None
    assert replayed["id"] == CASE_ID
    assert replayed["version"] == 2
    assert replayed["facts_hash"] == "b" * 64
    assert replayed["engine_version"] == "engine-it-2"
    assert replayed["status"] == "needs_confirmation"
    assert replayed["events"][0]["requirements"] == ["req.identity_photo", "req.address_proof"]
    assert replayed["resolution_trace"]["facts_hash"] == replayed["facts_hash"]

    with engine.connect() as conn:
        case_count = conn.execute(
            text("select count(*) from app.cases where id = :case_id"), {"case_id": CASE_ID}
        ).scalar_one()
        journey_revisions = conn.execute(
            text("select revision from app.journeys where case_id = :case_id order by revision"),
            {"case_id": CASE_ID},
        ).scalars().all()

    assert case_count == 1
    assert journey_revisions == [1, 2]


def test_sqlalchemy_case_repository_rejects_unpublished_ruleset(engine: Engine):
    repo = SqlAlchemyCaseRepository(engine)
    missing_ruleset_case = _case(
        id="44444444-4444-4444-4444-444444444444",
        ruleset_version="rs-not-published",
    )

    with pytest.raises(CasePersistenceError, match="ruleset_version 'rs-not-published' is not published"):
        repo.save(missing_ruleset_case)

    with engine.connect() as conn:
        persisted = conn.execute(
            text("select count(*) from app.cases where id = :case_id"),
            {"case_id": missing_ruleset_case["id"]},
        ).scalar_one()
    assert persisted == 0
