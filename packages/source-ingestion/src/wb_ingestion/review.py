"""Human review workflow.

Critical changes require two distinct reviewers. Non-critical
changes require one. An author cannot approve their own change.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum

from wb_ingestion.errors import IngestionProblemCode, ReviewError
from wb_ingestion.impact import ImpactLevel


class ReviewAction(str, Enum):
    """Possible review actions."""

    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_CHANGES = "request_changes"


class ReviewStatus(str, Enum):
    """Status of a review cycle."""

    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    CHANGES_REQUESTED = "changes_requested"


@dataclass(frozen=True)
class Review:
    """A single review by a human reviewer."""

    reviewer_id: str
    action: ReviewAction
    comment: str = ""
    reviewed_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class ReviewCycle:
    """A complete review cycle for a change.

    Tracks all reviews and determines when enough approvals
    have been collected based on the change's impact level.
    """

    change_id: str
    author_id: str
    impact_level: ImpactLevel
    status: ReviewStatus = ReviewStatus.PENDING
    reviews: list[Review] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def required_approvals(self) -> int:
        """Number of approvals needed based on impact level."""
        if self.impact_level in (ImpactLevel.URGENT,):
            return 2  # critical changes need two reviewers
        return 1

    @property
    def approvals(self) -> list[Review]:
        return [r for r in self.reviews if r.action == ReviewAction.APPROVE]

    @property
    def is_approved(self) -> bool:
        return (
            len(self.approvals) >= self.required_approvals
            and self.status != ReviewStatus.REJECTED
        )

    @property
    def is_rejected(self) -> bool:
        return self.status == ReviewStatus.REJECTED

    @property
    def reviewer_ids(self) -> set[str]:
        return {r.reviewer_id for r in self.reviews}


def submit_review(
    cycle: ReviewCycle,
    reviewer_id: str,
    action: ReviewAction,
    comment: str = "",
) -> ReviewCycle:
    """Submit a review for a change.

    Validates:
    - Reviewer is not the author (self-approval forbidden)
    - Reviewer hasn't already reviewed (one review per person)
    - Cycle is not already approved/rejected

    Returns updated ReviewCycle.
    """
    if reviewer_id == cycle.author_id:
        raise ReviewError(
            IngestionProblemCode.REVIEW_SELF_APPROVAL,
            f"Author {reviewer_id} cannot review their own change {cycle.change_id}",
        )

    if reviewer_id in cycle.reviewer_ids:
        raise ReviewError(
            IngestionProblemCode.REVIEW_REQUIRED,
            f"Reviewer {reviewer_id} already reviewed change {cycle.change_id}",
        )

    if cycle.status in (ReviewStatus.APPROVED, ReviewStatus.REJECTED):
        raise ReviewError(
            IngestionProblemCode.REVIEW_REQUIRED,
            f"Change {cycle.change_id} is already {cycle.status.value}",
        )

    review = Review(
        reviewer_id=reviewer_id,
        action=action,
        comment=comment,
    )
    cycle.reviews.append(review)
    cycle.status = ReviewStatus.IN_REVIEW

    # Update status based on action
    if action == ReviewAction.REJECT:
        cycle.status = ReviewStatus.REJECTED
    elif action == ReviewAction.REQUEST_CHANGES:
        cycle.status = ReviewStatus.CHANGES_REQUESTED
    elif cycle.is_approved:
        cycle.status = ReviewStatus.APPROVED

    return cycle


def create_review_cycle(
    change_id: str,
    author_id: str,
    impact_level: ImpactLevel,
) -> ReviewCycle:
    """Create a new review cycle for a change."""
    return ReviewCycle(
        change_id=change_id,
        author_id=author_id,
        impact_level=impact_level,
    )
