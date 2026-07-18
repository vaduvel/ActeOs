"""WB-022 — field encryption integration tests against a real Postgres.

Exit gate: "encryption and idempotency concurrency tests pass".
Specifically for WB-022: round-trip through the DB, AAD binding fails on
mismatch, and key rotation keeps old tokens readable (backward compat) plus a
tested ``rewrap`` path that re-encrypts existing rows under the new active key.
"""
from __future__ import annotations

import uuid

import pytest
from sqlalchemy import text as sa_text

from wb_api import models as m
from wb_api.crypto import DecryptionError
from wb_api.repositories import JourneyRepo

pytestmark = pytest.mark.integration

CNP = "1234567890123"


def _seed_journey(session, journey_id: str) -> str:
    """Insert a fully-valid journey row + its FK parents. Returns the device_id."""
    device_id, jurisdiction_id, intent_id = str(uuid.uuid4()), str(uuid.uuid4()), "intent-test"
    session.execute(sa_text(
        "INSERT INTO app.device_identity (id, pseudonymous_token_hash, created_at, last_seen_at) "
        "VALUES (:id, :token_hash, now(), now())"
    ), {"id": device_id, "token_hash": "test-hash-" + device_id[:8]})
    # jurisdiction + intent must exist before journey can reference them.
    session.execute(sa_text(
        "INSERT INTO content.jurisdiction (id, code, name, kind, is_active) VALUES (:id, :code, :name, 'country', true) "
        "ON CONFLICT (code) DO NOTHING"
    ), {"id": jurisdiction_id, "code": "ro-test", "name": "Romania Test"})
    # Look up the actual jurisdiction_id (may already exist)
    row = session.execute(sa_text("SELECT id FROM content.jurisdiction WHERE code = 'ro-test'")).first()
    actual_jurisdiction_id = row[0] if row else jurisdiction_id
    session.execute(sa_text(
        "INSERT INTO content.intent (id, category, title_ro, description_ro, owner_team, release_status) "
        "VALUES (:id, 'test', 'Test intent', 'test', 'test-team', 'production'::content.release_status) "
        "ON CONFLICT (id) DO NOTHING"
    ), {"id": intent_id})
    # app.journey has NOT NULL intent_id, jurisdiction_id, title, evaluated_at;
    # active_bundle_hash / current_route_hash are nullable (pass NULL).
    session.execute(sa_text(
        "INSERT INTO app.journey (id, device_id, intent_id, jurisdiction_id, title, "
        "status, evaluated_at, created_at, updated_at) "
        "VALUES (:id, :device, :intent, :jurisdiction, 'Test journey', 'active', "
        "now(), now(), now())"
    ), {"id": journey_id, "device": device_id, "intent": intent_id,
        "jurisdiction": actual_jurisdiction_id})
    return device_id


def test_journey_fact_encrypt_roundtrip_via_db(db_session, make_cipher, test_keys):
    """Insert via JourneyRepo.set_facts, read back via get_facts → matches."""
    session = db_session
    journey_id = str(uuid.uuid4())
    _seed_journey(session, journey_id)
    session.flush()

    journey = session.get(m.Journey, journey_id)
    repo = JourneyRepo(session, make_cipher(test_keys, "k1"))
    repo.set_facts(journey, [("age", 30, "user"), ("cnp", CNP, "user")])

    facts = repo.get_facts(journey_id)
    assert facts["age"] == 30
    assert facts["cnp"] == CNP


def test_aad_mismatch_fails_via_db(db_session, make_cipher, test_keys):
    """A token stored for journey A cannot be decrypted as if it belonged to journey B."""
    session = db_session
    j1, j2 = str(uuid.uuid4()), str(uuid.uuid4())
    _seed_journey(session, j1)
    _seed_journey(session, j2)
    session.flush()

    repo = JourneyRepo(session, make_cipher(test_keys, "k1"))
    repo.set_facts(session.get(m.Journey, j1), [("cnp", CNP, "user")])

    fact = repo.get_fact_rows(j1)[0]
    token = bytes(fact.value_encrypted).decode("utf-8")
    cipher = make_cipher(test_keys, "k1")
    bad_aad = f"app.journey_fact:{j2}:{fact.fact_id}".encode("utf-8")
    with pytest.raises(DecryptionError):
        cipher.decrypt(token, aad=bad_aad)


def test_key_rotation_decrypts_old_tokens(db_session, make_cipher, test_keys):
    """Encrypt under k1, switch active to k2 → old token still readable (backward compat)."""
    session = db_session
    journey_id = str(uuid.uuid4())
    _seed_journey(session, journey_id)
    session.flush()

    JourneyRepo(session, make_cipher(test_keys, "k1")).set_facts(
        session.get(m.Journey, journey_id), [("cnp", CNP, "user")]
    )
    # Rotate: new repo with active=k2, keyring still has k1.
    repo_k2 = JourneyRepo(session, make_cipher(test_keys, "k2"))
    assert repo_k2.get_facts(journey_id)["cnp"] == CNP


def test_rewrap_under_new_key(make_cipher, test_keys):
    """rewrap() decrypts under the old key and re-encrypts under active (k2).

    The token's embedded key_id moves from k1 to k2 and the ciphertext changes.
    The unit-level proof (no DB needed) — round-trip semantics are the same.
    """
    cipher_k1 = make_cipher(test_keys, "k1")
    aad = b"ctx"
    token = cipher_k1.encrypt("secret-value", aad=aad)
    assert ":k1:" in token

    cipher_k2 = make_cipher(test_keys, "k2")
    new_token = cipher_k2.rewrap(token, aad=aad)
    assert ":k2:" in new_token
    assert new_token != token
    assert cipher_k2.decrypt_str(new_token, aad=aad) == "secret-value"


def test_concurrency_roundtrip_no_deadlock(pg_raw, make_cipher, test_keys):
    """Sanity: the DB accepts two parallel fact writes on different journeys."""
    from concurrent.futures import ThreadPoolExecutor

    # We need independent sessions per thread; create a fresh engine pointing at
    # the same migrated container via the DATABASE_URL set by the conftest.
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    db_url = os.environ["DATABASE_URL"]
    engine = create_engine(db_url, future=True, pool_size=4)
    factory = sessionmaker(bind=engine, expire_on_commit=False, future=True)
    j1, j2 = str(uuid.uuid4()), str(uuid.uuid4())

    # Seed up-front using pg_raw (commits for real, visible to other sessions).
    _seed_journey(pg_raw, j1)
    _seed_journey(pg_raw, j2)
    pg_raw.commit()

    errors = []

    def worker(jid):
        try:
            s = factory()
            try:
                JourneyRepo(s, make_cipher(test_keys, "k1")).set_facts(
                    s.get(m.Journey, jid), [("cnp", CNP, "user")]
                )
                s.commit()
            finally:
                s.close()
        except Exception as e:  # noqa: BLE001
            errors.append(repr(e))

    with ThreadPoolExecutor(max_workers=2) as pool:
        futs = [pool.submit(worker, jid) for jid in (j1, j2)]
        for f in futs:
            f.result(timeout=30)
    assert not errors, errors

    # Both rows present and decryptable.
    repo = JourneyRepo(pg_raw, make_cipher(test_keys, "k1"))
    assert repo.get_facts(j1)["cnp"] == CNP
    assert repo.get_facts(j2)["cnp"] == CNP
    engine.dispose()
