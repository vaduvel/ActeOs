# Event Card — ro.life.rent_out_home (life.rent_out_home)

**Titlu:** Dau o locuință în chirie  
**Batch:** B07_RENT_OUT_HOME  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul este proprietar, uzufructuar sau alt deținător legal care cedează folosința unei locuințe și obține venitul. Evenimentul compune certificatul energetic, C168, asociația și raportarea anuală.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `contract_date` | date|null | ancoră C168 și asociație |
| `contract_change_date` | date|null | ancoră modificare/încetare |
| `filing_type` | enum | `initial`, `modification`, `termination` |
| `is_personal_property_income` | boolean | domeniul procedurii C168 |
| `is_arenda` | boolean | excludere |
| `is_tourist_rooms_personal_home` | boolean | excludere |
| `is_co_owned` | boolean | bun deținut în comun |
| `is_designated_registrant` | boolean | locator desemnat |
| `is_condominium` | boolean | notificare asociație |
| `is_residential_building` | boolean | certificat energetic |
| `energy_certificate_available` | boolean | certificat disponibil |
| `advertisement_published` | boolean | obligație indicatori |
| `income_year` | integer | an venit D212 |
| `tenant_payer_type` | enum | `individual`, `legal_entity_accounting`, `unknown` |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `provide_energy_certificate_copy_before_contract` | clădire/unitate închiriată | copie înainte de contract | `claim.energy.copy_before_contract` |
| `include_energy_indicators_in_ad` | anunț publicat | indicatori energetici | `claim.energy.advertisement` |
| `submit_c168` | contract inițial/modificare eligibilă | 30 zile | `claim.c168.deadline_30d` |
| `notify_association_of_tenant` | condominiu | 10 zile de la contract | `claim.association.occupants_10d` |
| `submit_d212_for_2025_income` | venit 2025 și situație inclusă | 25 mai 2026 | `claim.d212.2025_deadline` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| C168 | ANAF — registratură, poștă sau electronic | `verified` |
| D212 | ANAF/SPV/e-guvernare/hârtie | `verified_for_income_2025` |
| asociație | notificare scrisă către președinte/administrator | `verified` |
| certificat energetic | auditor energetic/proprietar | `verified` |

## Note de guvernanță

- Termenul C168 pentru încetare rămâne `needs_confirmation`; formularul o permite, dar sursa folosită nu este transformată într-un termen inventat.
- Arenda și camerele turistice nu sunt absorbite în procedura standard C168.
- Pentru coproprietate, motorul cere locatorul desemnat.
- D212 pentru venitul 2026 nu primește termen prezumat în 2027.

===
