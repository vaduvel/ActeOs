# Event Card — ro.life.retirement_age (life.retirement_age)

**Batch:** BATCH_11_PENSIONS_HEALTH_ADMIN  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau să aflu când mă pot pensiona” sau „vreau să verific dacă îndeplinesc condițiile pentru pensia de limită de vârstă”.

## Limită de domeniu

Determină traseul de verificare pentru pensia publică de limită de vârstă, inclusiv data din anexa nr. 5 și câteva reduceri expres modelate. Nu substituie certificarea stagiului de către CNPP și nu acoperă integral toate profesiile, condițiile speciale, sistemele militare ori pensiile de serviciu.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `birth_date` | date | data nașterii | da |
| `sex_for_annex5` | enum | `male`, `female` — strict pentru eșalonarea legală | da |
| `standard_retirement_date` | date | rezultat din anexa nr. 5 | da / derivat |
| `standard_age_reached` | boolean | compararea datei de referință cu data standard | da / derivat |
| `contributory_years` | decimal | stagiu contributiv verificat | da |
| `full_contributory_stage_met` | boolean | stagiul complet aferent anexei nr. 5 | condiționat |
| `extra_total_stage_years` | decimal | stagiu total peste stagiul complet pentru art. 56 | condiționat |
| `years_before_standard` | decimal | ani rămași până la vârsta standard | condiționat |
| `eligible_children_count` | integer | copii care îndeplinesc condiția legală de creștere | condiționat |
| `disability_degree` | enum | `none`, `severe`, `accentuated`, `medium`, `severe_visual` | condiționat |
| `permanent_disability_certificate` | boolean | certificat cu mențiunile legale | condiționat |
| `combined_reduction_years` | decimal | cumulul reducerilor permise | condiționat |
| `wants_continue_to_70` | boolean | opțiune de continuare a activității | condiționat |
| `conditions_met_date` | date | ancoră pentru termenul de 30 zile | condiționat |
| `application_date` | date | data depunerii | condiționat |
| `jurisdiction_id` | jurisdiction_id | domiciliul solicitantului | da |

## Traseu determinist

1. **lookup_annex5_retirement_schedule** — stabilește data exactă în funcție de luna și anul nașterii — `verified`.
2. **verify_contributory_stage** — verifică stagiul minim/complet și perioadele valorificabile — `verified`.
3. **evaluate_age_reductions** — aplică numai reducerile susținute de fapte și dovezi — `verified`.
4. **prepare_old_age_pension_application** — pregătește Anexa nr. 3 și actele aplicabile — `verified`.
5. **submit_old_age_pension_application** — depune la casa teritorială competentă — `verified_with_local_gap`.

## Canale oficiale

- `ch.cnpp.online_forms` — formulare și servicii electronice CNPP; autentificarea și disponibilitatea concretă se verifică la depunere
- `ch.cjp_timisoara.contact` — CJP Timiș, Str. Andrei Șaguna nr. 5A; programarea/ghișeul exact rămân de confirmat

## Excluderi și hand-off

- Pensiile militare, pensiile de serviciu și sistemele neintegrate necesită evenimente distincte.
- Reducerile pentru condiții deosebite/speciale și profesii sunt doar semnalate; tabelele complete nu sunt codificate în acest batch.
- Calculul cuantumului pensiei nu face parte din acest eveniment.

## Note de guvernanță

- Nu se hardcodează «65 de ani pentru toți»; anexa nr. 5 prevalează.
- Stagiul declarat de utilizator este orientativ până la confirmarea din evidența CNPP.
- Canalul local publicat pentru petiții nu este tratat automat ca un canal valid de depunere a cererii de pensie.
