from __future__ import annotations

from enum import Enum


class Tri(Enum):
    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"


def from_bool(value: bool) -> "Tri":
    return Tri.TRUE if value else Tri.FALSE


def tri_not(value: "Tri") -> "Tri":
    if value is Tri.UNKNOWN:
        return Tri.UNKNOWN
    return Tri.FALSE if value is Tri.TRUE else Tri.TRUE


def tri_all(values) -> "Tri":
    result = Tri.TRUE
    for v in values:
        if v is Tri.FALSE:
            return Tri.FALSE
        if v is Tri.UNKNOWN:
            result = Tri.UNKNOWN
    return result


def tri_any(values) -> "Tri":
    result = Tri.FALSE
    for v in values:
        if v is Tri.TRUE:
            return Tri.TRUE
        if v is Tri.UNKNOWN:
            result = Tri.UNKNOWN
    return result
