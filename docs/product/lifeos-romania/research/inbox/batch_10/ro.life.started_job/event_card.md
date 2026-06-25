---
schema_version: "3.0.0"
batch_id: "batch10.started_job"
event_type_id: "ro.life.started_job"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "verified_with_local_gap"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.started_job` |
| Titlu | Începerea unui loc de muncă în România |
| Scop | Verifică formalitățile esențiale înainte de prima zi de activitate. |
| Autoritate | Angajatorul, Inspecția Muncii / REGES-ONLINE și medicina muncii |
| Pilot local | România; suport local Timiș prin instituțiile teritoriale competente |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `worker_citizenship_scope` | enum | romanian_or_eu \| third_country | da |
| `third_country_work_right_ready` | boolean | Aviz sau excepție legală verificată, dacă este cazul. | da |
| `has_written_cim` | boolean | Contract semnat în scris înainte de începere. | da |
| `cim_transmitted_before_start` | boolean | Transmitere REGES cel târziu în ziua anterioară. | da |
| `received_cim_copy_before_start` | boolean | Exemplarul salariatului primit înainte de începere. | da |
| `has_medical_aptitude` | boolean | Certificat/fișă de aptitudine valabilă la data începerii. | da |
| `ssm_induction_completed` | boolean | Instruirea SSM efectuată înaintea activității. | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.started_job.route.v1` | adevărat | `include_step:review_employment_offer_and_terms`<br>`include_step:sign_written_employment_contract`<br>`include_step:complete_occupational_health_check`<br>`include_step:verify_reges_transmission`<br>`include_step:receive_employee_contract_copy`<br>`include_step:complete_ssm_induction` | `clm.started_job.cim_written`, `clm.started_job.cim_register`, `clm.started_job.medical_aptitude`, `clm.started_job.ssm_employer` | `active` |
| `rule.started_job.missing_written_cim.v1` | `has_written_cim` = `False` | `include_requirement:written_employment_contract_before_start`<br>`block:do_not_start_without_written_cim` | `clm.started_job.cim_written` | `active` |
| `rule.started_job.missing_reges_transmission.v1` | `cim_transmitted_before_start` = `False` | `include_requirement:reges_transmission_before_start`<br>`block:do_not_start_before_reges_transmission` | `clm.started_job.cim_register` | `active` |
| `rule.started_job.missing_employee_copy.v1` | `received_cim_copy_before_start` = `False` | `include_requirement:employee_copy_of_signed_cim`<br>`emit_warning:request_contract_copy_before_start` | `clm.started_job.cim_copy` | `active` |
| `rule.started_job.missing_medical_aptitude.v1` | `has_medical_aptitude` = `False` | `include_requirement:occupational_medical_aptitude`<br>`block:do_not_start_without_medical_aptitude` | `clm.started_job.medical_aptitude` | `active` |
| `rule.started_job.missing_ssm.v1` | `ssm_induction_completed` = `False` | `include_requirement:ssm_induction_and_instruction`<br>`block:do_not_start_without_ssm_induction` | `clm.started_job.ssm_employer` | `active` |
| `rule.started_job.third_country_ready.v1` | (`worker_citizenship_scope` = `third_country` ȘI `third_country_work_right_ready` = `True`) | `emit_advice:third_country_work_authorisation_or_exemption_verified`<br>`emit_advice:foreign_worker_medical_by_start_date` | `clm.started_job.third_country_ro_work`, `clm.started_job.foreign_medical` | `active` |
| `rule.started_job.third_country_not_ready.v1` | (`worker_citizenship_scope` = `third_country` ȘI `third_country_work_right_ready` = `False`) | `include_requirement:employment_authorisation_or_documented_exemption`<br>`block:third_country_work_right_not_ready` | `clm.started_job.third_country_ro_work` | `active` |

## Termene, praguri și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Contract scris | cel târziu în ziua anterioară începerii | `clm.started_job.cim_written` |
| Transmitere REGES | cel târziu în ziua anterioară începerii | `clm.started_job.cim_register` |
| Exemplar salariat | înainte de începerea activității | `clm.started_job.cim_copy` |
| Aptitudine medicală | obligatorie înainte de muncă | `clm.started_job.medical_aptitude` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.started_job.code_current` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.started_job.cim_written` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.started_job.cim_register` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.started_job.cim_copy` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.started_job.medical_aptitude` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.started_job.foreign_medical` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.started_job.ssm_employer` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/73772 |
| `clm.started_job.third_country_ro_work` | `verified` | `national_operational` | https://igi.mai.gov.ro/obtinerea-avizului/ |
