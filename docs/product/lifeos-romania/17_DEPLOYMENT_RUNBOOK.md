# Runbook de deployment — LifeOS România

## Medii

- `local` (Docker Compose), `staging`, `prod` (EU-region).

## Pași

1. Build imagini API + workers; rulare migrări (`10_DATABASE_SCHEMA.sql` + migrări eveniment).
2. Seed taxonomie din `seed/event_taxonomy.yaml`. Bundle-urile demo NU se încarcă în prod.
3. Publicare bundle-uri de producție doar prin curator (two-person rule + impact analysis).
4. Healthchecks: `/health`, conexiune DB, versiune motor, versiune orchestrator.
5. Observabilitate: loguri structurate (PII redactat), metrici de rute/planuri, alerte freshness.

## Rollback

- Bundle: `status=retracted` + revenire la versiunea anterioară publicată; rutele se reevaluează.
- Cod: redeploy imagine anterioară; migrările sunt aditive/reversibile.

## Fail-closed

- Regulă critică stale → nodul nu poate ajunge `READY_TO_SUBMIT`; se afișează `needs_confirmation`.
