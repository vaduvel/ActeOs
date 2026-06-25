# PLANS.md — Convenția ExecPlan pentru ActeOS

## 1. Scop

Un ExecPlan este planul viu prin care un agent poate executa o schimbare semnificativă fără să depindă de context ascuns, conversații anterioare sau presupuneri. El descrie rezultatul observabil, etapele, constrângerile, validarea și recuperarea.

Planul activ al produsului se află în `codex/EXECUTION_PLAN.md`.

## 2. Când este obligatoriu

Scrie sau actualizează un ExecPlan înainte de lucru dacă este adevărată oricare condiție:

- schimbarea traversează două sau mai multe module/deployables;
- modifică OpenAPI, JSON Schema, SQL, RLS sau contracte publice;
- introduce sau schimbă un ruleset, un algoritm al resolverului ori politica de prospețime;
- necesită migrare de date, backfill, rollout gradual sau rollback;
- include integrare externă, procesare de documente, autentificare ori PII;
- depășește un PR simplu sau este probabil să continue în mai multe sesiuni;
- pregătește un release sau schimbă un control de securitate.

Pentru un defect local, izolat, cu test evident, poate fi suficient backlog story + PR checklist.

## 3. Proprietățile obligatorii ale planului

Planul trebuie să fie:

1. **Self-contained:** explică suficient context pentru un agent nou.
2. **Outcome-first:** descrie ce poate face utilizatorul după schimbare.
3. **Executable:** include fișiere, comenzi, ordine și dependențe.
4. **Testable:** fiecare milestone are dovezi observabile și gate.
5. **Living document:** Progress, Surprises, Decision Log și Outcomes se actualizează în timpul lucrului.
6. **Safe to resume:** arată ce este terminat, ce nu este și cum se reia.
7. **Reversible:** descrie rollback sau motivul pentru care schimbarea este forward-only.
8. **Traceable:** leagă requirement IDs, story IDs, ADR-uri și contracte.

## 4. Structura minimă

Orice ExecPlan conține:

- Purpose and user-visible outcome;
- Context and repository map;
- Scope / non-scope;
- Constraints and invariants;
- Milestones, dependencies and gates;
- Concrete implementation steps;
- Validation commands and expected evidence;
- Data migration / rollout / rollback;
- Security, privacy and accessibility checks;
- Progress checklist with timestamps;
- Surprises and discoveries;
- Decision log;
- Outcomes and retrospective.

## 5. Reguli de actualizare

- Folosește timestamp ISO 8601 în UTC pentru progres.
- Bifează numai rezultate demonstrate, nu intenții.
- Orice deviație față de arhitectură produce ADR propus înainte de implementare.
- Orice schimbare de scope se consemnează cu motiv și impact.
- Dacă un test eșuează, notează rezultatul înainte de remediere dacă el schimbă înțelegerea sistemului.
- La final, înlocuiește presupunerile cu rezultate și listează riscurile rămase.

## 6. Gate universal de milestone

Un milestone nu este complet până când:

- codul, contractele și documentația sunt sincronizate;
- lint, typecheck și testele relevante sunt verzi;
- contractele și migrațiile sunt validate;
- a11y, privacy și security checks aplicabile au trecut;
- observabilitatea și failure states există;
- rollback-ul este posibil sau explicit justificat;
- `IMPLEMENTATION_STATUS.md` și planul viu sunt actualizate.

## 7. Relația cu backlogul

`codex/TASK_BACKLOG.yaml` definește unitățile trasabile de lucru. ExecPlan-ul definește ordinea reală, integrarea și dovada că ele formează un rezultat utilizabil. Backlog story fără milestone poate fi implementată doar dacă este strict locală; milestone fără story IDs nu este acceptat.
