# Research gaps — ro.life.change_name_admin_court

| gap_id | status | gap | impact | official_target | blocking |
|---|---|---|---|---|---|
| gap.name.timis_current | needs_confirmation | Pagina curentă, ne-arhivată, pentru programare, canal și documente în Timișoara. | Procedura locală nu poate fi publicată din pagina arhivată singură. | Direcția de Evidență a Persoanelor Timișoara | yes |
| gap.name.local_fee | needs_confirmation | Regimul actual al taxelor și costul publicării în Monitorul Oficial. | Nu se afișează „gratuit” pe baza paginii arhivate. | DEP Timișoara + Monitorul Oficial | yes |
| gap.name.publication_exceptions | needs_confirmation | Excepțiile exacte de la publicarea extrasului pentru cazul individual. | Motorul nu omite publicarea fără temei verificat. | Legea nr. 119/1996 / DEP | yes |
| gap.name.serious_ground_assessment | needs_confirmation | Evaluarea temeiniciei motivului și a dovezilor individuale. | Nu se garantează admiterea. | serviciul județean de evidență a persoanelor | yes |

## Conflict matrix

| conflict_id | source_a | source_b | conflict | treatment |
|---|---|---|---|---|
| conflict.name.sla | `claim.name.disposition_30` | `claim.name.local_60_conflict` | Legea consolidată: 30 zile de la primirea documentelor la serviciul județean; pagina locală arhivată: 60 zile. | Se aplică termenul normativ ca regulă națională, dar nu se promite un SLA local până la clarificarea oficială; rezultatul local rămâne `conflicting`. |

## Geographic guard

Regulile naționale se aplică pe `ro`. Datele pilot sunt limitate la `ro.tm` / `ro.tm.timisoara`. Pentru orice alt UAT, rezultatul local este `verified_with_local_gap`; motorul nu reutilizează automat contacte, adrese, programări, taxe sau practici din Timișoara.
