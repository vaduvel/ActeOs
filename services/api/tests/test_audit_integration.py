"""WB-023 — audit append-only integration tests against a real Postgres.

Exit gate: "audit tampering fails".

Three guarantees proven here:
1. The persisted hash chain is well-formed and ``verify_event_log`` accepts it.
2. Tampering (a row with a wrong hash, or a deleted row) is detected as False.
3. PII fields in the payload are redacted before being stored to disk.

The audit_no_update trigger (UPDATE/DELETE rejection) is exercised in
test_migration_integration.py.
"""
from __future__ import annotations

from datetime import timedelta, timezone

import pytest
from sqlalchemy import select, text as sa_text

from wb_api import models as m
from wb_api.audit import compute_event_hash, scrub_payload, verify_event_log
from wb_api.repositories import AuditRepo

pytestmark = pytest.mark.integration


def _load_rows(session) -> list[dict]:
    rows = session.execute(sa_text(
        "SELECT occurred_at, actor_type, actor_id, action, entity_type, entity_id, "
        "correlation_id, payload, previous_event_hash, event_hash "
        "FROM audit.event_log ORDER BY id ASC"
    )).mappings().all()
    return [dict(r) for r in rows]


def _truncate_audit(session) -> None:
    """Wipe audit.event_log for a clean test (circumventing the append-only trigger)."""
    session.execute(sa_text("ALTER TABLE audit.event_log DISABLE TRIGGER audit_no_update"))
    session.execute(sa_text("TRUNCATE audit.event_log RESTART IDENTITY"))
    session.execute(sa_text("ALTER TABLE audit.event_log ENABLE TRIGGER audit_no_update"))
    session.commit()


def test_append_chains_correctly(pg_raw):
    """Three appends produce a valid chain that verify_event_log accepts."""
    session = pg_raw
    _truncate_audit(session)
    repo = AuditRepo(session)
    for i in range(3):
        repo.append(
            actor_type="system", action="create",
            entity_type="journey", entity_id=str(i),
        )
    session.commit()

    rows = _load_rows(session)
    assert len(rows) == 3
    assert verify_event_log(rows) is True


def test_tamper_detected_wrong_hash(pg_raw):
    """A row whose event_hash was overwritten is detected."""
    session = pg_raw
    _truncate_audit(session)
    repo = AuditRepo(session)
    repo.append(actor_type="system", action="create", entity_type="t", entity_id="1")
    repo.append(actor_type="system", action="create", entity_type="t", entity_id="2")
    session.commit()

    rows = _load_rows(session)
    assert verify_event_log(rows) is True

    # Corrupt the second row's event_hash in-place. The trigger blocks UPDATE, so
    # we bypass it via a superuser statement (the session role in testcontainers
    # is the postgres superuser, which can temporarily disable the trigger).
    session.execute(sa_text("ALTER TABLE audit.event_log DISABLE TRIGGER audit_no_update"))
    session.execute(sa_text(
        "UPDATE audit.event_log SET event_hash = 'sha256:deadbeef' "
        "WHERE entity_id = '2'"
    ))
    session.execute(sa_text("ALTER TABLE audit.event_log ENABLE TRIGGER audit_no_update"))
    session.commit()

    rows = _load_rows(session)
    assert verify_event_log(rows) is False, "tampered chain must be detected"


def test_tamper_detected_deleted_row(pg_raw):
    """Missing (deleted) rows break chain continuity and are detected."""
    session = pg_raw
    _truncate_audit(session)
    repo = AuditRepo(session)
    repo.append(actor_type="system", action="create", entity_type="t", entity_id="1")
    repo.append(actor_type="system", action="create", entity_type="t", entity_id="2")
    repo.append(actor_type="system", action="create", entity_type="t", entity_id="3")
    session.commit()

    rows = _load_rows(session)
    assert verify_event_log(rows) is True

    # Delete the middle row, circumventing the trigger.
    session.execute(sa_text("ALTER TABLE audit.event_log DISABLE TRIGGER audit_no_update"))
    session.execute(sa_text("DELETE FROM audit.event_log WHERE entity_id = '2'"))
    session.execute(sa_text("ALTER TABLE audit.event_log ENABLE TRIGGER audit_no_update"))
    session.commit()

    rows = _load_rows(session)
    # Two rows remain; the third's previous_event_hash now points to a row that
    # no longer exists, so verification must fail.
    assert len(rows) == 2
    assert verify_event_log(rows) is False


def test_pii_scrubbed_in_stored_payload(pg_raw):
    """PII keys in the payload are redacted before being persisted."""
    session = pg_raw
    _truncate_audit(session)
    repo = AuditRepo(session)
    repo.append(
        actor_type="curator", action="journey.reviewed",
        entity_type="journey", entity_id="123",
        payload={
            "reviewer_email": "curator@example.com",
            "phone": "+40700",
            "user_name": "Ion Popescu",
            "cnp": "1234567890123",
            "decision": "approved",  # safe — not a PII key
        },
    )
    session.commit()

    rows = _load_rows(session)
    assert len(rows) == 1
    payload = rows[0]["payload"]
    assert payload["reviewer_email"] == "[redacted]"
    assert payload["phone"] == "[redacted]"
    assert payload["user_name"] == "[redacted]"
    assert payload["cnp"] == "[redacted]"
    assert payload["decision"] == "approved"


def test_scrub_payload_unit():
    """Pure unit cover: known PII keys redacted, nested values preserved."""
    out = scrub_payload({
        "user_email": "x@y",
        "name": "Ion",
        "address": {"street": "Main St"},
        "safe": {"id": 7, "ok": True},
        "items": ["a", {"phone": "+40"}],
    })
    assert out["user_email"] == "[redacted]"
    assert out["name"] == "[redacted]"
    assert out["address"] == "[redacted]"
    assert out["safe"] == {"id": 7, "ok": True}
    assert out["items"][0] == "a"
    assert out["items"][1] == {"phone": "[redacted]"}


def test_compute_event_hash_deterministic():
    """Pure unit cover for the persisted hash function with fixed inputs."""
    h = compute_event_hash(
        previous_event_hash="sha256:" + "0" * 64,
        occurred_at="2026-07-08T12:00:00+00:00",
        actor_type="system", actor_id=None, action="create",
        entity_type="journey", entity_id="1", correlation_id=None,
        payload={"k": "v"},
    )
    assert h.startswith("sha256:")
    # Re-running with the same inputs yields the same hash.
    assert compute_event_hash(
        previous_event_hash="sha256:" + "0" * 64,
        occurred_at="2026-07-08T12:00:00+00:00",
        actor_type="system", actor_id=None, action="create",
        entity_type="journey", entity_id="1", correlation_id=None,
        payload={"k": "v"},
    ) == h
