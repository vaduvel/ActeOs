"""Release certification governance checks for ActeOS rule batches.

This module implements the *automatable* subset of the
``acteos-release-certification`` skill: the deterministic content gates that
decide whether a research/authoring batch is allowed to be promoted from the
inbox into a published, activatable ruleset.

It is intentionally pure and side-effect free so it can be unit tested with
in-memory batch dictionaries. The thin CLI wrapper lives in
``infra/scripts/certify_release.py`` and is responsible for discovering and
loading batches from disk before delegating to :func:`certify_batches`.

Design references (grounded in repo, not guessed):
- Effect types: ``acteos_rule_engine.authoring.effects.EFFECT_TYPES``.
- Batch shape: ``acteos_rule_engine.authoring.loader.load_batch`` returns
  ``{"batch_dir", "ruleset", "fixtures", "claims"}`` where ``ruleset`` is the
  parsed ``rules.yaml`` (``{"rules": [...]}``) and ``claims`` is the parsed
  ``source_claims.yaml`` (``{"claims": [...]}``) or ``None``.
- Severity enum (rule.schema.json): critical | operational | explanatory.
- Claim confidence enum (source_claim.schema.json): verified |
  verified_with_local_gap | needs_confirmation | conflicting | expired.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Optional

from .effects import EFFECT_TYPES

# Effects that change what the citizen is legally/operationally required to do.
# These MUST be backed by a dated, cited claim before promotion.
NORMATIVE_EFFECT_TYPES: frozenset[str] = frozenset(
    {
        "block",
        "include_step",
        "exclude_step",
        "include_requirement",
        "set_requirement_obligation",
        "set_deadline",
        "override_rule",
        "trigger_child_event",
    }
)

# Advisory effects: helpful, but do not by themselves create an obligation.
ADVISORY_EFFECT_TYPES: frozenset[str] = frozenset(EFFECT_TYPES) - NORMATIVE_EFFECT_TYPES

# Effects that exist to DECLARE and contain an unresolved conflict rather than
# to assert a citizen obligation. Per the v2.1 conflict model (see effects.py /
# ADR-015) source conflicts are surfaced via ``block`` (plus ``require_confirmation``);
# ``flag_conflict`` is the documented extension. A rule whose effects are drawn
# EXCLUSIVELY from this set suppresses an uncertain value and asks for
# confirmation -- it does not assert content -- so a contradicted claim it cites
# is a handled conflict, not an uncited obligation. NOTE: this set deliberately
# overlaps both partitions above and is NOT part of the normative/advisory
# partition.
CONFLICT_DECLARATION_EFFECT_TYPES: frozenset[str] = frozenset(
    {"block", "require_confirmation", "flag_conflict"}
)

# Confidence values acceptable for a *critical* normative rule.
CRITICAL_OK_CONFIDENCE: frozenset[str] = frozenset(
    {"verified", "verified_with_local_gap"}
)

# Confidence values that are never acceptable for any activated normative rule.
HARD_BAD_CONFIDENCE: frozenset[str] = frozenset({"expired", "conflicting"})

BLOCKER = "blocker"
WARNING = "warning"
INFO = "info"

VERDICT_GO = "go"
VERDICT_CONDITIONAL = "conditional_go"
VERDICT_NO_GO = "no_go"

# Governance conditions from the skill that cannot be verified from inbox
# content alone and MUST be enforced at publish/activation time.
PUBLISH_TIME_OBLIGATIONS: tuple[str, ...] = (
    "four-eyes approval: the author of critical content must not be the sole approver",
    "rule bundle manifest + checksums + signature metadata + SBOM/provenance",
    "feature flags / kill switches wired for every risk-bearing ruleset",
    "migrations replayed on staging with restore/rollback demonstrated",
    "staged rollout cohort with explicit abort criteria",
)


@dataclass(frozen=True)
class Finding:
    """A single certification observation."""

    level: str
    code: str
    message: str
    batch_id: Optional[str] = None
    rule_id: Optional[str] = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "level": self.level,
            "code": self.code,
            "message": self.message,
            "batch_id": self.batch_id,
            "rule_id": self.rule_id,
        }


@dataclass
class CertificationReport:
    """Aggregated certification result across one or more batches."""

    findings: list[Finding] = field(default_factory=list)
    batch_ids: list[str] = field(default_factory=list)
    rule_count: int = 0

    @property
    def blockers(self) -> list[Finding]:
        return [f for f in self.findings if f.level == BLOCKER]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.level == WARNING]

    @property
    def infos(self) -> list[Finding]:
        return [f for f in self.findings if f.level == INFO]

    @property
    def verdict(self) -> str:
        if self.blockers:
            return VERDICT_NO_GO
        if self.warnings:
            return VERDICT_CONDITIONAL
        return VERDICT_GO

    def is_releasable(self, *, allow_conditional: bool = False) -> bool:
        if self.verdict == VERDICT_GO:
            return True
        if self.verdict == VERDICT_CONDITIONAL:
            return allow_conditional
        return False

    def as_dict(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict,
            "batch_count": len(self.batch_ids),
            "batch_ids": list(self.batch_ids),
            "rule_count": self.rule_count,
            "blocker_count": len(self.blockers),
            "warning_count": len(self.warnings),
            "info_count": len(self.infos),
            "findings": [f.as_dict() for f in self.findings],
            "publish_time_obligations": list(PUBLISH_TIME_OBLIGATIONS),
        }


def _rule_effect_types(rule: Mapping[str, Any]) -> list[str]:
    effects = rule.get("effects") or []
    types: list[str] = []
    for effect in effects:
        if isinstance(effect, Mapping):
            etype = effect.get("type")
            if isinstance(etype, str):
                types.append(etype)
    return types


def _is_normative(rule: Mapping[str, Any]) -> bool:
    return any(t in NORMATIVE_EFFECT_TYPES for t in _rule_effect_types(rule))


def _is_conflict_declaration_only(rule: Mapping[str, Any]) -> bool:
    """True when a rule's effects ONLY declare/contain a conflict.

    Such a rule (``block`` / ``require_confirmation`` / ``flag_conflict`` and
    nothing that asserts a citizen obligation) exists to *suppress* an uncertain
    value and request confirmation -- per the v2.1 conflict model it is the
    intended way to surface an unresolved source conflict. A contradicted claim
    it cites is therefore a handled conflict rather than an uncited obligation.
    """
    types = _rule_effect_types(rule)
    if not types:
        return False
    if not any(t in CONFLICT_DECLARATION_EFFECT_TYPES for t in types):
        return False
    return all(t in CONFLICT_DECLARATION_EFFECT_TYPES for t in types)


def _claims_index(batch: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    claims_doc = batch.get("claims")
    index: dict[str, Mapping[str, Any]] = {}
    if isinstance(claims_doc, Mapping):
        for claim in claims_doc.get("claims") or []:
            if isinstance(claim, Mapping):
                cid = claim.get("id")
                if isinstance(cid, str):
                    index[cid] = claim
    return index


def _certify_rule(
    rule: Mapping[str, Any],
    claims: Mapping[str, Mapping[str, Any]],
    batch_id: Optional[str],
) -> list[Finding]:
    findings: list[Finding] = []
    rule_id_raw = rule.get("id")
    rule_id = str(rule_id_raw) if rule_id_raw is not None else None
    is_critical = rule.get("severity") == "critical"
    normative = _is_normative(rule)
    conflict_declaration = _is_conflict_declaration_only(rule)

    raw_claim_ids = rule.get("source_claim_ids") or []
    claim_ids = [c for c in raw_claim_ids if isinstance(c, str)]

    # 1. Normative rules must be dated and cited.
    if normative:
        if not rule.get("effective_from"):
            findings.append(
                Finding(
                    BLOCKER,
                    "NORMATIVE_RULE_WITHOUT_EFFECTIVE_FROM",
                    "Normative rule has no effective_from; cannot place it on the legal timeline.",
                    batch_id,
                    rule_id,
                )
            )
        if not claim_ids:
            findings.append(
                Finding(
                    BLOCKER,
                    "NORMATIVE_RULE_WITHOUT_CLAIM",
                    "Normative rule has no source_claim_ids; obligation is uncited.",
                    batch_id,
                    rule_id,
                )
            )

    # 2. Critical rules must be cited regardless (defense-in-depth vs schema).
    if is_critical and not claim_ids:
        findings.append(
            Finding(
                BLOCKER,
                "CRITICAL_RULE_WITHOUT_CLAIM",
                "Critical rule has no source_claim_ids.",
                batch_id,
                rule_id,
            )
        )

    # 3. Claim-level checks.
    for cid in claim_ids:
        claim = claims.get(cid)
        if claim is None:
            findings.append(
                Finding(
                    BLOCKER,
                    "DANGLING_CLAIM_REFERENCE",
                    f"source_claim_id '{cid}' does not resolve to a claim in this batch.",
                    batch_id,
                    rule_id,
                )
            )
            continue

        confidence = claim.get("confidence")
        status = claim.get("status")
        snapshot_id = claim.get("snapshot_id")

        if is_critical:
            # A conflict-declaration-only rule (block/require_confirmation/
            # flag_conflict and nothing that asserts content) that cites an
            # EXPLICITLY contradicted claim is the intended, handled way to
            # surface an unresolved source conflict: the uncertain value is
            # already suppressed by the rule. Treat it as a conditional_go
            # caveat rather than a hard no_go blocker. `expired` is a freshness
            # failure (stale source), not a declared conflict, so it is not
            # downgraded here and still blocks via the branch below.
            declared_conflict = (
                conflict_declaration
                and bool(claim.get("contradiction_claim_ids"))
                and (confidence == "conflicting" or status == "conflicting")
            )
            if declared_conflict:
                findings.append(
                    Finding(
                        WARNING,
                        "CRITICAL_CONFLICT_DECLARED",
                        (
                            f"Critical conflict-declaration rule surfaces an unresolved "
                            f"source conflict via claim '{cid}' (confidence={confidence!r}, "
                            f"status={status!r}); the user-facing value is suppressed by the "
                            f"rule's block/require_confirmation pending resolution."
                        ),
                        batch_id,
                        rule_id,
                    )
                )
            else:
                if confidence in HARD_BAD_CONFIDENCE:
                    findings.append(
                        Finding(
                            BLOCKER,
                            "CRITICAL_CLAIM_BAD_CONFIDENCE",
                            f"Critical rule relies on claim '{cid}' with confidence '{confidence}'.",
                            batch_id,
                            rule_id,
                        )
                    )
                elif confidence not in CRITICAL_OK_CONFIDENCE:
                    findings.append(
                        Finding(
                            BLOCKER,
                            "CRITICAL_CLAIM_UNVERIFIED",
                            f"Critical rule relies on claim '{cid}' with non-verified confidence '{confidence}'.",
                            batch_id,
                            rule_id,
                        )
                    )
                if status not in (None, "active"):
                    findings.append(
                        Finding(
                            BLOCKER,
                            "CRITICAL_CLAIM_NOT_ACTIVE",
                            f"Critical rule relies on claim '{cid}' with status '{status}'.",
                            batch_id,
                            rule_id,
                        )
                    )
        else:
            if confidence in HARD_BAD_CONFIDENCE:
                findings.append(
                    Finding(
                        WARNING,
                        "CLAIM_BAD_CONFIDENCE",
                        f"Rule relies on claim '{cid}' with confidence '{confidence}'.",
                        batch_id,
                        rule_id,
                    )
                )
            elif confidence == "needs_confirmation" and normative:
                findings.append(
                    Finding(
                        WARNING,
                        "CLAIM_NEEDS_CONFIRMATION",
                        f"Normative rule relies on claim '{cid}' needing confirmation.",
                        batch_id,
                        rule_id,
                    )
                )
            if status not in (None, "active"):
                findings.append(
                    Finding(
                        WARNING,
                        "CLAIM_NOT_ACTIVE",
                        f"Rule relies on claim '{cid}' with status '{status}'.",
                        batch_id,
                        rule_id,
                    )
                )

        # Provenance: a pending snapshot is acceptable in inbox but must be
        # resolved before production; surface as a warning for normative rules.
        if normative and snapshot_id in (None, "", "pending"):
            findings.append(
                Finding(
                    WARNING,
                    "PROVENANCE_NOT_SNAPSHOTTED",
                    f"Claim '{cid}' has no resolved snapshot_id (got {snapshot_id!r}).",
                    batch_id,
                    rule_id,
                )
            )

    # 4. Unknown effect types (defense vs typos schema validation might miss).
    for etype in _rule_effect_types(rule):
        if etype not in EFFECT_TYPES:
            findings.append(
                Finding(
                    BLOCKER,
                    "UNKNOWN_EFFECT_TYPE",
                    f"Rule uses unknown effect type '{etype}'.",
                    batch_id,
                    rule_id,
                )
            )

    return findings


def certify_batch(
    batch: Mapping[str, Any],
    *,
    schemas: Optional[Mapping[str, Any]] = None,
) -> list[Finding]:
    """Certify a single loaded batch dict and return its findings."""

    findings: list[Finding] = []
    ruleset = batch.get("ruleset")
    if not isinstance(ruleset, Mapping):
        findings.append(
            Finding(
                BLOCKER,
                "BATCH_WITHOUT_RULESET",
                "Batch has no parsed ruleset (rules.yaml missing or invalid).",
                str(batch.get("batch_dir")) if batch.get("batch_dir") else None,
            )
        )
        return findings

    batch_id_raw = ruleset.get("batch_id") or batch.get("batch_dir")
    batch_id = str(batch_id_raw) if batch_id_raw is not None else None

    # Optional JSON-schema validation, if schemas were provided by the caller.
    if schemas is not None:
        try:
            from .validate import validate_batch

            report = validate_batch(batch, schemas)
        except Exception as exc:  # defensive: never crash the gate
            findings.append(
                Finding(
                    BLOCKER,
                    "SCHEMA_VALIDATION_FAILED",
                    f"Schema validation raised: {exc!r}",
                    batch_id,
                )
            )
        else:
            if not report.ok:
                for err in report.errors:
                    findings.append(
                        Finding(BLOCKER, "SCHEMA_INVALID", str(err), batch_id)
                    )

    claims = _claims_index(batch)
    for rule in ruleset.get("rules") or []:
        if not isinstance(rule, Mapping):
            findings.append(
                Finding(BLOCKER, "MALFORMED_RULE", "Rule entry is not a mapping.", batch_id)
            )
            continue
        findings.extend(_certify_rule(rule, claims, batch_id))

    return findings


def certify_batches(
    batches: Iterable[Mapping[str, Any]],
    *,
    schemas: Optional[Mapping[str, Any]] = None,
) -> CertificationReport:
    """Certify many loaded batches and aggregate them into one report."""

    report = CertificationReport()
    for batch in batches:
        ruleset = batch.get("ruleset")
        if isinstance(ruleset, Mapping):
            batch_id_raw = ruleset.get("batch_id") or batch.get("batch_dir")
            rules = ruleset.get("rules") or []
            report.rule_count += sum(1 for r in rules if isinstance(r, Mapping))
        else:
            batch_id_raw = batch.get("batch_dir")
        if batch_id_raw is not None:
            report.batch_ids.append(str(batch_id_raw))
        report.findings.extend(certify_batch(batch, schemas=schemas))
    return report
