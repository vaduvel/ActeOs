from __future__ import annotations

from datetime import date

from .dates import parse_date

_AUTHORITY_RANK = {
    "eu": 100,
    "national": 80,
    "county": 60,
    "uat": 40,
    "institution": 20,
}


def jurisdiction_matches(scope_codes: list[str], jurisdiction_id: str) -> str | None:
    """Return the most specific matching scope code, or None.

    A scope matches if the request jurisdiction equals it or is a descendant
    (dot-path), e.g. scope 'ro.timis' matches 'ro.timis.timisoara'.
    """
    best: str | None = None
    for scope in scope_codes:
        if jurisdiction_id == scope or jurisdiction_id.startswith(scope + "."):
            if best is None or len(scope) > len(best):
                best = scope
    return best


def temporal_applies(temporal: dict, reference_date: date) -> bool:
    eff_from = parse_date(temporal.get("effective_from"))
    eff_to = parse_date(temporal.get("effective_to"))
    if eff_from is not None and reference_date < eff_from:
        return False
    if eff_to is not None and reference_date > eff_to:
        return False
    return True


def specificity(rule: dict, matched_scope: str) -> tuple[int, int]:
    """Higher tuple = more specific: (scope depth, authority closeness)."""
    depth = matched_scope.count(".")
    authority = rule.get("jurisdiction", {}).get("authority_scope", "national")
    closeness = 100 - _AUTHORITY_RANK.get(authority, 0)
    return (depth, closeness)
