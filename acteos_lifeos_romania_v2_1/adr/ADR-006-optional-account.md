# ADR-006 — Optional account and progressive persistence

- **Status:** Accepted
- **Date:** 2026-06-25
- **Owners:** Product + Architecture

## Context

Birocrația este deja o barieră; autentificarea nu trebuie să fie prima.

## Decision

Căutarea, clasificarea și un traseu local de bază funcționează fără cont. Contul este cerut numai pentru sincronizare, gospodărie și notificări cross-device.

## Consequences

Datele anonime au TTL scurt; migrarea către cont cere consimțământ și nu dublează cazurile.

## Revisit triggers

- apar dovezi măsurabile că decizia blochează SLO, securitatea sau livrarea;
- contracte publice ori obligații legale schimbă premisele;
- costul operațional depășește beneficiul demonstrat;
- un înlocuitor este probat prin benchmark și plan de migrare.
