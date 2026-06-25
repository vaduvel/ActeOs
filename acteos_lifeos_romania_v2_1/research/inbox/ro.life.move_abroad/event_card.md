# Event Card — ro.life.move_abroad (life.move_abroad)

**Titlu:** Mă mut în străinătate  
**Batch:** B07_MOVE_ABROAD  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Persoana pleacă din România pentru o ședere lungă sau definitivă. Motorul separă plecarea fizică, rezidența fiscală, statutul de domiciliu CRDS și regulile statului de destinație.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `departure_date` | date | data plecării |
| `expected_days_abroad_rolling_12m` | integer | zile estimate în străinătate |
| `fiscal_status_before_departure` | enum | `resident`, `nonresident`, `unknown` |
| `had_z015_obligation` | boolean | nerezident care a avut obligație la sosire |
| `romanian_state_employee_abroad` | boolean | excepție Z017 |
| `changes_domicile_status_to_crds` | boolean | schimbă statutul domiciliului în străinătate |
| `destination_country` | ISO 3166-1 alpha-2|null | statul de destinație |
| `foreign_tax_residence_certificate_available` | boolean|null | document disponibil |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `submit_z017` | rezident sau fost obligat Z015 + ≥184 zile + fără excepție | Z017 cu 30 zile înainte | `claim.tax_departure.deadline_30_before` |
| `replace_passport_for_crds_status` | schimbă statutul în CRDS | anulare și pașaport nou | `claim.passport.status_change` |
| `verify_destination_entry_and_residence_rules` | orice destinație | confirmare la MAE/statul de destinație | `claim.passport.destination_rules` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| rezidență fiscală | ANAF/SPV — Z017 | `verified` |
| pașaport CRDS | serviciu pașapoarte / consulat | `verified` |
| stat de destinație | MAE — condiții de călătorie / misiune diplomatică | `verified_with_country_gap` |

## Note de guvernanță

- 184 este prima valoare care satisface formularea «depășește 183». 
- Z017 nu produce automat verdictul de nerezidență fiscală.
- Condițiile statului de destinație rămân `needs_confirmation` până la selectarea țării și a sursei oficiale locale.
- Schimbarea CRDS este o alegere/statut distinct de simpla plecare.

===
