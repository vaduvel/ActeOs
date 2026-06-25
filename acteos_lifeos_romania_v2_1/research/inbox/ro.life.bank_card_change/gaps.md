# Gaps — ro.life.bank_card_change

**Accessed at:** 2026-06-25  
**Status:** `research_candidate_not_production_published`

> Un gap nu este completat prin presupunere. Până la confirmare, motorul trebuie să emită `needs_confirmation`, `conflicting` sau să blocheze publicarea regulii critice.

## Gaps rămase

| id | severitate | descriere | rezolvare necesară |
|---|---|---|---|
| `gap.provider_matrix` | `critical` | Nu există procedură universală de reemitere; seed-ul acoperă parțial ING, BCR și CEC. | Research și snapshot per emitent/produs. |
| `gap.fees_delivery` | `critical` | Taxele și termenele de livrare sunt comerciale și dinamice. | Captură tarif și condiții înainte de afișare. |
| `gap.card_types` | `operational` | Cardurile virtuale, suplimentare și de credit pot avea ramuri distincte. | Extindere facts/card_form și reguli pe tip de card. |

## Conflicte oficiale

Nu a fost identificat un conflict oficial explicit în sursele folosite pentru acest seed. Aceasta nu înseamnă că nu există alte conflicte nepublicate sau încă neidentificate.

## Captură și aprobare necesare

- `snapshot_status`: `pending_immutable_capture` pentru toate sursele.
- Citatele trebuie reconfirmate pe snapshot/PDF și hash-uite SHA-256 înainte de activare.
- Un curator trebuie să aprobe separat fiecare claim critic și fiecare regulă derivată.
- Datele locale din afara pilotului Timiș/Timișoara rămân `verified_with_local_gap`.
