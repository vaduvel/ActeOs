"""SQLAlchemy 2.0 ORM mapping for the canonical PostgreSQL schema.

This maps the tables defined in `migrations/versions/0001_initial.py` (which
mirrors `docs/product/waze-birocratie/09_DATABASE_SCHEMA.sql`). The Alembic
migration is the source of truth for DDL; these classes are the typed read/write
surface used by repositories and services. Postgres-only by design (ADR-003):
native enums, JSONB, arrays, bytea, partial unique indexes.

Conventions:
- UUIDs are surfaced as ``str`` (``as_uuid=False``) so they serialize directly
  into JSON contracts and bind into engine fact hashing without conversion.
- Encrypted columns are ``bytea`` holding the self-describing ``wbenc:`` token
  produced by :mod:`wb_api.crypto`. Raw citizen data is never stored in clear.
- Enum columns reference the already-created Postgres enum types
  (``create_type=False``); the migration owns their lifecycle.
"""
from __future__ import annotations

import datetime as _dt

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, BYTEA, ENUM, JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

_UTC_NOW = text("timezone('utc', now())")
_GEN_UUID = text("gen_random_uuid()")


class Base(DeclarativeBase):
    pass


def _enum(name: str, schema: str, *values: str) -> ENUM:
    """Reference an existing Postgres enum type without managing its DDL."""
    return ENUM(*values, name=name, schema=schema, create_type=False)


# --- enum type handles (values mirror the migration) -------------------------
SOURCE_STATUS = _enum("source_status", "content", "active", "paused", "retired")
AUTHORITY_LEVEL = _enum(
    "authority_level", "content", "eu", "national_normative",
    "national_operational", "county", "uat", "institution", "signal_only",
)
FRESHNESS_CLASS = _enum("freshness_class", "content", "critical", "operational", "explanatory")
SNAPSHOT_STATUS = _enum("snapshot_status", "content", "fetched", "unchanged", "changed", "failed", "blocked")
RULE_STATUS = _enum(
    "rule_status", "content", "draft", "in_review", "changes_requested",
    "approved", "rejected", "published", "retired",
)
CONFIDENCE_STATE = _enum(
    "confidence_state", "content", "verified", "verified_with_local_gap",
    "needs_confirmation", "conflicting", "expired",
)
RELEASE_STATUS = _enum("release_status", "content", "preview", "production", "retired")
JOURNEY_STATUS = _enum("journey_status", "app", "active", "completed", "archived")
REQUIREMENT_STATUS = _enum(
    "requirement_status", "app", "not_started", "ready", "blocked",
    "in_progress", "submitted", "completed", "not_applicable",
)
FINDING_SEVERITY = _enum("finding_severity", "app", "blocking", "warning", "info", "unknown")
FINDING_STATUS = _enum("finding_status", "app", "detected", "not_detected", "unable_to_check")
JOB_STATUS = _enum("job_status", "ops", "queued", "running", "succeeded", "failed", "cancelled")
INCIDENT_STATUS = _enum("incident_status", "ops", "new", "triaged", "investigating", "resolved", "dismissed")


def _uuid_pk() -> Mapped[str]:
    return mapped_column(UUID(as_uuid=False), primary_key=True, server_default=_GEN_UUID)


# =========================== content schema ================================
class Jurisdiction(Base):
    __tablename__ = "jurisdiction"
    __table_args__ = {"schema": "content"}

    id: Mapped[str] = _uuid_pk()
    parent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("content.jurisdiction.id"), nullable=True)
    code: Mapped[str] = mapped_column(Text, unique=True)
    name: Mapped[str] = mapped_column(Text)
    kind: Mapped[str] = mapped_column(Text)
    timezone: Mapped[str] = mapped_column(Text, server_default=text("'Europe/Bucharest'"))
    meta: Mapped[dict] = mapped_column("metadata", JSONB, server_default=text("'{}'::jsonb"))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    updated_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


class Authority(Base):
    __tablename__ = "authority"
    __table_args__ = {"schema": "content"}

    id: Mapped[str] = _uuid_pk()
    jurisdiction_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("content.jurisdiction.id"), nullable=True)
    code: Mapped[str] = mapped_column(Text, unique=True)
    official_name: Mapped[str] = mapped_column(Text)
    authority_level: Mapped[str] = mapped_column(AUTHORITY_LEVEL)
    official_domains: Mapped[list[str]] = mapped_column(ARRAY(Text), server_default=text("'{}'"))
    meta: Mapped[dict] = mapped_column("metadata", JSONB, server_default=text("'{}'::jsonb"))
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    updated_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


