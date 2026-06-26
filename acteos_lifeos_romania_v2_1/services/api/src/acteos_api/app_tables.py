"""SQLAlchemy Core metadata for the ``app.*`` tables a case write touches.

Mirrors ``db/0001_init.sql`` + ``db/0002_case_resolution_snapshot.sql`` for the
two tables the case aggregate persists -- ``app.cases`` and ``app.journeys`` --
plus a read-only view of ``content.rule_sets`` used to resolve a served
``ruleset_version`` to its persisted id. Like ``content_tables``, these never
emit DDL (enums use ``create_type=False`` and no ForeignKey objects are declared
here -- the migrated database owns those constraints). They exist only to
compile parameterized INSERT/SELECT statements against the already-migrated
database.
"""

from __future__ import annotations

from sqlalchemy import CHAR, Column, Date, DateTime, Integer, MetaData, Table, Text
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, JSONB, UUID

metadata = MetaData()

_UUID = UUID(as_uuid=False)

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

cases = Table(
    "cases",
    metadata,
    Column("id", _UUID, primary_key=True),
    Column("user_id", _UUID),
    Column("installation_id", _UUID),
    Column("event_type_id", Text, nullable=False),
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
    Column("id", _UUID, primary_key=True),
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

# Read-only: resolve a served ruleset_version to its persisted rule_set id.
rule_sets = Table(
    "rule_sets",
    metadata,
    Column("id", _UUID, primary_key=True),
    Column("version", Text, nullable=False),
    schema="content",
)
