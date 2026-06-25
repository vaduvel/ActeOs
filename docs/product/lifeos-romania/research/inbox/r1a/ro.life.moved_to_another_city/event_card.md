# Event Card — ro.life.moved_to_another_city (life.moved_to_another_city)

**Batch:** R1A-7 (orchestrare)  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„M-am mutat în alt oraș / altă localitate".

> Eveniment **compozit**: nu introduce reguli noi de fond, ci orchestrează evenimente atomice deja cercetate, plus obligațiile specifice trecerii între UAT-uri (taxe locale auto la noul domiciliu).

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `move_date` | date | data mutării |
| `crosses_uat` | boolean | schimbare de localitate/UAT |
| `owns_vehicle` | boolean | deține autovehicul |
| `is_utility_holder` | boolean | titular contracte utilități |
| `has_children_in_school` | boolean | copii înscriși la școală/grădiniță |

## Evenimente declanșate (copii)

- `life.moved_home` — schimbarea adresei din CI (15 zile) — întotdeauna.
- `life.vehicle_change_address` — actualizare talon — dacă deține vehicul.
- `life.local_tax_declaration` (auto) — declarare la noul organ fiscal — dacă schimbă UAT și deține vehicul.
- `life.change_electricity_holder` / `life.change_gas_holder` / `life.change_water_holder` — dacă e titular.
- Înscriere școală/grădiniță la noua adresă — dacă are copii (R1B).

## Note

Obligațiile de fond (termene, documente) sunt definite în evenimentele copil; aici doar se determină ce evenimente se aprind.
