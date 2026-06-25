---
schema_version: "3.0.0"
batch_id: "batch10.hire_first_employee"
event_type_id: "ro.life.hire_first_employee"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "in_review"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.hire_first_employee` |
| Titlu | Angajarea primului salariat |
| Scop | Pregătește angajatorul, REGES, CIM, medicina muncii, SSM, salarizarea și raportarea. |
| Autoritate | Angajatorul, Inspecția Muncii / REGES-ONLINE, medicina muncii, ANAF și IGI pentru lucrători străini |
| Pilot local | Reguli naționale; serviciile teritoriale competente în Timiș pentru pilot |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `employer_entity_type` | enum | srl \| pfa \| other | da |
| `has_reges_access` | boolean | Angajatorul poate opera în REGES-ONLINE. | da |
| `candidate_scope` | enum | romanian_or_eu \| third_country | da |
| `third_country_work_right_ready` | boolean | Aviz sau excepție legală documentată, dacă este cazul. | da |
| `has_medical_aptitude` | boolean | Candidatul este declarat apt. | da |
| `cim_signed_before_start` | boolean | CIM scris și semnat la timp. | da |
| `cim_transmitted_before_start` | boolean | Transmiterea REGES este făcută la timp. | da |
| `employee_received_copy` | boolean | Salariatul a primit exemplarul CIM. | da |
| `ssm_risk_assessment_done` | boolean | Evaluarea riscurilor este realizată. | da |
| `prevention_plan_done` | boolean | Planul de prevenire și protecție este întocmit. | da |
| `ssm_service_arranged` | boolean | Activitățile de prevenire/protecție sunt organizate. | da |
| `ssm_training_done` | boolean | Instruirea salariatului este efectuată. | da |
| `payroll_setup_done` | boolean | Salarizarea și obligațiile declarative sunt configurate. | da |
| `d112_frequency_confirmed` | boolean | Frecvența și termenul D112 au fost confirmate pentru angajator. | da |
| `start_date_confirmed` | boolean | Data începerii este stabilită. | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.hire_first_employee.route.v1` | adevărat | `include_step:establish_first_employee_start_date`<br>`include_step:activate_reges_employer_access`<br>`include_step:complete_occupational_health_and_ssm_setup`<br>`include_step:sign_and_transmit_first_cim`<br>`include_step:configure_payroll_and_d112` | `clm.hire_first_employee.first_employee_reges`, `clm.hire_first_employee.medical_aptitude`, `clm.hire_first_employee.ssm_employer`, `clm.hire_first_employee.d112_current` | `active` |
| `rule.hire_first_employee.missing_start_date.v1` | `start_date_confirmed` = `False` | `include_requirement:confirmed_employment_start_date` | `clm.hire_first_employee.cim_written` | `active` |
| `rule.hire_first_employee.no_reges_access.v1` | `has_reges_access` = `False` | `include_requirement:reges_online_employer_access`<br>`include_step:obtain_reges_employer_access` | `clm.hire_first_employee.first_employee_reges` | `active` |
| `rule.hire_first_employee.no_medical.v1` | `has_medical_aptitude` = `False` | `include_requirement:occupational_medical_aptitude`<br>`block:candidate_not_cleared_for_start` | `clm.hire_first_employee.medical_aptitude` | `active` |
| `rule.hire_first_employee.no_cim.v1` | `cim_signed_before_start` = `False` | `include_requirement:written_signed_cim_before_start`<br>`block:first_employee_cim_missing` | `clm.hire_first_employee.cim_written` | `active` |
| `rule.hire_first_employee.no_transmission.v1` | `cim_transmitted_before_start` = `False` | `include_requirement:first_employee_reges_transmission_before_start`<br>`block:first_employee_reges_missing` | `clm.hire_first_employee.first_employee_reges`, `clm.hire_first_employee.cim_register` | `active` |
| `rule.hire_first_employee.no_copy.v1` | `employee_received_copy` = `False` | `include_requirement:signed_cim_copy_for_employee` | `clm.hire_first_employee.cim_copy` | `active` |
| `rule.hire_first_employee.no_risk_assessment.v1` | `ssm_risk_assessment_done` = `False` | `include_requirement:occupational_risk_assessment` | `clm.hire_first_employee.medical_risk_assessment`, `clm.hire_first_employee.ssm_employer` | `active` |
| `rule.hire_first_employee.no_prevention_plan.v1` | `prevention_plan_done` = `False` | `include_requirement:prevention_and_protection_plan` | `clm.hire_first_employee.ssm_plan` | `active` |
| `rule.hire_first_employee.no_ssm_service.v1` | `ssm_service_arranged` = `False` | `include_requirement:organised_prevention_and_protection_service` | `clm.hire_first_employee.ssm_employer` | `active` |
| `rule.hire_first_employee.no_training.v1` | `ssm_training_done` = `False` | `include_requirement:employee_ssm_training` | `clm.hire_first_employee.ssm_employer` | `active` |
| `rule.hire_first_employee.no_payroll.v1` | `payroll_setup_done` = `False` | `include_requirement:payroll_and_tax_reporting_setup` | `clm.hire_first_employee.d112_current` | `active` |
| `rule.hire_first_employee.d112_unconfirmed.v1` | `d112_frequency_confirmed` = `False` | `require_confirmation:confirm_d112_frequency_and_deadline` | `clm.hire_first_employee.d112_deadline_gap` | `in_review` |
| `rule.hire_first_employee.d112_current.v1` | `d112_frequency_confirmed` = `True` | `emit_advice:use_d112_version_valid_from_2026_01` | `clm.hire_first_employee.d112_current` | `active` |
| `rule.hire_first_employee.third_country_ready.v1` | (`candidate_scope` = `third_country` ȘI `third_country_work_right_ready` = `True`) | `emit_advice:retain_foreign_worker_authorisation_or_exemption`<br>`emit_advice:foreign_worker_medical_by_start` | `clm.hire_first_employee.third_country_ro_work`, `clm.hire_first_employee.foreign_medical` | `active` |
| `rule.hire_first_employee.third_country_not_ready.v1` | (`candidate_scope` = `third_country` ȘI `third_country_work_right_ready` = `False`) | `include_requirement:foreign_worker_employment_authorisation_or_exemption`<br>`block:foreign_worker_right_not_ready` | `clm.hire_first_employee.third_country_ro_work` | `active` |

