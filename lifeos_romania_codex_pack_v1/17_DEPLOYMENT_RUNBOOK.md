# Deployment Runbook

## Local
`docker compose up`
Run migrations, seed taxonomy, start API and mobile.

## Rollback
Rule bundle rollback is atomic: change current published bundle pointer. Code rollback uses normal deployment rollback.

## Smoke tests
- GET /health
- List event types
- Create session life.moved
- Resolve route
- Fetch route
