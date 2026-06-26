"""SQLAlchemy Core metadata for the publishable ``content.*`` tables.

These ``Table`` definitions mirror ``db/0001_init.sql`` exactly for the three
tables a release bundle writes: ``content.rule_sets``,
``content.rule_revisions`` and ``content.rule_set_members``. They exist only to
compile parameterized INSERT statements against the already-migrated database;
they never emit DDL (enums use ``create_type=False`` and no ForeignKey objects
are declared here -- the database owns those constraints).
"""

from __future__ import annotations

from sqlalchemy import CHAR, Column, Date, DateTime, Integer, MetaData, Table, Text
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, JSONB, UUID

metadata = MetaData()

_UUID = UUID(as_uuid=False)

# content.* enum types (already created by db/0001_init.sql).
ruleset_status = ENUM(
    "draft",
    "validating",
    "approved",
    "active",
    "superseded",
    "withdrawn",
    name="ruleset_status",
    schema="content",
    create_type=False,
)
review_status = ENUM(
    "draft",
    "in_review",
    "approved",
    "active",
    "stale",
    "hard_expired",
    "withdrawn",
    "superseded",
    "conflicting",
    name="review_status",
    schema="content",
    create_type=False,
)
freshness_class = ENUM(
    "critical",
    "operational",
    "explanatory",
    name="freshness_class",
    schema="content",
    create_type=False,
)

rule_sets = Table(
    "rule_sets",
    metadata,
    Column("id", _UUID, primary_key=True),
    Column("version", Text, nullable=False, unique=True),
    Column("scope", ARRAY(Text), nullable=False),
    Column("schema_version", Text, nullable=False),
    Column("engine_compatibility", Text, nullable=False),
    Column("manifest_sha256", CHAR(64), nullable=False, unique=True),
    Column("status", ruleset_status, nullable=False),
    Column("approved_by", ARRAY(_UUID), nullable=False),
    Column("published_by", _UUID),
    Column("published_at", DateTime(timezone=True)),
    Column("supersedes_ruleset_id", _UUID),
    Column("created_at", DateTime(timezone=True)),
    schema="content",
)

rule_revisions = Table(
    "rule_revisions",
    metadata,
    Column("id", _UUID, primary_key=True),
    Column("canonical_rule_id", Text, nullable=False),
    Column("revision", Integer, nullable=False),
    Column("event_type_id", Text, nullable=False),
    Column("jurisdiction_ids", ARRAY(Text), nullable=False),
    Column("authority_level", Text, nullable=False),
    Column("competence_scope", ARRAY(Text), nullable=False),
    Column("legal_rank", Text),
    Column("severity", freshness_class, nullable=False),
    Column("effective_from", Date, nullable=False),
    Column("effective_to", Date),
    Column("predicate", JSONB, nullable=False),
    Column("effects", JSONB, nullable=False),
    Column("source_claim_ids", ARRAY(_UUID), nullable=False),
    Column("override_rule_ids", ARRAY(_UUID), nullable=False),
    Column("status", review_status, nullable=False),
    Column("created_by", _UUID),
    Column("reviewed_by", _UUID),
    Column("approved_at", DateTime(timezone=True)),
    Column("created_at", DateTime(timezone=True)),
    schema="content",
)

rule_set_members = Table(
    "rule_set_members",
    metadata,
    Column("rule_set_id", _UUID, primary_key=True),
    Column("rule_revision_id", _UUID, primary_key=True),
    schema="content",
)
