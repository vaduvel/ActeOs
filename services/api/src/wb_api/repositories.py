"""Database access layer (SQLAlchemy 2.0, Postgres-only).

Repositories are the only place that talk SQL. They enforce two cross-cutting
guarantees the rest of the app relies on:

- **Encryption at rest**: citizen-supplied values (journey facts, requirement
  notes, feedback messages, minimized document fields) are stored only as
  ``wbenc:`` envelope tokens in ``bytea`` columns, with AAD binding each
  ciphertext to its column + owning row so values cannot be moved between
  fields (10_SECURITY_PRIVACY).
- **Ownership / anti-IDOR**: journey reads and writes always filter by the
  caller's ``device_id`` and ``deleted_at IS NULL``.

Transactions are owned by the caller (the request dependency commits/rolls
back); repositories never commit on their own.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable, Sequence

from sqlalchemy import func, select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from . import models as m
from .audit import GENESIS_HASH, compute_event_hash
from .canonical import sha256_hex
from .crypto import FieldCipher
from .errors import ConflictProblem, NotFoundError


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _canon(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def infer_value_type(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "decimal"
    return "string"


# =============================== catalog ====================================
class CatalogRepo:
    def __init__(self, session: Session):
        self.s = session

    def list_intents(self, *, include_preview: bool = False) -> list[m.Intent]:
        stmt = select(m.Intent)
        if not include_preview:
            stmt = stmt.where(m.Intent.release_status == "production")
        stmt = stmt.order_by(m.Intent.category, m.Intent.id)
        return list(self.s.scalars(stmt))

    def get_intent(self, intent_id: str) -> m.Intent:
        intent = self.s.get(m.Intent, intent_id)
        if intent is None:
            raise NotFoundError(f"intent '{intent_id}' not found", code="intent_not_found")
        return intent

    def list_jurisdictions(self, *, kind: str | None = None, parent_id: str | None = None, query: str | None = None, limit: int = 100) -> list[m.Jurisdiction]:
        stmt = select(m.Jurisdiction).where(m.Jurisdiction.is_active.is_(True))
        if kind:
            stmt = stmt.where(m.Jurisdiction.kind == kind)
        if parent_id:
            stmt = stmt.where(m.Jurisdiction.parent_id == parent_id)
        if query:
            stmt = stmt.where(m.Jurisdiction.name.ilike(f"%{query}%"))
        stmt = stmt.order_by(m.Jurisdiction.code).limit(limit)
        return list(self.s.scalars(stmt))

    def get_jurisdiction(self, jurisdiction_id: str) -> m.Jurisdiction:
        j = self.s.get(m.Jurisdiction, jurisdiction_id)
        if j is None:
            raise NotFoundError(f"jurisdiction '{jurisdiction_id}' not found", code="jurisdiction_not_found")
        return j

    def get_jurisdiction_by_code(self, code: str) -> m.Jurisdiction | None:
        return self.s.scalar(select(m.Jurisdiction).where(m.Jurisdiction.code == code))


# =============================== devices ====================================
class DeviceRepo:
    def __init__(self, session: Session):
        self.s = session

    def touch(self, device_id: str) -> None:
        """Register/refresh a pseudonymous device. The token hash is derived
        deterministically so the same device maps to the same row without
        storing the raw identifier in a second place."""
        token_hash = sha256_hex({"device": device_id})
        stmt = pg_insert(m.DeviceIdentity).values(
            id=device_id, pseudonymous_token_hash=token_hash, last_seen_at=_now(),
        ).on_conflict_do_update(
            index_elements=[m.DeviceIdentity.id], set_={"last_seen_at": _now()},
        )
        self.s.execute(stmt)


# =============================== journeys ===================================
class JourneyRepo:
    def __init__(self, session: Session, cipher: FieldCipher):
        self.s = session
        self.cipher = cipher

    # --- crud ---------------------------------------------------------------
    def create(self, *, device_id: str, intent_id: str, jurisdiction_id: str, title: str, evaluated_at: datetime) -> m.Journey:
        journey = m.Journey(
            id=str(uuid.uuid4()), device_id=device_id, intent_id=intent_id,
            jurisdiction_id=jurisdiction_id, title=title, status="active", evaluated_at=evaluated_at,
        )
        self.s.add(journey)
        self.s.flush()
        return journey

    def get_owned(self, journey_id: str, device_id: str) -> m.Journey:
        stmt = select(m.Journey).where(
            m.Journey.id == journey_id,
            m.Journey.device_id == device_id,
            m.Journey.deleted_at.is_(None),
        )
        journey = self.s.scalar(stmt)
        if journey is None:
            # Do not distinguish "not found" from "not yours": prevents IDOR probing.
            raise NotFoundError("journey not found", code="journey_not_found")
        return journey

    def list_for_device(self, device_id: str, *, limit: int = 50, offset: int = 0) -> list[m.Journey]:
        stmt = (
            select(m.Journey)
            .where(m.Journey.device_id == device_id, m.Journey.deleted_at.is_(None))
            .order_by(m.Journey.updated_at.desc())
            .limit(limit).offset(offset)
        )
        return list(self.s.scalars(stmt))

    def soft_delete(self, journey: m.Journey) -> None:
        journey.deleted_at = _now()
        journey.status = "archived"
        journey.updated_at = _now()

    # --- facts (encrypted) --------------------------------------------------
    def _fact_aad(self, journey_id: str, fact_id: str) -> bytes:
        return f"app.journey_fact:{journey_id}:{fact_id}".encode("utf-8")

    def set_facts(self, journey: m.Journey, facts: Iterable[tuple[str, Any, str]]) -> None:
        for fact_id, value, source in facts:
            token = self.cipher.encrypt(_canon(value), aad=self._fact_aad(journey.id, fact_id))
            stmt = pg_insert(m.JourneyFact).values(
                journey_id=journey.id, fact_id=fact_id,
                value_encrypted=token.encode("utf-8"),
                value_type=infer_value_type(value), source=source, updated_at=_now(),
            ).on_conflict_do_update(
                index_elements=[m.JourneyFact.journey_id, m.JourneyFact.fact_id],
                set_={
                    "value_encrypted": token.encode("utf-8"),
                    "value_type": infer_value_type(value),
                    "source": source, "updated_at": _now(),
                },
            )
            self.s.execute(stmt)
        journey.updated_at = _now()

    def get_fact_rows(self, journey_id: str) -> list[m.JourneyFact]:
        return list(self.s.scalars(select(m.JourneyFact).where(m.JourneyFact.journey_id == journey_id).order_by(m.JourneyFact.fact_id)))

    def get_facts(self, journey_id: str) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for row in self.get_fact_rows(journey_id):
            token = bytes(row.value_encrypted).decode("utf-8")
            raw = self.cipher.decrypt_str(token, aad=self._fact_aad(journey_id, row.fact_id))
            out[row.fact_id] = json.loads(raw)
        return out

    def get_fact_inputs(self, journey_id: str) -> list[dict]:
        result = []
        for row in self.get_fact_rows(journey_id):
            token = bytes(row.value_encrypted).decode("utf-8")
            value = json.loads(self.cipher.decrypt_str(token, aad=self._fact_aad(journey_id, row.fact_id)))
            result.append({"fact_id": row.fact_id, "value": value, "source": row.source})
        return result

    # --- resolutions --------------------------------------------------------
    def record_resolution(self, journey: m.Journey, *, status: str, engine_output: dict) -> m.RouteResolution:
        next_seq = (self.s.scalar(
            select(func.coalesce(func.max(m.RouteResolution.sequence), 0)).where(m.RouteResolution.journey_id == journey.id)
        ) or 0) + 1
        evaluated_at = _parse_dt(engine_output.get("evaluated_at")) or _now()
        resolution = m.RouteResolution(
            id=str(uuid.uuid4()), journey_id=journey.id, sequence=next_seq, status=status,
            evaluated_at=evaluated_at, engine_version=engine_output["engine_version"],
            bundle_hash=engine_output.get("rule_bundle_hash"), facts_hash=engine_output["facts_hash"],
            route_hash=engine_output.get("route_hash"), canonical_output=engine_output,
            confidence=engine_output["confidence"],
        )
        self.s.add(resolution)
        journey.current_route_hash = engine_output.get("route_hash")
        journey.active_bundle_hash = engine_output.get("rule_bundle_hash")
        journey.evaluated_at = evaluated_at
        journey.updated_at = _now()
        self.s.flush()
        return resolution

    def latest_resolution(self, journey_id: str) -> m.RouteResolution | None:
        return self.s.scalar(
            select(m.RouteResolution).where(m.RouteResolution.journey_id == journey_id)
            .order_by(m.RouteResolution.sequence.desc()).limit(1)
        )

    # --- requirement states -------------------------------------------------
    def upsert_requirement_state(self, journey_id: str, requirement_id: str, status: str, note: str | None) -> m.RequirementState:
        note_enc = None
        if note is not None:
            aad = f"app.requirement_state:{journey_id}:{requirement_id}".encode("utf-8")
            note_enc = self.cipher.encrypt(note, aad=aad).encode("utf-8")
        stmt = pg_insert(m.RequirementState).values(
            journey_id=journey_id, requirement_id=requirement_id, status=status,
            note_encrypted=note_enc, updated_at=_now(),
        ).on_conflict_do_update(
            index_elements=[m.RequirementState.journey_id, m.RequirementState.requirement_id],
            set_={"status": status, "note_encrypted": note_enc, "updated_at": _now()},
        )
        self.s.execute(stmt)
        return self.s.get(m.RequirementState, (journey_id, requirement_id))

    def get_requirement_states(self, journey_id: str) -> list[m.RequirementState]:
        return list(self.s.scalars(
            select(m.RequirementState).where(m.RequirementState.journey_id == journey_id)
            .order_by(m.RequirementState.requirement_id)
        ))

    # --- document analyses --------------------------------------------------
    def add_document_analysis(self, journey_id: str, payload: dict) -> m.DocumentAnalysis:
        analysis_id = str(uuid.uuid4())
        minimized = None
        if payload.get("extracted_fields"):
            aad = f"app.document_analysis:{analysis_id}".encode("utf-8")
            minimized = self.cipher.encrypt(_canon(payload["extracted_fields"]), aad=aad).encode("utf-8")
        analysis = m.DocumentAnalysis(
            id=analysis_id, journey_id=journey_id, local_document_id=payload["local_document_id"],
            requirement_id=payload["requirement_id"], document_type=payload["document_type"],
            analyzer_version=payload.get("analyzer_version") or "unknown",
            user_confirmed=bool(payload["user_confirmed"]), minimized_fields_encrypted=minimized,
        )
        self.s.add(analysis)
        for f in payload.get("findings", []):
            self.s.add(m.DocumentFinding(
                id=str(uuid.uuid4()), analysis_id=analysis_id, code=f["code"],
                severity=f["severity"], status=f["status"], message_code=f.get("message", "")[:500],
                field_ref=f.get("field_ref"),
            ))
        self.s.flush()
        return analysis


# =============================== evidence ===================================
class EvidenceRepo:
    def __init__(self, session: Session):
        self.s = session

    def get_claim(self, claim_id: str) -> tuple[m.SourceClaim, m.Source]:
        claim = self.s.get(m.SourceClaim, claim_id)
        if claim is None:
            raise NotFoundError("evidence not found", code="evidence_not_found")
        snapshot = self.s.get(m.SourceSnapshot, claim.source_snapshot_id)
        source = self.s.get(m.Source, snapshot.source_id) if snapshot else None
        if source is None:
            raise NotFoundError("source not found", code="source_not_found")
        return claim, source


# =============================== feedback ===================================
class FeedbackRepo:
    def __init__(self, session: Session, cipher: FieldCipher):
        self.s = session
        self.cipher = cipher

    def create(self, *, device_id: str | None, payload: dict) -> str:
        incident_id = str(uuid.uuid4())
        aad = f"app.feedback_incident:{incident_id}".encode("utf-8")
        message_enc = self.cipher.encrypt(payload["message"], aad=aad).encode("utf-8")
        incident = m.FeedbackIncident(
            id=incident_id, device_id=device_id, journey_id=payload.get("journey_id"),
            bundle_hash=payload.get("rule_bundle_hash"), step_id=payload.get("step_id"),
            requirement_id=payload.get("requirement_id"), incident_type=payload["type"],
            message_encrypted=message_enc, status="new", severity="untriaged",
        )
        self.s.add(incident)
        self.s.flush()
        return incident_id


# ============================= idempotency ==================================
class IdempotencyRepo:
    """Completed-response store keyed by (scope, key).

    Concurrent identical requests are serialized with a transaction-scoped
    advisory lock so the second caller waits and then replays the stored
    response instead of double-executing a side effect.
    """

    def __init__(self, session: Session):
        self.s = session

    @staticmethod
    def _lock_key(scope: str, key: str) -> int:
        digest = hashlib.sha256(f"{scope}\x00{key}".encode("utf-8")).digest()[:8]
        return int.from_bytes(digest, "big", signed=True)

    def lock(self, scope: str, key: str) -> None:
        self.s.execute(text("SELECT pg_advisory_xact_lock(:k)"), {"k": self._lock_key(scope, key)})

    def find(self, scope: str, key: str, request_hash: str) -> m.IdempotencyRecord | None:
        rec = self.s.get(m.IdempotencyRecord, (scope, key))
        if rec is None:
            return None
        if rec.expires_at <= _now():
            self.s.delete(rec)
            self.s.flush()
            return None
        if rec.request_hash != request_hash:
            raise ConflictProblem(
                "Idempotency-Key reused with a different request body.",
                code="idempotency_key_conflict",
            )
        return rec

    def store(self, scope: str, key: str, *, request_hash: str, status: int, body: dict | None, ttl_seconds: int) -> None:
        rec = m.IdempotencyRecord(
            scope=scope, idempotency_key=key, request_hash=request_hash,
            response_status=status, response_body=body,
            expires_at=_now() + timedelta(seconds=ttl_seconds),
        )
        self.s.add(rec)
        self.s.flush()


# =============================== audit ======================================
class AuditRepo:
    """Append-only writer for ``audit.event_log`` with a maintained hash chain."""

    def __init__(self, session: Session):
        self.s = session

    def _head(self) -> str:
        row = self.s.scalar(select(m.EventLog.event_hash).order_by(m.EventLog.id.desc()).limit(1))
        return row or GENESIS_HASH

    def append(self, *, actor_type: str, action: str, entity_type: str, entity_id: str,
               actor_id: str | None = None, correlation_id: str | None = None,
               payload: dict | None = None) -> str:
        prev = self._head()
        occurred_at = _now()
        payload = payload or {}
        event_hash = compute_event_hash(
            previous_event_hash=prev, occurred_at=occurred_at.isoformat(),
            actor_type=actor_type, actor_id=actor_id, action=action,
            entity_type=entity_type, entity_id=entity_id, correlation_id=correlation_id, payload=payload,
        )
        self.s.add(m.EventLog(
            occurred_at=occurred_at, actor_type=actor_type, actor_id=actor_id, action=action,
            entity_type=entity_type, entity_id=entity_id, correlation_id=correlation_id,
            payload=payload, previous_event_hash=prev, event_hash=event_hash,
        ))
        self.s.flush()
        return event_hash


# =========================== content / bundles ==============================
class ContentBundleRepo:
    """Reads the currently published rule bundle for an intent + jurisdiction."""

    def __init__(self, session: Session):
        self.s = session

    def current_publication(self, intent_id: str, jurisdiction_id: str, *, channel: str = "production") -> m.BundlePublication | None:
        stmt = (
            select(m.BundlePublication).where(
                m.BundlePublication.intent_id == intent_id,
                m.BundlePublication.jurisdiction_id == jurisdiction_id,
                m.BundlePublication.channel == channel,
                m.BundlePublication.is_current.is_(True),
            ).order_by(m.BundlePublication.published_at.desc()).limit(1)
        )
        return self.s.scalar(stmt)

    def bundle_rules(self, bundle_id: str) -> list[dict]:
        stmt = (
            select(m.RuleVersion.canonical_payload)
            .join(m.RuleBundleMember, m.RuleBundleMember.rule_version_id == m.RuleVersion.id)
            .where(m.RuleBundleMember.bundle_id == bundle_id)
            .order_by(m.RuleBundleMember.priority, m.RuleVersion.id)
        )
        return [row for row in self.s.scalars(stmt)]

    def get_bundle(self, bundle_id: str) -> m.RuleBundle | None:
        return self.s.get(m.RuleBundle, bundle_id)


def _parse_dt(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
