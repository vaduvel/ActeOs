"""Immutable content-addressed snapshot store.

Each snapshot is identified by the SHA-256 hash of its content.
Once created, snapshots cannot be modified or deleted — only
the production pointer moves between snapshots.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import UTC, datetime

from wb_ingestion.errors import IngestionProblemCode, SnapshotError


@dataclass(frozen=True)
class Snapshot:
    """An immutable content snapshot."""

    snapshot_id: str  # sha256 hex of content
    source_id: str
    url: str
    content: bytes
    content_type: str
    normalized_text: str | None
    captured_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    content_length: int = 0
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.content_length == 0:
            object.__setattr__(self, "content_length", len(self.content))


def compute_snapshot_id(content: bytes) -> str:
    """Content-addressed ID: SHA-256 hex of the raw content."""
    return hashlib.sha256(content).hexdigest()


class SnapshotStore:
    """In-memory immutable snapshot store.

    In production this would be backed by PostgreSQL + object storage.
    The interface is identical: store, get, list, but never update/delete.
    """

    def __init__(self) -> None:
        self._snapshots: dict[str, Snapshot] = {}
        self._by_source: dict[str, list[str]] = {}  # source_id → [snapshot_ids]

    def store(
        self,
        source_id: str,
        url: str,
        content: bytes,
        content_type: str,
        *,
        normalized_text: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> Snapshot:
        """Store a new snapshot. If content already exists, returns existing."""
        snap_id = compute_snapshot_id(content)

        existing = self._snapshots.get(snap_id)
        if existing is not None:
            return existing

        snapshot = Snapshot(
            snapshot_id=snap_id,
            source_id=source_id,
            url=url,
            content=content,
            content_type=content_type,
            normalized_text=normalized_text,
            metadata=metadata or {},
        )
        self._snapshots[snap_id] = snapshot
        self._by_source.setdefault(source_id, []).append(snap_id)
        return snapshot

    def get(self, snapshot_id: str) -> Snapshot:
        """Get snapshot by ID. Raises if not found."""
        try:
            return self._snapshots[snapshot_id]
        except KeyError:
            raise SnapshotError(
                IngestionProblemCode.SNAPSHOT_NOT_FOUND,
                f"Snapshot not found: {snapshot_id}",
            ) from None

    def exists(self, snapshot_id: str) -> bool:
        return snapshot_id in self._snapshots

    def list_for_source(self, source_id: str) -> list[Snapshot]:
        """List all snapshots for a source, oldest first."""
        ids = self._by_source.get(source_id, [])
        return [self._snapshots[sid] for sid in ids]

    def latest_for_source(self, source_id: str) -> Snapshot | None:
        """Get the most recent snapshot for a source, or None."""
        ids = self._by_source.get(source_id, [])
        if not ids:
            return None
        return self._snapshots[ids[-1]]

    def count(self) -> int:
        return len(self._snapshots)

    def count_for_source(self, source_id: str) -> int:
        return len(self._by_source.get(source_id, []))
