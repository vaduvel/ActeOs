# wb-api

Persistence layer for Waze-birocratie (P1).

- `crypto.py` - envelope field encryption (AES-256-GCM, key id + AAD binding).
- `audit.py` - append-only, hash-chained audit log (tamper-evident).
- `idempotency.py` - request-fingerprinted idempotency (new / replay / conflict).
- `models.py` - SQLAlchemy 2.0 models (journeys, route snapshots, audit, idempotency).
- `migrations/` - Alembic; the initial migration installs a trigger that makes
  `audit_events` reject UPDATE and DELETE at the database level.

Pure logic (crypto, audit, idempotency) has no database dependency and is unit
tested without Postgres. Models/migrations target PostgreSQL 17.
