"""Opt-in Postgres integration tests for app.journey_step_dependencies.

These tests exercise the real DB-level constraints on the journey step
dependency edge table against PostgreSQL: the self-dependency check, the
composite primary key, the foreign keys to ``app.journey_steps`` and the
``on delete cascade`` behaviour from both ``app.journey_steps`` and
``app.journeys``.

They are intentionally kept self-contained (separate from
``test_case_store_postgres.py``) so the proven case-store suite is untouched.

Safety guard: the module resets ``app``, ``content`` and ``audit`` schemas
before applying migrations. It only runs when both environment variables are
set:

* ``ACTEOS_DATABASE_URL`` -- disposable/local Postgres URL
* ``ACTEOS_DB_TEST_RESET=1`` -- explicit acknowledgement that the target DB may
  be reset
"""
from __future__ import annotations

import os
import re
import uuid
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

PACK_ROOT = Path(__file__).resolve().parents[3]
MIGRATIONS = sorted((PACK_ROOT / "db").glob("[0-9][0-9][0-9][0-9]_*.sql"))

DATABASE_URL = os.environ.get("ACTEOS_DATABASE_URL")
ALLOW_RESET = os.environ.get("ACTEOS_DB_TEST_RESET") == "1"

pytestmark = pytest.mark.skipif(
    not DATABASE_URL or not ALLOW_RESET,
    reason="requires ACTEOS_DATABASE_URL and ACTEOS_DB_TEST_RESET=1 for a disposable Postgres DB",
)

INSTALLATION_ID = "33333333-3333-3333-3333-333333333333"
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
        _ensure_local_auth_uid(conn)
        for migration_path in MIGRATIONS:
            sql = migration_path.read_text(encoding="utf-8")
            for statement in _split_sql(sql):
                conn.exec_driver_sql(statement)


def _ensure_local_auth_uid(conn: Any) -> None:
    """Provide the Supabase-compatible auth.uid() helper in local Postgres."""

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
    """Split migration SQL into executable statements without breaking on comments."""

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
                    :id, 'identity_documents', 'Imi expira cartea de identitate', '[]'::jsonb,
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


def _make_journey_with_steps(engine: Engine, step_keys: list[str]) -> tuple[str, dict[str, str]]:
    """Create an isolated case + journey + steps with fresh UUIDs.

    Returns the journey id and a mapping of semantic_key -> step id so each test
    can wire dependencies between known steps without colliding with other
    tests that share the module-scoped engine.
    """

    case_id = str(uuid.uuid4())
    journey_id = str(uuid.uuid4())
    step_ids: dict[str, str] = {key: str(uuid.uuid4()) for key in step_keys}
    with engine.begin() as conn:
        rule_set_id = conn.execute(
            text("select id from content.rule_sets where version = :version"),
            {"version": RULESET_VERSION},
        ).scalar_one()
        conn.execute(
            text(
                """
                insert into app.cases (
                    id, installation_id, event_type_id, reference_date,
                    jurisdiction_path, status
                ) values (
                    :id, :installation_id, :event_type_id, date '2026-06-27',
                    ARRAY['ro', 'ro.tm.timisoara'], 'resolved'
                )
                """
            ),
            {
                "id": case_id,
                "installation_id": INSTALLATION_ID,
                "event_type_id": EVENT_TYPE_ID,
            },
        )
        conn.execute(
            text(
                """
                insert into app.journeys (
                    id, case_id, revision, rule_set_id, ruleset_version,
                    reference_date, facts_hash, engine_version, trust_state,
                    resolution_trace
                ) values (
                    :id, :case_id, 1, :rule_set_id, :ruleset_version,
                    date '2026-06-27', :facts_hash, 'engine-dep-it', 'trusted',
                    '{}'::jsonb
                )
                """
            ),
            {
                "id": journey_id,
                "case_id": case_id,
                "rule_set_id": rule_set_id,
                "ruleset_version": RULESET_VERSION,
                "facts_hash": "a" * 64,
            },
        )
        for sequence, key in enumerate(step_keys, start=1):
            conn.execute(
                text(
                    """
                    insert into app.journey_steps (
                        id, journey_id, semantic_key, title_ro, instruction_ro,
                        sequence, status
                    ) values (
                        :id, :journey_id, :semantic_key, :semantic_key,
                        'instructiune de test', :sequence, 'available'
                    )
                    """
                ),
                {
                    "id": step_ids[key],
                    "journey_id": journey_id,
                    "semantic_key": key,
                    "sequence": sequence,
                },
            )
    return journey_id, step_ids


