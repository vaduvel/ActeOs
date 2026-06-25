"""Canonical JSON serialization and hashing.

This is the cross-language reference. Any other language (Kotlin, TypeScript)
MUST produce byte-identical canonical JSON to keep golden hashes stable:

- UTF-8 encoding.
- Object keys sorted lexicographically by Unicode code point.
- No insignificant whitespace: item separator ',', key separator ':'.
- Non-ASCII characters are emitted literally, not ASCII-escaped.
- Arrays preserve their given order; callers must pre-sort sets by id.
- Floats are avoided; use integers or decimal strings for money.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
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
