"""Atomic publishing and rollback.

The production pointer determines which snapshot is live.
Publishing moves the pointer to a new snapshot. Rollback moves
it back. History is never deleted — only the pointer moves.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from wb_ingestion.errors import IngestionProblemCode, PublishError
from wb_ingestion.snapshot import SnapshotStore


@dataclass(frozen=True)
class PublishRecord:
    """Record of a publish or rollback operation."""

    action: str  # "publish" or "rollback"
    source_id: str
    from_snapshot_id: str | None
    to_snapshot_id: str
    published_by: str
    published_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    review_cycle_id: str | None = None
    reason: str = ""


class ProductionPointer:
    """Manages the production pointer for each source.

    The pointer is the single source of truth for which snapshot
    is currently live. Publishing and rollback are atomic operations
    that move the pointer and record the transition.
    """

    def __init__(self, store: SnapshotStore) -> None:
        self._store = store
        self._pointers: dict[str, str] = {}  # source_id → snapshot_id
        self._history: list[PublishRecord] = []

    def current_snapshot(self, source_id: str) -> str | None:
        """Get the current production snapshot ID for a source."""
        return self._pointers.get(source_id)

    def publish(
        self,
        source_id: str,
        snapshot_id: str,
        published_by: str,
        *,
        review_cycle_id: str | None = None,
        reason: str = "",
    ) -> PublishRecord:
        """Publish a snapshot to production (move pointer).

        Raises PublishError if the snapshot doesn't exist.
        """
        if not self._store.exists(snapshot_id):
            raise PublishError(
                IngestionProblemCode.SNAPSHOT_NOT_FOUND,
                f"Cannot publish: snapshot {snapshot_id} not found",
            )

        from_snapshot = self._pointers.get(source_id)

        record = PublishRecord(
            action="publish",
            source_id=source_id,
            from_snapshot_id=from_snapshot,
            to_snapshot_id=snapshot_id,
            published_by=published_by,
            review_cycle_id=review_cycle_id,
            reason=reason,
        )

        # Atomic: move pointer + record history
        self._pointers[source_id] = snapshot_id
        self._history.append(record)
        return record

    def rollback(
        self,
        source_id: str,
        rolled_back_by: str,
        *,
        reason: str = "",
    ) -> PublishRecord:
        """Rollback to the previous production snapshot.

        Finds the last publish record for this source and restores
        the previous snapshot. Raises if no previous snapshot exists.
        """
        current = self._pointers.get(source_id)
        if current is None:
            raise PublishError(
                IngestionProblemCode.ROLLBACK_FAILED,
                f"Cannot rollback: no production pointer for {source_id}",
            )

        # Find the last publish record for this source
        previous: str | None = None
        for record in reversed(self._history):
            if record.source_id == source_id and record.action == "publish":
                if record.to_snapshot_id == current:
                    previous = record.from_snapshot_id
                    break

        if previous is None:
            raise PublishError(
                IngestionProblemCode.ROLLBACK_FAILED,
                f"Cannot rollback: no previous snapshot for {source_id}",
            )

        record = PublishRecord(
            action="rollback",
            source_id=source_id,
            from_snapshot_id=current,
            to_snapshot_id=previous,
            published_by=rolled_back_by,
            reason=reason,
        )

        # Atomic: move pointer + record history
        self._pointers[source_id] = previous
        self._history.append(record)
        return record

    def history(self, source_id: str | None = None) -> list[PublishRecord]:
        """Get publish history, optionally filtered by source."""
        if source_id is None:
            return list(self._history)
        return [r for r in self._history if r.source_id == source_id]

    def all_pointers(self) -> dict[str, str]:
        """Get all current production pointers."""
        return dict(self._pointers)
