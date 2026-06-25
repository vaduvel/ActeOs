"""Golden fixture runner for governed authoring rulesets.

Evaluates each fixture in a batch's ``fixtures/golden.yaml`` against the batch's
``rules.yaml`` and asserts the declared expectations. Set-style expectations are
subset checks (the route must *contain* the expected items); ``*_absent`` checks
assert the items are not present; ``missing_facts`` is an exact set match.

Pure (no IO): callers pass already-parsed dicts. Use the loader/cli for files.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from .ruleset import evaluate_ruleset


@dataclass
class FixtureFailure:
    fixture_id: str
    checks: list[str] = field(default_factory=list)


@dataclass
class GoldenReport:
    batch_id: str
    total: int = 0
    passed: int = 0
    failures: list[FixtureFailure] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures

    def summary(self) -> str:
        return f"{self.batch_id}: {self.passed}/{self.total} passed, {len(self.failures)} failed"


def _subset(expected: Iterable[str] | None, actual: list[str], label: str, checks: list[str]) -> None:
    missing = [x for x in (expected or []) if x not in set(actual)]
    if missing:
        checks.append(f"{label}: missing {missing} (got {sorted(actual)})")


def _absent(forbidden: Iterable[str] | None, actual: list[str], label: str, checks: list[str]) -> None:
    present = [x for x in (forbidden or []) if x in set(actual)]
    if present:
        checks.append(f"{label}: unexpectedly present {present}")


def run_fixtures(batch: Mapping[str, Any]) -> GoldenReport:
    ruleset = batch["ruleset"]
    spec = batch["fixtures"]
    defaults = spec.get("defaults", {})
    report = GoldenReport(batch_id=spec.get("batch_id", ruleset.get("batch_id", "unknown")))

    for fx in spec.get("fixtures", []):
        report.total += 1
        checks: list[str] = []
        facts = fx.get("facts", {}) or {}
        jp = fx.get("jurisdiction_path", defaults.get("jurisdiction_path", []))
        ref = fx.get("reference_date", defaults.get("reference_date"))
        result = evaluate_ruleset(ruleset, facts, jurisdiction_path=jp, reference_date=ref)
        expect = fx.get("expect", {}) or {}

        if "status" in expect and result.status != expect["status"]:
            checks.append(f"status: expected {expect['status']} got {result.status}")
        _subset(expect.get("included_steps"), result.included_steps, "included_steps", checks)
        _subset(expect.get("requirements"), result.requirements, "requirements", checks)
        _absent(expect.get("requirements_absent"), result.requirements, "requirements_absent", checks)
        _subset(expect.get("channels"), result.channels, "channels", checks)
        _absent(expect.get("channels_absent"), result.channels, "channels_absent", checks)
        _subset(expect.get("advice_tags"), result.advice_tags, "advice_tags", checks)
        _absent(expect.get("advice_absent"), result.advice_tags, "advice_absent", checks)
        _subset(expect.get("warnings_present"), result.warning_tags, "warnings_present", checks)
        _subset(expect.get("needs_confirmation"), result.confirmations, "needs_confirmation", checks)
        if "missing_facts" in expect:
            if set(expect["missing_facts"]) != set(result.missing_facts):
                checks.append(
                    f"missing_facts: expected {sorted(expect['missing_facts'])} got {sorted(result.missing_facts)}"
                )

        if checks:
            report.failures.append(FixtureFailure(fixture_id=fx.get("id", "?"), checks=checks))
        else:
            report.passed += 1
    return report
