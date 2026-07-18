# Implementation status

## Rezumat

| Fază | Subiect | Stories | Status |
|---|---|---|---|
| P0 | Fundație & reproductibilitate | WB-001…005 | 🟢 schelet inițializat (lockfiles reale = TODO) |
| P1 | Contracte, persistență, cripto | WB-010…024 | 🟡 nucleu făcut (hashing/erori/validare/cripto); DB migrații + codegen = TODO |
| P2 | Motor determinist de reguli | WB-030…035 | 🟢 nucleu + teste verzi |
| P3 | Source ingestion & content lifecycle | WB-040…045 | 🟢 10 module, 114 teste verzi |
| P4 | API & journey lifecycle | WB-050…055 | 🟢 125 teste verzi (contract + BOLA + integration + curator + PII + OpenAPI) |
| P5 | Curator portal | WB-060…065 | 🟡 Next.js app funcțional, 38 teste verzi; wire la API real = TODO |
| P6–P10 | … | … | ⬜ neînceput |

## P1 — Contracte & cripto

**Realizat (`packages/contracts` + `services/api`):**
- [x] `wb_contracts.canonical` — serializare JSON canonică + `sha256_hex`
- [x] `wb_contracts.errors` — vocabular de erori problem+json
- [x] `wb_contracts.schema` — validare JSON Schema (Draft 2020-12)
- [x] Modele PostgreSQL (SQLAlchemy 2.0 ORM, 489 linii, toate tabelele din 09_DATABASE_SCHEMA.sql)
- [x] Repository-uri (Catalog, Journey, Evidence, Feedback, Idempotency, Audit, ContentBundle)
- [x] Criptare de câmp key-versioned (`FieldCipher` cu AAD, rotație testată)
- [x] Audit append-only hash-chained (`AuditChain` + `compute_event_hash` + `verify_event_log`)
- [x] Idempotență (advisory lock + response replay + conflict detection)
- [x] Golden hash tests + fixtures
- [x] Migrații Alembic (0001_initial.py)

**De făcut pentru a închide P1:**
- [ ] Generare de cod cross-language (Py/Kotlin/TS) din scheme + golden hash identic
- [ ] RLS (row-level security) hardening

## P2 — Motor determinist

**Realizat (`packages/rule-engine`, zero dependențe runtime):**
- [x] logică three-valued (`trivalent.py`)
- [x] evaluare predicate tipate (`predicates.py`)
- [x] fapte derivate (`age_on_date`, context) (`facts.py`)
- [x] aplicabilitate jurisdicțională + temporală + specificitate (`applicability.py`)
- [x] gate-uri freshness (`freshness.py`)
- [x] sortare topologică stabilă + detecție cicluri (`graph.py`)
- [x] `resolve()` determinist cu hashes
- [x] `route_diff()` pentru impact analysis
- [x] teste unitare + property-based (hypothesis)

**De făcut pentru a închide P2:**
- [ ] merge complet de precedență legală
- [ ] suită amplă de fixture-uri + golden route hashes
- [ ] 95%+ coverage

## P3 — Source ingestion & content lifecycle

**Realizat (`packages/source-ingestion`):**
- [x] `registry.py` — source CRUD + domain allowlist + fetch scheduling
- [x] `fetcher.py` — bounded fetch cu SSRF protection (scheme, private IP, DNS, size, timeout)
- [x] `snapshot.py` — immutable content-addressed store (SHA-256)
- [x] `normalize.py` — HTML→text (stdlib only, structural breaks preserved)
- [x] `diff.py` — snapshot diff + severity (none/cosmetic/moderate/critical)
- [x] `impact.py` — impact analysis (claims/rules affected)
- [x] `ai_adapter.py` — optional AI extraction (AI_EXTRACTION_ENABLED flag, no self-publish)
- [x] `review.py` — 2 reviewers for critical, no self-approval
- [x] `publish.py` — atomic pointer + rollback, history never deleted
- [x] `staleness.py` — time-travel testable scheduler
- [x] 114 teste, toate verzi

## P4 — API & journey lifecycle

**Realizat (`services/api`):**
- [x] Toate endpoint-urile citizen (system, catalog, routes, journeys, evidence, feedback)
- [x] Curator router (auth + scope enforcement, sources, review, publish, rollback)
- [x] Ownership / anti-IDOR (device-scoped, no info leakage)
- [x] Idempotency middleware (advisory lock + replay)
- [x] Audit logging (append-only, hash-chained, PII-scrubbed)
- [x] Error handling (problem+json, field errors)
- [x] PII-free logging (JsonFormatter denylist + scrub_payload)
- [x] 105 teste: 13 contract + 13 BOLA + 10 integration + 18 curator + 27 PII + 9 OpenAPI + 15 existing

**De făcut pentru a închide P4:**
- [ ] Wire curator router la services layer (currently returns stubs)
- [ ] p95 load testing local
- [ ] OIDC real auth (currently placeholder Bearer token)

## P5 — Curator portal

**Realizat (`apps/curator-web`, Next.js 16 + TypeScript strict + Tailwind):**
- [x] Login page cu Bearer token auth (dev format)
- [x] DashboardShell cu auth guard + Nav filtrat pe scope-uri
- [x] Sources page — registry table, create form, fetch, status/freshness badges
- [x] Review page — 2-reviewer rule, rationale form, no self-approval
- [x] Publish page — canary/production + rollback cu confirmare
- [x] Staleness page — SLA dashboard (fresh/due/stale/critical)
- [x] Feedback page — incident list
- [x] auth.ts — RBAC, parseToken, canApproveChange (two-person rule)
- [x] api.ts — typed API client
- [x] sanitize.ts — stripHtml, escapeHtml, sanitizeUrl, containsXssPatterns
- [x] 38 teste (21 XSS + 17 RBAC), toate verzi

**De făcut pentru a închide P5:**
- [ ] Wire la API real (currently mock data)
- [ ] Structured rule editor (JSON schema-bound)
- [ ] Snapshot diff viewer (side-by-side)
- [ ] E2E review + rollback flow
- [ ] OIDC real auth

## Test totals

| Pachet | Teste | Status |
|---|---|---|
| packages/contracts | 8 | ✅ |
| packages/rule-engine | 58 passed, 1 skipped | ✅ |
| packages/source-ingestion | 114 | ✅ |
| services/api | 125 passed | ✅ |
| apps/curator-web | 38 | ✅ |
| **Total** | **343 passed, 1 skipped** | ✅ |

## Cum rulezi

```bash
make bootstrap          # instalează pachetele Python editabil cu dev deps
make test-unit          # rulează pytest pe toate pachetele Python
make test-integration   # rulează teste cu Docker (Postgres via testcontainers)
make test-web           # rulează vitest pe curator-web
```
