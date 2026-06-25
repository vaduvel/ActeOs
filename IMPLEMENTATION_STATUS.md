# Implementation status

## Rezumat

| Fază | Subiect | Stories | Status |
|---|---|---|---|
| P0 | Fundație & reproductibilitate | WB-001…005 | 🟢 schelet inițializat (lockfiles reale = TODO) |
| P1 | Contracte, persistență, cripto | WB-010…024 | 🟡 nucleu făcut (hashing/erori/validare); DB+cripto = TODO |
| P2 | Motor determinist de reguli | WB-030…035 | 🟢 nucleu + teste verzi |
| P3–P10 | … | … | ⬜ neopînit |

## P1 — Contracte & cripto

**Realizat (`packages/contracts`):**
- [x] `wb_contracts.canonical` — serializare JSON canonică + `sha256_hex` (referința cross-language pentru golden hashing)
- [x] `wb_contracts.errors` — vocabular de erori problem+json (`ProblemCode`, `WbError`)
- [x] `wb_contracts.schema` — utilitar de validare JSON Schema (Draft 2020-12)
- [x] teste unitare

**De făcut pentru a închide P1:**
- [ ] modele PostgreSQL + migrații Alembic (din `09_DATABASE_SCHEMA.sql`)
- [ ] repository-uri + idempotență
- [ ] criptare de câmp key-versioned + test de rotație
- [ ] audit append-only anti-tamper
- [ ] generare de cod cross-language (Py/Kotlin/TS) din scheme + golden hash identic

## P2 — Motor determinist

**Realizat (`packages/rule-engine`, zero dependențe runtime):**
- [x] logică three-valued (`trivalent.py`)
- [x] evaluare predicate tipate (`predicates.py`) conform `contracts/rule.schema.json`
- [x] fapte derivate (`age_on_date`, context) (`facts.py`)
- [x] aplicabilitate jurisdicțională (ancestry) + temporală + specificitate (`applicability.py`)
- [x] gate-uri freshness (`freshness.py`)
- [x] sortare topologică stabilă + detecție cicluri (`graph.py`)
- [x] `resolve()` determinist cu `rule_bundle_hash`/`facts_hash`/`route_hash` (exclude `route_id`+`evaluated_at`, include `engine_version`)
- [x] `route_diff()` pentru impact analysis
- [x] teste unitare + property-based (hypothesis)

**De făcut pentru a închide P2:**
- [ ] merge complet de precedență legală (base + lawful_override + supplement) — momentan selectează regula cea mai specifică și ridică `RuleConflict` la egalitate nerezolvată
- [ ] suită amplă de fixture-uri de traseu + golden route hashes
- [ ] 95%+ coverage motor, 100% ramuri critice

## Cum rulezi

```bash
make bootstrap   # instalează pachetele Python editabil cu dev deps
make test-unit   # rulează pytest pe contracts + rule-engine
```
