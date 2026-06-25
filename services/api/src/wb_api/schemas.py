"""Pydantic v2 request/response models mirroring `08_API_SPEC.yaml`.

These are the wire contract. They are intentionally decoupled from ORM models
and from the rule-engine's internal output shape; the service layer adapts
between them. Field patterns and enums are enforced here so invalid input is
rejected with a 422 problem before reaching domain logic.
"""
from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

# --- shared scalar types -----------------------------------------------------
StableId = Annotated[str, Field(pattern=r"^[a-z0-9][a-z0-9_.-]{2,127}$")]
Sha256 = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
Uuid = Annotated[str, Field(min_length=1)]

ConfidenceState = Literal[
    "verified", "verified_with_local_gap", "needs_confirmation", "conflicting", "expired"
]
RouteStatus = Literal["resolved", "needs_facts", "blocked"]
JourneyStatus = Literal["active", "completed", "archived"]
RequirementStatusValue = Literal[
    "not_started", "ready", "blocked", "in_progress", "submitted", "completed", "not_applicable"
]
FactSource = Literal["user", "derived", "document_confirmed"]


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    version: str
    timestamp: datetime
    checks: dict[str, str] | None = None


# --- catalog -----------------------------------------------------------------
class IntentSummary(BaseModel):
    id: StableId
    title: str
    short_description: str | None = None
    category: str
    keywords: list[str] = Field(default_factory=list)
    release_status: Literal["production", "preview"]


class Jurisdiction(BaseModel):
    id: Uuid
    parent_id: Optional[Uuid] = None
    code: StableId
    name: str
    type: Literal["country", "county", "uat", "institution"]
    timezone: Literal["Europe/Bucharest"] = "Europe/Bucharest"


# --- facts & routes ----------------------------------------------------------
class FactInput(BaseModel):
    fact_id: StableId
    value: Any
    source: FactSource = "user"


class FactQuestion(BaseModel):
    fact_id: StableId
    label: str
    value_type: Literal[
        "boolean", "string", "enum", "integer", "decimal", "date", "datetime", "jurisdiction_ref"
    ]
    options: list[dict[str, Any]] | None = None
    reason: str
    sensitive: bool = False


class Deadline(BaseModel):
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    timezone: Literal["Europe/Bucharest"] = "Europe/Bucharest"
    derived_from: Literal["fixed", "calendar_rule", "institution_schedule"] | None = None


class ResolvedRequirement(BaseModel):
    id: StableId
    title: str
    obligation: Literal["mandatory", "conditional", "optional", "later"]
    applies: Literal["yes", "no", "unknown"]
    reason: str | None = None
    accepted_forms: list[Literal["original", "copy", "electronic", "certified_copy"]] | None = None
    readiness_checks: list[StableId] = Field(default_factory=list)
    source_claim_ids: list[Uuid] = Field(default_factory=list)


class ResolvedStep(BaseModel):
    id: StableId
    title: str
    sequence: int = Field(ge=1)
    state: Literal["upcoming", "actionable", "blocked", "completed", "skipped"]
    instruction: str | None = None
    deadline: Optional[Deadline] = None
    requirements: list[ResolvedRequirement] = Field(default_factory=list)
    completion_evidence: str
    recovery_actions: list[str] = Field(default_factory=list)
    source_claim_ids: list[Uuid] = Field(default_factory=list)


class RouteIssue(BaseModel):
    code: StableId
    severity: Literal["blocking", "warning", "info"]
    message: str
    source_claim_ids: list[Uuid] = Field(default_factory=list)


class RouteResolution(BaseModel):
    status: RouteStatus
    route_hash: Optional[Sha256] = None
    rule_bundle_hash: Optional[Sha256] = None
    facts_hash: Sha256
    engine_version: str
    evaluated_at: datetime
    missing_facts: list[FactQuestion] = Field(default_factory=list)
    steps: list[ResolvedStep] = Field(default_factory=list)
    blocking_issues: list[RouteIssue] = Field(default_factory=list)
    confidence: ConfidenceState | None = None


class RouteResolveRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent_id: StableId
    jurisdiction_id: Uuid
    evaluated_at: datetime
    preferred_bundle_hash: Optional[Sha256] = None
    facts: list[FactInput] = Field(default_factory=list)


# --- journeys ----------------------------------------------------------------
class CreateJourneyRequest(BaseModel):
    intent_id: StableId
    jurisdiction_id: Uuid
    evaluated_at: datetime
    title_override: str | None = Field(default=None, max_length=120)
    facts: list[FactInput] = Field(default_factory=list)


class JourneySummary(BaseModel):
    id: Uuid
    intent_id: StableId
    title: str
    status: JourneyStatus
    next_action_title: str | None = None
    next_deadline: Optional[datetime] = None
    updated_at: datetime


class RequirementState(BaseModel):
    requirement_id: StableId
    status: RequirementStatusValue
    note: str | None = None
    updated_at: datetime


