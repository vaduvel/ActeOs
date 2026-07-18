"""Staleness scheduler.

Determines which sources need re-fetching based on their
fetch_interval_hours and last_fetched_at timestamp.
All functions accept `now` as parameter for time-travel testing.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import Enum

from wb_ingestion.registry import Source, SourceRegistry, SourceStatus


class StalenessLevel(str, Enum):
    """How stale a source is."""

    FRESH = "fresh"              # within fetch interval
    DUE = "due"                  # past fetch interval, needs re-fetch
    STALE = "stale"              # 2x past fetch interval, content may be outdated
    CRITICAL = "critical"        # 4x past fetch interval, content likely outdated


@dataclass(frozen=True)
class StalenessReport:
    """Staleness assessment for a single source."""

    source_id: str
    url: str
    level: StalenessLevel
    hours_since_fetch: float | None  # None if never fetched
    fetch_interval_hours: int
    overdue_by_hours: float | None


def assess_staleness(
    source: Source,
    now: datetime | None = None,
) -> StalenessReport:
    """Assess the staleness of a single source.

    Args:
        source: The source to assess.
        now: Current time (injectable for testing). Defaults to UTC now.

    Returns:
        StalenessReport with level and timing details.
    """
    now = now or datetime.now(UTC)

    if source.last_fetched_at is None:
        return StalenessReport(
            source_id=source.source_id,
            url=source.url,
            level=StalenessLevel.DUE,
            hours_since_fetch=None,
            fetch_interval_hours=source.fetch_interval_hours,
            overdue_by_hours=None,
        )

    elapsed = (now - source.last_fetched_at).total_seconds() / 3600
    interval = source.fetch_interval_hours
    overdue = elapsed - interval

    if elapsed < interval:
        level = StalenessLevel.FRESH
    elif elapsed < interval * 2:
        level = StalenessLevel.DUE
    elif elapsed < interval * 4:
        level = StalenessLevel.STALE
    else:
        level = StalenessLevel.CRITICAL

    return StalenessReport(
        source_id=source.source_id,
        url=source.url,
        level=level,
        hours_since_fetch=round(elapsed, 2),
        fetch_interval_hours=interval,
        overdue_by_hours=round(overdue, 2) if overdue > 0 else None,
    )


def find_stale_sources(
    registry: SourceRegistry,
    now: datetime | None = None,
    *,
    min_level: StalenessLevel = StalenessLevel.DUE,
) -> list[StalenessReport]:
    """Find all sources at or above the given staleness level.

    Args:
        registry: The source registry to scan.
        now: Current time (injectable for testing).
        min_level: Minimum staleness level to include.

    Returns:
        List of StalenessReports, sorted by overdue time (most stale first).
    """
    now = now or datetime.now(UTC)
    level_order = [
        StalenessLevel.FRESH,
        StalenessLevel.DUE,
        StalenessLevel.STALE,
        StalenessLevel.CRITICAL,
    ]
    min_index = level_order.index(min_level)

    reports: list[StalenessReport] = []
    for source in registry.list_active():
        report = assess_staleness(source, now)
        if level_order.index(report.level) >= min_index:
            reports.append(report)

    # Sort: most overdue first (None = never fetched → highest priority)
    reports.sort(
        key=lambda r: (
            r.overdue_by_hours if r.overdue_by_hours is not None else float("inf")
        ),
        reverse=True,
    )
    return reports
