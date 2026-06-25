# Gaps — ro.life.digital_identity_ro

**Accessed at:** 2026-06-25  
**Status:** `research_candidate_not_production_published`

> Un gap nu este completat prin presupunere. Până la confirmare, motorul trebuie să emită `needs_confirmation`, `conflicting` sau să blocheze publicarea regulii critice.

## Gaps rămase

| id | severitate | descriere | rezolvare necesară |
|---|---|---|---|
| `gap.validation_time_conflict` | `critical` | Pagina Cetățeni indică 24–72 ore lucrătoare, iar Termenii indică maximum 24 ore. | Solicitare de clarificare ADR; până atunci status conflicting și fără deadline garantat. |
| `gap.age_rules` | `critical` | Sursele publice cercetate nu oferă o regulă completă și neechivocă privind vârsta minimă pentru persoana fizică. | Confirmare oficială ADR înainte de modelarea minorilor. |
| `gap.platform_coverage` | `operational` | Lista exactă și curentă a platformelor compatibile se schimbă. | Import din lista oficială de furnizori ROeID cu freshness separat. |

## Conflicte oficiale

| id | claim A | claim B | status | comportament |
|---|---|---|---|---|
| `conflict.roeid.validation_duration` | `claim.digital_identity_ro.roeid_duration_24_72` | `claim.digital_identity_ro.roeid_duration_max_24` | `unresolved` | Nu se afișează termen garantat; utilizatorul urmărește notificarea oficială. |

## Captură și aprobare necesare

- `snapshot_status`: `pending_immutable_capture` pentru toate sursele.
- Citatele trebuie reconfirmate pe snapshot/PDF și hash-uite SHA-256 înainte de activare.
- Un curator trebuie să aprobe separat fiecare claim critic și fiecare regulă derivată.
- Datele locale din afara pilotului Timiș/Timișoara rămân `verified_with_local_gap`.
