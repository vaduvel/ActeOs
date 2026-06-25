> **⚠️ STACK OVERRIDE (2026-06-25).** Acest pachet v2 este folosit ca **DONATOR**, nu ca sursa unică de adevăr. Sursa canonică este `docs/product/lifeos-romania/`. Deciziile de **stack** din v2 (Expo/React Native, ADR-012) sunt **suprascrise**: produsul rămâne pe **Android nativ Kotlin + FastAPI `wb_api` + `wb_rule_engine`** din cauza dependențelor native de OCR. Vezi `docs/product/lifeos-romania/27_V2_DONOR_INTEGRATION.md` (ADR-027..030). Conținutul independent de stack (motor, contracte, doctrină, Data Bible, research, backlog) rămâne valabil și a fost transplantat în super-book.

---

# ActeOS / LifeOS România — Master Execution Pack v2.0.0

**Data pachetului:** 2026-06-25  
**Scop:** donator de referință pentru produs, design, arhitectură, cercetare, implementare și operare (sursa canonică: `docs/product/lifeos-romania/`).

ActeOS transformă un eveniment exprimat de utilizator — „m-am mutat”, „mi-am cumpărat o mașină”, „mi-am pierdut actele” — într-un traseu administrativ personalizat, determinist, temporal, teritorial și verificabil.

## Ordinea obligatorie de citire

1. `CODEX_START_HERE.md`
2. `AGENTS.md`
3. `PLANS.md`
4. `codex/EXECUTION_PLAN.md`
5. `docs/01_VISION_MANIFEST.md`
6. `docs/02_PRODUCT_DOCTRINE.md`
7. `docs/03_PRODUCT_STRATEGY_PRD.md`
8. `docs/04_EVENT_ATLAS.md`
9. `docs/05_RULE_ENGINE_SPEC.md`
10. `docs/06_UX_BIBLE.md`
11. `docs/08_ARCHITECTURE.md`
12. `docs/09_DATA_BIBLE.md`
13. `docs/26_CODEX_EXECUTION_MODEL.md`
14. `contracts/openapi.yaml`
15. `codex/CODEX_MASTER_PROMPT.md`
16. `codex/PHASE_PROMPTS.md`
17. `codex/TASK_BACKLOG.yaml`

## Regula absolută

Nicio cerință administrativă critică nu intră în producție fără `source_claim` aprobat, perioadă de valabilitate, jurisdicție și stare de prospețime. Datele sintetice sunt permise exclusiv în `testdata/` și CI blochează importul lor în bundle-ul de producție.

## Livrabile în pachet

- doctrină completă de produs;
- taxonomie extinsă a evenimentelor de viață;
- specificația motorului determinist;
- UX Bible și design system;
- arhitectură modulară, API-first și local-first pentru documente;
- OpenAPI, JSON Schemas și SQL;
- securitate, confidențialitate, accesibilitate și operațiuni;
- plan de cercetare și guvernanță a surselor;
- backlog și prompturi Codex fazate;
- repo scaffold și validatoare automate.
