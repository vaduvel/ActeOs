# ⚠️ DEPRECAT — pachet fuzionat în super-book

Acest pachet (generat de GPT 5.5 Pro) a fost **fuzionat** în super-book-ul canonic, unica sursă de adevăr:

## → `docs/product/lifeos-romania/`

Nu mai editați fișierele din acest folder. Tot ce era valoros aici a fost reconciliat și mutat:

| Aici (vechi) | În super-book (canonic) |
|---|---|
| 02_EVENT_TAXONOMY.yaml | `seed/event_taxonomy.yaml` (frequency_tier: high/medium/low + `depends_on`) |
| 04_DOMAIN_MODEL.md (EventSession state machine) | `04_DOMAIN_MODEL.md` |
| 06_RULE_ENGINE_SPEC.md (operatori predicat) | `05_RULE_ENGINE_SPEC.md` (Part A motor + Part B orchestrator) |
| 08_ARCHITECTURE.md (RN Expo) | `07_ARCHITECTURE.md` (Android nativ — RN respins, ADR-022) |
| 09_API_SPEC.yaml | `09_API_SPEC.yaml` (endpoints fuzionate + `/v1/event-plans`) |
| 10_DATABASE_SCHEMA.sql | `10_DATABASE_SCHEMA.sql` (+ `event_plans`, `event_procedure_refs`, `route_runs`) |
| 11..21 + config/ + contracts/ + seed/ | omoloage în super-book |

## Decizii cheie de reconciliere

- **Stack:** Android nativ Kotlin + FastAPI + Next.js curator (NU React Native Expo) — ADR-022.
- **Producție, nu demo:** `demo_mode: false` implicit; `true` doar în fixture de test — ADR-023.
- **Tier vs freshness:** `frequency_tier` = high/medium/low; A/B/C rămâne DOAR pentru clase de freshness — ADR-024.
- **Home canonic unic:** `docs/product/lifeos-romania/` — ADR-025.
- **Convenție ID:** `life.*` pentru evenimente, `<domain>.<action>` pentru obligații — ADR-026.

Vezi `docs/product/lifeos-romania/MERGE_PROVENANCE.md` pentru detalii complete.
