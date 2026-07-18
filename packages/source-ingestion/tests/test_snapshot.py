"""Tests for the immutable snapshot store."""

from __future__ import annotations

import pytest

from wb_ingestion.errors import SnapshotError
from wb_ingestion.snapshot import SnapshotStore, compute_snapshot_id


@pytest.fixture()
def store() -> SnapshotStore:
    return SnapshotStore()


class TestComputeSnapshotId:
    def test_deterministic(self) -> None:
        assert compute_snapshot_id(b"hello") == compute_snapshot_id(b"hello")

    def test_different_content(self) -> None:
        assert compute_snapshot_id(b"a") != compute_snapshot_id(b"b")

    def test_empty_content(self) -> None:
        sid = compute_snapshot_id(b"")
        assert isinstance(sid, str)
        assert len(sid) == 64  # SHA-256 hex


class TestSnapshotStore:
    def test_store_and_get(self, store: SnapshotStore) -> None:
        snap = store.store(
            source_id="src1",
            url="https://example.com",
            content=b"<html>test</html>",
            content_type="text/html",
        )
        assert snap.snapshot_id == compute_snapshot_id(b"<html>test</html>")
        assert snap.source_id == "src1"
        assert snap.content_length == len(b"<html>test</html>")

        fetched = store.get(snap.snapshot_id)
        assert fetched is snap

    def test_duplicate_content_returns_existing(self, store: SnapshotStore) -> None:
        snap1 = store.store("src1", "https://a.com", b"same content", "text/html")
        snap2 = store.store("src2", "https://b.com", b"same content", "text/html")
        assert snap1.snapshot_id == snap2.snapshot_id
        assert store.count() == 1

    def test_get_not_found(self, store: SnapshotStore) -> None:
        with pytest.raises(SnapshotError, match="not found"):
            store.get("nonexistent")

    def test_exists(self, store: SnapshotStore) -> None:
        snap = store.store("src1", "https://a.com", b"data", "text/html")
        assert store.exists(snap.snapshot_id)
        assert not store.exists("nonexistent")

    def test_list_for_source(self, store: SnapshotStore) -> None:
        store.store("src1", "https://a.com", b"v1", "text/html")
        store.store("src1", "https://a.com", b"v2", "text/html")
        store.store("src2", "https://b.com", b"other", "text/html")

        snaps = store.list_for_source("src1")
        assert len(snaps) == 2
        assert snaps[0].content == b"v1"
        assert snaps[1].content == b"v2"

    def test_latest_for_source(self, store: SnapshotStore) -> None:
        store.store("src1", "https://a.com", b"v1", "text/html")
        store.store("src1", "https://a.com", b"v2", "text/html")
        latest = store.latest_for_source("src1")
        assert latest is not None
        assert latest.content == b"v2"

    def test_latest_for_source_empty(self, store: SnapshotStore) -> None:
        assert store.latest_for_source("nonexistent") is None

    def test_with_normalized_text(self, store: SnapshotStore) -> None:
        snap = store.store(
            "src1", "https://a.com", b"<p>Hello</p>", "text/html",
            normalized_text="Hello",
        )
        assert snap.normalized_text == "Hello"

    def test_with_metadata(self, store: SnapshotStore) -> None:
        snap = store.store(
            "src1", "https://a.com", b"data", "text/html",
            metadata={"etag": "abc123", "last_modified": "2026-01-01"},
        )
        assert snap.metadata["etag"] == "abc123"

    def test_count_for_source(self, store: SnapshotStore) -> None:
        store.store("src1", "https://a.com", b"v1", "text/html")
        store.store("src1", "https://a.com", b"v2", "text/html")
        assert store.count_for_source("src1") == 2
        assert store.count_for_source("src2") == 0
