"""Golden fixture runner for governed authoring rulesets (rich contract).

Evaluates each fixture in a batch's ``fixtures/golden.yaml`` against the batch's
``rules.yaml`` and asserts the declared expectations.

Canonical expect keys:
  status (ok/resolved treated as synonyms), included_steps, steps_absent,
  requirements, requirements_absent, channels, channels_absent, advice_tags,
  advice_absent, warnings, warnings_absent, confirmations, confirmations_absent,
  conflicts, blocked_effects, overridden_rules, overridden_rules_absent,
  overdue_steps, obligations {req: value}, deadlines {step: 'YYYY-MM-DD'},
  missing_facts (exact set).

Accepted aliases (legacy fixture vocabulary): warnings_present->warnings,
needs_confirmation->confirmations, not_included->steps_absent.

Set-style expectations are subset checks; ``*_absent`` assert non-presence;
``deadlines``/``obligations`` are per-key exact; ``missing_facts`` is an exact
set. Pure (no IO): callers pass parsed dicts. Use the loader/cli for files.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from .ruleset import evaluate_ruleset

_SUCCESS = frozenset({"ok", "resolved"})


@dataclass
class FixtureFailure:
    fixture_id: str
    checks: list = field(default_factory=list)


@dataclass
class GoldenReport:
    batch_id: str
    total: int = 0
    passed: int = 0
    failures: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures

    def summary(self) -> str:
        return f"{self.batch_id}: {self.passed}/{self.total} passed, {len(self.failures)} failed"


def _subset(expected: Iterable | None, actual: list, label: str, checks: list) -> None:
    missing = [x for x in (expected or []) if x not in set(actual)]
    if missing:
        checks.append(f"{label}: missing {missing} (got {sorted(actual)})")


def _absent(forbidden: Iterable | None, actual: list, label: str, checks: list) -> None:
    present = [x for x in (forbidden or []) if x in set(actual)]
    if present:
        checks.append(f"{label}: unexpectedly present {present}")


def _check_status(expected: str, actual: str, checks: list) -> None:
    if expected in _SUCCESS and actual in _SUCCESS:
        return
    if expected != actual:
        checks.append(f"status: expected {expected} got {actual}")


def run_fixtures(batch: Mapping[str, Any]) -> GoldenReport:
    ruleset = batch["ruleset"]
    spec = batch["fixtures"]
    defaults = spec.get("defaults", {})
    report = GoldenReport(batch_id=spec.get("batch_id", ruleset.get("batch_id", "unknown")))

    for fx in spec.get("fixtures", []):
        report.total += 1
        checks: list = []
        facts = fx.get("facts", {}) or {}
        jp = fx.get("jurisdiction_path", defaults.get("jurisdiction_path", []))
        ref = fx.get("reference_date", defaults.get("reference_date"))
        result = evaluate_ruleset(ruleset, facts, jurisdiction_path=jp, reference_date=ref)
        expect = fx.get("expect", {}) or {}

        if "status" in expect:
            _check_status(expect["status"], result.status, checks)

        _subset(expect.get("included_steps"), result.included_steps, "included_steps", checks)
        _absent(expect.get("steps_absent") or expect.get("not_included"), result.included_steps, "steps_absent", checks)
        _subset(expect.get("requirements"), result.requirements, "requirements", checks)
        _absent(expect.get("requirements_absent"), result.requirements, "requirements_absent", checks)
        _subset(expect.get("channels"), result.channels, "channels", checks)
        _absent(expect.get("channels_absent"), result.channels, "channels_absent", checks)
        _subset(expect.get("advice_tags"), result.advice_tags, "advice_tags", checks)
        _absent(expect.get("advice_absent"), result.advice_tags, "advice_absent", checks)
        _subset(expect.get("warnings") or expect.get("warnings_present"), result.warning_tags, "warnings", checks)
        _absent(expect.get("warnings_absent"), result.warning_tags, "warnings_absent", checks)
        _subset(expect.get("confirmations") or expect.get("needs_confirmation"), result.confirmations, "confirmations", checks)
        _absent(expect.get("confirmations_absent"), result.confirmations, "confirmations_absent", checks)
        _subset(expect.get("conflicts"), result.conflicts, "conflicts", checks)
        _subset(expect.get("blocked_effects"), result.blocked_effects, "blocked_effects", checks)
        _subset(expect.get("overridden_rules"), result.overridden_rules, "overridden_rules", checks)
        _absent(expect.get("overridden_rules_absent"), result.overridden_rules, "overridden_rules_absent", checks)
        _subset(expect.get("overdue_steps"), result.overdue_steps, "overdue_steps", checks)

        for rid, val in (expect.get("obligations") or {}).items():
            got = result.obligations.get(rid)
            if got != val:
                checks.append(f"obligations[{rid}]: expected {val} got {got}")

        for step, dt in (expect.get("deadlines") or {}).items():
            got = result.deadline_dates.get(step)
            if got != dt:
                checks.append(f"deadlines[{step}]: expected {dt} got {got}")

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
