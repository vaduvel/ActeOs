"""Publish a compiled release bundle into the ``content.*`` schema.

This is the production persistence adapter behind a port. It consumes
``PublishedBundle.as_content_rows()`` from the engine's publish compiler and:

1. enforces the database NOT NULL invariants *before* touching the DB
   (``validate_content_rows``), so a malformed bundle is refused with a clear
   message instead of a raw IntegrityError;
2. builds ordered, idempotent ``INSERT ... ON CONFLICT DO NOTHING`` statements in
   FK-safe order (rule_sets -> rule_revisions -> rule_set_members);
3. executes them inside a single transaction via a SQLAlchemy ``Engine``.

The statement-building and validation are pure and unit tested without a live
database; only :meth:`SqlAlchemyContentRepository.publish` needs a real engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import insert as pg_insert

from acteos_rule_engine.authoring.publish import PublishedBundle

from .content_tables import rule_revisions, rule_set_members, rule_sets


class ContentPublishError(RuntimeError):
    """Raised when a bundle cannot be safely written to the content schema."""


# NOT NULL columns we populate per table (db/0001_init.sql). Columns with DB
# defaults (created_at, status defaults) or nullable columns are omitted.
REQUIRED_NOT_NULL: dict[str, tuple[str, ...]] = {
    "content.rule_sets": (
        "id",
        "version",
        "scope",
        "schema_version",
        "engine_compatibility",
        "manifest_sha256",
        "status",
        "approved_by",
    ),
    "content.rule_revisions": (
        "id",
        "canonical_rule_id",
        "revision",
        "event_type_id",
        "jurisdiction_ids",
        "authority_level",
        "competence_scope",
        "severity",
        "effective_from",
        "predicate",
        "effects",
        "source_claim_ids",
        "override_rule_ids",
        "status",
    ),
    "content.rule_set_members": (
        "rule_set_id",
        "rule_revision_id",
    ),
}


def validate_content_rows(rows: Mapping[str, list[dict[str, Any]]]) -> list[str]:
    """Return a list of ``table:identity:column`` NOT NULL violations."""

    violations: list[str] = []
    for table, required in REQUIRED_NOT_NULL.items():
        for index, row in enumerate(rows.get(table, [])):
            ident = (
                row.get("id")
                or row.get("canonical_rule_id")
                or row.get("version")
                or f"#{index}"
            )
            for column in required:
                if row.get(column) is None:
                    violations.append(f"{table}:{ident}:{column}")
    return violations


@dataclass(frozen=True)
class PublishResult:
    version: str
    manifest_sha256: str
    rule_set_count: int
    rule_revision_count: int
    rule_set_member_count: int


def build_publish_statements(
    bundle: PublishedBundle,
    *,
    strict: bool = True,
    validate: bool = True,
) -> list[Any]:
    """Build ordered, idempotent INSERT statements for a bundle."""

    rows = bundle.as_content_rows(strict=strict)
    if validate:
        violations = validate_content_rows(rows)
        if violations:
            raise ContentPublishError(
                "content rows violate NOT NULL invariants: "
                + ", ".join(violations[:20])
                + (" ..." if len(violations) > 20 else "")
            )

    statements: list[Any] = []
    if rows["content.rule_sets"]:
        statements.append(
            pg_insert(rule_sets)
            .values(rows["content.rule_sets"])
            .on_conflict_do_nothing(index_elements=["manifest_sha256"])
        )
    if rows["content.rule_revisions"]:
        statements.append(
            pg_insert(rule_revisions)
            .values(rows["content.rule_revisions"])
            .on_conflict_do_nothing(index_elements=["canonical_rule_id", "revision"])
        )
    if rows["content.rule_set_members"]:
        statements.append(
            pg_insert(rule_set_members)
            .values(rows["content.rule_set_members"])
            .on_conflict_do_nothing()
        )
    return statements


def compiled_sql(bundle: PublishedBundle, *, strict: bool = True) -> list[str]:
    """Render the Postgres SQL for the bundle's INSERTs (dry-run / ops)."""

    return [
        str(stmt.compile(dialect=postgresql.dialect()))
        for stmt in build_publish_statements(bundle, strict=strict)
    ]


class ContentRepository(Protocol):
    def publish(self, bundle: PublishedBundle) -> PublishResult: ...


class SqlAlchemyContentRepository:
    """Writes a release bundle to the content schema in one transaction."""

    def __init__(self, engine: Any) -> None:
        self._engine = engine

    def publish(self, bundle: PublishedBundle, *, strict: bool = True) -> PublishResult:
        rows = bundle.as_content_rows(strict=strict)
        statements = build_publish_statements(bundle, strict=strict)
        with self._engine.begin() as conn:
            for stmt in statements:
                conn.execute(stmt)
        return PublishResult(
            version=bundle.version,
            manifest_sha256=bundle.manifest_sha256,
            rule_set_count=len(rows["content.rule_sets"]),
            rule_revision_count=len(rows["content.rule_revisions"]),
            rule_set_member_count=len(rows["content.rule_set_members"]),
        )

    def compiled_sql(self, bundle: PublishedBundle, *, strict: bool = True) -> list[str]:
        return compiled_sql(bundle, strict=strict)
