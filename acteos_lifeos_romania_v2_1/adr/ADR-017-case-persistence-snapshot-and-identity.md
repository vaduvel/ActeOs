# ADR-017 — Persistența cazului: snapshot JSONB lossless + identitate anonymous-first

- **Status:** Accepted
- **Date:** 2026-06-26
- **Owners:** Product + Architecture

## Context

M3 cere persistarea agregatului de caz (cazul + journey-ul rezolvat) în PostgreSQL (ADR-008), păstrând determinismul resolverului (ADR-003), fără cont obligatoriu (ADR-006) și fără cuplare la un anume vendor (ADR-011). Schema (`db/0001_init.sql`) definește `app.cases` și `app.journeys` cu `resolution_trace jsonb`, `trust_state`, `unique(case_id, revision)` și `case_identity_ck (user_id is not null or installation_id is not null)`.

## Decision

1. **Snapshot lossless.** Journey-ul stochează rezolvarea completă a engine-ului ca **JSONB** (`resolution_snapshot`, migrația `db/0002_case_resolution_snapshot.sql`): events + advice/warnings/conflicts/deadlines/blocks + trace. `resolution_trace` rămâne ca **antet verificabil** (hash-uri + `engine_version`). Proiecțiile normalizate `journey_steps`/`journey_requirements` sunt **derivate ulterioare**, nu sursa de adevăr.
2. **Identitate anonymous-first.** `installation_id` și `user_id` sunt **ambele opționale** la nivel de API; DB impune cel puțin una prin `case_identity_ck`. Conform ADR-006: traseu de bază fără cont; contul se adaugă progresiv.
3. **Vendor-neutral.** Accesul la Postgres se face **doar** prin SQLAlchemy/psycopg via `ACTEOS_DATABASE_URL`. Gazda de producție (Supabase EU) nu introduce cuplare la SDK-ul vendorului (ADR-011); `auth.users`/RLS/Storage rămân un slice ulterior de identitate.
4. **Port + adaptor.** `CaseRepository` (Protocol). `InMemoryCaseRepository` rămâne default (dev/teste fără DB); `SqlAlchemyCaseRepository` se activează doar când există un engine configurat. Scrierea = **o singură tranzacție** care rezolvă `ruleset_version → content.rule_sets.id` și scrie cazul + journey-ul (revizia 1).
5. **Validare înainte de scriere.** NOT NULL, apartenență la enum-urile `case_status`/`journey_status`, identitate, lungimea `facts_hash` (64) — verificate înainte de orice `INSERT`; `on_conflict_do_nothing` asigură idempotența.

## Consequences

- În mod DB, persistarea unui caz cere **catalog publicat** (FK `content.life_event_types`) și **ruleset publicat** (`content.rule_sets`, pentru rezolvarea `ruleset_version`): pipeline-ul de conținut precede servirea cazurilor.
- `trust_state` are o mapare **provizorie documentată** (`needs_review` la conflict/confirmare/block, altfel `trusted`), de rafinat odată cu slice-ul de încredere.
- Documentele binare rămân în afara DB (ADR-005/ADR-008): object storage cu hash + referință.
- Default-ul in-memory păstrează dezvoltarea și testele fără infrastructură; comportamentul API este identic.

## Revisit triggers

- apar dovezi măsurabile că decizia blochează SLO, securitatea sau livrarea;
- contracte publice ori obligații legale schimbă premisele;
- slice-ul de autentificare aduce `app.installations` end-to-end și schimbă modelul de identitate;
- costul operațional depășește beneficiul demonstrat.
