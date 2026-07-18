"""Cross-language golden-vector tests for canonical JSON + SHA-256.

The fixture file ``canonical_vectors.json`` is the single source of truth for
the expected output. Kotlin and TypeScript implementations load the same file
and assert identical results. Any change here MUST be accompanied by a matching
change in the other two languages.
"""
from __future__ import annotations

import json
from pathlib import Path

from wb_contracts.canonical import canonical_json, sha256_hex

VECTORS = Path(__file__).parent / "golden" / "canonical_vectors.json"


def test_golden_vectors():
    with open(VECTORS, encoding="utf-8") as f:
        vectors = json.load(f)

    for v in vectors:
        name = v["name"]
        assert canonical_json(v["input"]) == v["expected_canonical_json"], (
            f"vector '{name}': canonical JSON mismatch"
        )
        assert sha256_hex(v["input"]) == v["expected_sha256"], (
            f"vector '{name}': SHA-256 mismatch"
        )


def test_golden_vector_count():
    """Guard against accidental deletion of vectors."""
    with open(VECTORS, encoding="utf-8") as f:
        vectors = json.load(f)
    assert len(vectors) >= 10, f"expected >= 10 golden vectors, got {len(vectors)}"