class Intent(Base):
    __tablename__ = "intent"
    __table_args__ = {"schema": "content"}

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    category: Mapped[str] = mapped_column(Text)
    title_ro: Mapped[str] = mapped_column(Text)
    description_ro: Mapped[str] = mapped_column(Text)
    keywords_ro: Mapped[list[str]] = mapped_column(ARRAY(Text), server_default=text("'{}'"))
    release_status: Mapped[str] = mapped_column(RELEASE_STATUS, server_default=text("'preview'"))
    owner_team: Mapped[str] = mapped_column(Text)
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    updated_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


class Source(Base):
    __tablename__ = "source"
    __table_args__ = {"schema": "content"}

    id: Mapped[str] = _uuid_pk()
    authority_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("content.authority.id"), nullable=True)
    jurisdiction_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("content.jurisdiction.id"), nullable=True)
    canonical_url: Mapped[str] = mapped_column(Text, unique=True)
    title: Mapped[str] = mapped_column(Text)
    publisher: Mapped[str] = mapped_column(Text)
    authority_level: Mapped[str] = mapped_column(AUTHORITY_LEVEL)
    status: Mapped[str] = mapped_column(SOURCE_STATUS, server_default=text("'active'"))
    freshness_class: Mapped[str] = mapped_column(FRESHNESS_CLASS)
    review_interval_days: Mapped[int] = mapped_column(Integer)
    robots_policy: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb"))
    fetch_policy: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb"))
    last_fetched_at: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_verified_at: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_review_at: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    consecutive_failures: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    created_by: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    updated_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


class SourceSnapshot(Base):
    __tablename__ = "source_snapshot"
    __table_args__ = {"schema": "content"}

    id: Mapped[str] = _uuid_pk()
    source_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.source.id"))
    fetched_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(SNAPSHOT_STATUS)
    http_status: Mapped[int | None] = mapped_column(Integer, nullable=True)
    final_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_type: Mapped[str | None] = mapped_column(Text, nullable=True)
    etag: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_modified: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_sha256: Mapped[str | None] = mapped_column(Text, nullable=True)
    normalized_sha256: Mapped[str | None] = mapped_column(Text, nullable=True)
    storage_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    extraction_metadata: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb"))
    error_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


class SourceClaim(Base):
    __tablename__ = "source_claim"
    __table_args__ = {"schema": "content"}

    id: Mapped[str] = _uuid_pk()
    source_snapshot_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.source_snapshot.id"))
    stable_key: Mapped[str] = mapped_column(Text)
    claim_text: Mapped[str] = mapped_column(Text)
    evidence_excerpt: Mapped[str] = mapped_column(Text)
    locator: Mapped[dict] = mapped_column(JSONB)
    jurisdiction_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("content.jurisdiction.id"), nullable=True)
    effective_from: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    effective_to: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    confidence: Mapped[str] = mapped_column(CONFIDENCE_STATE)
    extracted_by: Mapped[str] = mapped_column(Text)
    verified_by: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    verified_at: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


class RuleFamily(Base):
    __tablename__ = "rule_family"
    __table_args__ = {"schema": "content"}

    id: Mapped[str] = _uuid_pk()
    stable_id: Mapped[str] = mapped_column(Text, unique=True)
    intent_id: Mapped[str] = mapped_column(Text, ForeignKey("content.intent.id"))
    jurisdiction_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.jurisdiction.id"))
    title: Mapped[str] = mapped_column(Text)
    risk_class: Mapped[str] = mapped_column(Text)
    owner_team: Mapped[str] = mapped_column(Text)
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    updated_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


class RuleVersion(Base):
    __tablename__ = "rule_version"
    __table_args__ = {"schema": "content"}

    id: Mapped[str] = _uuid_pk()
    rule_family_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.rule_family.id"))
    revision: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(RULE_STATUS, server_default=text("'draft'"))
    effective_from: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True))
    effective_to: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    canonical_payload: Mapped[dict] = mapped_column(JSONB)
    canonical_sha256: Mapped[str] = mapped_column(Text)
    schema_version: Mapped[str] = mapped_column(Text)
    engine_min_version: Mapped[str] = mapped_column(Text)
    confidence: Mapped[str] = mapped_column(CONFIDENCE_STATE)
    supersedes_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("content.rule_version.id"), nullable=True)
    change_summary: Mapped[str] = mapped_column(Text)
    created_by: Mapped[str] = mapped_column(UUID(as_uuid=False))
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    approved_at: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    published_at: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class RuleClaimLink(Base):
    __tablename__ = "rule_claim_link"
    __table_args__ = {"schema": "content"}

    rule_version_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.rule_version.id"), primary_key=True)
    source_claim_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.source_claim.id"), primary_key=True)
    rule_path: Mapped[str] = mapped_column(Text, primary_key=True)
    is_critical: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))


