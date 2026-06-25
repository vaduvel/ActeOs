"""Multi-event orchestration over governed rulesets.

A single life event (e.g. ``ro.life.child_born``) can pull in other events via
the ``trigger_child_event`` effect (birth registration, CNP, allowance, ...).
``resolve_event`` evaluates the root ruleset and recursively resolves every
triggered child, aggregating the result into an ``EventNode`` tree.

Pure and deterministic: rulesets are passed in, keyed by event_type_id; the
clock (reference_date) and jurisdiction are injected. Cycles are guarded.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from .ruleset import RouteResult, evaluate_ruleset


@dataclass
class EventNode:
    event_type_id: str
    route: RouteResult
    children: list["EventNode"] = field(default_factory=list)

    def flatten(self) -> list["EventNode"]:
        out: list["EventNode"] = [self]
        for child in self.children:
            out.extend(child.flatten())
        return out

    def event_ids(self) -> list[str]:
        return [node.event_type_id for node in self.flatten()]


def resolve_event(
    event_type_id: str,
    rulesets_by_event: Mapping[str, Any],
    facts: Mapping[str, Any],
    *,
    jurisdiction_path: Sequence[str] = (),
    reference_date: Any = None,
    _seen: frozenset[str] | None = None,
) -> EventNode:
    ruleset = rulesets_by_event.get(event_type_id)
    if ruleset is None:
        raise KeyError(f"no ruleset for event_type_id={event_type_id}")

    seen = frozenset() if _seen is None else _seen
    route = evaluate_ruleset(
        ruleset, facts, jurisdiction_path=jurisdiction_path, reference_date=reference_date
    )
    node = EventNode(event_type_id=event_type_id, route=route)

    if event_type_id in seen:
        return node  # cycle guard: do not re-expand children
    seen = seen | {event_type_id}

    for child_id in route.child_events:
        if child_id in rulesets_by_event:
            node.children.append(
                resolve_event(
                    child_id,
                    rulesets_by_event,
                    facts,
                    jurisdiction_path=jurisdiction_path,
                    reference_date=reference_date,
                    _seen=seen,
                )
            )
        else:
            node.children.append(
                EventNode(event_type_id=child_id, route=RouteResult(status="unknown_event"))
            )
    return node
