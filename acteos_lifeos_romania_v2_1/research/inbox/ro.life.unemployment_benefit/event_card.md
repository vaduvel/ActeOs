---
schema_version: "3.0.0"
batch_id: "batch10.unemployment_benefit"
event_type_id: "ro.life.unemployment_benefit"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "verified_with_local_gap"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.unemployment_benefit` |
| Titlu | Solicitarea indemnizației de șomaj |
| Scop | Evaluează condițiile cumulative, dosarul, momentul cererii, durata și canalul competent. |
| Autoritate | Agenția pentru ocuparea forței de muncă din raza domiciliului sau reședinței |
| Pilot local | AJOFM Timiș / Agenția Locală Timișoara |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `termination_reason_class` | enum | non_imputable_confirmed \| imputable_confirmed \| unknown | da |
| `contribution_months_last_24` | integer | Luni de stagiu în ultimele 24 de luni. | da |
| `monthly_income_amount_ron` | number | Venit lunar din activități autorizate, în lei. | da |
| `pension_conditions_met` | boolean | Sunt îndeplinite condițiile de pensionare. | da |
| `registered_with_agency` | boolean | Înregistrare la agenția de domiciliu/reședință. | da |
| `jurisdiction_id` | string | Pilot: ro.tm.timisoara; alt UAT are gap local. | da |
| `filing_window` | enum | within_first_10_days \| after_10_days_within_12_months \| after_12_months | da |
| `has_identity_document` | boolean | Act de identitate disponibil. | da |
| `has_study_qualification_documents` | boolean | Acte de studii/calificare disponibile. | da |
| `has_employment_records` | boolean | Documentele privind raporturile de muncă și stagiul sunt disponibile. | da |
| `total_contribution_years` | integer | Stagiul total folosit la durată și procent. | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.unemployment_benefit.route.v1` | adevărat | `include_step:register_as_jobseeker`<br>`include_step:prepare_unemployment_benefit_file`<br>`include_step:submit_application_to_competent_agency` | `clm.unemployment_benefit.unemp_conditions`, `clm.unemployment_benefit.unemp_docs` | `active` |
| `rule.unemployment_benefit.reason_imputable.v1` | `termination_reason_class` = `imputable_confirmed` | `block:termination_reason_not_eligible` | `clm.unemployment_benefit.unemp_reason` | `active` |
| `rule.unemployment_benefit.reason_unknown.v1` | `termination_reason_class` = `unknown` | `require_confirmation:confirm_nonimputable_termination_reason` | `clm.unemployment_benefit.unemp_reason` | `in_review` |
| `rule.unemployment_benefit.insufficient_contribution.v1` | `contribution_months_last_24` < `12` | `block:minimum_contribution_not_met` | `clm.unemployment_benefit.unemp_conditions` | `active` |
| `rule.unemployment_benefit.income_at_or_above_isr.v1` | `monthly_income_amount_ron` ≥ `660` | `block:income_threshold_not_met` | `clm.unemployment_benefit.unemp_conditions`, `clm.unemployment_benefit.unemp_isr` | `active` |
| `rule.unemployment_benefit.pension_condition.v1` | `pension_conditions_met` = `True` | `block:pension_condition_excludes_benefit` | `clm.unemployment_benefit.unemp_conditions` | `active` |
| `rule.unemployment_benefit.not_registered.v1` | `registered_with_agency` = `False` | `include_requirement:jobseeker_registration_at_agency_by_domicile_or_residence`<br>`include_step:complete_ajofm_registration` | `clm.unemployment_benefit.unemp_conditions`, `clm.unemployment_benefit.jobseeker_register` | `active` |
| `rule.unemployment_benefit.missing_identity.v1` | `has_identity_document` = `False` | `include_requirement:identity_document` | `clm.unemployment_benefit.unemp_docs` | `active` |
| `rule.unemployment_benefit.missing_studies.v1` | `has_study_qualification_documents` = `False` | `include_requirement:study_and_qualification_documents` | `clm.unemployment_benefit.unemp_docs` | `active` |
| `rule.unemployment_benefit.missing_employment_records.v1` | `has_employment_records` = `False` | `include_requirement:employment_and_contribution_records` | `clm.unemployment_benefit.unemp_docs` | `active` |
| `rule.unemployment_benefit.first_10_days.v1` | `filing_window` = `within_first_10_days` | `emit_advice:entitlement_from_termination_if_filed_in_10_days` | `clm.unemployment_benefit.unemp_timing` | `active` |
| `rule.unemployment_benefit.after_10_days.v1` | `filing_window` = `after_10_days_within_12_months` | `emit_advice:entitlement_from_application_after_10_days` | `clm.unemployment_benefit.unemp_timing` | `active` |
| `rule.unemployment_benefit.after_12_months.v1` | `filing_window` = `after_12_months` | `block:application_after_12_month_forfeiture` | `clm.unemployment_benefit.unemp_timing` | `active` |
| `rule.unemployment_benefit.duration_6.v1` | (`total_contribution_years` ≥ `1` ȘI `total_contribution_years` < `5`) | `emit_advice:benefit_duration_6_months` | `clm.unemployment_benefit.unemp_duration` | `active` |
| `rule.unemployment_benefit.duration_9.v1` | (`total_contribution_years` ≥ `5` ȘI `total_contribution_years` ≤ `10`) | `emit_advice:benefit_duration_9_months` | `clm.unemployment_benefit.unemp_duration` | `active` |
| `rule.unemployment_benefit.duration_12.v1` | `total_contribution_years` > `10` | `emit_advice:benefit_duration_12_months` | `clm.unemployment_benefit.unemp_duration` | `active` |
| `rule.unemployment_benefit.amount_base.v1` | `total_contribution_years` < `3` | `emit_advice:benefit_amount_base_isr` | `clm.unemployment_benefit.unemp_amount`, `clm.unemployment_benefit.unemp_isr` | `active` |
| `rule.unemployment_benefit.amount_3.v1` | (`total_contribution_years` ≥ `3` ȘI `total_contribution_years` < `5`) | `emit_advice:benefit_increment_3_percent` | `clm.unemployment_benefit.unemp_amount` | `active` |
| `rule.unemployment_benefit.amount_5.v1` | (`total_contribution_years` ≥ `5` ȘI `total_contribution_years` < `10`) | `emit_advice:benefit_increment_5_percent` | `clm.unemployment_benefit.unemp_amount` | `active` |
| `rule.unemployment_benefit.amount_7.v1` | (`total_contribution_years` ≥ `10` ȘI `total_contribution_years` < `20`) | `emit_advice:benefit_increment_7_percent` | `clm.unemployment_benefit.unemp_amount` | `active` |
| `rule.unemployment_benefit.amount_10.v1` | `total_contribution_years` ≥ `20` | `emit_advice:benefit_increment_10_percent` | `clm.unemployment_benefit.unemp_amount` | `active` |
| `rule.unemployment_benefit.obligations.v1` | adevărat | `emit_advice:beneficiary_reporting_and_active_search_obligations` | `clm.unemployment_benefit.unemp_obligations` | `active` |
| `rule.unemployment_benefit.timis_channel.v1` | `jurisdiction_id` în ['ro.tm', 'ro.tm.timisoara'] | `attach_channel:ajofm_timis_bd_republicii_21` | `clm.unemployment_benefit.ajofm_timisoara` | `active` |
| `rule.unemployment_benefit.other_uat.v1` | `jurisdiction_id` nu este în ['ro.tm', 'ro.tm.timisoara'] | `attach_channel:ajofm_by_domicile_or_residence`<br>`emit_advice:verified_with_local_gap`<br>`require_confirmation:confirm_local_ajofm_channel` | `clm.unemployment_benefit.jobseeker_register` | `in_review` |

