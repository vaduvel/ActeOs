# Event Card — ro.life.register_drone (life.register_drone)

**Titlu:** Vreau să mă înregistrez ca operator de dronă  
**Batch:** B09_REGISTER_DRONE  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul dorește conformarea pentru operarea unei drone; motorul stabilește dacă se înregistrează operatorul, excepțiile sub 250 g și autoritatea competentă.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `operator_residence_country` | country code | statul UE de reședință |
| `operator_is_non_eu_resident` | boolean | ramura vizitator |
| `first_eu_operation_country` | country code\|null | pentru nerezident |
| `operation_category` | enum | open/specific/certified |
| `uas_mass_g` | number | masa dronei |
| `uas_mass_under_250g` | boolean | prag de clasificare |
| `has_camera_or_personal_data_sensor` | boolean | excepție sub 250 g |
| `is_toy` | boolean | excepție sub 250 g |
| `uas_class_label` | enum/string | C0-C4 etc. |
| `is_certified_aircraft` | boolean | înregistrare aeronava distinctă |
| `operator_registered_in_easa_state` | boolean | evită dublarea |
| `registration_required` | boolean | rezultat clasificare |
| `operator_registration_number_received` | boolean | pași post-înregistrare |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `classify_operator_and_uas_registration` | întotdeauna | stabilește obligația corectă | `claim.drone.operator_not_aircraft_general` |
| `register_drone_operator` | obligație activă | înregistrează operatorul, nu fiecare dronă | `claim.drone.register_once_no_duplicate` |
| `register_with_residence_country_naa` | rezident UE | folosește autoritatea statului de reședință | `claim.drone.register_country_residence` |
| `register_in_first_eu_operation_country` | nerezident UE | folosește prima țară de operare | `claim.drone.non_eu_first_country` |
| `display_operator_number_on_all_drones` | număr primit | marchează toate dronele | `claim.drone.after_registration_number` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| UE/EASA | autoritatea aeronautică națională competentă | `verified` |
| România | Portal AACR UAS | `verified_with_local_gap` |
| AACR procedură 2026 | pagina oficială neaccesibilă automat | `needs_confirmation` |

## Note de guvernanță

- De regulă se înregistrează operatorul, nu fiecare dronă.
- Înregistrarea EASA este unică și nu se dublează între state.
- Excepția sub 250 g depinde de cameră/senzor și statutul de jucărie.
- Categoria specific declanșează o procedură suplimentară.

===
