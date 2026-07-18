"""Tests for human review workflow."""

from __future__ import annotations

import pytest

from wb_ingestion.errors import ReviewError
from wb_ingestion.impact import ImpactLevel
from wb_ingestion.review import (
    ReviewAction,
    ReviewStatus,
    create_review_cycle,
    submit_review,
)


class TestReviewCycle:
    def test_create_cycle(self) -> None:
        cycle = create_review_cycle("chg1", "author1", ImpactLevel.NEEDS_REVIEW)
        assert cycle.status == ReviewStatus.PENDING
        assert cycle.required_approvals == 1

    def test_urgent_requires_two_approvals(self) -> None:
        cycle = create_review_cycle("chg1", "author1", ImpactLevel.URGENT)
        assert cycle.required_approvals == 2

    def test_single_approval_sufficient(self) -> None:
        cycle = create_review_cycle("chg1", "author1", ImpactLevel.NEEDS_REVIEW)
        cycle = submit_review(cycle, "reviewer1", ReviewAction.APPROVE)
        assert cycle.is_approved
        assert cycle.status == ReviewStatus.APPROVED

    def test_urgent_needs_two_reviewers(self) -> None:
        cycle = create_review_cycle("chg1", "author1", ImpactLevel.URGENT)
        cycle = submit_review(cycle, "reviewer1", ReviewAction.APPROVE)
        assert not cycle.is_approved  # only 1 of 2 required

        cycle = submit_review(cycle, "reviewer2", ReviewAction.APPROVE)
        assert cycle.is_approved
        assert cycle.status == ReviewStatus.APPROVED

    def test_self_approval_forbidden(self) -> None:
        cycle = create_review_cycle("chg1", "author1", ImpactLevel.NEEDS_REVIEW)
        with pytest.raises(ReviewError, match="cannot review their own"):
            submit_review(cycle, "author1", ReviewAction.APPROVE)

    def test_duplicate_review_forbidden(self) -> None:
        cycle = create_review_cycle("chg1", "author1", ImpactLevel.URGENT)
        cycle = submit_review(cycle, "reviewer1", ReviewAction.APPROVE)
        with pytest.raises(ReviewError, match="already reviewed"):
            submit_review(cycle, "reviewer1", ReviewAction.APPROVE)

    def test_rejection(self) -> None:
        cycle = create_review_cycle("chg1", "author1", ImpactLevel.NEEDS_REVIEW)
        cycle = submit_review(cycle, "reviewer1", ReviewAction.REJECT, "Not good")
        assert cycle.is_rejected
        assert not cycle.is_approved
        assert cycle.status == ReviewStatus.REJECTED

    def test_request_changes(self) -> None:
        cycle = create_review_cycle("chg1", "author1", ImpactLevel.NEEDS_REVIEW)
        cycle = submit_review(cycle, "reviewer1", ReviewAction.REQUEST_CHANGES, "Fix X")
        assert cycle.status == ReviewStatus.CHANGES_REQUESTED
        assert not cycle.is_approved

    def test_cannot_review_after_approval(self) -> None:
        cycle = create_review_cycle("chg1", "author1", ImpactLevel.NEEDS_REVIEW)
        cycle = submit_review(cycle, "reviewer1", ReviewAction.APPROVE)
        with pytest.raises(ReviewError, match="already"):
            submit_review(cycle, "reviewer2", ReviewAction.APPROVE)

    def test_cannot_review_after_rejection(self) -> None:
        cycle = create_review_cycle("chg1", "author1", ImpactLevel.NEEDS_REVIEW)
        cycle = submit_review(cycle, "reviewer1", ReviewAction.REJECT)
        with pytest.raises(ReviewError, match="already"):
            submit_review(cycle, "reviewer2", ReviewAction.APPROVE)
