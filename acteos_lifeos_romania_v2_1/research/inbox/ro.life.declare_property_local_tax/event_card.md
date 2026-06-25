---
schema_version: "3.0.0"
batch_id: "batch08.declare_property_local_tax"
event_type_id: "ro.life.declare_property_local_tax"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "verified_with_local_gap"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.declare_property_local_tax` |
| Titlu | Declararea proprietății la impozite locale |
| Scop | Determină traseul local pentru clădire, teren sau imobil mixt și marchează explicit termenul ori speța care nu pot fi verificate. |
| Autoritate națională / normativă | Regimul fiscal național; administrare de către UAT-ul unde este situat bunul |
| Pilot local | Municipiul Timișoara / județul Timiș |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `jurisdiction_id` | string | ID-ul UAT al imobilului. | da |
| `owner_type` | enum | `person`, `legal_entity` | da |
| `property_kind` | enum | `building`, `land`, `building_and_land` | da |
| `property_event` | enum | `acquired`, `built`, `revalued`, `modernized`, `split` | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.property_tax.timisoara.pf_land.v1` | (`jurisdiction_id` = `ro.tm.timisoara` ȘI `owner_type` = `person` ȘI `property_kind` = `land`) | `include_step:select_atlas_tax_case`<br>`include_step:prepare_property_tax_file`<br>`include_step:submit_property_tax_declaration`<br>`attach_channel:pmt_atlas_tax`<br>`emit_advice:atlas_case_controls_documents` | `clm.property_tax.pmt.pf_land` | `active` |
| `rule.property_tax.timisoara.pj_land.v1` | (`jurisdiction_id` = `ro.tm.timisoara` ȘI `owner_type` = `legal_entity` ȘI `property_kind` = `land` ȘI `property_event` = `acquired`) | `include_step:select_atlas_tax_case`<br>`include_requirement:copies_certified_conform_to_original`<br>`include_step:submit_property_tax_declaration`<br>`attach_channel:pmt_atlas_tax` | `clm.property_tax.pmt.pj_land` | `active` |
| `rule.property_tax.timisoara.pj_building_acquired.v1` | (`jurisdiction_id` = `ro.tm.timisoara` ȘI `owner_type` = `legal_entity` ȘI `property_kind` = `building` ȘI `property_event` = `acquired`) | `include_step:select_atlas_tax_case`<br>`include_requirement:destination_supporting_documents_if_applicable`<br>`include_requirement:copies_certified_conform_to_original`<br>`include_step:submit_property_tax_declaration`<br>`attach_channel:pmt_atlas_tax` | `clm.property_tax.pmt.pj_building` | `active` |
| `rule.property_tax.timisoara.pj_revaluation.v1` | (`jurisdiction_id` = `ro.tm.timisoara` ȘI `owner_type` = `legal_entity` ȘI `property_kind` = `building` ȘI `property_event` = `revalued`) | `include_step:select_atlas_revaluation_case`<br>`include_requirement:revaluation_supporting_document`<br>`include_requirement:copies_certified_conform_to_original`<br>`include_step:submit_property_tax_declaration`<br>`attach_channel:pmt_atlas_tax` | `clm.property_tax.pmt.pj_revaluation` | `active` |
| `rule.property_tax.timisoara.other_case.v1` | (`jurisdiction_id` = `ro.tm.timisoara` ȘI NU ((`owner_type` = `person` ȘI `property_kind` = `land`) SAU (`owner_type` = `legal_entity` ȘI `property_kind` = `land` ȘI `property_event` = `acquired`) SAU (`owner_type` = `legal_entity` ȘI `property_kind` = `building` ȘI `property_event` în [acquired, revalued]))) | `include_step:select_atlas_tax_case`<br>`attach_channel:pmt_atlas_tax`<br>`require_confirmation:confirm_atlas_property_case` | `clm.property_tax.pmt.index` | `in_review` |
| `rule.property_tax.other_uat.v1` | `jurisdiction_id` ≠ `ro.tm.timisoara` | `include_step:identify_competent_local_tax_authority`<br>`require_confirmation:confirm_local_property_tax_procedure`<br>`emit_advice:verified_with_local_gap` | `clm.property_tax.pmt.index` | `in_review` |
| `rule.property_tax.deadline_confirmation.v1` | adevărat | `require_confirmation:confirm_current_property_tax_declaration_deadline` | `clm.property_tax.cod_fiscal_unavailable` | `in_review` |

## Termene, taxe și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Canal pilot Timișoara | `pmt_atlas_tax` | `clm.property_tax.pmt.pf_land` |
| Termen național | `needs_confirmation` — fără valoare numerică | `clm.property_tax.cod_fiscal_unavailable` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.property_tax.pmt.index` | `verified` | `uat` | https://servicii.primariatm.ro/ |
| `clm.property_tax.pmt.pf_land` | `verified` | `uat` | https://servicii.primariatm.ro/dfmt-pf-declararea-terenurilor |
| `clm.property_tax.pmt.pj_land` | `verified` | `uat` | https://servicii.primariatm.ro/dfmt-pj-declararea-dobandirii-terenurilor |
| `clm.property_tax.pmt.pj_building` | `verified` | `uat` | https://servicii.primariatm.ro/dfmt-pj-declararea-cladirilor-dobandite |
| `clm.property_tax.pmt.pj_revaluation` | `verified` | `uat` | https://servicii.primariatm.ro/dfmt-pj-declararea-reevaluarii-cladirilor |
| `clm.property_tax.cod_fiscal_unavailable` | `needs_confirmation` | `national_operational` | https://legislatie.just.ro/Public/DetaliiDocument/171282 |