class Journey(JourneySummary):
    jurisdiction_id: Uuid
    created_at: datetime
    facts: list[FactInput] = Field(default_factory=list)
    resolution: RouteResolution
    requirement_states: list[RequirementState] = Field(default_factory=list)


class FactsPatch(BaseModel):
    facts: list[FactInput] = Field(min_length=1)


class RecalculateRequest(BaseModel):
    evaluated_at: datetime | None = None
    target_bundle_id: Optional[Uuid] = None
    reason: Literal["user_change", "new_bundle", "missed_deadline", "rejection", "expired_document"] | None = None


class RouteDiff(BaseModel):
    added_steps: list[StableId] = Field(default_factory=list)
    removed_steps: list[StableId] = Field(default_factory=list)
    changed_requirements: list[StableId] = Field(default_factory=list)
    deadline_changes: list[StableId] = Field(default_factory=list)


class RecalculationResult(BaseModel):
    previous_route_hash: Sha256
    resolution: RouteResolution
    diff: RouteDiff


class RequirementUpdate(BaseModel):
    status: RequirementStatusValue
    note: str | None = Field(default=None, max_length=1000)


# --- evidence & documents ----------------------------------------------------
class Source(BaseModel):
    id: Uuid
    canonical_url: str = Field(max_length=2048)
    publisher: str
    authority_level: Literal[
        "eu", "national_normative", "national_operational", "county", "uat", "institution", "signal_only"
    ]
    jurisdiction_id: Optional[Uuid] = None
    status: Literal["active", "paused", "retired"]
    freshness_class: Literal["critical", "operational", "explanatory"]
    review_interval_days: int | None = Field(default=None, ge=1, le=730)
    last_verified_at: Optional[datetime] = None


class SourceClaim(BaseModel):
    id: Uuid
    claim_text: str
    source: Source
    evidence_excerpt: str = Field(max_length=1000)
    locator: str | None = None
    effective_from: Optional[datetime] = None
    effective_to: Optional[datetime] = None
    accessed_at: datetime
    confidence: ConfidenceState


class DocumentFinding(BaseModel):
    code: StableId
    severity: Literal["blocking", "warning", "info", "unknown"]
    status: Literal["detected", "not_detected", "unable_to_check"]
    message: str = Field(max_length=500)
    field_ref: str | None = None


class DocumentAnalysisInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    local_document_id: Uuid
    requirement_id: StableId
    document_type: StableId
    user_confirmed: Literal[True]
    extracted_fields: dict[str, Any] | None = None
    findings: list[DocumentFinding] = Field(default_factory=list)
    analyzer_version: str | None = None


class DocumentAnalysis(DocumentAnalysisInput):
    id: Uuid
    created_at: datetime


# --- feedback ----------------------------------------------------------------
class FeedbackInput(BaseModel):
    journey_id: Optional[Uuid] = None
    rule_bundle_hash: Optional[Sha256] = None
    step_id: Optional[StableId] = None
    requirement_id: Optional[StableId] = None
    type: Literal[
        "extra_document_requested", "wrong_schedule", "wrong_address", "broken_link",
        "accepted_first_time", "other",
    ]
    message: str = Field(min_length=5, max_length=4000)
    consent_to_contact: bool = False
    contact_token: str | None = None


class FeedbackAccepted(BaseModel):
    incident_id: Uuid
    status: Literal["queued_for_review"] = "queued_for_review"


# --- curator (governed) ------------------------------------------------------
class CreateSourceRequest(BaseModel):
    canonical_url: str
    publisher: str = Field(min_length=2)
    authority_level: Literal[
        "eu", "national_normative", "national_operational", "county", "uat", "institution", "signal_only"
    ]
    jurisdiction_id: Optional[Uuid] = None
    freshness_class: Literal["critical", "operational", "explanatory"]
    review_interval_days: int = Field(ge=1, le=730)
    fetch_policy: dict[str, Any] | None = None


class RuleVersionReview(BaseModel):
    decision: Literal["approve", "request_changes", "reject"]
    rationale: str = Field(min_length=10, max_length=4000)
    checklist: dict[str, bool] | None = None


class RuleVersionStatus(BaseModel):
    rule_version_id: Uuid
    status: Literal[
        "draft", "in_review", "changes_requested", "approved", "rejected", "published", "retired"
    ]
    reviews_required: int
    reviews_received: int


class PublishBundleRequest(BaseModel):
    channel: Literal["canary", "production"]
    reason: str | None = Field(default=None, min_length=10, max_length=1000)
    expected_previous_bundle_hash: Optional[Sha256] = None


class RollbackBundleRequest(BaseModel):
    target_publication_id: Uuid
    reason: str = Field(min_length=20, max_length=2000)


class BundlePublication(BaseModel):
    publication_id: Uuid
    bundle_id: Uuid
    bundle_hash: Sha256
    channel: Literal["canary", "production"]
    published_at: datetime
