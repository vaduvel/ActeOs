# ExecPlan activ — ActeOS R0 → R1 Timișoara

- **Status:** ready_for_implementation
- **Plan owner:** principal implementation agent
- **Product owner:** ActeOS Product Team
- **Created:** 2026-06-25
- **Last updated:** 2026-06-25
- **Canonical backlog:** `codex/TASK_BACKLOG.yaml`
- **Phase prompts:** `codex/PHASE_PROMPTS.md`
- **Definition of Done:** `docs/22_DEFINITION_OF_DONE.md`

## 1. Purpose and observable outcome

Construiește o vertical slice production-oriented prin care un utilizator anonim poate:

1. descrie sau selecta un eveniment de viață activat;
2. răspunde progresiv la facts;
3. primi un traseu determinist cu pași, cerințe, deadline-uri, canale oficiale, surse și stări de încredere;
4. salva progresul local;
5. verifica formal documente pe dispozitiv fără verdict fals de autenticitate;
6. primi recalculare explicabilă când facts sau rulesetul se schimbă.

În paralel, un curator autorizat poate importa dovezi în inbox, crea drafturi, valida conflicte, simula impactul și publica un ruleset imutabil prin four-eyes approval.

R1 nu promite acoperire națională completă. Activează numai evenimentele pentru care există date oficiale aprobate și gate-uri verzi.

## 2. Context and repository map

- `apps/mobile`: experiența cetățeanului;
- `apps/admin`: portalul curatorilor;
- `services/api`: API FastAPI și use cases;
- `services/worker`: ingestie, change detection, freshness și notificări;
- `python/acteos_domain`: model de domeniu pur;
- `python/acteos_rule_engine`: resolver determinist;
- `contracts`: OpenAPI, JSON Schema și politici;
- `db`: migrations și RLS;
- `research/inbox`: material neaprobat;
- `data`: taxonomie și seed-uri, nu adevăr administrativ publicat implicit;
- `.agents/skills`: proceduri de lucru specializate.

## 3. Scope

### Included

- bootstrap monorepo, CI și reproducibilitate;
- contract generation și compatibility checks;
- predicate AST, temporal/jurisdiction resolver, DAG și trace;
- Postgres, repositories, RLS și audit;
- case/facts/resolve/journey API;
- shell mobil anonymous-first și persistence locală;
- UX complet al traseului și failure states;
- document readiness local formal;
- admin research/rule lifecycle;
- worker freshness/change detection;
- notifications/recalculation cu consimțământ;
- optional auth, household și privacy controls;
- observability, security hardening și release certification;
- import controlat al research-ului R1.

### Explicitly excluded from R1

- depunerea automată a cererilor la instituții fără integrare oficială;
- semnarea prin ROeID fără onboarding contractual/tehnic confirmat;
- verdict general de autenticitate al actelor;
- marketplace care cumpără prioritate în traseu;
- acoperirea tuturor celor 176 de evenimente;
- LLM runtime în decizia administrativă;
- scraping agresiv sau ocolirea controalelor surselor.

## 4. Invariants

- Output-ul resolverului este funcție de facts, jurisdiction, reference date și ruleset version.
- Un claim critic expirat/conflicting/unapproved nu poate produce `ready`.
- Fiecare pas critic păstrează `source_claim_ids` și explanation trace.
- Datele sintetice nu intră în bundle-ul de producție.
- Documentele rămân local implicit; cloud mode este explicit și revocabil.
- Ruta oficială DIY precedă orice partener.
- OpenAPI și JSON Schema preced implementările consumatorilor.

## 5. Milestones și gates

### M0 — Specification integrity (P0)

**Outcome:** orice agent poate bootstrap-ui repo-ul și valida pachetul identic.

- [ ] creează structura monorepo și lockfiles;
- [ ] implementează `make bootstrap`, `make validate`, `make test`;
- [ ] CI rulează pack validation, secret scan și production-bundle isolation;
- [ ] creează `IMPLEMENTATION_STATUS.md`.

