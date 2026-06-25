# 20 — Release Plan

Planul este bazat pe gate-uri, nu pe promisiuni calendaristice.

## R0 — Foundation

### Livrează

- monorepo și CI;
- contracts + generated clients;
- DB schema și auth skeleton;
- predicate DSL și rule engine;
- synthetic fixtures;
- mobile shell și admin shell;
- source/claim/rule workflow fără production rules.

### Gate

Determinism/property tests, OpenAPI valid, publish simulation și zero testdata în production bundle.

## R0.5 — Vertical Slice

### Livrează

Un eveniment complet pe date sintetice: input → triage → resolve → journey → readiness → admin publish → recalculation.

### Gate

E2E mobile/admin/API, offline cache și audit complet.

## R1A — Timișoara Core

### Events

- moved_home;
- bought_used_vehicle_ro;
- sold_vehicle_ro;
- identity_card_change_or_expiry;
- identity_card_lost_stolen;
- local_tax_certificate/declaration;
- lost_all_documents.

### Gate

Claims oficiale aprobate, fixtures reale-safe, user testing, rule rot monitoring și outcome feedback.

## R1B — Recurrence

### Capabilities

- household;
- document expiry;
- notifications;
- utility holder change;
- criminal record;
- passport;
- child birth basic;
- education approved pack.

### Gate

Retention/privacy review, notification accuracy și multi-person permissions.

## R2 — National Base

- extindere la 25–30 event families;
- base național + overrides locale selectate;
- export dosar;
- optional account sync;
- source change automation matură.

Gate: cost de mentenanță/event cunoscut și freshness SLO verde.

## R3 — Assisted Resolution

- human review;
- parteneri verificați;
- B2B2C;
- instituții pilot;
- integrare oficială numai unde există acord și sandbox.

Gate: neutrality audit și contractual/privacy review.

## Faze de execuție Codex

P0 — repository and tooling  
P1 — contracts and generated types  
P2 — domain model and predicate DSL  
P3 — rule engine and property tests  
P4 — database and repositories  
P5 — API case/journey slice  
P6 — mobile shell and local persistence  
P7 — mobile journey UX  
P8 — document readiness local  
P9 — admin content operations  
P10 — source/freshness worker  
P11 — notifications and recalculation  
P12 — auth/RBAC/privacy deletion  
P13 — observability/security hardening  
P14 — R1 research import  
P15 — release certification

Fiecare fază are prompt și acceptance criteria în `codex/`.
