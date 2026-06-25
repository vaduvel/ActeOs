# ADR-001 — Event-first domain model

- **Status:** Accepted
- **Date:** 2026-06-25
- **Owners:** Product + Architecture

## Context

O procedură instituțională este o componentă reutilizabilă a unui traseu. Același eveniment poate declanșa mai multe proceduri, iar aceeași procedură poate apărea în evenimente diferite.

## Decision

Modelăm produsul în jurul evenimentelor de viață și al cazurilor utilizatorului, nu în jurul instituțiilor.

## Consequences

Navigația, analytics și backlogul folosesc `life_event_id`; instituțiile și procedurile rămân entități de domeniu secundare.

## Revisit triggers

- apar dovezi măsurabile că decizia blochează SLO, securitatea sau livrarea;
- contracte publice ori obligații legale schimbă premisele;
- costul operațional depășește beneficiul demonstrat;
- un înlocuitor este probat prin benchmark și plan de migrare.
