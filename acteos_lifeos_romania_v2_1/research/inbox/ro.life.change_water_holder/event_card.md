# Event Card — ro.life.change_water_holder (life.change_water_holder)

**Batch:** R1B-6  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să trec contractul de apă-canal pe numele meu".

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `reason` | enum | `purchase` / `rent` / `inheritance_death` |
| `has_existing_branch` | boolean | există deja branșament/racord |
| `is_owner` | boolean | solicitantul e proprietar |

## Reguli cheie

- La Timișoara, serviciul public de apă și canalizare este operat **exclusiv de Aquatim S.A.** (concesiune, HCL 95/2000) — nu există piață liberă.
- Contractul se încheie pe baza documentației depuse la Serviciul Clienți Aquatim; formular **F-01.00.06-3**.
- Dacă există deja branșament/racord, se depun documentele pentru încheierea contractului, apoi semnare.

## Canale (Timișoara)

- Operator unic: **Aquatim S.A.**, sediu str. Gheorghe Lazar nr. 11A, Timișoara; portal `https://www.aquatim.ro`, contracte online disponibile.
