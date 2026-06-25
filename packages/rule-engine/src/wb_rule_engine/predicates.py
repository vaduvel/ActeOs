"""Typed predicate evaluation with three-valued logic.

Mirrors the predicate shapes in contracts/rule.schema.json. No dynamic code
execution: operators are matched explicitly.
"""
from __future__ import annotations

from typing import Any, Mapping

from .dates import parse_date
from .trivalent import Tri, from_bool, tri_all, tri_any, tri_not

MISSING = object()


class UnsupportedOperator(Exception):
    pass


def _num(value: Any):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _compare(op: str, value: Any, target: Any) -> Tri:
    if op in ("date_before", "date_on_or_before", "date_after", "date_on_or_after"):
        a = parse_date(value)
        b = parse_date(target)
        if a is None or b is None:
            return Tri.UNKNOWN
        if op == "date_before":
            return from_bool(a < b)
        if op == "date_on_or_before":
            return from_bool(a <= b)
        if op == "date_after":
            return from_bool(a > b)
        return from_bool(a >= b)
    a = _num(value)
    b = _num(target)
    if a is None or b is None:
        return Tri.UNKNOWN
    if op == "gt":
        return from_bool(a > b)
    if op == "gte":
        return from_bool(a >= b)
    if op == "lt":
        return from_bool(a < b)
    if op == "lte":
        return from_bool(a <= b)
    raise UnsupportedOperator(op)


def evaluate(pred: Mapping[str, Any], facts: Mapping[str, Any]) -> Tri:
    if "constant" in pred:
        return from_bool(bool(pred["constant"]))
    if "all" in pred:
        return tri_all([evaluate(p, facts) for p in pred["all"]])
    if "any" in pred:
        return tri_any([evaluate(p, facts) for p in pred["any"]])
    if "not" in pred:
        return tri_not(evaluate(pred["not"], facts))

    op = pred["operator"]
    fact_id = pred["fact"]
    value = facts.get(fact_id, MISSING)

    if op == "exists":
        return from_bool(value is not MISSING and value is not None)
    if op == "not_exists":
        return from_bool(value is MISSING or value is None)

    if value is MISSING or value is None:
        return Tri.UNKNOWN

    if op == "is_true":
        return from_bool(value is True)
    if op == "is_false":
        return from_bool(value is False)
    if op == "equals":
        return from_bool(value == pred.get("value"))
    if op == "not_equals":
        return from_bool(value != pred.get("value"))
    if op == "in":
        return from_bool(value in (pred.get("values") or []))
    if op == "not_in":
        return from_bool(value not in (pred.get("values") or []))
    if op == "between":
        lo = _compare("gte", value, pred.get("lower"))
        hi = _compare("lte", value, pred.get("upper"))
        return tri_all([lo, hi])
    if op in ("gt", "gte", "lt", "lte", "date_before", "date_on_or_before", "date_after", "date_on_or_after"):
        return _compare(op, value, pred.get("value"))
    raise UnsupportedOperator(op)


def collect_fact_refs(pred: Mapping[str, Any]) -> set[str]:
    """Return every fact id referenced anywhere inside a predicate tree.

    Used to determine which facts a citizen must supply when a decision cannot
    be evaluated. Boolean combinators recurse; leaf predicates contribute their
    ``fact``. Constants contribute nothing.
    """
    if not isinstance(pred, Mapping):
        return set()
    if "constant" in pred:
        return set()
    if "all" in pred:
        refs: set[str] = set()
        for p in pred["all"]:
            refs |= collect_fact_refs(p)
        return refs
    if "any" in pred:
        refs = set()
        for p in pred["any"]:
            refs |= collect_fact_refs(p)
        return refs
    if "not" in pred:
        return collect_fact_refs(pred["not"])
    if "fact" in pred:
        return {pred["fact"]}
    return set()