**Gate:** checkout curat → bootstrap → validate trece fără pași manuali ascunși.

### M1 — Contract-first foundation (P1)

**Outcome:** API și modele generate, fără DTO-uri duplicate.

- [ ] validează OpenAPI 3.1.1 și toate JSON Schemas;
- [ ] generează client TypeScript și modele Python;
- [ ] configurează breaking-change check;
- [ ] adaugă contract tests.

**Gate:** generarea este deterministă și `git diff` rămâne gol la rerun.

### M2 — Deterministic domain and resolver (P2–P3)

**Outcome:** golden fixtures produc același traseu și trace pe orice rulare.

- [ ] domain types și typed predicate AST;
- [ ] validare statică a regulilor;
- [ ] temporal + jurisdiction applicability;
- [ ] graph build/topological ordering/cycle detection;
- [ ] conflict states și no-silent-resolution;
- [ ] property, metamorphic și golden tests.

**Gate:** fără I/O/LLM în engine; mutation/property suite nu găsește încălcări ale invariantelor.

### M3 — Persistence and API vertical slice (P4–P5)

**Outcome:** create case → set facts → resolve → fetch journey funcționează end-to-end.

- [ ] migrations, indexes, RLS și repositories;
- [ ] append-only audit și ruleset pinning;
- [ ] idempotency, concurrency și standard error envelope;
- [ ] integration tests cu Postgres real;
- [ ] traceability de la output la source claims.

**Gate:** API contract tests, RLS negative tests și replay test sunt verzi.

### M4 — Citizen mobile journey (P6–P7)

**Outcome:** utilizatorul anonim finalizează traseul pe iOS/Android și îl poate relua offline.

- [ ] Expo shell, navigation, local encrypted persistence;
- [ ] event search/select și natural-language intent candidate UX;
- [ ] progressive facts și reason-for-question;
- [ ] journey step standard: acum / termen / necesar / finalizare / recovery;
- [ ] confidence, source, stale/conflict/offline states;
- [ ] accessibility și critical copy snapshots.

**Gate:** E2E pe ambele platforme pentru happy path și failure paths; fără cont obligatoriu.

### M5 — Local document readiness (P8)

**Outcome:** utilizatorul primește verificări formale, acționabile, fără promisiuni de autenticitate.

- [ ] camera/import, secure local storage și lifecycle;
- [ ] OCR adapter și document classifier abstract;
- [ ] checks: exists/readable/type/not_expired/field/signature/name consistency;
- [ ] consent separat pentru cloud mode;
- [ ] delete source bytes + derived artifacts.

**Gate:** airplane-mode flow funcționează; logs/analytics nu conțin OCR text sau PII.

### M6 — Curator and source operations (P9–P10)

**Outcome:** o regulă poate parcurge inbox → claims → draft → review → simulate → publish.

- [ ] SSO/RBAC pentru admin;
- [ ] source registry, snapshots, atomic claims și locators;
- [ ] rule editor AST, static validation și conflict matrix;
- [ ] four-eyes approval și immutable publish;
- [ ] worker fetch, hash/diff, freshness și safe retry;
- [ ] SSRF/egress controls și rate limits.

**Gate:** autorul nu își poate aproba propriul claim critic; publish fără dovezi este blocat.

### M7 — Recalculation, identity and privacy (P11–P12)

**Outcome:** schimbările relevante sunt explicate, iar contul rămâne opțional.

- [ ] impact analysis și before/after explanation;
- [ ] notification preferences și quiet hours;
- [ ] anonymous→account migration fără pierdere;
- [ ] household roles, export și deletion;
- [ ] retention jobs și DSR evidence.

**Gate:** opt-out funcționează; deletion test elimină bytes și date derivate conform politicii.

### M8 — Hardening and R1 content import (P13–P14)

