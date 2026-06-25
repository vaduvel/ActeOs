# Research gaps — ro.life.administrative_petition

| gap_id | status | gap | impact | official_target | blocking |
|---|---|---|---|---|---|
| gap.pet.authority_mapping | needs_confirmation | Harta completă și actuală a competențelor și canalelor oficiale pentru fiecare autoritate. | Motorul nu poate alege automat instituția din text liber fără verificare. | autoritatea publică competentă | yes |
| gap.pet.special_procedures | needs_confirmation | Identificarea procedurilor speciale care exclud sau completează OG nr. 27/2002. | O contestație ori plângere cu termen special nu trebuie tratată ca petiție generică. | autoritatea competentă / Portal Legislativ | yes |
| gap.pet.timis_email_typo | conflicting | Pagina Prefecturii Timiș afișează în nota GDPR o adresă aparent eronată; nu este folosită ca canal. | Trimiterea prin e-mail rămâne blocată până la confirmarea contactului oficial curent. | Instituția Prefectului — Județul Timiș | yes |
| gap.pet.remedies | needs_confirmation | Calea juridică individuală după depășirea termenului sau un răspuns nelegal. | Nu se generează automat acțiune în instanță ori plângere disciplinară. | autoritatea emitentă / instanța competentă | yes |

## Conflict matrix

Nu au fost identificate două surse oficiale aplicabile aceleiași situații care să impună rezultate incompatibile la data de referință.

## Geographic guard

Regulile naționale se aplică pe `ro`. Datele pilot sunt limitate la `ro.tm` / `ro.tm.timisoara`. Pentru orice alt UAT, rezultatul local este `verified_with_local_gap`; motorul nu reutilizează automat contacte, adrese, programări, taxe sau practici din Timișoara.
