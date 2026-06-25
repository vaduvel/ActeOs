# Prompturi pe faze — LifeOS România

Fiecare fază: livrabile clare, teste verzi, raport scurt. Nu se trece la faza următoare cu teste roșii.

## Faza 0 — Inventar și aliniere

Citește întregul workbook și codul existent (`services/api`, `packages/rule-engine`, `packages/contracts`). Confirmă ce se reutilizează. Livrabil: `IMPLEMENTATION_STATUS.md` cu maparea workbook → cod.

## Faza 1 — Contracte eveniment

Definește schemele JSON pentru `LifeEvent`, `ProcedureRef`, cererea și răspunsul orchestratorului și `source-registry.schema.json`. Validatoare + teste de contract. Nicio logică de business încă.

## Faza 2 — Orchestrator determinist

Implementează `plan_event` conform `05_RULE_ENGINE_SPEC.md` partea B: aplicabilitate tri-valued, graf de dependențe, detecție de cicluri, sortare topologică stabilă, agregare de încredere, `event_plan_hash`. Teste: golden hash, cicluri respinse, `unknown → needs_confirmation`.

## Faza 3 — Catalog R1

Codifică evenimentele 🔥 din `06_LIFE_EVENT_CATALOG.md` ca date (nu cod). Fixture-uri de plan pozitive și negative pentru E1–E5 și schelet pentru restul. Legături la `19_SOURCE_REGISTRY.json`. Conținutul nelegat rămâne `REQUIRES_HUMAN_CURATION`.

## Faza 4 — API și persistență

Endpoint-uri: `POST /life-events/classify` (assist-only), `POST /life-events/plan`, `GET /life-events/{id}`, plus reutilizarea rutelor de procedură existente pentru noduri. Migrări PostgreSQL pentru tabelele noi. Idempotență și audit ca în API-ul curent.

## Faza 5 — Clasificator NL (assist-only)

Maparea „Ce s-a întâmplat?" → eveniment din catalog cu întrebări de dezambiguizare. Fără generare de obligații. Evaluare separată cu set de fraze reale; prag de încredere; fallback la căutare în catalog.

## Faza 6 — Front-end fluxuri

Ecranul unic de intrare, harta evenimentului (deblocat/urmează/condițional), ecranul de procedură (standardul de 5 întrebări), stările de încredere, accesibilitate.

## Faza 7 — Întărire și analiză de impact

Impact analysis la publicare (compară `event_plan_hash` și grafuri), fail-closed pe stale, observabilitate, runbook de deploy. Raport final de validare.
