# 22 — Definition of Done

## Story DoD

- acceptance criteria trec;
- tests relevante adăugate;
- typecheck/lint green;
- contract și docs actualizate;
- analytics/observability definite fără PII;
- accessibility states verificate;
- security/privacy impact notat;
- error/recovery/offline states tratate;
- no TODO critic ascuns;
- reviewer aprobă.

## Rule DoD

- source snapshot și hash;
- atomic claims;
- authority/competence/territory/date;
- predicate/effects validate;
- claims active/fresh;
- fixtures și simulation;
- conflict matrix;
- content review;
- independent approval;
- publish/rollback manifest.

## API DoD

- OpenAPI first;
- authz;
- validation și error envelope;
- idempotency/concurrency;
- contract tests;
- rate limit și observability;
- generated client updated;
- backward compatibility verified.

## Mobile screen DoD

- loading/empty/error/offline;
- text scale/screen reader;
- no color-only state;
- analytics safe;
- local persistence behavior;
- privacy copy;
- platform parity sau diferență documentată.

## Release DoD

- toate phase gates;
- rules critical green;
- security/a11y reviews;
- migrations/backup/rollback;
- privacy/store disclosures;
- monitoring/alerts;
- support/runbook;
- signed artifact și manifest;
- staged rollout plan.
