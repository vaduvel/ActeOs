"""Compile governed step/requirement templates into content.* rows.

``content.step_templates`` and ``content.requirement_templates`` hold the
reusable, event-agnostic building blocks that journeys instantiate
(``app.journey_steps`` / ``app.journey_requirements`` copy title_ro /
instruction_ro from them). Rules only *reference* these templates by id through
``include_step`` / ``exclude_step`` / ``include_requirement`` /
``set_requirement_obligation`` / ``set_deadline`` effects; the human-readable
content is authored once per template in each batch's optional ``templates.yaml``:

    step_templates:
      - id: apply_minor_passport
        title_ro: "Depune cererea de pasaport"
        instruction_ro: "..."
    requirement_templates:
      - id: req.minor_birth_certificate
        title_ro: "Certificat de nastere"
        obligation: mandatory
        timing: now

Honesty (no fabrication): a template that lacks a NOT NULL column is *deferred*
(surfaced in :attr:`CompiledTemplates.deferred`) rather than invented — exactly
like rule revisions without ``effective_from``. The NOT NULL columns are, per
``db/0001_init.sql``:
  - step_templates: id, semantic_key, title_ro, instruction_ro
    (semantic_key defaults to id; sequence_hint/evidence/recovery/status have
    DB defaults).
  - requirement_templates: id, title_ro, obligation, timing
    (obligation in {mandatory,conditional,optional}; timing in {now,later}).

The module is pure and side-effect free, so it is unit tested with in-memory
batch dicts shaped like ``acteos_rule_engine.authoring.loader.load_batch``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

OBLIGATIONS: frozenset[str] = frozenset({"mandatory", "conditional", "optional"})
TIMINGS: frozenset[str] = frozenset({"now", "later"})
DEFAULT_SEQUENCE_HINT = 100
DEFAULT_STATUS = "draft"


def _str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [v for v in value if isinstance(v, str)]


def _nonempty_str(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


@dataclass(frozen=True)
class StepTemplateRecord:
    id: str
    semantic_key: str
    title_ro: str
    instruction_ro: str
    sequence_hint: int
    completion_evidence_ro: list[str]
    recovery_actions_ro: list[str]
    status: str

    def as_content_row(self) -> dict[str, Any]:
        # Exact column mapping for content.step_templates.
        return {
            "id": self.id,
            "semantic_key": self.semantic_key,
            "title_ro": self.title_ro,
            "instruction_ro": self.instruction_ro,
            "sequence_hint": self.sequence_hint,
            "completion_evidence_ro": list(self.completion_evidence_ro),
            "recovery_actions_ro": list(self.recovery_actions_ro),
            "status": self.status,
        }


@dataclass(frozen=True)
class RequirementTemplateRecord:
    id: str
    title_ro: str
    description_ro: str | None
    obligation: str
    timing: str
    accepted_forms: list[str]
    validity: dict[str, Any]
    readiness_checks: list[str]
    status: str

    def as_content_row(self) -> dict[str, Any]:
        # Exact column mapping for content.requirement_templates.
        return {
            "id": self.id,
            "title_ro": self.title_ro,
            "description_ro": self.description_ro,
            "obligation": self.obligation,
            "timing": self.timing,
            "accepted_forms": list(self.accepted_forms),
            "validity": dict(self.validity),
            "readiness_checks": list(self.readiness_checks),
            "status": self.status,
        }


@dataclass(frozen=True)
class CompiledTemplates:
    step_templates: list[StepTemplateRecord]
    requirement_templates: list[RequirementTemplateRecord]
    deferred: list[str]


@dataclass(frozen=True)
class TemplateCoverage:
    missing_steps: list[str]
    missing_requirements: list[str]

    @property
    def ok(self) -> bool:
        return not self.missing_steps and not self.missing_requirements


def _templates_doc(batch: Mapping[str, Any]) -> Mapping[str, Any]:
    doc = batch.get("templates")
    return doc if isinstance(doc, Mapping) else {}


def compile_templates(batches: Iterable[Mapping[str, Any]]) -> CompiledTemplates:
    """Compile authored templates into deterministic, FK-safe content records."""

    steps: dict[str, StepTemplateRecord] = {}
    requirements: dict[str, RequirementTemplateRecord] = {}
    deferred: list[str] = []

    for batch in batches:
        doc = _templates_doc(batch)

        for raw in doc.get("step_templates") or []:
            if not isinstance(raw, Mapping):
                continue
            sid = _nonempty_str(raw.get("id"))
            if sid is None:
                continue
            title = _nonempty_str(raw.get("title_ro"))
            if title is None:
                deferred.append(f"step:{sid}:missing_title_ro")
                continue
            instruction = _nonempty_str(raw.get("instruction_ro"))
            if instruction is None:
                deferred.append(f"step:{sid}:missing_instruction_ro")
                continue
            if sid in steps:
                deferred.append(f"step:{sid}:duplicate")
                continue
            sequence = raw.get("sequence_hint")
            steps[sid] = StepTemplateRecord(
                id=sid,
                semantic_key=_nonempty_str(raw.get("semantic_key")) or sid,
                title_ro=title,
                instruction_ro=instruction,
                sequence_hint=(
                    sequence
                    if isinstance(sequence, int) and not isinstance(sequence, bool)
                    else DEFAULT_SEQUENCE_HINT
                ),
                completion_evidence_ro=_str_list(raw.get("completion_evidence_ro")),
                recovery_actions_ro=_str_list(raw.get("recovery_actions_ro")),
                status=_nonempty_str(raw.get("status")) or DEFAULT_STATUS,
            )

        for raw in doc.get("requirement_templates") or []:
            if not isinstance(raw, Mapping):
                continue
            rid = _nonempty_str(raw.get("id"))
            if rid is None:
                continue
            title = _nonempty_str(raw.get("title_ro"))
            if title is None:
                deferred.append(f"requirement:{rid}:missing_title_ro")
                continue
            obligation = raw.get("obligation")
            if obligation not in OBLIGATIONS:
                deferred.append(f"requirement:{rid}:invalid_obligation")
                continue
            timing = raw.get("timing")
            if timing not in TIMINGS:
                deferred.append(f"requirement:{rid}:invalid_timing")
                continue
            if rid in requirements:
                deferred.append(f"requirement:{rid}:duplicate")
                continue
            validity = raw.get("validity")
            requirements[rid] = RequirementTemplateRecord(
                id=rid,
                title_ro=title,
                description_ro=_nonempty_str(raw.get("description_ro")),
                obligation=str(obligation),
                timing=str(timing),
                accepted_forms=_str_list(raw.get("accepted_forms")),
                validity=dict(validity) if isinstance(validity, Mapping) else {},
                readiness_checks=_str_list(raw.get("readiness_checks")),
                status=_nonempty_str(raw.get("status")) or DEFAULT_STATUS,
            )

    return CompiledTemplates(
        step_templates=sorted(steps.values(), key=lambda s: s.id),
        requirement_templates=sorted(requirements.values(), key=lambda r: r.id),
        deferred=sorted(deferred),
    )


def template_coverage(
    *,
    referenced_step_ids: Iterable[str],
    referenced_requirement_ids: Iterable[str],
    compiled: CompiledTemplates,
) -> TemplateCoverage:
    """Which referenced step/requirement ids lack an authored template row.

    Decoupled from the publish bundle (takes plain id iterables) so the publish
    pipeline can report unresolved journey content without a circular import.
    """

    step_ids = {s.id for s in compiled.step_templates}
    req_ids = {r.id for r in compiled.requirement_templates}
    return TemplateCoverage(
        missing_steps=sorted({s for s in referenced_step_ids if s not in step_ids}),
        missing_requirements=sorted(
            {r for r in referenced_requirement_ids if r not in req_ids}
        ),
    )
