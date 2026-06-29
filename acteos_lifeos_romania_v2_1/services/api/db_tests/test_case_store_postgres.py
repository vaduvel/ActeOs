"""Opt-in Postgres integration tests for DB-backed case replay.

These tests exercise the real ``SqlAlchemyCaseRepository`` against PostgreSQL,
including migrations, FK-backed seed rows, append-only journey revisions, latest
snapshot replay, RLS negative checks, and append-only audit enforcement. They are
intentionally outside ``tests/`` so the fast ``make api-test`` suite remains
DB-free.

Safety guard: the test resets ``app``, ``content`` and ``audit`` schemas before
applying migrations. It only runs when both environment variables are set:

* ``ACTEOS_DATABASE_URL`` -- disposable/local Postgres URL
* ``ACTEOS_DB_TEST_RESET=1`` -- explicit acknowledgement that the target DB may
  be reset
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from acteos_api.case_store import CasePersistenceError, SqlAlchemyCaseRepository

PACK_ROOT = Path(__file__).resolve().parents[3]
MIGRATIONS = sorted((PACK_ROOT / "db").glob("[0-9][0-9][0-9][0-9]_*.sql"))

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
RLS_ROLE = "acteos_rls_test_user"
USER_ID = "55555555-5555-5555-5555-555555555555"
OTHER_USER_ID = "66666666-6666-6666-6666-666666666666"
RLS_CASE_ID = "77777777-7777-7777-7777-777777777777"


@pytest.fixture(scope="module")
def engine() -> Engine:
    assert DATABASE_URL is not None
    engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)
    _reset_and_migrate(engine)
    _seed_minimal_content(engine)
    _seed_rls_role(engine)
    yield engine
    engine.dispose()


def _reset_and_migrate(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.exec_driver_sql("drop schema if exists audit cascade")
        conn.exec_driver_sql("drop schema if exists app cascade")
        conn.exec_driver_sql("drop schema if exists content cascade")
        _ensure_local_auth_uid(conn)
        for migration_path in MIGRATIONS:
            sql = migration_path.read_text(encoding="utf-8")
            for statement in _split_sql(sql):
                conn.exec_driver_sql(statement)


def _ensure_local_auth_uid(conn: Any) -> None:
    """Provide the Supabase-compatible auth.uid() helper in local Postgres.

    ``db/0003_rls.sql`` is intentionally written for Supabase and references
    ``auth.uid()``. Local disposable Postgres does not ship that schema, so the
    integration test creates a compatible function backed by the common
    ``request.jwt.claim.sub`` setting before applying the RLS migration.
    """

    conn.exec_driver_sql("create schema if not exists auth")
    conn.exec_driver_sql(
        """
        create or replace function auth.uid()
        returns uuid
        language sql
        stable
        as $$
            select nullif(current_setting('request.jwt.claim.sub', true), '')::uuid
        $$
        """
    )


def _split_sql(sql: str) -> list[str]:
    """Split migration SQL into executable statements without breaking on comments.

    We intentionally keep the integration test independent from a local ``psql``
    binary, but the migrations still contain semicolons inside comments and may
    later contain dollar-quoted functions. A naive ``split(';')`` turns comment
    tails into bogus SQL statements, so we scan the file and only split on
    statement terminators that are outside strings, identifiers, dollar-quoted
    bodies and comments.
    """

    statements: list[str] = []
    current: list[str] = []
    in_single_quote = False
    in_double_quote = False
    in_line_comment = False
    in_block_comment = False
    dollar_tag: str | None = None
    idx = 0

    while idx < len(sql):
        ch = sql[idx]
        nxt = sql[idx + 1] if idx + 1 < len(sql) else ""

        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
                current.append(ch)
            idx += 1
            continue

        if in_block_comment:
            if ch == "*" and nxt == "/":
                in_block_comment = False
                idx += 2
            else:
                idx += 1
            continue

        if dollar_tag is not None:
            if sql.startswith(dollar_tag, idx):
                current.append(dollar_tag)
                idx += len(dollar_tag)
                dollar_tag = None
            else:
                current.append(ch)
                idx += 1
            continue

        if in_single_quote:
            current.append(ch)
            if ch == "'" and nxt == "'":
                current.append(nxt)
                idx += 2
                continue
            if ch == "'":
                in_single_quote = False
            idx += 1
            continue

        if in_double_quote:
            current.append(ch)
            if ch == '"' and nxt == '"':
                current.append(nxt)
                idx += 2
                continue
            if ch == '"':
                in_double_quote = False
            idx += 1
            continue

        if ch == "-" and nxt == "-":
            in_line_comment = True
            idx += 2
            continue

        if ch == "/" and nxt == "*":
            in_block_comment = True
            idx += 2
            continue

        if ch == "'":
            in_single_quote = True
            current.append(ch)
            idx += 1
            continue

        if ch == '"':
            in_double_quote = True
            current.append(ch)
            idx += 1
            continue

        if ch == "$":
            match = re.match(r"^\$[A-Za-z_][A-Za-z0-9_]*\$|^\$\$", sql[idx:])
            if match:
                dollar_tag = match.group(0)
                current.append(dollar_tag)
                idx += len(dollar_tag)
                continue

        if ch == ";":
            statement = "".join(current).strip()
            if statement:
                statements.append(statement)
            current = []
            idx += 1
            continue

        current.append(ch)
        idx += 1

    tail = "".join(current).strip()
    if tail:
        statements.append(tail)

    return statements


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
                insert into content.intent_categories (
                    id, title_ro, display_order, status, catalog_version
                ) values (
                    'identity_documents', 'Acte de identitate', 1, 'active', '2.1.0-it'
                )
                """
            )
        )
        conn.execute(
            text(
                """
                insert into content.intent_types (
                    id, category_id, kind, title_ro, outcome_ro, jurisdiction_scope,
                    release_wave, research_status, production_status, availability_policy,
                    catalog_version
                ) values (
                    'ro.intent.identity.renew_expired_id', 'identity_documents', 'direct_goal',
                    'Reînnoiește buletinul expirat', 'Act de identitate valabil', 'mixed',
                    'R1A', 'required', 'not_available', 'source_required', '2.1.0-it'
                )
                """
            )
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


def _seed_rls_role(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.exec_driver_sql(
            f"""
            do $$
            begin
                if not exists (select 1 from pg_roles where rolname = '{RLS_ROLE}') then
                    create role {RLS_ROLE} nosuperuser nocreatedb nocreaterole;
                else
                    alter role {RLS_ROLE} with nosuperuser nocreatedb nocreaterole;
                end if;
            end
            $$
            """
        )
        conn.exec_driver_sql(f"grant {RLS_ROLE} to current_user")
        conn.exec_driver_sql(f"grant usage on schema app to {RLS_ROLE}")
        conn.exec_driver_sql(f"grant usage on schema auth to {RLS_ROLE}")
        conn.exec_driver_sql(f"grant execute on function auth.uid() to {RLS_ROLE}")
        conn.exec_driver_sql(f"grant select on app.cases, app.journeys to {RLS_ROLE}")


def _set_jwt_subject(conn: Any, subject: str) -> None:
    conn.execute(text("select set_config('request.jwt.claim.sub', :subject, false)"), {"subject": subject})


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
        "discovery_source": "intent_search",
        "event_context_ids": [EVENT_TYPE_ID],
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
        latest_journey_id = conn.execute(
            text("select id from app.journeys where case_id = :case_id and revision = 2"),
            {"case_id": CASE_ID},
        ).scalar_one()
        projected_steps = conn.execute(
            text(
                """
                select semantic_key, title_ro, sequence, status
                from app.journey_steps
                where journey_id = :journey_id
                order by sequence, semantic_key
                """
            ),
            {"journey_id": latest_journey_id},
        ).mappings().all()
        projected_requirements = conn.execute(
            text(
                """
                select jr.semantic_key, jr.title_ro, jr.status, js.semantic_key as step_semantic_key
                from app.journey_requirements jr
                join app.journey_steps js on js.id = jr.journey_step_id
                where js.journey_id = :journey_id
                order by jr.semantic_key
                """
            ),
            {"journey_id": latest_journey_id},
        ).mappings().all()

    assert case_count == 1
    assert journey_revisions == [1, 2]
    assert [row["semantic_key"] for row in projected_steps] == ["apply_identity_card_expired"]
    assert projected_steps[0]["title_ro"] == "apply_identity_card_expired"
    assert projected_steps[0]["status"] == "needs_confirmation"
    assert [row["semantic_key"] for row in projected_requirements] == [
        "req.address_proof",
        "req.identity_photo",
    ]
    assert {row["step_semantic_key"] for row in projected_requirements} == {
        "apply_identity_card_expired"
    }
    assert {row["status"] for row in projected_requirements} == {"missing"}


def test_case_row_persists_intent_discovery_columns(engine: Engine):
    repo = SqlAlchemyCaseRepository(engine)
    case_id = "88888888-8888-8888-8888-888888888888"
    repo.save(_case(id=case_id, facts_hash="e" * 64))
    with engine.connect() as conn:
        row = conn.execute(
            text(
                "select intent_type_id, event_context_ids, discovery_source "
                "from app.cases where id = :case_id"
            ),
            {"case_id": case_id},
        ).mappings().one()
    assert row["intent_type_id"] == "ro.intent.identity.renew_expired_id"
    assert row["event_context_ids"] == [EVENT_TYPE_ID]
    assert row["discovery_source"] == "intent_search"


def test_intent_only_case_persists_without_legacy_event(engine: Engine):
    repo = SqlAlchemyCaseRepository(engine)
    case_id = "99999999-9999-9999-9999-999999999999"
    repo.save(_case(id=case_id, event_type_id=None, facts_hash="f" * 64))
    with engine.connect() as conn:
        row = conn.execute(
            text("select event_type_id, intent_type_id from app.cases where id = :case_id"),
            {"case_id": case_id},
        ).mappings().one()
    assert row["event_type_id"] is None
    assert row["intent_type_id"] == "ro.intent.identity.renew_expired_id"


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


def test_rls_hides_cases_and_journeys_from_other_users(engine: Engine):
    repo = SqlAlchemyCaseRepository(engine)
    repo.save(
        _case(
            id=RLS_CASE_ID,
            user_id=USER_ID,
            installation_id=None,
            facts_hash="d" * 64,
        )
    )

    with engine.begin() as conn:
        conn.exec_driver_sql(f"set local role {RLS_ROLE}")
        _set_jwt_subject(conn, USER_ID)
        visible_cases = conn.execute(
            text("select count(*) from app.cases where id = :case_id"), {"case_id": RLS_CASE_ID}
        ).scalar_one()
        visible_journeys = conn.execute(
            text("select count(*) from app.journeys where case_id = :case_id"),
            {"case_id": RLS_CASE_ID},
        ).scalar_one()

    with engine.begin() as conn:
        conn.exec_driver_sql(f"set local role {RLS_ROLE}")
        _set_jwt_subject(conn, OTHER_USER_ID)
        hidden_cases = conn.execute(
            text("select count(*) from app.cases where id = :case_id"), {"case_id": RLS_CASE_ID}
        ).scalar_one()
        hidden_journeys = conn.execute(
            text("select count(*) from app.journeys where case_id = :case_id"),
            {"case_id": RLS_CASE_ID},
        ).scalar_one()

    assert visible_cases == 1
    assert visible_journeys == 1
    assert hidden_cases == 0
    assert hidden_journeys == 0


def test_audit_events_are_append_only(engine: Engine):
    with engine.begin() as conn:
        audit_id = conn.execute(
            text(
                """
                insert into audit.events (actor_type, actor_id, action, entity_type, entity_id, request_id)
                values ('system', 'db-test', 'case.replayed', 'case', :case_id, 'req-db-test')
                returning id
                """
            ),
            {"case_id": CASE_ID},
        ).scalar_one()

    with pytest.raises(SQLAlchemyError):
        with engine.begin() as conn:
            conn.execute(
                text("update audit.events set action = 'case.tampered' where id = :audit_id"),
                {"audit_id": audit_id},
            )

    with pytest.raises(SQLAlchemyError):
        with engine.begin() as conn:
            conn.execute(text("delete from audit.events where id = :audit_id"), {"audit_id": audit_id})

    with engine.connect() as conn:
        row = conn.execute(
            text("select action from audit.events where id = :audit_id"), {"audit_id": audit_id}
        ).one()

    assert row[0] == "case.replayed"
