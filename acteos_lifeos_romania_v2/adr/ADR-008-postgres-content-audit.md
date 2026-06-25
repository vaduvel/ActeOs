# ADR-008 — PostgreSQL as operational and content system of record

- **Status:** Accepted
- **Date:** 2026-06-25
- **Owners:** Product + Architecture

## Context

Avem nevoie de tranzacții, intervale temporale, RLS, căutare și audit fără a introduce infrastructură exotică.

## Decision

PostgreSQL păstrează cazuri, reguli, claim-uri, snapshots, rulesets și audit în scheme separate.

## Consequences

Documentele binare nu sunt stocate implicit; snapshots autorizate folosesc object storage cu hash și referință în DB.

## Revisit triggers

- apar dovezi măsurabile că decizia blochează SLO, securitatea sau livrarea;
- contracte publice ori obligații legale schimbă premisele;
- costul operațional depășește beneficiul demonstrat;
- un înlocuitor este probat prin benchmark și plan de migrare.