def _add_dependency(
    conn: Any, journey_id: str, step_id: str, depends_on_step_id: str
) -> None:
    conn.execute(
        text(
            """
            insert into app.journey_step_dependencies (
                journey_id, step_id, depends_on_step_id
            ) values (
                :journey_id, :step_id, :depends_on_step_id
            )
            """
        ),
        {
            "journey_id": journey_id,
            "step_id": step_id,
            "depends_on_step_id": depends_on_step_id,
        },
    )


def test_valid_dependency_persists(engine: Engine):
    journey_id, steps = _make_journey_with_steps(engine, ["dep.a", "dep.b"])
    with engine.begin() as conn:
        _add_dependency(conn, journey_id, steps["dep.b"], steps["dep.a"])
    with engine.connect() as conn:
        count = conn.execute(
            text(
                """
                select count(*) from app.journey_step_dependencies
                where step_id = :step_id and depends_on_step_id = :depends_on
                """
            ),
            {"step_id": steps["dep.b"], "depends_on": steps["dep.a"]},
        ).scalar_one()
    assert count == 1


def test_self_dependency_is_rejected(engine: Engine):
    journey_id, steps = _make_journey_with_steps(engine, ["dep.self"])
    with pytest.raises(SQLAlchemyError):
        with engine.begin() as conn:
            _add_dependency(conn, journey_id, steps["dep.self"], steps["dep.self"])


def test_duplicate_dependency_is_rejected(engine: Engine):
    journey_id, steps = _make_journey_with_steps(engine, ["dep.dup_a", "dep.dup_b"])
    with engine.begin() as conn:
        _add_dependency(conn, journey_id, steps["dep.dup_b"], steps["dep.dup_a"])
    with pytest.raises(SQLAlchemyError):
        with engine.begin() as conn:
            _add_dependency(conn, journey_id, steps["dep.dup_b"], steps["dep.dup_a"])


def test_dependency_requires_existing_target_step(engine: Engine):
    journey_id, steps = _make_journey_with_steps(engine, ["dep.fk"])
    missing_step_id = str(uuid.uuid4())
    with pytest.raises(SQLAlchemyError):
        with engine.begin() as conn:
            _add_dependency(conn, journey_id, steps["dep.fk"], missing_step_id)


def test_step_delete_cascades_dependencies(engine: Engine):
    journey_id, steps = _make_journey_with_steps(
        engine, ["dep.casc_a", "dep.casc_b", "dep.casc_c"]
    )
    with engine.begin() as conn:
        _add_dependency(conn, journey_id, steps["dep.casc_b"], steps["dep.casc_a"])
        _add_dependency(conn, journey_id, steps["dep.casc_c"], steps["dep.casc_b"])
    with engine.begin() as conn:
        conn.execute(
            text("delete from app.journey_steps where id = :id"),
            {"id": steps["dep.casc_b"]},
        )
    with engine.connect() as conn:
        remaining = conn.execute(
            text(
                """
                select count(*) from app.journey_step_dependencies
                where step_id = :b or depends_on_step_id = :b
                """
            ),
            {"b": steps["dep.casc_b"]},
        ).scalar_one()
        surviving_steps = conn.execute(
            text("select count(*) from app.journey_steps where journey_id = :journey_id"),
            {"journey_id": journey_id},
        ).scalar_one()
    assert remaining == 0
    assert surviving_steps == 2


def test_journey_delete_cascades_steps_and_dependencies(engine: Engine):
    journey_id, steps = _make_journey_with_steps(engine, ["dep.jdel_a", "dep.jdel_b"])
    with engine.begin() as conn:
        _add_dependency(conn, journey_id, steps["dep.jdel_b"], steps["dep.jdel_a"])
    with engine.begin() as conn:
        conn.execute(text("delete from app.journeys where id = :id"), {"id": journey_id})
    with engine.connect() as conn:
        dep_count = conn.execute(
            text(
                "select count(*) from app.journey_step_dependencies where journey_id = :journey_id"
            ),
            {"journey_id": journey_id},
        ).scalar_one()
        step_count = conn.execute(
            text("select count(*) from app.journey_steps where journey_id = :journey_id"),
            {"journey_id": journey_id},
        ).scalar_one()
    assert dep_count == 0
    assert step_count == 0
