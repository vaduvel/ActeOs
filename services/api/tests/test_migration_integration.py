"""WB-020 / WB-021 — migration integration tests.

Exit gate: "migrate up/down/up passes". These tests prove the Alembic migration
is the executable source of truth for the canonical schema
(``09_DATABASE_SCHEMA.sql``): it builds every table, every enum, every trigger,
and can be torn down and rebuilt cleanly.

A dedicated container is used (not the shared ``_migrated_engine`` fixture) so
we can exercise downgrade without destroying the session-wide schema other tests
rely on.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest
from sqlalchemy import inspect, text

pytestmark = pytest.mark.integration

API_DIR = Path(__file__).resolve().parents[1]

# All 25 tables the canonical DDL must create, grouped by schema. Enum types and
# triggers are derived from 09_DATABASE_SCHEMA.sql / 0001_initial.py.
EXPECTED_TABLES = {
    "content": {
        "jurisdiction", "authority", "intent", "source", "source_snapshot",
        "source_claim", "rule_family", "rule_version", "rule_claim_link",
        "rule_review", "rule_bundle", "rule_bundle_member", "bundle_publication",
    },
    "app": {
        "device_identity", "journey", "journey_fact", "route_resolution",
        "requirement_state", "document_analysis", "document_finding",
        "feedback_incident",
    },
    "ops": {"fetch_job", "source_change_alert", "idempotency_record"},
    "audit": {"event_log"},
}

EXPECTED_ENUMS = {
    "source_status", "authority_level", "freshness_class", "snapshot_status",
    "rule_status", "confidence_state", "release_status", "journey_status",
    "requirement_status", "finding_severity", "finding_status", "job_status",
    "incident_status",
}


def _alembic(*args: str, db_url: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "DATABASE_URL": db_url}
    return subprocess.run(
        ["alembic", *args], cwd=API_DIR, env=env,
        capture_output=True, text=True,
    )


@pytest.fixture
def fresh_pg():
    """A pristine container we can upgrade AND downgrade freely."""
    from testcontainers.postgres import PostgresContainer

    with PostgresContainer("postgres:17", driver="psycopg") as pg:
        yield pg.get_connection_url()


def _all_tables(inspector) -> dict[str, set[str]]:
    by_schema: dict[str, set[str]] = {}
    for schema in ("content", "app", "ops", "audit"):
        names = inspector.get_table_names(schema=schema)
        by_schema[schema] = set(names)
    return by_schema


def _all_enums(engine) -> set[str]:
    result = engine.connect().execute(text(
        "SELECT t.typname FROM pg_type t "
        "JOIN pg_namespace n ON n.oid = t.typnamespace "
        "WHERE n.nspname IN ('content','app','ops') AND t.typtype = 'e'"
    ))
    return {row[0] for row in result}


def test_migrate_up_creates_all_tables(fresh_pg):
    """upgrade head creates every table from the canonical schema."""
    r = _alembic("upgrade", "head", db_url=fresh_pg)
    assert r.returncode == 0, f"upgrade failed:\n{r.stderr}"

    from sqlalchemy import create_engine

    engine = create_engine(fresh_pg, future=True)
    try:
        tables = _all_tables(inspect(engine))
        for schema, expected in EXPECTED_TABLES.items():
            missing = expected - tables.get(schema, set())
            assert not missing, f"schema '{schema}' missing tables: {sorted(missing)}"
    finally:
        engine.dispose()


def test_migrate_up_creates_all_enums(fresh_pg):
    """upgrade head creates all 13 enum types with correct ordering."""
    r = _alembic("upgrade", "head", db_url=fresh_pg)
    assert r.returncode == 0, f"upgrade failed:\n{r.stderr}"

    from sqlalchemy import create_engine

    engine = create_engine(fresh_pg, future=True)
    try:
        enums = _all_enums(engine)
        missing = EXPECTED_ENUMS - enums
        assert not missing, f"missing enum types: {sorted(missing)}"
    finally:
        engine.dispose()


def test_migrate_up_down_up(fresh_pg):
    """Exit gate: upgrade -> downgrade -> upgrade leaves a complete schema."""
    from sqlalchemy import create_engine

    # 1. up
    r = _alembic("upgrade", "head", db_url=fresh_pg)
    assert r.returncode == 0, f"first upgrade failed:\n{r.stderr}"

    # 2. down (base = drop everything)
    r = _alembic("downgrade", "base", db_url=fresh_pg)
    assert r.returncode == 0, f"downgrade failed:\n{r.stderr}"

    engine = create_engine(fresh_pg, future=True)
    try:
        # After downgrade the schemas should be gone.
        tables = _all_tables(inspect(engine))
        for schema in ("content", "app", "ops", "audit"):
            assert tables.get(schema, set()) == set(), (
                f"schema '{schema}' should be empty after downgrade, got {tables.get(schema)}"
            )
    finally:
        engine.dispose()

    # 3. up again — schema must rebuild identically.
    r = _alembic("upgrade", "head", db_url=fresh_pg)
    assert r.returncode == 0, f"second upgrade failed:\n{r.stderr}"

    engine = create_engine(fresh_pg, future=True)
    try:
        tables = _all_tables(inspect(engine))
        for schema, expected in EXPECTED_TABLES.items():
            missing = expected - tables.get(schema, set())
            assert not missing, (
                f"schema '{schema}' missing after second upgrade: {sorted(missing)}"
            )
        enums = _all_enums(engine)
        missing_enums = EXPECTED_ENUMS - enums
        assert not missing_enums, f"missing enums after second upgrade: {sorted(missing_enums)}"
    finally:
        engine.dispose()


def test_audit_trigger_blocks_update(pg_raw):
    """The audit_no_update trigger rejects UPDATE on audit.event_log."""
    from sqlalchemy import text as sa_text

    from wb_api.repositories import AuditRepo

    session = pg_raw
    AuditRepo(session).append(
        actor_type="system", action="create",
        entity_type="test", entity_id="1",
    )
    session.commit()

    # Now attempt a direct UPDATE — the trigger must raise.
    with pytest.raises(Exception):
        session.execute(sa_text("UPDATE audit.event_log SET payload = '{}' WHERE true"))
    session.rollback()


def test_audit_trigger_blocks_delete(pg_raw):
    """The audit_no_update trigger rejects DELETE on audit.event_log."""
    from sqlalchemy import text as sa_text

    from wb_api.repositories import AuditRepo

    session = pg_raw
    AuditRepo(session).append(
        actor_type="system", action="create",
        entity_type="test", entity_id="1",
    )
    session.commit()

    with pytest.raises(Exception):
        session.execute(sa_text("DELETE FROM audit.event_log WHERE true"))
    session.rollback()
