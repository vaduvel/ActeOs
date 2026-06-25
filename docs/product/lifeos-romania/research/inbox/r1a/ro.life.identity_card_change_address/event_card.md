# Event Card — ro.life.identity_card_change_address (life.id_card_change_address)

**Batch:** R1A-2  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Mi-am schimbat adresa și trebuie să actualizez actul de identitate".

> Acest eveniment acoperă strict actualizarea actului de identitate la schimbarea adresei. Mutarea completă (vehicul, utilități, fiscal, medic de familie) este acoperită de `ro.life.moved_home`.

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `id_card_type` | enum | `buletin`, `ci_simpla`, `cei` |
| `change_type` | enum | `domiciliu`, `resedinta` |
| `new_address_relation` | enum | `owner`, `host_consent`, `family` |
| `move_date` | date | data mutării |

## Reguli cheie (verificate)

- Schimbare **domiciliu** → obligație act nou în **15 zile** (OUG 97/2005, art. 19 alin. 1 lit. b).
- **CEI**: schimbarea adresei NU impune emiterea unui nou suport fizic (adresa este gestionată electronic) — suprascrie regula de 15 zile pentru actul fizic.
- Dovada adresei obligatorie; dacă nu ești proprietar → declarația găzduitorului.

## Canale (Timișoara)

`https://hub.mai.gov.ro/cei/programari/create?judet=TM`; DEP Timișoara L–V 08:00–16:00.
