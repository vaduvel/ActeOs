# 21 — Engineering Workbook

## 1. Repo bootstrap

```text
acteos/
  AGENTS.md
  PLANS.md
  .agents/skills
  codex/EXECUTION_PLAN.md
  apps/mobile
  apps/admin
  services/api
  services/worker
  packages/contracts
  packages/design-tokens
  packages/generated-api-client
  python/acteos_domain
  python/acteos_rule_engine
  python/acteos_application
  python/acteos_adapters
  db/migrations
  research/inbox
  testdata
  infra
  docs
```

## 2. Build commands țintă

```bash
make bootstrap
make validate
make test
make dev
make api
make worker
make mobile
make admin
make generate-clients
make migration name=...
make production-bundle-check
```

Codex trebuie să implementeze comenzile și să le țină sincronizate cu CI.

## 3. Package boundaries

### `acteos_domain`

Entități, value objects, enums și errors. Fără DB, HTTP sau framework.

### `acteos_rule_engine`

Predicate parser/evaluator, jurisdiction, temporal, graph, conflicts, trace. Pur și determinist.

### `acteos_application`

Use cases: create case, set facts, resolve, recalculate, publish ruleset, submit feedback.

### `acteos_adapters`

Postgres, storage, auth, notifications, source fetch, OCR/LLM interfaces.

### API

Transport only: auth, validation, use-case call, response mapping.

## 4. Coding standards

- Python: ruff, mypy/pyright strict pentru domain/engine, pytest, Hypothesis;
- TypeScript: strict, no `any` fără justificare, ESLint, Prettier;
- React: server state în TanStack Query, forms în React Hook Form/Zod;
- UI state local simplu; nu duplicăm server cache în Zustand;
- generated API client este singurul client HTTP business;
- SQL migrations reviewate;
- no business rules în UI sau SQL triggers ascunse.

## 5. API-first workflow

1. editează OpenAPI/schema;
2. validate/diff;
3. generează client/types;
4. implementează backend;
5. contract tests;
6. implementează UI;
7. E2E.

Nu ajustăm manual răspunsul backend ca să „meargă ecranul” fără actualizarea contractului.

## 6. Definition of ready pentru story

- user/business value clar;
- requirement ID și traceability;
- contract/data impact;
- security/privacy impact;
- source dependency declarată;
- acceptance criteria testabile;
- out-of-scope;
- mock only dacă nu există date administrative și este marcat dev/test.

## 7. PR template

- ce problemă rezolvă;
- docs/contracts schimbate;
- screenshots/video pentru UI;
- tests executate;
- migrations;
- privacy/security;
- observability;
- rollback;
- known gaps;
- no synthetic production data checkbox.

## 8. Phase gates

### P0

Repo compilează, CI rulează, env docs există.

### P1

OpenAPI și schemas sunt validate; generated client compilează.

### P2

Domain objects nu depind de framework; serialization roundtrip.

### P3

Intent Resolver + Rule Engine sunt deterministe; ranking, ambiguity și property tests sunt green.

### P4

Migrations/RLS/repositories; cross-user access tests.

### P5

Case→facts→resolve→journey API vertical slice.

### P6

Mobile local anonymous flow și offline persistence.

### P7

Home search + categories + disambiguation + Journey UX complet cu trust states și official channel.

### P8

Local readiness și deletion.

### P9

Admin source→claim→rule→publish.

### P10

Freshness jobs, diff și gap queues.

### P11

Notifications, journey recalculation și progress migration.

### P12

Optional account, household, RBAC, DSAR/delete.

### P13

Telemetry redaction, SLO dashboards, security scans.

### P14

Import only approved research; no direct inbox publication.

### P15

Full release checklist, staging exercise și signed artifacts.

## 9. Implementation status

După fiecare fază, Codex actualizează:

- status;
- commit/PR;
- files changed;
- tests;
- contract changes;
- unresolved risks;
- next phase prerequisites.

Template: `codex/IMPLEMENTATION_STATUS.template.md`.

## 10. Architectural change

Dacă Codex consideră că o cerință este inconsistentă, nu improvizează. Creează `PROPOSED_ADR.md` cu context, opțiuni, consecințe și recomandare, apoi continuă numai cu părțile neafectate.