## Termene, praguri și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Stagiu minim | 12 luni în ultimele 24 | `clm.unemployment_benefit.unemp_conditions` |
| Prag venit publicat | sub ISR; pagina pilot indică 660 lei | `clm.unemployment_benefit.unemp_isr` |
| Cerere favorabilă | în 10 zile de la încetare | `clm.unemployment_benefit.unemp_timing` |
| Termen de decădere | 12 luni | `clm.unemployment_benefit.unemp_timing` |
| Durată | 6 / 9 / 12 luni după stagiu | `clm.unemployment_benefit.unemp_duration` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.unemployment_benefit.unemp_reason` | `verified` | `county` | https://www.anofm.ro/timis/indemnizatie-de-somaj-pentru-persoanele-cu-experienta-in-munca/ |
| `clm.unemployment_benefit.unemp_conditions` | `verified` | `county` | https://www.anofm.ro/timis/indemnizatie-de-somaj-pentru-persoanele-cu-experienta-in-munca/ |
| `clm.unemployment_benefit.unemp_isr` | `verified` | `county` | https://www.anofm.ro/timis/indemnizatie-de-somaj-pentru-persoanele-cu-experienta-in-munca/ |
| `clm.unemployment_benefit.unemp_docs` | `verified` | `county` | https://www.anofm.ro/timis/indemnizatie-de-somaj-pentru-persoanele-cu-experienta-in-munca/ |
| `clm.unemployment_benefit.unemp_timing` | `verified` | `county` | https://www.anofm.ro/timis/indemnizatie-de-somaj-pentru-persoanele-cu-experienta-in-munca/ |
| `clm.unemployment_benefit.unemp_duration` | `verified` | `county` | https://www.anofm.ro/timis/indemnizatie-de-somaj-pentru-persoanele-cu-experienta-in-munca/ |
| `clm.unemployment_benefit.unemp_amount` | `verified` | `county` | https://www.anofm.ro/timis/indemnizatie-de-somaj-pentru-persoanele-cu-experienta-in-munca/ |
| `clm.unemployment_benefit.unemp_obligations` | `verified` | `county` | https://www.anofm.ro/timis/indemnizatie-de-somaj-pentru-persoanele-cu-experienta-in-munca/ |
| `clm.unemployment_benefit.jobseeker_register` | `verified` | `county` | https://www.anofm.ro/timis/inregistrarea-somerilor/ |
| `clm.unemployment_benefit.ajofm_timisoara` | `verified` | `county` | https://www.anofm.ro/timis/contact/ |
