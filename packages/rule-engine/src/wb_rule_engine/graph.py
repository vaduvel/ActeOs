from __future__ import annotations

from .errors import DependencyCycle


def stable_topo_sort(steps: list[dict]) -> list[dict]:
    """Deterministic Kahn topological sort.

    Ready nodes are always taken in (sequence_hint, id) order so two runs never
    reorder arbitrarily. Raises DependencyCycle if a cycle remains.
    """
    by_id = {s["id"]: s for s in steps}
    indeg = {s["id"]: 0 for s in steps}
    adj: dict[str, list[str]] = {s["id"]: [] for s in steps}
    for s in steps:
        for dep in s.get("depends_on", []):
            if dep in by_id:
                adj[dep].append(s["id"])
                indeg[s["id"]] += 1

    def sort_key(sid: str) -> tuple[int, str]:
        s = by_id[sid]
        return (int(s.get("sequence_hint", 0)), sid)

    ready = sorted([sid for sid, d in indeg.items() if d == 0], key=sort_key)
    order: list[str] = []
    while ready:
        sid = ready.pop(0)
        order.append(sid)
        for nxt in adj[sid]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                ready.append(nxt)
        ready.sort(key=sort_key)
    if len(order) != len(steps):
        remaining = sorted(sid for sid in by_id if sid not in order)
        raise DependencyCycle(f"dependency cycle among: {remaining}")
    return [by_id[sid] for sid in order]
