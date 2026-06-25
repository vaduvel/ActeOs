# Arhitectură — LifeOS România (canonic, reconciliat)

## Stack (vezi ADR-022)

- **Mobil:** Android nativ Kotlin 2.x + Jetpack Compose, minSdk 26. (React Native Expo din pachetul B este respins.)
- **API:** FastAPI (Python 3.13) — serviciul existent `services/api/src/wb_api`.
- **Motor:** `packages/rule-engine` (`wb_rule_engine`, `resolve`, `route_diff`, `ENGINE_VERSION`) + **orchestrator de evenimente** nou.
- **Contracte:** `packages/contracts` (schemele din `contracts/`).
- **Curator:** portal Next.js 16 / React 19.
- **Persistență:** PostgreSQL 17.
- **Regiune:** EU, conform GDPR.

## Structură monorepo (existentă, păstrată)

- `services/api` — FastAPI (catalog, evidence, feedback, journeys, routes, system; se adaugă routerul de evenimente).
- `packages/rule-engine` — motor determinist.
- `packages/contracts` — scheme și tipuri generate.
- `apps/curator` — portal de curatoriere (Next.js).
- `apps/mobile-android` — aplicația Android nativă.
- `data/` — taxonomie și bundle-uri (din `seed/`).
- `infra/` — Docker, migrări, runbook-uri.

## Runtime

Mobil → API → (Orchestrator eveniment → Rule Engine) → PostgreSQL. Workerii tratează snapshot-uri de surse, freshness și notificări. Extragerea AI este offline / pe partea de curator, niciodată decizie de runtime.

## Fluxul unei cereri de eveniment

1. `POST /v1/events/interpret` → candidate `event_type_id` + `required_facts` (assist-only).
2. `POST /v1/event-sessions` → creează sesiunea.
3. `PATCH /v1/event-sessions/{id}/facts` → colectează faptele.
4. `POST /v1/event-sessions/{id}/resolve` → orchestratorul produce planul (graf de obligații cu `depends_on`) și, per nod, motorul produce traseul determinist.
5. `GET /v1/routes/{id}` → traseul unui nod.
