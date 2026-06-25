# Event Card — ro.life.energy_performance_certificate (life.energy_performance_certificate)

**Titlu:** Vreau să obțin certificatul de performanță energetică  
**Batch:** B09_ENERGY_PERFORMANCE_CERTIFICATE  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul are nevoie de un certificat energetic pentru vânzare, închiriere, recepția unei clădiri noi sau verificarea valabilității.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `purpose_class` | enum | sale/rent/new_building_reception/information/other |
| `is_exempt_building_type` | boolean | aplicabilitatea excepțiilor legale |
| `has_valid_certificate` | boolean | certificat valabil |
| `has_certificate` | boolean | există înscrisul |
| `certificate_age_years_gte_10` | boolean | prag valabilitate |
| `major_renovation_changed_consumption` | boolean | excepție de la valabilitate |
| `unique_registration_code_present` | boolean | cod unic minister |
| `contract_concluded` | boolean | stadiul tranzacției |
| `needs_new_certificate` | boolean | este necesară emiterea |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `determine_certificate_applicability` | întotdeauna | verifică excepțiile | `claim.energy.auditor_issues` |
| `select_attested_energy_auditor` | certificat necesar | alege auditor atestat | `claim.energy.auditor_list` |
| `obtain_energy_certificate` | lipsește/expirat/renovare majoră | obține certificat cu cod unic | `claim.energy.unique_code_nullity` |
| `give_copy_to_potential_buyer_before_contract` | vânzare înainte de contract | predă copia | `claim.energy.copy_before_sale_rent` |
| `present_certificate_at_reception` | clădire nouă | prezintă la recepție | `claim.energy.new_building_reception` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| național | auditor energetic atestat | `verified` |
| registru auditori | pagina autorității centrale competente | `verified` |
| organ fiscal competent | depunere copie la înregistrarea contractului | `verified_with_local_gap` |

## Note de guvernanță

- Motorul nu inventează onorariul auditorului.
- Excepțiile de la aplicare sunt facts explicite, nu presupuneri.
- Lipsa codului unic blochează utilizarea certificatului.

===
