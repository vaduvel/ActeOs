# Event Card — ro.life.residence_registration (life.residence_registration)

**Batch:** B01_RESIDENCE_REGISTRATION  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Locuiesc temporar la o adresă secundară și vreau să îmi înscriu reședința.”

## Limita evenimentului

Acoperă mențiunea/dovada de reședință, nu schimbarea domiciliului. Pragul este locuirea efectivă mai mult de 15 zile pe lună.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `age_years` | `integer` | vârsta | da |
| `days_per_month_at_secondary` | `integer` | zile/lună la adresa secundară | da |
| `requested_period_days` | `integer` | durata solicitată, max. un an | da |
| `current_document_type` | `enum` | `cei`, `cis`, `ci1997` | da |
| `host_status` | `enum` | `owner`, `hosted`, `campus_or_institution` | da |
| `has_residence_proof` | `boolean` | dovada adresei | da |
| `service_matches_residence` | `boolean` | serviciu competent teritorial | da |
| `host_declaration_location` | `enum` | `romania`, `romanian_authority_abroad` | condițional |
| `host_declaration_age_days` | `integer` | vechimea declarației | condițional |
| `request_channel` | `enum` | `counter`, `email` | da |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `register_residence` | reședință înscrisă | >15 zile, max. un an, dosar, competență |
| `receive_residence_certificate` | dovadă separată pentru CEI/CIS | tip act |
| `apply_residence_sticker` | autocolant pe CI 1997 | tip act |

## Reguli-cheie verificate

- Reședința se înscrie pentru locuire mai mult de 15 zile și cel mult un an.
- Cererea este personală și se depune la serviciul competent pentru adresa secundară.
- Găzduirea necesită consimțământ și dovada titlului.
- HUB publică gratuitate, dar normele păstrează o referire la dovada plății; conflictul rămâne vizibil.

## Canal pilot Timișoara / Timiș

Pentru pilot se atașează DEP Timișoara și pagina oficială locală privind dovada adresei; circumscripția exactă trebuie rezolvată din adresă.

## Guvernanță

Motorul nu transformă automat reședința în domiciliu și nu taxează utilizatorul pe baza unei referiri normative conflictuale.
