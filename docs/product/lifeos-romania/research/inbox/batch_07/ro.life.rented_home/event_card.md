# Event Card — ro.life.rented_home (life.rented_home)

**Titlu:** Am închiriat o locuință  
**Batch:** B07_RENTED_HOME  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul este chiriaș/locatar și a dobândit folosința unei locuințe. Evenimentul nu îl confundă cu locatorul care obține venitul și înregistrează fiscal contractul.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `contract_date` | date|null | data contractului |
| `move_date` | date | data mutării efective |
| `is_residential_building` | boolean | intră în domeniul certificatului energetic |
| `energy_certificate_copy_received_before_contract` | boolean | copie primită anterior contractului |
| `changes_domicile` | boolean | locuința devine principală |
| `days_per_month_at_secondary_address` | integer 0..31 | pentru reședință |
| `has_address_proof` | boolean|null | dovada legală a adresei |
| `is_condominium` | boolean | există asociație/condominiu |
| `tenant_is_legal_holder_locator` | boolean | rol juridic dual excepțional |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `request_energy_certificate_copy` | clădire închiriată + copia lipsește | solicitare către proprietar | `claim.energy.copy_before_contract` |
| `update_identity_for_new_domicile` | schimbă domiciliul | 15 zile de la mutare | `claim.identity.domicile_new_id_15d` |
| `register_residence` | adresă secundară >15 zile/lună | 15 zile de la mutare | `claim.identity.residence_over_15d` |
| `submit_c168` | chiriaș obișnuit | exclus; obligația locatorului | `claim.rented.c168_income_earner` |
| `association_notice` | condominiu | informare: obligația principală revine proprietarului | `claim.association.occupants_10d` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| identitate/reședință | SPCLEP competent | `verified_with_local_gap` |
| certificat energetic | proprietar/locator | `verified` |
| C168 | ANAF — nu este pas al chiriașului obișnuit | `verified` |

## Note de guvernanță

- Contractul de închiriere nu este tratat automat ca dovadă suficientă a adresei; se aplică formele legale de dovadă și, după caz, acordul găzduitorului.
- Chiriașul nu primește fals obligația C168.
- Relația internă privind întreținerea nu schimbă creditorul legal al asociației: proprietarul rămâne obligat.
- Valabilitatea unui contract verbal nu este decisă de acest eveniment.

===
