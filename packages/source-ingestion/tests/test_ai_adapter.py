"""Tests for AI draft extraction adapter."""

from __future__ import annotations

import os

import pytest

from wb_ingestion.ai_adapter import (
    AiExtractionDisabled,
    NoOpExtractor,
    extract_draft,
    get_extractor,
    is_ai_enabled,
)


class TestAiDisabled:
    """Default mode: AI_EXTRACTION_ENABLED is not set or false."""

    def test_ai_disabled_by_default(self) -> None:
        # Ensure env var is not set
        os.environ.pop("AI_EXTRACTION_ENABLED", None)
        assert not is_ai_enabled()

    def test_ai_disabled_false(self) -> None:
        os.environ["AI_EXTRACTION_ENABLED"] = "false"
        assert not is_ai_enabled()
        os.environ.pop("AI_EXTRACTION_ENABLED", None)

    def test_extract_draft_raises_when_disabled(self) -> None:
        os.environ.pop("AI_EXTRACTION_ENABLED", None)
        with pytest.raises(AiExtractionDisabled):
            extract_draft("snap1", "some text", "https://example.com")

    def test_noop_extractor_returns_empty(self) -> None:
        extractor = NoOpExtractor()
        assert extractor.extract_claims("text", "url") == []
        assert extractor.extract_rules("text", []) == []

    def test_get_extractor_disabled(self) -> None:
        os.environ.pop("AI_EXTRACTION_ENABLED", None)
        extractor = get_extractor()
        assert isinstance(extractor, NoOpExtractor)


class TestAiEnabled:
    """When AI_EXTRACTION_ENABLED=true."""

    def test_ai_enabled(self) -> None:
        os.environ["AI_EXTRACTION_ENABLED"] = "true"
        assert is_ai_enabled()
        os.environ.pop("AI_EXTRACTION_ENABLED", None)

    def test_extract_draft_returns_result(self) -> None:
        os.environ["AI_EXTRACTION_ENABLED"] = "true"
        result = extract_draft("snap1", "some normalized text", "https://example.com")
        # With NoOp extractor, returns empty but valid result
        assert result.snapshot_id == "snap1"
        assert isinstance(result.draft_claims, list)
        assert isinstance(result.draft_rules, list)
        os.environ.pop("AI_EXTRACTION_ENABLED", None)

    def test_drafts_require_human_review(self) -> None:
        os.environ["AI_EXTRACTION_ENABLED"] = "true"
        result = extract_draft("snap1", "text", "https://example.com")
        for claim in result.draft_claims:
            assert claim.requires_human_review is True
        for rule in result.draft_rules:
            assert rule.requires_human_review is True
        os.environ.pop("AI_EXTRACTION_ENABLED", None)

    def test_ai_cannot_self_publish(self) -> None:
        """AI output is always draft — there is no 'publish' method on drafts."""
        from wb_ingestion.ai_adapter import DraftClaim

        claim = DraftClaim(
            text="Test claim",
            evidence_excerpt="excerpt",
            source_url="https://example.com",
        )
        assert claim.confidence == "draft"
        assert claim.requires_human_review is True
        # There is no publish() or activate() method
        assert not hasattr(claim, "publish")
        assert not hasattr(claim, "activate")
