# Event Card — ro.life.identity_card_lost / identity_card_stolen (life.id_card_lost_stolen)

**Batch:** R1A-4  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Mi-am pierdut / mi-a fost furat / s-a distrus / s-a deteriorat actul de identitate".

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `id_card_type` | enum | `buletin`, `ci_simpla`, `cei` |
| `loss_type` | enum | `lost`, `stolen`, `destroyed`, `deteriorated` |
| `event_date` | date | data pierderii/furtului/distrugerii |
| `facial_image_in_rnep` | boolean | imaginea facială există deja în R.N.E.P. |
| `new_address_relation` | enum | `owner`, `host_consent`, `family` |

## Reguli cheie (verificate)

- Solicitarea unui nou act în **15 zile** de la pierdere/furt (OUG 97/2005; surse SPCLEP).
- **Furt** → reclamat la poliție în **24 de ore** de la constatare.
- **Pierdere/distrugere** → se anunță direct la SPCLEP (fără poliție).
- Actele declarate pierdute/furate/distruse sunt **nule de drept**.
- Dacă actul declarat e găsit ulterior → predat în **48 de ore** la SPCLEP unde s-a declarat.
- Dacă imaginea facială NU e în R.N.E.P. → un document oficial cu fotografie recentă (permis/pașaport).

## Conflict deschis

Cuantum sancțiune: surse oficiale divergente (40–80 lei vs 500–1000 lei). Pentru pierdere/furt, surse SPCLEP citează 500–1000 lei. Status `conflicting`; nu se afișează un cuantum unic.

## Canale (Timișoara)

`https://hub.mai.gov.ro/cei/programari/create?judet=TM`; pentru furt, secția de poliție competentă.
