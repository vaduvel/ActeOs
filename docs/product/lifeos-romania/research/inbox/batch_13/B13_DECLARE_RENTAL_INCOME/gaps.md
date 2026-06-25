# Research gaps — B13_DECLARE_RENTAL_INCOME

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Termenul material de înregistrare pentru contract nou/modificat/încetat | `needs_confirmation` | numărul de zile și data de la care curge | Codul fiscal consolidat + OPANAF nr. 161/2025 |
| 2 | Tratamentul fiscal în funcție de tipul chiriașului | `needs_confirmation` | reținerea la sursă, venitul net și obligațiile declarative | Codul fiscal + ghid ANAF 2026 |
| 3 | CASS și pragurile aplicabile veniturilor din chirii | `needs_confirmation` | plafoanele și cumulul veniturilor pentru anul fiscal | Codul fiscal + D212 2026 |
| 4 | Situația coproprietarilor și locatorului desemnat | `needs_confirmation` | cine depune și cum se declară cotele | instrucțiunile C168 / ANAF |
| 5 | Corectarea contractelor înregistrate în ani anteriori | `needs_confirmation` | versiunea formularului și identificatorul cererii | ANAF C168 |

## Politica truth-guard

Motorul verifică instrumentul C168 și atașamentul obligatoriu, dar nu produce termene ori calcule fiscale din memorie.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale`, `expired` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
