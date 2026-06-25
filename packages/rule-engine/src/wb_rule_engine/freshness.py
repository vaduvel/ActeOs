from __future__ import annotations

from datetime import datetime

from .dates import parse_datetime


def freshness_state(freshness: dict, now: datetime) -> str:
    hard = parse_datetime(freshness.get("hard_expiry_at"))
    review = parse_datetime(freshness.get("review_due_at"))
    if hard is not None and now >= hard:
        return "expired"
    if review is not None and now >= review:
        return "review_due"
    return "fresh"


def on_expiry_effect(freshness: dict) -> str:
    return freshness.get("on_expiry", "warn")
