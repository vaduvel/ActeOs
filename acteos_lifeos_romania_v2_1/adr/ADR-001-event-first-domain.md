# ADR-001 — Event-first domain model

- **Status:** Superseded for public discovery by ADR-013
- **Date:** 2026-06-25
- **Owners:** Product + Architecture

## Original decision

Modelarea inițială folosea evenimentul de viață ca intrare principală și context de compoziție.

## Current interpretation

Event Atlas rămâne context intern pentru bundle-uri, relații și recomandări. Public discovery folosește `intent_type_id` conform ADR-013. Nicio migrare nu șterge event context-ul istoric.
