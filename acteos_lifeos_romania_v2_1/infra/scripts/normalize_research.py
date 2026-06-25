#!/usr/bin/env python3
"""Canonicalize research YAML so it conforms to the v2.1 JSON Schemas.

Legacy/authoring drift makes otherwise-correct research fail schema validation
even though the values are right. The most widespread case:

  * Bare ISO date scalars. YAML auto-types ``accessed_at: 2026-06-25`` as a
    Python ``datetime.date``; the schema (correctly) requires a ``string`` with
    ``format: date``. We quote the known date-valued keys so they load as
    strings WITHOUT changing the date value.

This normalizer is intentionally minimal-diff (line-targeted regex) so the git
diff on the research tree stays small and reviewable. It never touches evidence
text, statements, URLs, or predicate logic. Already-quoted dates are left alone,
so it is idempotent.

The ``when.clauses`` -> typed ``op``/``args`` predicate migration is deliberately
NOT done here yet: the exact legacy shape must be read first so the transform is
faithful rather than guessed.

Usage (from the pack root; default targets the legacy research inbox)::

    python infra/scripts/normalize_research.py             # dry run (report only)
    python infra/scripts/normalize_research.py --write     # apply in place
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PACK_ROOT.parent

# Keys whose value is a date per the v2.1 schemas (rule/source_claim) plus the
# golden-fixture ambient ``reference_date``.
DATE_KEYS = (
    "accessed_at",
    "published_at",
    "effective_from",
    "effective_to",
    "review_due_at",
    "hard_expiry_at",
    "reference_date",
)

# Matches a block-style ``key: 2026-06-25`` (optionally a list item ``- key:``)
# with an UNQUOTED ISO date value, optionally followed by a comment. Quoted
# values never match because the value would start with a quote, not a digit.
_DATE_LINE = re.compile(
    r"(?m)^(?P<prefix>\s*(?:-\s*)?(?:" + "|".join(DATE_KEYS) + r")\s*:[ \t]*)"
    r"(?P<date>\d{4}-\d{2}-\d{2})"
    r"(?P<suffix>[ \t]*(?:#.*)?)$"
)


def quote_dates(text: str) -> tuple[str, int]:
    return _DATE_LINE.subn(r"\g<prefix>'\g<date>'\g<suffix>", text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Quote bare ISO date scalars in research YAML (schema canonicalization)."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=REPO_ROOT / "docs/product/lifeos-romania/research/inbox",
        help="root of the research tree to normalize",
    )
    parser.add_argument("--write", action="store_true", help="apply changes in place (default: dry run)")
    args = parser.parse_args(argv)

    if not args.source.is_dir():
        print(f"source not found: {args.source}", file=sys.stderr)
        return 2

    total_files = 0
    total_changes = 0
    changed_files = 0
    for path in sorted(args.source.rglob("*.yaml")):
        total_files += 1
        original = path.read_text(encoding="utf-8")
        updated, count = quote_dates(original)
        if count:
            changed_files += 1
            total_changes += count
            rel = path.relative_to(args.source)
            print(f"{'WROTE' if args.write else 'WOULD FIX'} {rel}: {count} date scalar(s)")
            if args.write:
                path.write_text(updated, encoding="utf-8")

    mode = "applied" if args.write else "dry-run"
    print(
        f"\n{mode}: {total_changes} date scalar(s) quoted across {changed_files}/{total_files} YAML file(s)"
    )
    if not args.write and total_changes:
        print("Re-run with --write to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
