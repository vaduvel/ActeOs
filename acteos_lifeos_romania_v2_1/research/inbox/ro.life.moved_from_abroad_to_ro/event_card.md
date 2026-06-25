# Event Card — ro.life.moved_from_abroad_to_ro (life.moved_from_abroad_to_ro)

**Titlu:** M-am mutat din străinătate în România  
**Batch:** B07_MOVED_FROM_ABROAD_TO_RO  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Persoana sosește din străinătate și începe să locuiască în România. Evenimentul separă cetățenia, situația de imigrare, domiciliul/reședința și rezidența fiscală; simpla sosire nu le face automat echivalente.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `citizenship_status` | enum | `romanian`, `eu_eea_swiss`, `third_country` |
| `move_date` | date | data mutării la adresa din România |
| `establishes_romanian_domicile` | boolean | declară locuința principală în România |
| `lives_at_secondary_address_days_per_month` | integer 0..31 | zile/lună la locuința secundară |
| `fiscal_status_on_arrival` | enum | `resident`, `nonresident`, `unknown` |
| `days_present_in_rolling_12m` | integer | prezență totală într-un interval de 12 luni |
| `day_183_date` | date|null | ancora termenului Z015 |
| `arrival_tax_exception` | enum | `none`, `diplomatic_consular`, `international_body_employee`, `foreign_state_employee`, `family_of_exception` |
| `residence_basis` | enum|null | `employment`, `self_sufficient`, `study`, `family`, `other` |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `establish_domicile_and_update_identity` | român + stabilește domiciliul | act de identitate/adresă în 15 zile | `claim.identity.domicile_new_id_15d` |
| `register_residence` | nu schimbă domiciliul + >15 zile/lună la adresa secundară | înscriere reședință în 15 zile | `claim.identity.residence_over_15d` |
| `submit_z015` | nerezident + ≥184 zile + fără excepție | Z015 în 30 de zile de la ziua 183 | `claim.tax_arrival.deadline_30d` |
| `prepare_igi_registration` | cetățean UE/SEE/Elveția | dosar după temei; termen de confirmat | `claim.igi.registration_timing_gap` |
| `life.residence_right_ro` | cetățean stat terț | eveniment copil separat | `claim.igi.third_country_route` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| rezidență fiscală | ANAF/SPV — formular Z015 | `verified` |
| imigrare UE/SEE | IGI — pagina după temeiul șederii | `verified_with_timing_gap` |
| domiciliu/reședință | SPCLEP competent; pilot local de confirmat | `verified_with_local_gap` |

## Note de guvernanță

- Pragul de 183 de zile declanșează chestionarul numai când este depășit; fixture-ul de frontieră folosește 184.
- Rezidența fiscală este o concluzie ANAF, nu un boolean derivat exclusiv din numărul de zile.
- Ramura cetățenilor din state terțe nu reutilizează documentele UE/SEE.
- Nicio taxă locală sau listă locală de acte nu este introdusă fără sursă Timiș/Timișoara.

===
