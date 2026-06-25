# 14 — Test Strategy

## 1. Obiectiv

Testarea trebuie să demonstreze nu doar că aplicația rulează, ci că motorul produce aceeași rută pentru aceleași condiții, nu publică afirmații fără dovezi și nu pierde date/progres la schimbări de reguli.

## 2. Piramida

### Unit

- predicate operators;
- temporal boundaries;
- jurisdiction selection;
- graph composition/toposort;
- conflict detection;
- freshness policy;
- readiness checks;
- copy/format helpers.

### Property-based

Folosim Hypothesis pentru:

- determinism;
- no cycles after valid composition;
- stable ordering;
- boundary dates;
- fact completeness;
- idempotent recalculation;
- no critical effect without claim.

### Contract

- OpenAPI schema validation;
- generated client compile;
- response conformance;
- backward compatibility diff;
- consumer contract tests mobile/admin.

### Integration

- Postgres repositories;
- RLS/authz;
- ruleset publish transaction;
- job queue retry/dead letter;
- storage signed URL lifecycle;
- notification outbox.

### E2E

- mobile: Maestro pe flows canonice;
- admin: Playwright pentru source→claim→rule→publish;
- API: test journey from case facts to rendered response;
- offline/online resync;
- account deletion/document deletion.

## 3. Data test policy

- `testdata/` este singurul loc pentru date sintetice;
- fiecare fixture are `data_class: synthetic_test_only`;
- domenii `.test`/`.invalid` și instituții fictive clar marcate;
- build production rule bundle refuză orice `data_class` sintetic;
- research inputs reale intră în `research/inbox` până la approval;
- CI verifică proveniența fiecărui rule production.

## 4. Rule fixture matrix

Pentru fiecare event R1:

- happy path;
- missing fact;
- conditional requirement true/false;
- exact date boundary;
- local jurisdiction vs alt UAT;
- claim stale;
- claim hard-expired;
- conflict official sources;
- source unavailable;
- recalculation adds step;
- recalculation removes step;
- progress migration;
- unknown/pending publication;
- malformed rule rejected;
- graph cycle rejected.

Minimum 20 fixtures/event family înainte de release; complex events pot avea mult mai multe.

## 5. Document readiness tests

- wrong document type;
- unreadable/partial image;
- expired/not expired boundary;
- missing required field;
- names inconsistent;
- address inconsistent;
- signature visible/uncertain;
- multipage missing page;
- no authenticity claim;
- local-only no network;
- cloud consent absent;
- deletion cleans derived artifacts.

## 6. Security tests

- OWASP ASVS/MASVS checklist mapping;
- SAST, dependency and secret scanning;
- authz matrix tests;
- RLS tests with cross-user access attempts;
- upload content-type spoofing;
- SSRF in source fetcher;
- malicious PDF/HTML extraction;
- prompt injection content;
- rate limits;
- signed URL replay/expiry;
- admin publish separation of duties;
- log redaction tests.

## 7. Accessibility tests

Automat:

- contrast/touch target where tooling supports;
- labels/roles;
- web axe checks;
- keyboard navigation admin.

Manual:

- VoiceOver/TalkBack;
- 200% text;
- reduced motion;
- screen sizes mici;
- limbaj clar cu utilizatori reali.

## 8. Performance tests

- resolver 10k rules synthetic benchmark;
- journey response payload size;
- cold/warm API;
- mobile cold start and SQLite read;
- ruleset cache load;
- admin diff pentru ruleset mare;
- job queue backlog recovery.

Performanța nu justifică eliminarea trace-ului sau evidenței.

## 9. Resilience tests

- DB connection loss;
- source portal timeout;
- worker crash mid-job;
- duplicate notification;
- stale mobile cache;
- ruleset rollback;
- storage unavailable;
- partial deployment;
- expired signing key.

## 10. Coverage

Nu folosim un procent unic drept mască. Gate-uri:

- rule engine și predicate: branch coverage ≥ 95%;
- security/authz: toate ramurile critice;
- API application services: ≥ 85%;
- UI: flows și state matrix, nu snapshot-uri inutile;
- fiecare bug P0/P1 produce regression test.

## 11. CI gates

1. format/lint;
2. typecheck;
3. unit/property;
4. schema/OpenAPI validation;
5. SQL migration checks;
6. contract tests;
7. security scans;
8. no-test-data-production check;
9. build mobile/admin/api;
10. E2E smoke pe staging pentru release branch.

## 12. Release certification

Un release nu este certificat dacă:

- există critical rules hard-expired în scope R1;
- OpenAPI și client generated diferă;
- migration nu a fost testată pe copie staging;
- rollback nu este definit;
- document deletion eșuează;
- un flow critic nu trece offline/poor network;
- a11y P0/P1 rămâne deschis;
- security scan are finding critic neacceptat explicit.
