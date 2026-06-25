# Event Card — ro.life.lost_all_documents (life.lost_all_documents)

**Batch:** R1A-9 (orchestrare)  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Mi-am pierdut toate actele".

> Eveniment **compozit** (pierdere, nu furt). Ordinea cheie: **întâi actul de identitate** (CI), pentru că e necesar la înlocuirea celorlalte documente.

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `loss_date` | date | data pierderii |
| `lost_id_card` | boolean | CI |
| `lost_passport` | boolean | pașaport |
| `lost_driving_license` | boolean | permis |
| `lost_vehicle_registration` | boolean | talon |

## Reguli cheie

- **Pierdere, nu furt** → nu este obligatorie sesizarea la poliție (diferență față de `documents_stolen_bundle`).
- **CI se reface prima**; restul documentelor au nevoie de CI valid.
- Se aprind evenimente de înlocuire pentru fiecare document pierdut.

## Note

Regulile de fond traiesc în evenimentele copil (`id_card_lost_stolen` varianta pierdere etc.).
