"""WB-024 — idempotency integration tests against a real Postgres.

Exit gate: "encryption and idempotency concurrency tests pass".

Proves:
1. Two concurrent identical requests (same scope, key, payload) — only one runs
   the producer; the other replays the stored response. Uses the real
   ``pg_advisory_xact_lock`` already in ``IdempotencyRepo.lock``.
2. Same key + different payload → the second caller gets a 409 conflict.
3. ``delete_expired`` proactively removes rows past their TTL (the sweeper path
   referenced by WB-045).
"""
from __future__ import annotations

import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wb_api.repositories import IdempotencyRepo

pytestmark = pytest.mark.integration


def _fresh_engine_on_container(db_url):
    """New engine+session on the same migrated container, so we get independent
    transactions for each concurrent worker (a shared Session is not safe across
    threads)."""
    engine = create_engine(db_url, future=True, pool_size=8)
    return engine, sessionmaker(bind=engine, expire_on_commit=False, future=True)


def test_concurrent_same_key_one_wins(db_url):
    """Two threads, same (scope, key, payload) → exactly one runs the producer.

    We don't use ``run_idempotent`` here (it needs a FastAPI Services handle);
    instead we replicate the lock-find-or-store flow directly on the repo so the
    concurrency primitive under test is precisely ``pg_advisory_xact_lock``.
    """
    engine, factory = _fresh_engine_on_container(db_url)
    scope = "journeys.create"
    key = "client-req-" + uuid.uuid4().hex
    # DB constraint: request_hash ~ '^[a-f0-9]{64}$' (raw hex, no "sha256:" prefix).
    request_hash = "a" * 64
    payload_body = {"journey_id": str(uuid.uuid4())}

    run_starts = []
    run_results = []
    barrier = threading.Barrier(2)

    def worker():
        barrier.wait()  # release both threads at once
        session = factory()
        try:
            repo = IdempotencyRepo(session)
            # Replicate run_idempotent's lock-then-find-then-store flow.
            repo.lock(scope, key)
            existing = repo.find(scope, key, request_hash)
            if existing is not None:
                run_results.append(("replay", existing.response_body))
                return
            run_starts.append(threading.current_thread().name)
            run_results.append(("produced", payload_body))
            repo.store(
                scope, key, request_hash=request_hash, status=201,
                body=payload_body, ttl_seconds=3600,
            )
            session.commit()
        except Exception as e:
            run_results.append(("error", repr(e)))
            session.rollback()
        finally:
            session.close()

    with ThreadPoolExecutor(max_workers=2) as pool:
        futs = [pool.submit(worker) for _ in range(2)]
        for f in futs:
            f.result(timeout=30)

    producers = [r for r in run_results if r[0] == "produced"]
    replays = [r for r in run_results if r[0] == "replay"]
    errors = [r for r in run_results if r[0] == "error"]
    assert not errors, f"unexpected errors: {errors}"
    assert len(producers) == 1, f"expected exactly one producer, got {len(producers)}"
    assert len(replays) == 1, f"expected exactly one replay, got {len(replays)}"

    # The replayed body matches what the producer stored.
    assert replays[0][1] == payload_body

    engine.dispose()


def test_concurrent_same_key_different_payload_conflict(db_url, db_session):
    """Same key, different payload → the loser raises a 409 conflict.

    Using the shared ``db_session`` fixture (rolled back at the end) keeps this
    single-threaded and deterministic: insert once with payload A, then attempt
    to find with payload B → ConflictProblem raised.
    """
    from wb_api.errors import ConflictProblem

    scope = "scope-" + uuid.uuid4().hex
    key = "key-" + uuid.uuid4().hex
    hash_a = "a" * 64  # raw hex per DB constraint
    hash_b = "b" * 64

    repo = IdempotencyRepo(db_session)
    repo.store(scope, key, request_hash=hash_a, status=201, body={"x": 1}, ttl_seconds=3600)

    with pytest.raises(ConflictProblem):
        repo.find(scope, key, hash_b)


def test_ttl_sweeper_removes_expired(db_session):
    """delete_expired() proactively removes rows past their expires_at."""
    from sqlalchemy import text as sa_text

    # Clean any leftover expired rows from other tests
    db_session.execute(sa_text("DELETE FROM ops.idempotency_record WHERE expires_at <= now()"))

    scope = "scope-" + uuid.uuid4().hex
    key = "key-" + uuid.uuid4().hex
    repo = IdempotencyRepo(db_session)

    repo.store(scope, key, request_hash="a" * 64, status=200, body={}, ttl_seconds=1)
    # Force expire: move the row's expires_at into the past.
    db_session.execute(
        sa_text("UPDATE ops.idempotency_record SET expires_at = now() - interval '1 hour'")
    )

    n = repo.delete_expired()
    assert n >= 1  # at least our row was cleaned
    # Our specific row is gone.
    from wb_api.models import IdempotencyRecord
    remaining = db_session.get(IdempotencyRecord, (scope, key))
    assert remaining is None


def test_ttl_sweeper_leaves_unexpired(db_session):
    """delete_expired() leaves rows that are still within their TTL."""
    from sqlalchemy import text as sa_text

    # Clean any leftover expired rows from other tests
    db_session.execute(sa_text("DELETE FROM ops.idempotency_record WHERE expires_at <= now()"))

    scope = "scope-" + uuid.uuid4().hex
    key = "key-" + uuid.uuid4().hex
    repo = IdempotencyRepo(db_session)
    repo.store(scope, key, request_hash="a" * 64, status=200, body={}, ttl_seconds=3600)

    n = repo.delete_expired()
    assert n == 0
    from wb_api.models import IdempotencyRecord
    remaining = db_session.get(IdempotencyRecord, (scope, key))
    assert remaining is not None
