# Research gaps — ro.life.road_accident_admin

| gap_id | status | gap | impact | official_target | blocking |
|---|---|---|---|---|---|
| gap.acc.timis_material_office | needs_confirmation | Adresa, programul și competența exactă a structurii de accidente ușoare din Timiș pentru locul concret. | Nu se trimite utilizatorul la un sediu neverificat. | IPJ Timiș — Poliția Rutieră | yes |
| gap.acc.insurer_documents | needs_confirmation | Lista de documente cerută de asigurătorul RCA/CASCO pentru dosarul concret. | Dosarul de daună nu poate fi validat generic. | asigurătorul din poliță | yes |
| gap.acc.cross_border | needs_confirmation | Procedura pentru accident în afara României sau cu vehicul înmatriculat în alt stat. | Necesită reguli Carte Verde/BAAR și jurisdicția locului. | BAAR + autoritatea statului accidentului | yes |
| gap.acc.injury_legal | needs_confirmation | Pașii juridici individuali în accidente cu victime, alcool sau cercetare penală. | Motorul se limitează la obligațiile administrative imediate. | Poliția Română / avocat | yes |

## Conflict matrix

Nu au fost identificate două surse oficiale aplicabile aceleiași situații care să impună rezultate incompatibile la data de referință.

## Geographic guard

Regulile naționale se aplică pe `ro`. Datele pilot sunt limitate la `ro.tm` / `ro.tm.timisoara`. Pentru orice alt UAT, rezultatul local este `verified_with_local_gap`; motorul nu reutilizează automat contacte, adrese, programări, taxe sau practici din Timișoara.
