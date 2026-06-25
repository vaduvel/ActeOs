---
name: acteos-vertical-slice
description: Use when implementing or modifying an end-to-end ActeOS citizen journey across contracts, domain, resolver, database, API and mobile UI.
---

# ActeOS Vertical Slice

## Goal

Livrează un rezultat utilizabil cap-coadă fără a sparge contract-first, determinismul sau trasabilitatea.

## Procedure

1. Identifică outcome-ul utilizatorului, phase gate-ul și story IDs.
2. Citește `PLANS.md`, planul activ și specificațiile de domeniu/UX relevante.
3. Verifică sau modifică mai întâi OpenAPI/JSON Schema; rulează breaking-change check.
4. Generează tipurile/clienții; nu crea DTO-uri paralele manual.
5. Implementează domain/use case cu ports explicite și fără I/O în rule engine.
6. Adaugă persistence/migration idempotentă și RLS dacă se schimbă datele.
7. Implementează API-ul cu idempotency, concurrency și error envelope standard.
8. Implementează mobile states: loading, needs facts, ready, stale, conflict, offline, failed și completed.
9. Pentru fiecare pas afișează: ce fac acum, până când, ce îmi trebuie, de ce, dovada finalizării și recovery.
10. Adaugă unit, integration, contract, E2E, a11y și critical-copy tests.
11. Instrumentează metrics/traces fără PII.
12. Rulează gate-ul milestone-ului și actualizează planul viu.

## Constraints

- Core journey funcționează fără cont.
- Official DIY route este prima.
- Runtime output păstrează ruleset version, reference date și source claim IDs.
- Failure/degraded states sunt produs, nu excepții ascunse.
- Nu introduce integrare externă neconfirmată pentru a închide flow-ul.

## Completion evidence

- flow-ul este demonstrabil în staging/local cu fixture permis;
- rerularea resolverului este reproductibilă;
- API/client generation este curată;
- migration up/down sau forward recovery este testată;
- a11y și offline/degraded behavior sunt verificate;
- PR checklist și ExecPlan sunt actualizate.
