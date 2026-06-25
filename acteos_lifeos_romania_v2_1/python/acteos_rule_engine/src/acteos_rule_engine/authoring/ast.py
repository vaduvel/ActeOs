"""Typed predicate AST evaluator for the authoring contract language.

Mirrors contracts/predicate.schema.json exactly: predicates are objects with an
``op`` plus ``field``/``value``/``values`` for leaves, ``args`` for all/any and
``arg`` for not. Three-valued logic is shared with the runtime engine via
acteos_rule_engine.trivalent: a missing fact is never silently coerced to False.

Date-comparison ops (date_before/date_after/date_between/within_window) resolve
both sides through ``resolve_date_token``, which understands:
  * literal ISO dates ('2026-06-25')
  * the ambient 'reference_date'
  * fact names ('move_date', 'expiry_date')
  * relative expressions '<token>_minus_<N>d' / '<token>_plus_<N>d'
    (e.g. 'expiry_date_minus_180d', 'move_date_plus_15d').

No dynamic code execution: every operator is matched explicitly.

NOTE (v2.1 reconciliation, tracked for M3 API wiring): the published runtime
contract (docs/05_RULE_ENGINE_SPEC.md) namespaces predicate fields as
``facts.*`` and ``context.*``. This evaluator currently uses bare fact names
(matching the migrated R1 batches). A normalization shim that strips ``facts.``
and maps ``context.*`` to EvalContext will be added when the API layer is wired,
with its own unit tests; behavior is intentionally unchanged here.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any, Mapping

from ..dates import completed_years, parse_date
from ..trivalent import Tri, from_bool, tri_all, tri_any, tri_not

MISSING = object()

_DELTA_RE = re.compile(r"^(.+)_(minus|plus)_(\d+)d$")
DATE_CMP_OPS = frozenset({"date_before", "date_after", "date_between", "within_window"})


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


def resolve_date_token(token: Any, facts: Mapping[str, Any], ctx: EvalContext | None = None) -> date | None:
    """Resolve a date token to a concrete date (or None if it cannot be resolved).

    Supports literal ISO dates, 'reference_date', fact names, and relative
    expressions like 'expiry_date_minus_180d' / 'move_date_plus_15d'.
    """
    if token is None:
        return None
    if isinstance(token, date):
        return parse_date(token)
    s = str(token)
    m = _DELTA_RE.match(s)
    if m:
        base = resolve_date_token(m.group(1), facts, ctx)
        if base is None:
            return None
        delta = timedelta(days=int(m.group(3)))
        return base - delta if m.group(2) == "minus" else base + delta
    if s == "reference_date":
        return ctx.reference_date if ctx else None
    if s in facts:
        return parse_date(facts.get(s))
    return parse_date(s)


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

    if op == "exists":
        v = facts.get(field_id, MISSING) if field_id is not None else MISSING
        return from_bool(v is not MISSING and v is not None)
    if op == "missing":
        v = facts.get(field_id, MISSING) if field_id is not None else MISSING
        return from_bool(v is MISSING or v is None)

    # Date-comparison ops resolve tokens on both sides (field may be
    # 'reference_date' or a relative expression), so they run before the
    # generic missing-fact guard below.
    if op in ("date_before", "date_after"):
        a = resolve_date_token(field_id, facts, ctx)
        b = resolve_date_token(pred.get("value"), facts, ctx)
        if a is None or b is None:
            return Tri.UNKNOWN
        return from_bool(a < b) if op == "date_before" else from_bool(a > b)
    if op in ("date_between", "within_window"):
        vals = pred.get("values") or []
        a = resolve_date_token(field_id, facts, ctx)
        lo = resolve_date_token(vals[0], facts, ctx) if len(vals) > 0 else None
        hi = resolve_date_token(vals[1], facts, ctx) if len(vals) > 1 else None
        if a is None or lo is None or hi is None:
            return Tri.UNKNOWN
        return from_bool(lo <= a <= hi)

    value = facts.get(field_id, MISSING) if field_id is not None else MISSING
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
