from wb_rule_engine.precedence import resolve_precedence


def _rule(rule_id, authority="national", effective_from="2026-01-01"):
    return {
        "rule_id": rule_id,
        "jurisdiction": {"authority_scope": authority},
        "temporal": {"effective_from": effective_from},
    }


def test_single_rule_no_conflict():
    r = _rule("a")
    winner, conflicts = resolve_precedence([r])
    assert winner is r
    assert conflicts == []


def test_higher_authority_wins():
    nat = _rule("nat", authority="national")
    eu = _rule("eu", authority="eu")
    winner, conflicts = resolve_precedence([nat, eu])
    assert winner["rule_id"] == "eu"
    assert conflicts == []


def test_lex_posterior_wins():
    old = _rule("old", effective_from="2025-01-01")
    new = _rule("new", effective_from="2026-01-01")
    winner, conflicts = resolve_precedence([old, new])
    assert winner["rule_id"] == "new"
    assert conflicts == []


def test_genuine_conflict_is_flagged_and_deterministic():
    a = _rule("a")
    b = _rule("b")
    w1, c1 = resolve_precedence([a, b])
    w2, c2 = resolve_precedence([b, a])
    assert w1["rule_id"] == w2["rule_id"]  # deterministic regardless of input order
    assert c1 and c1[0]["code"] == "RULE_CONFLICT_UNRESOLVED"
    assert c1[0]["rule_ids"] == ["a", "b"]
