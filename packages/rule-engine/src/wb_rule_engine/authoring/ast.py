"""Typed predicate AST evaluator for the authoring contract language.

Mirrors contracts/predicate.schema.json exactly: predicates are objects with an
``op`` plus ``field``/``value``/``values`` for leaves, ``args`` for all/any and
``arg`` for not. Three-valued logic is shared with the runtime engine via
wb_rule_engine.trivalent: a missing fact is never silently coerced to False.

No dynamic code execution: every operator is matched explicitly.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Mapping

from ..dates import completed_years, parse_date
from ..trivalent import Tri, from_bool, tri_all, tri_any, tri_not

MISSING = object()


class UnsupportedOperator(Exception):
    pass


@dataclass(frozen=True)
class EvalContext:
    """Ambient context for ops that are not pure functions of a single fact."""

    reference_date: date | None = None
    jurisdiction_path: tuple[str, ...] = ()


def _num(value: Any):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def evaluate(pred: Mapping[str, Any], facts: Mapping[str, Any], ctx: EvalContext | None = None) -> Tri:
    ctx = ctx or EvalContext()
    op = pred.get("op")
    if op is None:
        raise UnsupportedOperator("predicate missing 'op'")

    if op == "const":
        return from_bool(bool(pred.get("value")))
    if op == "all":
        return tri_all([evaluate(p, facts, ctx) for p in pred.get("args", [])])
    if op == "any":
        return tri_any([evaluate(p, facts, ctx) for p in pred.get("args", [])])
    if op == "not":
        return tri_not(evaluate(pred["arg"], facts, ctx))

    field_id = pred.get("field")
    value = facts.get(field_id, MISSING) if field_id is not None else MISSING

    if op == "exists":
        return from_bool(value is not MISSING and value is not None)
    if op == "missing":
        return from_bool(value is MISSING or value is None)

    if value is MISSING or value is None:
        return Tri.UNKNOWN

    if op == "eq":
        return from_bool(value == pred.get("value"))
    if op == "neq":
        return from_bool(value != pred.get("value"))
    if op == "in":
        return from_bool(value in (pred.get("values") or []))
    if op == "not_in":
        return from_bool(value not in (pred.get("values") or []))
    if op == "contains":
        if isinstance(value, (list, tuple, str)):
            return from_bool(pred.get("value") in value)
        return Tri.UNKNOWN
    if op in ("lt", "lte", "gt", "gte"):
        a, b = _num(value), _num(pred.get("value"))
        if a is None or b is None:
            return Tri.UNKNOWN
        if op == "lt":
            return from_bool(a < b)
        if op == "lte":
            return from_bool(a <= b)
        if op == "gt":
            return from_bool(a > b)
        return from_bool(a >= b)
    if op in ("date_before", "date_after"):
        a, b = parse_date(value), parse_date(pred.get("value"))
        if a is None or b is None:
            return Tri.UNKNOWN
        return from_bool(a < b) if op == "date_before" else from_bool(a > b)
    if op in ("date_between", "within_window"):
        vals = pred.get("values") or []
        d = parse_date(value)
        lo = parse_date(vals[0]) if len(vals) > 0 else None
        hi = parse_date(vals[1]) if len(vals) > 1 else None
        if d is None or lo is None or hi is None:
            return Tri.UNKNOWN
        return from_bool(lo <= d <= hi)
    if op in ("age_on_date_gte", "age_on_date_lt"):
        birth = parse_date(value)
        on = ctx.reference_date
        target = _num(pred.get("value"))
        if birth is None or on is None or target is None:
            return Tri.UNKNOWN
        years = completed_years(birth, on)
        return from_bool(years >= target) if op == "age_on_date_gte" else from_bool(years < target)
    if op == "days_between_lte":
        d = parse_date(value)
        on = ctx.reference_date
        target = _num(pred.get("value"))
        if d is None or on is None or target is None:
            return Tri.UNKNOWN
        return from_bool(abs((on - d).days) <= target)
    if op in ("jurisdiction_is", "institution_is"):
        return from_bool(str(value) == str(pred.get("value")))
    if op == "jurisdiction_descends_from":
        ancestor = str(pred.get("value"))
        v = str(value)
        return from_bool(v == ancestor or v.startswith(ancestor + "."))
    if op == "authority_scope_contains":
        if isinstance(value, (list, tuple)):
            return from_bool(pred.get("value") in value)
        return Tri.UNKNOWN
    raise UnsupportedOperator(op)


def collect_fact_refs(pred: Mapping[str, Any]) -> set[str]:
    """Return every fact id referenced anywhere inside a predicate tree."""
    if not isinstance(pred, Mapping):
        return set()
    op = pred.get("op")
    if op in ("all", "any"):
        refs: set[str] = set()
        for p in pred.get("args", []):
            refs |= collect_fact_refs(p)
        return refs
    if op == "not":
        return collect_fact_refs(pred.get("arg", {}))
    field_id = pred.get("field")
    return {field_id} if field_id else set()
