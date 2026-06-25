---
schema_version: "3.0.0"
batch_id: "batch08.declare_home_local_tax"
event_type_id: "ro.life.declare_home_local_tax"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "verified_with_local_gap"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.declare_home_local_tax` |
| Titlu | Declararea locuinței la impozite locale |
| Scop | Identifică traseul de declarare fiscală locală pentru o locuință, fără a inventa termenul sau lista dinamică de documente. |
| Autoritate națională / normativă | Regimul fiscal național; administrare de către UAT-ul unde este situat imobilul |
| Pilot local | Municipiul Timișoara / județul Timiș |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `jurisdiction_id` | string | ID-ul UAT al imobilului; pilot `ro.tm.timisoara`. | da |
| `owner_type` | enum | `person`, `legal_entity` | da |
| `home_case` | enum | `new_residential_building`, `apartment`, `acquired_residential_building`, `built_residential_building` | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.home_tax.timisoara.pf_new.v1` | (`jurisdiction_id` = `ro.tm.timisoara` ȘI `owner_type` = `person` ȘI `home_case` = `new_residential_building`) | `include_step:select_atlas_tax_case`<br>`include_step:prepare_home_tax_file`<br>`include_step:submit_home_tax_declaration`<br>`attach_channel:pmt_atlas_tax`<br>`emit_advice:atlas_case_controls_documents` | `clm.home_tax.pmt.pf_new_atlas` | `active` |
| `rule.home_tax.timisoara.pf_apartment.v1` | (`jurisdiction_id` = `ro.tm.timisoara` ȘI `owner_type` = `person` ȘI `home_case` = `apartment`) | `include_step:select_atlas_tax_case`<br>`include_step:prepare_home_tax_file`<br>`include_step:submit_home_tax_declaration`<br>`attach_channel:pmt_atlas_tax`<br>`emit_advice:atlas_case_controls_documents` | `clm.home_tax.pmt.pf_apartment_atlas` | `active` |
| `rule.home_tax.timisoara.pj_built_or_acquired.v1` | (`jurisdiction_id` = `ro.tm.timisoara` ȘI `owner_type` = `legal_entity` ȘI `home_case` în [built_residential_building, acquired_residential_building]) | `include_step:select_atlas_tax_case`<br>`include_step:prepare_home_tax_file`<br>`include_requirement:destination_supporting_documents_if_applicable`<br>`include_requirement:utility_expense_supporting_documents_if_applicable`<br>`include_requirement:copies_certified_conform_to_original`<br>`include_step:submit_home_tax_declaration`<br>`attach_channel:pmt_atlas_tax` | `clm.home_tax.pmt.pj_built`, `clm.home_tax.pmt.pj_acquired` | `active` |
| `rule.home_tax.timisoara.unmapped_case.v1` | (`jurisdiction_id` = `ro.tm.timisoara` ȘI NU ((`owner_type` = `person` ȘI `home_case` = `new_residential_building`) SAU (`owner_type` = `person` ȘI `home_case` = `apartment`) SAU (`owner_type` = `legal_entity` ȘI `home_case` în [built_residential_building, acquired_residential_building]))) | `include_step:select_atlas_tax_case`<br>`attach_channel:pmt_atlas_tax`<br>`require_confirmation:confirm_atlas_home_case` | `clm.home_tax.pmt.index` | `in_review` |
| `rule.home_tax.other_uat.v1` | `jurisdiction_id` ≠ `ro.tm.timisoara` | `include_step:identify_competent_local_tax_authority`<br>`require_confirmation:confirm_local_home_tax_procedure`<br>`emit_advice:verified_with_local_gap` | `clm.home_tax.pmt.index` | `in_review` |
| `rule.home_tax.deadline_confirmation.v1` | adevărat | `require_confirmation:confirm_current_home_tax_declaration_deadline` | `clm.home_tax.cod_fiscal_unavailable` | `in_review` |

## Termene, taxe și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Canal pilot Timișoara | `pmt_atlas_tax` | `clm.home_tax.pmt.pf_new_atlas` |
| Termen național | `needs_confirmation` — nu este afirmat numeric | `clm.home_tax.cod_fiscal_unavailable` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.home_tax.pmt.index` | `verified` | `uat` | https://servicii.primariatm.ro/ |
| `clm.home_tax.pmt.pf_new_atlas` | `verified` | `uat` | https://servicii.primariatm.ro/dfmt-pf-declararea-cladirilor-rezidentiale-nou-edificate |
| `clm.home_tax.pmt.pf_apartment_atlas` | `verified` | `uat` | https://servicii.primariatm.ro/dfmt-pf-declarare-impunere-apartamente |
| `clm.home_tax.pmt.pj_built` | `verified` | `uat` | https://servicii.primariatm.ro/dfmt-pj-declararea-cladirilor-construite |
| `clm.home_tax.pmt.pj_acquired` | `verified` | `uat` | https://servicii.primariatm.ro/dfmt-pj-declararea-cladirilor-dobandite |
| `clm.home_tax.cod_fiscal_unavailable` | `needs_confirmation` | `national_operational` | https://legislatie.just.ro/Public/DetaliiDocument/171282 |
