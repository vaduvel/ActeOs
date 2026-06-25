# Event Card — ro.life.open_working_point (life.open_working_point)

**Batch:** B12_OPEN_WORKING_POINT  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să deschid un punct de lucru.”

## Limita evenimentului

Acoperă înregistrarea unui punct de lucru/sediu secundar pentru PFA sau SRL și legătura cu autorizarea activității la adresă. Nu tratează o sucursală cu regim juridic distinct și nu emite avizele locale ori sectoriale.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `entity_type` | `enum` | pfa sau srl | da |
| `working_point_address` | `string` | adresa punctului | da |
| `has_use_right_document` | `boolean` | drept de folosință asupra spațiului | da pentru PFA; de verificat pentru SRL |
| `activity_already_registered_authorized` | `boolean` | activitatea este deja în obiect și autorizată | da |
| `company_decision_date` | `date` | data hotărârii/deciziei SRL | condițional |
| `constitutive_act_is_modified` | `boolean` | operațiunea schimbă actul constitutiv | condițional |
| `filing_actor` | `enum` | titular/reprezentant/mandatar/avocat | da |
| `filing_channel` | `enum` | counter, post_courier, online | da |
| `local_activity_family` | `enum` | retail, food_service, services, other | condițional |
| `local_commercial_agreement_applicable` | `boolean` | procedură locală aplicabilă | condițional |
| `use_right_valid_on_start_date` | `boolean` | dreptul de folosință este valabil la data începerii | condițional |
| `special_permit_required` | `boolean` | activitatea cere aviz/licență sectorială | condițional |
| `special_permit_obtained` | `boolean` | avizul/licența sectorială este obținută | condițional |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `register_pfa_working_point` | mențiune punct de lucru PFA | folosință și activitate autorizată |
| `approve_srl_secondary_office` | hotărâre internă SRL | competența din actul constitutiv |
| `file_working_point_mention` | depunere mențiune ONRC | termen și semnatar |
| `register_or_authorize_new_activity` | extinderea activității | dacă activitatea nu este deja autorizată |
| `obtain_timisoara_commercial_agreement_for_point` | acord local | tipul activității și spațiului |

## Reguli-cheie verificate

- Punctul de lucru PFA se înregistrează la registrul comerțului.
- Pentru PFA se dovedește dreptul de folosință asupra spațiului.
- Pentru SRL, competența și eventuala modificare a actului constitutiv se verifică înaintea depunerii.
- Acordul comercial Timișoara este separat și dependent de cazul selectat.

## Canal pilot Timișoara / Timiș

Pentru Timișoara, serviciul local diferențiază activitățile; alimentația publică are întrebări suplimentare privind incendiu, mediu și program. Motorul nu generalizează aceste cerințe pentru alte UAT-uri.

## Guvernanță

Termenul „punct de lucru” nu este echivalat automat cu „sucursală”. Dacă utilizatorul descrie o sucursală, clasificarea trebuie corectată înainte de generarea dosarului.
