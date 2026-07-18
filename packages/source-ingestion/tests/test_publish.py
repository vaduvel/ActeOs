"""Tests for atomic publishing and rollback."""

from __future__ import annotations

import pytest

from wb_ingestion.errors import PublishError
from wb_ingestion.publish import ProductionPointer
from wb_ingestion.snapshot import SnapshotStore


@pytest.fixture()
def store() -> SnapshotStore:
    s = SnapshotStore()
    s.store("src1", "https://a.com", b"version 1", "text/html")
    s.store("src1", "https://a.com", b"version 2", "text/html")
    s.store("src1", "https://a.com", b"version 3", "text/html")
    return s


@pytest.fixture()
def pointer(store: SnapshotStore) -> ProductionPointer:
    return ProductionPointer(store)


class TestPublish:
    def test_publish_first_snapshot(self, pointer: ProductionPointer, store: SnapshotStore) -> None:
        snap = store.latest_for_source("src1")
        assert snap is not None
        record = pointer.publish("src1", snap.snapshot_id, "admin1")
        assert record.action == "publish"
        assert record.from_snapshot_id is None
        assert pointer.current_snapshot("src1") == snap.snapshot_id

    def test_publish_nonexistent_snapshot_raises(self, pointer: ProductionPointer) -> None:
        with pytest.raises(PublishError, match="not found"):
            pointer.publish("src1", "nonexistent_snap", "admin1")

    def test_publish_updates_pointer(self, pointer: ProductionPointer, store: SnapshotStore) -> None:
        snaps = store.list_for_source("src1")
        pointer.publish("src1", snaps[0].snapshot_id, "admin1")
        assert pointer.current_snapshot("src1") == snaps[0].snapshot_id

        pointer.publish("src1", snaps[1].snapshot_id, "admin1")
        assert pointer.current_snapshot("src1") == snaps[1].snapshot_id

    def test_publish_records_history(self, pointer: ProductionPointer, store: SnapshotStore) -> None:
        snaps = store.list_for_source("src1")
        pointer.publish("src1", snaps[0].snapshot_id, "admin1")
        pointer.publish("src1", snaps[1].snapshot_id, "admin2")

        history = pointer.history("src1")
        assert len(history) == 2
        assert history[0].published_by == "admin1"
        assert history[1].published_by == "admin2"


class TestRollback:
    def test_rollback_restores_previous(self, pointer: ProductionPointer, store: SnapshotStore) -> None:
        snaps = store.list_for_source("src1")
        pointer.publish("src1", snaps[0].snapshot_id, "admin1")
        pointer.publish("src1", snaps[1].snapshot_id, "admin1")
        assert pointer.current_snapshot("src1") == snaps[1].snapshot_id

        record = pointer.rollback("src1", "admin2", reason="Bad content")
        assert record.action == "rollback"
        assert pointer.current_snapshot("src1") == snaps[0].snapshot_id

    def test_rollback_without_previous_raises(self, pointer: ProductionPointer) -> None:
        with pytest.raises(PublishError, match="no production pointer"):
            pointer.rollback("src1", "admin1")

    def test_rollback_at_first_publish_raises(self, pointer: ProductionPointer, store: SnapshotStore) -> None:
        snaps = store.list_for_source("src1")
        pointer.publish("src1", snaps[0].snapshot_id, "admin1")
        with pytest.raises(PublishError, match="no previous snapshot"):
            pointer.rollback("src1", "admin1")

    def test_rollback_history_preserved(self, pointer: ProductionPointer, store: SnapshotStore) -> None:
        snaps = store.list_for_source("src1")
        pointer.publish("src1", snaps[0].snapshot_id, "admin1")
        pointer.publish("src1", snaps[1].snapshot_id, "admin1")
        pointer.rollback("src1", "admin2")

        history = pointer.history("src1")
        assert len(history) == 3
        assert history[2].action == "rollback"

    def test_history_not_deleted_on_rollback(self, pointer: ProductionPointer, store: SnapshotStore) -> None:
        """Rollback moves the pointer but never deletes snapshot data."""
        snaps = store.list_for_source("src1")
        pointer.publish("src1", snaps[0].snapshot_id, "admin1")
        pointer.publish("src1", snaps[1].snapshot_id, "admin1")
        pointer.rollback("src1", "admin1")

        # All snapshots still exist
        assert store.count() == 3
        for snap in snaps:
            assert store.exists(snap.snapshot_id)
