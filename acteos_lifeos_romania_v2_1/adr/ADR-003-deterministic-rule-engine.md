# ADR-003 — Deterministic runtime rule engine

- **Status:** Accepted
- **Date:** 2026-06-25
- **Owners:** Product + Architecture

## Context

Deciziile administrative trebuie reproduse, testate și explicate. Modelele generative pot extrage drafturi din surse, dar nu sunt o autoritate.

## Decision

Resolverul de eligibilitate, pași, acte, termene și stări de încredere este determinist și nu apelează un LLM.

## Consequences

Aceleași facts, aceeași jurisdicție, aceeași dată de referință și același ruleset produc același rezultat și același explanation trace.

## Revisit triggers

- apar dovezi măsurabile că decizia blochează SLO, securitatea sau livrarea;
- contracte publice ori obligații legale schimbă premisele;
- costul operațional depășește beneficiul demonstrat;
- un înlocuitor este probat prin benchmark și plan de migrare.
