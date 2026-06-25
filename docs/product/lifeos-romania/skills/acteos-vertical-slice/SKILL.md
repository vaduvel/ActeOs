---
name: acteos-vertical-slice
description: Use when implementing or modifying an end-to-end ActeOS citizen journey across contracts, domain, resolver, database, API and the Android native UI.
---

# ActeOS Vertical Slice

## Goal
Livrează un rezultat utilizabil cap-coadă fără a sparge contract-first, determinismul sau trasabilitatea.

## Procedure
1. Identifică outcome-ul utilizatorului, phase gate-ul și story IDs.
2. Citește `26_EXECUTION_MODEL_AND_PLANS.md`, planul activ și specificațiile de domeniu/UX relevante.
3. Verifică sau modifică mai întâi OpenAPI/JSON Schema; rulează breaking-change check.
4. Generează tipurile/clienții; nu crea DTO-uri paralele manual.
5. Implementează domain/use case cu ports explicite și fără I/O în rule engine (`wb_rule_engine`).
6. Adaugă persistence/migration idempotentă și RLS dacă se schimbă datele.
7. Implementează API-ul (`wb_api`) cu idempotency, concurrency și error envelope standard.
8. Implementează stările Android nativ: loading, needs facts, ready, stale, conflict, offline, failed, completed.
9. Pentru fiecare pas afișează: ce fac acum, până când, ce îmi trebuie, de ce, dovada finalizării și recovery.
10. Adaugă unit, integration, contract, E2E, a11y și critical-copy tests.
11. Instrumentează metrics/traces fără PII.
12. Rulează gate-ul milestone-ului și actualizează planul viu.

## Constraints
- Core journey funcționează fără cont.
- Ruta oficială DIY este prima.
- Runtime output păstrează ruleset version, reference date și source claim IDs.
- Failure/degraded states sunt produs, nu excepții ascunse.
- Nu introduce integrare externă neconfirmată pentru a închide flow-ul.
