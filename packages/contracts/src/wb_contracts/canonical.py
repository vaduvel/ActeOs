"""Canonical JSON serialization and hashing.

This is the cross-language reference. Any other language (Kotlin, TypeScript)
MUST produce byte-identical canonical JSON to keep golden hashes stable:

- UTF-8 encoding.
- Object keys sorted lexicographically by Unicode code point.
- No insignificant whitespace: item separator ',', key separator ':'.
- Non-ASCII characters are emitted literally, not ASCII-escaped.
- Arrays preserve their given order; callers must pre-sort sets by id.
- Floats are prohibited: use integers or decimal strings for money. Passing a
  ``float`` raises ``WbError`` because ``json.dumps`` and ``JSON.stringify``
  format floats differently (e.g. ``1.0`` → ``"1.0"`` in Python vs ``"1"`` in
  JavaScript), which would break cross-language hash stability.
- NaN / Infinity are rejected (``allow_nan=False``).
- Datetime values must be UTC strings ending in ``Z``; callers normalize before
  hashing. Different timezone offsets for the same instant would diverge.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .errors import ProblemCode, WbError


def _reject_floats(value: Any) -> None:
    """Walk *value* and raise if any float is found (including inside containers)."""
    if isinstance(value, float):
        raise WbError(
            f"canonical JSON prohibits float values; "
            f"use int or decimal string instead. Got: {value!r}",
            ProblemCode.VALIDATION_FAILED,
        )
    if isinstance(value, dict):
        for v in value.values():
            _reject_floats(v)
    elif isinstance(value, list):
        for v in value:
            _reject_floats(v)


def canonical_json(value: Any) -> str:
    _reject_floats(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def sha256_hex(value: Any) -> str:
    digest = hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"
