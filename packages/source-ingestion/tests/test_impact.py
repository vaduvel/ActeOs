"""Tests for impact analysis."""

from __future__ import annotations

from wb_ingestion.diff import ChangeSeverity
from wb_ingestion.impact import (
    AffectedClaim,
    AffectedRule,
    ImpactLevel,
    compute_impact,
)


class TestComputeImpact:
    def test_no_affected(self) -> None:
        report = compute_impact("src1", ChangeSeverity.MODERATE, [], [])
        assert report.impact_level == ImpactLevel.NONE
        assert report.critical_claims_affected == 0

    def test_cosmetic_change_informational(self) -> None:
        claims = [
            AffectedClaim(
                claim_id="c1", source_id="src1",
                status="active", confidence="verified",
                criticality="critical",
            )
        ]
        report = compute_impact("src1", ChangeSeverity.COSMETIC, claims, [])
        assert report.impact_level == ImpactLevel.INFORMATIONAL

    def test_moderate_change_needs_review(self) -> None:
        claims = [
            AffectedClaim(
                claim_id="c1", source_id="src1",
                status="active", confidence="verified",
                criticality="operational",
            )
        ]
        report = compute_impact("src1", ChangeSeverity.MODERATE, claims, [])
        assert report.impact_level == ImpactLevel.NEEDS_REVIEW

    def test_moderate_with_critical_claims_urgent(self) -> None:
        claims = [
            AffectedClaim(
                claim_id="c1", source_id="src1",
                status="active", confidence="verified",
                criticality="critical",
            )
        ]
        report = compute_impact("src1", ChangeSeverity.MODERATE, claims, [])
        assert report.impact_level == ImpactLevel.URGENT

    def test_critical_change_always_urgent(self) -> None:
        claims = [
            AffectedClaim(
                claim_id="c1", source_id="src1",
                status="active", confidence="verified",
                criticality="operational",
            )
        ]
        report = compute_impact("src1", ChangeSeverity.CRITICAL, claims, [])
        assert report.impact_level == ImpactLevel.URGENT

    def test_critical_with_rules(self) -> None:
        rules = [
            AffectedRule(
                rule_id="r1", source_id="src1",
                severity="critical", claim_ids=["c1"],
            )
        ]
        report = compute_impact("src1", ChangeSeverity.CRITICAL, [], rules)
        assert report.impact_level == ImpactLevel.URGENT
        assert report.critical_rules_affected == 1

    def test_summary_content(self) -> None:
        claims = [
            AffectedClaim(
                claim_id="c1", source_id="src1",
                status="active", confidence="verified",
                criticality="critical",
            )
        ]
        report = compute_impact("src1", ChangeSeverity.MODERATE, claims, [])
        assert "src1" in report.summary
        assert "1 claims" in report.summary
        assert "1 critical" in report.summary
