"""Tests for the case resolution API slice (POST/GET /v1/cases).

Injects a small in-test ruleset + intent links via dependency override, so the
tests never depend on the on-disk research pack.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from acteos_api.cases import CaseService, get_case_service
from acteos_api.main import app
from acteos_api.repository import InMemoryCaseRepository
from acteos_api.rulesets import RulesetRepository

MINOR_PASSPORT = {
    "event_type_id": "life.minor_passport",
    "status": "draft",
    "rules": [
        {
            "id": "rule.mp.docs",
            "canonical_rule_id": "minor_passport.docs",
            "event_type_id": "life.minor_passport",
            "jurisdiction_ids": ["ro"],
            "severity": "critical",
            "when": {"op": "const", "value": True},
            "effects": [
                {"type": "include_step", "step_id": "apply_minor_passport"},
                {"type": "include_requirement", "requirement_id": "req.minor_birth_certificate"},
            ],
            "source_claim_ids": ["claim.mp.docs"],
            "status": "draft",
        },
        {
            "id": "rule.mp.single_parent_gate",
            "canonical_rule_id": "minor_passport.single_parent_gate",
            "event_type_id": "life.minor_passport",
            "jurisdiction_ids": ["ro"],
            "severity": "critical",
            "when": {
                "op": "all",
                "args": [
                    {"op": "eq", "field": "both_parents_consent", "value": False},
                    {"op": "eq", "field": "has_single_parent_doc", "value": False},
                ],
            },
            "effects": [
                {"type": "block", "message_ro": "Fara ambii parinti ai nevoie de procura."},
            ],
            "source_claim_ids": ["claim.mp.single"],
            "status": "draft",
        },
    ],
}

INTENT_LINKS = {"ro.intent.identity.obtain_minor_passport": ["ro.life.minor_passport"]}


@pytest.fixture()
def client():
    repo = RulesetRepository.from_mapping({"life.minor_passport": MINOR_PASSPORT})
    svc = CaseService(INTENT_LINKS, repo, InMemoryCaseRepository(), ruleset_version="test-1")
    app.dependency_overrides[get_case_service] = lambda: svc
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _payload(**overrides):
    base = {
        "intent_type_id": "ro.intent.identity.obtain_minor_passport",
        "reference_date": "2026-06-25",
        "timezone": "Europe/Bucharest",
        "jurisdiction_path": ["ro", "ro.tm.timisoara"],
        "facts": {"both_parents_consent": True, "has_single_parent_doc": False},
    }
    base.update(overrides)
    return base


def test_create_case_resolved(client):
    resp = client.post("/v1/cases", json=_payload())
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "resolved"
    assert body["event_type_id"] == "life.minor_passport"
    assert body["engine_version"]
    assert body["ruleset_version"] == "test-1"
    assert "rule.mp.docs" in body["resolution_trace"]["included_rule_ids"]
    assert "rule.mp.single_parent_gate" in body["resolution_trace"]["excluded_rule_ids"]
    event = body["events"][0]
    assert "apply_minor_passport" in event["included_steps"]
    assert "req.minor_birth_certificate" in event["requirements"]
    assert len(body["facts_hash"]) == 64


def test_create_case_blocked_when_single_parent_without_doc(client):
    resp = client.post(
        "/v1/cases",
        json=_payload(facts={"both_parents_consent": False, "has_single_parent_doc": False}),
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "blocked"
    assert "rule.mp.single_parent_gate" in body["resolution_trace"]["included_rule_ids"]
    assert body["events"][0]["blocks"]


def test_get_case_roundtrip(client):
    created = client.post("/v1/cases", json=_payload()).json()
    fetched = client.get(f"/v1/cases/{created['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == created["id"]


def test_unknown_intent_returns_404(client):
    resp = client.post("/v1/cases", json=_payload(intent_type_id="ro.intent.does.not_exist"))
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "INTENT_NOT_FOUND"


def test_validation_error_on_short_jurisdiction_path(client):
    resp = client.post("/v1/cases", json=_payload(jurisdiction_path=["ro"]))
    assert resp.status_code == 422
