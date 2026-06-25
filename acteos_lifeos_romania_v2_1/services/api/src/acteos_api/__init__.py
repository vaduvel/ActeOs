"""ActeOS API service (FastAPI modular monolith).

P1 discovery slice: serves only published intents and wires the deterministic
Intent Resolver. Domain stays decoupled from adapters; the rule engine and the
intent resolver are pure packages tested independently.
"""
from __future__ import annotations

__all__ = ["create_app"]

from .main import create_app
