---
schema_version: "3.0.0"
batch_id: "batch08.building_permit"
event_type_id: "ro.life.building_permit"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "verified_with_local_gap"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.building_permit` |
| Titlu | Obținerea autorizației de construire |
| Scop | Modelează traseul național al autorizației, dosarul, termenele și limitele de valabilitate; canalul și taxa locală rămân controlate prin confirmare. |
| Autoritate națională / normativă | Autoritatea administrației publice competente potrivit Legii nr. 50/1991 |
| Pilot local | Municipiul Timișoara / județul Timiș |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `jurisdiction_id` | string | UAT-ul competent; pilot `ro.tm.timisoara`. | da |
| `work_scope` | enum | `new_building`, `reconstruction`, `consolidation`, `modification`, `extension`, `rehabilitation`, `change_of_use_with_works`, `repair_not_exempt` | da |
| `has_real_right` | boolean | `true`, `false` | da |
| `has_urbanism_certificate` | boolean | `true`, `false` | da |
| `cadastral_evidence_requirement_satisfied` | boolean | `true`, `false` | da |
| `has_dt` | boolean | `true`, `false` | da |
| `approvals_requirement_satisfied` | boolean | `true`, `false` | da |
| `environmental_requirement_satisfied` | boolean | `true`, `false` | da |
| `has_fee_proof` | boolean | `true`, `false` | da |
| `protected_area` | boolean | `true`, `false` | da |
| `application_complete` | boolean | `true`, `false` | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.building_permit.route.v1` | `work_scope` în [new_building, reconstruction, consolidation, modification, extension, rehabilitation, change_of_use_with_works, repair_not_exempt] | `include_step:obtain_urbanism_certificate`<br>`include_step:complete_environmental_procedure`<br>`include_step:obtain_required_approvals`<br>`include_step:prepare_technical_documentation_dt`<br>`include_step:pay_authorisation_fee`<br>`include_step:submit_complete_permit_file`<br>`include_step:receive_building_permit`<br>`emit_warning:do_not_start_before_permit` | `clm.building_permit.law50.permit_scope`, `clm.building_permit.law50.procedure_docs` | `active` |
| `rule.building_permit.missing_real_right.v1` | `has_real_right` = `False` | `include_requirement:proof_of_title_or_real_right` | `clm.building_permit.law50.required_docs` | `active` |
| `rule.building_permit.missing_cu.v1` | `has_urbanism_certificate` = `False` | `include_requirement:urbanism_certificate` | `clm.building_permit.law50.required_docs` | `active` |
| `rule.building_permit.missing_cadastral.v1` | `cadastral_evidence_requirement_satisfied` = `False` | `include_requirement:current_cadastral_plan_and_land_book_extract_if_applicable` | `clm.building_permit.law50.required_docs` | `active` |
| `rule.building_permit.missing_dt.v1` | `has_dt` = `False` | `include_requirement:technical_documentation_for_authorisation` | `clm.building_permit.law50.required_docs` | `active` |
| `rule.building_permit.missing_approvals.v1` | `approvals_requirement_satisfied` = `False` | `include_requirement:approvals_and_agreements_from_urbanism_certificate` | `clm.building_permit.law50.required_docs` | `active` |
| `rule.building_permit.missing_environment.v1` | `environmental_requirement_satisfied` = `False` | `include_requirement:environmental_authority_act_if_applicable` | `clm.building_permit.law50.required_docs` | `active` |
| `rule.building_permit.missing_fee_proof.v1` | `has_fee_proof` = `False` | `include_requirement:authorisation_fee_payment_proof` | `clm.building_permit.law50.required_docs` | `active` |
| `rule.building_permit.inconsistent_complete_file.v1` | (`application_complete` = `True` ȘI (`has_real_right` = `False` SAU `has_urbanism_certificate` = `False` SAU `cadastral_evidence_requirement_satisfied` = `False` SAU `has_dt` = `False` SAU `approvals_requirement_satisfied` = `False` SAU `environmental_requirement_satisfied` = `False` SAU `has_fee_proof` = `False`)) | `override_rule:rule.building_permit.complete_file.v1`<br>`block:inconsistent_complete_file` | `clm.building_permit.law50.required_docs`, `clm.building_permit.law50.procedure_docs` | `active` |
| `rule.building_permit.complete_file.v1` | `application_complete` = `True` | `emit_advice:permit_decision_max_30_calendar_days` | `clm.building_permit.law50.procedure_docs` | `active` |
| `rule.building_permit.incomplete_file.v1` | `application_complete` = `False` | `emit_advice:incomplete_notice_5_working_days`<br>`emit_advice:supplement_window_max_3_months` | `clm.building_permit.law50.incomplete` | `active` |
| `rule.building_permit.protected.v1` | `protected_area` = `True` | `include_requirement:specific_heritage_and_protected_area_approvals`<br>`emit_warning:protected_area_special_route` | `clm.building_permit.law50.protected` | `active` |
| `rule.building_permit.validity.v1` | adevărat | `emit_advice:start_validity_max_24_months`<br>`emit_advice:extension_request_45_working_days_before`<br>`emit_advice:single_free_extension_max_24_months` | `clm.building_permit.law50.validity` | `active` |
| `rule.building_permit.timisoara_channel_gap.v1` | `jurisdiction_id` = `ro.tm.timisoara` | `emit_advice:timisoara_archived_permit_service`<br>`require_confirmation:confirm_current_timisoara_permit_submission_channel` | `clm.building_permit.pmt.permit_page_expired` | `in_review` |
| `rule.building_permit.other_uat_channel.v1` | `jurisdiction_id` ≠ `ro.tm.timisoara` | `include_step:identify_authorising_local_authority`<br>`require_confirmation:confirm_local_permit_submission_channel`<br>`emit_advice:verified_with_local_gap` | `clm.building_permit.law50.procedure_docs` | `in_review` |
| `rule.building_permit.fee_amount_gap.v1` | adevărat | `require_confirmation:confirm_current_local_permit_fee_amount` | `clm.building_permit.law50.required_docs` | `in_review` |

## Termene, taxe și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Emiterea după dosar complet | `maxim 30 zile` | `clm.building_permit.law50.procedure_docs` |
| Notificare dosar incomplet | `5 zile lucrătoare` | `clm.building_permit.law50.incomplete` |
| Valabilitate pentru începere | `maxim 24 luni` | `clm.building_permit.law50.validity` |
| Canal Timișoara 2026 | `needs_confirmation` | `clm.building_permit.pmt.permit_page_expired` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.building_permit.law50.current` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.building_permit.law50.permit_scope` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.building_permit.law50.procedure_docs` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.building_permit.law50.required_docs` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.building_permit.law50.incomplete` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.building_permit.law50.validity` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.building_permit.law50.protected` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.building_permit.pmt.permit_page_expired` | `expired` | `uat` | https://servicii.primariatm.ro/autorizatie-construire-desfiintare |
