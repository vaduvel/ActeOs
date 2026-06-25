---
schema_version: "3.0.0"
batch_id: "batch10.medical_leave"
event_type_id: "ro.life.medical_leave"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "in_review"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.medical_leave` |
| Titlu | Obținerea și administrarea concediului medical |
| Scop | Verifică stagiul, certificatul, predarea, înregistrarea, durata și calculul pentru ruta declarată. |
| Autoritate | Medicul curant, angajatorul, casa de asigurări de sănătate și REGES-ONLINE |
| Pilot local | Reguli naționale; operațiuni prin angajator și casa competentă |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `leave_reason_class` | enum | ordinary_illness \| statutory_no_stage_exception \| other_statutory_category \| unknown | da |
| `insurance_months_last_12` | integer | Luni de stagiu în ultimele 12 luni. | da |
| `has_medical_certificate` | boolean | Certificatul de concediu medical este emis. | da |
| `certificate_delivered_by_day5` | boolean | Certificatul a fost predat până la data de 5 a lunii următoare. | da |
| `employer_registered_certificate` | boolean | Angajatorul a înregistrat și transmis suspendarea în termenul operațional. | da |
| `episode_days` | integer | Numărul de zile din episodul de boală obișnuită. | da |
| `cumulative_days_last_year` | integer | Zile cumulate de incapacitate temporară în ultimul an. | da |
| `has_expert_approval_after_day90` | boolean | Avizul medicului expert este disponibil pentru prelungirea peste ziua 90. | da |
| `one_day_reduction_exception_applies` | boolean | Excepție legală de la diminuarea cu o zi. | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.medical_leave.route.v1` | adevărat | `include_step:obtain_medical_certificate`<br>`include_step:deliver_certificate_to_employer`<br>`include_step:employer_registers_medical_leave_in_reges` | `clm.medical_leave.medical_certificate`, `clm.medical_leave.medical_delivery` | `active` |
| `rule.medical_leave.ordinary_insufficient_stage.v1` | (`leave_reason_class` = `ordinary_illness` ȘI `insurance_months_last_12` < `6`) | `block:ordinary_medical_leave_stage_not_met` | `clm.medical_leave.medical_stage` | `active` |
| `rule.medical_leave.no_stage_exception.v1` | `leave_reason_class` = `statutory_no_stage_exception` | `emit_advice:no_minimum_stage_for_verified_exception_categories` | `clm.medical_leave.medical_no_stage` | `active` |
| `rule.medical_leave.other_category.v1` | `leave_reason_class` = `other_statutory_category` | `require_confirmation:confirm_category_specific_medical_leave_rules` | `clm.medical_leave.medical_certificate` | `in_review` |
| `rule.medical_leave.unknown_category.v1` | `leave_reason_class` = `unknown` | `require_confirmation:confirm_medical_leave_category` | `clm.medical_leave.medical_certificate` | `in_review` |
| `rule.medical_leave.missing_certificate.v1` | `has_medical_certificate` = `False` | `include_requirement:medical_leave_certificate_from_treating_physician`<br>`block:no_medical_leave_without_certificate` | `clm.medical_leave.medical_certificate` | `active` |
| `rule.medical_leave.late_delivery.v1` | `certificate_delivered_by_day5` = `False` | `emit_warning:certificate_not_delivered_by_day5` | `clm.medical_leave.medical_delivery` | `active` |
| `rule.medical_leave.employer_not_registered.v1` | `employer_registered_certificate` = `False` | `emit_warning:employer_reges_transmission_pending` | `clm.medical_leave.medical_delivery` | `active` |
| `rule.medical_leave.rate_55.v1` | (`leave_reason_class` = `ordinary_illness` ȘI `episode_days` ≤ `7`) | `emit_advice:ordinary_illness_rate_55_percent` | `clm.medical_leave.medical_rates` | `active` |
| `rule.medical_leave.rate_65.v1` | (`leave_reason_class` = `ordinary_illness` ȘI `episode_days` ≥ `8` ȘI `episode_days` ≤ `14`) | `emit_advice:ordinary_illness_rate_65_percent` | `clm.medical_leave.medical_rates` | `active` |
| `rule.medical_leave.day15_gap.v1` | (`leave_reason_class` = `ordinary_illness` ȘI `episode_days` = `15`) | `require_confirmation:confirm_ordinary_illness_rate_for_day_15` | `clm.medical_leave.medical_day15_gap` | `in_review` |
| `rule.medical_leave.rate_75.v1` | (`leave_reason_class` = `ordinary_illness` ȘI `episode_days` > `15`) | `emit_advice:ordinary_illness_rate_75_percent` | `clm.medical_leave.medical_rates` | `active` |
| `rule.medical_leave.over_90_no_approval.v1` | (`cumulative_days_last_year` > `90` ȘI `has_expert_approval_after_day90` = `False`) | `include_requirement:medical_expert_approval_for_extension_after_day90`<br>`block:extension_after_day90_not_approved` | `clm.medical_leave.medical_duration` | `active` |
| `rule.medical_leave.over_183.v1` | `cumulative_days_last_year` > `183` | `block:ordinary_annual_duration_limit_exceeded` | `clm.medical_leave.medical_duration` | `active` |
| `rule.medical_leave.one_day_reduction.v1` | `one_day_reduction_exception_applies` = `False` | `emit_advice:temporary_one_day_reduction_2026_2027` | `clm.medical_leave.medical_one_day` | `active` |
| `rule.medical_leave.one_day_exception.v1` | `one_day_reduction_exception_applies` = `True` | `emit_advice:one_day_reduction_exception_to_be_documented` | `clm.medical_leave.medical_one_day` | `active` |

## Termene, praguri și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Stagiu minim — ruta obișnuită | 6 luni în ultimele 12 | `clm.medical_leave.medical_stage` |
| Predare certificat | până la data de 5 a lunii următoare | `clm.medical_leave.medical_delivery` |
| Transmitere angajator REGES | 3 zile lucrătoare de la înregistrare | `clm.medical_leave.medical_delivery` |
| Durată obișnuită maximă | 183 zile/an; aviz după ziua 90 | `clm.medical_leave.medical_duration` |
| Ziua 15 | needs_confirmation | `clm.medical_leave.medical_day15_gap` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.medical_leave.medical_stage` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/66305 |
| `clm.medical_leave.medical_no_stage` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/66305 |
| `clm.medical_leave.medical_certificate` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/66305 |
| `clm.medical_leave.medical_delivery` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/ajutor/intrebari-frecvente/ |
| `clm.medical_leave.medical_duration` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/66305 |
| `clm.medical_leave.medical_rates` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/66305 |
| `clm.medical_leave.medical_day15_gap` | `needs_confirmation` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/66305 |
| `clm.medical_leave.medical_one_day` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/66305 |
| `clm.medical_leave.medical_july_change` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/66305 |
