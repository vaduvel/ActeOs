# 27 — Integrarea pachetului v2 ca donator

**Data:** 2026-06-25

Pachetul `acteos_lifeos_romania_v2/` (generat de GPT 5.5 Pro, 121 fișiere, validare PASS) este cel mai matur artefact. Decizie: **NU îl adoptăm wholesale**; îl folosim ca **donator** peste super-book-ul canonic `docs/product/lifeos-romania/`. Motivul principal: depindem de **funcții native de OCR** pe Android, deci nu schimbăm stack-ul.

## ADR-027 — v2 adoptat ca donator, stack neschimbat

- **Decizie:** păstrăm stack-ul actual — **Android nativ Kotlin** + FastAPI `wb_api` + `wb_rule_engine` + curator Next.js. Respingem stack-ul mobil din v2 (Expo/React Native, ADR-012 v2).
- **Motiv:** dependențe native de OCR și cod Android deja scris; migrarea pe RN ar rescrie exact zona cu cel mai mare risc.
- **Consecință:** ADR-012 din v2 este **suprascris** de această decizie. ADR-022 din super-book rămâne în vigoare.

## ADR-028 — Convenție de ID păstrată

- **Decizie:** păstrăm `life.*` (evenimente) și `<domain>.<action>` (obligații), deja cablate în cod și seed.
- **Mapare către v2:** `life.moved ↔ ro.life.moved_home`, `life.bought_vehicle ↔ ro.life.bought_vehicle`, `life.lost_documents ↔ ro.life.lost_documents`. La importul taxonomiei v2 se aplică această normalizare.

## ADR-029 — Motor: adoptăm modelul aprofundat din v2

- **Decizie:** `08_RULE_ENGINE_DEEP_SPEC.md` (predicate AST, efecte, jurisdiction resolver, temporal engine, conflict model, freshness, proprietăți testabile) devine specificația canonică a motorului, implementată în `wb_rule_engine`. Orchestratorul Part B (graf `depends_on`, `event_plan_hash`) coexistă, exprimat prin `trigger_child_event` + muchii explicite.

## ADR-030 — Contracte și metodologie din v2

- **Decizie:** adoptăm schemele mai bogate (`predicate`, `rule`, `source_claim`, `ruleset_manifest`), `freshness_policy` pe clase (critical/operational/explanatory), `error_codes` extins, convenția **ExecPlan** și cele 4 **skills** repo-scoped.

## Ce transplantăm din v2 (independent de stack)

- specificația aprofundată a motorului → `08_RULE_ENGINE_DEEP_SPEC.md`;
- doctrina D1–D20 → `24_PRODUCT_DOCTRINE.md`;
- Data Bible → `25_DATA_BIBLE.md`;
- model de execuție + ExecPlan + skills → `26_EXECUTION_MODEL_AND_PLANS.md` + `skills/`;
- contracte JSON și config → `contracts/` + `config/`;
- brief-uri de cercetare R1 → rămân referite din `acteos_lifeos_romania_v2/research/briefs/` (surse reale, nu se dublează).

## Ce NU luăm din v2

- stack-ul mobil Expo/RN (ADR-027);
- re-scaffold-ul monorepo care ar înlocui `wb_api`/`wb_rule_engine`;
- a treia convenție de ID (`ro.life.*`) ca formă canonică — doar ca mapare.

## Status surse de adevăr

- **Canonic:** `docs/product/lifeos-romania/` (acest super-book, îmbogățit cu donor v2).
- **Donator de referință:** `acteos_lifeos_romania_v2/` (se păstrează pentru research, OpenAPI, backlog și taxonomie; stack-ul său mobil e suprascris).
- **Depreciate:** `lifeos_romania_codex_pack_v1/` și workbook-ul inițial.
