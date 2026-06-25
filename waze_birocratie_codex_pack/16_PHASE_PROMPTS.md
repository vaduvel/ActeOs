# Phase prompts for Codex

These prompts are executable phase contracts. Run them in order. A phase cannot be marked complete while its exit gate is red.

## P0 — Foundation and reproducibility

**Stories:** WB-001…WB-005.

**Prompt:**

Create the monorepo skeleton, pin toolchains, add Docker Compose, CI foundations, ADR process and root Makefile. Do not implement product logic. Ensure a clean checkout can run `make doctor`, `make bootstrap`, `make up` and `make smoke-local`. Create `IMPLEMENTATION_STATUS.md`, record exact versions and add an ADR for any version deviation from the workbook.

**Exit gate:**

- repository tree matches architecture;
- all lockfiles committed;
- local infrastructure healthy;
- CI parses and runs a minimal smoke;
- no secrets or generated junk committed.

## P1 — Contracts, persistence and cryptographic foundations

**Stories:** WB-010…WB-024.

**Prompt:**

Implement canonical JSON Schemas, code generation, cross-language hashing, error vocabulary, PostgreSQL models/migrations, repositories, field encryption, append-only audit and idempotency. Use `09_DATABASE_SCHEMA.sql` as target model while expressing it through incremental Alembic migrations. Add positive and negative schema fixtures. Make sensitive-field encryption key-versioned and test rotation.

**Exit gate:**

- schemas reject text conditions and unknown critical fields;
- Python/Kotlin/TypeScript models compile;
- golden hash is identical in all languages;
- migrate up/down/up passes;
- audit tampering fails;
- encryption and idempotency concurrency tests pass.

## P2 — Deterministic rule engine

**Stories:** WB-030…WB-035.

**Prompt:**

Build the pure rule-engine package with typed predicates, three-valued logic, temporal and jurisdictional applicability, lawful precedence, stable graph ordering, freshness gates, deterministic resolution and route diff. The package must have no network, database, clock or LLM dependency; inject time and bundle as input. Implement property-based tests and the route fixture suite.

**Exit gate:**

- no `eval`/dynamic expression execution;
- 95%+ engine coverage and 100% critical branches;
- all invariants and golden fixtures pass;
- cycle/conflict/stale critical rules fail safely;
- deterministic hash survives repeated and cross-process runs.

## P3 — Source ingestion and content lifecycle

**Stories:** WB-040…WB-045.

**Prompt:**

Implement a safe source registry, bounded fetcher, immutable snapshots, normalization, diff severity, impact analysis, optional schema-bound AI draft extraction, human review services, atomic publishing, rollback and staleness scheduler. Build the AI adapter so the entire system works with `AI_EXTRACTION_ENABLED=false`. Protect the fetcher from SSRF and hostile content. Preserve evidence required for audit, subject to copyright-minimizing storage policy.

**Exit gate:**

- controlled HTML/PDF fixtures traverse fetch-to-draft;
- AI output cannot publish itself;
- critical changes require two distinct reviewers;
- staleness alerts are time-travel tested;
- rollback restores the production pointer without deleting history;
- SSRF/malformed document tests pass.

## P4 — API and journey lifecycle

**Stories:** WB-050…WB-055.

**Prompt:**

Implement FastAPI according to `08_API_SPEC.yaml`: health, catalog, route resolution, journeys, facts, requirement states, recalculation, evidence and feedback. Generate or validate the OpenAPI document against the committed contract. Add ownership checks, encrypted facts, optimistic concurrency, problem+json errors, idempotency and privacy-safe logs. Route resolution must perform no external call.

**Exit gate:**

- contract tests pass with no undocumented response fields;
- BOLA/IDOR tests pass;
- p95 target is met locally under the defined load profile;
- logs contain no fixture PII;
- journey create-to-recalculate integration passes.

## P5 — Curator portal

**Stories:** WB-060…WB-065.

