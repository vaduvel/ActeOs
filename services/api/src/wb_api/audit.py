"""Append-only, hash-chained audit log.

Two hash chains live here, intentionally:

1. ``AuditChain`` / ``compute_entry_hash`` / ``verify_chain`` — an in-memory
   reference chain used by unit tests and offline verification.
2. ``compute_event_hash`` / ``verify_event_log`` — the canonical chain that
   matches the persisted ``audit.event_log`` columns
   (``previous_event_hash`` -> ``event_hash``). This is what the running service
   writes for every state-changing action.

Every entry commits to the previous entry's hash, so any insertion, deletion,
or mutation invalidates all following hashes and is detected on verification.
The database migration also forbids UPDATE/DELETE on the audit table as defence
in depth, and the payload must never contain raw PII (10_SECURITY_PRIVACY §8).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

from .canonical import sha256_hex

GENESIS_HASH = "sha256:" + "0" * 64


# --- in-memory reference chain (unit-tested) --------------------------------
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


# --- canonical persisted chain (audit.event_log) ----------------------------
def compute_event_hash(
    *,
    previous_event_hash: str,
    occurred_at: str,
    actor_type: str,
    actor_id: str | None,
    action: str,
    entity_type: str,
    entity_id: str,
    correlation_id: str | None,
    payload: Mapping[str, Any],
) -> str:
    """Hash one ``audit.event_log`` row over its immutable, content-bearing
    fields plus the previous row's hash. Field order is irrelevant because the
    canonical serializer sorts keys.
    """
    return sha256_hex({
        "previous_event_hash": previous_event_hash,
        "occurred_at": occurred_at,
        "actor_type": actor_type,
        "actor_id": actor_id,
        "action": action,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "correlation_id": correlation_id,
        "payload": payload,
    })


def _iso(value: Any) -> str:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat()
    return str(value)


def verify_event_log(rows: Sequence[Mapping[str, Any]]) -> bool:
    """Verify a sequence of ``audit.event_log`` rows ordered by ascending id.

    Each row must expose ``occurred_at``, ``actor_type``, ``actor_id``,
    ``action``, ``entity_type``, ``entity_id``, ``correlation_id``, ``payload``,
    ``previous_event_hash`` and ``event_hash``.
    """
    prev = GENESIS_HASH
    for row in rows:
        if row.get("previous_event_hash") not in (prev, None) and prev != GENESIS_HASH:
            return False
        stored_prev = row.get("previous_event_hash") or GENESIS_HASH
        if stored_prev != prev:
            return False
        expected = compute_event_hash(
            previous_event_hash=prev,
            occurred_at=_iso(row["occurred_at"]),
            actor_type=row["actor_type"],
            actor_id=row.get("actor_id"),
            action=row["action"],
            entity_type=row["entity_type"],
            entity_id=row["entity_id"],
            correlation_id=row.get("correlation_id"),
            payload=row.get("payload") or {},
        )
        if expected != row.get("event_hash"):
            return False
        prev = row["event_hash"]
    return True
