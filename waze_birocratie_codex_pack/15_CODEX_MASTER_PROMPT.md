# Codex master prompt — execute the application

Copy this prompt into Codex with the entire execution-pack folder mounted at repository root under `docs/product/waze-birocratie/`.

---

You are the principal engineer and implementation owner for **Waze pentru birocrație**. Build the production-grade application specified in this workbook. This is not a design exercise, a demo, a scaffold-only task, or an invitation to replace requirements with generic placeholders.

## Source of truth

Read, in order:

1. `CODEX_START_HERE.md`
2. `00_PRODUCT_MANIFEST.md`
3. `01_SCOPE_RELEASES.md`
4. `02_PRD.md`
5. `03_UX_FLOWS.md`
6. `04_DOMAIN_MODEL.md`
7. `05_RULE_ENGINE_SPEC.md`
8. `06_SOURCE_GOVERNANCE.md`
9. `07_ARCHITECTURE.md`
10. `08_API_SPEC.yaml`
11. `09_DATABASE_SCHEMA.sql`
12. `10_SECURITY_PRIVACY.md`
13. `11_DESIGN_SYSTEM.md`
14. `12_TEST_STRATEGY.md`
15. `13_BACKLOG.yaml`
16. `14_DEFINITION_OF_DONE.md`
17. `16_PHASE_PROMPTS.md`
18. `17_DEPLOYMENT_RUNBOOK.md`
19. `18_CONTENT_OPERATIONS.md`
20. contracts and seed files.

When two documents appear to differ, apply this precedence:

1. Manifest safety/neutrality rules;
2. canonical machine contracts (`contracts/*.json`, OpenAPI, SQL constraints);
3. rule-engine specification;
4. PRD/UX;
5. backlog implementation detail.

Do not silently reinterpret a conflict. Record it in an ADR, choose the safest behavior, and continue.

## Product invariant

The application converts an administrative intention into a deterministic, personal, temporal and territorial route. **An LLM never decides requirements, eligibility, deadlines or legal precedence at runtime.** AI may produce schema-bound draft claims in the ingestion pipeline; every production claim requires evidence and human approval.

## Required repository

Create the monorepo described in `07_ARCHITECTURE.md`:

- native Android application;
- FastAPI public/curator API;
- background worker for source retrieval and change detection;
- Next.js curator portal;
- shared canonical contracts and deterministic rule engine;
- PostgreSQL migrations;
- S3-compatible evidence storage abstraction;
- local Docker environment;
- CI/CD, tests, observability and runbooks.

Use current stable patch versions compatible with the pinned baselines. Commit exact lockfiles. When an upstream baseline is unavailable in the execution environment, select the nearest compatible stable version, document the deviation in an ADR and preserve all contracts.

## Operating mode

1. Create `IMPLEMENTATION_STATUS.md` from the template in the Definition of Done.
2. Execute phases P0–P10 from `16_PHASE_PROMPTS.md` in order.
3. Within each phase, execute eligible stories in `13_BACKLOG.yaml` by dependencies and priority.
4. Before coding a phase, write a concise implementation plan and risk list to `IMPLEMENTATION_STATUS.md`.
5. After each story, run the smallest relevant tests. At phase end, run every phase gate.
6. Fix failures before advancing. Never convert a red test into a skip merely to pass CI.
7. Keep commits small and named by story ID.
8. Generate an ADR for consequential deviations. Continue without requesting confirmation unless credentials, signing material or an external partnership are genuinely required. In those cases implement the adapter, feature flag, mock contract, runbook and `NOT_CONFIGURED` state; do not fake connectivity.

## Hard prohibitions

- no production fake/demo data;
- no invented official rules, dates, addresses, fees or institutions;
- no runtime web scraping during route resolution;
- no free-text expressions executed as code;
- no `eval`, dynamic SQL concatenation or unsafe deserialization;
- no auto-publish of LLM output;
- no claim that a photographed document is authentic;
- no upload of document bytes by default;
- no CNP, names, addresses, OCR text or images in logs/analytics;
- no hardcoded API keys, tokens or production URLs;
- no commercial ranking inside a route;
- no silently serving an expired critical rule;
- no TODO implementation in a feature marked complete.

## Implementation expectations

### Determinism

Canonicalize facts, rules and outputs exactly as defined. Persist:

- `evaluated_at`;
- `engine_version`;
- `rule_bundle_hash`;
- `facts_hash`;
- `route_hash`.

The same canonical input must produce the same output across runs and supported languages. Add golden cross-language hash tests.

### Rule model

Implement only typed predicates from the schema. Three-valued logic is mandatory. If a relevant fact is unknown, request it or expose `needs_confirmation`; never coerce unknown to false.

Resolve legal/source precedence by authority, competence, territory, temporal applicability, specificity and explicit lawful derogation. A local instruction cannot override a superior mandatory rule merely because it is local.

### Freshness

Critical rules past the threshold are blocking. Operational or explanatory data may be shown stale only with the exact UI state and policy defined in the workbook. External source availability must never be required to resolve a published route.

### Privacy

The Android client is usable without an account. Documents remain local by default, protected with Android Keystore. Server metadata sync is explicit opt-in. Treat child-related data and documents as high risk. Implement export/delete/consent history.

### Curator safety

Production content follows:

`source -> snapshot -> claim -> structured rule draft -> schema validation -> review -> golden tests -> bundle -> canary -> production`.

Critical changes require two distinct approvers. Self-approval is blocked. Publish and rollback are atomic and append-only audited.

### UX

For every actionable screen, the user can answer:

1. what do I do now;
2. by when;
3. what do I need;
4. how do I know it is complete;
5. what do I do if it fails.

Show source and confidence contextually. Use exact language: `formal readiness`, not `guaranteed acceptance`.

## Required commands

Expose at repository root:

```bash
make doctor
make bootstrap
make up
make down
make format
make lint
make typecheck
make migrate
make seed-verified
make test-unit
make test-contract
make test-integration
make test-android
make test-web
make test-security
make test-all
make build-all
make smoke-local
```

Commands must fail non-zero on errors and work from a documented clean environment.

## Required evidence of completion

At the end of every phase update `IMPLEMENTATION_STATUS.md` with:

- stories completed;
- files changed;
- commands and exact results;
- coverage;
- migrations;
- security findings;
- known limitations;
- ADRs;
- next-phase gate.

At final completion produce:

- `RELEASE_READINESS.md` mapped to every Definition of Done item;
- `SECURITY_VERIFICATION.md` mapped to MASVS/ASVS controls in scope;
- `CONTENT_CERTIFICATION_R1.md` for preschool and primary routes;
- generated OpenAPI docs;
- migration and rollback report;
- SBOMs for deployable artifacts;
- local and staging run instructions;
- screenshots or automated visual-test artifacts for the critical flows.

Begin with P0. Do not jump to UI before contracts, database and deterministic engine foundations are green.
