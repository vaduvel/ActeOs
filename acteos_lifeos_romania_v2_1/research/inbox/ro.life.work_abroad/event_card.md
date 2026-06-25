---
schema_version: "3.0.0"
batch_id: "batch10.work_abroad"
event_type_id: "ro.life.work_abroad"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "in_review"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.work_abroad` |
| Titlu | Pregătirea pentru muncă în străinătate |
| Scop | Separă angajarea directă de detașare și verifică dreptul de muncă, calificarea, securitatea socială și rezidența fiscală. |
| Autoritate | Autoritățile statului gazdă, angajatorul, EURES, instituțiile de securitate socială și ANAF |
| Pilot local | AJOFM Timiș — EURES și formulare europene |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `employment_model` | enum | direct_host_employer \| posted_by_ro_employer | da |
| `destination_scope` | enum | eu \| non_eu | da |
| `worker_citizenship_scope` | enum | romanian_or_eu \| third_country | da |
| `profession_regulated` | boolean | Profesia este reglementată în statul gazdă. | da |
| `qualification_recognition_ready` | boolean | Recunoașterea este obținută/confirmată. | da |
| `social_security_status_confirmed` | boolean | Statul de asigurare și documentele aferente sunt confirmate. | da |
| `tax_residence_review_done` | boolean | Rezidența fiscală la plecare a fost analizată. | da |
| `posting_reges_data_ready` | boolean | Datele detașării pentru REGES sunt pregătite. | da |
| `posting_contract_terms_complete` | boolean | CIM/actul cuprinde informațiile pentru munca în străinătate. | da |
| `jurisdiction_id` | string | Pilot: ro.tm.timisoara pentru canalul EURES verificat. | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.work_abroad.route.v1` | adevărat | `include_step:identify_employment_model_and_destination`<br>`include_step:verify_work_right_and_profession_rules`<br>`include_step:confirm_social_security_coverage`<br>`include_step:review_tax_residence_departure` | `clm.work_abroad.eu_no_permit`, `clm.work_abroad.regulated_qualification`, `clm.work_abroad.social_security_rule`, `clm.work_abroad.z017` | `active` |
| `rule.work_abroad.eu_direct_romanian.v1` | (`employment_model` = `direct_host_employer` ȘI `destination_scope` = `eu` ȘI `worker_citizenship_scope` = `romanian_or_eu`) | `emit_advice:eu_citizen_generally_no_work_permit_in_eu` | `clm.work_abroad.eu_no_permit` | `active` |
| `rule.work_abroad.country_specific_permit.v1` | (`destination_scope` = `non_eu` SAU `worker_citizenship_scope` = `third_country`) | `require_confirmation:confirm_destination_work_and_residence_right` | `clm.work_abroad.non_eu_permit_gap` | `in_review` |
| `rule.work_abroad.regulated_not_ready.v1` | (`profession_regulated` = `True` ȘI `qualification_recognition_ready` = `False`) | `include_requirement:professional_qualification_recognition_in_destination`<br>`block:regulated_profession_recognition_missing` | `clm.work_abroad.regulated_qualification` | `active` |
| `rule.work_abroad.social_not_confirmed.v1` | `social_security_status_confirmed` = `False` | `include_requirement:confirmed_social_security_coverage_and_required_portable_document` | `clm.work_abroad.social_security_rule` | `active` |
| `rule.work_abroad.tax_not_reviewed.v1` | `tax_residence_review_done` = `False` | `include_step:review_z017_tax_residence_departure_applicability`<br>`emit_advice:z017_is_departure_tax_residence_form` | `clm.work_abroad.z017` | `active` |
| `rule.work_abroad.posted_route.v1` | `employment_model` = `posted_by_ro_employer` | `include_step:verify_continued_relation_with_ro_employer`<br>`include_step:verify_posting_contract_information`<br>`include_step:record_transnational_posting_in_reges`<br>`emit_advice:posted_worker_may_remain_in_origin_social_system` | `clm.work_abroad.posting_relationship`, `clm.work_abroad.posting_contract`, `clm.work_abroad.posting_reges`, `clm.work_abroad.posted_social` | `active` |
| `rule.work_abroad.posted_contract_incomplete.v1` | (`employment_model` = `posted_by_ro_employer` ȘI `posting_contract_terms_complete` = `False`) | `include_requirement:posting_duration_currency_payment_and_benefits_terms` | `clm.work_abroad.posting_contract` | `active` |
| `rule.work_abroad.posted_reges_missing.v1` | (`employment_model` = `posted_by_ro_employer` ȘI `posting_reges_data_ready` = `False`) | `include_requirement:posting_start_end_state_beneficiary_and_activity_for_reges` | `clm.work_abroad.posting_reges` | `active` |
| `rule.work_abroad.timis_eures.v1` | `jurisdiction_id` în ['ro.tm', 'ro.tm.timisoara'] | `attach_channel:ajofm_timis_eures_and_european_forms` | `clm.work_abroad.eures_timisoara` | `active` |
| `rule.work_abroad.other_eures.v1` | `jurisdiction_id` nu este în ['ro.tm', 'ro.tm.timisoara'] | `attach_channel:eures_romania_local_adviser`<br>`require_confirmation:confirm_local_eures_contact` | `clm.work_abroad.eures_timisoara` | `in_review` |

## Termene, praguri și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Cetățean UE în alt stat UE | de regulă fără permis de muncă | `clm.work_abroad.eu_no_permit` |
| Profesie reglementată | poate necesita recunoașterea calificării | `clm.work_abroad.regulated_qualification` |
| Detașare | date obligatorii în REGES și informații contractuale | `clm.work_abroad.posting_reges` |
| Rezidență fiscală la plecare | formular Z017 — aplicabilitate de verificat | `clm.work_abroad.z017` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.work_abroad.eu_no_permit` | `verified` | `eu` | https://europa.eu/youreurope/citizens/work/work-abroad/work-permits/index_ro.htm |
| `clm.work_abroad.non_eu_permit_gap` | `needs_confirmation` | `eu` | https://europa.eu/youreurope/citizens/work/work-abroad/work-permits/index_ro.htm |
| `clm.work_abroad.regulated_qualification` | `verified` | `eu` | https://europa.eu/youreurope/citizens/work/professional-qualifications/regulated-professions/index_ro.htm |
| `clm.work_abroad.social_security_rule` | `verified` | `eu` | https://europa.eu/youreurope/citizens/work/social-security-and-benefits/country-coverage/index_ro.htm |
| `clm.work_abroad.posted_social` | `verified` | `eu` | https://europa.eu/youreurope/citizens/work/social-security-and-benefits/country-coverage/index_ro.htm |
| `clm.work_abroad.posting_relationship` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/informatii-utile/detasarea-transnationala-in-cadrul-prestarii-de-servicii/ |
| `clm.work_abroad.posting_contract` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/informatii-utile/detasarea-transnationala-in-cadrul-prestarii-de-servicii/ |
| `clm.work_abroad.posting_reges` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/informatii-utile/detasarea-transnationala-in-cadrul-prestarii-de-servicii/ |
| `clm.work_abroad.z017` | `verified` | `national_operational` | https://static.anaf.ro/static/10/Anaf/Declaratii_R/Z017.html |
| `clm.work_abroad.eures_timisoara` | `verified` | `county` | https://www.anofm.ro/timis/contact/ |
