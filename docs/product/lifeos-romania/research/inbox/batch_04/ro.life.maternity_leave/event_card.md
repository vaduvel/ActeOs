# Event Card — ro.life.maternity_leave (life.maternity_leave)

**Batch:** BATCH_04_CHILD_BIRTH_PARENTAL_BENEFITS  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Am nevoie de concediul și indemnizația de maternitate pentru sarcină și lăuzie.”

## Limită de domeniu

Acoperă dreptul de asigurări sociale de sănătate, stagiul, durata, distribuția prenatal/postnatal, cuantumul procentual și circuitul certificatului medical. Nu emite certificat medical și nu substituie medicul sau casa de asigurări.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `insured_months_last_12` | integer | luni de stagiu eligibil | da |
| `birth_or_due_date` | date | ancoră temporală | da |
| `actual_birth_date` | date|null | activează minimum 42 zile postnatal | condiționat |
| `planned_prenatal_days` | integer | plan orientativ medical | condiționat |
| `planned_postnatal_days` | integer | minimum legal 42 | condiționat |
| `medical_certificate_issued` | boolean | controlează depunerea la plătitor | condiționat |
| `certificate_month` | year_month | ancoră termen ziua 5 | condiționat |
| `birth_outcome` | enum | `pending`, `live_alive`, `stillborn`, `child_died_during_puerperium` | condiționat |
| `mother_has_disability` | boolean | posibil start din luna 6 | condiționat |
| `pregnancy_month` | integer | 1–9 | condiționat |
| `lost_insured_status_non_attributable` | boolean | excepția de 9 luni | condiționat |
| `months_between_loss_and_birth` | integer | 0+ | condiționat |

## Traseu determinist

1. **verify_insurance_stage** — confirmă minimum 6 luni în ultimele 12 — `verified`.
2. **plan_prenatal_postnatal** — respectă 126 zile și minimum 42 postnatale — `verified`.
3. **obtain_maternity_medical_certificates** — certificatul este emis de medic conform regulilor medicale — `verified`.
4. **submit_certificates_for_payment** — predă documentul plătitorului până la data de 5 — `verified`.
5. **verify_payment** — aplică 85% din baza legală — `verified`.

## Canale oficiale

- Nu există pas local în pilot; traseul este național sau derulat prin angajator.

## Excluderi și hand-off

- Concediul de risc maternal este în `life.pregnancy_admin`.
- CCC începe după condițiile proprii și este în `life.parental_leave_benefit`.
- Decizia medicală privind distribuția zilelor aparține medicului și asiguratei în limitele legii.

## Note de guvernanță

- Zilele sunt calendaristice.
- Minimum 42 zile postnatale este un gate critic.
- Baza de calcul nu se ghicește; se preia din documentele oficiale de venit/asigurare.
