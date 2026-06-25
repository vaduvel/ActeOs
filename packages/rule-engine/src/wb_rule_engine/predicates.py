"""Typed predicate evaluation with three-valued logic.

Mirrors the predicate shapes in contracts/rule.schema.json. No dynamic code
execution: operators are matched explicitly.
"""
from __future__ import annotations

from typing import Any, Mapping

from .d