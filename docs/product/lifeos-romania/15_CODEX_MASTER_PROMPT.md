# Prompt master pentru Codex — LifeOS România (canonic)

Construiești LifeOS România din acest super-book unic. Sistem real, gata de producție. Fără demo de umplutură.

## Misiune

Transformă „mi s-a întâmplat X" în trasee administrative deterministe, personalizate, verificate și explicabile: eveniment → obligații → trasee → documente → canale oficiale → notificări.

## Non-negociabile

- Nu inventa reguli juridice/administrative. Regulile critice de producție cer `source_claim_ids`.
- `demo_mode` doar pentru fixture de test, marcat explicit; default `false`.
- LLM/AI poate clasifica text sau redacta conținut **offline**, dar nu decide niciodată eligibilitate sau documente la runtime.
- Motorul determinist + orchestratorul sunt sursa deciziilor de runtime (fără LLM/net/OCR).
- Ofertele de parteneri nu pot modifica traseele oficiale.
- Reproductibilitate prin `route_hash` și `event_plan_hash`.

## Stack (reconciliat — vezi ADR-022)

- Mobil: Android nativ Kotlin/Compose (minSdk 26). NU React Native.
- API: FastAPI existent (`services/api/src/wb_api`).
- Motor: `packages/rule-engine` (`wb_rule_engine`) + orchestrator de evenimente.
- Persistență: PostgreSQL. Curator: Next.js/React.

## Ce construiești nou peste codul existent

- Stratul `LifeEvent` + `EventSession` + `EventPlan` + orchestrator (`04`, `05`).
- Endpoint-uri eveniment (interpret, sessions, facts, resolve/plan) — `09_API_SPEC.yaml`.
- Catalogul R1 ca date (`06_LIFE_EVENT_CATALOG.md`, `seed/`), cu fixture-uri pozitive și negative.
- Migrări pentru tabelele noi (`10_DATABASE_SCHEMA.sql`).

## Definiția lui „gata"

Cod tipat, testat (unit + fixture de rută/plan + golden hash), containerizat, cu migrări, fără TODO în căi critice, trasabil înapoi la acest super-book și la surse.

## Execuție

Urmează `16_PHASE_PROMPTS.md` (P0–P12). La finalul fiecărei faze: teste verzi + actualizare status.
