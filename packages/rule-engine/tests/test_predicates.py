from wb_rule_engine.predicates import evaluate
from wb_rule_engine.trivalent import Tri


def test_exists():
    assert evaluate({"operator": "exists", "fact": "x"}, {"x": 1}) is Tri.TRUE
    assert evaluate({"operator": "exists", "fact": "x"}, {}) is Tri.FALSE
    assert evaluate({"operator": "not_exists", "fact": "x"}, {}) is Tri.TRUE


def test_missing_fact_is_unknown():
    assert evaluate({"operator": "equals", "fact": "x", "value": 1}, {}) is Tri.UNKNOWN
    assert evaluate({"operator": "gte", "fact": "x", "value": 1}, {}) is Tri.UNKNOWN


def test_comparisons():
    assert evaluate({"operator": "gte", "fact": "age", "value": 3}, {"age": 3}) is Tri.TRUE
    assert evaluate({"operator": "lt", "fact": "age", "value": 3}, {"age": 3}) is Tri.FALSE
    assert evaluate({"operator": "between", "fact": "age", "lower": 3, "upper": 6}, {"age": 5}) is Tri.TRUE
    assert evaluate({"operator": "between", "fact": "age", "lower": 3, "upper": 6}, {"age": 7}) is Tri.FALSE


def test_membership():
    p = {"operator": "in", "fact": "city", "values": ["timisoara", "arad"]}
    assert evaluate(p, {"city": "timisoara"}) is Tri.TRUE
    assert evaluate(p, {"city": "cluj"}) is Tri.FALSE


def test_dates():
    p = {"operator": "date_before", "fact": "d", "value": "2026-09-01"}
    assert evaluate(p, {"d": "2026-08-31"}) is Tri.TRUE
    assert evaluate(p, {"d": "2026-09-02"}) is Tri.FALSE


def test_boolean_logic():
    p = {"all": [
        {"operator": "is_true", "fact": "a"},
        {"any": [
            {"operator": "is_true", "fact": "b"},
            {"operator": "is_true", "fact": "c"},
        ]},
    ]}
    assert evaluate(p, {"a": True, "b": False, "c": True}) is Tri.TRUE
    assert evaluate(p, {"a": True, "b": False, "c": False}) is Tri.FALSE
