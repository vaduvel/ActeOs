"""Lawful precedence resolution among equally-specific candidate rules.

When jurisdiction/temporal specificity does not single out one rule, we apply
classic lawful precedence using only fields present in rule.schema.json:
  1. higher authority wins (eu > national > county > uat > institution)
  2. lex posterior derogat priori: the more recent effective_from wins
  3. if still indistinguishable it is a genuine conflict -> pick deterministically
     by rule_id and surface a conflict note so confidence drops to 'conflicting'.
"""
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


def _authority_rank(rule: dict) -> int:
    scope = rule.get("jurisdiction", {}).get("authority_scope", "national")
    return _AUTHORITY_RANK.get(scope, 0)


def _lawful_key(rule: dict) -> tuple[int, int]:
    eff = parse_date(rule.get("temporal", {}).get("effective_from")) or date.min
    return (_authority_rank(rule), eff.toordinal())


def resolve_precedence(rules: list[dict]) -> tuple[dict, list[dict]]:
    """Return (winning_rule, conflicts) for a set of candidate rules."""
    if len(rules) == 1:
        return rules[0], []
    ranked = sorted(rules, key=lambda r: (_lawful_key(r), r["rule_id"]), reverse=True)
    winner = ranked[0]
    tied = [r for r in ranked if _lawful_key(r) == _lawful_key(winner)]
    conflicts: list[dict] = []
    if len(tied) > 1:
        conflicts.append({
            "code": "RULE_CONFLICT_UNRESOLVED",
            "message": "Reguli echivalente ca autoritate si data; selectie determinista, necesita confirmare.",
            "rule_ids": sorted(r["rule_id"] for r in tied),
            "selected_rule_id": winner["rule_id"],
        })
    return winner, conflicts
