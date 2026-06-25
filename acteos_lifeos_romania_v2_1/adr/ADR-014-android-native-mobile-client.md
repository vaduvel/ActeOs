# ADR-014 — Android-native (Kotlin) mobile client

- **Status:** Accepted
- **Date:** 2026-06-25
- **Owners:** Product + Architecture
- **Supersedes:** ADR-012 pentru decizia de client mobil (portalul curatorilor Next.js din ADR-012 rămâne valabil)

## Context

ADR-012 alesese Expo/React Native pentru un stack TypeScript comun. Pentru ActeOS, readiness-ul de documente local (M5) depinde de OCR și de procesare de imagine pe dispozitiv, cu acces controlat la cameră, stocare criptată și pipeline nativ. Echipa are deja competență și componente native Android (Kotlin) reutilizabile pentru OCR, iar dependențele native de OCR sunt mai mature și mai controlabile pe Android nativ decât printr-un dev-client Expo.

Decizia se ia înainte de bootstrap-ul implementării, deci nu introduce migrare de cod existent în producție.

## Decision

Clientul mobil al cetățeanului se construiește **Android-nativ în Kotlin** (Jetpack Compose), nu în Expo/React Native. Portalul curatorilor rămâne Next.js (App Router), conform ADR-012. Restul invarianților (anonymous-first, local-first documents, ruta oficială mai întâi, no LLM în decizia administrativă) rămân neschimbați.

OCR și clasificarea documentelor folosesc componente native Android, în spatele unui adapter abstract, astfel încât verdictul de autenticitate să rămână interzis și logica să rămână înlocuibilă.

## Consequences

- `apps/mobile` din pack devine un proiect Android-nativ (Kotlin/Compose), nu Expo.
- Acceptance-ul „E2E pe iOS/Android” din M4 se restrânge la Android pentru R1; iOS este out-of-scope pentru R1 și se reia printr-un ADR viitor dacă apare nevoia.
- Contractele API (OpenAPI 3.1.1) și engine-ul determinist rămân neschimbate; clientul nativ consumă același contract.
- Persistența locală criptată și ștergerea byte-urilor sursă (M5) se implementează cu primitivele native Android.
- Snapshot-urile de copy critic și a11y se adaptează la componente native echivalente WCAG 2.2 AA.

## Revisit triggers

- apare nevoia confirmată de iOS sau de paritate cross-platform;
- costul de mentenanță nativ depășește beneficiul OCR demonstrat;
- un OCR cross-platform este probat prin benchmark și plan de migrare;
- contracte publice ori obligații legale schimbă premisele.
