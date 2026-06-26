"""Case service + router: turn an intent into a resolved administrative route.

POST /v1/cases takes an intent (plus reference_date, jurisdiction_path and the
citizen's known facts), resolves the linked life event(s) through the
deterministic rule engine, persists the case, and returns the resolution with a
verifiable resolution_trace (facts_hash + engine_version + included/excluded
rule ids).

This is the engine-output slice: it returns exactly what the governed rulesets
encode (semantic step/requirement/channel ids, authored advice/warnings,
deadlines, blocks, missing facts). Materializing human-facing step content
(title_ro/instruction_ro) requires published step/requirement templates and is a
separate slice; see acteos_rule_engine.authoring.resolution.

Persistence is behind the CaseRepository port: an in-memory adapter by default,
or the PostgreSQL adapter (app.cases + app.journeys) when ACTEOS_DATABASE_URL is
configured. Subject identity is anonymous-first (installation_id) with optional
authenticated user_id; the database enforces that at least one is present.
"""
from __future__ import annotations

import os
import uuid
from datetime import date, datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

import yaml
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from acteos_rule_engine.authoring.orchestrator import resolve_event
from acteos_rule_engine.authoring.resolution import build_resolution

from .discovery import DiscoveryError
from .repository import CaseRepository, InMemoryCaseRepository
from .rulesets import RulesetRepository

_PACK_ROOT = Path(__file__).resolve().parents[4]

DiscoverySource = Literal[
    "search",
    "category",
    "quick_action",
    "related_intent",
    "deep_link",
    "legacy_event",
]

# Case-level resolution statuses that mean the route is not cleanly trusted yet
# and a journey should surface for review (drives app.journeys.trust_state).
_REVIEW_STATUSES = frozenset({"conflicting", "needs_confirmation", "blocked"})


class CaseError(DiscoveryError):
    """Case-domain error; reuses the ErrorResponse handler via DiscoveryError."""


def _trust_state(resolution: dict) -> str:
    """Derive a journey trust_state from the resolution (provisional mapping).

    A clean resolution is ``trusted``; an unresolved source conflict, a required
    confirmation, a block, or any event carrying conflicts/blocks downgrades to
    ``needs_review`` so the journey is not presented as fully settled.
    """

    if resolution.get("status") in _REVIEW_STATUSES:
        return "needs_review"
    for event in resolution.get("events", []) or []:
        if event.get("conflicts") or event.get("blocks"):
            return "needs_review"
    return "trusted"


# -- request/response models (mirror contracts/jsonschema/case.schema.json) ----
class CreateCaseRequest(BaseModel):
    intent_type_id: str = Field(pattern=r"^ro\.intent\.[a-z0-9_.-]+$")
    reference_date: date
    timezone: Literal["Europe/Bucharest"] = "Europe/Bucharest"
    jurisdiction_path: list[str] = Field(min_length=2)
    event_type_id: str | None = Field(default=None, pattern=r"^ro\.life\.[a-z0-9_.-]+$")
    subject_ref: str | None = None
    user_id: str | None = None
    installation_id: str | None = None
    discovery_source: DiscoverySource | None = None
    facts: dict[str, Any] = Field(default_factory=dict)


class ResolutionTrace(BaseModel):
    facts_hash: str
    engine_version: str
    included_rule_ids: list[str]
    excluded_rule_ids: list[str]
    ruleset_version: str
    reference_date: str | None = None
    root_event_type_id: str
    event_type_ids: list[str]
    has_unknown_events: bool = False
    intent_type_id: str | None = None


class EventResolution(BaseModel):
    event_type_id: str
    status: str
    included_steps: list[str]
    requirements: list[str]
    obligations: dict[str, Any]
    channels: list[str]
    advice: list[dict]
    warnings: list[dict]
    confirmations: list[str]
    conflicts: list[str]
    blocks: list[dict]
    deadlines: dict[str, Any]
    overdue_steps: list[str]
    child_events: list[str]
    missing_facts: list[str]
    overridden_rules: list[str]
    fired_rule_ids: list[str]
    excluded_rule_ids: list[str]


class CaseResponse(BaseModel):
    id: str
    intent_type_id: str
    event_type_id: str
    reference_date: date
    timezone: str
    jurisdiction_path: list[str]
    status: str
    version: int
    facts_hash: str
    engine_version: str
    ruleset_version: str
    events: list[EventResolution]
    resolution_trace: ResolutionTrace
    created_at: datetime


