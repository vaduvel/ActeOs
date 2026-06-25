"""Canonical error vocabulary (problem+json `type` codes)."""
from __future__ import annotations

from enum import Enum


class ProblemCode(str, Enum):
    VALIDATION_FAILED = "validation_failed"
    INTENT_NOT_FOUND = "intent_not_found"
    NO_APPLICABLE_RULE = "no_applicable_rule"
    BUNDLE_INCOMPATIBLE = "bundle_incompatible"
    RULE_CONFLICT = "rule_conflict"
    DEPENDENCY_CYCLE = "dependency_cycle"
    DANGLING_DEPENDENCY = "dangling_dependency"
    SOURCE_STALE = "source_stale"
    UNSUPPORTED_OPERATOR = "unsupported_operator"
    NOT_CONFIGURED = "not_configured"


class WbError(Exception):
    """Base error carrying a canonical problem code."""

    code: ProblemCode = ProblemCode.VALIDATION_FAILED

    def __init__(self, message: str, code: ProblemCode | None = None) -> None:
        super().__init__(message)
        if code is not None:
            self.code = code
        self.message = message

    def to_problem(self) -> dict:
        return {"type": self.code.value, "title": self.message}
