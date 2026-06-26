"""Publish/compile pipeline: certified inbox batches -> content-addressed bundle.

This module is the deterministic compiler that turns governed research/authoring
batches (the inbox) into a :class:`PublishedBundle` whose records mirror the
``content.*`` schema in ``db/0001_init.sql``.  It is the ``rule bundle manifest +
checksums`` deliverable from the ``acteos-release-certification`` skill and the
prerequisite for the Postgres content adapters (the bundle is what they insert).

It is pure and side-effect free so it can be unit tested with in-memory batch
dictionaries shaped like ``acteos_rule_engine.authoring.loader.load_batch``.

Honesty guarantees (no fabricated data):
- The certification gate runs first; a ``no_go`` bundle is refused, and a
  ``conditional_go`` bundle requires ``allow_conditional=True``.
- Claims whose ``snapshot_id`` is missing/``pending`` are surfaced in
  ``provenance_pending`` and are NOT emitted as ``content.source_claims`` rows,
  because that table's ``source_id``/``snapshot_id`` are NOT-NULL FKs that the
  inbox cannot yet satisfy.
- Rules without ``effective_from`` are surfaced as deferred, because
  ``content.rule_revisions.effective_from`` is ``NOT NULL``;
  :meth:`PublishedBundle.as_content_rows` with ``strict=True`` refuses them.
- ``content.rule_revisions.source_claim_ids`` has no FK in the schema, so
  ``content.rule_sets`` + ``content.rule_revisions`` + ``content.rule_set_members``
  are FK-safe to publish independently of the (deferred) source_claims.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from .. import ENGINE_VERSION
from .certification import (
    VERDICT_CONDITIONAL,
    VERDICT_NO_GO,
    CertificationReport,
    certify_batches,
)

# Stable namespace for deterministic uuid5 identity minting. Computed once at
# import time from a fixed URL, so it never changes across runs/machines.
ACTEOS_NAMESPACE: uuid.UUID = uuid.uuid5(uuid.NAMESPACE_URL, "acteos.ro/lifeos-romania")

CONTENT_SCHEMA_VERSION = "2.1.0"
DEFAULT_REVISION = 1

# content.review_status enum (db/0001_init.sql).
REVIEW_STATUS_VALUES: frozenset[str] = frozenset(
    {
        "draft",
        "in_review",
        "approved",
        "active",
        "stale",
        "hard_expired",
        "withdrawn",
        "superseded",
        "conflicting",
    }
)

# content.freshness_class enum (db/0001_init.sql).
FRESHNESS_CLASSES: frozenset[str] = frozenset({"critical", "operational", "explanatory"})


class PublishError(RuntimeError):
    """Raised when a bundle cannot be compiled or published safely."""

    def __init__(self, message: str, report: CertificationReport | None = None) -> None:
        super().__init__(message)
        self.report = report


def mint_uuid(*parts: str) -> str:
    """Deterministic uuid5 from the ActeOS namespace over ``parts``."""

    return str(uuid.uuid5(ACTEOS_NAMESPACE, ":".join(parts)))


def _review_status(value: Any) -> str:
    return value if value in REVIEW_STATUS_VALUES else "draft"


def _batch_id(batch: Mapping[str, Any]) -> str | None:
    ruleset = batch.get("ruleset")
    if isinstance(ruleset, Mapping):
        bid = ruleset.get("batch_id") or batch.get("batch_dir")
    else:
        bid = batch.get("batch_dir")
    return str(bid) if bid is not None else None


def _claims(batch: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    doc = batch.get("claims")
    if isinstance(doc, Mapping):
        return [c for c in (doc.get("claims") or []) if isinstance(c, Mapping)]
    return []


def _rules(batch: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    ruleset = batch.get("ruleset")
    if isinstance(ruleset, Mapping):
        return [r for r in (ruleset.get("rules") or []) if isinstance(r, Mapping)]
    return []


@dataclass(frozen=True)
class SourceClaimRecord:
    id: str
    stable_key: str
    source_ref: str | None
    snapshot_ref: str | None
    statement: str | None
    evidence_excerpt: str | None
    locator: str | None
    authority_level: str | None
    confidence: str | None
    freshness_class: str | None
    published_at: str | None
    accessed_at: str | None
    effective_from: str | None
    effective_to: str | None
    status: str
    batch_id: str | None
    provenance_ready: bool

    def manifest_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "stable_key": self.stable_key,
            "source_ref": self.source_ref,
            "snapshot_ref": self.snapshot_ref,
            "authority_level": self.authority_level,
            "confidence": self.confidence,
            "freshness_class": self.freshness_class,
            "statement": self.statement,
            "effective_from": self.effective_from,
            "effective_to": self.effective_to,
            "status": self.status,
        }


@dataclass(frozen=True)
class RuleRevisionRecord:
    id: str
    canonical_rule_id: str
    revision: int
    event_type_id: str
    jurisdiction_ids: list[str]
    authority_level: str | None
    competence_scope: list[str]
    legal_rank: str | None
    severity: str
    effective_from: str | None
    effective_to: str | None
    predicate: Any
    effects: Any
    source_claim_ids: list[str]
    override_rule_ids: list[str]
    status: str
    batch_id: str | None

    @property
    def publishable(self) -> bool:
        return bool(self.effective_from)

    def manifest_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "canonical_rule_id": self.canonical_rule_id,
            "revision": self.revision,
            "event_type_id": self.event_type_id,
            "jurisdiction_ids": list(self.jurisdiction_ids),
            "authority_level": self.authority_level,
            "competence_scope": list(self.competence_scope),
            "legal_rank": self.legal_rank,
            "severity": self.severity,
            "effective_from": self.effective_from,
            "effective_to": self.effective_to,
            "predicate": self.predicate,
            "effects": self.effects,
            "source_claim_ids": list(self.source_claim_ids),
            "override_rule_ids": list(self.override_rule_ids),
            "status": self.status,
        }

    def as_content_row(self) -> dict[str, Any]:
        # Exact column mapping for content.rule_revisions.
        return {
            "id": self.id,
            "canonical_rule_id": self.canonical_rule_id,
            "revision": self.revision,
            "event_type_id": self.event_type_id,
            "jurisdiction_ids": list(self.jurisdiction_ids),
            "authority_level": self.authority_level,
            "competence_scope": list(self.competence_scope),
            "legal_rank": self.legal_rank,
            "severity": self.severity,
            "effective_from": self.effective_from,
            "effective_to": self.effective_to,
            "predicate": self.predicate,
            "effects": self.effects,
            "source_claim_ids": list(self.source_claim_ids),
            "override_rule_ids": list(self.override_rule_ids),
            "status": self.status,
        }


@dataclass
class PublishedBundle:
    version: str
    manifest_sha256: str
    schema_version: str
    engine_compatibility: str
    scope: list[str]
    rule_revisions: list[RuleRevisionRecord]
    source_claims: list[SourceClaimRecord]
    required_event_type_ids: list[str]
    referenced_step_ids: list[str]
    referenced_requirement_ids: list[str]
    referenced_channel_ids: list[str]
    provenance_pending: list[str]
    issues: list[str] = field(default_factory=list)
    certification: CertificationReport | None = None

    @property
    def rule_set_id(self) -> str:
        return mint_uuid("ruleset", self.version)

    def publishable_revisions(self) -> list[RuleRevisionRecord]:
        return [r for r in self.rule_revisions if r.publishable]

    def deferred_revisions(self) -> list[RuleRevisionRecord]:
        return [r for r in self.rule_revisions if not r.publishable]

    def as_content_rows(self, *, strict: bool = True) -> dict[str, list[dict[str, Any]]]:
        """Emit FK-safe content rows (rule_sets + rule_revisions + members).

        With ``strict=True`` (default) refuse to emit if any rule lacks
        ``effective_from`` (NOT NULL in content.rule_revisions).
        """

        deferred = self.deferred_revisions()
        if strict and deferred:
            raise PublishError(
                f"{len(deferred)} rule revision(s) lack effective_from; cannot emit "
                "content.rule_revisions rows (NOT NULL). Re-run with strict=False to "
                "emit only the publishable subset."
            )

        rule_set_id = self.rule_set_id
        rule_sets = [
            {
                "id": rule_set_id,
                "version": self.version,
                "scope": list(self.scope),
                "schema_version": self.schema_version,
                "engine_compatibility": self.engine_compatibility,
                "manifest_sha256": self.manifest_sha256,
                "status": "draft",
                "approved_by": [],
                "published_by": None,
                "published_at": None,
                "supersedes_ruleset_id": None,
            }
        ]
        publishable = self.publishable_revisions()
        rule_revisions = [r.as_content_row() for r in publishable]
        rule_set_members = [
            {"rule_set_id": rule_set_id, "rule_revision_id": r.id} for r in publishable
        ]
        return {
            "content.rule_sets": rule_sets,
            "content.rule_revisions": rule_revisions,
            "content.rule_set_members": rule_set_members,
        }

    def summary(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "manifest_sha256": self.manifest_sha256,
            "schema_version": self.schema_version,
            "engine_compatibility": self.engine_compatibility,
            "scope": list(self.scope),
            "rule_revision_count": len(self.rule_revisions),
            "publishable_rule_count": len(self.publishable_revisions()),
            "deferred_rule_count": len(self.deferred_revisions()),
            "source_claim_count": len(self.source_claims),
            "provenance_pending_count": len(self.provenance_pending),
            "required_event_type_ids": list(self.required_event_type_ids),
            "referenced_step_ids": list(self.referenced_step_ids),
            "referenced_requirement_ids": list(self.referenced_requirement_ids),
            "referenced_channel_ids": list(self.referenced_channel_ids),
            "issue_count": len(self.issues),
            "certification_verdict": (
                self.certification.verdict if self.certification else None
            ),
        }

    def to_manifest(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "manifest_sha256": self.manifest_sha256,
            "schema_version": self.schema_version,
            "engine_compatibility": self.engine_compatibility,
            "scope": list(self.scope),
            "rule_set_id": self.rule_set_id,
            "rule_revisions": [r.manifest_dict() for r in self.rule_revisions],
            "source_claims": [c.manifest_dict() for c in self.source_claims],
            "required_event_type_ids": list(self.required_event_type_ids),
            "referenced_step_ids": list(self.referenced_step_ids),
            "referenced_requirement_ids": list(self.referenced_requirement_ids),
            "referenced_channel_ids": list(self.referenced_channel_ids),
            "provenance_pending": list(self.provenance_pending),
            "issues": list(self.issues),
        }


def _canonical_content(
    *,
    schema_version: str,
    engine_compatibility: str,
    scope: list[str],
    rule_revisions: list[RuleRevisionRecord],
    source_claims: list[SourceClaimRecord],
    required_event_type_ids: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": schema_version,
        "engine_compatibility": engine_compatibility,
        "scope": sorted(scope),
        "rule_revisions": [r.manifest_dict() for r in rule_revisions],
        "source_claims": [c.manifest_dict() for c in source_claims],
        "required_event_type_ids": sorted(required_event_type_ids),
    }


def compile_bundle(
    batches: Iterable[Mapping[str, Any]],
    *,
    scope: Iterable[str] = ("R1",),
    schemas: Mapping[str, Any] | None = None,
    allow_conditional: bool = False,
    revision: int = DEFAULT_REVISION,
) -> PublishedBundle:
    """Compile certified inbox batches into a deterministic PublishedBundle."""

    batches = list(batches)
    report = certify_batches(batches, schemas=schemas)
    if report.verdict == VERDICT_NO_GO:
        raise PublishError(
            "certification verdict is no_go; refusing to compile a release bundle.",
            report,
        )
    if report.verdict == VERDICT_CONDITIONAL and not allow_conditional:
        raise PublishError(
            "certification verdict is conditional_go; pass allow_conditional=True "
            "to compile with documented warnings.",
            report,
        )

    issues: list[str] = []

    # --- Pass 1: claims -> deterministic uuids (collision-checked). ---------
    claim_records: dict[str, SourceClaimRecord] = {}
    claim_uuid_by_key: dict[str, str] = {}
    for batch in batches:
        bid = _batch_id(batch)
        for claim in _claims(batch):
            cid = claim.get("id")
            if not isinstance(cid, str):
                continue
            if cid in claim_records:
                issues.append(f"CLAIM_ID_COLLISION:{cid}")
                continue
            freshness = claim.get("freshness_class")
            if freshness not in FRESHNESS_CLASSES:
                issues.append(f"CLAIM_FRESHNESS_MISSING:{cid}")
            snapshot_ref = claim.get("snapshot_id")
            provenance_ready = snapshot_ref not in (None, "", "pending")
            claim_uuid = mint_uuid("claim", cid)
            claim_uuid_by_key[cid] = claim_uuid
            claim_records[cid] = SourceClaimRecord(
                id=claim_uuid,
                stable_key=cid,
                source_ref=claim.get("source_id"),
                snapshot_ref=snapshot_ref,
                statement=claim.get("statement"),
                evidence_excerpt=claim.get("evidence_excerpt"),
                locator=claim.get("locator"),
                authority_level=claim.get("authority_level"),
                confidence=claim.get("confidence"),
                freshness_class=freshness if freshness in FRESHNESS_CLASSES else None,
                published_at=claim.get("published_at"),
                accessed_at=claim.get("accessed_at"),
                effective_from=claim.get("effective_from"),
                effective_to=claim.get("effective_to"),
                status=_review_status(claim.get("status")),
                batch_id=bid,
                provenance_ready=provenance_ready,
            )

    # --- Pass 2: rule ids -> deterministic uuids (for override resolution). --
    rule_uuid_by_id: dict[str, str] = {}
    raw_rules: list[tuple[str | None, Mapping[str, Any], str]] = []
    for batch in batches:
        bid = _batch_id(batch)
        for rule in _rules(batch):
            rid = rule.get("id")
            canonical = str(rule.get("canonical_rule_id") or rid)
            rule_uuid = mint_uuid("rule", canonical, str(revision))
            if isinstance(rid, str):
                if rid in rule_uuid_by_id:
                    issues.append(f"RULE_ID_COLLISION:{rid}")
                rule_uuid_by_id[rid] = rule_uuid
            raw_rules.append((bid, rule, rule_uuid))

    # --- Pass 3: build rule revision records. -------------------------------
    rule_revisions: list[RuleRevisionRecord] = []
    required_events: set[str] = set()
    step_ids: set[str] = set()
    requirement_ids: set[str] = set()
    channel_ids: set[str] = set()

    for bid, rule, rule_uuid in raw_rules:
        event_type_id = rule.get("event_type_id")
        if isinstance(event_type_id, str):
            required_events.add(event_type_id)

        claim_uuids: list[str] = []
        for cid in rule.get("source_claim_ids") or []:
            mapped = claim_uuid_by_key.get(cid)
            if mapped is not None and mapped not in claim_uuids:
                claim_uuids.append(mapped)

        override_uuids: list[str] = []
        for tid in rule.get("override_rule_ids") or []:
            mapped = rule_uuid_by_id.get(tid)
            if mapped is None:
                issues.append(f"OVERRIDE_TARGET_UNRESOLVED:{tid}")
            elif mapped not in override_uuids:
                override_uuids.append(mapped)

        for eff in rule.get("effects") or []:
            if not isinstance(eff, Mapping):
                continue
            etype = eff.get("type")
            if etype == "override_rule":
                tid = eff.get("rule_id") or eff.get("target_rule_id") or eff.get("value")
                if tid:
                    mapped = rule_uuid_by_id.get(tid)
                    if mapped is None:
                        issues.append(f"OVERRIDE_TARGET_UNRESOLVED:{tid}")
                    elif mapped not in override_uuids:
                        override_uuids.append(mapped)
            elif etype in ("include_step", "exclude_step", "set_deadline"):
                if eff.get("step_id"):
                    step_ids.add(eff["step_id"])
            elif etype in ("include_requirement", "set_requirement_obligation"):
                if eff.get("requirement_id"):
                    requirement_ids.add(eff["requirement_id"])
            elif etype == "attach_channel":
                if eff.get("channel_id"):
                    channel_ids.add(eff["channel_id"])

        rule_revisions.append(
            RuleRevisionRecord(
                id=rule_uuid,
                canonical_rule_id=str(rule.get("canonical_rule_id") or rule.get("id")),
                revision=revision,
                event_type_id=str(event_type_id),
                jurisdiction_ids=[
                    j for j in (rule.get("jurisdiction_ids") or []) if isinstance(j, str)
                ],
                authority_level=rule.get("authority_level"),
                competence_scope=[
                    c for c in (rule.get("competence_scope") or []) if isinstance(c, str)
                ],
                legal_rank=rule.get("legal_rank"),
                severity=str(rule.get("severity")),
                effective_from=rule.get("effective_from"),
                effective_to=rule.get("effective_to"),
                predicate=rule.get("when") or {"op": "const", "value": True},
                effects=rule.get("effects") or [],
                source_claim_ids=claim_uuids,
                override_rule_ids=override_uuids,
                status=_review_status(rule.get("status")),
                batch_id=bid,
            )
        )

    rule_revisions.sort(key=lambda r: (r.canonical_rule_id, r.revision))
    source_claims = sorted(claim_records.values(), key=lambda c: c.stable_key)
    scope_list = sorted({s for s in scope if isinstance(s, str)})

    canonical = _canonical_content(
        schema_version=CONTENT_SCHEMA_VERSION,
        engine_compatibility=ENGINE_VERSION,
        scope=scope_list,
        rule_revisions=rule_revisions,
        source_claims=source_claims,
        required_event_type_ids=sorted(required_events),
    )
    manifest_sha256 = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()
    version = f"r1-{manifest_sha256[:12]}"

    provenance_pending = sorted(
        c.stable_key for c in source_claims if not c.provenance_ready
    )

    return PublishedBundle(
        version=version,
        manifest_sha256=manifest_sha256,
        schema_version=CONTENT_SCHEMA_VERSION,
        engine_compatibility=ENGINE_VERSION,
        scope=scope_list,
        rule_revisions=rule_revisions,
        source_claims=source_claims,
        required_event_type_ids=sorted(required_events),
        referenced_step_ids=sorted(step_ids),
        referenced_requirement_ids=sorted(requirement_ids),
        referenced_channel_ids=sorted(channel_ids),
        provenance_pending=provenance_pending,
        issues=issues,
        certification=report,
    )
