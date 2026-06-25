# ADR-002 — Modular monolith before microservices

- **Status:** Accepted
- **Date:** 2026-06-25
- **Owners:** Product + Architecture

## Context

Domeniul este complex, dar volumul și frontierele reale nu sunt încă demonstrate. Microserviciile premature ar multiplica tranzacțiile distribuite, observabilitatea și costul operațional.

## Decision

Pornim cu un modular monolith: API FastAPI, worker separat ca proces și PostgreSQL comun, cu limite de module aplicate în cod.

## Consequences

Modulele au porturi explicite; extracția într-un serviciu separat cere ADR și dovezi de scalare, securitate sau ownership.

## Revisit triggers

- apar dovezi măsurabile că decizia blochează SLO, securitatea sau livrarea;
- contracte publice ori obligații legale schimbă premisele;
- costul operațional depășește beneficiul demonstrat;
- un înlocuitor este probat prin benchmark și plan de migrare.
