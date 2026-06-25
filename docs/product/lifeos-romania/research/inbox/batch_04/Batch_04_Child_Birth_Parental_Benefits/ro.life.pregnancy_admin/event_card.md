# Event Card — ro.life.pregnancy_admin (life.pregnancy_admin)

**Batch:** BATCH_04_CHILD_BIRTH_PARENTAL_BENEFITS  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Sunt gravidă / am născut recent / alăptez și trebuie să îmi activez drepturile administrative la locul de muncă.”

## Limită de domeniu

Acoperă notificarea angajatorului, evaluarea riscurilor, adaptarea postului, concediul de risc maternal, consultațiile, reducerea programului, alăptarea și protecțiile de muncă. Nu oferă diagnostic sau recomandare medicală.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `written_notice_sent` | boolean | notificare scrisă către angajator | da |
| `medical_document_attached` | boolean | document medic familie/specialist | da |
| `workplace_risk_identified` | boolean | risc evaluat pentru mamă/copil | condiționat |
| `adaptation_or_transfer_possible` | boolean | înainte de risc maternal | condiționat |
| `doctor_recommends_reduced_schedule` | boolean | reducere cu o pătrime | condiționat |
| `prenatal_consultations_only_during_work` | boolean | dispensă max. 16 ore/lună | condiționat |
| `is_breastfeeding` | boolean | pauze/reducere până la un an | condiționat |
| `child_age_months` | integer | 0–12+ | condiționat |
| `works_night_shift` | boolean | transfer la muncă de zi | condiționat |
| `insalubrious_or_hard_work` | boolean | transfer la loc sigur | condiționat |
| `dismissal_or_retaliation_threat` | boolean | protecție și escaladare | condiționat |

## Traseu determinist

1. **notify_employer_pregnancy** — transmite notificarea și documentul medical — `verified`.
2. **request_risk_assessment_and_adaptation** — aplică ierarhia adaptare → transfer → risc maternal — `verified`.
3. **request_maternity_risk_leave** — obține concediul medical dacă măsurile nu sunt posibile — `verified`.
4. **request_quarter_schedule_reduction** — reduce programul cu o pătrime pe recomandare medicală — `verified`.
5. **request_prenatal_consultation_leave** — folosește maximum 16 ore/lună în condițiile legii — `verified`.
6. **request_breastfeeding_breaks_or_reduction** — două pauze sau două ore reducere până la un an — `verified`.
7. **request_safe_work_transfer** — elimină noaptea/condițiile insalubre — `verified`.

## Canale oficiale

- Nu există pas local în pilot; traseul este național sau derulat prin angajator.

## Excluderi și hand-off

- Concediul de maternitate de 126 zile este în `life.maternity_leave`.
- Consultația medicală și certificatul sunt emise de profesioniștii competenți.
- Litigiile se predau către ITM/instanță/consiliere juridică.

## Note de guvernanță

- Protecțiile speciale nu sunt presupuse fără notificarea și documentul medical cerute de lege.
- Concediul de risc maternal este ultima treaptă după adaptare/transfer, dacă faptele confirmă imposibilitatea.
- Aplicația nu divulgă starea de graviditate în analytics sau notificări neprotejate.
