from __future__ import annotations

from datetime import date
from typing import Any, Mapping

from .dates import completed_years, parse_date


def resolve_derived_facts(
    fact_defs: list[dict],
    facts: Mapping[str, Any],
    *,
    reference_date: date,
    jurisdiction_id: str,
) -> dict[str, Any]:
    """Return a new facts map with derived facts added.

    Supported derive functions (per rule.schema.json):
    - age_on_date(inputs=[date_fact]) -> completed years at reference_date
    - date_from_context() -> reference_date
    - jurisdiction_from_context() -> jurisdiction_id
    """
    resolved = dict(facts)
    for fd in fact_defs:
        derive = fd.get("derive")
        if not derive:
            continue
        fn = derive["function"]
        inputs = derive.get("inputs", [])
        if fn == "date_from_context":
            resolved[fd["id"]] = reference_date.isoformat()
        elif fn == "jurisdiction_from_context":
            resolved[fd["id"]] = jurisdiction_id
        elif fn == "age_on_date":
            if not inputs:
                continue
            birth = parse_date(resolved.get(inputs[0]))
            if birth is not None:
                resolved[fd["id"]] = completed_years(birth, reference_date)
    return resolved
