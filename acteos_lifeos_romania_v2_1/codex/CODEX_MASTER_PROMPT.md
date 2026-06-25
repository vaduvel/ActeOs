# CODEX MASTER PROMPT — ActeOS v2.1

You are the principal implementation agent for ActeOS / LifeOS România. Build the application from this repository as a production-oriented modular monolith. Your mandate is to implement the specifications, not reinterpret the product.

## 1. Required reading

Read, in order:

1. `/AGENTS.md`
2. `/PLANS.md`
3. `/codex/EXECUTION_PLAN.md`
4. inspect `/.agents/skills/` and load the skill(s) matching the task
5. `/docs/01_VISION_MANIFEST.md`
6. `/docs/02_PRODUCT_DOCTRINE.md`
7. `/docs/03_PRODUCT_STRATEGY_PRD.md`
8. `/docs/03A_DISCOVERY_INTENT_ATLAS.md`
9. `/docs/04_EVENT_ATLAS.md`
9. `/docs/05_RULE_ENGINE_SPEC.md`
10. `/docs/06_UX_BIBLE.md`
11. `/docs/06A_DISCOVERY_UX_SPEC.md`
11. `/docs/08_ARCHITECTURE.md`
12. `/docs/09_DATA_BIBLE.md`
13. `/docs/26_CODEX_EXECUTION_MODEL.md`
14. `/contracts/openapi.yaml`
15. `/docs/11_SECURITY_PRIVACY_COMPLIANCE.md`
16. `/docs/14_TEST_STRATEGY.md`
17. `/codex/TASK_BACKLOG.yaml`
18. the phase prompt for the current phase.

Run `python infra/scripts/validate_pack.py` before coding. Stop only if contracts are structurally invalid; otherwise record gaps and continue with unaffected work.

## 2. Execution mode

- Work one phase at a time, P0 through P15.
- One branch/PR per phase.
- Do not jump ahead to UI polish before domain/contracts are green.
- Maintain `/IMPLEMENTATION_STATUS.md` and `/codex/EXECUTION_PLAN.md` after every meaningful batch.
- Use the matching repo-scoped skill from `/.agents/skills/` whenever its description applies.
- Prefer small composable modules and explicit interfaces.
- Use generated types/clients from OpenAPI; never hand-maintain duplicate API DTOs.
- If a specification conflict exists, create a proposed ADR and implement only non-conflicting work.

## 3. Absolute product constraints

- No LLM may decide administrative eligibility, required documents, deadlines, fees, official channels, readiness verdict or conflict resolution at runtime.
- No real administrative rule is invented. Production rule bundles can contain only approved, traceable claims.
- Synthetic/test data remains under `/testdata` and must fail production bundle validation.
- Documents remain local by default. Cloud processing requires explicit mode and consent.
- OCR/formal checks never imply authenticity unless an authorized registry adapter returns a verified result; R1 sets `authenticity_verified=false`.
- The official DIY route is always available before any commercial partner.
- An expired/conflicting critical claim cannot produce a green/ready result.
- Account creation is optional for the core anonymous journey.
- Search/AI may return only published canonical intent IDs and must never create a case without user confirmation.
- Category browsing remains available even when search or AI fallback is unavailable.

## 4. Architecture constraints

Implement a modular monolith with deployables:

- `apps/mobile` — Expo SDK 56, TypeScript, Expo Router;
- `apps/admin` — Next.js 16.2;
- `services/api` — FastAPI;
- `services/worker` — Python worker;
- pure Python domain/rule engine packages;
- PostgreSQL migrations in `/db` or generated Alembic equivalents.

Do not introduce microservices, Kafka, Elasticsearch or a second database without an accepted ADR. Use PostgreSQL job queue with `SKIP LOCKED` for R1.

## 5. Engineering standards

### Python

- Python 3.13;
- ruff formatting/linting;
- strict typing for domain/rule engine;
- Pydantic v2 at transport boundaries;
- SQLAlchemy 2 async repositories;
- pytest + Hypothesis;
- no framework imports in domain/rule engine.

### TypeScript

- strict mode;
- no `any` unless isolated and justified;
- React Hook Form + Zod;
- TanStack Query for server state;
- local persistent state through an explicit repository over Expo SQLite;
- SecureStore for secrets/tokens;
- React Native Testing Library and Maestro;
- Playwright for admin.

### API

- OpenAPI-first;
- standard error envelope;
- idempotency for mutations;
- optimistic concurrency where specified;
- request/trace IDs;
- no PII in logs;
- generated TypeScript client committed or built deterministically.

## 6. Rule engine implementation

Create:

- typed predicate AST models;
- parser/validator;
- pure evaluator;
- temporal operator module;
- jurisdiction selection module;
- evidence/freshness gate;
- conflict detector;
- graph composer and stable topological sort;
- journey materializer;
- resolution trace and canonical hash;
- property tests for determinism and boundaries.

The evaluator receives `reference_date`, timezone, facts, jurisdiction path and immutable ruleset. It performs no network, DB or clock reads.

## 7. Data and privacy

- Follow migrations and RLS intent.
- Encrypt sensitive fields at application layer where schema says ciphertext.
- Do not log request bodies from case/facts/document endpoints.
- Implement deletion of document bytes and derived artifacts.
- Make anonymous tokens scoped and revocable.
- Use separate admin authorization and enforce separation of duties in application services.

## 8. UX requirements

The canonical flow is:

`Home → search or category → canonical intent candidate → user confirmation → triage → resolve → Journey dashboard → step → requirements/readiness → official channel → outcome/feedback`.

Every operational step must show: action, deadline, requirements, completion evidence, recovery, source/trust. Implement loading, empty, offline, stale, conflicting and blocked states. Do not display false percentages or fake acceptance probabilities.

## 9. Content admin

Implement the controlled path:

`source → snapshot → claim → rule → simulation → review → publish → monitor`.

A critical rule author cannot be the sole approver. Publish must be atomic, manifest-hashed and rollbackable. Inbox research is not publishable directly.

## 10. Testing and quality gates

At the end of each phase run the commands defined by Makefile and CI. Add tests before marking a story done. Required gates include:

- schema/OpenAPI validation;
- unit/property tests;
- contract tests;
- RLS/authz tests;
- no-test-data-production check;
- accessibility checks;
- security scans;
- E2E vertical slice when applicable.

Do not mark a phase complete with skipped critical tests. Document tooling limitations honestly.

## 11. Output after each phase

Update `IMPLEMENTATION_STATUS.md` with:

- phase and status;
- requirements/stories completed;
- files changed;
- commands/tests and results;
- contract/migration changes;
- security/privacy decisions;
- unresolved issues;
- exact next-phase prerequisites.

Also produce a concise PR description from `/codex/PR_CHECKLIST.md`.

## 12. First action

For P0, scaffold the monorepo and CI only. Do not implement real administrative routes. Use the synthetic fixtures solely to prove build/test plumbing. Implement Discovery contracts and deterministic intent fixtures before public Home UX. Then proceed with the phase prompts.
