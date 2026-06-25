# Event Card — ro.life.documents_stolen_bundle (life.documents_stolen_bundle)

**Batch:** R1A-8 (orchestrare)  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Mi-au fost furate mai multe acte (portofel cu buletin, permis, talon etc.)".

> Eveniment **compozit**: o singură sesizare la poliție acoperă întregul pachet furat, apoi se aprinde câte un eveniment de înlocuire pentru fiecare document.

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `theft_date` | date | data furtului |
| `lost_id_card` | boolean | buletin/CI |
| `lost_passport` | boolean | pașaport |
| `lost_driving_license` | boolean | permis de conducere |
| `lost_vehicle_registration` | boolean | certificat înmatriculare (talon) |

## Reguli cheie

- **O singură sesizare la poliție** acoperă tot pachetul (nu câte una per act).
- Se declanșează `life.id_card_lost_stolen` (varianta furt) când e cazul.
- Se aprind evenimente de înlocuire pentru pașaport / permis / talon, după caz.

## Note

Regulile de fond (termene, documente, null-by-law) sunt definite în evenimentele copil.
