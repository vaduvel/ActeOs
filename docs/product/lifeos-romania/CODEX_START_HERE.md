# START HERE — LifeOS România (Super-Book)

Acesta este pachetul canonic unic. Citește în ordine și nu sări peste contracte.

## Ordine de citire

1. `15_CODEX_MASTER_PROMPT.md` — misiunea și regulile inviolabile.
2. `MERGE_PROVENANCE.md` — deciziile de fuziune (stack, ID-uri, demo vs producție, tier vs freshness).
3. `01_SCOPE_RELEASES.md`, `02_PRD.md`, `04_DOMAIN_MODEL.md`, `05_RULE_ENGINE_SPEC.md`, `06_LIFE_EVENT_CATALOG.md`.
4. Contractele tehnice sunt sursa de adevăr: `contracts/*.schema.json`, `09_API_SPEC.yaml`, `10_DATABASE_SCHEMA.sql`.
5. Implementează fazele din `16_PHASE_PROMPTS.md` în ordine P0–P12, reutilizând codul existent.

## Reguli de adevăr (din pachetul canonic anterior, păstrate)

- Nu inventa instituții, documente, termene, taxe, coduri sau URL-uri.
- Orice regulă administrativă reală are nevoie de `source_claim_ids`. Fără ele rămâne `REQUIRES_HUMAN_CURATION`.
- `demo_mode` este permis doar pentru fixture-uri de test, marcat explicit; niciodată ca adevăr de producție.
- Necunoscut ≠ fals (logică tri-valued). `unknown` pe o ramură critică → `NEEDS_FACTS` / `needs_confirmation`.
- Reproductibilitate: același (eveniment + fapte + jurisdicție + dată + bundle + versiuni) ⇒ același `route_hash`/`event_plan_hash`.

## Stack canonic (reconciliat)

- Backend: **FastAPI** existent (`services/api/src/wb_api`).
- Motor: **`packages/rule-engine`** (`wb_rule_engine`) + orchestrator de evenimente deasupra.
- Mobil: **Android nativ Kotlin/Compose** (ADR-001 din pachetul original). React Native NU se adoptă (vezi MERGE_PROVENANCE / ADR-022).
- Curator: portal **Next.js/React**.
- Persistență: **PostgreSQL**.

Comandă conceptuală pentru Codex:

```text
Build LifeOS Romania from this single canonical super-book. Reuse existing FastAPI service and rule-engine. Add the LifeEvent orchestration layer above the deterministic engine. Keep AI out of runtime legal/admin decisions. Production posture, not demo. Real rules require source claims. Do not invent administrative requirements.
```
