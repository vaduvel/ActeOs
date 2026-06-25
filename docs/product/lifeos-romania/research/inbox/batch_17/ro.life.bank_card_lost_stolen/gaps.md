# Gaps — ro.life.bank_card_lost_stolen

**Accessed at:** 2026-06-25  
**Status:** `research_candidate_not_production_published`

> Un gap nu este completat prin presupunere. Până la confirmare, motorul trebuie să emită `needs_confirmation`, `conflicting` sau să blocheze publicarea regulii critice.

## Gaps rămase

| id | severitate | descriere | rezolvare necesară |
|---|---|---|---|
| `gap.provider_coverage` | `critical` | Seed-ul include ING, BT, BCR și CEC; alți emitenți necesită surse proprii. | Extindere registru emitent și testare periodică a numerelor. |
| `gap.replacement_fees` | `operational` | Costul și termenul reemiterii nu sunt universale. | Document tarifar și condiții actuale per produs. |
| `gap.police_report` | `operational` | Nu a fost confirmată o obligație universală de plângere la poliție pentru reemiterea cardului. | Modelare numai dacă emitentul o solicită explicit sau există un alt incident penal. |

## Conflicte oficiale

| id | claim A | claim B | status | comportament |
|---|---|---|---|---|
| `conflict.cec.secondary_phone` | `claim.bank_card_lost_stolen.cec_faq_numbers` | `claim.bank_card_lost_stolen.cec_contact_numbers` | `unresolved` | Nu se alege numărul secundar; se afișează doar 021 202 69 99, comun ambelor surse, până la clarificare. |

## Captură și aprobare necesare

- `snapshot_status`: `pending_immutable_capture` pentru toate sursele.
- Citatele trebuie reconfirmate pe snapshot/PDF și hash-uite SHA-256 înainte de activare.
- Un curator trebuie să aprobe separat fiecare claim critic și fiecare regulă derivată.
- Datele locale din afara pilotului Timiș/Timișoara rămân `verified_with_local_gap`.
