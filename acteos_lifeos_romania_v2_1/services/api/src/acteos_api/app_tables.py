"""SQLAlchemy Core metadata for the ``app.*`` tables a case write touches.

Mirrors ``db/0001_init.sql`` + later additive migrations for the case aggregate:

* ``app.cases``
* ``app.journeys``
* ``app.journey_steps``
* ``app.journey_requirements``

plus a read-only view of ``content.rule_sets`` used to resolve a served
``ruleset_version`` to its persisted id. Like ``content_tables``, these never
emit DDL (enums use ``create_type=False`` and no ForeignKey objects are declared
here -- the migrated database owns those constraints). They exist only to
compile parameterized INSERT/SELECT statements against the already-migrated
database. The ``id`` ``server_default``s mirror the schema's
``gen_random_uuid()`` so the insert compiler treats an omitted primary key as
DB-generated instead of a missing value.
"""

from __future__ import annotations

from sqlalchemy import CHAR, Column, Date, DateTime, Integer, LargeBinary, MetaData, Table, Text, text
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, JSONB, UUID

metadata = MetaData()

_UUID = UUID(as_uuid=False)
_GEN_UUID = text("gen_random_uuid()")

# app.* enum types (already created by db/0001_init.sql).
case_status = ENUM(
    "draft",
    "needs_facts",
    "resolved",
    "needs_confirmation",
    "conflicting",
    "blocked",
    "completed",
    "cancelled",
    name="case_status",
    schema="app",
    create_type=False,
)
journey_status = ENUM(
    "active",
    "needs_review",
    "completed",
    "cancelled",
    "archived",
    "blocked",
    name="journey_status",
    schema="app",
    create_type=False,
)
step_status = ENUM(
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
    name="step_status",
    schema="app",
    create_type=False,
)
requirement_status = ENUM(
    "missing",
    "provided",
    "needs_review",
    "ready",
    "expired",
    "rejected",
    "not_applicable",
    name="requirement_status",
    schema="app",
    create_type=False,
)

cases = Table(
    "cases",
    metadata,
    Column("id", _UUID, primary_key=True, server_default=_GEN_UUID),
    Column("user_id", _UUID),
    Column("installation_id", _UUID),
    # ``event_type_id`` became nullable in db/0004_intent_discovery.sql. A case is
    # valid when either ``intent_type_id`` (intent-first discovery) or
    # ``event_type_id`` (legacy event-first) is present -- enforced in the DB by
    # app.cases.case_intent_or_legacy_event_ck.
    Column("event_type_id", Text),
    Column("intent_type_id", Text),
    Column("event_context_ids", ARRAY(Text), nullable=False),
    Column("discovery_source", Text),
    Column("subject_ref", Text),
    Column("reference_date", Date, nullable=False),
    Column("timezone", Text, nullable=False),
    Column("jurisdiction_path", ARRAY(Text), nullable=False),
    Column("status", case_status, nullable=False),
    Column("version", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True)),
    Column("updated_at", DateTime(timezone=True)),
    schema="app",
)

journeys = Table(
    "journeys",
    metadata,
    Column("id", _UUID, primary_key=True, server_default=_GEN_UUID),
    Column("case_id", _UUID, nullable=False),
    Column("revision", Integer, nullable=False),
    Column("previous_journey_id", _UUID),
    Column("rule_set_id", _UUID, nullable=False),
    Column("ruleset_version", Text, nullable=False),
    Column("reference_date", Date, nullable=False),
    Column("facts_hash", CHAR(64), nullable=False),
    Column("engine_version", Text, nullable=False),
    Column("status", journey_status, nullable=False),
    Column("trust_state", Text, nullable=False),
    Column("resolution_trace", JSONB, nullable=False),
    Column("resolution_snapshot", JSONB, nullable=False),
    Column("created_at", DateTime(timezone=True)),
    Column("archived_at", DateTime(timezone=True)),
    schema="app",
)

journey_steps = Table(
    "journey_steps",
    metadata,
    Column("id", _UUID, primary_key=True, server_default=_GEN_UUID),
    Column("journey_id", _UUID, nullable=False),
    Column("template_id", Text),
    Column("semantic_key", Text, nullable=False),
    Column("title_ro", Text, nullable=False),
    Column("instruction_ro", Text, nullable=False),
    Column("sequence", Integer, nullable=False),
    Column("status", step_status, nullable=False),
    Column("deadline", JSONB),
    Column("completion_evidence_ro", JSONB, nullable=False),
    Column("recovery_actions_ro", JSONB, nullable=False),
    Column("source_claim_ids", ARRAY(_UUID), nullable=False),
    Column("user_note_ciphertext", LargeBinary),
    Column("version", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True)),
    Column("updated_at", DateTime(timezone=True)),
    schema="app",
)

journey_requirements = Table(
    "journey_requirements",
    metadata,
    Column("id", _UUID, primary_key=True, server_default=_GEN_UUID),
    Column("journey_step_id", _UUID, nullable=False),
    Column("template_id", Text),
    Column("semantic_key", Text, nullable=False),
    Column("title_ro", Text, nullable=False),
    Column("description_ro", Text),
    Column("obligation", Text, nullable=False),
    Column("timing", Text, nullable=False),
    Column("accepted_forms", ARRAY(Text), nullable=False),
    Column("validity", JSONB, nullable=False),
    Column("readiness_checks", ARRAY(Text), nullable=False),
    Column("source_claim_ids", ARRAY(_UUID), nullable=False),
    Column("status", requirement_status, nullable=False),
    Column("version", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True)),
    Column("updated_at", DateTime(timezone=True)),
    schema="app",
)

# Read-only: resolve a served ruleset_version to its persisted rule_set id.
rule_sets = Table(
    "rule_sets",
    metadata,
    Column("id", _UUID, primary_key=True),
    Column("version", Text, nullable=False),
    schema="content",
)
