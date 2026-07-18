"""Snapshot diff and severity classification.

Compares normalized text of two snapshots and classifies
the severity of changes: cosmetic, moderate, or critical.
"""

from __future__ import annotations

import difflib
from dataclasses import dataclass
from enum import Enum


class ChangeSeverity(str, Enum):
    """How significant a content change is."""

    NONE = "none"                # identical
    COSMETIC = "cosmetic"        # whitespace, formatting, minor rewording
    MODERATE = "moderate"        # content changed, meaning likely similar
    CRITICAL = "critical"        # substantive change (numbers, dates, requirements)


@dataclass(frozen=True)
class DiffResult:
    """Result of comparing two snapshots."""

    old_snapshot_id: str
    new_snapshot_id: str
    severity: ChangeSeverity
    similarity_ratio: float  # 0.0 to 1.0
    added_lines: int
    removed_lines: int
    changed_lines: int
    unified_diff: str


# Patterns that indicate critical changes
_CRITICAL_PATTERNS = [
    # Numbers that could be fees, deadlines, thresholds
    "lei", "RON", "EUR", "%",
    # Temporal markers
    "termen", "deadline", "valabil", "expiră", "valabilitate",
    # Legal markers
    "art.", "alin.", "lege", "OG", "HG", "ordin", "hotărâre",
    # Requirements
    "obligatoriu", "obligatorie", "trebuie", "necesar", "necesară",
]


def compute_diff(
    old_snapshot_id: str,
    old_text: str,
    new_snapshot_id: str,
    new_text: str,
) -> DiffResult:
    """Compute diff between two normalized text snapshots.

    Returns a DiffResult with severity classification.
    """
    if old_text == new_text:
        return DiffResult(
            old_snapshot_id=old_snapshot_id,
            new_snapshot_id=new_snapshot_id,
            severity=ChangeSeverity.NONE,
            similarity_ratio=1.0,
            added_lines=0,
            removed_lines=0,
            changed_lines=0,
            unified_diff="",
        )

    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)

    # Similarity ratio
    matcher = difflib.SequenceMatcher(None, old_text, new_text)
    ratio = matcher.ratio()

    # Unified diff
    diff_lines = list(difflib.unified_diff(
        old_lines, new_lines,
        fromfile=f"snapshot:{old_snapshot_id[:12]}",
        tofile=f"snapshot:{new_snapshot_id[:12]}",
        lineterm="",
    ))
    unified = "\n".join(diff_lines)

    # Count changes
    added = sum(1 for l in diff_lines if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in diff_lines if l.startswith("-") and not l.startswith("---"))
    changed = min(added, removed)

    # Classify severity
    severity = _classify_severity(ratio, unified, added, removed)

    return DiffResult(
        old_snapshot_id=old_snapshot_id,
        new_snapshot_id=new_snapshot_id,
        severity=severity,
        similarity_ratio=ratio,
        added_lines=added,
        removed_lines=removed,
        changed_lines=changed,
        unified_diff=unified,
    )


def _classify_severity(
    ratio: float,
    diff_text: str,
    added: int,
    removed: int,
) -> ChangeSeverity:
    """Classify change severity based on similarity and content patterns."""
    # Very high similarity = cosmetic
    if ratio >= 0.98:
        return ChangeSeverity.COSMETIC

    # Check for critical patterns in the diff
    diff_lower = diff_text.lower()
    for pattern in _CRITICAL_PATTERNS:
        if pattern.lower() in diff_lower:
            # Critical pattern found in changed lines
            if ratio < 0.95:
                return ChangeSeverity.CRITICAL

    # Medium similarity = moderate
    if ratio >= 0.85:
        return ChangeSeverity.MODERATE

    # Low similarity = critical (major content change)
    return ChangeSeverity.CRITICAL
