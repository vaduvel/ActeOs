---
schema_version: "3.0.0"
batch_id: "batch08.land_split_merge"
event_type_id: "ro.life.land_split_merge"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "conflicting"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.land_split_merge` |
| Titlu | Dezlipirea sau alipirea terenului |
| Scop | Modelează fluxul cadastral întrerupt 2026, documentele OCPI și separă explicit tariful/termenul curent neconfirmat. |
| Autoritate națională / normativă | ANCPI; OCPI competent teritorial; notar public pentru actul autentic |
| Pilot local | Municipiul Timișoara / județul Timiș |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `jurisdiction_id` | enum | `ro.tm`, `other_county` | da |
| `operation` | enum | `split`, `merge` | da |
| `has_application` | boolean | `true`, `false` | da |
| `has_cadastral_documentation` | boolean | `true`, `false` | da |
| `has_authentic_act` | boolean | `true`, `false` | da |
| `has_fee_proof` | boolean | `true`, `false` | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.land_split_merge.flow.v1` | adevărat | `include_step:submit_cadastral_reception`<br>`include_step:obtain_reception_report_notation`<br>`include_step:execute_authentic_notarial_act`<br>`include_step:request_land_book_registration`<br>`emit_advice:interrupted_cadastral_flow` | `clm.land_split_merge.ancpi_2026_flow` | `active` |
| `rule.land_split_merge.operation_split.v1` | `operation` = `split` | `emit_advice:operation_split` | `clm.land_split_merge.ancpi_2026_flow` | `active` |
| `rule.land_split_merge.operation_merge.v1` | `operation` = `merge` | `emit_advice:operation_merge` | `clm.land_split_merge.ancpi_2026_flow` | `active` |
| `rule.land_split_merge.missing_application.v1` | `has_application` = `False` | `include_requirement:standard_ocpi_application` | `clm.land_split_merge.ocpi_docs` | `active` |
| `rule.land_split_merge.missing_cadastral_docs.v1` | `has_cadastral_documentation` = `False` | `include_requirement:cadastral_split_or_merge_documentation` | `clm.land_split_merge.ocpi_docs` | `active` |
| `rule.land_split_merge.missing_authentic_act.v1` | `has_authentic_act` = `False` | `include_requirement:authentic_notarial_act_after_reception` | `clm.land_split_merge.ancpi_2026_flow`, `clm.land_split_merge.ocpi_docs` | `active` |
| `rule.land_split_merge.missing_fee.v1` | `has_fee_proof` = `False` | `include_requirement:full_cadastral_tariff_payment_proof` | `clm.land_split_merge.ocpi_docs` | `active` |
| `rule.land_split_merge.fee_term_confirmation.v1` | adevărat | `require_confirmation:confirm_current_split_merge_tariff`<br>`require_confirmation:confirm_current_split_merge_term` | `clm.land_split_merge.ancpi_later_amendments`, `clm.land_split_merge.ocpi_old_tariffs`, `clm.land_split_merge.ocpi_old_terms` | `in_review` |
| `rule.land_split_merge.timis_channel.v1` | `jurisdiction_id` = `ro.tm` | `attach_channel:ocpi_timis_documents_and_service_info` | `clm.land_split_merge.ocpi_docs` | `active` |
| `rule.land_split_merge.other_county.v1` | `jurisdiction_id` ≠ `ro.tm` | `include_step:identify_competent_ocpi`<br>`require_confirmation:confirm_local_ocpi_channel`<br>`emit_advice:verified_with_local_gap` | `clm.land_split_merge.ocpi_docs` | `in_review` |

## Termene, taxe și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Ordine operații | recepție cadastrală → act autentic → înscriere CF | `clm.land_split_merge.ancpi_2026_flow` |
| Tarif și termen curent | `needs_confirmation` | `clm.land_split_merge.ancpi_later_amendments` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.land_split_merge.ancpi_2026_flow` | `verified` | `national_normative` | https://www.ancpi.ro/wp-content/uploads/2026/03/Ordin-nr.-293-din-2026.pdf |
| `clm.land_split_merge.ocpi_docs` | `verified` | `county` | https://tm.ancpi.ro/documente-necesare/ |
| `clm.land_split_merge.ancpi_later_amendments` | `verified` | `national_operational` | https://www.ancpi.ro/ordine-director-general/ |
| `clm.land_split_merge.ocpi_old_tariffs` | `expired` | `county` | https://tm.ancpi.ro/tarife-servicii/ |
| `clm.land_split_merge.ocpi_old_terms` | `expired` | `county` | https://tm.ancpi.ro/termene-servicii/ |
