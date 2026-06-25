---
schema_version: "3.0.0"
batch_id: "batch08.property_cadastral_registration"
event_type_id: "ro.life.property_cadastral_registration"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "conflicting"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.property_cadastral_registration` |
| Titlu | Înscrierea cadastrală și în cartea funciară |
| Scop | Construiește dosarul pentru înscrierea dreptului sau a construcției finalizate și separă tarifele/termenele 2026 verificate de paginile vechi. |
| Autoritate națională / normativă | Agenția Națională de Cadastru și Publicitate Imobiliară; OCPI competent teritorial |
| Pilot local | Municipiul Timișoara / județul Timiș |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `jurisdiction_id` | enum | `ro.tm`, `other_county` | da |
| `registration_case` | enum | `ownership`, `finished_individual_house`, `finished_other_construction` | da |
| `has_application` | boolean | `true`, `false` | da |
| `has_cadastral_documentation` | boolean | `true`, `false` | da |
| `has_title_document` | boolean | `true`, `false` | da |
| `has_completion_certificate` | boolean | `true`, `false` | da |
| `has_fiscal_certificate` | boolean | `true`, `false` | da |
| `superficies_act_applicable` | boolean | `true`, `false` | da |
| `superficies_act_available` | boolean | `true`, `false` | da |
| `has_fee_proof` | boolean | `true`, `false` | da |
| `urgent_service` | boolean | `true`, `false` | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.cadastral.base.v1` | adevărat | `include_step:prepare_ocpi_registration_file`<br>`include_step:submit_cadastral_and_land_book_request` | `clm.cadastral_registration.ocpi_ownership_docs`, `clm.cadastral_registration.ocpi_construction_docs` | `active` |
| `rule.cadastral.missing_application.v1` | `has_application` = `False` | `include_requirement:standard_ocpi_application` | `clm.cadastral_registration.ocpi_ownership_docs`, `clm.cadastral_registration.ocpi_construction_docs` | `active` |
| `rule.cadastral.missing_cadastral_docs.v1` | `has_cadastral_documentation` = `False` | `include_requirement:received_cadastral_documentation_if_applicable` | `clm.cadastral_registration.ocpi_ownership_docs`, `clm.cadastral_registration.ocpi_construction_docs` | `active` |
| `rule.cadastral.missing_fee_proof.v1` | `has_fee_proof` = `False` | `include_requirement:cadastral_tariff_payment_proof` | `clm.cadastral_registration.ocpi_ownership_docs`, `clm.cadastral_registration.ocpi_construction_docs` | `active` |
| `rule.cadastral.ownership.missing_title.v1` | (`registration_case` = `ownership` ȘI `has_title_document` = `False`) | `include_requirement:ownership_title_documents` | `clm.cadastral_registration.ocpi_ownership_docs` | `active` |
| `rule.cadastral.construction.missing_completion.v1` | (`registration_case` în [finished_individual_house, finished_other_construction] ȘI `has_completion_certificate` = `False`) | `include_requirement:municipality_completion_or_edification_certificate` | `clm.cadastral_registration.ocpi_construction_docs` | `active` |
| `rule.cadastral.construction.missing_fiscal.v1` | (`registration_case` în [finished_individual_house, finished_other_construction] ȘI `has_fiscal_certificate` = `False`) | `include_requirement:fiscal_certificate_with_tax_value` | `clm.cadastral_registration.ocpi_construction_docs` | `active` |
| `rule.cadastral.construction.missing_superficies.v1` | (`registration_case` în [finished_individual_house, finished_other_construction] ȘI `superficies_act_applicable` = `True` ȘI `superficies_act_available` = `False`) | `include_requirement:surface_right_or_superficies_act` | `clm.cadastral_registration.ocpi_construction_docs` | `active` |
| `rule.cadastral.house.normal.v1` | (`registration_case` = `finished_individual_house` ȘI `urgent_service` = `False`) | `emit_advice:individual_house_tariff_0_05_percent`<br>`emit_advice:individual_house_normal_term_15_working_days` | `clm.cadastral_registration.ancpi_house_tariff_2026`, `clm.cadastral_registration.ancpi_house_terms_2026` | `active` |
| `rule.cadastral.house.urgent.v1` | (`registration_case` = `finished_individual_house` ȘI `urgent_service` = `True`) | `emit_advice:individual_house_tariff_0_05_percent`<br>`emit_advice:individual_house_urgent_term_5_working_days` | `clm.cadastral_registration.ancpi_house_tariff_2026`, `clm.cadastral_registration.ancpi_house_terms_2026` | `active` |
| `rule.cadastral.generic_fee_term_gap.v1` | `registration_case` în [ownership, finished_other_construction] | `require_confirmation:confirm_current_generic_cadastral_tariff`<br>`require_confirmation:confirm_current_generic_cadastral_term` | `clm.cadastral_registration.ancpi_later_amendments`, `clm.cadastral_registration.ocpi_old_tariffs`, `clm.cadastral_registration.ocpi_old_terms` | `in_review` |
| `rule.cadastral.timis_channel.v1` | `jurisdiction_id` = `ro.tm` | `attach_channel:ocpi_timis_documents_and_service_info` | `clm.cadastral_registration.ocpi_ownership_docs`, `clm.cadastral_registration.ocpi_construction_docs` | `active` |
| `rule.cadastral.other_county.v1` | `jurisdiction_id` ≠ `ro.tm` | `include_step:identify_competent_ocpi`<br>`require_confirmation:confirm_local_ocpi_channel`<br>`emit_advice:verified_with_local_gap` | `clm.cadastral_registration.ocpi_ownership_docs` | `in_review` |

## Termene, taxe și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Locuință individuală finalizată — tarif | `0.05%` din valoarea de impozitare | `clm.cadastral_registration.ancpi_house_tariff_2026` |
| Locuință individuală — termen normal/urgent | `15 / 5 zile lucrătoare` | `clm.cadastral_registration.ancpi_house_terms_2026` |
| Alte servicii — tarif/termen | `needs_confirmation` | `clm.cadastral_registration.ancpi_later_amendments` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.cadastral_registration.ocpi_ownership_docs` | `verified` | `county` | https://tm.ancpi.ro/documente-necesare/ |
| `clm.cadastral_registration.ocpi_construction_docs` | `verified` | `county` | https://tm.ancpi.ro/documente-necesare/ |
| `clm.cadastral_registration.ancpi_house_tariff_2026` | `verified` | `national_normative` | https://www.ancpi.ro/wp-content/uploads/2026/03/292.pdf |
| `clm.cadastral_registration.ancpi_house_terms_2026` | `verified` | `national_normative` | https://www.ancpi.ro/wp-content/uploads/2026/03/289.pdf |
| `clm.cadastral_registration.ancpi_later_amendments` | `verified` | `national_operational` | https://www.ancpi.ro/ordine-director-general/ |
| `clm.cadastral_registration.ocpi_old_tariffs` | `expired` | `county` | https://tm.ancpi.ro/tarife-servicii/ |
| `clm.cadastral_registration.ocpi_old_terms` | `expired` | `county` | https://tm.ancpi.ro/termene-servicii/ |
