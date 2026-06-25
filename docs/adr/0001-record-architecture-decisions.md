# ADR-0001: Înregistrăm deciziile de arhitectură

- **Status:** acceptat
- **Data:** 2026-06-25

## Context

Workbook-ul (`20_CANONICAL_DECISIONS.md`) definește decizii canonice implicite (ADR-001…ADR-015). Avem nevoie de un proces ușor de înregistrare a deciziilor și a deviațiilor.

## Decizie

Folosim ADR-uri în Markdown în `docs/adr/`, numerotate secvențial, pornind de la `0000-adr-template.md`. Orice deviație de la baseline-ul din workbook sau orice conflict între documente produce un ADR nou.

## Consecințe

Istoric trasabil al deciziilor. ADR-urile canonice din workbook vor fi materializate ca fișiere formale pe măsura implementării fazelor.
