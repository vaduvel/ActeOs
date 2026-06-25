---
schema_version: "3.0.0"
batch_id: "batch08.house_extension"
event_type_id: "ro.life.house_extension"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "verified_with_local_gap"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.house_extension` |
| Titlu | Extinderea unei case |
| Scop | Confirmă că extinderea rămâne supusă autorizației și separă situația conformă RLU de cea care poate necesita documentație urbanistică suplimentară. |
| Autoritate națională / normativă | Autoritatea administrației publice competente potrivit Legii nr. 50/1991 |
| Pilot local | Municipiul Timișoara / județul Timiș |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `jurisdiction_id` | string | UAT-ul casei. | da |
| `is_extension` | boolean | `true`, `false` | da |
| `fits_local_urbanism` | boolean | `true`, `false` | da |
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
| `rule.house_extension.not_applicable.v1` | `is_extension` = `False` | `block:event_not_applicable`<br>`emit_advice:choose_correct_construction_event` | `clm.house_extension.law50.permit_scope` | `active` |
| `rule.house_extension.permit_route.v1` | `is_extension` = `True` | `include_step:obtain_urbanism_certificate`<br>`include_step:verify_local_urbanism_fit`<br>`include_step:complete_environmental_procedure`<br>`include_step:obtain_required_approvals`<br>`include_step:prepare_extension_dt`<br>`include_step:pay_authorisation_fee`<br>`include_step:submit_complete_extension_file`<br>`include_step:receive_building_permit`<br>`trigger_child_event:ro.life.building_permit`<br>`emit_warning:extension_requires_building_permit` | `clm.house_extension.law50.permit_scope`, `clm.house_extension.law50.procedure_docs` | `active` |
| `rule.house_extension.rlu_fit.v1` | (`is_extension` = `True` ȘI `fits_local_urbanism` = `True`) | `emit_advice:no_prior_planning_documentation_if_rlu_fit` | `clm.house_extension.law50.no_prior_planning_if_rlu` | `active` |
| `rule.house_extension.rlu_not_fit.v1` | (`is_extension` = `True` ȘI `fits_local_urbanism` = `False`) | `require_confirmation:confirm_required_planning_documentation`<br>`emit_warning:rlu_nonconformity` | `clm.house_extension.law50.no_prior_planning_if_rlu` | `in_review` |
| `rule.house_extension.missing_real_right.v1` | (`is_extension` = `True` ȘI `has_real_right` = `False`) | `include_requirement:proof_of_title_or_real_right` | `clm.house_extension.law50.required_docs` | `active` |
| `rule.house_extension.missing_cu.v1` | (`is_extension` = `True` ȘI `has_urbanism_certificate` = `False`) | `include_requirement:urbanism_certificate` | `clm.house_extension.law50.required_docs` | `active` |
| `rule.house_extension.missing_cadastral.v1` | (`is_extension` = `True` ȘI `cadastral_evidence_requirement_satisfied` = `False`) | `include_requirement:current_cadastral_plan_and_land_book_extract_if_applicable` | `clm.house_extension.law50.required_docs` | `active` |
| `rule.house_extension.missing_dt.v1` | (`is_extension` = `True` ȘI `has_dt` = `False`) | `include_requirement:technical_documentation_for_extension` | `clm.house_extension.law50.required_docs` | `active` |
| `rule.house_extension.missing_approvals.v1` | (`is_extension` = `True` ȘI `approvals_requirement_satisfied` = `False`) | `include_requirement:approvals_and_agreements_from_urbanism_certificate` | `clm.house_extension.law50.required_docs` | `active` |
| `rule.house_extension.missing_environment.v1` | (`is_extension` = `True` ȘI `environmental_requirement_satisfied` = `False`) | `include_requirement:environmental_authority_act_if_applicable` | `clm.house_extension.law50.required_docs` | `active` |
| `rule.house_extension.missing_fee.v1` | (`is_extension` = `True` ȘI `has_fee_proof` = `False`) | `include_requirement:authorisation_fee_payment_proof` | `clm.house_extension.law50.required_docs` | `active` |
| `rule.house_extension.inconsistent_complete_file.v1` | (`is_extension` = `True` ȘI `application_complete` = `True` ȘI (`has_real_right` = `False` SAU `has_urbanism_certificate` = `False` SAU `cadastral_evidence_requirement_satisfied` = `False` SAU `has_dt` = `False` SAU `approvals_requirement_satisfied` = `False` SAU `environmental_requirement_satisfied` = `False` SAU `has_fee_proof` = `False`)) | `override_rule:rule.house_extension.complete_file.v1`<br>`block:inconsistent_complete_file` | `clm.house_extension.law50.required_docs`, `clm.house_extension.law50.procedure_docs` | `active` |
| `rule.house_extension.complete_file.v1` | (`is_extension` = `True` ȘI `application_complete` = `True`) | `emit_advice:extension_decision_max_30_calendar_days` | `clm.house_extension.law50.procedure_docs` | `active` |
| `rule.house_extension.incomplete_file.v1` | (`is_extension` = `True` ȘI `application_complete` = `False`) | `emit_advice:incomplete_notice_5_working_days`<br>`emit_advice:supplement_window_max_3_months` | `clm.house_extension.law50.incomplete` | `active` |
| `rule.house_extension.protected.v1` | (`is_extension` = `True` ȘI `protected_area` = `True`) | `include_requirement:specific_heritage_and_protected_area_approvals` | `clm.house_extension.law50.protected` | `active` |
| `rule.house_extension.validity.v1` | `is_extension` = `True` | `emit_advice:start_validity_max_24_months`<br>`emit_advice:extension_request_45_working_days_before` | `clm.house_extension.law50.validity` | `active` |
| `rule.house_extension.timisoara_channel_gap.v1` | (`is_extension` = `True` ȘI `jurisdiction_id` = `ro.tm.timisoara`) | `emit_advice:timisoara_archived_permit_service`<br>`require_confirmation:confirm_current_timisoara_extension_submission_channel` | `clm.house_extension.pmt.permit_page_expired` | `in_review` |
| `rule.house_extension.other_uat.v1` | (`is_extension` = `True` ȘI `jurisdiction_id` ≠ `ro.tm.timisoara`) | `include_step:identify_authorising_local_authority`<br>`require_confirmation:confirm_local_extension_submission_channel`<br>`emit_advice:verified_with_local_gap` | `clm.house_extension.law50.procedure_docs` | `in_review` |
| `rule.house_extension.fee_gap.v1` | `is_extension` = `True` | `require_confirmation:confirm_current_local_extension_fee_amount` | `clm.house_extension.law50.required_docs` | `in_review` |

## Termene, taxe și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Autorizație | obligatorie pentru extindere | `clm.house_extension.law50.permit_scope` |
| Fără documentație urbanistică prealabilă | posibil numai dacă propunerea respectă RLU | `clm.house_extension.law50.no_prior_planning_if_rlu` |
| Termen dosar complet | `maxim 30 zile` | `clm.house_extension.law50.procedure_docs` |
| Canal Timișoara 2026 | `needs_confirmation` | `clm.house_extension.pmt.permit_page_expired` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.house_extension.law50.current` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.house_extension.law50.permit_scope` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.house_extension.law50.procedure_docs` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.house_extension.law50.required_docs` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.house_extension.law50.incomplete` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.house_extension.law50.validity` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.house_extension.law50.protected` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.house_extension.law50.no_prior_planning_if_rlu` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.house_extension.pmt.permit_page_expired` | `expired` | `uat` | https://servicii.primariatm.ro/autorizatie-construire-desfiintare |
