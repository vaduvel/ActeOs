from datetime import date

from acteos_rule_engine.authoring.ast import EvalContext, collect_fact_refs, evaluate
from acteos_rule_engine.trivalent import Tri


def test_const_and_eq():
    assert evaluate({"op": "const", "value": True}, {}) is Tri.TRUE
    assert evaluate({"op": "eq", "field": "x", "value": 1}, {"x": 1}) is Tri.TRUE
    assert evaluate({"op": "eq", "field": "x", "value": 1}, {"x": 2}) is Tri.FALSE


def test_missing_fact_is_unknown_but_exists_is_definite():
    assert evaluate({"op": "eq", "field": "x", "value": 1}, {}) is Tri.UNKNOWN
    assert evaluate({"op": "exists", "field": "x"}, {}) is Tri.FALSE
    assert evaluate({"op": "missing", "field": "x"}, {}) is Tri.TRUE
    assert evaluate({"op": "exists", "field": "x"}, {"x": 5}) is Tri.TRUE


def test_all_any_not_trivalent():
    p = {"op": "all", "args": [{"op": "const", "value": True}, {"op": "eq", "field": "x", "value": 1}]}
    assert evaluate(p, {"x": 1}) is Tri.TRUE
    assert evaluate(p, {"x": 2}) is Tri.FALSE
    assert evaluate(p, {}) is Tri.UNKNOWN
    any_p = {"op": "any", "args": [{"op": "eq", "field": "x", "value": 1}, {"op": "const", "value": False}]}
    assert evaluate(any_p, {}) is Tri.UNKNOWN
    assert evaluate({"op": "not", "arg": {"op": "const", "value": True}}, {}) is Tri.FALSE


def test_membership_and_numeric():
    assert evaluate({"op": "in", "field": "x", "values": ["a", "b"]}, {"x": "a"}) is Tri.TRUE
    assert evaluate({"op": "not_in", "field": "x", "values": ["a"]}, {"x": "b"}) is Tri.TRUE
    assert evaluate({"op": "gte", "field": "n", "value": 5}, {"n": 5}) is Tri.TRUE
    assert evaluate({"op": "lt", "field": "n", "value": 5}, {"n": 7}) is Tri.FALSE
    assert evaluate({"op": "contains", "field": "tags", "value": "x"}, {"tags": ["x", "y"]}) is Tri.TRUE


def test_age_and_days_use_context():
    ctx = EvalContext(reference_date=date(2026, 9, 1))
    assert evaluate({"op": "age_on_date_gte", "field": "bd", "value": 3}, {"bd": "2021-03-10"}, ctx) is Tri.TRUE
    assert evaluate({"op": "age_on_date_lt", "field": "bd", "value": 3}, {"bd": "2025-01-10"}, ctx) is Tri.TRUE
    assert evaluate({"op": "days_between_lte", "field": "d", "value": 30}, {"d": "2026-08-20"}, ctx) is Tri.TRUE
    # without context the temporal ops cannot decide
    assert evaluate({"op": "age_on_date_gte", "field": "bd", "value": 3}, {"bd": "2021-03-10"}) is Tri.UNKNOWN


def test_date_and_jurisdiction_ops():
    assert evaluate({"op": "date_before", "field": "d", "value": "2026-01-01"}, {"d": "2025-12-31"}) is Tri.TRUE
    assert evaluate({"op": "date_between", "field": "d", "values": ["2026-01-01", "2026-12-31"]}, {"d": "2026-06-01"}) is Tri.TRUE
    assert evaluate({"op": "jurisdiction_descends_from", "field": "j", "value": "ro.tm"}, {"j": "ro.tm.timisoara"}) is Tri.TRUE
    assert evaluate({"op": "jurisdiction_descends_from", "field": "j", "value": "ro.cj"}, {"j": "ro.tm.timisoara"}) is Tri.FALSE
    assert evaluate({"op": "jurisdiction_is", "field": "j", "value": "ro"}, {"j": "ro"}) is Tri.TRUE


def test_collect_fact_refs():
    p = {"op": "all", "args": [{"op": "eq", "field": "a", "value": 1}, {"op": "not", "arg": {"op": "exists", "field": "b"}}]}
    assert collect_fact_refs(p) == {"a", "b"}
    assert collect_fact_refs({"op": "const", "value": True}) == set()
