---
schema_version: "3.0.0"
batch_id: "batch08.construction_start_notice"
event_type_id: "ro.life.construction_start_notice"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "verified_with_local_gap"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.construction_start_notice` |
| Titlu | Înștiințarea începerii lucrărilor |
| Scop | Separă obligația față de emitent de obligația față de inspectoratul teritorial și blochează începerea fără autorizație valabilă. |
| Autoritate națională / normativă | Autoritatea emitentă și inspectoratul teritorial în construcții |
| Pilot local | Municipiul Timișoara / județul Timiș |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `jurisdiction_id` | string | UAT-ul emitent al autorizației. | da |
| `permit_exists` | boolean | `true`, `false` | da |
| `permit_valid` | boolean | `true`, `false` | da |
| `start_date_known` | boolean | `true`, `false` | da |
| `issuer_notified` | boolean | `true`, `false` | da |
| `isc_notified` | boolean | `true`, `false` | da |
| `tax_regularization_applicable` | boolean | `true`, `false` | da |
| `tax_regularization_done` | boolean | `true`, `false` | da |
| `representative_used` | boolean | `true`, `false` | da |
| `power_of_attorney_available` | boolean | `true`, `false` | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.start_notice.no_permit.v1` | `permit_exists` = `False` | `block:no_building_permit`<br>`emit_warning:do_not_start_works` | `clm.construction_start.law50.notice_duty` | `active` |
| `rule.start_notice.invalid_permit.v1` | (`permit_exists` = `True` ȘI `permit_valid` = `False`) | `block:permit_not_valid`<br>`emit_warning:verify_extension_or_new_permit` | `clm.construction_start.law50.notice_duty` | `active` |
| `rule.start_notice.base.v1` | (`permit_exists` = `True` ȘI `permit_valid` = `True`) | `include_step:record_actual_start_date`<br>`include_step:verify_issuer_and_isc_notifications` | `clm.construction_start.law50.notice_duty` | `active` |
| `rule.start_notice.date_missing.v1` | ((`permit_exists` = `True` ȘI `permit_valid` = `True`) ȘI `start_date_known` = `False`) | `include_requirement:actual_construction_start_date` | `clm.construction_start.law50.notice_duty` | `active` |
| `rule.start_notice.issuer_missing_timisoara.v1` | ((`permit_exists` = `True` ȘI `permit_valid` = `True`) ȘI `jurisdiction_id` = `ro.tm.timisoara` ȘI `issuer_notified` = `False`) | `include_step:submit_start_notice_to_timisoara`<br>`include_requirement:standard_start_notice`<br>`include_requirement:building_permit_copy`<br>`include_requirement:identity_document`<br>`attach_channel:pmt_construction_start_notice_online` | `clm.construction_start.pmt.start_service`, `clm.construction_start.law50.notice_duty` | `active` |
| `rule.start_notice.issuer_missing_other_uat.v1` | ((`permit_exists` = `True` ȘI `permit_valid` = `True`) ȘI `jurisdiction_id` ≠ `ro.tm.timisoara` ȘI `issuer_notified` = `False`) | `include_step:identify_issuer_notice_channel`<br>`require_confirmation:confirm_local_issuer_start_notice_channel`<br>`emit_advice:verified_with_local_gap` | `clm.construction_start.law50.notice_duty`, `clm.construction_start.pmt.start_service` | `in_review` |
| `rule.start_notice.isc_missing.v1` | ((`permit_exists` = `True` ȘI `permit_valid` = `True`) ȘI `isc_notified` = `False`) | `include_step:submit_start_notice_to_territorial_isc`<br>`require_confirmation:confirm_current_isc_start_notice_channel` | `clm.construction_start.law50.notice_duty` | `in_review` |
| `rule.start_notice.tax_regularization.timisoara.v1` | ((`permit_exists` = `True` ȘI `permit_valid` = `True`) ȘI `jurisdiction_id` = `ro.tm.timisoara` ȘI `tax_regularization_applicable` = `True` ȘI `tax_regularization_done` = `False`) | `include_requirement:authorisation_fee_regularization_proof_if_applicable` | `clm.construction_start.pmt.start_service` | `active` |
| `rule.start_notice.tax_regularization.other_uat.v1` | ((`permit_exists` = `True` ȘI `permit_valid` = `True`) ȘI `jurisdiction_id` ≠ `ro.tm.timisoara` ȘI `tax_regularization_applicable` = `True` ȘI `tax_regularization_done` = `False`) | `require_confirmation:confirm_local_start_tax_regularization` | `clm.construction_start.pmt.start_service` | `in_review` |
| `rule.start_notice.power_of_attorney.timisoara.v1` | ((`permit_exists` = `True` ȘI `permit_valid` = `True`) ȘI `jurisdiction_id` = `ro.tm.timisoara` ȘI `representative_used` = `True` ȘI `power_of_attorney_available` = `False`) | `include_requirement:power_of_attorney` | `clm.construction_start.pmt.start_service` | `active` |
| `rule.start_notice.omission_warning.v1` | ((`permit_exists` = `True` ȘI `permit_valid` = `True`) ȘI (`issuer_notified` = `False` SAU `isc_notified` = `False`)) | `emit_warning:start_notice_omission_affects_duration`<br>`emit_warning:start_notice_omission_contravention` | `clm.construction_start.law50.omission_effects`, `clm.construction_start.law50.contravention` | `active` |
| `rule.start_notice.completed.v1` | ((`permit_exists` = `True` ȘI `permit_valid` = `True`) ȘI `start_date_known` = `True` ȘI `issuer_notified` = `True` ȘI `isc_notified` = `True`) | `emit_advice:both_start_notices_completed` | `clm.construction_start.law50.notice_duty` | `active` |

## Termene, taxe și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Destinatari | emitentul autorizației + inspectoratul teritorial | `clm.construction_start.law50.notice_duty` |
| Omiterea notificării | afectează durata de execuție și este contravenție | `clm.construction_start.law50.omission_effects` |
| Canal emitent Timișoara | `pmt_construction_start_notice_online` | `clm.construction_start.pmt.start_service` |
| Canal ISC curent | `needs_confirmation` | `clm.construction_start.law50.notice_duty` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.construction_start.law50.notice_duty` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.construction_start.law50.omission_effects` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.construction_start.law50.contravention` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.construction_start.pmt.start_service` | `verified` | `uat` | https://servicii.primariatm.ro/inceperea-lucrarilor |
