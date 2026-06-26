#!/usr/bin/env python3
"""Compile certified inbox batches into a content-addressed release bundle.

Discovers + loads research-inbox batches via the engine loader, runs the
certification gate and the publish compiler, prints a summary and (optionally)
writes the bundle manifest JSON.

    exit 0  -> bundle compiled (go, or conditional_go with --allow-conditional)
    exit 2  -> conditional_go without --allow-conditional
    exit 1  -> no_go / usage error

Usage:
    python infra/scripts/publish_release.py --out build/bundle.json
    python infra/scripts/publish_release.py --batch ro.life.minor_passport --allow-conditional
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INBOX = PACK_ROOT / "research" / "inbox"
DEFAULT_CONTRACTS = PACK_ROOT / "contracts" / "jsonschema"

ENGINE_SRC = PACK_ROOT / "python" / "acteos_rule_engine" / "src"
if ENGINE_SRC.exists() and str(ENGINE_SRC) not in sys.path:
    sys.path.insert(0, str(ENGINE_SRC))

from acteos_rule_engine.authoring.loader import (  # noqa: E402
    discover_batches,
    load_batch,
)
from acteos_rule_engine.authoring.publish import (  # noqa: E402
    PublishError,
    compile_bundle,
)


def _print_summary(bundle) -> None:
    s = bundle.summary()
    print("=" * 72)
    print("ActeOS Release Bundle")
    print("=" * 72)
    print(f"version           : {s['version']}")
    print(f"manifest_sha256   : {s['manifest_sha256']}")
    print(f"engine_compat     : {s['engine_compatibility']}")
    print(f"certification     : {s['certification_verdict']}")
    print(f"rule revisions    : {s['rule_revision_count']} "
          f"(publishable {s['publishable_rule_count']}, deferred {s['deferred_rule_count']})")
    print(f"source claims     : {s['source_claim_count']} "
          f"(provenance pending {s['provenance_pending_count']})")
    print(f"required events   : {len(s['required_event_type_ids'])}")
    print(f"issues            : {s['issue_count']}")
    if bundle.issues:
        print()
        print("ISSUES:")
        for issue in bundle.issues:
            print(f"  - {issue}")
    if bundle.deferred_revisions():
        print()
        print("DEFERRED (no effective_from -> cannot enter content.rule_revisions):")
        for rev in bundle.deferred_revisions():
            print(f"  - {rev.canonical_rule_id}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ActeOS release bundle compiler.")
    parser.add_argument("--inbox", type=Path, default=DEFAULT_INBOX)
    parser.add_argument("--contracts", type=Path, default=DEFAULT_CONTRACTS)
    parser.add_argument("--batch", action="append", default=None,
                        help="Restrict to specific batch directory name(s). Repeatable.")
    parser.add_argument("--scope", action="append", default=None,
                        help="Release scope tag(s). Repeatable. Defaults to R1.")
    parser.add_argument("--out", type=Path, default=None,
                        help="Write the bundle manifest JSON to this path.")
    parser.add_argument("--no-schema", action="store_true",
                        help="Skip JSON-schema validation of batches.")
    parser.add_argument("--allow-conditional", action="store_true",
                        help="Compile even when certification is conditional_go.")
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
    if not args.no_schema and args.contracts.exists():
        from acteos_rule_engine.authoring.validate import load_schemas

        schemas = load_schemas(args.contracts)

    batches = [load_batch(d) for d in batch_dirs]
    scope = tuple(args.scope) if args.scope else ("R1",)

    try:
        bundle = compile_bundle(
            batches,
            scope=scope,
            schemas=schemas,
            allow_conditional=args.allow_conditional,
        )
    except PublishError as exc:
        print(f"PUBLISH REFUSED: {exc}", file=sys.stderr)
        if exc.report is not None and exc.report.verdict == "conditional_go":
            return 2
        return 1

    _print_summary(bundle)

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(bundle.to_manifest(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print()
        print(f"wrote bundle manifest -> {args.out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
