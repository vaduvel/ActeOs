"""JSON Schema validation for governed authoring batches.

Requires jsonschema>=4.18 (ships the ``referencing`` library); part of the
``authoring`` extra. Each rule is validated against contracts/rule.schema.json
and each source claim against contracts/source_claim.schema.json. The predicate
$ref is resolved via a referencing Registry keyed by each schema's $id.

When the step/requirement template schemas are present in the loaded schema set,
each entry in a batch ``templates.yaml`` (``step_templates`` /
``requirement_templates``) is validated too. Template validation is *guarded*:
if those schemas are absent (e.g. a caller passing a minimal schema dict), the
template checks are skipped rather than raising.

Likewise, when source_provenance.schema.json is present in the loaded schema set
and the batch carries a provenance document (a sibling ``sources.yaml`` loaded
under the ``provenance`` key, or inline sources/snapshots), that document is
validated. This too is guarded: callers passing a minimal schema dict skip it.

Also performs a cross-check that every rule.source_claim_ids entry resolves to a
claim declared in source_claims.yaml (a common authoring drift).
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "jsonschema>=4.18 is required for batch validation: pip install 'acteos-rule-engine[authoring]'"
    ) from exc

CONTRACTS_SUBDIR = "contracts"
RULE_SCHEMA = "rule.schema.json"
CLAIM_SCHEMA = "source_claim.schema.json"
PREDICATE_SCHEMA = "predicate.schema.json"
STEP_TEMPLATE_SCHEMA = "step_template.schema.json"
REQUIREMENT_TEMPLATE_SCHEMA = "requirement_template.schema.json"
SOURCE_PROVENANCE_SCHEMA = "source_provenance.schema.json"
DEFAULT_INBOX = "research/inbox"

# Schemas always loaded from disk. Template + provenance schemas are loaded
# best-effort so an older contracts/ checkout without them does not break
# rule/claim validation.
_REQUIRED_SCHEMAS = (RULE_SCHEMA, CLAIM_SCHEMA, PREDICATE_SCHEMA)
_OPTIONAL_SCHEMAS = (STEP_TEMPLATE_SCHEMA, REQUIREMENT_TEMPLATE_SCHEMA, SOURCE_PROVENANCE_SCHEMA)


@dataclass
class ValidationReport:
    batch_id: str
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def load_schemas(contracts_dir: Any) -> dict[str, Any]:
    base = Path(contracts_dir)
    out: dict[str, Any] = {}
    for name in _REQUIRED_SCHEMAS:
        with (base / name).open("r", encoding="utf-8") as fh:
            out[name] = json.load(fh)
    for name in _OPTIONAL_SCHEMAS:
        path = base / name
        if path.exists():
            with path.open("r", encoding="utf-8") as fh:
                out[name] = json.load(fh)
    return out


def _registry(schemas: Mapping[str, Any]) -> "Registry":
    registry = Registry()
    for schema in schemas.values():
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return registry


def _fmt(prefix: str, error: Any) -> str:
    loc = "/".join(str(p) for p in error.path)
    return f"{prefix}: {error.message} at /{loc}" if loc else f"{prefix}: {error.message}"


def validate_batch(batch: Mapping[str, Any], schemas: Mapping[str, Any]) -> ValidationReport:
    registry = _registry(schemas)
    rule_validator = Draft202012Validator(schemas[RULE_SCHEMA], registry=registry)
    claim_validator = Draft202012Validator(schemas[CLAIM_SCHEMA], registry=registry)

    ruleset = batch["ruleset"] or {}
    report = ValidationReport(batch_id=ruleset.get("batch_id", "unknown"))

    for rule in ruleset.get("rules", []):
        for err in sorted(rule_validator.iter_errors(rule), key=lambda e: list(e.path)):
            report.errors.append(_fmt(f"rule {rule.get('id', '?')}", err))

    claims_doc = batch.get("claims") or {}
    for claim in claims_doc.get("claims", []):
        for err in sorted(claim_validator.iter_errors(claim), key=lambda e: list(e.path)):
            report.errors.append(_fmt(f"claim {claim.get('id', '?')}", err))

    # Template validation is guarded: only runs when the schemas are available
    # AND the batch declares a templates document.
    templates_doc = batch.get("templates") or {}
    step_schema = schemas.get(STEP_TEMPLATE_SCHEMA)
    if step_schema is not None:
        step_validator = Draft202012Validator(step_schema, registry=registry)
        for tpl in templates_doc.get("step_templates", []):
            for err in sorted(step_validator.iter_errors(tpl), key=lambda e: list(e.path)):
                report.errors.append(_fmt(f"step_template {tpl.get('id', '?')}", err))
    req_schema = schemas.get(REQUIREMENT_TEMPLATE_SCHEMA)
    if req_schema is not None:
        req_validator = Draft202012Validator(req_schema, registry=registry)
        for tpl in templates_doc.get("requirement_templates", []):
            for err in sorted(req_validator.iter_errors(tpl), key=lambda e: list(e.path)):
                report.errors.append(_fmt(f"requirement_template {tpl.get('id', '?')}", err))

    # Provenance doc validation is guarded the same way: only runs when the
    # source_provenance schema is loaded AND the batch carries a provenance doc.
    prov_schema = schemas.get(SOURCE_PROVENANCE_SCHEMA)
    provenance_doc = batch.get("provenance")
    if prov_schema is not None and isinstance(provenance_doc, Mapping) and provenance_doc:
        prov_validator = Draft202012Validator(prov_schema, registry=registry)
        label = provenance_doc.get("batch_id", report.batch_id)
        for err in sorted(prov_validator.iter_errors(provenance_doc), key=lambda e: list(e.path)):
            report.errors.append(_fmt(f"provenance {label}", err))

    claim_ids = {c.get("id") for c in claims_doc.get("claims", [])}
    for rule in ruleset.get("rules", []):
        for cid in rule.get("source_claim_ids", []):
            if cid not in claim_ids:
                report.errors.append(
                    f"rule {rule.get('id', '?')}: source_claim_id '{cid}' not found in source_claims.yaml"
                )
    return report


def validate_main(argv: list[str] | None = None) -> int:
    from .loader import discover_batches, load_batch

    argv = list(sys.argv[1:] if argv is None else argv)
    inbox = argv[0] if argv else DEFAULT_INBOX
    base = Path(inbox)
    contracts = Path(argv[1]) if len(argv) > 1 else base.parent.parent / CONTRACTS_SUBDIR
    if not base.exists():
        print(f"inbox not found: {base}", file=sys.stderr)
        return 2
    if not contracts.exists():
        print(f"contracts not found: {contracts}", file=sys.stderr)
        return 2

    schemas = load_schemas(contracts)
    batches = discover_batches(base)
    failed = 0
    for batch_dir in batches:
        report = validate_batch(load_batch(batch_dir), schemas)
        status = "OK  " if report.ok else "FAIL"
        print(f"[{status}] {report.batch_id}: {len(report.errors)} error(s)")
        if not report.ok:
            failed += 1
            for err in report.errors:
                print(f"        {err}")
    print(f"\nTOTAL: {len(batches) - failed}/{len(batches)} batches valid")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(validate_main())
