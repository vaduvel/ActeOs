from __future__ import annotations


class EngineError(Exception):
    code = "engine_error"


class InvalidRequest(EngineError):
    code = "validation_failed"


class NoApplicableRule(EngineError):
    code = "no_applicable_rule"


class RuleConflict(EngineError):
    code = "rule_conflict"


class DependencyCycle(EngineError):
    code = "dependency_cycle"
