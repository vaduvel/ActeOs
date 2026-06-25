"""End-to-end tests for the discovery slice over the FastAPI app.

Verifies: resolve-query (high / no_result / too_short), category listing only
for published categories, discovery home, intent listing + search, intent
detail, not-found error shape, and health.
"""
from __future__ import annotations

RENEW_ID = "ro.intent.identity.renew_expired_id"
PASSPORT = "ro.intent.identity.obtain_or_renew_passport"


def _resolve(client, query: str, **extra):
    payload = {"query": query, "locale": "ro-RO", **extra}
    return client.post("/v1/intents/resolve-query", json=payload)


def test_resolve_query_high_confidence(client):
    resp = _resolve(client, "buletin expirat")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["resolution_state"] == "high"
    assert len(body["candidates"]) == 1
    cand = body["candidates"][0]
    assert cand["intent"]["id"] == RENEW_ID
    assert cand["match_mode"] == "exact_alias"
    assert cand["matched_alias"] == "buletin expirat"
    assert cand["requires_confirmation"] is True
    assert cand["intent"]["available"] is True
    assert cand["score"] == 0.96
    assert body["request_id"]
    assert resp.headers.get("X-Request-ID") == body["request_id"]
    assert body["resolver_version"] == "2.1.0"


def test_resolve_query_no_result(client):
    resp = _resolve(client, "reteta de paste")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["resolution_state"] == "no_result"
    assert body["candidates"] == []


def test_resolve_query_too_short(client):
    resp = _resolve(client, "!!")
    assert resp.status_code == 422, resp.text
    body = resp.json()
    assert body["error"]["code"] == "INTENT_QUERY_TOO_SHORT"
    assert body["error"]["request_id"]


def test_resolve_query_below_min_length_is_validation_error(client):
    resp = _resolve(client, "a")
    assert resp.status_code == 422, resp.text
    assert resp.json()["error"]["code"] == "VALIDATION_ERROR"


def test_categories_only_published(client):
    resp = client.get("/v1/categories")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    ids = [c["id"] for c in body["items"]]
    assert ids == ["identity_documents", "vehicle_mobility"]
    counts = {c["id"]: c["intent_count"] for c in body["items"]}
    assert counts["identity_documents"] == 2
    assert counts["vehicle_mobility"] == 1
    assert "family_children" not in ids  # has no active intent
    assert body["catalog_version"] == "2.1.0-test"


def test_discovery_home(client):
    resp = client.get("/v1/discovery/home")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["headline_ro"]
    assert body["search_placeholder_ro"]
    assert len(body["quick_actions"]) == 3
    assert len(body["categories"]) == 2
    assert body["resolver_version"] == "2.1.0"


def test_list_intents_all(client):
    resp = client.get("/v1/intents")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    ids = {i["id"] for i in body["items"]}
    assert ids == {RENEW_ID, PASSPORT, "ro.intent.vehicle.register_used_purchase_ro"}
    assert body["page"]["has_more"] is False


def test_list_intents_search(client):
    resp = client.get("/v1/intents", params={"query": "pasaport"})
    assert resp.status_code == 200, resp.text
    items = resp.json()["items"]
    assert items, "expected at least one match"
    assert items[0]["id"] == PASSPORT


def test_list_intents_filter_by_category(client):
    resp = client.get("/v1/intents", params={"category_id": "vehicle_mobility"})
    assert resp.status_code == 200, resp.text
    ids = [i["id"] for i in resp.json()["items"]]
    assert ids == ["ro.intent.vehicle.register_used_purchase_ro"]


def test_get_intent_detail(client):
    resp = client.get(f"/v1/intents/{RENEW_ID}")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["id"] == RENEW_ID
    assert body["available"] is True
    assert body["production_status"] == "active"
    assert body["availability_message_ro"] is None


def test_get_intent_not_found(client):
    resp = client.get("/v1/intents/ro.intent.does.not.exist")
    assert resp.status_code == 404, resp.text
    body = resp.json()
    assert body["error"]["code"] == "INTENT_NOT_FOUND"
    assert body["error"]["request_id"]


def test_health_live(client):
    resp = client.get("/health/live")
    assert resp.status_code == 200, resp.text
    assert resp.json()["message"] == "alive"
