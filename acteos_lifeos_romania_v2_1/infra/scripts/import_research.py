#!/usr/bin/env python3
"""Import processed research rule-pack batches into the v2.1 governed inbox.

Each *event batch* is a directory that holds the six authoring artifacts:

    event_card.md
    rules.yaml
    source_claims.yaml
    intent_proposal.yaml
    gaps.md
    fixtures/golden.yaml

The research was authored under a legacy tree nested as
``<inbox>/batch_NN/<event>/`` while the v2.1 loader (``discover_batches``)
expects each batch directory directly under ``research/inbox/``. This tool
bridges the gap deterministically:

  * discovers event batches recursively (any depth, so batch_NN/<event>/ works);
  * validates each batch against the v2.1 JSON Schemas, reusing the SAME
    validator the engine uses (acteos_rule_engine.authoring.validate) so an
    import that passes here will load and validate identically in the engine;
  * copies the artifacts VERBATIM (byte-for-byte) into
    research/inbox/<event_type_id>/ so loader.discover_batches finds them flat;
  * writes IMPORT_MANIFEST.json (SHA-256 + size per file) and a human-readable
    IMPORT_REPORT.md (counts + every rejected/skipped batch with reasons).

Governance (skill: acteos-research-import):
  * the inbox is STAGING ONLY — this tool NEVER promotes anything to the active
    ruleset. Promotion requires a separate four-eyes review + release gate.
  * any rule/claim ``status: active`` present in the source is copied verbatim
    but has no runtime effect until that governed promotion happens.
  * only batches that PASS schema validation are copied; invalid batches are
    reported as rejected and left untouched.

Usage (from the pack root; defaults wire the standard repo layout)::

    python infra/scripts/import_research.py            # import with defaults
    python infra/scripts/import_research.py --check-only  # validate, copy nothing
    python infra/scripts/import_research.py --overwrite   # replace existing dirs

Exit code is 0 when no batch was rejected, 1 when at least one batch failed
validation, and 2 on a fatal setup error (missing source/contracts).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

# Reuse the governed validator/loader so import validation == engine validation.
try:
    from acteos_rule_engine.authoring.loader import load_batch
    from acteos_rule_engine.authoring.validate import load_schemas, validate_batch
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "acteos-rule-engine[authoring] must be installed: "
        "pip install -e 'python/acteos_rule_engine[authoring]'"
    ) from exc

# Pack root = .../acteos_lifeos_romania_v2_1 ; repo root = its parent.
PACK_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PACK_ROOT.parent

# The six artifacts per event batch (relative to the batch directory).
PACK_FILES = (
    "event_card.md",
    "rules.yaml",
    "source_claims.yaml",
    "intent_proposal.yaml",
    "gaps.md",
    "fixtures/golden.yaml",
)
# A directory is a batch iff it contains at least these (loader contract).
BATCH_MARKERS = ("rules.yaml", "fixtures/golden.yaml")


def find_event_batches(source: Path) -> list[Path]:
    """Recursively find event-batch directories under ``source``.

    A directory qualifies when it directly contains rules.yaml AND
    fixtures/golden.yaml. Once a directory qualifies we do not descend into it.
    """
    found: list[Path] = []

    def walk(directory: Path) -> None:
        if all((directory / marker).is_file() for marker in BATCH_MARKERS):
            found.append(directory)
            return
        for child in sorted(p for p in directory.iterdir() if p.is_dir()):
            walk(child)

    if source.is_dir():
        walk(source)
    return sorted(found)


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def event_type_id_of(batch_dir: Path) -> str:
    doc = yaml.safe_load((batch_dir / "rules.yaml").read_text(encoding="utf-8")) or {}
    event_type_id = doc.get("event_type_id")
    if not event_type_id or not isinstance(event_type_id, str):
        raise ValueError(f"{batch_dir}/rules.yaml is missing a string 'event_type_id'")
    return event_type_id


def validate_event(batch_dir: Path, schemas: dict[str, Any]) -> list[str]:
    return list(validate_batch(load_batch(batch_dir), schemas).errors)


def copy_pack(batch_dir: Path, dest_dir: Path) -> list[str]:
    copied: list[str] = []
    for rel in PACK_FILES:
        src = batch_dir / rel
        if not src.is_file():
            continue
        dst = dest_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(rel)
    return copied


def _render_report(manifest: dict[str, Any]) -> str:
    counts = manifest["counts"]
    lines: list[str] = [
        "# Research Import Report",
        "",
        f"- generated_at: {manifest['generated_at']}",
        f"- source: `{manifest['source']}`",
        f"- dest: `{manifest['dest']}`",
        f"- mode: {'check-only' if manifest['check_only'] else 'import'}",
        "",
        "## Counts",
        "",
        f"- discovered: {counts['discovered']}",
        f"- imported (valid): {counts['imported']}",
        f"- rejected (invalid): {counts['rejected']}",
        f"- skipped (duplicate/exists): {counts['skipped']}",
        "",
    ]
    if manifest["rejected"]:
        lines += ["## Rejected (NOT imported)", ""]
        for item in manifest["rejected"]:
            label = item.get("event_type_id") or item["source"]
            lines.append(f"### {label}")
            lines.append(f"- source: `{item['source']}`")
            for err in item["errors"]:
                lines.append(f"  - {err}")
            lines.append("")
    if manifest["skipped"]:
        lines += ["## Skipped", ""]
        for item in manifest["skipped"]:
            lines.append(
                f"- `{item['source']}` ({item.get('event_type_id')}): {item['reason']}"
            )
        lines.append("")
    lines += [
        "## Governance",
        "",
        "The inbox is staging only. Nothing imported here is active. Promotion to",
        "the active ruleset requires four-eyes review + the release gate",
        "(skill: acteos-release-certification). `status: active` on a source rule",
        "or claim is preserved verbatim but has no runtime effect until then.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--source",
        type=Path,
        default=REPO_ROOT / "docs/product/lifeos-romania/research/inbox",
        help="root of the research tree to import (default: legacy docs inbox)",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=PACK_ROOT / "research/inbox",
        help="governed v2.1 inbox to import into",
    )
    parser.add_argument(
        "--contracts",
        type=Path,
        default=PACK_ROOT / "contracts/jsonschema",
        help="directory holding rule/source_claim/predicate .schema.json",
    )
    parser.add_argument("--report", type=Path, default=None, help="report path (default: <dest>/../IMPORT_REPORT.md)")
    parser.add_argument("--manifest", type=Path, default=None, help="manifest path (default: <dest>/IMPORT_MANIFEST.json)")
    parser.add_argument("--check-only", action="store_true", help="validate only; copy nothing and write no files")
    parser.add_argument("--overwrite", action="store_true", help="overwrite an existing destination event directory")
    args = parser.parse_args(argv)

    source: Path = args.source
    dest: Path = args.dest
    if not source.is_dir():
        print(f"source not found: {source}", file=sys.stderr)
        return 2
    if not args.contracts.is_dir():
        print(f"contracts not found: {args.contracts}", file=sys.stderr)
        return 2

    schemas = load_schemas(args.contracts)
    batches = find_event_batches(source)

    imported: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    seen: dict[str, Path] = {}

    for batch_dir in batches:
        try:
            event_type_id = event_type_id_of(batch_dir)
        except (ValueError, yaml.YAMLError) as exc:
            rejected.append({"source": str(batch_dir), "event_type_id": None, "errors": [str(exc)]})
            continue

        if event_type_id in seen:
            skipped.append({
                "source": str(batch_dir),
                "event_type_id": event_type_id,
                "reason": f"duplicate event_type_id (already imported from {seen[event_type_id]})",
            })
            continue

        errors = validate_event(batch_dir, schemas)
        if errors:
            rejected.append({"source": str(batch_dir), "event_type_id": event_type_id, "errors": errors})
            continue

        dest_dir = dest / event_type_id
        if not args.check_only and dest_dir.exists() and not args.overwrite:
            skipped.append({
                "source": str(batch_dir),
                "event_type_id": event_type_id,
                "reason": "destination already exists (use --overwrite)",
            })
            continue

        files_meta = [
            {"path": f"{event_type_id}/{rel}", "sha256": sha256_of(batch_dir / rel), "bytes": (batch_dir / rel).stat().st_size}
            for rel in PACK_FILES
            if (batch_dir / rel).is_file()
        ]
        if not args.check_only:
            copy_pack(batch_dir, dest_dir)

        seen[event_type_id] = batch_dir
        imported.append({"event_type_id": event_type_id, "source": str(batch_dir), "files": files_meta})

    manifest = {
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "source": str(source),
        "dest": str(dest),
        "check_only": args.check_only,
        "counts": {
            "discovered": len(batches),
            "imported": len(imported),
            "rejected": len(rejected),
            "skipped": len(skipped),
        },
        "imported": imported,
        "rejected": rejected,
        "skipped": skipped,
    }

    report_text = _render_report(manifest)

    if not args.check_only:
        manifest_path = args.manifest or (dest / "IMPORT_MANIFEST.json")
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report_path = args.report or (dest.parent / "IMPORT_REPORT.md")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report_text, encoding="utf-8")

    print(report_text)
    print(
        f"TOTAL: {len(imported)}/{len(batches)} imported, "
        f"{len(rejected)} rejected, {len(skipped)} skipped"
    )
    return 0 if not rejected else 1


if __name__ == "__main__":
    raise SystemExit(main())
