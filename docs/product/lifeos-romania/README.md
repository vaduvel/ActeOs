# LifeOS România — Super-Book (sursa unică de adevăr)

Acest director este **singurul adevăr** pentru produsul LifeOS România. Fuzionează două surse:

1. Workbook-ul de continuitate (acest director, scris peste pachetul canonic anterior `waze-birocratie`) — model determinist matur, orchestrator eveniment→graf, surse oficiale **verificate real**, ADR-uri.
2. Pachetul `lifeos_romania_codex_pack_v1/` (generat de GPT 5.5 Pro) — schelet buildabil complet: OpenAPI, schemă DB, contracte JSON, config, seed, strategii de test, backlog, faze P0–P12.

Unde cele două se contraziceau, conflictele sunt rezolvate explicit în `MERGE_PROVENANCE.md`. Pachetul vechi rămâne ca arhivă, dar **nu mai este sursa de adevăr** (vezi pointer-ul de depreciere din el).

## Principiu de produs

Utilizatorul scrie în limbaj natural „Ce s-a întâmplat?". Aplicația clasifică evenimentul de viață și generează **graful complet de obligații administrative**: eveniment → obligații → trasee → documente → canale oficiale → notificări. Birocrația este primul modul.

## Reguli de execuție (inviolabile)

- **Producție, nu demo.** Totul matur, real, gata de producție. `demo_mode` există doar ca flag de test/fixture, niciodată ca adevăr implicit.
- **Zero invenții.** Nu se inventează instituții, documente, termene, taxe, coduri sau URL-uri. O regulă reală cere `source_claim_ids`; restul rămâne `REQUIRES_HUMAN_CURATION`.
- **Determinism la runtime.** Motorul de reguli și orchestratorul nu apelează LLM/internet/OCR la evaluare. AI doar clasifică text și extrage offline.
- **Reutilizează codul existent**: `services/api` (FastAPI), `packages/rule-engine` (`wb_rule_engine`), `packages/contracts`.

## Hartă de citire

1. `CODEX_START_HERE.md` — punct de intrare și ordine.
2. `MERGE_PROVENANCE.md` — ce vine din ce sursa și cum s-au rezolvat conflictele.
3. `00_PRODUCT_MANIFEST.md`, `01_SCOPE_RELEASES.md`, `02_PRD.md` — viziune, scop, cerințe.
4. `03_UX_FLOWS.md`, `04_DOMAIN_MODEL.md` — fluxuri și model (cu EventSession state machine).
5. `05_RULE_ENGINE_SPEC.md` — motor determinist (Partea A) + orchestrator eveniment (Partea B) + operatori predicat.
6. `06_LIFE_EVENT_CATALOG.md` — catalogul R1 cu descompunere și `depends_on`.
7. `06_SOURCE_GOVERNANCE.md`, `19_SOURCE_REGISTRY.json` — guvernanță + surse oficiale verificate.
8. `07_ARCHITECTURE.md`, `09_API_SPEC.yaml`, `10_DATABASE_SCHEMA.sql`, `contracts/`, `config/`, `seed/` — artefacte buildabile.
9. `11_SECURITY_PRIVACY.md`, `12_TEST_STRATEGY.md`, `13_DEFINITION_OF_DONE.md`, `17_DEPLOYMENT_RUNBOOK.md`, `18_CONTENT_OPERATIONS.md`.
10. `15_CODEX_MASTER_PROMPT.md`, `16_PHASE_PROMPTS.md` — execuție Codex.
11. `20_CANONICAL_DECISIONS.md`, `21_METRICS_AND_BUSINESS.md`, `22_PARTNER_NEUTRALITY_POLICY.md`, `23_TRACEABILITY_MATRIX.csv`.
