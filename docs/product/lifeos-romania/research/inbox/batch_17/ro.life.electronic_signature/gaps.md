# Gaps — ro.life.electronic_signature

**Accessed at:** 2026-06-25  
**Status:** `research_candidate_not_production_published`

> Un gap nu este completat prin presupunere. Până la confirmare, motorul trebuie să emită `needs_confirmation`, `conflicting` sau să blocheze publicarea regulii critice.

## Gaps rămase

| id | severitate | descriere | rezolvare necesară |
|---|---|---|---|
| `gap.recipient_acceptance` | `critical` | Tipul acceptat trebuie confirmat pentru fiecare act și platformă țintă. | Research și conector per platformă/demers. |
| `gap.provider_prices` | `operational` | Tarifele și promoțiile se schimbă și nu reprezintă taxe publice. | Nu publica preț fără snapshot curent și aprobare. |
| `gap.provider_coverage` | `critical` | Seed-ul operațional acoperă certSIGN și DigiSign, nu toți prestatorii din Trusted List. | Import automat al Trusted List și research per prestator. |

## Conflicte oficiale

Nu a fost identificat un conflict oficial explicit în sursele folosite pentru acest seed. Aceasta nu înseamnă că nu există alte conflicte nepublicate sau încă neidentificate.

## Captură și aprobare necesare

- `snapshot_status`: `pending_immutable_capture` pentru toate sursele.
- Citatele trebuie reconfirmate pe snapshot/PDF și hash-uite SHA-256 înainte de activare.
- Un curator trebuie să aprobe separat fiecare claim critic și fiecare regulă derivată.
- Datele locale din afara pilotului Timiș/Timișoara rămân `verified_with_local_gap`.
