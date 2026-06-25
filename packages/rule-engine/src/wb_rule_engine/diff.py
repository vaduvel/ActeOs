from __future__ import annotations


def route_diff(old: dict, new: dict) -> dict:
    """Compare two resolved routes for impact analysis."""
    old_steps = {s["id"]: s for s in old.get("steps", [])}
    new_steps = {s["id"]: s for s in new.get("steps", [])}
    added = sorted(set(new_steps) - set(old_steps))
    removed = sorted(set(old_steps) - set(new_steps))
    changed = sorted(
        sid for sid in set(old_steps) & set(new_steps)
        if old_steps[sid] != new_steps[sid]
    )
    return {
        "route_hash_changed": old.get("route_hash") != new.get("route_hash"),
        "confidence_changed": old.get("confidence") != new.get("confidence"),
        "steps_added": added,
        "steps_removed": removed,
        "steps_changed": changed,
        "conflicts_delta": len(new.get("conflicts", [])) - len(old.get("conflicts", [])),
    }
