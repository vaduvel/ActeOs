"""missing_facts: derived facts must be reported as their answerable inputs."""
from datetime import datetime, timezone

from wb_rule_engine import resolve

NOW = datetime(2026, 9, 1, tzinfo=timezone.utc)


def test_missing_fact_expands_to_input(bundle):
    # birth_date drives the derived 'age' gate; omitting it must surface
    # birth_date (answerable), never 'age' (derived).
    request = {
        "intent_id": "test.enroll",
        "jurisdiction_id": "ro.timis.timisoara",
        "reference_date": "2026-09-01",
        "facts": {},
    }
    out = resolve(request, bundle, now=NOW)
    ids = {m["fact_id"] for m in out["missing_facts"]}
    assert ids == {"birth_date"}
    assert "age" not in ids


def test_no_missing_when_facts_complete(bundle, request_eligible):
    out = resolve(request_eligible, bundle, now=NOW)
    assert out["missing_facts"] == []


def test_missing_facts_uses_question_metadata(bundle):
    enriched = {**bundle}
    enriched["rules"] = [dict(bundle["rules"][0])]
    enriched["rules"][0]["fact_questions"] = {
        "birth_date": {
            "label": "Data nasterii copilului",
            "value_type": "date",
            "reason": "Stabileste eligibilitatea de varsta.",
            "sensitive": True,
        }
    }
    request = {
        "intent_id": "test.enroll",
        "jurisdiction_id": "ro.timis.timisoara",
        "reference_date": "2026-09-01",
        "facts": {},
    }
    out = resolve(request, enriched, now=NOW)
    q = next(m for m in out["missing_facts"] if m["fact_id"] == "birth_date")
    assert q["value_type"] == "date"
    assert q["sensitive"] is True
    assert q["label"] == "Data nasterii copilului"
