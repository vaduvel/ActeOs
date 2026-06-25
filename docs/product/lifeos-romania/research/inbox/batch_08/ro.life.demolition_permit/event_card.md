---
schema_version: "3.0.0"
batch_id: "batch08.demolition_permit"
event_type_id: "ro.life.demolition_permit"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "verified_with_local_gap"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.demolition_permit` |
| Titlu | Obținerea autorizației de desființare |
| Scop | Modelează autorizarea demolării/dezafectării și cazul combinat cu o construcție nouă, fără a presupune taxa sau canalul local. |
| Autoritate națională / normativă | Autoritatea administrației publice competente potrivit Legii nr. 50/1991 |
| Pilot local | Municipiul Timișoara / județul Timiș |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `jurisdiction_id` | string | UAT-ul competent; pilot `ro.tm.timisoara`. | da |
| `demolition_scope` | enum | `partial`, `total`, `decommission`, `disassembly` | da |
| `replacement_building_planned` | boolean | `true`, `false` | da |
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
| `rule.demolition_permit.route.v1` | `demolition_scope` în [partial, total, decommission, disassembly] | `include_step:obtain_urbanism_certificate`<br>`include_step:complete_environmental_procedure`<br>`include_step:obtain_required_approvals`<br>`include_step:prepare_demolition_technical_documentation`<br>`include_step:pay_authorisation_fee`<br>`include_step:submit_demolition_permit_file`<br>`include_step:receive_demolition_permit`<br>`emit_warning:do_not_demolish_before_permit` | `clm.demolition_permit.law50.demolition_required`, `clm.demolition_permit.law50.docs_term` | `active` |
| `rule.demolition_permit.combined.v1` | `replacement_building_planned` = `True` | `emit_advice:single_combined_authorisation`<br>`emit_advice:only_building_fee_for_combined_case`<br>`trigger_child_event:ro.life.building_permit` | `clm.demolition_permit.law50.combined_authorisation` | `active` |
| `rule.demolition_permit.missing_real_right.v1` | `has_real_right` = `False` | `include_requirement:proof_of_title_or_real_right` | `clm.demolition_permit.law50.docs_term` | `active` |
| `rule.demolition_permit.missing_cu.v1` | `has_urbanism_certificate` = `False` | `include_requirement:urbanism_certificate` | `clm.demolition_permit.law50.docs_term` | `active` |
| `rule.demolition_permit.missing_cadastral.v1` | `cadastral_evidence_requirement_satisfied` = `False` | `include_requirement:current_cadastral_plan_and_land_book_extract_if_applicable` | `clm.demolition_permit.law50.docs_term` | `active` |
| `rule.demolition_permit.missing_dt.v1` | `has_dt` = `False` | `include_requirement:technical_documentation_for_demolition` | `clm.demolition_permit.law50.docs_term` | `active` |
| `rule.demolition_permit.missing_approvals.v1` | `approvals_requirement_satisfied` = `False` | `include_requirement:approvals_and_agreements_from_urbanism_certificate` | `clm.demolition_permit.law50.docs_term` | `active` |
| `rule.demolition_permit.missing_environment.v1` | `environmental_requirement_satisfied` = `False` | `include_requirement:environmental_authority_act_if_applicable` | `clm.demolition_permit.law50.docs_term` | `active` |
| `rule.demolition_permit.missing_fee.v1` | `has_fee_proof` = `False` | `include_requirement:authorisation_fee_payment_proof` | `clm.demolition_permit.law50.docs_term` | `active` |
| `rule.demolition_permit.inconsistent_complete_file.v1` | (`application_complete` = `True` ȘI (`has_real_right` = `False` SAU `has_urbanism_certificate` = `False` SAU `cadastral_evidence_requirement_satisfied` = `False` SAU `has_dt` = `False` SAU `approvals_requirement_satisfied` = `False` SAU `environmental_requirement_satisfied` = `False` SAU `has_fee_proof` = `False`)) | `override_rule:rule.demolition_permit.complete_file.v1`<br>`block:inconsistent_complete_file` | `clm.demolition_permit.law50.docs_term` | `active` |
| `rule.demolition_permit.complete_file.v1` | `application_complete` = `True` | `emit_advice:demolition_decision_max_30_calendar_days` | `clm.demolition_permit.law50.docs_term` | `active` |
| `rule.demolition_permit.incomplete_file.v1` | `application_complete` = `False` | `emit_advice:incomplete_notice_5_working_days`<br>`emit_advice:supplement_window_max_3_months` | `clm.demolition_permit.law50.incomplete` | `active` |
| `rule.demolition_permit.protected.v1` | `protected_area` = `True` | `include_requirement:specific_heritage_and_protected_area_approvals`<br>`emit_warning:protected_demolition_special_route` | `clm.demolition_permit.law50.protected` | `active` |
| `rule.demolition_permit.timisoara_channel_gap.v1` | `jurisdiction_id` = `ro.tm.timisoara` | `emit_advice:timisoara_archived_permit_service`<br>`require_confirmation:confirm_current_timisoara_demolition_submission_channel` | `clm.demolition_permit.pmt.permit_page_expired` | `in_review` |
| `rule.demolition_permit.other_uat.v1` | `jurisdiction_id` ≠ `ro.tm.timisoara` | `include_step:identify_authorising_local_authority`<br>`require_confirmation:confirm_local_demolition_submission_channel`<br>`emit_advice:verified_with_local_gap` | `clm.demolition_permit.law50.demolition_required` | `in_review` |
| `rule.demolition_permit.fee_amount_gap.v1` | adevărat | `require_confirmation:confirm_current_local_demolition_fee_amount` | `clm.demolition_permit.law50.combined_authorisation`, `clm.demolition_permit.law50.docs_term` | `in_review` |

## Termene, taxe și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Necesitatea autorizației | înainte de demolare/desființare | `clm.demolition_permit.law50.demolition_required` |
| Caz demolare + construcție nouă | o singură autorizație; numai taxa de construire | `clm.demolition_permit.law50.combined_authorisation` |
| Termen dosar complet | `maxim 30 zile` | `clm.demolition_permit.law50.docs_term` |
| Canal Timișoara 2026 | `needs_confirmation` | `clm.demolition_permit.pmt.permit_page_expired` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.demolition_permit.law50.current` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.demolition_permit.law50.demolition_required` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.demolition_permit.law50.combined_authorisation` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.demolition_permit.law50.docs_term` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.demolition_permit.law50.incomplete` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.demolition_permit.law50.protected` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.demolition_permit.pmt.permit_page_expired` | `expired` | `uat` | https://servicii.primariatm.ro/autorizatie-construire-desfiintare |
