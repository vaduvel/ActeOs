# Event Card — ro.life.open_pfa (life.open_pfa)

**Batch:** B12_OPEN_PFA  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să îmi deschid un PFA.”

## Limita evenimentului

Acoperă înregistrarea și autorizarea inițială a unui PFA la ONRC. Nu acoperă profesiile liberale care nu se înregistrează în registrul comerțului, alegerea regimului fiscal detaliat ori autorizările sectoriale în sine.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `applicant_has_full_capacity` | `boolean` | capacitate deplină de exercițiu | da |
| `professional_seat_in_ro` | `boolean` | sediu profesional în România | da |
| `has_use_right_document` | `boolean` | înscris de folosință pentru sediu | da |
| `seat_is_dwelling` | `boolean` | sediul este locuință | condițional |
| `activity_at_professional_seat` | `boolean` | se lucrează efectiv la sediu | condițional |
| `caen_class_count` | `integer` | numărul claselor CAEN solicitate | da |
| `special_qualification_required` | `boolean` | activitate cu cerințe de calificare | condițional |
| `special_permit_required` | `boolean` | aviz/licență sectorială prealabilă | condițional |
| `filing_actor` | `enum` | applicant, authenticated_proxy, lawyer, other | da |
| `filing_channel` | `enum` | counter, post_courier, online | da |
| `local_commercial_agreement_applicable` | `boolean` | acord comercial local aplicabil | condițional |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `prepare_pfa_registration` | pregătirea cererii și declarațiilor ONRC | eligibilitate, sediu, CAEN |
| `file_pfa_registration` | depunerea la ONRC | semnatar și canal valid |
| `obtain_sector_permits` | obținerea avizelor speciale | numai pentru activități reglementate |
| `obtain_timisoara_commercial_agreement` | acord local de funcționare | activitate și amplasament eligibile |

## Reguli-cheie verificate

- PFA se înregistrează înainte de începerea activității economice.
- Sediul profesional trebuie să fie în România și să existe dovada dreptului de folosință.
- PFA poate avea cel mult cinci clase CAEN.
- Depunerea electronică folosește semnătură electronică calificată.

## Canal pilot Timișoara / Timiș

Pentru activitățile comerciale din Timișoara, motorul verifică separat serviciul local aplicabil. Taxa și lista de documente sunt dinamice și nu sunt transformate în constante.

## Guvernanță

Profesiile liberale/reglementate și avizele sectoriale sunt gate-uri separate. În lipsa identificării actului special, rezultatul rămâne `needs_confirmation`.
