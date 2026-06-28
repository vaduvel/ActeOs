"""PostgreSQL persistence adapter for the resolved case aggregate.

The ``CaseRepository`` *port* lives in ``repository.py``; this module is the
production *adapter* plus the pure statement builders / validators it relies on.

A resolved case is persisted as one logical aggregate inside one transaction:

* ``app.cases``                -- the case header + subject identity,
* ``app.journeys``             -- the immutable lossless resolution snapshot,
* ``app.journey_steps``        -- normalized derived step projection, and
* ``app.journey_requirements`` -- normalized derived requirement projection.

``app.journeys.resolution_snapshot`` remains authoritative for replay / serve.
The normalized journey tables are queryable projections derived from that
snapshot; reads still return the authoritative snapshot so a round-tripped case
is byte-identical to what the resolver produced.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Mapping
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import insert as pg_insert

from .app_tables import (
    cases,
    journey_requirements,
    journey_steps,
    journeys,
    rule_sets,
)

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
STEP_STATUSES = frozenset(
    {
        "locked",
        "available",
        "in_progress",
        "ready_to_submit",
        "submitted",
        "completed",
        "blocked",
        "needs_confirmation",
        "failed",
        "skipped_not_applicable",
    }
)
REQUIREMENT_STATUSES = frozenset(
    {"missing", "provided", "needs_review", "ready", "expired", "rejected", "not_applicable"}
)
REQUIREMENT_OBLIGATIONS = frozenset({"mandatory", "conditional", "optional"})
REQUIREMENT_TIMINGS = frozenset({"now", "later"})

_EVENT_TO_STEP_STATUS = {
    "draft": "locked",
    "needs_facts": "locked",
    "resolved": "available",
    "needs_confirmation": "needs_confirmation",
    "conflicting": "blocked",
    "blocked": "blocked",
    "completed": "completed",
    "cancelled": "blocked",
}

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
_STEP_REQUIRED = (
    "journey_id",
    "semantic_key",
    "title_ro",
    "instruction_ro",
    "sequence",
    "status",
)
_REQUIREMENT_REQUIRED = (
    "journey_step_id",
    "semantic_key",
    "title_ro",
    "obligation",
    "timing",
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


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple):
        return list(value)
    return []


def _as_string_list(value: Any) -> list[str]:
    return [str(item) for item in _as_list(value) if item is not None]


def _as_mapping(value: Any) -> Mapping[str, Any] | None:
    if isinstance(value, Mapping):
        return value
    return None


def _as_uuid_list(value: Any) -> list[str]:
    uuids: list[str] = []
    for item in _as_list(value):
        try:
            uuids.append(str(UUID(str(item))))
        except (TypeError, ValueError, AttributeError):
            continue
    return uuids


def _coerce_int(value: Any, default: int) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    return default


def _semantic_key(value: Any, fallback: str) -> str:
    if isinstance(value, str) and value:
        return value
    mapping = _as_mapping(value)
    if mapping is not None:
        for key in ("semantic_key", "id", "template_id", "key"):
            raw = mapping.get(key)
            if isinstance(raw, str) and raw:
                return raw
    return fallback


def _template_id(value: Any) -> str | None:
    mapping = _as_mapping(value)
    if mapping is None:
        return None
    raw = mapping.get("template_id")
    if isinstance(raw, str) and raw:
        return raw
    return None


def _default_step_status(event_status: Any, explicit: Any) -> str:
    if isinstance(explicit, str) and explicit in STEP_STATUSES:
        return explicit
    if isinstance(event_status, str):
        return _EVENT_TO_STEP_STATUS.get(event_status, "available")
    return "available"


def _default_requirement_status(explicit: Any) -> str:
    if isinstance(explicit, str) and explicit in REQUIREMENT_STATUSES:
        return explicit
    return "missing"


def _default_requirement_obligation(explicit: Any) -> str:
    if isinstance(explicit, str) and explicit in REQUIREMENT_OBLIGATIONS:
        return explicit
    return "mandatory"


def _default_requirement_timing(explicit: Any) -> str:
    if isinstance(explicit, str) and explicit in REQUIREMENT_TIMINGS:
        return explicit
    return "now"


def _synthetic_step_row(
    journey_id: str,
    event_key: str,
    event_status: Any,
    sequence: int,
) -> dict[str, Any]:
    semantic_key = f"{event_key}::requirements"
    return {
        "journey_id": journey_id,
        "template_id": None,
        "semantic_key": semantic_key,
        "title_ro": semantic_key,
        "instruction_ro": semantic_key,
        "sequence": sequence,
        "status": _default_step_status(event_status, None),
        "deadline": None,
        "completion_evidence_ro": [],
        "recovery_actions_ro": [],
        "source_claim_ids": [],
        "version": 1,
    }


def _build_step_row(
    journey_id: str,
    event: Mapping[str, Any],
    event_index: int,
    step_value: Any,
    sequence: int,
) -> tuple[dict[str, Any], list[Any]]:
    step = _as_mapping(step_value) or {}
    event_key = _semantic_key(event.get("event_type_id"), f"event_{event_index}")
    semantic_key = _semantic_key(step_value, f"{event_key}::step_{sequence}")
    row = {
        "journey_id": journey_id,
        "template_id": _template_id(step_value),
        "semantic_key": semantic_key,
        "title_ro": step.get("title_ro") or semantic_key,
        "instruction_ro": step.get("instruction_ro") or semantic_key,
        "sequence": _coerce_int(step.get("sequence"), sequence),
        "status": _default_step_status(event.get("status"), step.get("status")),
        "deadline": step.get("deadline"),
        "completion_evidence_ro": _as_list(step.get("completion_evidence_ro")),
        "recovery_actions_ro": _as_list(step.get("recovery_actions_ro")),
        "source_claim_ids": _as_uuid_list(step.get("source_claim_ids")),
        "version": _coerce_int(step.get("version"), 1),
    }
    return row, _as_list(step.get("requirements"))


def _build_requirement_spec(
    step_semantic_key: str,
    requirement_value: Any,
    fallback_prefix: str,
    position: int,
) -> dict[str, Any]:
    requirement = _as_mapping(requirement_value) or {}
    semantic_key = _semantic_key(requirement_value, f"{fallback_prefix}::requirement_{position}")
    return {
        "journey_step_semantic_key": step_semantic_key,
        "template_id": _template_id(requirement_value),
        "semantic_key": semantic_key,
        "title_ro": requirement.get("title_ro") or semantic_key,
        "description_ro": requirement.get("description_ro"),
        "obligation": _default_requirement_obligation(requirement.get("obligation")),
        "timing": _default_requirement_timing(requirement.get("timing")),
        "accepted_forms": _as_string_list(requirement.get("accepted_forms")),
        "validity": dict(requirement.get("validity")) if _as_mapping(requirement.get("validity")) else {},
        "readiness_checks": _as_string_list(requirement.get("readiness_checks")),
        "source_claim_ids": _as_uuid_list(requirement.get("source_claim_ids")),
        "status": _default_requirement_status(requirement.get("status")),
        "version": _coerce_int(requirement.get("version"), 1),
    }


def _bind_requirement_row(spec: Mapping[str, Any], journey_step_id: str) -> dict[str, Any]:
    return {
        "journey_step_id": journey_step_id,
        "template_id": spec.get("template_id"),
        "semantic_key": spec.get("semantic_key"),
        "title_ro": spec.get("title_ro"),
        "description_ro": spec.get("description_ro"),
        "obligation": spec.get("obligation"),
        "timing": spec.get("timing"),
        "accepted_forms": _as_string_list(spec.get("accepted_forms")),
        "validity": dict(spec.get("validity")) if _as_mapping(spec.get("validity")) else {},
        "readiness_checks": _as_string_list(spec.get("readiness_checks")),
        "source_claim_ids": _as_uuid_list(spec.get("source_claim_ids")),
        "status": _default_requirement_status(spec.get("status")),
        "version": _coerce_int(spec.get("version"), 1),
    }


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
    payload and must therefore agree with the journey header columns that are
    used for lookups, provenance, and deterministic replay.
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


def validate_step_row(row: Mapping[str, Any]) -> list[str]:
    """Return ``app.journey_steps:semantic_key:column`` invariant violations."""

    ident = row.get("semantic_key", "?")
    violations: list[str] = []
    for column in _STEP_REQUIRED:
        if row.get(column) is None:
            violations.append(f"app.journey_steps:{ident}:{column}")
    status = row.get("status")
    if status is not None and status not in STEP_STATUSES:
        violations.append(f"app.journey_steps:{ident}:status_enum({status})")
    sequence = row.get("sequence")
    if not isinstance(sequence, int) or isinstance(sequence, bool):
        violations.append(f"app.journey_steps:{ident}:sequence_int")
    return violations


def validate_requirement_row(row: Mapping[str, Any]) -> list[str]:
    """Return ``app.journey_requirements:semantic_key:column`` invariant violations."""

    ident = row.get("semantic_key", "?")
    violations: list[str] = []
    for column in _REQUIREMENT_REQUIRED:
        if row.get(column) is None:
            violations.append(f"app.journey_requirements:{ident}:{column}")
    status = row.get("status")
    if status is not None and status not in REQUIREMENT_STATUSES:
        violations.append(f"app.journey_requirements:{ident}:status_enum({status})")
    return violations


def prepare_rows(case: Mapping[str, Any], rule_set_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
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


def prepare_projection_rows(
    snapshot: Mapping[str, Any], journey_id: str
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Derive normalized step / requirement projections from a snapshot.

    The returned requirement rows are still unbound to DB step ids; they carry a
    temporary ``journey_step_semantic_key`` so ``save()`` can resolve / reuse
    the actual step id after the step INSERTs finish.
    """

    snapshot_mapping = _as_mapping(snapshot)
    if snapshot_mapping is None:
        return [], []

    step_rows: list[dict[str, Any]] = []
    requirement_specs: list[dict[str, Any]] = []
    seen_steps: set[str] = set()
    seen_requirements: set[tuple[str, str]] = set()
    next_sequence = 1

    def register_step(row: dict[str, Any]) -> str:
        nonlocal next_sequence
        semantic_key = row["semantic_key"]
        if semantic_key in seen_steps:
            return semantic_key
        row["sequence"] = _coerce_int(row.get("sequence"), next_sequence)
        next_sequence = max(next_sequence, row["sequence"] + 1)
        step_rows.append(row)
        seen_steps.add(semantic_key)
        return semantic_key

    def register_requirement(step_semantic_key: str, requirement_value: Any, position: int) -> None:
        semantic_key = _semantic_key(requirement_value, f"{step_semantic_key}::requirement_{position}")
        pair = (step_semantic_key, semantic_key)
        if pair in seen_requirements:
            return
        seen_requirements.add(pair)
        requirement_specs.append(
            _build_requirement_spec(
                step_semantic_key,
                requirement_value,
                step_semantic_key,
                position,
            )
        )

    for event_index, event_value in enumerate(_as_list(snapshot_mapping.get("events")), start=1):
        event = _as_mapping(event_value)
        if event is None:
            continue
        event_key = _semantic_key(event.get("event_type_id"), f"event_{event_index}")
        raw_steps = _as_list(event.get("included_steps"))
        raw_requirements = _as_list(event.get("requirements"))
        event_step_keys: list[str] = []

        for step_index, step_value in enumerate(raw_steps, start=1):
            step_row, nested_requirements = _build_step_row(
                journey_id,
                event,
                event_index,
                step_value,
                next_sequence,
            )
            step_key = register_step(step_row)
            event_step_keys.append(step_key)
            for requirement_index, requirement_value in enumerate(nested_requirements, start=1):
                register_requirement(step_key, requirement_value, requirement_index)

        if raw_requirements:
            if event_step_keys:
                target_step_key = event_step_keys[0]
            else:
                target_step_key = register_step(
                    _synthetic_step_row(journey_id, event_key, event.get("status"), next_sequence)
                )
            for requirement_index, requirement_value in enumerate(raw_requirements, start=1):
                register_requirement(target_step_key, requirement_value, requirement_index)

    return step_rows, requirement_specs


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


