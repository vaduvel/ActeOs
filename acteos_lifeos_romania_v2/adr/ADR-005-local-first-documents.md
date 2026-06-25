# ADR-005 — Local-first document processing

- **Status:** Accepted
- **Date:** 2026-06-25
- **Owners:** Product + Architecture

## Context

Actele conțin PII cu risc ridicat. Uploadul implicit ar crește suprafața de atac și ar încălca principiul minimizării.

## Decision

Documentele utilizatorului rămân pe dispozitiv implicit; backendul primește metadate și rezultate minimizate.

## Consequences

Cloud processing este opt-in, cu scop, retenție, consimțământ și ștergere explicite. Autenticitatea nu este dedusă numai din imagine.

## Revisit triggers

- apar dovezi măsurabile că decizia blochează SLO, securitatea sau livrarea;
- contracte publice ori obligații legale schimbă premisele;
- costul operațional depășește beneficiul demonstrat;
- un înlocuitor este probat prin benchmark și plan de migrare.
