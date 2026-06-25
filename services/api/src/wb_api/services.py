"""Domain services: orchestrate repositories, the bundle provider, the rule
engine, and contract mapping. Routers call services; services own no HTTP or
SQL details beyond the repositories they compose.

Key invariants enforced here:
- Route resolution is reproducible: the engine is given ``now = evaluated_at``
  and a reference date derived from it, so re-resolving identical inputs yields
  the same ``route_hash``.
- ADR-011 fail-closed: when a critical source is expired, the route is blocked
  rather than presented with stale guidance.
- Every state change writes an append-only audit event.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from wb_rule_engine import resolve as engine_resolve
from wb_rule_engine import route_diff

from . import mapping
from . import schemas as S
from .bundles import BundleProvider, ResolvedBundle
from .errors import ConflictProblem, NotFoundError, ValidationProblem
from .repositories import (
    AuditRepo,
    CatalogRepo,
    EvidenceRepo,
    FeedbackRepo,
    JourneyRepo,
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _facts_dict(facts: list[S.FactInput]) -> dict[str, Any]:
    return {f.fact_id: f.value for f in facts}


# =============================== catalog ====================================
class CatalogService:
    def __init__(self, catalog: CatalogRepo):
        self.catalog = catalog

    def list_intents(self, *, include_preview: bool = False) -> list[S.IntentSummary]:
        out = []
        for i in self.catalog.list_intents(include_preview=include_preview):
            out.append(S.IntentSummary(
                id=i.id, title=i.title_ro, short_description=i.description_ro,
                category=i.category, keywords=list(i.keywords_ro or []),
                release_status="production" if i.release_status == "production" else "preview",
            ))
        return out

    def list_jurisdictions(self, *, kind: str | None = None, parent_id: str | None = None, query: str | None = None) -> list[S.Jurisdiction]:
        out = []
        for j in self.catalog.list_jurisdictions(kind=kind, parent_id=parent_id, query=query):
            jtype = j.kind if j.kind in ("country", "county", "uat", "institution") else "institution"
            out.append(S.Jurisdiction(
                id=j.id, parent_id=j.parent_id, code=j.code, name=j.name,
                type=jtype, timezone="Europe/Bucharest",
            ))
        return out


# ============================ route resolver ================================
class RouteResolver:
    """Shared engine invocation used by stateless resolve and by journeys."""

    def __init__(self, catalog: CatalogRepo, provider: BundleProvider, *, fail_closed: bool):
        self.catalog = catalog
        self.provider = provider
        self.fail_closed = fail_closed

    def resolve_engine(self, *, intent_id: str, jurisdiction_id: str, evaluated_at: datetime, facts: dict) -> tuple[dict, ResolvedBundle]:
        jur = self.catalog.get_jurisdiction(jurisdiction_id)
        bundle = self.provider.for_intent(intent_id, jurisdiction_id)
        if bundle is None:
            raise ConflictProblem(
                "No published rule bundle is available for this intent and jurisdiction.",
                code="bundle_unavailable",
            )
        request = {
            "intent_id": intent_id,
            "jurisdiction_id": jur.code,
            "reference_date": evaluated_at.astimezone(timezone.utc).date().isoformat(),
            "facts": facts,
        }
        output = engine_resolve(request, bundle.engine_bundle, now=evaluated_at)
        if self.fail_closed and output.get("confidence") == "expired":
            output["blocked"] = True
            output.setdefault("gates", []).append({
                "code": "RULE_SOURCE_EXPIRED",
                "message": "Sursa critica este expirata; traseul este blocat din motive de siguranta.",
                "effect": "block",
            })
        return output, bundle

    def resolve(self, req: S.RouteResolveRequest) -> S.RouteResolution:
        output, _ = self.resolve_engine(
            intent_id=req.intent_id, jurisdiction_id=req.jurisdiction_id,
            evaluated_at=req.evaluated_at, facts=_facts_dict(req.facts),
        )
        return mapping.to_route_resolution(output)


# =============================== journeys ===================================
class JourneyService:
    def __init__(self, *, catalog: CatalogRepo, journeys: JourneyRepo, resolver: RouteResolver, audit: AuditRepo):
        self.catalog = catalog
        self.journeys = journeys
        self.resolver = resolver
        self.audit = audit

    def create(self, *, device_id: str, req: S.CreateJourneyRequest) -> S.Journey:
        intent = self.catalog.get_intent(req.intent_id)
        self.catalog.get_jurisdiction(req.jurisdiction_id)  # validate existence
        title = req.title_override or intent.title_ro
        journey = self.journeys.create(
            device_id=device_id, intent_id=req.intent_id, jurisdiction_id=req.jurisdiction_id,
            title=title, evaluated_at=req.evaluated_at,
        )
        if req.facts:
            self.journeys.set_facts(journey, [(f.fact_id, f.value, f.source) for f in req.facts])
        output, _ = self.resolver.resolve_engine(
            intent_id=req.intent_id, jurisdiction_id=req.jurisdiction_id,
            evaluated_at=req.evaluated_at, facts=self.journeys.get_facts(journey.id),
        )
        resolution = mapping.to_route_resolution(output)
        self.journeys.record_resolution(journey, status=resolution.status, engine_output=output)
        self.audit.append(
            actor_type="device", actor_id=device_id, action="journey.create",
            entity_type="journey", entity_id=journey.id,
            payload={"intent_id": req.intent_id, "route_hash": output.get("route_hash")},
        )
        return self._assemble(journey, output)

    def get(self, *, device_id: str, journey_id: str) -> S.Journey:
        journey = self.journeys.get_owned(journey_id, device_id)
        latest = self.journeys.latest_resolution(journey_id)
        if latest is None:
            raise NotFoundError("journey has no resolution", code="journey_incomplete")
        return self._assemble(journey, latest.canonical_output)

    def list(self, *, device_id: str, limit: int, offset: int) -> list[S.JourneySummary]:
        out = []
        for journey in self.journeys.list_for_device(device_id, limit=limit, offset=offset):
            latest = self.journeys.latest_resolution(journey.id)
            resolution = mapping.to_route_resolution(latest.canonical_output) if latest else None
            out.append(mapping.build_summary(journey, resolution))
        return out

    def delete(self, *, device_id: str, journey_id: str) -> None:
        journey = self.journeys.get_owned(journey_id, device_id)
        self.journeys.soft_delete(journey)
        self.audit.append(
            actor_type="device", actor_id=device_id, action="journey.delete",
            entity_type="journey", entity_id=journey_id, payload={},
        )

    def patch_facts(self, *, device_id: str, journey_id: str, facts: list[S.FactInput]) -> S.Journey:
        journey = self.journeys.get_owned(journey_id, device_id)
        self.journeys.set_facts(journey, [(f.fact_id, f.value, f.source) for f in facts])
        output, _ = self.resolver.resolve_engine(
            intent_id=journey.intent_id, jurisdiction_id=journey.jurisdiction_id,
            evaluated_at=journey.evaluated_at, facts=self.journeys.get_facts(journey.id),
        )
        resolution = mapping.to_route_resolution(output)
        self.journeys.record_resolution(journey, status=resolution.status, engine_output=output)
        self.audit.append(
            actor_type="device", actor_id=device_id, action="journey.facts.update",
            entity_type="journey", entity_id=journey_id,
            payload={"fact_ids": sorted(f.fact_id for f in facts), "route_hash": output.get("route_hash")},
        )
        return self._assemble(journey, output)

    def recalculate(self, *, device_id: str, journey_id: str, req: S.RecalculateRequest) -> S.RecalculationResult:
        journey = self.journeys.get_owned(journey_id, device_id)
        previous = self.journeys.latest_resolution(journey_id)
        previous_output = previous.canonical_output if previous else {}
        evaluated_at = req.evaluated_at or _now()
        output, _ = self.resolver.resolve_engine(
            intent_id=journey.intent_id, jurisdiction_id=journey.jurisdiction_id,
            evaluated_at=evaluated_at, facts=self.journeys.get_facts(journey.id),
        )
        resolution = mapping.to_route_resolution(output)
        self.journeys.record_resolution(journey, status=resolution.status, engine_output=output)
        diff = route_diff(previous_output, output)
        deadline_changes = self._deadline_changes(previous_output, output)
        self.audit.append(
            actor_type="device", actor_id=device_id, action="journey.recalculate",
            entity_type="journey", entity_id=journey_id,
            payload={"reason": req.reason, "previous_route_hash": previous_output.get("route_hash"), "route_hash": output.get("route_hash")},
        )
        return S.RecalculationResult(
            previous_route_hash=previous_output.get("route_hash"),
            resolution=resolution,
            diff=S.RouteDiff(
                added_steps=diff["steps_added"],
                removed_steps=diff["steps_removed"],
                changed_requirements=diff["steps_changed"],
                deadline_changes=deadline_changes,
            ),
        )

    def update_requirement(self, *, device_id: str, journey_id: str, requirement_id: str, body: S.RequirementUpdate) -> S.RequirementState:
        journey = self.journeys.get_owned(journey_id, device_id)
        state = self.journeys.upsert_requirement_state(journey.id, requirement_id, body.status, body.note)
        self.audit.append(
            actor_type="device", actor_id=device_id, action="requirement.update",
            entity_type="journey", entity_id=journey_id,
            payload={"requirement_id": requirement_id, "status": body.status},
        )
        return S.RequirementState(
            requirement_id=state.requirement_id, status=state.status, note=None, updated_at=state.updated_at,
        )

    def add_document_analysis(self, *, device_id: str, journey_id: str, body: S.DocumentAnalysisInput) -> S.DocumentAnalysis:
        journey = self.journeys.get_owned(journey_id, device_id)
        analysis = self.journeys.add_document_analysis(journey.id, body.model_dump())
        self.audit.append(
            actor_type="device", actor_id=device_id, action="document.analysis.create",
            entity_type="journey", entity_id=journey_id,
            payload={"requirement_id": body.requirement_id, "document_type": body.document_type,
                     "findings": [f.code for f in body.findings]},
        )
        return S.DocumentAnalysis(
            id=analysis.id, created_at=analysis.created_at,
            local_document_id=body.local_document_id, requirement_id=body.requirement_id,
            document_type=body.document_type, user_confirmed=True,
            extracted_fields=None, findings=body.findings, analyzer_version=body.analyzer_version,
        )

    # --- helpers ------------------------------------------------------------
    def _assemble(self, journey, engine_output: dict) -> S.Journey:
        resolution = mapping.to_route_resolution(engine_output)
        fact_inputs = self.journeys.get_fact_inputs(journey.id)
        states = self.journeys.get_requirement_states(journey.id)
        return mapping.build_journey(journey, resolution, states, fact_inputs)

    @staticmethod
    def _deadline_changes(old: dict, new: dict) -> list[str]:
        def deadlines(o: dict) -> dict[str, Any]:
            return {s["id"]: (s.get("deadline") or {}).get("ends_at") for s in o.get("steps", [])}
        old_d, new_d = deadlines(old), deadlines(new)
        changed = [sid for sid in new_d if sid in old_d and old_d[sid] != new_d[sid]]
        return sorted(changed)


# =============================== evidence ===================================
class EvidenceService:
    def __init__(self, evidence: EvidenceRepo):
        self.evidence = evidence

    def get_claim(self, claim_id: str) -> S.SourceClaim:
        claim, source = self.evidence.get_claim(claim_id)
        return S.SourceClaim(
            id=claim.id, claim_text=claim.claim_text,
            source=S.Source(
                id=source.id, canonical_url=source.canonical_url, publisher=source.publisher,
                authority_level=source.authority_level, jurisdiction_id=source.jurisdiction_id,
                status=source.status, freshness_class=source.freshness_class,
                review_interval_days=source.review_interval_days, last_verified_at=source.last_verified_at,
            ),
            evidence_excerpt=claim.evidence_excerpt, locator=claim.locator,
            effective_from=claim.effective_from, effective_to=claim.effective_to,
            accessed_at=claim.created_at, confidence=claim.confidence,
        )


# =============================== feedback ===================================
class FeedbackService:
    def __init__(self, *, feedback: FeedbackRepo, journeys: JourneyRepo, audit: AuditRepo):
        self.feedback = feedback
        self.journeys = journeys
        self.audit = audit

    def submit(self, *, device_id: str, body: S.FeedbackInput) -> S.FeedbackAccepted:
        if body.journey_id is not None:
            # Ownership check: a device may only attach feedback to its own journey.
            self.journeys.get_owned(body.journey_id, device_id)
        incident_id = self.feedback.create(device_id=device_id, payload=body.model_dump())
        self.audit.append(
            actor_type="device", actor_id=device_id, action="feedback.submit",
            entity_type="feedback_incident", entity_id=incident_id,
            payload={"type": body.type, "journey_id": body.journey_id},
        )
        return S.FeedbackAccepted(incident_id=incident_id, status="queued_for_review")
