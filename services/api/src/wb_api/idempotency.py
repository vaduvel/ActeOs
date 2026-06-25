"""Request-fingerprinted idempotency.

begin(key, request_payload) returns one of:
  - ('new', None)         first time this key is seen; caller should process.
  - ('in_progress', None) key seen, same request, not yet completed.
  - ('replay', response)  key already completed; return the stored response.
and raises ConflictError if the same key is reused with a different request.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from .canonical import sha256_hex


class ConflictError(Exception):
    pass


def request_fingerprint(payload: Any) -> str:
    return sha256_hex(payload)


@dataclass
class IdempotencyRecord:
    key: str
    request_hash: str
    status: str  # 'in_progress' | 'completed'
    response: Optional[Any] = None


class IdempotencyStore:
    """In-memory reference implementation; the DB model mirrors these fields."""

    def __init__(self) -> None:
        self._records: dict[str, IdempotencyRecord] = {}

    def begin(self, key: str, request_payload: Any) -> tuple[str, Optional[Any]]:
        request_hash = request_fingerprint(request_payload)
        record = self._records.get(key)
        if record is None:
            self._records[key] = IdempotencyRecord(key, request_hash, "in_progress")
            return ("new", None)
        if record.request_hash != request_hash:
            raise ConflictError(f"idempotency key '{key}' reused with a different request body")
        if record.status == "completed":
            return ("replay", record.response)
        return ("in_progress", None)

    def complete(self, key: str, response: Any) -> IdempotencyRecord:
        record = self._records.get(key)
        if record is None:
            raise KeyError(key)
        record.status = "completed"
        record.response = response
        return record
