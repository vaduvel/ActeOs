# ADR-007 — OpenAPI-first contracts

- **Status:** Accepted
- **Date:** 2026-06-25
- **Owners:** Product + Architecture

## Context

Mobile, admin și backend trebuie să poată evolua în paralel și să detecteze incompatibilitățile în CI.

## Decision

OpenAPI 3.1.1 și JSON Schema sunt contractele canonice pentru request, response, events și erori.

## Consequences

Orice schimbare de contract începe în `contracts/`, generează clienți și trece compatibility checks înainte de codul consumator.

## Revisit triggers

- apar dovezi măsurabile că decizia blochează SLO, securitatea sau livrarea;
- contracte publice ori obligații legale schimbă premisele;
- costul operațional depășește beneficiul demonstrat;
- un înlocuitor este probat prin benchmark și plan de migrare.
