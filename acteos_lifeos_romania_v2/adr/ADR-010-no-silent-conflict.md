# ADR-010 — No silent conflict resolution

- **Status:** Accepted
- **Date:** 2026-06-25
- **Owners:** Product + Architecture

## Context

Rangul juridic, competența, teritoriul, temporalitatea și delegarea trebuie evaluate. Unele conflicte necesită confirmare umană.

## Decision

Conflictele dintre surse nu sunt rezolvate prin ordinea de ingestie sau prin „cea mai locală sursă”.

## Consequences

Resolverul poate aplica numai reguli compatibile; altfel produce `CONFLICTING_SOURCE` și recovery action.

## Revisit triggers

- apar dovezi măsurabile că decizia blochează SLO, securitatea sau livrarea;
- contracte publice ori obligații legale schimbă premisele;
- costul operațional depășește beneficiul demonstrat;
- un înlocuitor este probat prin benchmark și plan de migrare.
