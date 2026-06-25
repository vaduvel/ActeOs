# Event Card — ro.life.invalidity_pension (life.invalidity_pension)

**Batch:** BATCH_11_PENSIONS_HEALTH_ADMIN  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau să obțin pensie de invaliditate” sau „trebuie să fac expertiza capacității de muncă”.

## Limită de domeniu

Acoperă traseul din sistemul public: expertiza medicală, cererea de pensie, termenele, contestația medicală și revizuirea periodică. Nu stabilește diagnostic, grad ori cuantum.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `below_standard_age` | boolean | persoana este sub vârsta standard din anexa nr. 5 | da |
| `has_qualifying_contributory_stage` | boolean | stagiu eligibil înaintea riscului | da |
| `person_status` | enum | employee / pupil / apprentice / student / other | da |
| `practice_professional_accident` | boolean | excepția de practică profesională | condiționat |
| `risk_cause` | enum | work_accident / occupational_disease / ordinary_disease / ordinary_accident | da |
| `medical_decision_exists` | boolean | decizia medicului expert există | da |
| `medical_grade` | enum | I / II / III | din decizie |
| `application_within_30_days_of_medical_decision` | boolean | cerere în termen | da |
| `wants_to_contest_medical_decision` | boolean | intenția de contestare | da |
| `already_receives_invalidity_pension` | boolean | este deja beneficiar | da |
| `review_exempt` | boolean | excepție stabilită/confirmată | condiționat |
| `jurisdiction_id` | jurisdiction_id | domiciliul solicitantului | da |

## Traseu determinist

1. **request_medical_capacity_evaluation** — depune Anexa nr. 9 și documentele medicale — `verified`.
2. **receive_medical_capacity_decision** — preia gradul și termenul de revizuire — `verified`.
3. **prepare_invalidity_pension_application** — pregătește Anexa nr. 6 și actele — `verified`.
4. **submit_invalidity_pension_application** — depune la casa teritorială competentă — `verified_with_local_gap`.
5. **monitor_review_or_appeal** — urmărește revizuirea ori contestația medicală — `verified`.

## Canale oficiale

- `ch.cnpp.online_forms` — CNPP — Anexele nr. 6 și nr. 9
- `ch.cjp_timisoara.contact` — CJP Timiș — contact; cabinetul de expertiză se reconfirmă

## Excluderi și hand-off

- Nu clasifică medical gradul de invaliditate.
- Nu tratează pensiile militare sau de serviciu.
- Nu presupune că orice concediu medical deschide dreptul la pensie de invaliditate.

## Note de guvernanță

- Expertiza medicală și cererea de pensie sunt două etape distincte, cu formulare diferite.
- Contestația deciziei medicale urmează circuitul special, nu plângerea prealabilă generică.
- Revizuirea se face la termenul din decizie fără a aștepta o notificare.