class CaseService:
    def __init__(
        self,
        intent_links: dict[str, list[str]],
        rulesets: RulesetRepository,
        repository: CaseRepository,
        *,
        ruleset_version: str | None = None,
    ) -> None:
        self._intent_links = dict(intent_links)
        self._rulesets = rulesets
        self._repository = repository
        self._ruleset_version = ruleset_version or rulesets.content_version()

    @classmethod
    def from_paths(
        cls,
        taxonomy_path: str,
        inbox_dir: str,
        repository: CaseRepository | None = None,
    ) -> "CaseService":
        taxonomy = yaml.safe_load(Path(taxonomy_path).read_text(encoding="utf-8")) or {}
        links = {
            i["id"]: list(i.get("linked_event_ids", []) or [])
            for i in taxonomy.get("intents", [])
            if i.get("id")
        }
        rulesets = RulesetRepository.from_inbox(inbox_dir)
        return cls(links, rulesets, repository or InMemoryCaseRepository())

    def _resolve_root_event(self, req: "CreateCaseRequest") -> str:
        if req.intent_type_id not in self._intent_links:
            raise CaseError(404, "INTENT_NOT_FOUND", "Intentul nu exista in catalog.")
        candidates: list[str] = []
        if req.event_type_id:
            candidates.append(req.event_type_id)
        candidates.extend(self._intent_links.get(req.intent_type_id, []))
        for candidate in candidates:
            canonical = self._rulesets.canonical(candidate)
            if canonical is not None:
                return canonical
        raise CaseError(
            422,
            "INTENT_NOT_RESOLVABLE",
            "Nu exista inca un set de reguli publicat pentru acest intent.",
        )

    def create_case(self, req: "CreateCaseRequest", request_id: str = "") -> "CaseResponse":
        root_event = self._resolve_root_event(req)
        node = resolve_event(
            root_event,
            self._rulesets.engine_map,
            req.facts,
            jurisdiction_path=req.jurisdiction_path,
            reference_date=req.reference_date,
        )
        resolution = build_resolution(
            node,
            self._rulesets.engine_map,
            req.facts,
            ruleset_version=self._ruleset_version,
            intent_type_id=req.intent_type_id,
            reference_date=req.reference_date,
        )
        case = {
            "id": str(uuid.uuid4()),
            "intent_type_id": req.intent_type_id,
            "event_type_id": root_event,
            "reference_date": req.reference_date.isoformat(),
            "timezone": req.timezone,
            "jurisdiction_path": list(req.jurisdiction_path),
            "subject_ref": req.subject_ref,
            "user_id": req.user_id,
            "installation_id": req.installation_id,
            "discovery_source": req.discovery_source,
            "status": resolution["status"],
            "version": 1,
            "facts_hash": resolution["facts_hash"],
            "engine_version": resolution["engine_version"],
            "ruleset_version": resolution["ruleset_version"],
            "trust_state": _trust_state(resolution),
            "events": resolution["events"],
            "resolution_trace": resolution["resolution_trace"],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._repository.save(case)
        return self._to_response(case)

    def get_case(self, case_id: str) -> "CaseResponse":
        case = self._repository.get(case_id)
        if case is None:
            raise CaseError(404, "CASE_NOT_FOUND", "Cazul nu exista.")
        return self._to_response(case)

    @staticmethod
    def _to_response(case: dict) -> "CaseResponse":
        return CaseResponse(
            id=case["id"],
            intent_type_id=case["intent_type_id"],
            event_type_id=case["event_type_id"],
            reference_date=date.fromisoformat(case["reference_date"]),
            timezone=case["timezone"],
            jurisdiction_path=case["jurisdiction_path"],
            status=case["status"],
            version=case["version"],
            facts_hash=case["facts_hash"],
            engine_version=case["engine_version"],
            ruleset_version=case["ruleset_version"],
            events=[EventResolution(**e) for e in case["events"]],
            resolution_trace=ResolutionTrace(**case["resolution_trace"]),
            created_at=datetime.fromisoformat(case["created_at"]),
        )


def _taxonomy_path() -> str:
    return os.environ.get("ACTEOS_TAXONOMY_PATH", str(_PACK_ROOT / "data" / "intent_taxonomy.yaml"))


def _inbox_path() -> str:
    return os.environ.get("ACTEOS_RESEARCH_INBOX", str(_PACK_ROOT / "research" / "inbox"))


@lru_cache(maxsize=1)
def get_case_service() -> CaseService:
    from .db import get_case_repository

    return CaseService.from_paths(_taxonomy_path(), _inbox_path(), repository=get_case_repository())


router = APIRouter(prefix="/v1", tags=["Cases"])


@router.post("/cases", response_model=CaseResponse, status_code=201)
def create_case(
    req: CreateCaseRequest,
    request: Request,
    svc: CaseService = Depends(get_case_service),
) -> CaseResponse:
    request_id = getattr(request.state, "request_id", "")
    return svc.create_case(req, request_id)


@router.get("/cases/{case_id}", response_model=CaseResponse)
def get_case(
    case_id: str,
    svc: CaseService = Depends(get_case_service),
) -> CaseResponse:
    return svc.get_case(case_id)
