"""Adapters between the rule-engine output and the public API contract.

The engine speaks an internal, hash-stable dialect; the API speaks
`08_API_SPEC.yaml`. All translation lives here so the engine stays pure and the
routers stay thin. No business decisions are made here — only shape mapping.
"""
from __future__ import annotations

from typing import Any

from . import schemas as S

_OBLIGATION = {
    "required": "mandatory", "mandatory": "mandatory", "conditional": "conditional",
    "optional": "optional", "recommended": "optional", "later": "later",
}
_DEADLINE_ORIGIN = {"fixed_window": "fixed", "fixed_instant": "fixed", "relative": "calendar_rule"}


def route_status(engine_output: dict) -> str:
    if engine_output.get("blocked"):
        return "blocked"
    if engine_output.get("missing_facts"):
        return "needs_facts"
    return "resolved"


def _deadline(d: dict | None) -> S.Deadline | None:
    if not d or d.get("kind", "none") == "none":
        return None
    return S.Deadline(
        starts_at=d.get("starts_at"),
        ends_at=d.get("ends_at"),
        timezone=d.get("timezone", "Europe/Bucharest"),
        derived_from=_DEADLINE_ORIGIN.get(d.get("kind")),
    )


def _requirement(r: dict) -> S.ResolvedRequirement:
    return S.ResolvedRequirement(
        id=r["id"],
        title=r["title"],
        obligation=_OBLIGATION.get(r.get("obligation", ""), "mandatory"),
        applies="yes" if r.get("applies") == "yes" else "unknown",
        accepted_forms=[f for f in r.get("accepted_forms", []) if f in ("original", "copy", "electronic", "certified_copy")] or None,
        readiness_checks=r.get("readiness_checks", []),
        source_claim_ids=r.get("source_claim_ids", []),
    )


def to_route_resolution(engine_output: dict) -> S.RouteResolution:
    status = route_status(engine_output)
    reqs_by_step: dict[str, list[dict]] = {}
    for r in engine_output.get("requirements", []):
        reqs_by_step.setdefault(r["step_id"], []).append(r)

    steps: list[S.ResolvedStep] = []
    for idx, s in enumerate(engine_output.get("steps", []), start=1):
        if s.get("blocked"):
            state = "blocked"
        elif idx == 1:
            state = "actionable"
        else:
            state = "upcoming"
        steps.append(S.ResolvedStep(
            id=s["id"], title=s["title"], sequence=idx, state=state,
            instruction=s.get("instruction"), deadline=_deadline(s.get("deadline")),
            requirements=[_requirement(r) for r in reqs_by_step.get(s["id"], [])],
            completion_evidence=s.get("completion_evidence") or "Confirmarea finalizarii pasului.",
            recovery_actions=s.get("recovery_actions", []),
            source_claim_ids=s.get("source_claim_ids", []),
        ))

    issues: list[S.RouteIssue] = []
    for g in engine_output.get("gates", []):
        issues.append(S.RouteIssue(code=g["code"], severity="blocking", message=g["message"]))
    for c in engine_output.get("conflicts", []):
        issues.append(S.RouteIssue(code=c.get("code", "rule_conflict"), severity="warning", message=c.get("message", "Conflict de reguli.")))
    for w in engine_output.get("warnings", []):
        issues.append(S.RouteIssue(code=w.get("code", "warning"), severity="warning", message=w.get("message", "")))

    missing = [S.FactQuestion(**mf) for mf in engine_output.get("missing_facts", [])]

    return S.RouteResolution(
        status=status,
        route_hash=engine_output.get("route_hash"),
        rule_bundle_hash=engine_output.get("rule_bundle_hash"),
        facts_hash=engine_output["facts_hash"],
        engine_version=engine_output["engine_version"],
        evaluated_at=engine_output["evaluated_at"],
        missing_facts=missing,
        steps=steps,
        blocking_issues=issues,
        confidence=engine_output.get("confidence"),
    )


def _next_action(resolution: S.RouteResolution) -> tuple[str | None, Any]:
    for step in resolution.steps:
        if step.state == "actionable":
            deadline = step.deadline.ends_at if step.deadline else None
            return step.title, deadline
    return None, None


def build_journey(journey, resolution: S.RouteResolution, requirement_states, fact_inputs: list[dict]) -> S.Journey:
    next_title, next_deadline = _next_action(resolution)
    return S.Journey(
        id=journey.id,
        intent_id=journey.intent_id,
        title=journey.title,
        status=journey.status,
        next_action_title=next_title,
        next_deadline=next_deadline,
        updated_at=journey.updated_at,
        jurisdiction_id=journey.jurisdiction_id,
        created_at=journey.created_at,
        facts=[S.FactInput(fact_id=f["fact_id"], value=f["value"], source=f["source"]) for f in fact_inputs],
        resolution=resolution,
        requirement_states=[
            S.RequirementState(requirement_id=rs.requirement_id, status=rs.status, note=None, updated_at=rs.updated_at)
            for rs in requirement_states
        ],
    )


def build_summary(journey, resolution: S.RouteResolution | None = None) -> S.JourneySummary:
    next_title, next_deadline = _next_action(resolution) if resolution else (None, None)
    return S.JourneySummary(
        id=journey.id, intent_id=journey.intent_id, title=journey.title, status=journey.status,
        next_action_title=next_title, next_deadline=next_deadline, updated_at=journey.updated_at,
    )
