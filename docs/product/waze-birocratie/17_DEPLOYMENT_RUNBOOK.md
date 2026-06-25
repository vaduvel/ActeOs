# Deployment and operations runbook

## 1. Reference topology

### Local

- Docker Compose: PostgreSQL 16, MinIO, mail catcher, API, worker, curator portal.
- Android emulator/device points to local API through a build variant.

### Staging/production reference

- **PostgreSQL + auth/storage:** EU-region managed Postgres; Supabase EU is acceptable if configured and contractually approved.
- **API/worker:** OCI containers in an EU region with background jobs and private network access to DB/storage.
- **Curator portal:** Vercel EU-capable deployment or the same container platform; server routes only, no secrets in client bundle.
- **Object storage:** EU-region S3-compatible bucket with versioning, encryption and lifecycle policies.
- **Queue/scheduler:** managed Redis/queue or Postgres-backed job system initially; exact choice recorded in ADR.
- **Observability:** OpenTelemetry collector, metrics, logs and traces in an EU-compatible provider.

The code must stay provider-agnostic. No integration is considered active solely because a provider is named here.

## 2. Environments

| Environment | Purpose | Data |
|---|---|---|
| local | development | synthetic TEST_ONLY + local official snapshots |
| CI | automated verification | synthetic TEST_ONLY |
| staging | production-like acceptance | sanitized fixtures + verified content bundles |
| production | citizens and curators | real journey metadata; local documents remain client-side by default |

Databases, buckets, keys, auth tenants and analytics projects are isolated per environment.

## 3. Required environment variables

See `.env.example`. Categories:

- application identity/version;
- database DSN and pool limits;
- object storage endpoint/bucket/credentials;
- encryption KMS/master-key reference, never raw key in repo;
- OIDC issuer/client/audience for curator;
- worker queue/scheduler;
- AI extraction provider, disabled by default;
- OpenTelemetry endpoints;
- allowed origins and official outbound host policy;
- feature flags for ROeID/ANAF/Ghișeul/Hub integrations;
- notification providers.

Startup must fail closed when a required production variable is absent.

## 4. Local bootstrap

```bash
cp .env.example .env
make doctor
make bootstrap
make up
make migrate
make seed-verified
make smoke-local
```

`seed-verified` loads only the committed, schema-valid content package. It must not scrape live sites.

## 5. Database changes

Use expand/contract:

1. add nullable/new structures;
2. deploy backward-compatible code;
3. backfill with bounded job;
4. verify counts/checksums;
5. switch reads/writes;
6. remove old structures in a later release.

Every migration records:

- expected duration and lock profile;
- forward fix;
- rollback or restore strategy;
- data validation query;
- owner.

Never run destructive migrations automatically with the first application pod.

## 6. Deploy sequence

1. Freeze the release manifest and SBOM.
2. Verify latest backup and restore timestamp.
3. Run migration preflight against staging clone.
4. Deploy API/worker canary with no traffic.
5. Run readiness and internal contract smoke.
6. Shift 5% traffic.
7. Watch error rate, latency, DB saturation and route mismatch.
8. Promote 25% → 50% → 100% if gates remain green.
9. Deploy portal.
10. Release Android through internal → closed → staged production track.
11. Publish content bundle independently after content gates.

## 7. Rollback thresholds

Automatic or immediate manual rollback when:

- HTTP 5xx > 2% for 5 minutes;
- route resolve p95 > 1.5 s for 10 minutes;
- deterministic mismatch or unknown bundle hash appears;
- authorization regression;
- PII in logs;
- critical rule bundle incident;
- migration corrupts validation counts.

Application rollback must preserve DB compatibility. Content rollback changes the current publication pointer atomically.

## 8. Content emergency procedure

1. Mark affected bundle `retired` or point to last known good publication.
2. Public API returns `needs_confirmation`/unavailable for affected journey if no safe bundle exists.
3. Notify active affected users without exposing procedure details on lockscreen.
4. Open critical incident and preserve evidence.
5. Curate, review, test, canary and republish.
6. Publish an incident note and learning review.

## 9. Backup and restore

- PostgreSQL PITR + daily encrypted snapshot;
- object storage versioning + lifecycle;
- rule bundles additionally exported as signed immutable artifacts;
- key configuration backed up through provider KMS policy, not raw export;
- restore drill at least quarterly and before major schema changes.

Targets: RPO 24h maximum for operational data, lower where provider supports PITR; RTO 4h. Published rule bundles must be immediately recoverable from signed artifacts.

## 10. Secret rotation

- database credentials: 90 days or managed short-lived;
- OIDC client secrets: 90 days;
- storage credentials: short-lived workload identity preferred;
- signing keys: hardware/KMS-backed with documented rotation;
- notification credentials: 90 days;
- emergency rotation after any suspected exposure.

Rotation is tested in staging without downtime.

## 11. Observability minimum

Dashboards:

- API golden signals;
- route resolve by engine/bundle version;
- DB pool/locks/slow queries;
- worker queue/failures/source staleness;
- content conflicts and review SLA;
- Android crash/ANR without sensitive payload;
- privacy jobs and deletion failures.

Every page alert links to a runbook and owner.

## 12. External integration states

Use these runtime states:

- `DISABLED` — feature not enabled;
- `NOT_CONFIGURED` — adapter exists, credentials/agreement absent;
- `SANDBOX` — official test environment;
- `CANARY` — limited production use;
- `ACTIVE` — approved production;
- `DEGRADED` — adapter failing, route falls back to safe deep-link;
- `SUSPENDED` — security/legal/content incident.

ROeID, ANAF and payment capabilities stay `NOT_CONFIGURED` until formal requirements are satisfied. Deep-links are separate features.