class RuleReview(Base):
    __tablename__ = "rule_review"
    __table_args__ = {"schema": "content"}

    id: Mapped[str] = _uuid_pk()
    rule_version_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.rule_version.id"))
    reviewer_id: Mapped[str] = mapped_column(UUID(as_uuid=False))
    reviewer_role: Mapped[str] = mapped_column(Text)
    decision: Mapped[str] = mapped_column(Text)
    rationale: Mapped[str] = mapped_column(Text)
    checklist: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb"))
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


class RuleBundle(Base):
    __tablename__ = "rule_bundle"
    __table_args__ = {"schema": "content"}

    id: Mapped[str] = _uuid_pk()
    intent_id: Mapped[str] = mapped_column(Text, ForeignKey("content.intent.id"))
    jurisdiction_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.jurisdiction.id"))
    channel: Mapped[str] = mapped_column(Text)
    valid_from: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True))
    valid_to: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    engine_version: Mapped[str] = mapped_column(Text)
    manifest: Mapped[dict] = mapped_column(JSONB)
    bundle_sha256: Mapped[str] = mapped_column(Text, unique=True)
    created_by: Mapped[str] = mapped_column(UUID(as_uuid=False))
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


class RuleBundleMember(Base):
    __tablename__ = "rule_bundle_member"
    __table_args__ = {"schema": "content"}

    bundle_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.rule_bundle.id"), primary_key=True)
    rule_version_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.rule_version.id"), primary_key=True)
    priority: Mapped[int] = mapped_column(Integer, server_default=text("0"))


class BundlePublication(Base):
    __tablename__ = "bundle_publication"
    __table_args__ = {"schema": "content"}

    id: Mapped[str] = _uuid_pk()
    bundle_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.rule_bundle.id"))
    channel: Mapped[str] = mapped_column(Text)
    jurisdiction_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.jurisdiction.id"))
    intent_id: Mapped[str] = mapped_column(Text, ForeignKey("content.intent.id"))
    previous_publication_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("content.bundle_publication.id"), nullable=True)
    action: Mapped[str] = mapped_column(Text)
    reason: Mapped[str] = mapped_column(Text)
    published_by: Mapped[str] = mapped_column(UUID(as_uuid=False))
    published_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    is_current: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))


# ============================= app schema ==================================
class DeviceIdentity(Base):
    __tablename__ = "device_identity"
    __table_args__ = {"schema": "app"}

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    pseudonymous_token_hash: Mapped[str] = mapped_column(Text, unique=True)
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    last_seen_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    deleted_at: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Journey(Base):
    __tablename__ = "journey"
    __table_args__ = {"schema": "app"}

    id: Mapped[str] = _uuid_pk()
    device_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("app.device_identity.id", ondelete="CASCADE"))
    account_subject: Mapped[str | None] = mapped_column(Text, nullable=True)
    intent_id: Mapped[str] = mapped_column(Text, ForeignKey("content.intent.id"))
    jurisdiction_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.jurisdiction.id"))
    title: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(JOURNEY_STATUS, server_default=text("'active'"))
    evaluated_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True))
    active_bundle_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    current_route_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    updated_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    deleted_at: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    facts: Mapped[list["JourneyFact"]] = relationship(cascade="all, delete-orphan", lazy="selectin")
    resolutions: Mapped[list["RouteResolution"]] = relationship(cascade="all, delete-orphan", lazy="selectin")
    requirement_states: Mapped[list["RequirementState"]] = relationship(cascade="all, delete-orphan", lazy="selectin")


class JourneyFact(Base):
    __tablename__ = "journey_fact"
    __table_args__ = {"schema": "app"}

    journey_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("app.journey.id", ondelete="CASCADE"), primary_key=True)
    fact_id: Mapped[str] = mapped_column(Text, primary_key=True)
    value_encrypted: Mapped[bytes] = mapped_column(BYTEA)
    value_type: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(Text)
    updated_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


class RouteResolution(Base):
    __tablename__ = "route_resolution"
    __table_args__ = {"schema": "app"}

    id: Mapped[str] = _uuid_pk()
    journey_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("app.journey.id", ondelete="CASCADE"))
    sequence: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(Text)
    evaluated_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True))
    engine_version: Mapped[str] = mapped_column(Text)
    bundle_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    facts_hash: Mapped[str] = mapped_column(Text)
    route_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    canonical_output: Mapped[dict] = mapped_column(JSONB)
    confidence: Mapped[str] = mapped_column(CONFIDENCE_STATE)
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


