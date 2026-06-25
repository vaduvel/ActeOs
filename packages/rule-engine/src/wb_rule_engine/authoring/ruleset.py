"""Deterministic evaluation of a governed authoring ruleset.

``evaluate_ruleset`` consumes a ruleset in the authoring contract shape (the
``rules.yaml`` of a governed batch) plus a citizen's facts, and produces a
``RouteResult``: included steps, requirements, channels, advice, warnings,
confirmations and the user-answerable facts still missing.

Pure and deterministic: no IO, no network, no clock. ``reference_date`` and
``jurisdiction_path`` are injected by the caller (the golden runner or the API).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Mapping, Sequence

from ..dates import parse_date
from ..trivalent import Tri
from .ast import EvalContext, collect_fact_refs, evaluate
from .effects import effect_tag


@dataclass
class RouteResult:
    status: str = "ok"
    included_steps: list[str] = field(default_factory=list)
    requirements: list[str] = field(default_factory=list)
    channels: list[str] = field(default_factory=list)
    advice: list[dict] = field(default_factory=list)
    warnings: list[dict] = field(default_factory=list)
    confirmations: list[str] = field(default_factory=list)
    child_events: list[str] = field(default_factory=list)
    deadlines: list[dict] = field(default_factory=list)
    obligations: dict = field(default_factory=dict)
    freshness: list[dict] = field(default_factory=list)
    blocks: list[dict] = field(default_factory=list)
    missing_facts: list[str] = field(default_factory=list)
    fired_rule_ids: list[str] = field(default_factory=list)

    @property
    def advice_tags(self) -> list[str]:
        return [a["tag"] for a in self.advice if a.get("tag")]

    @property
    def warning_tags(self) -> list[str]:
        return [w["tag"] for w in self.warnings if w.get("tag")]


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


def _required_facts(ruleset: Mapping[str, Any]) -> list[str]:
    declared = ruleset.get("required_facts")
    if declared:
        return list(declared)
    seen: list[str] = []
    for rule in ruleset.get("rules", []):
        for ref in sorted(collect_fact_refs(rule.get("when", {}))):
            if ref not in seen:
                seen.append(ref)
    return seen


def _add(seq: list, value) -> None:
    if value is not None and value not in seq:
        seq.append(value)


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

    firing: list[Mapping[str, Any]] = []
    for rule in ruleset.get("rules", []):
        if not _jurisdiction_ok(rule, jurisdiction_path):
            continue
        if not _temporal_ok(rule, reference_date):
            continue
        if evaluate(rule.get("when", {"op": "const", "value": True}), facts, ctx) is Tri.TRUE:
            firing.append(rule)

    overridden: set[str] = set()
    for rule in firing:
        for rid in rule.get("override_rule_ids", []) or []:
            overridden.add(rid)
        for eff in rule.get("effects", []):
            if eff.get("type") == "override_rule":
                target = eff.get("rule_id") or eff.get("value")
                if target:
                    overridden.add(target)
    firing = [r for r in firing if r.get("id") not in overridden]

    excluded_steps: set[str] = set()
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
            elif etype == "block":
                result.blocks.append({"message_ro": eff.get("message_ro"), "code": eff.get("code")})
            elif etype == "set_deadline":
                result.deadlines.append({"step_id": eff.get("step_id"), "value": eff.get("value")})
            elif etype == "trigger_child_event":
                _add(result.child_events, eff.get("event_type_id") or eff.get("value"))
            elif etype == "set_freshness_state":
                result.freshness.append({"value": eff.get("value")})

    for step_id in excluded_steps:
        if step_id in result.included_steps:
            result.included_steps.remove(step_id)

    if result.blocks:
        result.status = "blocked"
    elif result.missing_facts:
        result.status = "needs_facts"
    else:
        result.status = "ok"
    return result
