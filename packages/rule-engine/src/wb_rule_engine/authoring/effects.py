"""Effect vocabulary for the authoring rule language (contracts/rule.schema.json)."""
from __future__ import annotations

from typing import Any, Mapping

EFFECT_TYPES = frozenset(
    {
        "include_step",
        "exclude_step",
        "include_requirement",
        "set_requirement_obligation",
        "set_deadline",
        "attach_channel",
        "emit_warning",
        "emit_advice",
        "block",
        "require_confirmation",
        "override_rule",
        "trigger_child_event",
        "set_freshness_state",
    }
)


def effect_tag(effect: Mapping[str, Any], rule: Mapping[str, Any]) -> str:
    """Stable short tag used to group advice / warnings / confirmations.

    Prefers an explicit ``tag`` on the effect; otherwise falls back to the last
    dotted segment of the rule's canonical_rule_id
    (e.g. ``change_water_holder.death_path`` -> ``death_path``).
    """
    tag = effect.get("tag")
    if tag:
        return tag
    canonical = rule.get("canonical_rule_id") or rule.get("id") or ""
    return canonical.rsplit(".", 1)[-1] if canonical else ""
