from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
ERRORS: list[str] = []
WARNINGS: list[str] = []


def error(message: str) -> None:
    ERRORS.append(message)


def warn(message: str) -> None:
    WARNINGS.append(message)


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        error(f"Invalid YAML {path.relative_to(ROOT)}: {exc}")
        return None


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        error(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
        return None


def check_required_files() -> None:
    required = [
        "README.md", "CODEX_START_HERE.md", "AGENTS.md", "PLANS.md",
        "codex/EXECUTION_PLAN.md",
        ".agents/skills/acteos-rule-authoring/SKILL.md",
        ".agents/skills/acteos-vertical-slice/SKILL.md",
        ".agents/skills/acteos-research-import/SKILL.md",
        ".agents/skills/acteos-release-certification/SKILL.md",
        ".agents/skills/acteos-intent-authoring/SKILL.md",
        "docs/02_PRODUCT_DOCTRINE.md", "docs/03A_DISCOVERY_INTENT_ATLAS.md", "docs/05_RULE_ENGINE_SPEC.md",
        "docs/11_SECURITY_PRIVACY_COMPLIANCE.md",
        "contracts/openapi.yaml", "contracts/jsonschema/rule.schema.json",
        "contracts/jsonschema/source_claim.schema.json",
        "contracts/jsonschema/intent.schema.json", "contracts/intent_ranking.yaml",
        "data/intent_taxonomy.yaml", "db/0004_intent_discovery.sql",
        "db/0001_init.sql", "codex/CODEX_MASTER_PROMPT.md",
        "codex/PHASE_PROMPTS.md", "codex/TASK_BACKLOG.yaml",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            error(f"Missing required file: {rel}")


def check_parseable_files() -> None:
    for path in ROOT.rglob("*.json"):
        load_json(path)
    for path in list(ROOT.rglob("*.yaml")) + list(ROOT.rglob("*.yml")):
        load_yaml(path)


def check_json_schemas() -> None:
    schema_dir = ROOT / "contracts/jsonschema"
    ids: set[str] = set()
    for path in schema_dir.glob("*.json"):
        schema = load_json(path)
        if not isinstance(schema, dict):
            continue
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            error(f"Invalid JSON Schema {path.name}: {exc}")
        schema_id = schema.get("$id")
        if not schema_id:
            error(f"JSON Schema missing $id: {path.name}")
        elif schema_id in ids:
            error(f"Duplicate JSON Schema $id: {schema_id}")
        else:
            ids.add(schema_id)


def check_openapi() -> None:
    spec = load_yaml(ROOT / "contracts/openapi.yaml")
    if not isinstance(spec, dict):
        return
    if spec.get("openapi") != "3.1.1":
        error("OpenAPI version must be exactly 3.1.1")
    paths = spec.get("paths", {})
    if not paths:
        error("OpenAPI has no paths")
    operation_ids: set[str] = set()
    for path_name, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method.lower() not in {"get", "post", "put", "patch", "delete"}:
                continue
            if not isinstance(operation, dict):
                error(f"Invalid operation {method.upper()} {path_name}")
                continue
            op_id = operation.get("operationId")
            if not op_id:
                error(f"Missing operationId: {method.upper()} {path_name}")
            elif op_id in operation_ids:
                error(f"Duplicate operationId: {op_id}")
            else:
                operation_ids.add(op_id)
            responses = operation.get("responses", {})
            if not responses:
                error(f"Missing responses: {method.upper()} {path_name}")
    if len(operation_ids) < 20:
        warn(f"Only {len(operation_ids)} OpenAPI operations found")


def check_event_taxonomy() -> None:
    data = load_yaml(ROOT / "data/event_taxonomy.yaml")
    if not isinstance(data, dict):
        return
    events = data.get("events", [])
    ids: set[str] = set()
    slugs: set[str] = set()
    for event in events:
        if not isinstance(event, dict):
            error("Event taxonomy contains non-object event")
            continue
        event_id = event.get("id")
        slug = event.get("slug") or event_id
        if not event_id or not re.fullmatch(r"[a-z0-9][a-z0-9_.-]+", event_id):
            error(f"Invalid event id: {event_id}")
        elif event_id in ids:
            error(f"Duplicate event id: {event_id}")
        else:
            ids.add(event_id)
        if not slug or slug in slugs:
            error(f"Missing/duplicate event slug: {slug}")
        else:
            slugs.add(slug)
        if event.get("production_status") == "active" and not event.get("ruleset_id"):
            error(f"Active event without ruleset_id: {event_id}")
    if len(events) < 100:
        error(f"Event atlas is unexpectedly small: {len(events)} events")



def check_intent_taxonomy() -> None:
    data = load_yaml(ROOT / "data/intent_taxonomy.yaml")
    events_data = load_yaml(ROOT / "data/event_taxonomy.yaml")
    if not isinstance(data, dict) or not isinstance(events_data, dict):
        return
    intents = data.get("intents", [])
    event_ids = {e.get("id") for e in events_data.get("events", []) if isinstance(e, dict)}
    ids: set[str] = set()
    normalized_alias_pairs: set[tuple[str, str]] = set()
    for intent in intents:
        if not isinstance(intent, dict):
            error("Intent taxonomy contains non-object intent")
            continue
        intent_id = intent.get("id")
        if not intent_id or not re.fullmatch(r"ro\.intent\.[a-z0-9_.-]+", intent_id):
            error(f"Invalid intent id: {intent_id}")
        elif intent_id in ids:
            error(f"Duplicate intent id: {intent_id}")
        else:
            ids.add(intent_id)
        if not intent.get("aliases_ro"):
            error(f"Intent without aliases: {intent_id}")
        for alias in intent.get("aliases_ro", []):
            norm = re.sub(r"\s+", " ", alias.casefold()).strip()
            pair = (intent_id, norm)
            if pair in normalized_alias_pairs:
                error(f"Duplicate alias inside intent {intent_id}: {alias}")
            normalized_alias_pairs.add(pair)
        for event_id in intent.get("linked_event_ids", []):
            if event_id not in event_ids:
                error(f"Unknown linked event {event_id} in {intent_id}")
    if len(intents) < 20:
        error(f"Intent atlas is unexpectedly small: {len(intents)} intents")
    spec = load_yaml(ROOT / "contracts/openapi.yaml")
    required_paths = {"/v1/discovery/home", "/v1/categories", "/v1/intents", "/v1/intents/resolve-query", "/v1/intents/{intent_type_id}"}
    missing = required_paths - set((spec or {}).get("paths", {}))
    if missing:
        error(f"OpenAPI missing discovery paths: {sorted(missing)}")


def check_backlog() -> None:
    data = load_yaml(ROOT / "codex/TASK_BACKLOG.yaml")
    if not isinstance(data, dict):
        return
    stories = data.get("stories", [])
    ids = {s.get("id") for s in stories if isinstance(s, dict)}
    if None in ids:
        error("Backlog story without id")
    if len(ids) != len(stories):
        error("Duplicate story IDs in backlog")
    for story in stories:
        for dep in story.get("depends_on", []):
            if dep not in ids:
                error(f"Unknown backlog dependency {dep} in {story.get('id')}")
        if not (story.get("acceptance_criteria") or story.get("acceptance")):
            error(f"Story without acceptance criteria: {story.get('id')}")
    if len(stories) < 180:
        error(f"Backlog is unexpectedly small: {len(stories)} stories")


def check_synthetic_isolation() -> None:
    forbidden_markers = ["synthetic", "demo-safe", ".example", ".test"]
    production_dirs = [ROOT / "data/production", ROOT / "rules/production"]
    for directory in production_dirs:
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            for marker in forbidden_markers:
                if marker in text:
                    error(f"Synthetic marker '{marker}' found in production path {path.relative_to(ROOT)}")


def check_sql() -> None:
    init = ROOT / "db/0001_init.sql"
    text = init.read_text(encoding="utf-8") if init.exists() else ""
    for token in ["create schema", "create table", "source_claim", "ruleset", "audit"]:
        if token not in text.lower():
            error(f"SQL baseline missing expected token: {token}")
    if "row level security" not in (ROOT / "db/0003_rls.sql").read_text(encoding="utf-8").lower():
        error("RLS migration does not enable row level security")


def check_traceability() -> None:
    path = ROOT / "codex/TRACEABILITY_MATRIX.csv"
    if not path.exists():
        error("Missing traceability matrix")
        return
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    required = {"requirement_id", "phases", "representative_story_ids", "verification"}
    if not rows or not required.issubset(rows[0].keys()):
        error("Traceability matrix has invalid headers or is empty")


def check_markdown_hygiene() -> None:
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if "turn0search" in text or "cite" in text or "sandbox:/" in text:
            error(f"Internal citation token leaked into {path.relative_to(ROOT)}")
        if len(text.strip()) < 80 and path.name not in {"README.md"}:
            warn(f"Very short documentation file: {path.relative_to(ROOT)}")


def compute_fingerprint() -> str:
    h = hashlib.sha256()
    excluded = {"SHA256SUMS.txt", "VALIDATION_REPORT.md", "PACK_MANIFEST.json"}
    for path in sorted(p for p in ROOT.rglob("*") if p.is_file() and p.name not in excluded):
        h.update(str(path.relative_to(ROOT)).encode())
        h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    check_required_files()
    check_parseable_files()
    check_json_schemas()
    check_openapi()
    check_event_taxonomy()
    check_intent_taxonomy()
    check_backlog()
    check_synthetic_isolation()
    check_sql()
    check_traceability()
    check_markdown_hygiene()

    print(f"Pack fingerprint: {compute_fingerprint()}")
    for item in WARNINGS:
        print(f"WARNING: {item}")
    for item in ERRORS:
        print(f"ERROR: {item}")
    print(f"Validation: {'PASS' if not ERRORS else 'FAIL'} ({len(ERRORS)} errors, {len(WARNINGS)} warnings)")
    return 0 if not ERRORS else 1


if __name__ == "__main__":
    raise SystemExit(main())
