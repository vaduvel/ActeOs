"""SQLAlchemy Core metadata for the publishable ``content.*`` tables.

These ``Table`` definitions mirror ``db/0001_init.sql`` exactly for the tables a
release writes: ``content.life_event_types`` (FK parent), the reusable content
templates ``content.step_templates`` / ``content.requirement_templates``,
``content.rule_sets`` / ``content.rule_revisions`` / ``content.rule_set_members``,
and the provenance chain ``content.sources`` / ``content.source_snapshots`` /
``content.source_claims``.
They exist only to compile parameterized INSERT statements against the
already-migrated database; they never emit DDL (enums use ``create_type=False``
and no ForeignKey objects are declared here -- the database owns those
constraints).
"""

from __future__ import annotations

from sqlalchemy import (
    CHAR,
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    MetaData,
    Table,
    Text,
)
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

life_event_types = Table(
    "life_event_types",
    metadata,
    Column("id", Text, primary_key=True),
    Column("category_id", Text),
    Column("title_ro", Text, nullable=False),
    Column("description_ro", Text),
    Column("trigger_phrases_ro", JSONB),
    Column("parent_event_id", Text),
    Column("release_wave", Text),
    Column("research_status", Text),
    Column("production_status", Text),
    Column("schema_version", Text),
    schema="content",
)

step_templates = Table(
    "step_templates",
    metadata,
    Column("id", Text, primary_key=True),
    Column("semantic_key", Text, nullable=False),
    Column("title_ro", Text, nullable=False),
    Column("instruction_ro", Text, nullable=False),
    Column("sequence_hint", Integer, nullable=False),
    Column("completion_evidence_ro", JSONB),
    Column("recovery_actions_ro", JSONB),
    Column("status", Text, nullable=False),
    schema="content",
)

requirement_templates = Table(
    "requirement_templates",
    metadata,
    Column("id", Text, primary_key=True),
    Column("title_ro", Text, nullable=False),
    Column("description_ro", Text),
    Column("obligation", Text, nullable=False),
    Column("timing", Text, nullable=False),
    Column("accepted_forms", ARRAY(Text), nullable=False),
    Column("validity", JSONB),
    Column("readiness_checks", ARRAY(Text), nullable=False),
    Column("status", Text, nullable=False),
    schema="content",
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

# --- Provenance chain (db/0001_init.sql). Written only when real sources and
# snapshots are authored; the publish adapter gates on that, so these tables are
# present and ready but receive no rows until provenance lands. ----------------
sources = Table(
    "sources",
    metadata,
    Column("id", _UUID, primary_key=True),
    Column("canonical_url", Text, nullable=False, unique=True),
    Column("publisher", Text, nullable=False),
    Column("authority_level", Text, nullable=False),
    Column("legal_rank", Text),
    Column("territory_ids", ARRAY(Text), nullable=False),
    Column("competence_scope", ARRAY(Text), nullable=False),
    Column("fetch_mode", Text, nullable=False),
    Column("allowed_to_fetch", Boolean, nullable=False),
    Column("status", Text, nullable=False),
    Column("last_checked_at", DateTime(timezone=True)),
    Column("next_check_at", DateTime(timezone=True)),
    Column("created_by", _UUID),
    Column("created_at", DateTime(timezone=True)),
    Column("updated_at", DateTime(timezone=True)),
    schema="content",
)

source_snapshots = Table(
    "source_snapshots",
    metadata,
    Column("id", _UUID, primary_key=True),
    Column("source_id", _UUID, nullable=False),
    Column("captured_at", DateTime(timezone=True), nullable=False),
    Column("http_status", Integer),
    Column("content_type", Text),
    Column("storage_object_key", Text),
    Column("normalized_text_object_key", Text),
    Column("sha256", CHAR(64), nullable=False),
    Column("etag", Text),
    Column("last_modified", Text),
    Column("previous_snapshot_id", _UUID),
    Column("change_detected", Boolean, nullable=False),
    Column("change_summary", JSONB),
    Column("status", Text, nullable=False),
    schema="content",
)

source_claims = Table(
    "source_claims",
    metadata,
    Column("id", _UUID, primary_key=True),
    Column("stable_key", Text, nullable=False),
    Column("source_id", _UUID, nullable=False),
    Column("snapshot_id", _UUID, nullable=False),
    Column("statement", Text, nullable=False),
    Column("evidence_excerpt", Text, nullable=False),
    Column("locator", Text, nullable=False),
    Column("authority_level", Text, nullable=False),
    Column("legal_rank", Text),
    Column("territory_ids", ARRAY(Text)),
    Column("competence_scope", ARRAY(Text)),
    Column("published_at", Date),
    Column("accessed_at", Date, nullable=False),
    Column("effective_from", Date),
    Column("effective_to", Date),
    Column("confidence", Text, nullable=False),
    Column("freshness_class", freshness_class, nullable=False),
    Column("review_due_at", Date),
    Column("hard_expiry_at", Date),
    Column("status", review_status, nullable=False),
    Column("created_by", _UUID),
    Column("reviewed_by", _UUID),
    Column("approved_at", DateTime(timezone=True)),
    Column("supersedes_claim_id", _UUID),
    Column("created_at", DateTime(timezone=True)),
    Column("updated_at", DateTime(timezone=True)),
    schema="content",
)
