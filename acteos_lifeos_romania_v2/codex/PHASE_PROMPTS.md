# Codex Phase Prompts

Use exactly one section at a time together with `CODEX_MASTER_PROMPT.md`.

## P0 — Repository and tooling

Create monorepo layout, package managers, Python workspace, lint/type/test commands, Docker/local DB, CI, secret scanning and implementation status. Acceptance: all empty shells build and `make validate` passes.

## P1 — Contracts and generated types

Validate OpenAPI/JSON Schemas, introduce lint/diff tooling, generate TypeScript client and Python transport models where appropriate. Acceptance: generated code is reproducible and no duplicate handwritten DTOs exist.

## P2 — Domain model and predicate DSL

Implement value objects, enums, canonical serialization, predicate models/parser and errors. No DB or FastAPI imports. Acceptance: schema roundtrip and invalid AST cases covered.

## P3 — Deterministic rule engine

Implement evaluator, temporal/jurisdiction/freshness/conflict/graph/materialization/trace. Use only testdata. Acceptance: property tests and canonical hash determinism pass.

## P4 — Database and repositories

Translate SQL baseline to Alembic if used, configure Postgres, repositories, transactions, RLS tests and job queue. Acceptance: migrations on clean DB and cross-user isolation tests pass.

## P5 — API vertical slice

Implement case create/get, facts update, resolve and journey get. Add auth modes, idempotency, errors and contract tests. Acceptance: synthetic event resolves end-to-end through HTTP.

## P6 — Mobile shell and local persistence

Create Expo app, navigation, design tokens, API client, anonymous identity, SQLite repositories, outbox and offline shell. Acceptance: app runs Android/iOS development builds and restores a cached synthetic journey offline.

## P7 — Journey UX

Implement Home, candidates, triage, dashboard, step, requirements, trust states, official channel and feedback shell. Acceptance: canonical synthetic flow passes Maestro and accessibility smoke.

## P8 — Document readiness local

Implement local metadata, file selection/camera abstraction, local-only storage, formal checks interface, expiry/field/result states and deletion. No authenticity. Acceptance: test documents never upload and derived data is deleted.

## P9 — Content admin

Implement admin auth/RBAC and source/snapshot/claim/rule/simulation/review/publish flow. Acceptance: critical separation-of-duties and rollback ruleset tests pass.

## P10 — Freshness worker

Implement source scheduling, safe fetch adapter, hashing/diff, review due/hard expiry, queues and gap dashboard. Acceptance: mocked source changes create review tasks and never auto-publish.

## P11 — Notifications and recalculation

Implement deadline/expiry/rule-change scheduler, outbox delivery, journey revision and progress migration. Acceptance: timezone/boundary/idempotency tests pass.

## P12 — Optional account and household

Implement account linking from anonymous mode, household/member/assets, sync and deletion/export. Acceptance: anonymous core remains functional and permissions are granular.

## P13 — Security, privacy and observability

Implement redaction, audit, rate limits, session controls, kill switches, metrics/traces, backup/restore scripts and security checks. Acceptance: security test matrix and PII log tests pass.

## P14 — Approved research import

Build importer/validator for approved research packs. Import only claims with approval metadata and passing schemas. Do not import inbox files. Acceptance: production bundle validator rejects missing/expired/synthetic evidence.

## P15 — Release certification

Run full CI/E2E/a11y/security/performance, staging migration/rollback, ruleset rollback, store privacy manifests and runbook exercise. Produce release manifest and unresolved risk statement.
