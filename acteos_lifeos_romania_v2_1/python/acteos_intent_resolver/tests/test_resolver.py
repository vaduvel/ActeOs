import pytest

from acteos_intent_resolver import IntentCatalog, IntentResolver, RankingConfig

# A small slice of data/intent_taxonomy.yaml, marked active so we can exercise
# the ranking pipeline (the real taxonomy is production_status: not_available).
_RAW = [
    {
        "id": "ro.intent.identity.renew_expired_id",
        "category_id": "identity_documents",
        "kind": "direct_goal",
        "title_ro": "Vreau s\u0103 schimb cartea de identitate expirat\u0103",
        "outcome_ro": "Ob\u021bin o carte de identitate valabil\u0103 dup\u0103 expirare",
        "aliases_ro": ["buletin expirat", "schimb buletin expirat", "re\u00eennoire buletin", "carte de identitate expirat\u0103", "ci expirat\u0103"],
        "negative_aliases_ro": ["schimb domiciliul", "buletin pierdut", "buletin furat"],
        "production_status": "active",
    },
    {
        "id": "ro.intent.identity.replace_lost_id",
        "category_id": "identity_documents",
        "kind": "direct_goal",
        "title_ro": "Vreau s\u0103 \u00eenlocuiesc cartea de identitate pierdut\u0103",
        "outcome_ro": "Ob\u021bin un nou act de identitate dup\u0103 pierdere",
        "aliases_ro": ["mi-am pierdut buletinul", "buletin pierdut", "carte identitate pierdut\u0103", "am pierdut ci"],
        "negative_aliases_ro": ["buletin furat", "buletin expirat"],
        "production_status": "active",
    },
    {
        "id": "ro.intent.identity.change_address_on_id",
        "category_id": "identity_documents",
        "kind": "direct_goal",
        "title_ro": "Vreau s\u0103 schimb domiciliul \u00een cartea de identitate",
        "outcome_ro": "Actualizez adresa din actul de identitate",
        "aliases_ro": ["schimb domiciliul \u00een buletin", "schimb adresa din buletin", "buletin adres\u0103 nou\u0103", "schimbare domiciliu ci"],
        "negative_aliases_ro": ["sediu firm\u0103", "domiciliu fiscal firm\u0103"],
        "production_status": "active",
    },
    {
        "id": "ro.intent.identity.obtain_criminal_record",
        "category_id": "identity_documents",
        "kind": "direct_goal",
        "title_ro": "Vreau s\u0103 ob\u021bin cazier judiciar",
        "outcome_ro": "Ob\u021bin certificatul de cazier judiciar",
        "aliases_ro": ["cazier", "cazier judiciar", "scot cazier", "certificat cazier"],
        "negative_aliases_ro": ["cazier fiscal", "cazier auto"],
        "production_status": "active",
    },
]


def _catalog():
    return IntentCatalog.from_records(_RAW, catalog_version="2.1.0", index_version="test")


@pytest.fixture()
def resolver() -> IntentResolver:
    return IntentResolver(_catalog(), RankingConfig())


def test_exact_title_is_high(resolver):
    res = resolver.resolve("Vreau s\u0103 schimb cartea de identitate expirat\u0103")
    assert res.resolution_state == "high"
    top = res.candidates[0]
    assert top.intent_type_id == "ro.intent.identity.renew_expired_id"
    assert top.match_mode == "exact_title"
    assert top.score == pytest.approx(1.0, abs=1e-6)  # no uniform jurisdiction bonus
    assert res.needs_confirmation is True  # never auto-start, even at high


def test_exact_alias_diacritics_insensitive(resolver):
    res = resolver.resolve("buletin expirat")
    assert res.resolution_state == "high"
    top = res.candidates[0]
    assert top.intent_type_id == "ro.intent.identity.renew_expired_id"
    assert top.match_mode == "exact_alias"
    assert top.matched_alias == "buletin expirat"
    assert top.score == pytest.approx(0.96, abs=1e-6)


def test_no_uniform_jurisdiction_bonus_when_unknown(resolver):
    # Without a jurisdiction set, no +0.10 is added to anyone.
    res = resolver.resolve("cazier")
    assert res.candidates[0].score == pytest.approx(0.96, abs=1e-6)
    assert "jurisdiction_available_bonus" not in res.candidates[0].signals


def test_jurisdiction_bonus_only_when_known_and_available():
    # Soft filter: known jurisdiction availability differentiates candidates.
    res = IntentResolver(_catalog()).resolve(
        "buletin expirat",
        jurisdiction_available_ids={"ro.intent.identity.renew_expired_id"},
        apply_hard_filters=False,
    )
    top = res.candidates[0]
    assert top.intent_type_id == "ro.intent.identity.renew_expired_id"
    assert top.score == pytest.approx(1.06, abs=1e-6)  # 0.96 + 0.10 jurisdiction
    assert top.signals["jurisdiction_available_bonus"] == pytest.approx(0.10, abs=1e-6)


def test_negative_alias_demotes_other_intent(resolver):
    # 'buletin pierdut' is an exact alias of replace_lost_id and a NEGATIVE
    # alias of renew_expired_id -> lost must win, expired must not be returned.
    res = resolver.resolve("buletin pierdut")
    assert res.candidates[0].intent_type_id == "ro.intent.identity.replace_lost_id"
    ids = [c.intent_type_id for c in res.candidates]
    assert "ro.intent.identity.renew_expired_id" not in ids


def test_diacritics_insensitive_query_matches_address_intent(resolver):
    res = resolver.resolve("schimb domiciliul in buletin")  # no diacritics
    assert res.candidates[0].intent_type_id == "ro.intent.identity.change_address_on_id"
    assert res.candidates[0].match_mode == "exact_alias"
    assert res.resolution_state == "high"


def test_cazier_exact_alias(resolver):
    res = resolver.resolve("cazier")
    assert res.candidates[0].intent_type_id == "ro.intent.identity.obtain_criminal_record"
    assert res.candidates[0].match_mode == "exact_alias"


def test_query_too_short(resolver):
    res = resolver.resolve("c")
    assert res.resolution_state == "too_short"
    assert res.error_code == "INTENT_QUERY_TOO_SHORT"
    assert res.candidates == []


def test_no_result(resolver):
    res = resolver.resolve("reteta de paste cu branza")
    assert res.resolution_state == "no_result"
    assert res.error_code == "INTENT_NOT_FOUND"
    assert res.candidates == []


def test_max_three_candidates(resolver):
    res = resolver.resolve("buletin")
    assert len(res.candidates) <= 3


def test_hard_filter_excludes_not_available():
    raw = [dict(r, production_status="not_available") for r in _RAW]
    catalog = IntentCatalog.from_records(raw, catalog_version="2.1.0")
    res = IntentResolver(catalog).resolve("buletin expirat")
    assert res.resolution_state == "no_result"
    res2 = IntentResolver(catalog).resolve("buletin expirat", apply_hard_filters=False)
    assert res2.candidates[0].intent_type_id == "ro.intent.identity.renew_expired_id"


def test_jurisdiction_hard_filter():
    res = IntentResolver(_catalog()).resolve(
        "buletin expirat",
        jurisdiction_available_ids={"ro.intent.identity.change_address_on_id"},
    )
    ids = [c.intent_type_id for c in res.candidates]
    assert "ro.intent.identity.renew_expired_id" not in ids


def test_trace_metadata_present(resolver):
    res = resolver.resolve("cazier")
    assert res.resolver_version == "2.1.0"
    assert res.normalization_version == "2.1.0"
    assert res.catalog_version == "2.1.0"
    assert res.index_version == "test"
    assert res.fallback_used is False
