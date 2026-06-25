"""Authoring-language rule evaluation (rich contract).

This subpackage evaluates governed rulesets written in the *authoring* contract
shape (contracts/rule.schema.json + contracts/predicate.schema.json), i.e. the
files under docs/product/lifeos-romania/research/inbox/<EVENT>/rules.yaml.

It is intentionally separate from the compiled runtime language in
wb_rule_engine.predicates/engine (operator/fact, gates/steps). The pure pieces
(ast, effects, ruleset, golden, orchestrator) import with no third-party
dependency. The file loaders (loader, cli) need PyYAML and the schema validator
(validate) needs jsonschema; both are imported lazily.
"""
from __future__ import annotations

from .ast import (
    EvalContext,
    UnsupportedOperator,
    collect_fact_refs,
    evaluate,
    resolve_date_token,
)
from .effects import EFFECT_TYPES, effect_tag
from .golden import FixtureFailure, GoldenReport, run_fixtures
from .orchestrator import EventNode, resolve_event
from .ruleset import RouteResult, evaluate_ruleset

__all__ = [
    "EvalContext",
    "UnsupportedOperator",
    "collect_fact_refs",
    "evaluate",
    "resolve_date_token",
    "EFFECT_TYPES",
    "effect_tag",
    "RouteResult",
    "evaluate_ruleset",
    "FixtureFailure",
    "GoldenReport",
    "run_fixtures",
    "EventNode",
    "resolve_event",
]
