# Event Card — ro.life.return_to_romania (life.return_to_romania)

**Titlu:** Mă întorc definitiv în România  
**Batch:** B07_RETURN_TO_ROMANIA  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Cetățeanul român sau persoana care a locuit în străinătate revine cu intenție de stabilire. Evenimentul este mai îngust decât simpla sosire și tratează explicit revenirea de la statut CRDS.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `is_romanian_citizen` | boolean | ramura de identitate românească |
| `prior_domicile_status` | enum | `domicile_abroad`, `domicile_ro`, `unknown` |
| `restores_domicile_in_ro` | boolean | restabilește domiciliul principal |
| `move_date` | date | ancoră act identitate/reședință |
| `lives_at_secondary_address_days_per_month` | integer 0..31 | dacă nu restabilește domiciliul |
| `fiscal_status_on_arrival` | enum | `resident`, `nonresident`, `unknown` |
| `days_present_in_rolling_12m` | integer | prezență în România |
| `day_183_date` | date|null | ancoră Z015 |
| `arrival_tax_exception` | enum | excepțiile ANAF |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `replace_passport_for_domicile_ro_status` | român cu domiciliu anterior în străinătate + restabilește domiciliul | pașaport corespunzător statutului | `claim.passport.status_change` |
| `establish_domicile_and_update_identity` | restabilește domiciliul | act identitate în 15 zile | `claim.identity.domicile_new_id_15d` |
| `register_residence` | nu schimbă domiciliul + >15 zile/lună | reședință în 15 zile | `claim.identity.residence_over_15d` |
| `submit_z015` | nerezident + ≥184 zile + fără excepție | Z015 în 30 zile | `claim.tax_arrival.deadline_30d` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| identitate | SPCLEP competent | `verified_with_local_gap` |
| pașaport | DGP / serviciu pașapoarte / consulat | `verified` |
| rezidență fiscală | ANAF/SPV Z015 | `verified` |

## Note de guvernanță

- `return_to_romania` nu înlocuiește evenimentul general IGI pentru cetățeni străini.
- Statutul CRDS este fapt separat; nu se presupune din durata șederii în străinătate.
- Revenirea declarată «definitivă» nu decide singură rezidența fiscală.
- Regulile istorice necesită ruleset după data de referință.

===
