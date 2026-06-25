"""ActeOS deterministic rule engine (pure, no IO/clock/LLM at evaluation time).

The authoring evaluator lives in :mod:`acteos_rule_engine.authoring`. This module
is intentionally thin so importing the top-level package pulls in no third-party
dependency. The compiled runtime contract version is exposed as ENGINE_VERSION,
aligned with docs/05_RULE_ENGINE_SPEC.md.
"""
from __future__ import annotations

ENGINE_VERSION = "2.1.0"

__all__ = ["ENGINE_VERSION"]
