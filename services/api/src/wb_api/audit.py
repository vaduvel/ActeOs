"""Append-only, hash-chained audit log.

Each event hashes (prev_hash, seq, actor, action, payload, created_at) with the
canonical serializer. Because every entry commits to the previous entry hash,
any insertion, deletion, or mutation in the middle of the chain invalidates all
following hashes and is detected by verify_chain. The database migration also
forbids UPDATE/DELETE on the audit table as defence in depth.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .canonical import sha256_hex

GENESIS_HASH = "sha256:" + "0" * 64


def compute_entry_hash(
    prev_hash: str, seq: int, actor: str, action: str, payload: Any, created_at: str
) -> str:
    return sha256_hex({
        "prev_hash": prev_hash,
        "seq": seq,
        "actor": actor,
        "action": action,
        "payload": payload,
        "created_at": created_at,
    })


class AuditChain:
    def __init__(self) -> None:
        self._entries: list[dict] = []

    @property
    def head(self) -> str:
        return self._entries[-1]["entry_hash"] if self._entries else GENESIS_HASH

    @property
    def entries(self) -> list[dict]:
        return list(self._entries)

    def append(self, actor: str, action: str, payload: Any, *, created_at: datetime | None = None) -> dict:
        ts = (created_at or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
        seq = len(self._entries) + 1
        prev = self.head
        entry_hash = compute_entry_hash(prev, seq, actor, action, payload, ts)
        entry = {
            "seq": seq,
            "prev_hash": prev,
            "entry_hash": entry_hash,
            "actor": actor,
            "action": action,
            "payload": payload,
            "created_at": ts,
        }
        self._entries.append(entry)
        return entry


def verify_chain(entries: list[dict]) -> bool:
    prev = GENESIS_HASH
    for index, entry in enumerate(entries, start=1):
        if entry.get("seq") != index:
            return False
        if entry.get("prev_hash") != prev:
            return False
        expected = compute_entry_hash(
            prev, entry["seq"], entry["actor"], entry["action"], entry["payload"], entry["created_at"]
        )
        if expected != entry.get("entry_hash"):
            return False
        prev = entry["entry_hash"]
    return True