**Outcome:** sistemul este observabil, defensiv și servește numai reguli aprobate.

- [ ] SLO dashboards, traces și privacy-safe logs;
- [ ] threat model, SAST/DAST/dependency/container scans;
- [ ] importă research cu checksum și schema validation;
- [ ] curator independent verifică fiecare claim critic;
- [ ] simulează golden cases și impact pe cazuri active;
- [ ] activează numai evenimentele certificate.

**Gate:** security/privacy/research release gates sunt verzi; gap-urile rămân blocate explicit.

### M9 — Release certification (P15)

**Outcome:** staging exercise și rollout gradual pot fi repetate și inversate sigur.

- [ ] migration rehearsal și restore test;
- [ ] mobile/web/API E2E pe staging;
- [ ] accessibility, performance și resilience gates;
- [ ] signed rule bundle manifest și SBOM/provenance;
- [ ] staged rollout, kill switches și rollback drill;
- [ ] release verdict și owner on-call.

**Gate:** checklistul `operations/RELEASE_CHECKLIST.md` este complet cu dovezi.

## 6. Concrete execution procedure

Pentru fiecare milestone:

1. selectează stories dependente din backlog;
2. deschide branch-ul fazei și actualizează Progress;
3. rulează validatorul pack înainte de modificări;
4. implementează contract/domain/data înaintea UI-ului dependent;
5. adaugă teste în aceeași schimbare;
6. rulează comenzile de validare relevante;
7. documentează surprizele și deciziile;
8. actualizează OpenAPI/schema/docs/ADR dacă s-a schimbat comportamentul;
9. completează PR checklist și implementation status;
10. marchează milestone-ul doar după gate.

## 7. Validation commands

Comenzile țintă după bootstrap:

```bash
python infra/scripts/validate_pack.py
make validate
make test
make production-bundle-check
pnpm lint
pnpm typecheck
pnpm test
pytest -q
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

Pentru release se adaugă E2E mobile/web, a11y, security scans, migration rehearsal, backup restore și signed bundle verification.

## 8. Rollout and rollback

- contractele additive se lansează înaintea consumatorilor;
- migrațiile destructive cer expand/migrate/contract și backup verificat;
- ruleseturile se publică imutabil și pot fi dezactivate/revertate prin pointer, nu rescrise;
- funcțiile cu risc folosesc feature flags și cohort rollout;
- mobile păstrează compatibilitate cu minimum două versiuni API suportate sau primește forced-upgrade policy explicită;
- incidentul de reguli oprește rulesetul afectat fără a șterge auditul.

## 9. Progress

- [x] 2026-06-25T06:00:00Z — vision, doctrine, PRD, architecture, data, API, security și operations specification create.
- [x] 2026-06-25T06:00:00Z — event atlas, schemas, SQL, backlog și pack validator create.
- [x] 2026-06-25T06:00:00Z — Codex instructions, ExecPlan convention și repo-scoped skills create.
- [ ] M0 implementation started.
- [ ] M1 complete.
- [ ] M2 complete.
- [ ] M3 complete.
- [ ] M4 complete.
- [ ] M5 complete.
- [ ] M6 complete.
- [ ] M7 complete.
- [ ] M8 complete.
- [ ] M9 complete.

## 10. Surprises and discoveries

- Niciuna la începutul implementării. Adaugă aici rezultate care schimbă planul, nu simple defecte de rutină.

## 11. Decision log

- 2026-06-25 — modular monolith înainte de microservicii; motiv: consistență și cost operațional.
- 2026-06-25 — deterministic runtime; LLM numai în pipeline-ul asistat de cercetare.
- 2026-06-25 — anonymous-first și local-first pentru documente.
- 2026-06-25 — R1 activează evenimente numai după evidence/freshness/release gates.

## 12. Outcomes and retrospective

De completat după fiecare milestone cu: rezultat observabil, dovezi, deviații, cost operațional, riscuri și următorul pas.
