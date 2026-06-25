"""Thin JSON Schema validation utility.

The canonical schemas live in the execution pack (contracts/*.json). Point
WB_SCHEMA_DIR at that folder, or pass an explicit schema_dir.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .errors import ProblemCode, WbError

SCHEMA_DIR = Path(os.environ.get("WB_SCHEMA_DIR", "contracts"))


def load_schema(name: str, schema_dir: Path | None = None) -> dict:
    base = schema_dir or SCHEMA_DIR
    path = base / name
    if not path.exists():
        raise WbError(f"schema not found: {path}", ProblemCode.NOT_CONFIGURED)
    return json.loads(path.read_text(encoding="utf-8"))


def validate(instance: Any, schema: dict) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        joined = "; ".join(f"{list(e.path)}: {e.message}" for e in errors)
        raise WbError(joined, ProblemCode.VALIDATION_FAILED)
