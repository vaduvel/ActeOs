"""PostgreSQL persistence adapter for the resolved case aggregate.

The ``CaseRepository`` *port* lives in ``repository.py``; this module is the
production *adapter* plus the pure statement builders / validators it relies on.

A resolved case is persisted as two rows inside one transaction:

* ``app.cases``     -- the case header + subject identity, and
* ``app.journeys``  -- revision 1: the immutable resolution snapshot.

The full engine resolution (``events`` + ``resolution_trace``) is stored
losslessly in ``app.journeys.resolution_snapshot`` (jsonb); the normalized
``journey_steps`` / ``journey_requirements`` projection is a later slice. Reads
return the authoritative snapshot, so a round-tripped case is byte-identical to
what the resolver produced.

Statement building and validation are pure and unit-tested without a live
database; only ``save`` / ``get`` need a real SQLAlchemy ``Engine``.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Mapping

from sqlalchemy import select
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import insert as pg_insert

from .app_tables import cases, journeys, rule_sets

# app.case_status / app.journey_status enum labels (db/0001_init.sql).
CASE_STATUSES = frozenset(
    {
        "draft",
        "needs_facts",
        "resolved",
        "needs_confirmation",
        "conflicting",
        "blocked",
        "completed",
        "cancelled",
    }
)
JOURNEY_STATUSES = frozenset(
    {"active", "needs_review", "completed", "cancelled", "archived", "blocked"}
)

_CASE_REQUIRED = ("event_type_id", "reference_date", "jurisdiction_path", "status", "version")
_JOURNEY_REQUIRED = (
    "case_id",
    "revision",
    "rule_set_id",
    "ruleset_version",
    "reference_date",
    "facts_hash",
    "engine_version",
    "trust_state",
    "resolution_trace",
    "resolution_snapshot",
    "status",
)


class CasePersistenceError(RuntimeError):
    """Raised when a case cannot be safely written to the ``app.*`` schema."""


def _as_date(value: Any) -> Any:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value)
    return value


def _iso_date(value: Any) -> Any:
    if isinstance(value, date):
        return value.isoformat()
    return value


def validate_case_row(row: Mapping[str, Any]) -> list[str]:
    """Return ``app.cases:identity:column`` invariant violations."""

    ident = row.get("id", "?")
    violations: list[str] = []
    # app.cases.case_identity_ck: user_id is not null OR installation_id is not null
    if not row.get("user_id") and not row.get("installation_id"):
        violations.append(f"app.cases:{ident}:identity(user_id|installation_id)")
    for column in _CASE_REQUIRED:
        if row.get(column) is None:
            violations.append(f"app.cases:{ident}:{column}")
    status = row.get("status")
    if status is not None and status not in CASE_STATUSES:
        violations.append(f"app.cases:{ident}:status_enum({status})")
    return violations


def validate_resolution_snapshot(row: Mapping[str, Any]) -> list[str]:
    """Return violations for the journey's lossless replay snapshot.

    ``app.journeys.resolution_snapshot`` is the authoritative replay/serve
    payload until the normalized projection is materialized. It must therefore
    agree with the journey header columns that are used for lookups, provenance,
    and deterministic replay.
    """

    ident = row.get("case_id", "?")
    snapshot = row.get("resolution_snapshot")
    violations: list[str] = []
    if snapshot is None:
        return violations
    if not isinstance(snapshot, Mapping):
        return [f"app.journeys:{ident}:resolution_snapshot_object"]

    expected_pairs = (
        ("id", "case_id"),
        ("version", "revision"),
        ("reference_date", "reference_date"),
        ("facts_hash", "facts_hash"),
        ("engine_version", "engine_version"),
        ("ruleset_version", "ruleset_version"),
    )
    for snapshot_key, row_key in expected_pairs:
        snapshot_value = _iso_date(snapshot.get(snapshot_key))
        row_value = _iso_date(row.get(row_key))
        if snapshot_value != row_value:
            violations.append(
                f"app.journeys:{ident}:snapshot_{snapshot_key}_mismatch"
                f"({snapshot_value}!={row_value})"
            )

    trace = snapshot.get("resolution_trace")
    if not isinstance(trace, Mapping):
        violations.append(f"app.journeys:{ident}:snapshot_resolution_trace_object")
    else:
        for key in ("facts_hash", "engine_version", "ruleset_version"):
            if trace.get(key) != snapshot.get(key):
                violations.append(f"app.journeys:{ident}:trace_{key}_mismatch")

    events = snapshot.get("events")
    if not isinstance(events, list):
        violations.append(f"app.journeys:{ident}:snapshot_events_array")
    return violations


def validate_journey_row(row: Mapping[str, Any]) -> list[str]:
    """Return ``app.journeys:case_id:column`` invariant violations."""

    ident = row.get("case_id", "?")
    violations: list[str] = []
    for column in _JOURNEY_REQUIRED:
        if row.get(column) is None:
            violations.append(f"app.journeys:{ident}:{column}")
    status = row.get("status")
    if status is not None and status not in JOURNEY_STATUSES:
        violations.append(f"app.journeys:{ident}:status_enum({status})")
    facts_hash = row.get("facts_hash")
    if isinstance(facts_hash, str) and len(facts_hash) != 64:
        violations.append(f"app.journeys:{ident}:facts_hash_len({len(facts_hash)})")
    violations.extend(validate_resolution_snapshot(row))
    return violations


def prepare_rows(case: Mapping[str, Any], rule_set_id: str) -> tuple[dict, dict]:
    """Project a resolved case dict into (app.cases row, app.journeys row).

    ``created_at`` / ``updated_at`` and the journey ``id`` are intentionally
    omitted so the database defaults (``now()`` / ``gen_random_uuid()``) apply.
    """

    reference_date = _as_date(case.get("reference_date"))
    case_row = {
        "id": case.get("id"),
        "user_id": case.get("user_id"),
        "installation_id": case.get("installation_id"),
        "event_type_id": case.get("event_type_id"),
        "subject_ref": case.get("subject_ref"),
        "reference_date": reference_date,
        "timezone": case.get("timezone", "Europe/Bucharest"),
        "jurisdiction_path": list(case.get("jurisdiction_path", [])),
        "status": case.get("status"),
        "version": case.get("version", 1),
    }
    journey_row = {
        "case_id": case.get("id"),
        "revision": case.get("version", 1),
        "rule_set_id": rule_set_id,
        "ruleset_version": case.get("ruleset_version"),
        "reference_date": reference_date,
        "facts_hash": case.get("facts_hash"),
        "engine_version": case.get("engine_version"),
        "status": "active",
        "trust_state": case.get("trust_state", "trusted"),
        "resolution_trace": case.get("resolution_trace"),
        "resolution_snapshot": dict(case),
    }
    return case_row, journey_row


def build_case_statements(
    case_row: Mapping[str, Any],
    journey_row: Mapping[str, Any],
    *,
    validate: bool = True,
) -> list[Any]:
    """Build the ordered, append-only INSERTs for a case + its journey.

    Duplicate case ids or duplicate ``(case_id, revision)`` journey rows are not
    updated in place. The database unique constraints enforce the append-only
    journey model; a later revision must be written with a higher revision.
    """

    if validate:
        violations = validate_case_row(case_row) + validate_journey_row(journey_row)
        if violations:
            raise CasePersistenceError(
                "case rows violate app.* invariants: " + ", ".join(violations[:20])
            )
    return [
        pg_insert(cases).values([dict(case_row)]).on_conflict_do_nothing(index_elements=["id"]),
        pg_insert(journeys)
        .values([dict(journey_row)])
        .on_conflict_do_nothing(index_elements=["case_id", "revision"]),
    ]


def build_latest_journey_snapshot_query(case_id: str) -> Any:
    """Build the replay query: latest journey snapshot for one case id."""

    return (
        select(journeys.c.resolution_snapshot)
        .where(journeys.c.case_id == case_id)
        .order_by(journeys.c.revision.desc())
        .limit(1)
    )


def compiled_case_sql(case_row: Mapping[str, Any], journey_row: Mapping[str, Any]) -> list[str]:
    """Render the Postgres SQL for the case + journey INSERTs (dry-run / ops)."""

    return [
        str(stmt.compile(dialect=postgresql.dialect()))
        for stmt in build_case_statements(case_row, journey_row)
    ]


def compiled_latest_journey_sql(case_id: str) -> str:
    """Render the Postgres replay SELECT for dry-run / regression tests."""

    return str(build_latest_journey_snapshot_query(case_id).compile(dialect=postgresql.dialect()))


class SqlAlchemyCaseRepository:
    """Persists the resolved case aggregate to ``app.*`` in one transaction."""

    def __init__(self, engine: Any) -> None:
        self._engine = engine

    def _resolve_rule_set_id(self, conn: Any, version: str | None) -> str:
        if not version:
            raise CasePersistenceError("case is missing ruleset_version; cannot resolve rule_set_id")
        row = conn.execute(
            select(rule_sets.c.id).where(rule_sets.c.version == version)
        ).first()
        if row is None:
            raise CasePersistenceError(
                f"ruleset_version '{version}' is not published to content.rule_sets; "
                "publish the release before persisting cases against it"
            )
        return row[0]

    def save(self, case: dict) -> dict:
        with self._engine.begin() as conn:
            rule_set_id = self._resolve_rule_set_id(conn, case.get("ruleset_version"))
            case_row, journey_row = prepare_rows(case, rule_set_id)
            for stmt in build_case_statements(case_row, journey_row):
                conn.execute(stmt)
        return case

    def get(self, case_id: str) -> dict | None:
        with self._engine.connect() as conn:
            row = conn.execute(build_latest_journey_snapshot_query(case_id)).first()
        if row is None or row[0] is None:
            return None
        return dict(row[0])
