# 16 — Deployment & Operations Runbook

## 1. Environments

- `local`: date sintetice și servicii locale;
- `dev`: integrare continuă, niciun claim production;
- `staging`: copie anonimă/configurație production-like și ruleset candidate;
- `production`: numai rulesets aprobate și secrets reale.

Proiectele cloud, bazele și storage buckets sunt separate. Nu folosim prefixe într-o singură bază drept separare completă.

## 2. Branch și release

- trunk-based cu feature branches scurte;
- PR obligatoriu;
- release tag semnat;
- changelog tehnic și de produs;
- mobile channels dev/preview/production;
- ruleset publish este independent de app release.

## 3. Deploy backend

1. CI verde;
2. backup/restore point verificat;
3. migration expand;
4. deploy API canary;
5. smoke/contract tests;
6. deploy worker;
7. monitor errors/latency;
8. complete data migration;
9. contract cleanup într-un release ulterior.

## 4. Ruleset publish

1. manifest hash;
2. validation + fixtures;
3. independent approval;
4. publish transaction;
5. cache invalidation/version pointer update;
6. sample resolution compare;
7. queue impacted journeys;
8. monitor feedback/conflicts;
9. rollback pointer dacă gate-ul eșuează.

## 5. Mobile release

- generated client sync;
- native build reproducibil;
- permission diff review;
- privacy manifest/data safety forms update;
- a11y and security smoke;
- staged rollout;
- minimum supported version policy;
- remote kill switches for risky features, nu pentru core offline journey.

## 6. Rollback

- code: previous container/image;
- database: prefer roll-forward; rollback doar migration safe;
- ruleset: atomic pointer la versiunea anterioară;
- feature: flag off;
- mobile: EAS update pentru JS-safe fix sau store hotfix dacă native;
- source channel: mark suspended and remove from response.

## 7. Backup și disaster recovery

- automated DB backups + point-in-time recovery;
- storage versioning unde este compatibil cu deletion policy;
- ruleset manifests și snapshots replicate;
- encryption keys managed separately;
- restore drill documentat;
- RPO/RTO măsurate, nu presupuse.

## 8. Secret rotation

Inventar: DB, JWT, storage, push, observability, LLM extraction, email. Fiecare secret are owner, scope, rotation procedure și revocation test. Nu există cheie comună pentru mobile.

## 9. Emergency kill switches

- disable event family;
- disable rule/ruleset;
- force needs_confirmation;
- disable source fetcher/domain;
- disable cloud document processing;
- disable partner links;
- disable notifications;
- require minimum app version.

Kill switch-ul păstrează explicația și nu șterge silently traseul.

## 10. On-call checklist

- confirm severity și scope;
- stop harmful path;
- preserve evidence;
- identify ruleset/app versions;
- communicate factual status;
- remediate și verify;
- notify impacted users dacă este necesar;
- postmortem + test.
