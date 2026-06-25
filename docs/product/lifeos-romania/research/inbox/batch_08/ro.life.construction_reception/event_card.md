---
schema_version: "3.0.0"
batch_id: "batch08.construction_reception"
event_type_id: "ro.life.construction_reception"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "verified_with_local_gap"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.construction_reception` |
| Titlu | Recepția construcției |
| Scop | Modelează recepția la terminarea lucrărilor, suspendarea/respingerea, folosirea construcției și recepția finală după garanție. |
| Autoritate națională / normativă | Investitor/proprietar, comisia de recepție, ISC și autoritatea emitentă, potrivit Regulamentului de recepție |
| Pilot local | Municipiul Timișoara / județul Timiș |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `jurisdiction_id` | string | UAT-ul emitent al autorizației. | da |
| `works_completed` | boolean | `true`, `false` | da |
| `executor_notified_investor` | boolean | `true`, `false` | da |
| `reception_decision` | enum | `not_started`, `suspended`, `admitted`, `rejected` | da |
| `technical_book_complete` | boolean | `true`, `false` | da |
| `permit_and_project_docs_complete` | boolean | `true`, `false` | da |
| `isc_payment_confirmation_available` | boolean | `true`, `false` | da |
| `energy_certificate_applicable` | boolean | `true`, `false` | da |
| `energy_certificate_available` | boolean | `true`, `false` | da |
| `tax_regularization_applicable` | boolean | `true`, `false` | da |
| `tax_regularization_proof_available` | boolean | `true`, `false` | da |
| `designer_and_site_manager_reports_available` | boolean | `true`, `false` | da |
| `warranty_expired` | boolean | `true`, `false` | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.reception.not_completed.v1` | `works_completed` = `False` | `block:works_not_completed`<br>`emit_advice:complete_works_before_reception` | `clm.construction_reception.regulation.general` | `active` |
| `rule.reception.completed_route.v1` | `works_completed` = `True` | `include_step:executor_notifies_completion_in_writing`<br>`include_step:organise_reception_at_completion` | `clm.construction_reception.regulation.general`, `clm.construction_reception.regulation.notifications` | `active` |
| `rule.reception.executor_notice_missing.v1` | (`works_completed` = `True` ȘI `executor_notified_investor` = `False`) | `include_requirement:written_executor_completion_notice`<br>`include_step:obtain_executor_completion_notice` | `clm.construction_reception.regulation.notifications` | `active` |
| `rule.reception.not_started.v1` | (`works_completed` = `True` ȘI `reception_decision` = `not_started`) | `include_step:investor_requests_representatives_within_5_days`<br>`include_step:set_reception_date_and_place`<br>`include_step:collect_participant_responses`<br>`include_step:appoint_reception_commission`<br>`emit_advice:participant_response_10_days`<br>`emit_advice:commission_appointment_max_3_days` | `clm.construction_reception.regulation.notifications` | `active` |
| `rule.reception.missing_permit_project_docs.v1` | (`works_completed` = `True` ȘI `permit_and_project_docs_complete` = `False`) | `include_requirement:permit_project_execution_and_as_built_documents` | `clm.construction_reception.regulation.documents` | `active` |
| `rule.reception.missing_technical_book.v1` | (`works_completed` = `True` ȘI `technical_book_complete` = `False`) | `include_requirement:complete_technical_book` | `clm.construction_reception.regulation.documents` | `active` |
| `rule.reception.missing_isc_payment.v1` | (`works_completed` = `True` ȘI `isc_payment_confirmation_available` = `False`) | `include_requirement:isc_payment_confirmation` | `clm.construction_reception.regulation.documents` | `active` |
| `rule.reception.missing_energy_certificate.v1` | (`works_completed` = `True` ȘI `energy_certificate_applicable` = `True` ȘI `energy_certificate_available` = `False`) | `include_requirement:energy_performance_certificate` | `clm.construction_reception.regulation.documents` | `active` |
| `rule.reception.suspended.v1` | `reception_decision` = `suspended` | `include_step:remedy_reception_defects_and_missing_documents`<br>`emit_warning:reception_suspended`<br>`emit_advice:suspension_communication_max_3_working_days`<br>`emit_advice:remediation_max_90_days`<br>`emit_advice:possible_external_factor_extension_max_90_days`<br>`emit_warning:do_not_use_before_admission` | `clm.construction_reception.regulation.suspension`, `clm.construction_reception.regulation.use_after_admission` | `active` |
| `rule.reception.rejected.v1` | `reception_decision` = `rejected` | `include_step:remedy_rejection_causes`<br>`include_step:restart_reception_after_remediation`<br>`emit_warning:reception_rejected` | `clm.construction_reception.regulation.suspension`, `clm.construction_reception.regulation.use_after_admission` | `active` |
| `rule.reception.admitted.v1` | `reception_decision` = `admitted` | `include_step:investor_approves_and_signs_minutes_within_3_days`<br>`include_step:communicate_reception_minutes_within_5_days`<br>`include_step:take_over_construction`<br>`include_step:obtain_use_authorisations_if_required`<br>`emit_advice:use_only_after_admitted_reception` | `clm.construction_reception.regulation.decision`, `clm.construction_reception.regulation.use_after_admission` | `active` |
| `rule.reception.tax_regularization_missing.v1` | (`reception_decision` = `admitted` ȘI `tax_regularization_applicable` = `True` ȘI `tax_regularization_proof_available` = `False`) | `include_requirement:authorisation_fee_regularization_proof` | `clm.construction_reception.regulation.documents`, `clm.construction_reception.pmt.finalization` | `active` |
| `rule.reception.final.v1` | (`reception_decision` = `admitted` ȘI `warranty_expired` = `True`) | `include_step:organise_final_reception_within_10_days_after_warranty`<br>`emit_advice:final_reception_after_warranty` | `clm.construction_reception.regulation.decision` | `active` |
| `rule.reception.timisoara_finalization.v1` | (`jurisdiction_id` = `ro.tm.timisoara` ȘI `reception_decision` = `admitted`) | `include_step:submit_timisoara_work_finalization_file`<br>`include_requirement:building_permit_copy`<br>`include_requirement:reception_minutes`<br>`attach_channel:pmt_construction_finalization_online` | `clm.construction_reception.pmt.finalization` | `active` |
| `rule.reception.timisoara_reports_missing.v1` | (`jurisdiction_id` = `ro.tm.timisoara` ȘI `reception_decision` = `admitted` ȘI `designer_and_site_manager_reports_available` = `False`) | `include_requirement:designer_and_site_manager_completion_reports` | `clm.construction_reception.pmt.finalization` | `active` |
| `rule.reception.other_uat_finalization.v1` | (`jurisdiction_id` ≠ `ro.tm.timisoara` ȘI `reception_decision` = `admitted`) | `include_step:identify_local_post_reception_procedure`<br>`require_confirmation:confirm_local_post_reception_finalization`<br>`emit_advice:verified_with_local_gap` | `clm.construction_reception.pmt.finalization` | `in_review` |

## Termene, taxe și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Solicitarea reprezentanților | `5 zile` de la comunicarea terminării | `clm.construction_reception.regulation.notifications` |
| Remediere după suspendare | `maxim 90 zile` + posibil max. 90 zile | `clm.construction_reception.regulation.suspension` |
| Semnarea hotărârii | `3 zile` | `clm.construction_reception.regulation.decision` |
| Recepția finală | `maxim 10 zile` după expirarea garanției | `clm.construction_reception.regulation.decision` |
| Post-recepție Timișoara | `pmt_construction_finalization_online` | `clm.construction_reception.pmt.finalization` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.construction_reception.regulation.general` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocumentAfis/188977 |
| `clm.construction_reception.regulation.use_after_admission` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocumentAfis/188977 |
| `clm.construction_reception.regulation.notifications` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocumentAfis/188977 |
| `clm.construction_reception.regulation.documents` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocumentAfis/188977 |
| `clm.construction_reception.regulation.suspension` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocumentAfis/188977 |
| `clm.construction_reception.regulation.decision` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocumentAfis/188977 |
| `clm.construction_reception.pmt.finalization` | `verified` | `uat` | https://servicii.primariatm.ro/finalizarea-lucrarilor |