**Prompt:**

Build the Next.js curator portal and server-side OIDC/RBAC boundary. Implement source registry, snapshot diff, structured rule editor, claim evidence panel, review, impact, publish, rollback, staleness and feedback operations. Never render untrusted source HTML directly; sanitize or show text. Do not allow a critical author to approve their own change.

**Exit gate:**

- all roles and forbidden actions tested;
- structured editor always emits valid schema;
- XSS/source-content tests pass;
- review and rollback E2E pass;
- dashboards expose SLA and conflict states without raw PII.

## P6 — Android citizen experience

**Stories:** WB-070…WB-077.

**Prompt:**

Build the native Android application using Compose and the architecture in the workbook. Implement accountless onboarding, jurisdiction, controlled intent search, dynamic questionnaire, timeline, next-action screen, checklist, evidence, official channel, feedback and recalculation diff. Add Room cache and offline behavior. Use generated contract models. Follow the design system and the five-question operational standard.

**Exit gate:**

- Android debug/release compile;
- critical Compose UI tests pass;
- flow remains usable offline after initial sync;
- process-death restore works;
- TalkBack and 200% font scale pass critical flow;
- no production fake journeys are visible.

## P7 — Local document readiness

**Stories:** WB-080…WB-085.

**Prompt:**

Implement the local document vault, OCR, bounded document classification, user-confirmed field extraction, formal readiness checks, findings UI and optional metadata-only sync. Protect keys with Android Keystore. Test in airplane mode. Do not claim authenticity and do not upload image bytes or raw OCR by default.

**Exit gate:**

- imported files are protected and deletable;
- OCR/readiness works without network;
- signature ambiguity becomes `unable_to_check`;
- sensitive fields are masked;
- network inspection confirms no document content leaves the device by default;
- metadata sync is disabled until explicit consent.

## P8 — Verified R1 content, official routing and reminders

**Stories:** WB-090…WB-103.

**Prompt:**

Load only the verified official source registry and rule seeds. Complete human-curation placeholders for Timiș/Timișoara through the portal; do not invent missing local facts. Certify preschool and primary bundles with golden route suites, provenance coverage and two-person approval. Implement official-domain allowlisting, safe deep links and reminders. Keep high-school functionality feature-flagged until current local booklet/codes are curated.

**Exit gate:**

- preschool and primary certification reports pass;
- no critical claim lacks evidence;
- local gaps are visible as confirmation states;
- links resolve only through allowed official destinations;
- reminders pass timezone/DST tests;
- canary bundle rollback drill passes.

## P9 — Security, privacy, observability and recovery

**Stories:** WB-110…WB-124.

**Prompt:**

Complete threat model, key/secret controls, API and mobile hardening, privacy rights, consent and retention, DPIA inputs, structured telemetry, SLO dashboards, alerts, runbooks, backups, restore and audit-integrity verification. Map controls to OWASP MASVS 2.1 and ASVS 5.0. Fix every critical/high finding or record a formal time-bound acceptance by an authorized role.

**Exit gate:**

- secret/SAST/dependency/container/DAST gates pass;
- export/delete and retention E2E pass;
- log-leak tests pass;
- restore meets measured RPO/RTO;
- audit chain verifies;
- legal/privacy review artifacts exist.

## P10 — Deployment and production release

**Stories:** WB-130…WB-135.

**Prompt:**

Containerize deployable services, provision separated EU-region environments through IaC, implement signed build/deployment pipelines, migration rehearsal, independent content release pipeline, canary, observability gates and rollback. Execute the full Definition of Done. Do not embed real credentials in evidence; report secret names and configuration status.

**Exit gate:**

- `make test-all` and `make build-all` pass;
- staging is fully reproducible;
- DB and content rollback drills pass;
- SBOMs and signed artifacts exist;
- R1 content, security, privacy and release reports are approved;
- production canary passes before broad rollout.
