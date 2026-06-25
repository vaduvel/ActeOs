# Definition of Done

## 1. Definition of Done pentru orice story

Un story este `done` numai când:

- codul și documentația sunt în path-urile declarate;
- criteriile de acceptare sunt demonstrate, nu doar afirmate;
- testele cerute sunt scrise și trec;
- format/lint/type-check trec fără suppressions nejustificate;
- nu există TODO/FIXME pentru behaviorul cerut;
- erorile au coduri stabile și mesaje localizabile;
- logurile și analytics au fost verificate pentru PII;
- documentația API/ADR/runbook este actualizată;
- schimbarea este accesibilă și observabilă;
- `IMPLEMENTATION_STATUS.md` conține comenzile și rezultatul;
- reviewerul poate reproduce local schimbarea dintr-un checkout curat.

## 2. Done pentru o regulă procedurală

- sursa este oficială și activă;
- snapshotul și hash-ul sunt păstrate;
- claim-urile au evidence excerpt + locator;
- jurisdicția, competența și intervalul temporal sunt explicite;
- predicatele sunt tipate și validate;
- toate cerințele critice au provenance;
- cazurile pozitive, negative și boundary trec;
- freshness SLA este setat;
- conflictele sunt rezolvate sau transformate în blocaj/confirmare;
- review-ul necesar riscului este complet;
- bundle-ul poate fi reprodus bit-for-bit.

## 3. Done pentru un traseu publicabil

- toate ramurile critice sunt mapate;
- localizarea vizată are date suficiente sau gaps vizibile;
- user flow răspunde la cele 5 întrebări operaționale;
- există next action, deadline, completion evidence și recovery;
- ruta oficială este allowlisted și testată;
- niciun pas nu promovează un partener comercial;
- golden route E2E trece offline/online unde se aplică;
- content owner și publisher aprobă;
- canary nu arată regresii;
- există procedură de retragere imediată.

## 4. Done pentru API/backend

- OpenAPI este actualizat și lintuit;
- contract tests trec;
- authn/authz/idempotency/rate limit sunt testate;
- query-urile sunt parametrizate și migrațiile sunt expand/contract;
- p95/p99 sunt în buget;
- failure modes și retries sunt bounded;
- metrics, traces și runbook există;
- ASVS baseline aplicabil este verde.

## 5. Done pentru Android

- debug și release compilează;
- testele unit/instrumented/UI trec;
- TalkBack și font scale 200% permit flow-ul;
- offline și process death sunt testate;
- no secrets și no sensitive backup;
- documentele rămân locale implicit;
- no PII in logs/analytics/crash reports;
- MASVS baseline aplicabil este verde;
- Play Console data safety inputs sunt documentate.

## 6. Done pentru portal curator

- RBAC este verificat server-side;
- editorul produce numai schema canonică;
- reviewerul vede dovada și impactul;
- self-approval critic este imposibil;
- publish/rollback sunt atomice și auditate;
- staleness/conflict/SLA sunt vizibile;
- ASVS baseline aplicabil este verde.

## 7. Done pentru release

- toate story-urile release-ului sunt done;
- zero P0/P1 deschise;
- vulnerabilități critical/high: zero sau acceptare formală cu termen;
- migration rehearsal și restore drill trec;
- backup curent verificat;
- bundle-urile sunt semnate/hash-uite;
- smoke staging și canary trec;
- privacy/legal/content sign-off există;
- rollback a fost exersat;
- release notes și customer-facing limitations sunt publicate.

## 8. Dovezi obligatorii în `IMPLEMENTATION_STATUS.md`

Pentru fiecare fază:

```text
Commit / branch:
Scope implementat:
Fișiere cheie:
Comenzi rulate:
Rezultate teste:
Coverage:
Migrații:
Security scans:
Known limitations:
ADR-uri:
Next phase entry gate:
```
