#!/usr/bin/env python3
"""CLI: compile certified inbox batches + event catalog -> content.* publish.

This is the operational entry point that ties the three pure compilers together
and drives the Postgres content adapter:

    compile_event_types(catalog)  ->  content.life_event_types rows
    compile_bundle(batches)       ->  content.rule_sets / rule_revisions / members
    SqlAlchemyContentRepository.publish_release(...)  ->  one FK-safe transaction

Two modes:
    dry-run (default)  Compiles everything in memory, prints the FK-ordered SQL
                       (life_event_types -> rule_sets -> rule_revisions ->
                       rule_set_members) and a summary. Touches no database.
    --apply            Opens an engine from --database-url / ACTEOS_DATABASE_URL
                       and writes the release in a single transaction.

The heavy lifting (:func:`build_dry_run` / :func:`compile_release`) is pure and
unit tested with in-memory dicts, so it needs neither the filesystem nor a
database. Only :func:`main` (file loading) and ``--apply`` touch I/O.

Exit codes:
    0  dry-run compiled OK, or --apply wrote the release
    2  certification verdict is conditional_go without --allow-conditional
    1  no_go / usage error / uncovered event types / missing database url

Usage:
    python -m acteos_api.publish_db                       # dry-run, all R1
    python -m acteos_api.publish_db --batch ro.life.minor_passport
    python -m acteos_api.publish_db --apply --database-url postgresql+psycopg://...
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from acteos_rule_engine.authoring.event_types import compile_event_types
from acteos_rule_engine.authoring.publish import (
    PublishError,
    PublishedBundle,
    compile_bundle,
)

from .content_publish import (
    ContentPublishError,
    SqlAlchemyContentRepository,
    compiled_event_type_sql,
    compiled_sql,
    missing_event_types,
)

# services/api/src/acteos_api/publish_db.py -> parents[4] == pack root.
_PACK_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CATALOG = _PACK_ROOT / "data" / "r1_event_catalog.yaml"
DEFAULT_INBOX = _PACK_ROOT / "research" / "inbox"
DEFAULT_CONTRACTS = _PACK_ROOT / "contracts" / "jsonschema"


@dataclass(frozen=True)
class DryRunPlan:
    """Pure, serialization-friendly result of compiling a release for publish."""

    version: str
    manifest_sha256: str
    event_type_count: int
    event_type_sql: list[str]
    publish_sql: list[str]
    missing_event_types: list[str]
    deferred_rule_ids: list[str]
    summary: dict[str, Any]

    @property
    def statements_sql(self) -> list[str]:
        """All INSERTs in FK-safe order (event types first, then the bundle)."""
        return [*self.event_type_sql, *self.publish_sql]


def compile_release(
    catalog: Mapping[str, Any],
    batches: Sequence[Mapping[str, Any]],
    *,
    scope: Iterable[str] = ("R1",),
    schemas: Mapping[str, Any] | None = None,
    allow_conditional: bool = False,
) -> tuple[list[Any], PublishedBundle]:
    """Compile event-type records and the rule bundle for one release scope.

    Pure and side-effect free. Raises :class:`PublishError` if certification is
    ``no_go`` (always) or ``conditional_go`` without ``allow_conditional``.
    """

    scope_tuple = tuple(scope)
    event_records = compile_event_types(catalog, scope=scope_tuple)
    bundle = compile_bundle(
        list(batches),
        scope=scope_tuple,
        schemas=schemas,
        allow_conditional=allow_conditional,
    )
    return event_records, bundle


def build_dry_run(
    catalog: Mapping[str, Any],
    batches: Sequence[Mapping[str, Any]],
    *,
    scope: Iterable[str] = ("R1",),
    schemas: Mapping[str, Any] | None = None,
    allow_conditional: bool = False,
    strict: bool = False,
) -> DryRunPlan:
    """Compile a release into a printable, DB-free :class:`DryRunPlan`.

    ``strict=False`` (default) renders only the publishable subset of rule
    revisions (rules with ``effective_from``); deferred rules are surfaced in
    ``deferred_rule_ids`` rather than fabricated. ``strict=True`` re-raises
    :class:`PublishError` if any rule lacks ``effective_from``.
    """

    event_records, bundle = compile_release(
        catalog,
        batches,
        scope=scope,
        schemas=schemas,
        allow_conditional=allow_conditional,
    )
    missing = missing_event_types(bundle, event_records)
    event_type_sql = compiled_event_type_sql(event_records)
    publish_sql = compiled_sql(bundle, strict=strict)

    summary = dict(bundle.summary())
    summary["event_type_count"] = len(event_records)
    summary["missing_event_types"] = missing

    return DryRunPlan(
        version=bundle.version,
        manifest_sha256=bundle.manifest_sha256,
        event_type_count=len(event_records),
        event_type_sql=event_type_sql,
        publish_sql=publish_sql,
        missing_event_types=missing,
        deferred_rule_ids=[r.canonical_rule_id for r in bundle.deferred_revisions()],
        summary=summary,
    )


def _print_plan(plan: DryRunPlan) -> None:
    s = plan.summary
    print("=" * 72)
    print("ActeOS DB Publish - DRY RUN (no database writes)")
    print("=" * 72)
    print(f"version           : {plan.version}")
    print(f"manifest_sha256   : {plan.manifest_sha256}")
    print(f"event types       : {plan.event_type_count}")
    print(
        f"rule revisions    : {s['rule_revision_count']} "
        f"(publishable {s['publishable_rule_count']}, deferred {s['deferred_rule_count']})"
    )
    print(f"required events   : {len(s['required_event_type_ids'])}")
    print(f"missing events    : {len(plan.missing_event_types)}")
    print(f"certification     : {s['certification_verdict']}")
    print()
    print(
        f"-- {len(plan.event_type_sql)} event-type statement(s), "
        f"{len(plan.publish_sql)} bundle statement(s) --"
    )
    for sql in plan.statements_sql:
        print()
        print(sql + ";")
    if plan.missing_event_types:
        print()
        print("WARNING: bundle references event types absent from catalog rows")
        print("         (--apply will refuse until the catalog covers them):")
        for event_id in plan.missing_event_types:
            print(f"  - {event_id}")
    if plan.deferred_rule_ids:
        print()
        print("DEFERRED (no effective_from -> excluded from content.rule_revisions):")
        for rid in plan.deferred_rule_ids:
            print(f"  - {rid}")


def _load_catalog(path: Path) -> Mapping[str, Any]:
    import yaml  # lazy: only needed for the filesystem path, not build_dry_run.

    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, Mapping):
        raise ValueError(f"catalog at {path} is not a mapping")
    return data


def _load_batches(
    inbox: Path,
    contracts: Path,
    *,
    wanted: set[str] | None,
    use_schema: bool,
) -> tuple[list[Mapping[str, Any]], Mapping[str, Any] | None]:
    # Lazy imports: the engine authoring loader requires PyYAML at import time.
    from acteos_rule_engine.authoring.loader import discover_batches, load_batch

    batch_dirs = list(discover_batches(inbox))
    if wanted:
        batch_dirs = [d for d in batch_dirs if Path(d).name in wanted]

    schemas = None
    if use_schema and contracts.exists():
        from acteos_rule_engine.authoring.validate import load_schemas

        schemas = load_schemas(contracts)

    batches = [load_batch(d) for d in batch_dirs]
    return batches, schemas


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compile + publish an ActeOS content release into content.*",
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG,
                        help="Life-event catalog YAML (waves -> events).")
    parser.add_argument("--inbox", type=Path, default=DEFAULT_INBOX,
                        help="Research inbox directory of governed batches.")
    parser.add_argument("--contracts", type=Path, default=DEFAULT_CONTRACTS,
                        help="JSON-schema directory for batch validation.")
    parser.add_argument("--batch", action="append", default=None,
                        help="Restrict to batch directory name(s). Repeatable.")
    parser.add_argument("--scope", action="append", default=None,
                        help="Release scope tag(s). Repeatable. Defaults to R1.")
    parser.add_argument("--no-schema", action="store_true",
                        help="Skip JSON-schema validation of batches.")
    parser.add_argument("--allow-conditional", action="store_true",
                        help="Compile even when certification is conditional_go.")
    parser.add_argument("--strict", action="store_true",
                        help="Refuse to emit if any rule lacks effective_from.")
    parser.add_argument("--apply", action="store_true",
                        help="Execute against the database instead of a dry-run.")
    parser.add_argument("--database-url", default=None,
                        help="Database URL for --apply (else ACTEOS_DATABASE_URL).")
    args = parser.parse_args(argv)

    if not args.catalog.exists():
        print(f"error: catalog not found: {args.catalog}", file=sys.stderr)
        return 1
    if not args.inbox.exists():
        print(f"error: inbox not found: {args.inbox}", file=sys.stderr)
        return 1

    scope = tuple(args.scope) if args.scope else ("R1",)
    wanted = set(args.batch) if args.batch else None

    catalog = _load_catalog(args.catalog)
    batches, schemas = _load_batches(
        args.inbox,
        args.contracts,
        wanted=wanted,
        use_schema=not args.no_schema,
    )
    if wanted and not batches:
        print(f"error: no batches matched {sorted(wanted)}", file=sys.stderr)
        return 1

    try:
        plan = build_dry_run(
            catalog,
            batches,
            scope=scope,
            schemas=schemas,
            allow_conditional=args.allow_conditional,
            strict=args.strict,
        )
    except PublishError as exc:
        print(f"PUBLISH REFUSED: {exc}", file=sys.stderr)
        if exc.report is not None and exc.report.verdict == "conditional_go":
            return 2
        return 1

    _print_plan(plan)

    if not args.apply:
        return 0

    # --- apply path: requires a real engine -------------------------------
    database_url = args.database_url or os.environ.get("ACTEOS_DATABASE_URL")
    if not database_url:
        print(
            "error: --apply requires --database-url or ACTEOS_DATABASE_URL",
            file=sys.stderr,
        )
        return 1

    from sqlalchemy import create_engine

    engine = create_engine(database_url, future=True, pool_pre_ping=True)
    event_records, bundle = compile_release(
        catalog,
        batches,
        scope=scope,
        schemas=schemas,
        allow_conditional=args.allow_conditional,
    )
    repo = SqlAlchemyContentRepository(engine)
    try:
        result = repo.publish_release(bundle, event_records, strict=args.strict)
    except ContentPublishError as exc:
        print(f"PUBLISH REFUSED: {exc}", file=sys.stderr)
        return 1

    print()
    print("=" * 72)
    print("APPLIED to content.* schema")
    print("=" * 72)
    print(f"version           : {result.version}")
    print(f"event types       : {result.event_type_count}")
    print(f"rule sets         : {result.rule_set_count}")
    print(f"rule revisions    : {result.rule_revision_count}")
    print(f"rule set members  : {result.rule_set_member_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
