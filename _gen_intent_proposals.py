#!/usr/bin/env python3
"""Generate intent_proposal.yaml for all research events in inbox."""
import os
import yaml

INBOX = "docs/product/lifeos-romania/research/inbox"
TAXONOMY = "acteos_lifeos_romania_v2_1/data/intent_taxonomy.yaml"
LINKS = "acteos_lifeos_romania_v2_1/data/intent_event_links.yaml"

with open(TAXONOMY) as f:
    tx = yaml.safe_load(f)

event_to_intents = {}
for intent in tx.get("intents", []):
    for eid in intent.get("linked_event_ids", []):
        event_to_intents.setdefault(eid, []).append(intent)

if os.path.exists(LINKS):
    with open(LINKS) as f:
        links = yaml.safe_load(f)
    for item in links.get("event_intent_links", []):
        eid = item["event_id"]
        intent_id = item.get("intent_id") or item.get("primary_intent_id")
        if intent_id and eid:
            event_to_intents.setdefault(eid, [])
            if not any(i.get("id") == intent_id for i in event_to_intents[eid]):
                stub = {
                    "id": intent_id,
                    "title_ro": item.get("title_ro", ""),
                    "outcome_ro": item.get("outcome_ro", ""),
                    "category_id": item.get("category_id", ""),
                    "kind": item.get("kind", "direct_goal"),
                    "aliases_ro": item.get("aliases_ro", []),
                    "negative_aliases_ro": item.get("negative_aliases_ro", []),
                }
                event_to_intents[eid].append(stub)


def normalize_event_id(name):
    """Convert dir name to canonical ro.life.<slug>."""
    n = name.replace("B01_", "").replace("B03_", "").replace("R1_", "")
    if not n.startswith("ro.life."):
        n = "ro.life." + n.lower()
    return n


def slug_to_title(slug):
    parts = slug.rsplit(".", 1)[-1].split("_")
    return " ".join(p.capitalize() for p in parts)


def read_event_title(event_dir):
    """Read the descriptive title from event_card.md."""
    card_path = os.path.join(event_dir, "event_card.md")
    if not os.path.exists(card_path):
        return None
    with open(card_path) as f:
        for line in f:
            s = line.strip()
            if s.startswith("# Event Card") and "—" in s:
                return s.split("—", 1)[1].strip()
            if s.startswith("## Declanșator") or s.startswith("## Trigger"):
                break
    # fallback: first non-empty line after title
    with open(card_path) as f:
        for line in f:
            s = line.strip()
            if s.startswith("trigger_ro:"):
                return s.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def generate_proposal(event_id, event_dir):
    proposal_path = os.path.join(event_dir, "intent_proposal.yaml")
    if os.path.exists(proposal_path):
        return 0  # already exists

    intents = event_to_intents.get(event_id, [])
    event_title = read_event_title(event_dir) or slug_to_title(event_id)

    proposals = []
    def _make_title(s):
        s = s.strip()
        if s.lower().startswith("vreau să") or s.lower().startswith("vreau sa"):
            return s
        return f"Vreau să {s[0].lower() + s[1:]}"

    if intents:
        for intent in intents:
            proposals.append({
                "id": intent["id"],
                "title_ro": intent.get("title_ro", _make_title(event_title)),
                "outcome_ro": intent.get("outcome_ro", event_title),
                "aliases_ro": intent.get("aliases_ro", []),
                "negative_aliases_ro": intent.get("negative_aliases_ro", []),
                "linked_event_ids": [event_id],
                "category_id": intent.get("category_id", "legal_emergency_civic"),
                "kind": intent.get("kind", "direct_goal"),
            })
    else:
        parts = event_id.split(".")
        domain = parts[1] if len(parts) > 1 else "general"
        action = parts[-1]
        proposals.append({
            "id": f"ro.intent.{domain}.{action}",
            "title_ro": _make_title(event_title),
            "outcome_ro": event_title,
            "aliases_ro": [],
            "negative_aliases_ro": [],
            "linked_event_ids": [event_id],
            "category_id": "legal_emergency_civic",
            "kind": "direct_goal",
        })

    data = {
        "schema_version": "2.1.0",
        "generated_at": "2026-06-25",
        "source": "auto-generated from event research data",
        "event_id": event_id,
        "intent_proposals": proposals,
    }
    with open(proposal_path, "w") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    return len(proposals)


count = 0
# Walk everything, process leaf dirs that have event_card.md
for root, dirs, files in os.walk(INBOX):
    if "event_card.md" in files:
        event_name = os.path.basename(root)
        event_id = normalize_event_id(event_name)
        n = generate_proposal(event_id, root)
        if n:
            count += 1
            print(f"  {event_id} ({n} intents)")

print(f"\nDone: {count} intent_proposal.yaml files generated")
