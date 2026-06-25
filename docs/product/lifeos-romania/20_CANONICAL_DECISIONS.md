# Decizii de arhitectură canonice — LifeOS România

Deciziile ADR-001 … ADR-015 din pachetul anterior rămân valabile și se moștenesc integral (Android nativ, FastAPI monolith modular, PostgreSQL, reguli ca JSON canonic imutabil, fără LLM în runtime de rutare, local-first documents, cont opțional, OIDC/RBAC curatori, publicare bundle independentă, deep-link înainte de API, fail-closed pe stale critic, two-person rule, Docker-first, EU-region, fără ranking de parteneri).

Se adaugă deciziile specifice noii direcții:

| ADR | Decizie | Raționament | Revisit trigger |
|---|---|---|---|
| ADR-016 | Strat de orchestrare `LifeEvent` deasupra procedurilor (intents), nu rescriere a motorului | Reutilizează motorul determinist; separă compoziția de rezolvare | dacă compoziția cere stare partajată complexă între proceduri |
| ADR-017 | Planul de eveniment este determinist și are `event_plan_hash` (include engine + orchestrator version) | reproductibilitate și audit la nivel de eveniment | schimbare de model de versionare |
| ADR-018 | R1: pași naționali la nivel național; pași locali doar pilot Timiș; restul `verified_with_local_gap`/`needs_confirmation` | onestitate teritorială, extindere fără a minți | curatoriere locală pentru un nou UAT |
| ADR-019 | Clasificatorul NL „Ce s-a întâmplat?" mapează doar la un catalog controlat de evenimente; nu generează obligații | siguranță, fără chatbot liber | doar cu garduri și evaluare formală separată |
| ADR-020 | Dependențele dintre proceduri necesită claim aprobat (provenance), la fel ca cerințele critice | o dependență greșită produce drum inutil | niciodată relaxat pentru noduri critice |
| ADR-021 | Faptele se colectează o dată și se partajează în eveniment; minimizare și scop de retenție per fapt | UX și confidențialitate | cerințe legale de izolare |

Codex creează fișiere ADR formale în `docs/adr/` la implementare.
