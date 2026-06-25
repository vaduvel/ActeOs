import pytest


def _bundle():
    """Synthetic, non-official fixture bundle for engine tests only.

    This is NOT verified legal content. It exercises the engine mechanics
    (selection, gates, derived facts, step ordering, hashing) with made-up data.
    """
    return {
        "bundle_version": "test-0.0.1",
        "rules": [
            {
                "rule_id": "test.rule.national",
                "intent_id": "test.enroll",
                "jurisdiction": {"scope_codes": ["ro"], "authority_scope": "national"},
                "temporal": {"effective_from": "2026-01-01", "effective_to": "2026-12-31"},
                "source_claims": [{"id": "sc1", "confidence": "verified"}],
                "freshness": {
                    "review_due_at": "2999-01-01T00:00:00+00:00",
                    "hard_expiry_at": "2999-01-01T00:00:00+00:00",
                    "on_expiry": "warn",
                },
                "facts": [
                    {"id": "age", "derive": {"function": "age_on_date", "inputs": ["birth_date"]}},
                ],
                "gates": [
                    {
                        "id": "g.too_young",
                        "priority": 10,
                        "when": {"operator": "lt", "fact": "age", "value": 3},
                        "effect": "block",
                        "code": "NOT_ELIGIBLE_AGE",
                        "message": "Copilul nu a implinit varsta minima.",
                        "recovery_actions": [],
                    }
                ],
                "steps": [
                    {
                        "id": "s.submit",
                        "sequence_hint": 2,
                        "depends_on": ["s.prepare"],
                        "title": "Depune dosarul",
                        "instruction": "Depune dosarul la unitate.",
                        "deadline": {"kind": "none"},
                        "requirements": [],
                    },
                    {
                        "id": "s.prepare",
                        "sequence_hint": 1,
                        "depends_on": [],
                        "title": "Pregateste actele",
                        "instruction": "Pregateste documentele necesare.",
                        "deadline": {"kind": "none"},
                        "requirements": [
                            {
                                "id": "r.birth_cert",
                                "title": "Certificat de nastere",
                                "obligation": "required",
                                "timing": "at_submission",
                                "accepted_forms": ["copy", "certified_copy"],
                                "source_claim_ids": ["sc1"],
                            }
                        ],
                    },
                ],
            }
        ],
    }


@pytest.fixture
def bundle():
    return _bundle()


@pytest.fixture
def request_eligible():
    return {
        "intent_id": "test.enroll",
        "jurisdiction_id": "ro.timis.timisoara",
        "reference_date": "2026-09-01",
        "facts": {"birth_date": "2021-03-10"},
    }
