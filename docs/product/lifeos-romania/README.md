# LifeOS România — Super-Book (sursa unică de adevăr)

Acest director este **singurul adevăr** pentru produsul LifeOS România. Fuzionează trei surse:

1. Workbook-ul de continuitate (acest director, scris peste pachetul canonic anterior `waze-birocratie`) — model determinist matur, orchestrator eveniment→graf, surse oficiale **verificate real**, ADR-uri.
2. Pachetul `lifeos_romania_codex_pack_v1/` (GPT 5.5 Pro) — schelet buildabil: OpenAPI, schemă DB, contracte, config, seed, test, backlog, faze P0–P12. **Depreciat.**
3. Pachetul `acteos_lifeos_romania_v2/` (GPT 5.5 Pro, v2.0.0, 121 fișiere, validare PASS) — folosit ca **donator** (vezi `27_V2_DONOR_INTEGRATION.md`). Stack-ul său mobil (Expo/RN) este **suprascris**; rămâne ca referință pentru motor, contracte, research și backlog.

Conflictele istorice sunt rezolvate în `MERGE_PROVENANCE.md`; deciziile față de v2 în `27_V2_DONOR_INTEGRATION.md`.

## Principiu de produs

Utilizatorul scrie în limbaj natural „Ce s-a întâmplat?". Aplicația clasifică evenimentul de viață și generează **graful complet de obligații administrative**: eveniment → obligații → trasee → documente → canale oficiale → notificări.

## Reguli de execuție (inviolabile)

- **Producție, nu demo.** `demo_mode` există doar ca flag de test/fixture.
- **Zero invenții.** Nimic fără `source_claim_ids`; restul rămâne `REQUIRES_HUMAN_CURATION`.
- **Determinism la runtime.** Motorul și orchestratorul nu apelează LLM/internet/OCR la evaluare.
- **Stack păstrat (ADR-027):** Android nativ Kotlin + `services/api` (`wb_api`) + `packages/rule-engine` (`wb_rule_engine`) + curator Next.js. **Nu** Expo/RN.

## Hartă de citire

1. `CODEX_START_HERE.md` — punct de intrare.
2. `MERGE_PROVENANCE.md` + `27_V2_DONOR_INTEGRATION.md` — proveniență și decizii.
3. `00_PRODUCT_MANIFEST.md`, `24_PRODUCT_DOCTRINE.md` — viziune și doctrină (D1–D20).
4. `01_SCOPE_RELEASES.md`, `02_PRD.md`, `03_UX_FLOWS.md`, `04_DOMAIN_MODEL.md`.
5. `05_RULE_ENGINE_SPEC.md` + `08_RULE_ENGINE_DEEP_SPEC.md` — motor determinist + model aprofundat (predicate AST, jurisdicție, temporal, conflict, freshness).
6. `06_LIFE_EVENT_CATALOG.md`, `06_SOURCE_GOVERNANCE.md`, `19_SOURCE_REGISTRY.json`.
7. `07_ARCHITECTURE.md`, `09_API_SPEC.yaml`, `10_DATABASE_SCHEMA.sql`, `25_DATA_BIBLE.md`, `contracts/`, `config/`, `seed/`.
8. `11_SECURITY_PRIVACY.md`, `12_TEST_STRATEGY.md`, `13_DEFINITION_OF_DONE.md`, `17_DEPLOYMENT_RUNBOOK.md`, `18_CONTENT_OPERATIONS.md`.
9. `26_EXECUTION_MODEL_AND_PLANS.md` + `skills/` — ExecPlan și skills repo-scoped.
10. `15_CODEX_MASTER_PROMPT.md`, `16_PHASE_PROMPTS.md`.
11. `20_CANONICAL_DECISIONS.md` (ADR-001..030), `21_METRICS_AND_BUSINESS.md`, `22_PARTNER_NEUTRALITY_POLICY.md`, `23_TRACEABILITY_MATRIX.csv`.
