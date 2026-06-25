from datetime import datetime, timezone

import pytest

from wb_rule_engine import resolve
from wb_rule_engine.errors import NoApplicableRule

NOW = datetime(2026, 6, 1, tzinfo=timezone.utc)


def test_resolves_and_orders_steps(bundle, request_eligible):
    route = resolve(request_eligible, bundle, now=NOW)
    ids = [s["id"] for s in route["steps"]]
    assert ids == ["s.prepare", "s.submit"]
    assert route["confidence"] == "verified"
    assert route["blocked"] is False
    assert any(r["id"] == "r.birth_cert" for r in route["requirements"])


def test_route_hash_is_deterministic(bundle, request_eligible):
    a = resolve(request_eligible, bundle, now=NOW)
    b = resolve(request_eligible, bundle, now=datetime(2027, 1, 1, tzinfo=timezone.utc))
    # route_hash excludes route_id and evaluated_at, so different clocks match
    assert a["route_hash"] == b["route_hash"]
    assert a["route_id"] != b["route_id"]


def test_gate_blocks_when_too_young(bundle):
    req = {
        "intent_id": "test.enroll",
        "jurisdiction_id": "ro.timis.timisoara",
        "reference_date": "2026-09-01",
        "facts": {"birth_date": "2025-01-10"},
    }
    route = resolve(req, bundle, now=NOW)
    assert route["blocked"] is True
    assert any(g["code"] == "NOT_ELIGIBLE_AGE" for g in route["gates"])


def test_unknown_age_yields_needs_confirmation(bundle):
    req = {
        "intent_id": "test.enroll",
        "jurisdiction_id": "ro.timis.timisoara",
        "reference_date": "2026-09-01",
        "facts": {},
    }
    route = resolve(req, bundle, now=NOW)
    assert route["confidence"] == "needs_confirmation"


def test_no_rule_raises(bundle):
    req = {
        "intent_id": "test.enroll",
        "jurisdiction_id": "fr.paris",
        "reference_date": "2026-09-01",
        "facts": {"birth_date": "2021-03-10"},
    }
    with pytest.raises(NoApplicableRule):
        resolve(req, bundle, now=NOW)
