# ADR-012 — Expo mobile and Next.js curator portal

- **Status:** Accepted
- **Date:** 2026-06-25
- **Owners:** Product + Architecture

## Context

Un stack TypeScript comun reduce divergența modelelor, iar Expo accelerează distribuția și capabilitățile native controlate.

## Decision

Clientul mobil folosește Expo/React Native, iar portalul curatorilor folosește Next.js App Router.

## Consequences

Modulele native și upgrade-urile majore cer testare EAS/dev-client; aplicația nu depinde de Expo Go în producție.

## Revisit triggers

- apar dovezi măsurabile că decizia blochează SLO, securitatea sau livrarea;
- contracte publice ori obligații legale schimbă premisele;
- costul operațional depășește beneficiul demonstrat;
- un înlocuitor este probat prin benchmark și plan de migrare.
