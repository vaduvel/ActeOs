---
schema_version: "3.0.0"
batch_id: "batch08.renovation_authorisation_check"
event_type_id: "ro.life.renovation_authorisation_check"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "verified_with_local_gap"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.renovation_authorisation_check` |
| Titlu | Verificarea necesității autorizației pentru renovare |
| Scop | Separă excepțiile art. 11 de lucrările care depășesc excepția și tratează distinct zonele protejate și monumentele. |
| Autoritate națională / normativă | Autoritatea competentă potrivit Legii nr. 50/1991; autoritățile de patrimoniu când este cazul |
| Pilot local | Municipiul Timișoara / județul Timiș |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `jurisdiction_id` | string | UAT-ul imobilului. | da |
| `work_kind` | enum | `interior_finishes`, `fence_repair`, `roof_repair`, `exterior_finishes`, `internal_installations`, `external_joinery`, `light_partition`, `energy_rehabilitation_small_house`, `change_of_use_without_permit_work`, `other` | da |
| `changes_structure` | boolean | `true`, `false` | da |
| `changes_architectural_appearance` | boolean | `true`, `false` | da |
| `protected_status` | enum | `none`, `protected_zone_non_monument`, `monument_or_architectural_value` | da |
| `preserves_specific_conditions` | boolean | `true`, `false` | da |
| `local_urbanism_compliant` | boolean | `true`, `false` | da |
| `wants_official_position` | boolean | `true`, `false` | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.renovation.no_permit.general.v1` | (`work_kind` în [interior_finishes, fence_repair, roof_repair, exterior_finishes, internal_installations, external_joinery, light_partition, energy_rehabilitation_small_house] ȘI `changes_structure` = `False` ȘI `changes_architectural_appearance` = `False` ȘI `protected_status` = `none` ȘI `preserves_specific_conditions` = `True`) | `include_step:document_art11_assessment`<br>`emit_advice:permit_not_required_under_art11` | `clm.renovation_check.law50.general_exemption`, `clm.renovation_check.law50.listed_works`, `clm.renovation_check.law50.energy_change_use` | `active` |
| `rule.renovation.no_permit.change_use.v1` | (`work_kind` = `change_of_use_without_permit_work` ȘI `changes_structure` = `False` ȘI `changes_architectural_appearance` = `False` ȘI `protected_status` = `none` ȘI `preserves_specific_conditions` = `True` ȘI `local_urbanism_compliant` = `True`) | `include_step:document_change_of_use_assessment`<br>`emit_advice:change_of_use_no_permit_if_no_authorised_works` | `clm.renovation_check.law50.energy_change_use` | `active` |
| `rule.renovation.protected_zone_strict_exemption.v1` | (`protected_status` = `protected_zone_non_monument` ȘI `work_kind` în [interior_finishes, fence_repair, roof_repair, exterior_finishes, internal_installations, external_joinery, light_partition, energy_rehabilitation_small_house] ȘI `changes_structure` = `False` ȘI `changes_architectural_appearance` = `False` ȘI `preserves_specific_conditions` = `True`) | `include_step:document_protected_zone_art11_assessment`<br>`emit_advice:protected_zone_exemption_strict_conditions`<br>`require_confirmation:confirm_protected_zone_art11_exemption` | `clm.renovation_check.law50.protected_nonmonument` | `in_review` |
| `rule.renovation.monument_notice.v1` | `protected_status` = `monument_or_architectural_value` | `include_step:notify_local_authority_before_works`<br>`include_step:notify_deconcentrated_culture_service`<br>`include_requirement:written_heritage_agreement`<br>`emit_advice:heritage_agreement_max_30_days`<br>`emit_warning:do_not_treat_as_ordinary_art11_exemption` | `clm.renovation_check.law50.monument_notice` | `active` |
| `rule.renovation.permit_required.v1` | (`changes_structure` = `True` SAU `changes_architectural_appearance` = `True` SAU `work_kind` = `other` SAU `preserves_specific_conditions` = `False` SAU (`work_kind` = `change_of_use_without_permit_work` ȘI `local_urbanism_compliant` = `False`)) | `include_step:start_building_permit_route`<br>`trigger_child_event:ro.life.building_permit`<br>`emit_warning:permit_likely_required` | `clm.renovation_check.law50.general_exemption`, `clm.renovation_check.law50.energy_change_use` | `active` |
| `rule.renovation.timisoara_official_position.v1` | (`jurisdiction_id` = `ro.tm.timisoara` ȘI `wants_official_position` = `True`) | `include_step:prepare_art11_local_request`<br>`include_requirement:art11_standard_request`<br>`include_requirement:title_document`<br>`include_requirement:land_book_extract_max_30_days`<br>`include_requirement:site_plan_photos_and_intervention_proposal`<br>`attach_channel:pmt_art11_online_service` | `clm.renovation_check.pmt.art11_service` | `active` |
| `rule.renovation.other_uat_official_position.v1` | (`jurisdiction_id` ≠ `ro.tm.timisoara` ȘI `wants_official_position` = `True`) | `include_step:identify_local_art11_contact`<br>`require_confirmation:confirm_local_art11_position_procedure`<br>`emit_advice:verified_with_local_gap` | `clm.renovation_check.pmt.art11_service` | `in_review` |

## Termene, taxe și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Test general fără autorizație | lucrare enumerată + fără structură/aspect modificat + condiții păstrate | `clm.renovation_check.law50.general_exemption` |
| Monument / valoare arhitecturală | notificări și acord scris; termen legal max. 30 zile | `clm.renovation_check.law50.monument_notice` |
| Poziție oficială Timișoara | `pmt_art11_online_service` | `clm.renovation_check.pmt.art11_service` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.renovation_check.law50.general_exemption` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.renovation_check.law50.listed_works` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.renovation_check.law50.energy_change_use` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.renovation_check.law50.protected_nonmonument` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.renovation_check.law50.monument_notice` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/55794 |
| `clm.renovation_check.pmt.art11_service` | `verified` | `uat` | https://servicii.primariatm.ro/aprobare-lucrari-art-11 |
