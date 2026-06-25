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

Field namespace shim (v2.1 reconciliation, docs/05_RULE_ENGINE_SPEC.md):
the published runtime contract namespaces predicate fields as ``facts.*`` and
``context.*``. This evaluator accepts both the namespaced and the bare form:
  * ``facts.<name>``  -> looked up as the bare fact key ``<name>``
  * ``context.reference_date``    -> EvalContext.reference_date
  * ``context.jurisdiction_path`` -> list(EvalContext.jurisdiction_path)
  * ``<name>``        -> bare fact key (unchanged legacy behavior)
The stripping/mapping is purely at lookup time, so the migrated R1 batches
(which use bare names) behave exactly as before. ``context.*`` references are
injected from the ambient context and are therefore NOT reported by
``collect_fact_refs`` as user-answerable facts.
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

_FACTS_PREFIX = "facts."
_CONTEXT_PREFIX = "context."


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


def _strip_facts_prefix(field_id: str) -> str:
    """Strip a leading ``facts.`` namespace so the bare fact key is looked up."""
    if field_id.startswith(_FACTS_PREFIX):
        return field_id[len(_FACTS_PREFIX):]
    return field_id


def _context_value(name: str, ctx: EvalContext) -> Any:
    """Resolve a ``context.*`` reference from the ambient EvalContext.

    Returns MISSING for an unset reference_date or an unknown context name so
    that the three-valued guards treat it as undecidable rather than False.
    """
    if name == "reference_date":
        return ctx.reference_date if ctx.reference_date is not None else MISSING
    if name == "jurisdiction_path":
        return list(ctx.jurisdiction_path)
    return MISSING


def _lookup_field(field_id: Any, facts: Mapping[str, Any], ctx: EvalContext) -> Any:
    """Resolve a (possibly namespaced) ``field`` reference to its value or MISSING.

    ``context.*`` resolves from the EvalContext; ``facts.<name>`` and bare
    ``<name>`` both resolve from the facts mapping.
    """
    if not isinstance(field_id, str):
        return MISSING
    if field_id.startswith(_CONTEXT_PREFIX):
        return _context_value(field_id[len(_CONTEXT_PREFIX):], ctx)
    return facts.get(_strip_facts_prefix(field_id), MISSING)


def resolve_date_token(token: Any, facts: Mapping[str, Any], ctx: EvalContext | None = None) -> date | None:
    """Resolve a date token to a concrete date (or None if it cannot be resolved).

    Supports literal ISO dates, 'reference_date', fact names, relative
    expressions like 'expiry_date_minus_180d' / 'move_date_plus_15d', and the
    namespaced forms 'facts.<name>' and 'context.reference_date'.
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
    if s.startswith(_CONTEXT_PREFIX):
        name = s[len(_CONTEXT_PREFIX):]
        if name == "reference_date":
            return ctx.reference_date if ctx else None
        return None
    if s == "reference_date":
        return ctx.reference_date if ctx else None
    key = _strip_facts_prefix(s)
    if key in facts:
        return parse_date(facts.get(key))
    return parse_date(key)


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
        v = _lookup_field(field_id, facts, ctx)
        return from_bool(v is not MISSING and v is not None)
    if op == "missing":
        v = _lookup_field(field_id, facts, ctx)
        return from_bool(v is MISSING or v is None)

    # Date-comparison ops resolve tokens on both sides (field may be
    # 'reference_date', 'context.reference_date' or a relative expression), so
    # they run before the generic missing-fact guard below.
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

    value = _lookup_field(field_id, facts, ctx)
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
    """Return every user-answerable fact id referenced inside a predicate tree.

    ``facts.`` prefixes are stripped to the bare key; ``context.*`` references
    are injected from the ambient context and are intentionally excluded.
    """
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
    if not field_id or not isinstance(field_id, str):
        return set()
    if field_id.startswith(_CONTEXT_PREFIX):
        return set()
    return {_strip_facts_prefix(field_id)}