## Termene, praguri și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Primul CIM în REGES | cel târziu în ziua anterioară începerii | `clm.hire_first_employee.first_employee_reges` |
| Aptitudine medicală | înaintea începerii muncii | `clm.hire_first_employee.medical_aptitude` |
| Evaluare și plan SSM | înainte/odată cu organizarea activității | `clm.hire_first_employee.ssm_plan` |
| D112 2026 | versiunea este verificată; frecvența necesită confirmare | `clm.hire_first_employee.d112_deadline_gap` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.hire_first_employee.first_employee_reges` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/ajutor/intrebari-frecvente/ |
| `clm.hire_first_employee.cim_written` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.hire_first_employee.cim_register` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.hire_first_employee.cim_copy` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.hire_first_employee.medical_aptitude` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.hire_first_employee.foreign_medical` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.hire_first_employee.third_country_ro_work` | `verified` | `national_operational` | https://igi.mai.gov.ro/obtinerea-avizului/ |
| `clm.hire_first_employee.ssm_employer` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/73772 |
| `clm.hire_first_employee.ssm_plan` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/73772 |
| `clm.hire_first_employee.medical_risk_assessment` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/82130 |
| `clm.hire_first_employee.d112_current` | `verified` | `national_operational` | https://static.anaf.ro/static/10/Anaf/Declaratii_R/112.html |
| `clm.hire_first_employee.d112_deadline_gap` | `needs_confirmation` | `national_operational` | https://static.anaf.ro/static/10/Anaf/Declaratii_R/112.html |
