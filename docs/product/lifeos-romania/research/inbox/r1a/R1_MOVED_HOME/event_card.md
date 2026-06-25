# Event Card — ro.life.moved_home (life.moved)

**Batch:** R1A-1  
**Status:** research_inbox (neaprobat; NU în producție până la review independent)  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at surse:** 2026-06-25

## Declanșator

„M-am mutat" / „mi-am schimbat adresa". Distinge **domiciliu** (permanent) de **reședință** (flotant). Mutarea în alt oraș/județ = `ro.life.moved_to_another_city` (event înrudit, aceleași obligații + transfer dosar fiscal).

## Fapte cerute (typed facts)

| fact | tip | valori |
|---|---|---|
| `change_type` | enum | `domiciliu`, `resedinta` |
| `id_card_type` | enum | `buletin`, `ci_simpla`, `cei` |
| `new_address_relation` | enum | `owner`, `host_consent` |
| `has_minor_children_moving` | boolean | |
| `minor_children_under_14` | boolean | |
| `owns_vehicle` | boolean | |
| `days_since_move` | number | |
| `move_date` | date | ancoră termen |

## Obligații (sub-graf)

1. **update_identity_card** — act de identitate nou la schimbare domiciliu. **Critic, 15 zile** (CI simplă/buletin). Excepție CEI: fără act nou.
2. **update_vehicle_registration** — dacă `owns_vehicle` și `change_type=domiciliu`. Termen `needs_confirmation`.
3. **register_local_taxes** — declarare/transfer la DITL/DFMT (proprietate/vehicul). `needs_confirmation`.
4. **register_residence_visa** — viză de reședință (flotant) dacă `change_type=resedinta`. `needs_confirmation`.

## Canale oficiale (Timișoara)

- DEP Primăria Timișoara, program L–V 08:00–16:00; programare CEI prin `https://hub.mai.gov.ro/`.
- Dovada adresei: `https://www.primariatm.ro/dovada-adresa-domiciliu`.

## Note de guvernanță

Doar `update_identity_card` are claim-uri **verified** suficiente pentru regulă critică. Restul rămâne `needs_confirmation` până la locator oficial (vezi `gaps.md`).
