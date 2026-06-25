# Gaps — ro.life.baptism

**Accessed at:** 2026-06-25  
**Status:** `research_candidate_not_production_published`

> Un gap nu este completat prin presupunere. Până la confirmare, motorul trebuie să emită `needs_confirmation`, `conflicting` sau să blocheze publicarea regulii critice.

## Gaps rămase

| id | severitate | descriere | rezolvare necesară |
|---|---|---|---|
| `gap.parish_checklists` | `critical` | Actele, condițiile pentru nași/sponsori, cateheza și calendarul nu sunt uniforme național. | Confirmare la unitatea locală competentă. |
| `gap.parental_authority_conflicts` | `critical` | Legea cultelor nu oferă în pagina cercetată un algoritm complet pentru conflicte între reprezentanți privind botezul minorului. | Nu decide automat; solicită clarificare juridică și a cultului. |
| `gap.certificate_form` | `operational` | Existența, forma și procedura de duplicat a certificatului religios diferă între culte/unități. | Research per cult și parohie. |
| `gap.other_cults_local` | `critical` | Pilotul are numai canale eparhiale ortodox și romano-catolic pentru Timișoara. | Extindere per cult și unitate locală. |

## Conflicte oficiale

Nu a fost identificat un conflict oficial explicit în sursele folosite pentru acest seed. Aceasta nu înseamnă că nu există alte conflicte nepublicate sau încă neidentificate.

## Captură și aprobare necesare

- `snapshot_status`: `pending_immutable_capture` pentru toate sursele.
- Citatele trebuie reconfirmate pe snapshot/PDF și hash-uite SHA-256 înainte de activare.
- Un curator trebuie să aprobe separat fiecare claim critic și fiecare regulă derivată.
- Datele locale din afara pilotului Timiș/Timișoara rămân `verified_with_local_gap`.
