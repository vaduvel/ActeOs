"""Impact analysis: which claims and rules are affected by a source change.

Given a source_id and a change severity, determines which claims
and rules reference that source and computes impact.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from wb_ingestion.diff import ChangeSeverity


class ImpactLevel(str, Enum):
    """How urgently a change needs review."""

    NONE = "none"                    # no claims/rules affected
    INFORMATIONAL = "informational"  # cosmetic change, claims unaffected
    NEEDS_REVIEW = "needs_review"    # moderate change, review recommended
    URGENT = "urgent"                # critical change affecting critical claims/rules


@dataclass(frozen=True)
class AffectedClaim:
    """A claim affected by a source change."""

    claim_id: str
    source_id: str
    status: str  # active, in_review, draft
    confidence: str  # verified, verified_with_local_gap
    criticality: str  # critical, operational


@dataclass(frozen=True)
class AffectedRule:
    """A rule affected by a source change."""

    rule_id: str
    source_id: str
    severity: str  # critical, operational
    claim_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ImpactReport:
    """Complete impact analysis for a source change."""

    source_id: str
    change_severity: ChangeSeverity
    impact_level: ImpactLevel
    affected_claims: list[AffectedClaim] = field(default_factory=list)
    affected_rules: list[AffectedRule] = field(default_factory=list)
    summary: str = ""

    @property
    def critical_claims_affected(self) -> int:
        return sum(
            1 for c in self.affected_claims
            if c.criticality == "critical"
        )

    @property
    def critical_rules_affected(self) -> int:
        return sum(
            1 for r in self.affected_rules
            if r.severity == "critical"
        )


def compute_impact(
    source_id: str,
    change_severity: ChangeSeverity,
    affected_claims: list[AffectedClaim],
    affected_rules: list[AffectedRule],
) -> ImpactReport:
    """Compute the impact level of a source change.

    Rules:
    - No affected claims/rules → NONE
    - Cosmetic change → INFORMATIONAL
    - Moderate change with affected claims → NEEDS_REVIEW
    - Critical change, or moderate with critical claims/rules → URGENT
    """
    if not affected_claims and not affected_rules:
        level = ImpactLevel.NONE
    elif change_severity == ChangeSeverity.NONE:
        level = ImpactLevel.NONE
    elif change_severity == ChangeSeverity.COSMETIC:
        level = ImpactLevel.INFORMATIONAL
    elif change_severity == ChangeSeverity.CRITICAL:
        level = ImpactLevel.URGENT
    else:
        # Moderate
        has_critical = any(
            c.criticality == "critical" for c in affected_claims
        ) or any(
            r.severity == "critical" for r in affected_rules
        )
        level = ImpactLevel.URGENT if has_critical else ImpactLevel.NEEDS_REVIEW

    critical_claims = sum(1 for c in affected_claims if c.criticality == "critical")
    critical_rules = sum(1 for r in affected_rules if r.severity == "critical")

    summary = (
        f"Source {source_id}: {change_severity.value} change → {level.value}. "
        f"{len(affected_claims)} claims ({critical_claims} critical), "
        f"{len(affected_rules)} rules ({critical_rules} critical)."
    )

    return ImpactReport(
        source_id=source_id,
        change_severity=change_severity,
        impact_level=level,
        affected_claims=affected_claims,
        affected_rules=affected_rules,
        summary=summary,
    )
