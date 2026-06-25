# Gaps — ro.life.bank_account_open

**Accessed at:** 2026-06-25  
**Status:** `research_candidate_not_production_published`

> Un gap nu este completat prin presupunere. Până la confirmare, motorul trebuie să emită `needs_confirmation`, `conflicting` sau să blocheze publicarea regulii critice.

## Gaps rămase

| id | severitate | descriere | rezolvare necesară |
|---|---|---|---|
| `gap.provider_catalog` | `critical` | Nu există o listă unică de documente pentru toate băncile; trebuie cercetat fiecare produs/provider. | Adăugare conector și snapshot oficial per provider. |
| `gap.fees` | `critical` | Comisioanele și condițiile comerciale sunt dinamice și nu sunt modelate ca fapt universal. | Captură a documentului de tarife în vigoare pentru produsul ales. |
| `gap.minors` | `critical` | Produsele pentru minori au reguli distincte și nu sunt deduse din fluxurile standard pentru adulți. | Eveniment/intent separat pentru contul minorului. |

## Conflicte oficiale

Nu a fost identificat un conflict oficial explicit în sursele folosite pentru acest seed. Aceasta nu înseamnă că nu există alte conflicte nepublicate sau încă neidentificate.

## Captură și aprobare necesare

- `snapshot_status`: `pending_immutable_capture` pentru toate sursele.
- Citatele trebuie reconfirmate pe snapshot/PDF și hash-uite SHA-256 înainte de activare.
- Un curator trebuie să aprobe separat fiecare claim critic și fiecare regulă derivată.
- Datele locale din afara pilotului Timiș/Timișoara rămân `verified_with_local_gap`.
