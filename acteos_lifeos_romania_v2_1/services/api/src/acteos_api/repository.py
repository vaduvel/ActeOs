"""Case persistence port + in-memory adapter.

The API persists a resolved Case aggregate (the case plus its computed
resolution snapshot). ``CaseRepository`` is the port; ``InMemoryCaseRepository``
is a complete, process-local adapter suitable for single-node serving and tests.
A PostgreSQL-backed adapter (db/0001_init.sql: app.cases + app.journeys) is the
production deployment target and plugs in behind the same port.
"""
from __future__ import annotations

import threading
from typing import Protocol


class CaseRepository(Protocol):
    def save(self, case: dict) -> dict: ...

    def get(self, case_id: str) -> dict | None: ...


class InMemoryCaseRepository:
    """Thread-safe, process-local case store."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._cases: dict[str, dict] = {}

    def save(self, case: dict) -> dict:
        with self._lock:
            self._cases[case["id"]] = dict(case)
        return case

    def get(self, case_id: str) -> dict | None:
        with self._lock:
            stored = self._cases.get(case_id)
            return dict(stored) if stored is not None else None
