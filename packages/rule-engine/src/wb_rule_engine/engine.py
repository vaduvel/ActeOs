"""Deterministic route resolution.

resolve(request, bundle, *, now) follows the algorithm in 05_RULE_ENGINE_SPEC.md:
select an applicable rule, canonicalize facts, evaluate typed gates/steps with
three-valued logic, resolve deadlines, order steps with a stable topological sort,
and compute a reproducible route_hash that excludes route_id and evaluated_at.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping

from .applicability import jurisdiction_matches, specificity, temporal_applies
from .canonical import sha256_hex
from .dates import parse_date
from .errors import InvalidRequest, NoApplicableRule, RuleConflict
from .facts import resolve_derived_facts
from .freshness import freshness_state, on_expiry_effect
from .graph import stable_topo_sort
from .predicates import evaluate
from .trivalent import Tri
from .version import ENGINE_VERSION

_CONFIDENCE_ORDER = [
    "verified",
    "verified_with_local_gap",
    "needs_confirmation",
    "conflicting",
    "expired",
]


def _worst_confidence(values: list[str]) -> str:
    worst = "verified"
    for v in values:
        if _CONFIDENCE_ORDER.index(v) > _CONFIDENCE_ORDER.index(worst):
            worst = v
    return worst


def _select_rule(bundle, intent_id, jurisdiction_id, reference_date):
    applicable = []
    for rule in bundle.get("rules", []):
        if rule.get("intent_id") != intent_id:
            continue
        scope_codes = rule.get("jurisdiction", {}).get("scope_codes", [])
        matched = jurisdiction_matches(scope_codes, jurisdiction_id)
        if matched is None:
            continue
        if not temporal_applies(rule.get("temporal", {}), reference_date):
            continue
        applicable.append((specificity(rule, matched), rule))
    if not applicable:
        raise NoApplicableRule(
            f"no rule for intent={intent_id} jurisdiction={jurisdiction_id} at {reference_date}"
        )
    applicable.sort(key=lambda t: t[0], reverse=True)
    top_spec = applicable[0][0]
    top = [r for (spec, r) in applicable if spec == top_spec]
    if len(top) > 1:
        ids = sorted(r["rule_id"] for r in top)
        raise RuleConflict(
            "multiple equally specific rules; needs lawful precedence: " + ", ".join(ids)
        )
    return applicable[0][1]


def _resolve_deadline(deadline: Mapping[str, Any], facts: Mapping[str, Any]) -> dict:
    kind = deadline.get("kind", "none")
    result: dict[str, Any] = {"kind": kind, "timezone": deadline.get("timezone", "Europe/Bucharest")}
    if kind in ("fixed_window", "fixed_instant"):
        result["starts_at"] = deadline.get("starts_at")
        result["ends_at"] = deadline.get("ends_at")
    elif kind == "relative":
        base_fact = deadline.get("relative_to_fact")
        offset = deadline.get("offset_days")
        base = parse_date(facts.get(base_fact)) if base_fact else None
        if base is not None and offset is not None:
            result["ends_at"] = (base + timedelta(days=int(offset))).isoformat()
        else:
            result["ends_at"] = None
            result["pending"] = True
    return result


def resolve(request: Mapping[str, Any], bundle: Mapping[str, Any], *, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    for key in ("intent_id", "jurisdiction_id", "reference_date", "facts"):
        if key not in request:
            raise InvalidRequest(f"missing request field: {key}")
    intent_id = request["intent_id"]
    jurisdiction_id = request["jurisdiction_id"]
    reference_date = parse_date(request["reference_date"])
    if reference_date is None:
        raise InvalidRequest("reference_date must be an ISO date")
    input_facts = dict(request["facts"])

    rule = _select_rule(bundle, intent_id, jurisdiction_id, reference_date)
    facts = resolve_derived_facts(
        rule.get("facts", []),
        input_facts,
        reference_date=reference_date,
        jurisdiction_id=jurisdiction_id,
    )

    warnings: list[dict] = []
    conflicts: list[dict] = []
    unresolved: list[dict] = []
    confidence_inputs = [c.get("confidence", "verified") for c in rule.get("source_claims", [])]

    fr = rule.get("freshness", {})
    fr_state = freshness_state(fr, now)
    if fr_state == "expired":
        eff = on_expiry_effect(fr)
        if eff == "block":
            confidence_inputs.append("expired")
        elif eff == "needs_confirmation":
            confidence_inputs.append("needs_confirmation")
        warnings.append({"code": "RULE_SOURCE_STALE", "message": "Sursa a depasit pragul de prospetime."})
    elif fr_state == "review_due":
        warnings.append({"code": "RULE_SOURCE_STALE", "message": "Sursa asteapta reverificare."})

    gate_results: list[dict] = []
    for gate in sorted(rule.get("gates", []), key=lambda g: (int(g.get("priority", 0)), g["id"])):
        res = evaluate(gate["when"], facts)
        effect = gate["effect"]
        if res is Tri.TRUE:
            if effect == "block":
                gate_results.append({
                    "id": gate["id"], "effect": "block", "code": gate["code"],
                    "message": gate["message"], "recovery_actions": gate.get("recovery_actions", []),
                })
                confidence_inputs.append("needs_confirmation")
            elif effect == "needs_confirmation":
                unresolved.append({"gate_id": gate["id"], "code": gate["code"], "message": gate["message"]})
                confidence_inputs.append("needs_confirmation")
            elif effect == "warn":
                warnings.append({"code": gate["code"], "message": gate["message"]})
        elif res is Tri.UNKNOWN and effect in ("block", "needs_confirmation"):
            unresolved.append({
                "gate_id": gate["id"], "code": gate["code"], "message": gate["message"],
                "reason": "fapt necunoscut",
            })
            confidence_inputs.append("needs_confirmation")

    blocked = any(g["effect"] == "block" for g in gate_results)

    included_steps: list[dict] = []
    for step in rule.get("steps", []):
        res = evaluate(step.get("applies_when", {"constant": True}), facts)
        if res is Tri.TRUE:
            included_steps.append(step)
        elif res is Tri.UNKNOWN:
            included_steps.append(step)
            unresolved.append({"step_id": step["id"], "reason": "aplicabilitate necunoscuta"})
            confidence_inputs.append("needs_confirmation")

    included_ids = {s["id"] for s in included_steps}
    sortable: list[dict] = []
    for s in included_steps:
        for dep in s.get("depends_on", []):
            if dep not in included_ids:
                warnings.append({
                    "code": "DANGLING_DEPENDENCY",
                    "message": f"Pasul {s['id']} depinde de {dep} care nu se aplica.",
                })
        sc = dict(s)
        sc["depends_on"] = [d for d in s.get("depends_on", []) if d in included_ids]
        sortable.append(sc)
    ordered = stable_topo_sort(sortable)

    out_steps: list[dict] = []
    out_requirements: list[dict] = []
    for s in ordered:
        applicable_reqs: list[str] = []
        for req in s.get("requirements", []):
            r = evaluate(req.get("applies_when", {"constant": True}), facts)
            if r is Tri.FALSE:
                continue
            applicable_reqs.append(req["id"])
            out_requirements.append({
                "id": req["id"], "step_id": s["id"], "title": req["title"],
                "obligation": req["obligation"], "timing": req["timing"],
                "accepted_forms": req["accepted_forms"], "readiness_status": "unknown",
                "applies": "yes" if r is Tri.TRUE else "needs_confirmation",
                "source_claim_ids": req.get("source_claim_ids", []),
            })
            if r is Tri.UNKNOWN:
                confidence_inputs.append("needs_confirmation")
        out_steps.append({
            "id": s["id"], "title": s["title"], "instruction": s["instruction"],
            "deadline": _resolve_deadline(s.get("deadline", {"kind": "none"}), facts),
            "requirement_ids": applicable_reqs,
            "completion_evidence": s.get("completion_evidence"),
            "recovery_actions": s.get("recovery_actions", []),
            "official_channel_ids": s.get("official_channel_ids", []),
            "source_claim_ids": s.get("source_claim_ids", []),
            "blocked": blocked,
        })

    confidence = _worst_confidence(confidence_inputs) if confidence_inputs else "verified"

    core = {
        "engine_version": ENGINE_VERSION,
        "intent_id": intent_id,
        "jurisdiction_id": jurisdiction_id,
        "reference_date": reference_date.isoformat(),
        "rule_id": rule["rule_id"],
        "rule_bundle_version": bundle.get("bundle_version"),
        "rule_bundle_hash": sha256_hex(bundle),
        "facts_hash": sha256_hex({k: input_facts[k] for k in sorted(input_facts)}),
        "confidence": confidence,
        "blocked": blocked,
        "steps": out_steps,
        "requirements": out_requirements,
        "gates": gate_results,
        "unresolved_questions": unresolved,
        "conflicts": conflicts,
        "warnings": warnings,
    }
    route_hash = sha256_hex(core)

    output = dict(core)
    output["route_id"] = str(uuid.uuid4())
    output["evaluated_at"] = now.astimezone(timezone.utc).isoformat()
    output["route_hash"] = route_hash
    return output
