# Event Card — ro.life.event_public_space_authorisation (life.event_public_space_authorisation)

**Titlu:** Vreau să autorizez un eveniment în spațiul public  
**Batch:** B09_EVENT_PUBLIC_SPACE_AUTHORISATION  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul organizează un eveniment care utilizează domeniul public și trebuie să identifice dosarul local și eventualele ramuri speciale.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `jurisdiction_id` | jurisdiction id | UAT-ul evenimentului |
| `organizer_type` | enum | natural_person/legal_person |
| `event_type` | enum | public_domain_event/public_assembly_or_protest/other |
| `uses_public_domain` | boolean | declanșator local |
| `is_outdoor_cultural_event` | boolean | condiția a |
| `public_place_delimited` | boolean | condiția b |
| `public_access_limited` | boolean | condiția c |
| `special_event_branch` | boolean | ramura taxei speciale |
| `event_start_date` | date | limită „înainte de” |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `classify_event_and_public_space_use` | întotdeauna | selectează tipul corect | `claim.tm.event.generic_cases` |
| `submit_timisoara_event_request` | Timișoara și domeniu public | trimite cererea | `claim.tm.event.generic_steps` |
| `assess_limited_access_outdoor_event_tax` | toate cele 3 condiții | activează ramura specială | `claim.tm.event.special_cumulative_conditions` |
| `submit_before_event_start` | ramura specială | depune înainte de început | `claim.tm.event.submit_before_start` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| Timișoara | Portal PMT — Organizare evenimente | `verified_with_local_gap` |
| Timișoara special | Portal PMT — evenimente culturale în aer liber | `conflicting` |
| național adunări publice | Poliția Română — rută oficială | `verified_with_local_gap` |

## Note de guvernanță

- Conflictul HCL 2025/2026 este păstrat explicit și blochează lista exactă de acte.
- Nu se aplică taxa specială dacă lipsește una dintre condițiile cumulative.
- Adunarea publică este declanșată ca ramură separată, fără termen inventat.

===
