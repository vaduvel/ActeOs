# Event Card — ro.life.pension_recalculation (life.pension_recalculation)

**Batch:** BATCH_11_PENSIONS_HEALTH_ADMIN  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau să cer recalcularea pensiei” pentru venituri, stagii sau perioade nevalorificate.

## Limită de domeniu

Acoperă recalcularea la cerere, stagiul după pensionare, diferența față de revizuire și termenul special de contestare a deciziei. Nu recalculează punctajul monetar în afara datelor oficiale.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `recalculation_basis` | enum | unvalued_income / unvalued_stage / assimilated_period / rectifying_declaration / post_retirement_contributions | da |
| `period_after_2001_04_01` | boolean | perioada este ulterioară pragului CNPP | condiționat |
| `data_present_in_cnpp_database` | boolean | datele apar în baza CNPP | condiționat |
| `already_requested_this_calendar_year` | boolean | cerere anterioară pentru stagiu post-pensionare | condiționat |
| `issue_type` | enum | new_evidence / wrong_amount_or_payment | da |
| `material_or_calculation_error` | boolean | excepția de eroare materială/calcul | condiționat |
| `application_date` | date | data înregistrării cererii | da |
| `wants_to_contest_decision` | boolean | contestarea deciziei rezultate | da |
| `jurisdiction_id` | jurisdiction_id | domiciliul pensionarului | da |

## Traseu determinist

1. **classify_recalculation_or_review** — separă recalcularea de revizuirea unei erori — `verified`.
2. **collect_unvalued_evidence** — identifică perioada și documentul justificativ — `verified`.
3. **prepare_recalculation_application** — pregătește Anexa nr. 16 și actele — `verified`.
4. **derive_next_month_effect** — stabilește luna efectelor — `verified`.
5. **submit_recalculation_application** — depune la casa teritorială competentă — `verified_with_local_gap`.

## Canale oficiale

- `ch.cnpp.online_forms` — CNPP — Anexa nr. 16 și servicii electronice
- `ch.cjp_timisoara.contact` — CJP Timiș — date locale de contact

## Excluderi și hand-off

- Nu confundă recalcularea cu indexarea legală automată.
- Nu promite majorarea cuantumului; rezultatul depinde de valorificarea oficială.
- Nu aplică termenul general de contencios în locul termenului special de 45 de zile al deciziei de pensie.

## Note de guvernanță

- Adeverințele trebuie validate atât ca sursă, cât și ca formă; simpla încărcare nu dovedește valorificarea.
- Regula după 1 aprilie 2001 presupune că datele există efectiv în baza CNPP; discrepanțele se clarifică.
- Recalcularea pentru stagiu după pensionare are limită de frecvență anuală.
