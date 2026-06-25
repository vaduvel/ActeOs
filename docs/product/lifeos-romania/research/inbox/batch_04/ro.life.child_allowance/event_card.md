# Event Card — ro.life.child_allowance (life.child_allowance)

**Batch:** BATCH_04_CHILD_BIRTH_PARENTAL_BENEFITS  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau alocația de stat pentru copil” sau „vreau continuarea alocației după 18 ani”.

## Limită de domeniu

Acoperă eligibilitatea și inițierea/continuarea alocației de stat. Nu calculează automat cuantumul numeric 2026 fără o publicație oficială curentă și nu rezolvă coordonarea prestațiilor între state.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `child_birth_date` | date | folosit pentru vârsta la data de referință | da |
| `child_citizenship` | country_code | cetățenia copilului | condiționat |
| `resident_in_romania` | boolean | pentru copil străin/apatrid | condiționat |
| `lives_with_parent_in_romania` | boolean | condiție pentru copil străin/apatrid | condiționat |
| `education_status` | enum | `not_applicable`, `school`, `high_school_or_vocational`, `preuniversity`, `none` | condiționat |
| `has_finished_program` | boolean | finalizarea liceului/profesionalului | condiționat |
| `child_has_disability` | boolean | certificat de handicap/dizabilitate | condiționat |
| `repeats_school_year` | boolean | repetă anul după 18 ani | condiționat |
| `repeat_due_to_health` | boolean | motiv medical dovedibil | condiționat |
| `application_date` | date | ancoră plată și retroactivitate | condiționat |
| `requested_payee` | enum | `mother`, `father`, `legal_representative`, `child`, `young_adult` | condiționat |
| `direct_payment_requested` | boolean | plată directă după 14 ani | condiționat |
| `relevant_change_occurred` | boolean | schimbare care poate afecta dreptul | condiționat |
| `change_date` | date | ancoră termen 15 zile | condiționat |

## Traseu determinist

1. **check_age_and_status** — determină categoria de vârstă și educație — `verified`.
2. **collect_application_proof** — cerere și acte justificative — `verified`.
3. **select_payee_and_payment** — stabilește persoana care încasează și metoda — `verified`.
4. **apply_child_allowance** — depune cererea la circuitul local/AJPIS — `verified_with_local_gap`.
5. **report_allowance_change** — notifică modificările în 15 zile — `verified`.

## Canale oficiale

- `ch.child_allowance.timisoara` — canalul local pentru dosarul de alocație — URL/listă statică încă neconfirmate

## Excluderi și hand-off

- Prestațiile familiale din alt stat UE necesită analiză de coordonare separată.
- Alocația nu este același drept cu indemnizația CCC sau stimulentul de inserție.
- Plata pentru copii aflați în protecție specială are reguli distincte.

## Note de guvernanță

- Cuantumul 2026 rămâne `needs_confirmation`; nu se hardcodează o valoare dedusă.
- Retroactivitatea nu depășește 12 luni, dar data efectivă se calculează de autoritate.
- Pentru alte UAT-uri, regulile naționale sunt verificate, canalul local este gap.
