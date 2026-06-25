# Event Card — ro.life.passport_lost_stolen (life.passport_lost_stolen)

**Batch:** B01_PASSPORT_LOST_STOLEN  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Mi-am pierdut pașaportul / mi-a fost furat / s-a distrus.”

## Limita evenimentului

Acoperă declararea evenimentului, invalidarea documentului și cererea unui nou pașaport. Nu promite pașaport temporar pentru o simplă vacanță.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `incident_type` | `enum` | `lost`, `stolen`, `destroyed` | da |
| `incident_country` | `enum` | `ro`, `foreign` | da |
| `event_declared` | `boolean` | eveniment declarat autorității competente | da |
| `passport_found_after_declaration` | `boolean` | document găsit ulterior | da |
| `age_years` | `integer` | vârsta titularului | da |
| `passport_type` | `enum` | `electronic`, `temporary` | da |
| `urgency_reason` | `enum` | `medical`, `study`, `legal`, `tourism`, `none` | da |
| `has_police_certificate` | `boolean` | adeverință de furt | condițional |
| `request_location` | `enum` | `country`, `abroad` | da |
| `request_channel` | `enum` | `counter`, `electronic` | da |
| `pickup_method` | `enum` | `personal`, `proxy`, `courier` | da |
| `payment_status` | `enum` | `paid`, `unpaid` | da |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `declare_passport_event` | pierderea/distrugerea declarată | canal competent |
| `report_passport_theft_to_police` | furt declarat și adeverință | unitatea de poliție competentă |
| `request_replacement_passport` | nou pașaport solicitat | eveniment declarat, dosar, biometrie, plată |
| `surrender_found_invalid_passport` | document nul predat | document găsit după declarare |

## Reguli-cheie verificate

- Pașaportul declarat pierdut/furat/distrus devine nul și nu poate fi reutilizat.
- Pentru furt este necesară sesizarea imediată a poliției și adeverința de declarare.
- Pașaportul temporar necesită situație obiectivă și urgentă probată; turismul exclusiv este exclus.
- Contravaloarea publicată la 25 iunie 2026 este 265 lei pentru ambele tipuri.

## Canal pilot Timișoara / Timiș

SPCEEPS Timiș: Bd. Demetriade nr. 1, Iulius Mall, etaj 1. Punctele Lugoj, Sânnicolau Mare, Jimbolia și Deta sunt publicate ca suspendate temporar.

## Guvernanță

Termenele operaționale și programul sunt claim-uri volatile. Motorul păstrează separat limita legală de 15 zile și estimarea curentă de cel mult 5 zile.
