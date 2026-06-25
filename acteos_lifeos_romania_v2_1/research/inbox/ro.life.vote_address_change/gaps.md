# Research gaps — ro.life.vote_address_change

| gap_id | status | gap | impact | official_target | blocking |
|---|---|---|---|---|---|
| gap.vote.current_election_calendar | needs_confirmation | Data și actele oficiale ale următorului scrutin concret. | Motorul nu presupune existența sau data unei alegeri. | AEP / Monitorul Oficial | yes |
| gap.vote.european_referendum | needs_confirmation | Regulile de adresă și liste pentru alegeri europene și referendum. | Aceste ramuri nu extrapolează din alte scrutine. | Portal Legislativ / AEP | yes |
| gap.vote.exact_6_month_calc | needs_confirmation | Interpretarea exactă a pragului „mai mare de 6 luni” la data concretă. | Cazul de frontieră nu este decis automat. | AEP / autoritatea electorală competentă | yes |
| gap.vote.other_uat_residence | verified_with_local_gap | Serviciul de stabilire a reședinței pentru alt UAT. | Nu se reutilizează termenul Timișoara. | serviciul local de evidență a persoanelor | yes |

## Conflict matrix

Nu au fost identificate două surse oficiale aplicabile aceleiași situații care să impună rezultate incompatibile la data de referință.

## Geographic guard

Regulile naționale se aplică pe `ro`. Datele pilot sunt limitate la `ro.tm` / `ro.tm.timisoara`. Pentru orice alt UAT, rezultatul local este `verified_with_local_gap`; motorul nu reutilizează automat contacte, adrese, programări, taxe sau practici din Timișoara.
