---
schema_version: "3.0.0"
batch_id: "batch10.home_care_support"
event_type_id: "ro.life.home_care_support"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "in_review"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.home_care_support` |
| Titlu | Solicitarea concediului de îngrijitor |
| Scop | Modelează dreptul salariatului la cele 5 zile de îngrijitor și îl separă de urgența familială de 10 zile. |
| Autoritate | Angajatorul; documentarea medicală conform actului subsecvent aplicabil |
| Pilot local | Regulă națională, fără taxă sau canal UAT |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `is_employee` | boolean | Persoana solicitantă are calitatea de salariat. | da |
| `relationship` | enum | child \| parent \| spouse \| household_member \| other | da |
| `same_household` | boolean | Persoana îngrijită locuiește în aceeași gospodărie, când relația nu este ruda enumerată. | da |
| `serious_medical_problem_documented` | boolean | Problema medicală gravă este documentată. | da |
| `written_request_ready` | boolean | Cererea scrisă către angajator este pregătită. | da |
| `days_used_this_year` | integer | Zile de concediu de îngrijitor folosite în anul calendaristic. | da |
| `collective_agreement_extra_days` | boolean | Există zile suplimentare prevăzute de lege specială/contract colectiv. | da |
| `need_is_emergency_unforeseen` | boolean | Situația este o urgență familială neprevăzută, distinctă de concediul de îngrijitor. | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.home_care_support.not_employee.v1` | `is_employee` = `False` | `block:caregiver_leave_requires_employee_status` | `clm.home_care_support.caregiver_basic` | `active` |
| `rule.home_care_support.eligible_route.v1` | (`is_employee` = `True` ȘI (`relationship` în ['child', 'parent', 'spouse'] SAU (`relationship` = `household_member` ȘI `same_household` = `True`)) ȘI `days_used_this_year` < `5`) | `include_step:prepare_written_caregiver_leave_request`<br>`include_step:attach_medical_supporting_documents`<br>`include_step:submit_request_to_employer`<br>`emit_advice:caregiver_leave_paid_and_preserves_rights` | `clm.home_care_support.caregiver_basic`, `clm.home_care_support.caregiver_rights` | `active` |
| `rule.home_care_support.ineligible_relation.v1` | (`is_employee` = `True` ȘI `relationship` = `other`) | `block:relationship_not_in_verified_caregiver_scope` | `clm.home_care_support.caregiver_relatives`, `clm.home_care_support.caregiver_basic` | `active` |
| `rule.home_care_support.household_not_same.v1` | (`relationship` = `household_member` ȘI `same_household` = `False`) | `block:household_member_not_same_household` | `clm.home_care_support.caregiver_basic` | `active` |
| `rule.home_care_support.missing_medical_docs.v1` | `serious_medical_problem_documented` = `False` | `include_requirement:documents_supporting_serious_medical_problem`<br>`require_confirmation:confirm_caregiver_medical_documents` | `clm.home_care_support.caregiver_docs_gap` | `in_review` |
| `rule.home_care_support.missing_request.v1` | `written_request_ready` = `False` | `include_requirement:written_caregiver_leave_request` | `clm.home_care_support.caregiver_basic` | `active` |
| `rule.home_care_support.five_days_exhausted.v1` | (`days_used_this_year` ≥ `5` ȘI `collective_agreement_extra_days` = `False`) | `block:statutory_caregiver_days_exhausted` | `clm.home_care_support.caregiver_basic` | `active` |
| `rule.home_care_support.extra_days.v1` | (`days_used_this_year` ≥ `5` ȘI `collective_agreement_extra_days` = `True`) | `require_confirmation:confirm_collective_or_special_extra_caregiver_days` | `clm.home_care_support.caregiver_basic` | `in_review` |
| `rule.home_care_support.family_emergency.v1` | `need_is_emergency_unforeseen` = `True` | `emit_advice:distinct_family_emergency_absence_up_to_10_days` | `clm.home_care_support.family_emergency` | `active` |

## Termene, praguri și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Durată minimă legală | 5 zile lucrătoare/an | `clm.home_care_support.caregiver_basic` |
| Cerere | scrisă către angajator | `clm.home_care_support.caregiver_basic` |
| Persoane acoperite | copil, părinte, soț/soție sau persoană din aceeași gospodărie | `clm.home_care_support.caregiver_relatives` |
| Urgență familială distinctă | maximum 10 zile lucrătoare/an, cu recuperare | `clm.home_care_support.family_emergency` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.home_care_support.caregiver_basic` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.home_care_support.caregiver_rights` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.home_care_support.caregiver_relatives` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.home_care_support.caregiver_docs_gap` | `needs_confirmation` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.home_care_support.family_emergency` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
