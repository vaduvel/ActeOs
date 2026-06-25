# Event Card — ro.life.minor_travel_abroad (life.minor_travel_abroad)

**Batch:** BATCH_04_CHILD_BIRTH_PARENTAL_BENEFITS  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau să călătoresc în străinătate cu un minor / minorul călătorește singur.”

## Limită de domeniu

Acoperă condițiile române de ieșire din țară pentru minori cetățeni români. Nu verifică regulile de intrare ale statului de destinație, vizele, condițiile companiei aeriene sau alertele Schengen.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `minor_age_years` | integer | vârsta la data trecerii frontierei | da |
| `travel_companion` | enum | `both_parents`, `one_parent`, `third_person`, `unaccompanied` | da |
| `sole_parental_authority_or_exception` | boolean | autoritate exclusivă, deces, hotărâre/altă excepție | condiționat |
| `destination_residence_proved` | boolean | domiciliu/reședință în țara de destinație | condiționat |
| `travel_purpose` | enum | `tourism`, `return_to_residence`, `urgent_medical_treatment`, `study`, `official_competition` | condiționat |
| `consent_signed_abroad` | boolean | activează autentificare/apostilă | condiționat |
| `has_valid_travel_document` | boolean | pașaport/CI recunoscută, după caz | condiționat |

## Traseu determinist

1. **verify_minor_travel_document** — confirmă documentul individual valabil — `verified`.
2. **classify_companion_and_consent** — alege declarația/excepția aplicabilă — `verified`.
3. **authenticate_consent** — verifică notar/consulat/apostilă după locul semnării — `verified`.
4. **prepare_exception_documents** — reședință, medical, studii sau concurs — `verified`.
5. **predeparture_border_check** — reconfirmă condițiile operaționale înainte de plecare — `conflicting_for_age16_unaccompanied`.

## Canale oficiale

- `ch.border_police.conditions` — pagina oficială Poliția de Frontieră pentru condițiile de ieșire ale minorilor

## Excluderi și hand-off

- Pașaportul minorului este un eveniment separat.
- Regulile de intrare în destinație se verifică la MAE/autoritatea statului respectiv.
- Refuzul/contestarea la frontieră necesită asistență juridică și actele concrete.

## Note de guvernanță

- Legea 248/2005 este sursa normativă; pagina operațională este păstrată separat.
- Neconcordanța privind minorii de 16+ neînsoțiți este expusă ca `conflicting`, nu ascunsă.
- Verificarea cazierului însoțitorului este electronică; aplicația nu cere încărcarea cazierului fizic.
