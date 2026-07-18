# ADR-0002: sha256_hex prefix vs DB constraint mismatch

- **Status:** propus
- **Data:** 2026-07-18
- **Context contractual:** contracte mașină (09_DATABASE_SCHEMA.sql)

## Context

`wb_api.canonical.sha256_hex()` returnează `"sha256:" + hex_digest` (cu prefix),
dar constraint-ul DB pe `ops.idempotency_record.request_hash` cere
`CHECK (request_hash ~ '^[a-f0-9]{64}$')` — raw hex, fără prefix.

Consecință: `run_idempotent()` în producție ar crăpa la prima cerere cu
`Idempotency-Key` pentru că `request_hash` ar conține prefixul `sha256:`.

Același pattern există în `schemas.py` unde `Sha256` are pattern-ul
`^sha256:[a-f0-9]{64}$` (cu prefix), dar DB-ul are `^[a-f0-9]{64}$` (fără).

## Decizie

Standardizăm pe **raw hex (64 chars, no prefix)** în DB și **prefixed (sha256:hex)**
la API boundary. Conversia se face la granița repository:

- `sha256_hex()` continuă să returneze prefixed (e API contract)
- Repositories strip prefixul înainte de INSERT/SELECT pe coloane cu constraint raw-hex
- Alternativ: relaxăm constraint-ul DB să accepte ambele forme

**Alegem:** strip prefix la repository boundary — DB stochează raw hex (mai simplu,
mai puțin storage, indexes mai eficiente), API-ul expune prefixed (self-describing).

## Consecințe

- **De făcut:** `IdempotencyRepo.store()` și `find()` trebuie să strip-uiască prefixul
- **De făcut:** același fix pentru orice altă coloană cu `^[a-f0-9]{64}$` constraint
- **Ușor:** testele de integrare folosesc deja raw hex (workaround)
- **Greu:** trebuie auditat codul existent pentru alte locuri unde prefixul se strecoară în DB
