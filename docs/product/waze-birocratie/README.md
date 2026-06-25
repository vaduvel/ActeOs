# Waze pentru birocrație — Codex Execution Pack

Acesta este pachetul canonic de implementare. Nu este un pitch și nu este un prototip de design. Conține contractele, arhitectura, regulile de adevăr, backlogul, testele și instrucțiunile după care Codex trebuie să construiască produsul.

## Ordinea obligatorie de citire

1. `CODEX_START_HERE.md`
2. `00_PRODUCT_MANIFEST.md`
3. `01_SCOPE_RELEASES.md`
4. `02_PRD.md`
5. `03_UX_FLOWS.md`
6. `04_DOMAIN_MODEL.md`
7. `05_RULE_ENGINE_SPEC.md`
8. `06_SOURCE_GOVERNANCE.md`
9. `07_ARCHITECTURE.md`
10. `08_API_SPEC.yaml`
11. `09_DATABASE_SCHEMA.sql`
12. `10_SECURITY_PRIVACY.md`
13. `11_DESIGN_SYSTEM.md`
14. `12_TEST_STRATEGY.md`
15. `13_BACKLOG.yaml`
16. `14_DEFINITION_OF_DONE.md`
17. `15_CODEX_MASTER_PROMPT.md`
18. `16_PHASE_PROMPTS.md`
19. `17_DEPLOYMENT_RUNBOOK.md`
20. `18_CONTENT_OPERATIONS.md`

## Reguli de execuție care nu se negociază

- Datele procedurale de producție provin exclusiv din surse oficiale/publice verificabile.
- Nu se publică nicio regulă fără `source_claim` și review uman.
- Nu se folosește LLM la runtime pentru a decide pașii, eligibilitatea, documentele ori termenele.
- Nu se servește tăcut o regulă critică depășită de pragul de prospețime.
- Datele sintetice sunt permise numai în test și trebuie etichetate `TEST_ONLY`.
- Documentele utilizatorului rămân pe dispozitiv în configurația implicită.
- Orice integrare publică este implementată numai la nivelul permis de documentația și acordul oficial; altfel folosim deep-link.
- Codul este considerat terminat numai când criteriile din `14_DEFINITION_OF_DONE.md` sunt îndeplinite.

## Livrabilul tehnic urmărit

Un monorepo production-grade cu:

- aplicație Android nativă;
- API FastAPI;
- worker de ingestie și monitorizare a surselor;
- portal web pentru curatori;
- motor determinist de reguli;
- PostgreSQL + storage S3-compatibil;
- CI/CD, migrații, observabilitate, audit și teste;
- două trasee publicabile în R1: înscriere preșcolar și înscriere clasa pregătitoare;
- infrastructură gata pentru extindere la liceu, identitate, stare civilă, auto, proprietate, fiscal și beneficii.

## Ce nu trebuie făcut

Nu se umple aplicația cu liste generice doar ca să pară mare. O călătorie este vizibilă utilizatorului numai când are acoperire `production`, surse actuale și toate ramurile critice testate.
