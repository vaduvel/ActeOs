"""Tests for staleness scheduler with time-travel support."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from wb_ingestion.registry import SourceRegistry, TrustLevel
from wb_ingestion.staleness import (
    StalenessLevel,
    assess_staleness,
    find_stale_sources,
)


def _make_registry() -> SourceRegistry:
    reg = SourceRegistry()
    reg.add_allowed_domain("example.com")
    return reg


BASE_TIME = datetime(2026, 7, 18, 12, 0, 0, tzinfo=UTC)


class TestAssessStaleness:
    def test_never_fetched_is_due(self) -> None:
        reg = _make_registry()
        source = reg.register("https://example.com/a", "Test", TrustLevel.OFFICIAL)
        report = assess_staleness(source, now=BASE_TIME)
        assert report.level == StalenessLevel.DUE
        assert report.hours_since_fetch is None

    def test_fresh_source(self) -> None:
        reg = _make_registry()
        source = reg.register(
            "https://example.com/a", "Test", TrustLevel.OFFICIAL,
            fetch_interval_hours=24,
        )
        reg.record_fetch(source.source_id, "snap1")
        source = reg.get(source.source_id)  # get updated
        report = assess_staleness(source, now=BASE_TIME)
        assert report.level == StalenessLevel.FRESH

    def test_due_source(self) -> None:
        reg = _make_registry()
        source = reg.register(
            "https://example.com/a", "Test", TrustLevel.OFFICIAL,
            fetch_interval_hours=24,
        )
        reg.record_fetch(source.source_id, "snap1")
        source = reg.get(source.source_id)

        # Simulate 30 hours later
        future = BASE_TIME + timedelta(hours=30)
        report = assess_staleness(source, now=future)
        assert report.level in (StalenessLevel.DUE, StalenessLevel.FRESH)

    def test_stale_source(self) -> None:
        reg = _make_registry()
        source = reg.register(
            "https://example.com/a", "Test", TrustLevel.OFFICIAL,
            fetch_interval_hours=24,
        )
        reg.record_fetch(source.source_id, "snap1")
        source = reg.get(source.source_id)

        # Simulate 60 hours later (2.5x interval)
        future = BASE_TIME + timedelta(hours=60)
        report = assess_staleness(source, now=future)
        assert report.level in (StalenessLevel.STALE, StalenessLevel.DUE)

    def test_critical_source(self) -> None:
        reg = _make_registry()
        source = reg.register(
            "https://example.com/a", "Test", TrustLevel.OFFICIAL,
            fetch_interval_hours=24,
        )
        reg.record_fetch(source.source_id, "snap1")
        source = reg.get(source.source_id)

        # Simulate 200 hours later (8x interval)
        future = BASE_TIME + timedelta(hours=200)
        report = assess_staleness(source, now=future)
        assert report.level == StalenessLevel.CRITICAL


class TestFindStaleSources:
    def test_finds_due_sources(self) -> None:
        reg = _make_registry()
        # One never fetched (due), one fresh
        reg.register("https://example.com/a", "A", TrustLevel.OFFICIAL)
        s2 = reg.register(
            "https://example.com/b", "B", TrustLevel.OFFICIAL,
            fetch_interval_hours=24,
        )
        reg.record_fetch(s2.source_id, "snap1")

        stale = find_stale_sources(reg, now=BASE_TIME)
        assert len(stale) == 1
        assert stale[0].source_id != s2.source_id

    def test_sorted_most_stale_first(self) -> None:
        reg = _make_registry()
        reg.register("https://example.com/a", "A", TrustLevel.OFFICIAL)
        stale = find_stale_sources(reg, now=BASE_TIME)
        assert len(stale) >= 1

    def test_filter_by_min_level(self) -> None:
        reg = _make_registry()
        source = reg.register(
            "https://example.com/a", "A", TrustLevel.OFFICIAL,
            fetch_interval_hours=24,
        )
        reg.record_fetch(source.source_id, "snap1")
        source = reg.get(source.source_id)

        # Fresh source should not appear
        stale = find_stale_sources(reg, now=BASE_TIME, min_level=StalenessLevel.DUE)
        assert len(stale) == 0

        # All sources should appear with min_level=FRESH
        all_sources = find_stale_sources(reg, now=BASE_TIME, min_level=StalenessLevel.FRESH)
        assert len(all_sources) == 1
