# Event Card — ro.life.survivor_pension (life.survivor_pension)

**Batch:** BATCH_11_PENSIONS_HEALTH_ADMIN  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau să obțin pensie de urmaș” după decesul unui susținător.

## Limită de domeniu

Acoperă eligibilitatea copilului sau soțului supraviețuitor, documentele, procentul și data de început în sistemul public. Nu acoperă pensiile militare, toate coordonările internaționale ori calculul monetar integral.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `beneficiary_type` | enum | child / spouse | da |
| `deceased_status` | enum | pensioner / non_pensioner | da |
| `child_age` | integer | vârsta copilului | pentru child |
| `continues_studies` | boolean | continuă studiile între 16 și 26 ani | condiționat |
| `eligible_disability` | boolean | invaliditatea a apărut în perioada eligibilă | condiționat |
| `standard_age_reached` | boolean | soțul a atins vârsta standard | pentru spouse |
| `marriage_months` | integer | durata exactă a căsătoriei | pentru spouse |
| `spouse_invalidity_grade` | enum | I / II / III / none | condiționat |
| `income_condition_met` | boolean | condiția privind categoriile și pragul de venit | condiționat |
| `death_cause` | enum | ordinary / work_accident / occupational_disease | da |
| `cares_for_child_under_7` | boolean | îngrijirea unui copil sub 7 ani | condiționat |
| `eligible_survivor_count` | integer | numărul urmașilor eligibili | da |
| `application_within_30_days` | boolean | cererea este în fereastra legală | da |
| `jurisdiction_id` | jurisdiction_id | domiciliul titularului/reprezentantului | da |

## Traseu determinist

1. **classify_survivor_route** — identifică ruta copil/soț și condițiile speciale — `verified`.
2. **collect_survivor_documents** — selectează Anexa nr. 7 și actele condiționate — `verified`.
3. **determine_survivor_percentage** — aplică procentul după numărul urmașilor — `verified`.
4. **derive_survivor_start_date** — stabilește data efectelor după statut și termen — `verified`.
5. **submit_survivor_application** — depune la casa teritorială competentă — `verified_with_local_gap`.

## Canale oficiale

- `ch.cnpp.online_forms` — formularul oficial CNPP — Anexa nr. 7
- `ch.cjp_timisoara.contact` — CJP Timiș — contact local verificat; canalul concret se reconfirmă

## Excluderi și hand-off

- Nu calculează cuantumul final al pensiei susținătorului.
- Cazurile transfrontaliere se redirecționează către coordonarea internațională.
- Nu substituie decizia medicală asupra capacității de muncă.

## Note de guvernanță

- Pragul de venit se evaluează la data relevantă; motorul nu hardcodează valoarea salariului minim.
- Pentru copilul de 16–26 ani, dovada studiilor este atât document de eligibilitate, cât și obligație periodică.
- Data de început este o regulă cu ramuri; nu se reduce la formula «de la deces».
