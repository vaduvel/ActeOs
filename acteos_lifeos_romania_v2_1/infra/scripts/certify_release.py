#!/usr/bin/env python3
"""Release certification gate for ActeOS rule batches.

Discovers research-inbox batches, runs the deterministic governance gate from
``acteos_rule_engine.authoring.certification`` and emits a machine + human
report plus an exit code suitable for CI:

    exit 0  -> go
    exit 0  -> conditional_go ONLY when --allow-conditional is passed
    exit 2  -> conditional_go without --allow-conditional
    exit 1  -> no_go (one or more blockers) / usage error

Usage:
    python infra/scripts/certify_release.py
    python infra/scripts/certify_release.py --inbox research/inbox --json out.json
    python infra/scripts/certify_release.py --batch ro.life.minor_passport
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INBOX = PACK_ROOT / "research" / "inbox"
DEFAULT_CONTRACTS = PACK_ROOT / "contracts" / "jsonschema"

# Make the rule engine importable when run directly from a checkout (fallback;
# in CI the package is installed via pyproject and this is a no-op).
ENGINE_SRC = PACK_ROOT / "python" / "acteos_rule_engine" / "src"
if ENGINE_SRC.exists() and str(ENGINE_SRC) not in sys.path:
    sys.path.insert(0, str(ENGINE_SRC))

from acteos_rule_engine.authoring.certification import (  # noqa: E402
    PUBLISH_TIME_OBLIGATIONS,
    VERDICT_CONDITIONAL,
    VERDICT_NO_GO,
    certify_batches,
)
from acteos_rule_engine.authoring.loader import (  # noqa: E402
    discover_batches,
    load_batch,
)


def _print_human_report(report) -> None:
    print("=" * 72)
    print("ActeOS Release Certification")
    print("=" * 72)
    print(f"batches : {len(report.batch_ids)}")
    print(f"rules   : {report.rule_count}")
    print(f"blockers: {len(report.blockers)}")
    print(f"warnings: {len(report.warnings)}")
    print()

    if report.blockers:
        print("BLOCKERS (no-go):")
        for f in report.blockers:
            loc = " / ".join(x for x in (f.batch_id, f.rule_id) if x)
            print(f"  [{f.code}] {loc}: {f.message}")
        print()

    if report.warnings:
        print("WARNINGS (conditional):")
        for f in report.warnings:
            loc = " / ".join(x for x in (f.batch_id, f.rule_id) if x)
            print(f"  [{f.code}] {loc}: {f.message}")
        print()

    print("Publish-time obligations (NOT checkable from inbox content):")
    for note in PUBLISH_TIME_OBLIGATIONS:
        print(f"  - {note}")
    print()

    print(f"VERDICT: {report.verdict.upper()}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ActeOS release certification gate.")
    parser.add_argument("--inbox", type=Path, default=DEFAULT_INBOX)
    parser.add_argument("--contracts", type=Path, default=DEFAULT_CONTRACTS)
    parser.add_argument(
        "--batch",
        action="append",
        default=None,
        help="Restrict to specific batch directory name(s). Repeatable.",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=None,
        help="Write the machine-readable report to this path.",
    )
    parser.add_argument(
        "--no-schema",
        action="store_true",
        help="Skip JSON-schema validation of batches.",
    )
    parser.add_argument(
        "--allow-conditional",
        action="store_true",
        help="Treat conditional_go as releasable (exit 0).",
    )
    args = parser.parse_args(argv)

    inbox: Path = args.inbox
    if not inbox.exists():
        print(f"error: inbox not found: {inbox}", file=sys.stderr)
        return 1

    batch_dirs = list(discover_batches(inbox))
    if args.batch:
        wanted = set(args.batch)
        batch_dirs = [d for d in batch_dirs if Path(d).name in wanted]
        if not batch_dirs:
            print(f"error: no batches matched {sorted(wanted)}", file=sys.stderr)
            return 1

    schemas = None
    if not args.no_schema:
        if args.contracts.exists():
            from acteos_rule_engine.authoring.validate import load_schemas

            schemas = load_schemas(args.contracts)
        else:
            print(
                f"warning: contracts dir not found, skipping schema checks: {args.contracts}",
                file=sys.stderr,
            )

    batches = [load_batch(d) for d in batch_dirs]
    report = certify_batches(batches, schemas=schemas)

    _print_human_report(report)

    if args.json is not None:
        args.json.write_text(
            json.dumps(report.as_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    if report.verdict == VERDICT_NO_GO:
        return 1
    if report.verdict == VERDICT_CONDITIONAL and not args.allow_conditional:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
