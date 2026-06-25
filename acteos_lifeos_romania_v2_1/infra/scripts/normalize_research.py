#!/usr/bin/env python3
"""Canonicalize research YAML so it conforms to the v2.1 JSON Schemas.

Legacy/authoring drift makes otherwise-correct research fail schema validation
even though the underlying values are right. This normalizer is intentionally
minimal-diff (line/token-targeted regex) so the git diff on the research tree
stays small and reviewable. It never touches evidence text, statements, URLs,
numeric thresholds, or message_ro wording. Every transform is idempotent.

Why string-level (and not a YAML round-trip): safe_load->safe_dump would re-type
bare ISO dates as datetime.date and reflow the whole file. We deliberately edit
text so a single pass quotes dates AND rewrites the few legacy tokens without
disturbing anything else.

Transforms (each verified against the v2.1 contracts + engine and the real
research files, not guessed):

  1. Bare ISO date scalars. YAML auto-types ``accessed_at: 2026-06-25`` as a
     Python ``datetime.date``; the schema requires a ``string``/``format: date``.
     Known date-valued keys are quoted so they load as strings WITHOUT changing
     the value. Already-quoted dates never match (idempotent).

  2. Legacy boolean predicate shape -> typed predicate (predicate.schema.json):
       ``op: and`` -> ``op: all``     ``op: or`` -> ``op: any``
       ``clauses:`` -> ``args:``
     The engine AST (acteos_rule_engine.authoring.ast) only knows
     all/any/not(+args/arg); ``and``/``or``/``clauses`` are rejected by the
     predicate schema (op enum + additionalProperties:false) and are dead to the
     evaluator. Nested leaf predicates are already op/field/value -> untouched.

  3. ``authority_level: local`` -> ``authority_level: uat``. ``local`` is not in
     the taxonomy; every occurrence in the corpus is a municipal (Primarie/UAT)
     source or rule whose canonical level is ``uat`` (source_claim.schema enum).
     Applied to both rules.yaml and source_claims.yaml.

  4. ``emt_warning_placeholder`` -> ``emit_warning``. A literal authoring typo
     for the ``emit_warning`` effect (rule.schema effects enum).

NOT done here: fabricating ``effective_from``. It is OPTIONAL on rules (the
engine treats a missing lower temporal bound safely) and inventing a legal start
date -- e.g. from a claim's ``accessed_at`` -- would violate the truth-guard.
Temporal completeness is enforced at the release-certification gate, not import.

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

# Block-style ``key: 2026-06-25`` (optionally a ``- key:`` list item) with an
# UNQUOTED ISO date value, optionally followed by a comment. Quoted values never
# match (the value would start with a quote, not a digit), so this is idempotent.
_DATE_LINE = re.compile(
    r"(?m)^(?P<prefix>\s*(?:-\s*)?(?:" + "|".join(DATE_KEYS) + r")\s*:[ \t]*)"
    r"(?P<date>\d{4}-\d{2}-\d{2})"
    r"(?P<suffix>[ \t]*(?:#.*)?)$"
)

# Legacy boolean operators -> typed combinators. Anchored on the ``op:`` key so
# a field value or free text is never touched. Handles block style (``op: and``)
# and flow style (``{ op: and, ... }``). ``\b`` after the word prevents matching
# ``android``/``order`` and the already-correct ``all``/``any``.
_OP_AND = re.compile(r"(?P<k>\bop:[ \t]*)and\b")
_OP_OR = re.compile(r"(?P<k>\bop:[ \t]*)or\b")
# Legacy ``clauses:`` (the args list of and/or) -> ``args:``. ``clauses`` is
# unique to the legacy predicate shape in this corpus.
_CLAUSES = re.compile(r"\bclauses(?P<s>[ \t]*:)")
# ``authority_level: local`` -> ``uat`` (block or ``- `` list item).
_LOCAL = re.compile(r"(?P<k>\bauthority_level:[ \t]*)local\b")

_TYPO_FROM = "emt_warning_placeholder"
_TYPO_TO = "emit_warning"


def normalize(text: str) -> tuple[str, dict[str, int]]:
    """Apply every canonicalization to ``text``; return (new_text, counts)."""
    counts: dict[str, int] = {}
    text, counts["dates_quoted"] = _DATE_LINE.subn(
        r"\g<prefix>'\g<date>'\g<suffix>", text
    )
    text, counts["op_and_to_all"] = _OP_AND.subn(r"\g<k>all", text)
    text, counts["op_or_to_any"] = _OP_OR.subn(r"\g<k>any", text)
    text, counts["clauses_to_args"] = _CLAUSES.subn(r"args\g<s>", text)
    text, counts["authority_local_to_uat"] = _LOCAL.subn(r"\g<k>uat", text)
    typo = text.count(_TYPO_FROM)
    if typo:
        text = text.replace(_TYPO_FROM, _TYPO_TO)
    counts["emt_warning_typo_fixed"] = typo
    return text, counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Canonicalize research YAML to the v2.1 JSON Schemas (minimal-diff)."
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
    changed_files = 0
    totals: dict[str, int] = {}
    for path in sorted(args.source.rglob("*.yaml")):
        total_files += 1
        original = path.read_text(encoding="utf-8")
        updated, counts = normalize(original)
        changed = sum(counts.values())
        if changed:
            changed_files += 1
            for key, value in counts.items():
                totals[key] = totals.get(key, 0) + value
            rel = path.relative_to(args.source)
            detail = ", ".join(f"{k}={v}" for k, v in counts.items() if v)
            print(f"{'WROTE' if args.write else 'WOULD FIX'} {rel}: {detail}")
            if args.write:
                path.write_text(updated, encoding="utf-8")

    mode = "applied" if args.write else "dry-run"
    summary = ", ".join(f"{k}={v}" for k, v in totals.items() if v) or "no changes"
    print(f"\n{mode}: {summary} across {changed_files}/{total_files} YAML file(s)")
    if not args.write and changed_files:
        print("Re-run with --write to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
