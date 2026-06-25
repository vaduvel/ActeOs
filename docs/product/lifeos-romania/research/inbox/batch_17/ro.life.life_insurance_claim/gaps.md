# Gaps — ro.life.life_insurance_claim

**Accessed at:** 2026-06-25  
**Status:** `research_candidate_not_production_published`

> Un gap nu este completat prin presupunere. Până la confirmare, motorul trebuie să emită `needs_confirmation`, `conflicting` sau să blocheze publicarea regulii critice.

## Gaps rămase

| id | severitate | descriere | rezolvare necesară |
|---|---|---|---|
| `gap.contract_terms` | `critical` | Termenele, beneficiarii, excluderile și actele finale sunt definite de contractul concret. | Ingestie condiții contractuale și formular versiunea curentă. |
| `gap.provider_coverage` | `critical` | Seed-ul acoperă NN, Allianz-Țiriac și Groupama, nu toată piața. | Research per asigurător și produs. |
| `gap.entitlement` | `critical` | Aplicația nu poate decide dreptul la indemnizație sau cuantumul. | Status needs_confirmation până la decizia oficială a asigurătorului. |

## Conflicte oficiale

Nu a fost identificat un conflict oficial explicit în sursele folosite pentru acest seed. Aceasta nu înseamnă că nu există alte conflicte nepublicate sau încă neidentificate.

## Captură și aprobare necesare

- `snapshot_status`: `pending_immutable_capture` pentru toate sursele.
- Citatele trebuie reconfirmate pe snapshot/PDF și hash-uite SHA-256 înainte de activare.
- Un curator trebuie să aprobe separat fiecare claim critic și fiecare regulă derivată.
- Datele locale din afara pilotului Timiș/Timișoara rămân `verified_with_local_gap`.
