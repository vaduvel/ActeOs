"""Deterministic evaluation of a governed authoring ruleset (rich contract).

``evaluate_ruleset`` consumes a ruleset in the authoring contract shape (the
``rules.yaml`` of a governed batch) plus a citizen's facts, and produces a
``RouteResult`` carrying steps, requirements, obligations, channels, advice,
warnings, confirmations, conflicts, blocked effects, overridden rules, computed
deadlines (with overdue detection) and the user-answerable facts still missing.

Status precedence (highest first):
  needs_facts > conflicting > blocked > needs_confirmation > resolved

Pure and deterministic: no IO, no network, no clock. ``reference_date`` and
``jurisdiction_path`` are injected by the caller (the golden runner or the API).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any, Mapping, Sequence

from ..dates import parse_date
from ..trivalent import Tri
from .ast import EvalContext, collect_fact_refs, evaluate, resolve_date_token
from .effects import effect_tag


@dataclass
class RouteResult:
    status: str = "resolved"
    included_steps: list = field(default_factory=list)
    requirements: list = field(default_factory=list)
    obligations: dict = field(default_factory=dict)
    channels: list = field(default_factory=list)
    advice: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    confirmations: list = field(default_factory=list)
    conflicts: list = field(default_factory=list)
    blocked_effects: list = field(default_factory=list)
    blocks: list = field(default_factory=list)
    overridden_rules: list = field(default_factory=list)
    deadlines: dict = field(default_factory=dict)
    child_events: list = field(default_factory=list)
    freshness: list = field(default_factory=list)
    missing_facts: list = field(default_factory=list)
    fired_rule_ids: list = field(default_factory=list)

    @property
    def advice_tags(self) -> list:
        return [a["tag"] for a in self.advice if a.get("tag")]

    @property
    def warning_tags(self) -> list:
        return [w["tag"] for w in self.warnings if w.get("tag")]

    @property
    def deadline_dates(self) -> dict:
        return {k: v.get("date") for k, v in self.deadlines.items()}

    @property
    def overdue_steps(self) -> list:
        return [k for k, v in self.deadlines.items() if v.get("overdue")]


def _temporal_ok(rule: Mapping[str, Any], reference_date: date | None) -> bool:
    if reference_date is None:
        return True
    ef = parse_date(rule.get("effective_from"))
    et = parse_date(rule.get("effective_to"))
    if ef is not None and reference_date < ef:
        return False
    if et is not None and reference_date > et:
        return False
    return True


def _jurisdiction_ok(rule: Mapping[str, Any], jurisdiction_path: Sequence[str]) -> bool:
    ids = rule.get("jurisdiction_ids") or []
    if not ids or not jurisdiction_path:
        return True
    path = set(jurisdiction_path)
    return any(j in path for j in ids)


def _required_facts(ruleset: Mapping[str, Any]) -> list:
    declared = ruleset.get("required_facts")
    if declared:
        return [f for f in declared if f != "reference_date"]
    seen: list = []
    for rule in ruleset.get("rules", []):
        for ref in sorted(collect_fact_refs(rule.get("when", {}))):
            if ref not in seen and ref != "reference_date":
                seen.append(ref)
    return seen


def _add(seq: list, value) -> None:
    if value is not None and value not in seq:
        seq.append(value)


def _compute_deadline(value: Mapping[str, Any], facts: Mapping[str, Any], ctx: EvalContext) -> dict:
    kind = value.get("kind")
    entry: dict = {"kind": kind, "date": None, "days": None, "hours": None, "overdue": False}
    if kind in ("relative_calendar_days", "relative_days"):
        anchor = resolve_date_token(value.get("anchor"), facts, ctx)
        days = value.get("days")
        entry["days"] = days
        if anchor is not None and days is not None:
            entry["date"] = (anchor + timedelta(days=int(days))).isoformat()
    elif kind == "relative_hours":
        anchor = resolve_date_token(value.get("anchor"), facts, ctx)
        hours = value.get("hours")
        entry["hours"] = hours
        if anchor is not None and hours is not None:
            entry["date"] = (anchor + timedelta(days=math.ceil(int(hours) / 24))).isoformat()
    elif kind == "window":
        frm = resolve_date_token(value.get("from"), facts, ctx)
        to = resolve_date_token(value.get("to"), facts, ctx)
        entry["from"] = frm.isoformat() if frm else None
        entry["to"] = to.isoformat() if to else None
        entry["date"] = entry["to"]
    if entry["date"] is not None and ctx.reference_date is not None:
        deadline = parse_date(entry["date"])
        entry["overdue"] = deadline is not None and ctx.reference_date > deadline
    return entry


def evaluate_ruleset(
    ruleset: Mapping[str, Any],
    facts: Mapping[str, Any],
    *,
    jurisdiction_path: Sequence[str] = (),
    reference_date: Any = None,
) -> RouteResult:
    if isinstance(reference_date, str):
        reference_date = parse_date(reference_date)
    ctx = EvalContext(reference_date=reference_date, jurisdiction_path=tuple(jurisdiction_path))
    result = RouteResult()

    required = _required_facts(ruleset)
    result.missing_facts = [f for f in required if facts.get(f) is None]

    eligible: list = []
    for rule in ruleset.get("rules", []):
        if not _jurisdiction_ok(rule, jurisdiction_path):
            continue
        if not _temporal_ok(rule, reference_date):
            continue
        if evaluate(rule.get("when", {"op": "const", "value": True}), facts, ctx) is Tri.TRUE:
            eligible.append(rule)

    overridden: set = set()
    for rule in eligible:
        for rid in rule.get("override_rule_ids", []) or []:
            overridden.add(rid)
        for eff in rule.get("effects", []):
            if eff.get("type") == "override_rule":
                target = eff.get("rule_id") or eff.get("target_rule_id") or eff.get("value")
                if target:
                    overridden.add(target)
    firing = [r for r in eligible if r.get("id") not in overridden]
    all_ids = {r.get("id") for r in ruleset.get("rules", [])}
    result.overridden_rules = sorted(rid for rid in overridden if rid in all_ids)

    excluded_steps: set = set()
    for rule in firing:
        result.fired_rule_ids.append(rule.get("id"))
        for eff in rule.get("effects", []):
            etype = eff.get("type")
            if etype == "include_step":
                _add(result.included_steps, eff.get("step_id"))
            elif etype == "exclude_step":
                if eff.get("step_id"):
                    excluded_steps.add(eff.get("step_id"))
            elif etype == "include_requirement":
                _add(result.requirements, eff.get("requirement_id"))
            elif etype == "set_requirement_obligation":
                rid = eff.get("requirement_id")
                if rid:
                    result.obligations[rid] = eff.get("value") or eff.get("obligation")
            elif etype == "attach_channel":
                _add(result.channels, eff.get("channel_id"))
            elif etype == "emit_advice":
                result.advice.append({"tag": effect_tag(eff, rule), "message_ro": eff.get("message_ro")})
            elif etype == "emit_warning":
                result.warnings.append({"tag": effect_tag(eff, rule), "message_ro": eff.get("message_ro")})
            elif etype == "require_confirmation":
                _add(result.confirmations, effect_tag(eff, rule))
            elif etype == "flag_conflict":
                _add(result.conflicts, effect_tag(eff, rule))
                if eff.get("blocked_effect"):
                    _add(result.blocked_effects, eff.get("blocked_effect"))
            elif etype == "block":
                result.blocks.append({"message_ro": eff.get("message_ro"), "code": eff.get("code")})
            elif etype == "set_deadline":
                step = eff.get("step_id")
                if step:
                    result.deadlines[step] = _compute_deadline(eff.get("value") or {}, facts, ctx)
            elif etype == "trigger_child_event":
                _add(result.child_events, eff.get("event_type_id") or eff.get("value"))
            elif etype == "set_freshness_state":
                result.freshness.append({"step_id": eff.get("step_id"), "value": eff.get("value")})

    for step_id in excluded_steps:
        if step_id in result.included_steps:
            result.included_steps.remove(step_id)

    if result.missing_facts:
        result.status = "needs_facts"
    elif result.conflicts:
        result.status = "conflicting"
    elif result.blocks:
        result.status = "blocked"
    elif result.confirmations:
        result.status = "needs_confirmation"
    else:
        result.status = "resolved"
    return result