class RequirementState(Base):
    __tablename__ = "requirement_state"
    __table_args__ = {"schema": "app"}

    journey_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("app.journey.id", ondelete="CASCADE"), primary_key=True)
    requirement_id: Mapped[str] = mapped_column(Text, primary_key=True)
    status: Mapped[str] = mapped_column(REQUIREMENT_STATUS, server_default=text("'not_started'"))
    note_encrypted: Mapped[bytes | None] = mapped_column(BYTEA, nullable=True)
    updated_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


class DocumentAnalysis(Base):
    __tablename__ = "document_analysis"
    __table_args__ = {"schema": "app"}

    id: Mapped[str] = _uuid_pk()
    journey_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("app.journey.id", ondelete="CASCADE"))
    local_document_id: Mapped[str] = mapped_column(UUID(as_uuid=False))
    requirement_id: Mapped[str] = mapped_column(Text)
    document_type: Mapped[str] = mapped_column(Text)
    analyzer_version: Mapped[str] = mapped_column(Text)
    user_confirmed: Mapped[bool] = mapped_column(Boolean)
    minimized_fields_encrypted: Mapped[bytes | None] = mapped_column(BYTEA, nullable=True)
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)

    findings: Mapped[list["DocumentFinding"]] = relationship(cascade="all, delete-orphan", lazy="selectin")


class DocumentFinding(Base):
    __tablename__ = "document_finding"
    __table_args__ = {"schema": "app"}

    id: Mapped[str] = _uuid_pk()
    analysis_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("app.document_analysis.id", ondelete="CASCADE"))
    code: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(FINDING_SEVERITY)
    status: Mapped[str] = mapped_column(FINDING_STATUS)
    message_code: Mapped[str] = mapped_column(Text)
    field_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


class FeedbackIncident(Base):
    __tablename__ = "feedback_incident"
    __table_args__ = {"schema": "app"}

    id: Mapped[str] = _uuid_pk()
    device_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("app.device_identity.id", ondelete="SET NULL"), nullable=True)
    journey_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("app.journey.id", ondelete="SET NULL"), nullable=True)
    bundle_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    step_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    requirement_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    incident_type: Mapped[str] = mapped_column(Text)
    message_encrypted: Mapped[bytes] = mapped_column(BYTEA)
    status: Mapped[str] = mapped_column(INCIDENT_STATUS, server_default=text("'new'"))
    severity: Mapped[str] = mapped_column(Text, server_default=text("'untriaged'"))
    assigned_to: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    updated_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    resolved_at: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


# ============================= ops schema ==================================
class FetchJob(Base):
    __tablename__ = "fetch_job"
    __table_args__ = {"schema": "ops"}

    id: Mapped[str] = _uuid_pk()
    source_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.source.id"))
    status: Mapped[str] = mapped_column(JOB_STATUS, server_default=text("'queued'"))
    scheduled_for: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True))
    started_at: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    idempotency_key: Mapped[str] = mapped_column(Text, unique=True)
    trace_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


class SourceChangeAlert(Base):
    __tablename__ = "source_change_alert"
    __table_args__ = {"schema": "ops"}

    id: Mapped[str] = _uuid_pk()
    source_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.source.id"))
    previous_snapshot_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("content.source_snapshot.id"), nullable=True)
    current_snapshot_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("content.source_snapshot.id"))
    severity: Mapped[str] = mapped_column(Text)
    diff_summary: Mapped[dict] = mapped_column(JSONB)
    impacted_rule_versions: Mapped[list[str]] = mapped_column(ARRAY(UUID(as_uuid=False)), server_default=text("'{}'"))
    status: Mapped[str] = mapped_column(INCIDENT_STATUS, server_default=text("'new'"))
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    resolved_at: Mapped[_dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class IdempotencyRecord(Base):
    __tablename__ = "idempotency_record"
    __table_args__ = {"schema": "ops"}

    scope: Mapped[str] = mapped_column(Text, primary_key=True)
    idempotency_key: Mapped[str] = mapped_column(Text, primary_key=True)
    request_hash: Mapped[str] = mapped_column(Text)
    response_status: Mapped[int] = mapped_column(Integer)
    response_body: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    expires_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)


# ============================ audit schema =================================
class EventLog(Base):
    __tablename__ = "event_log"
    __table_args__ = {"schema": "audit"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    occurred_at: Mapped[_dt.datetime] = mapped_column(DateTime(timezone=True), server_default=_UTC_NOW)
    actor_type: Mapped[str] = mapped_column(Text)
    actor_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    action: Mapped[str] = mapped_column(Text)
    entity_type: Mapped[str] = mapped_column(Text)
    entity_id: Mapped[str] = mapped_column(Text)
    correlation_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_agent_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    payload: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb"))
    previous_event_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    event_hash: Mapped[str] = mapped_column(Text, unique=True)
