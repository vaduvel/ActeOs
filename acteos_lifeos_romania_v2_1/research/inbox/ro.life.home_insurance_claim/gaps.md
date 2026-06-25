# Gaps — ro.life.home_insurance_claim

**Accessed at:** 2026-06-25  
**Status:** `research_candidate_not_production_published`

> Un gap nu este completat prin presupunere. Până la confirmare, motorul trebuie să emită `needs_confirmation`, `conflicting` sau să blocheze publicarea regulii critice.

## Gaps rămase

| id | severitate | descriere | rezolvare necesară |
|---|---|---|---|
| `gap.contract_specific` | `critical` | Polițele facultative au condiții și excluderi contractuale diferite. | Ingestie a condițiilor poliței concrete și aprobare curator. |
| `gap.local_authorities` | `critical` | Contactele locale sunt pilot Timiș/Timișoara; alte UAT-uri necesită mapare proprie. | Registru ISU/SVSU/CLSU per jurisdicție. |
| `gap.coverage_decision` | `critical` | Aplicația nu poate decide acoperirea sau valoarea despăgubirii numai din descrierea utilizatorului. | Afișare ca needs_confirmation până la decizia asigurătorului. |

## Conflicte oficiale

Nu a fost identificat un conflict oficial explicit în sursele folosite pentru acest seed. Aceasta nu înseamnă că nu există alte conflicte nepublicate sau încă neidentificate.

## Captură și aprobare necesare

- `snapshot_status`: `pending_immutable_capture` pentru toate sursele.
- Citatele trebuie reconfirmate pe snapshot/PDF și hash-uite SHA-256 înainte de activare.
- Un curator trebuie să aprobe separat fiecare claim critic și fiecare regulă derivată.
- Datele locale din afara pilotului Timiș/Timișoara rămân `verified_with_local_gap`.
