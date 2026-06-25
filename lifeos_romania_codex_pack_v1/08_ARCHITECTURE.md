# Architecture

## Monorepo
- `apps/mobile`: React Native Expo app.
- `apps/api`: FastAPI.
- `apps/curator`: Next.js/React admin portal.
- `packages/contracts`: schemas and generated types.
- `packages/rule-engine`: deterministic engine.
- `data/seeds`: taxonomy and demo bundles.
- `ops`: Docker, migrations, runbooks.

## Runtime
Mobile -> API -> Rule Engine -> Postgres. Workers handle snapshots, freshness, notifications. AI extraction is offline/curator-side, not runtime decisioning.
