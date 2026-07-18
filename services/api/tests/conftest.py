"""Pytest fixtures shared across the services/api suite.

Two layers of tests live here:

* **Unit tests** (no marker) — pure, in-memory, no Docker. Always run.
* **Integration tests** (``@pytest.mark.integration``) — require a real Postgres,
  provisioned on the fly by testcontainers. Skipped automatically when Docker is
  not available so ``make test-unit`` stays green on any machine.

The integration layer gives every test a clean schema: a fresh container is
started once per test session, ``alembic upgrade head`` builds the schema, and
each test runs inside a transaction that is rolled back so tables are never
polluted across tests. The audit append-only trigger deliberately *cannot* be
exercised inside a rolled-back transaction (the trigger fires on UPDATE/DELETE,
not on rollback), so tamper tests use the ``pg_raw`` session which bypasses the
transaction wrapper.
"""
from __future__ import annotations

import os
from collections.abc import Iterator
from datetime import datetime, timezone
from typing import Callable

import pytest

# ---------------------------------------------------------------------------
# Unit-test fixtures (no Docker, always available).
# ---------------------------------------------------------------------------


@pytest.fixture
def test_keys() -> dict[str, bytes]:
    """Deterministic 256-bit test keys (32 raw bytes each, as FieldCipher expects)."""
    return {
        "k1": bytes.fromhex("00" * 32),
        "k2": bytes.fromhex("11" * 32),
        "k3": bytes.fromhex("22" * 32),
    }


@pytest.fixture
def now_utc() -> datetime:
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Integration-test layer (Docker + Postgres via testcontainers).
# ---------------------------------------------------------------------------

# Marker registration: also declared in pyproject [tool.pytest.ini_options], but
# duplicated here so collection never fails if the marker list drifts.


def _docker_available() -> bool:
    """True if the Docker daemon answers ``docker info``."""
    import shutil
    import subprocess

    if not shutil.which("docker"):
        return False
    try:
        r = subprocess.run(
            ["docker", "info", "--format", "{{.ServerVersion}}"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return r.returncode == 0 and bool(r.stdout.strip())
    except (OSError, subprocess.SubprocessError):
        return False


_HAS_DOCKER = _docker_available()


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip integration tests when Docker is not running."""
    if _HAS_DOCKER:
        return
    skip = pytest.mark.skip(reason="Docker not available — integration tests need testcontainers")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip)


@pytest.fixture(scope="session")
def pg_container():
    """Start a fresh postgres:17 container for the whole session."""
    if not _HAS_DOCKER:
        pytest.skip("Docker not available")
    from testcontainers.postgres import PostgresContainer

    with PostgresContainer("postgres:17", driver="psycopg") as pg:
        yield pg


@pytest.fixture(scope="session")
def db_url(pg_container) -> str:
    """The live psycopg connection URL for the session container."""
    url = pg_container.get_connection_url()
    # env.py reads DATABASE_URL at import time; alembic commands spawned as
    # subprocesses inherit this env var.
    os.environ["DATABASE_URL"] = url
    return url


@pytest.fixture(scope="session")
def _migrated_engine(db_url):
    """Build the schema once via alembic and yield a shared engine.

    We shell out to ``alembic upgrade head`` (the same path operators use) rather
    than calling ``Base.metadata.create_all``: the migration is the source of
    truth and owns the triggers/enums/partial indexes the ORM does not model.
    """
    import subprocess
    from pathlib import Path

    api_dir = Path(__file__).resolve().parents[1]
    env = {**os.environ, "DATABASE_URL": db_url}
    r = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=api_dir,
        env=env,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(
            f"alembic upgrade head failed:\nstdout:\n{r.stdout}\nstderr:\n{r.stderr}"
        )
    from sqlalchemy import create_engine

    engine = create_engine(db_url, future=True)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(_migrated_engine) -> Iterator:
    """A session on the migrated DB, rolled back after each test.

    For most tests this gives table-level isolation. Append-only audit and
    trigger behaviour that must survive a real commit use ``pg_raw`` instead.
    """
    from sqlalchemy.orm import sessionmaker

    factory = sessionmaker(bind=_migrated_engine, expire_on_commit=False, future=True)
    session = factory()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def pg_raw(_migrated_engine):
    """A session that commits for real — needed by tamper/trigger tests.

    Tests using this fixture own their cleanup (DELETE rows they insert).
    """
    from sqlalchemy.orm import sessionmaker

    factory = sessionmaker(bind=_migrated_engine, expire_on_commit=False, future=True)
    return factory()


@pytest.fixture
def make_cipher(test_keys) -> Callable[..., "object"]:
    """Factory that builds a ``FieldCipher`` from a keyring + active id."""
    from wb_api.crypto import FieldCipher

    def _make(keys: dict[str, str] | None = None, active: str = "k1") -> FieldCipher:
        return FieldCipher(keyring=keys or test_keys, active_key_id=active)

    return _make
