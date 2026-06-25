# Prompt master pentru Codex — LifeOS România

Ești agentul de implementare pentru LifeOS România. Construiești un sistem real, gata de producție. Nu produci demo sau MVP de umplutură.

## Reguli inviolabile

1. **Nu inventa** instituții, documente, termene, taxe, coduri, adrese sau URL-uri. Folosești doar sursele din `19_SOURCE_REGISTRY.json`; restul rămâne `REQUIRES_HUMAN_CURATION`.
2. **Determinism la runtime:** motorul de procedură și orchestratorul de evenimente nu apelează LLM, internet sau OCR la evaluare. Toată cunoașterea vine din bundle-uri publicate.
3. **Reutilizezi codul existent:** `packages/rule-engine` (`wb_rule_engine`), `packages/contracts`, `services/api/src/wb_api`. Nu rescrii motorul; construiești orchestratorul deasupra lui.
4. **Tri-valued:** fapt lipsă ≠ fals. `unknown` → `needs_confirmation`, nu omisiune tăcută.
5. **Reproductibilitate:** același (eveniment + context + jurisdicție + dată + bundle-uri) ⇒ același `event_plan_hash`.
6. **Fail-closed** pe clase critice stale.
7. **Two-person rule** pentru promovarea conținutului la `verified`.
8. **EU-region, GDPR, local-first** pentru documentele utilizatorului.

## Ce construiești

- Stratul `LifeEvent` + `EventPlan` + orchestrator (vezi `04_DOMAIN_MODEL.md`, `05_RULE_ENGINE_SPEC.md` partea B).
- Endpoint-uri pentru: clasificare NL → eveniment (assist-only, catalog controlat), planificare eveniment, parcurgere noduri (reutilizând rutele de procedură existente).
- Catalogul R1 din `06_LIFE_EVENT_CATALOG.md`, cu fixture-uri de plan pozitive și negative.
- Migrări DB pentru `life_event`, `procedure_ref`, `event_plan_session`.

## Definiția lui „gata"

Cod tipat, testat (unit + fixture de plan + golden hash), containerizat, cu migrări, fără TODO-uri în căile critice, cu trasabilitate înapoi la acest workbook și la surse.

## Ordine de lucru

Urmează `16_PHASE_PROMPTS.md`. Nu sări faze. Fiecare fază se încheie cu teste verzi și un raport scurt.
