"""Tests for snapshot diff and severity classification."""

from __future__ import annotations

from pathlib import Path

from wb_ingestion.diff import ChangeSeverity, compute_diff
from wb_ingestion.normalize import normalize_html

FIXTURES = Path(__file__).parent / "fixtures"


class TestComputeDiff:
    def test_identical_text(self) -> None:
        result = compute_diff("s1", "same text", "s2", "same text")
        assert result.severity == ChangeSeverity.NONE
        assert result.similarity_ratio == 1.0
        assert result.added_lines == 0
        assert result.removed_lines == 0

    def test_cosmetic_change(self) -> None:
        old = normalize_html((FIXTURES / "sample_page.html").read_text())
        new = normalize_html((FIXTURES / "sample_cosmetic_change.html").read_text())
        result = compute_diff("s1", old, "s2", new)
        # Cosmetic changes (whitespace, extra spaces) should be low severity
        assert result.severity in (ChangeSeverity.NONE, ChangeSeverity.COSMETIC)

    def test_critical_change(self) -> None:
        old = normalize_html((FIXTURES / "sample_page.html").read_text())
        new = normalize_html((FIXTURES / "sample_page_updated.html").read_text())
        result = compute_diff("s1", old, "s2", new)
        # Price changed (68→89 lei), validity changed (10→5 ani), new requirement added
        assert result.severity == ChangeSeverity.CRITICAL
        assert result.similarity_ratio < 1.0
        assert result.added_lines > 0

    def test_completely_different(self) -> None:
        result = compute_diff("s1", "completely different text A", "s2", "totally unrelated content Z")
        assert result.severity == ChangeSeverity.CRITICAL
        assert result.similarity_ratio < 0.5

    def test_diff_output_contains_changes(self) -> None:
        old = "line one\nline two\nline three"
        new = "line one\nline modified\nline three"
        result = compute_diff("s1", old, "s2", new)
        assert "line modified" in result.unified_diff
        assert "line two" in result.unified_diff

    def test_similarity_ratio_range(self) -> None:
        result = compute_diff("s1", "abcdef", "s2", "abcxyz")
        assert 0.0 <= result.similarity_ratio <= 1.0


class TestChangeSeverity:
    def test_severity_ordering(self) -> None:
        # All severity values are valid enum members
        assert ChangeSeverity.NONE.value == "none"
        assert ChangeSeverity.COSMETIC.value == "cosmetic"
        assert ChangeSeverity.MODERATE.value == "moderate"
        assert ChangeSeverity.CRITICAL.value == "critical"
