# ADR-009 — Immutable ruleset publication

- **Status:** Accepted
- **Date:** 2026-06-25
- **Owners:** Product + Architecture

## Context

Trebuie să putem reproduce traseul istoric și să facem rollback sigur.

## Decision

Publicarea creează un manifest imutabil și semnat logic, nu modifică reguli active in-place.

## Consequences

Cazurile păstrează `ruleset_version`; retragerea produce o versiune nouă sau status explicit, cu audit.

## Revisit triggers

- apar dovezi măsurabile că decizia blochează SLO, securitatea sau livrarea;
- contracte publice ori obligații legale schimbă premisele;
- costul operațional depășește beneficiul demonstrat;
- un înlocuitor este probat prin benchmark și plan de migrare.
