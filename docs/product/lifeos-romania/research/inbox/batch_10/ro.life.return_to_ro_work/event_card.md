---
schema_version: "3.0.0"
batch_id: "batch10.return_to_ro_work"
event_type_id: "ro.life.return_to_ro_work"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "in_review"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.return_to_ro_work` |
| Titlu | Revenirea în România pentru muncă |
| Scop | Leagă documentele din străinătate de angajare, recunoașterea calificării, prestații și rezidența fiscală. |
| Autoritate | Angajatorul român, autoritatea profesională, AJOFM/EURES, instituțiile de securitate socială și ANAF |
| Pilot local | AJOFM Timiș — EURES și formulare europene |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `returning_from_scope` | enum | eu \| non_eu | da |
| `has_ro_job_offer` | boolean | Există ofertă/contract pregătit în România. | da |
| `plans_immediate_employment` | boolean | Persoana vrea să înceapă imediat un job. | da |
| `profession_regulated_in_ro` | boolean | Profesia este reglementată în România. | da |
| `qualification_recognition_ready` | boolean | Recunoașterea calificării este pregătită. | da |
| `needs_foreign_periods_for_benefits` | boolean | Perioadele externe trebuie valorificate pentru prestații. | da |
| `has_foreign_employment_documents` | boolean | Documentele de muncă/asigurare din străinătate sunt disponibile. | da |
| `tax_residence_review_done` | boolean | Rezidența fiscală la sosire a fost analizată. | da |
| `needs_european_form_support` | boolean | Este necesar sprijin pentru formulare europene/EURES. | da |
| `jurisdiction_id` | string | Pilot: ro.tm.timisoara pentru AJOFM/EURES. | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.return_to_ro_work.route.v1` | adevărat | `include_step:collect_foreign_employment_and_insurance_documents`<br>`include_step:review_professional_qualification_in_ro`<br>`include_step:review_tax_residence_arrival`<br>`include_step:choose_job_start_or_jobseeker_route` | `clm.return_to_ro_work.social_periods`, `clm.return_to_ro_work.regulated_qualification`, `clm.return_to_ro_work.z015` | `active` |
| `rule.return_to_ro_work.job_offer.v1` | (`has_ro_job_offer` = `True` ȘI `plans_immediate_employment` = `True`) | `trigger_child_event:ro.life.started_job`<br>`include_step:prepare_ro_employment_start` | `clm.return_to_ro_work.cim_written`, `clm.return_to_ro_work.cim_register` | `active` |
| `rule.return_to_ro_work.no_offer.v1` | `has_ro_job_offer` = `False` | `include_step:register_for_employment_services_in_ro`<br>`attach_channel:ajofm_by_domicile_or_residence` | `clm.return_to_ro_work.jobseeker_register` | `active` |
| `rule.return_to_ro_work.regulated_missing.v1` | (`profession_regulated_in_ro` = `True` ȘI `qualification_recognition_ready` = `False`) | `include_requirement:professional_qualification_recognition_in_romania`<br>`block:regulated_profession_not_ready_in_ro` | `clm.return_to_ro_work.regulated_qualification` | `active` |
| `rule.return_to_ro_work.eu_periods.v1` | (`needs_foreign_periods_for_benefits` = `True` ȘI `returning_from_scope` = `eu`) | `emit_advice:eu_periods_must_be_taken_into_account`<br>`include_step:request_relevant_european_form_or_period_confirmation` | `clm.return_to_ro_work.social_periods` | `active` |
| `rule.return_to_ro_work.non_eu_periods.v1` | (`needs_foreign_periods_for_benefits` = `True` ȘI `returning_from_scope` = `non_eu`) | `require_confirmation:confirm_non_eu_period_coordination` | `clm.return_to_ro_work.non_eu_social_periods_gap` | `in_review` |
| `rule.return_to_ro_work.missing_foreign_docs.v1` | (`needs_foreign_periods_for_benefits` = `True` ȘI `has_foreign_employment_documents` = `False`) | `include_requirement:foreign_employment_and_insurance_documents`<br>`require_confirmation:confirm_exact_foreign_period_documents` | `clm.return_to_ro_work.foreign_period_documents_gap` | `in_review` |
| `rule.return_to_ro_work.tax_not_reviewed.v1` | `tax_residence_review_done` = `False` | `include_step:review_z015_tax_residence_arrival_applicability`<br>`emit_advice:z015_is_arrival_tax_residence_form` | `clm.return_to_ro_work.z015` | `active` |
| `rule.return_to_ro_work.timis_forms.v1` | (`needs_european_form_support` = `True` ȘI `jurisdiction_id` în ['ro.tm', 'ro.tm.timisoara']) | `attach_channel:ajofm_timis_eures_and_european_forms` | `clm.return_to_ro_work.eures_timisoara` | `active` |
| `rule.return_to_ro_work.other_forms.v1` | (`needs_european_form_support` = `True` ȘI `jurisdiction_id` nu este în ['ro.tm', 'ro.tm.timisoara']) | `attach_channel:ajofm_or_eures_by_domicile`<br>`require_confirmation:confirm_local_eures_or_forms_contact` | `clm.return_to_ro_work.eures_timisoara` | `in_review` |

## Termene, praguri și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Angajare în România | se declanșează ruta started_job | `clm.return_to_ro_work.cim_written` |
| Perioade UE | trebuie luate în calcul de instituția competentă | `clm.return_to_ro_work.social_periods` |
| Perioade non-UE | needs_confirmation după acordul aplicabil | `clm.return_to_ro_work.non_eu_social_periods_gap` |
| Rezidență fiscală la sosire | formular Z015 — aplicabilitate de verificat | `clm.return_to_ro_work.z015` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.return_to_ro_work.cim_written` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.return_to_ro_work.cim_register` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.return_to_ro_work.jobseeker_register` | `verified` | `county` | https://www.anofm.ro/timis/inregistrarea-somerilor/ |
| `clm.return_to_ro_work.regulated_qualification` | `verified` | `eu` | https://europa.eu/youreurope/citizens/work/professional-qualifications/regulated-professions/index_ro.htm |
| `clm.return_to_ro_work.social_periods` | `verified` | `eu` | https://europa.eu/youreurope/citizens/work/social-security-and-benefits/country-coverage/index_ro.htm |
| `clm.return_to_ro_work.non_eu_social_periods_gap` | `needs_confirmation` | `eu` | https://europa.eu/youreurope/citizens/work/social-security-and-benefits/country-coverage/index_ro.htm |
| `clm.return_to_ro_work.foreign_period_documents_gap` | `needs_confirmation` | `county` | https://www.anofm.ro/timis/contact/ |
| `clm.return_to_ro_work.z015` | `verified` | `national_operational` | https://static.anaf.ro/static/10/Anaf/Declaratii_R/Z015.html |
| `clm.return_to_ro_work.eures_timisoara` | `verified` | `county` | https://www.anofm.ro/timis/contact/ |
