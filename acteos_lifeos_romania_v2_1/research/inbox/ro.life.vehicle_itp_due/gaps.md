# Research gaps — ro.life.vehicle_itp_due

| gap_id | status | gap | impact | official_target | blocking |
|---|---|---|---|---|---|
| gap.itp.station_dossier | needs_confirmation | Documentele și condițiile concrete cerute de stația ITP pentru categoria exactă. | Motorul nu generează o listă universală neverificată. | RAR + stația ITP autorizată | yes |
| gap.itp.special_categories | needs_confirmation | Periodicitatea pentru categorii tehnice rare sau combinații neacoperite de faptele modelate. | Necesită clasificare RAR înainte de calcul. | RAR — RNTR 1 | yes |
| gap.itp.fees | needs_confirmation | Prețul inspecției la operatorul ales. | Nu se afișează o taxă comercială generică. | stația ITP autorizată | yes |
| gap.itp.rntr_freshness | needs_confirmation | Confirmarea că versiunea PDF RNTR 1 este ultima consolidare operativă la data publicării. | Publicarea trebuie blocată dacă documentul se modifică. | RAR / Ministerul Transporturilor | yes |

## Conflict matrix

Nu au fost identificate două surse oficiale aplicabile aceleiași situații care să impună rezultate incompatibile la data de referință.

## Geographic guard

Regulile naționale se aplică pe `ro`. Datele pilot sunt limitate la `ro.tm` / `ro.tm.timisoara`. Pentru orice alt UAT, rezultatul local este `verified_with_local_gap`; motorul nu reutilizează automat contacte, adrese, programări, taxe sau practici din Timișoara.
