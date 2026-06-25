# ADR-004 — Evidence-gated production rules

- **Status:** Accepted
- **Date:** 2026-06-25
- **Owners:** Product + Architecture

## Context

O pagină oficială poate fi ambiguă sau se poate schimba. Proveniența trebuie păstrată până la pasul afișat utilizatorului.

## Decision

Nicio regulă critică nu este publicabilă fără claim atomic, snapshot, locator, autoritate, interval temporal și review uman.

## Consequences

CI și serviciul de publicare blochează reguli fără dovezi; research-ul intră numai în inbox.

## Revisit triggers

- apar dovezi măsurabile că decizia blochează SLO, securitatea sau livrarea;
- contracte publice ori obligații legale schimbă premisele;
- costul operațional depășește beneficiul demonstrat;
- un înlocuitor este probat prin benchmark și plan de migrare.