def build_journey_id_query(case_id: str, revision: int) -> Any:
    """Build the lookup query for the persisted journey primary key."""

    return (
        select(journeys.c.id)
        .where(journeys.c.case_id == case_id, journeys.c.revision == revision)
        .limit(1)
    )


def _build_journey_step_id_query(journey_id: str, semantic_key: str) -> Any:
    return (
        select(journey_steps.c.id)
        .where(
            journey_steps.c.journey_id == journey_id,
            journey_steps.c.semantic_key == semantic_key,
        )
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
        row = conn.execute(select(rule_sets.c.id).where(rule_sets.c.version == version)).first()
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

            journey_id = conn.execute(
                build_journey_id_query(str(case_row["id"]), int(journey_row["revision"]))
            ).scalar_one_or_none()
            if journey_id is None:
                raise CasePersistenceError(
                    "journey row was not readable after insert; cannot project journey_steps"
                )

            step_rows, requirement_specs = prepare_projection_rows(
                journey_row["resolution_snapshot"],
                journey_id,
            )
            step_ids: dict[str, str] = {}

            for step_row in step_rows:
                violations = validate_step_row(step_row)
                if violations:
                    raise CasePersistenceError(
                        "step rows violate app.* invariants: " + ", ".join(violations[:20])
                    )
                inserted_step_id = conn.execute(
                    pg_insert(journey_steps)
                    .values([dict(step_row)])
                    .on_conflict_do_nothing(index_elements=["journey_id", "semantic_key"])
                    .returning(journey_steps.c.id)
                ).scalar_one_or_none()
                if inserted_step_id is None:
                    inserted_step_id = conn.execute(
                        _build_journey_step_id_query(journey_id, str(step_row["semantic_key"]))
                    ).scalar_one()
                step_ids[str(step_row["semantic_key"])] = inserted_step_id

            for requirement_spec in requirement_specs:
                step_key = str(requirement_spec["journey_step_semantic_key"])
                step_id = step_ids.get(step_key)
                if step_id is None:
                    raise CasePersistenceError(
                        f"requirement projection references unknown step semantic_key '{step_key}'"
                    )
                requirement_row = _bind_requirement_row(requirement_spec, step_id)
                violations = validate_requirement_row(requirement_row)
                if violations:
                    raise CasePersistenceError(
                        "requirement rows violate app.* invariants: "
                        + ", ".join(violations[:20])
                    )
                conn.execute(
                    pg_insert(journey_requirements)
                    .values([requirement_row])
                    .on_conflict_do_nothing(index_elements=["journey_step_id", "semantic_key"])
                )
        return case

    def get(self, case_id: str) -> dict | None:
        with self._engine.connect() as conn:
            row = conn.execute(build_latest_journey_snapshot_query(case_id)).first()
        if row is None or row[0] is None:
            return None
        return dict(row[0])
