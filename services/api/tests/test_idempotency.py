import pytest

from wb_api.idempotency import ConflictError, IdempotencyStore


def test_new_then_replay():
    store = IdempotencyStore()
    payload = {"intent": "x", "facts": {"a": 1}}
    state, resp = store.begin("key-1", payload)
    assert state == "new" and resp is None
    store.complete("key-1", {"route_id": "r1"})
    state, resp = store.begin("key-1", payload)
    assert state == "replay"
    assert resp == {"route_id": "r1"}


def test_in_progress_before_completion():
    store = IdempotencyStore()
    store.begin("key-1", {"a": 1})
    state, resp = store.begin("key-1", {"a": 1})
    assert state == "in_progress" and resp is None


def test_same_key_different_request_conflicts():
    store = IdempotencyStore()
    store.begin("key-1", {"a": 1})
    with pytest.raises(ConflictError):
        store.begin("key-1", {"a": 2})


def test_key_order_independent_fingerprint():
    store = IdempotencyStore()
    store.begin("key-1", {"a": 1, "b": 2})
    # same content, different key order must NOT be treated as a conflict
    state, _ = store.begin("key-1", {"b": 2, "a": 1})
    assert state == "in_progress"
