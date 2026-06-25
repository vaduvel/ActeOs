# 15 — Observability & SLO

## 1. Trei fluxuri separate

- product telemetry: utilizare agregată, fără PII;
- operational observability: logs, metrics, traces;
- compliance/security audit: append-only, acces restricționat.

Ele nu se amestecă. Auditul nu este trimis în analytics, iar logurile nu devin bază de profilare.

## 2. Core identifiers

Fiecare request/resolve păstrează:

- `request_id`;
- `trace_id`;
- `case_id` pseudonimizat;
- `journey_id`;
- `event_type_id`;
- `ruleset_version`;
- `engine_version`;
- `reference_date`;
- status/error code.

Nu păstrează fact values sensibile.

## 3. SLO R1

- API availability: 99,5% lunar;
- resolver successful technical execution: 99,9% din request-urile valide;
- P95 resolver: <500 ms cached;
- P95 GET journey: <350 ms;
- ruleset publish propagation: <5 minute;
- notification scheduling accuracy: 99% în fereastra configurată;
- source change detection: conform clasei de freshness, nu un singur SLA;
- restore verification: cel puțin lunar în staging.

## 4. Metrics

### API

request count/latency/errors by route, status, auth mode, app version.

### Rule engine

resolution status, rules evaluated, missing facts, conflicts, stale claims, graph size, cache hit.

### Content ops

source changes, claims due, publish failures, time-to-verify, open gaps, feedback volume.

### Mobile

crash-free sessions, cold start, offline errors, sync queue, document readiness duration.

### Security

auth failures, rate-limit hits, anomalous admin access, signed URL misuse, publish attempts.

## 5. Logs

Structured JSON, severity, event name și IDs. Redaction denylist + allowlist. Free text de la user nu este logat. Query parameters sensibili sunt eliminați. Exception traces sunt scrubbed înainte de vendor.

## 6. Alerts

P0:

- document exposure or cross-user access;
- ruleset integrity/hash failure;
- critical wrong rule confirmed;
- admin compromise.

P1:

- critical claims hard-expired în event active;
- resolver error rate spike;
- DB unavailable;
- ruleset publish failure with partial state;
- official channel domain changed unexpectedly.

## 7. Dashboards

- product outcome;
- API health;
- rule engine health;
- source/freshness;
- admin/security;
- mobile release adoption;
- jobs/notifications.

## 8. Error budgets

Când error budget-ul unui SLO este consumat, funcționalitățile noi din zona afectată se opresc în favoarea fiabilității. Rule correctness incidents au prioritate indiferent de availability budget.
