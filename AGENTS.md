# AGENTS.md — instrucțiuni de execuție pentru agenții de cod

Acest repo se construiește după pachetul canonic din [`docs/product/waze-birocratie/`](./docs/product/waze-birocratie/).

## Ordine de citire obligatorie

Începe întotdeauna cu `docs/product/waze-birocratie/CODEX_START_HERE.md`, apoi `15_CODEX_MASTER_PROMPT.md` și `16_PHASE_PROMPTS.md`.

## Reguli care nu se negociază

- Regulile deterministe decid traseul; un LLM NU decide cerințe/eligibilitate/termene/precedență legală la runtime.
- Fiecare claim de producție are dovadă + aprobare umană.
- Fără `eval`, SQL prin concatenare, deserializare nesigură.
- Fără secrete/URL-uri de producție hardcodate.
- Fără date demo în producție.
- Documentele utilizatorului rămân locale implicit.
- Nicio fotografie nu dovedește autenticitatea unui act.

## Precedență la conflicte

1. Manifest (siguranță/neutralitate)
2. Contracte mașină (`contracts/*.json`, OpenAPI, constrângeri SQL)
3. Specificația motorului de reguli
4. PRD/UX
5. Detaliul din backlog

Conflictele se rezolvă printr-un ADR în `docs/adr/`, alegând comportamentul cel mai sigur. Nu reinterpreta tăcut.

## Mod de lucru

Execută fazele P0–P10 în ordine. O fază nu e completă dacă exit gate-ul e roșu. Actualizează `IMPLEMENTATION_STATUS.md` la fiecare fază.
