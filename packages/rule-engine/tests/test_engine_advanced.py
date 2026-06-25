from datetime import datetime, timezone

from wb_rule_engine import resolve

from tests.conftest import _advanced_bundle

NOW = datetime(2026, 6, 1, tzinfo=timezone.utc)
BUNDLE = _advanced_bundle()


def _req(intent, jurisdiction="ro.timis.timisoara", facts=None):
    return {
        "intent_id": intent,
        "jurisdiction_id": jurisdiction,
        "reference_date": "2026-09-01",
        "facts": facts or {},
    }


def test_county_overrides_national():
    route = resolve(
        _req("adv.enroll", facts={"needs_extra": False, "reference_anchor": "2026-09-01"}),
        BUNDLE, now=NOW,
    )
    assert route["rule_id"] == "adv.rule.county"
    assert any(s["id"] == "b.submit" for s in route["steps"])


def test_relative_deadline_resolved():
    route = resolve(
        _req("adv.enroll", facts={"needs_extra": False, "reference_anchor": "2026-09-01"}),
        BUNDLE, now=NOW,
    )
    submit = next(s for s in route["steps"] if s["id"] == "b.submit")
    assert submit["deadline"]["kind"] == "relative"
    assert submit["deadline"]["ends_at"] == "2026-10-01"


def test_requirement_applies_when_filtering():
    route = resolve(
        _req("adv.enroll", facts={"needs_extra": False, "reference_anchor": "2026-09-01"}),
        BUNDLE, now=NOW,
    )
    req_ids = {r["id"] for r in route["requirements"]}
    assert "r.always" in req_ids
    assert "r.cond" not in req_ids  # excluded because needs_extra is False


def test_dangling_dependency_warns():
    route = resolve(
        _req("adv.enroll", facts={"needs_extra": False, "reference_anchor": "2026-09-01"}),
        BUNDLE, now=NOW,
    )
    assert any(w["code"] == "DANGLING_DEPENDENCY" for w in route["warnings"])


def test_freshness_expired_blocks_confidence():
    route = resolve(_req("adv.expired"), BUNDLE, now=NOW)
    assert route["confidence"] == "expired"


def test_engine_records_conflict_for_tied_rules():
    route = resolve(_req("adv.tie"), BUNDLE, now=NOW)
    assert route["conflicts"]
    assert route["confidence"] == "conflicting"
