---
schema_version: "3.0.0"
batch_id: "batch10.employment_history_proof"
event_type_id: "ro.life.employment_history_proof"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "in_review"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.employment_history_proof` |
| Titlu | Obținerea dovezii de vechime și activitate |
| Scop | Alege extrasul REGES sau documentul angajatorului și gestionează perioadele lipsă ori erorile. |
| Autoritate | Angajatorul/fostul angajator, REGES-ONLINE, administratorul/lichidatorul și instituțiile de arhivă competente |
| Pilot local | Regulă națională; fără dependență de UAT pentru extrasul online |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `history_period_bucket` | enum | reges_available_records \| legacy_or_mixed \| unknown | da |
| `has_reges_access` | boolean | Acces activ în aplicația Salariat. | da |
| `preferred_scope` | enum | individual \| centralized | da |
| `needs_employer_certificate` | boolean | Este necesar și documentul eliberat de angajator. | da |
| `employer_active` | boolean | Angajatorul/fostul angajator mai este activ. | da |
| `employer_in_insolvency_or_liquidation` | boolean | Există administrator/lichidator judiciar. | da |
| `data_complete_in_reges` | boolean | Perioadele necesare apar complet în extras. | da |
| `has_data_discrepancy` | boolean | Există date incorecte sau lipsă. | da |
| `needs_signed_electronic_extract` | boolean | Este necesar un document semnat electronic. | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.employment_history_proof.route.v1` | adevărat | `include_step:access_reges_employee_portal`<br>`include_step:generate_employment_history_extract`<br>`include_step:verify_extract_completeness` | `clm.employment_history_proof.history_extract`, `clm.employment_history_proof.history_reges_formats` | `active` |
| `rule.employment_history_proof.no_access.v1` | `has_reges_access` = `False` | `include_step:create_or_recover_reges_employee_access`<br>`include_requirement:roeid_or_email_account_for_reges` | `clm.employment_history_proof.history_reges_access` | `active` |
| `rule.employment_history_proof.individual.v1` | `preferred_scope` = `individual` | `emit_advice:request_individual_reges_extract` | `clm.employment_history_proof.history_reges_formats` | `active` |
| `rule.employment_history_proof.centralized.v1` | `preferred_scope` = `centralized` | `emit_advice:request_centralized_reges_extract` | `clm.employment_history_proof.history_centralizer` | `active` |
| `rule.employment_history_proof.employer_certificate_active.v1` | (`needs_employer_certificate` = `True` ȘI `employer_active` = `True`) | `include_step:request_activity_and_seniority_document_from_employer`<br>`include_requirement:employer_activity_duration_salary_and_seniority_document` | `clm.employment_history_proof.history_employer` | `active` |
| `rule.employment_history_proof.insolvency.v1` | (`needs_employer_certificate` = `True` ȘI `employer_active` = `False` ȘI `employer_in_insolvency_or_liquidation` = `True`) | `include_step:request_document_from_judicial_administrator_or_liquidator`<br>`emit_advice:insolvency_document_max_60_calendar_days` | `clm.employment_history_proof.history_insolvency` | `active` |
| `rule.employment_history_proof.inactive_unknown_route.v1` | (`needs_employer_certificate` = `True` ȘI `employer_active` = `False` ȘI `employer_in_insolvency_or_liquidation` = `False`) | `require_confirmation:confirm_inactive_employer_history_route` | `clm.employment_history_proof.history_inactive_employer_gap` | `in_review` |
| `rule.employment_history_proof.legacy_period.v1` | `history_period_bucket` în ['legacy_or_mixed', 'unknown'] | `require_confirmation:confirm_legacy_employment_record_coverage` | `clm.employment_history_proof.history_legacy_gap` | `in_review` |
| `rule.employment_history_proof.incomplete_reges.v1` | `data_complete_in_reges` = `False` | `include_requirement:supplementary_employer_or_archive_documents`<br>`require_confirmation:confirm_missing_reges_periods` | `clm.employment_history_proof.history_legacy_gap`, `clm.employment_history_proof.history_employer` | `in_review` |
| `rule.employment_history_proof.discrepancy_active.v1` | (`has_data_discrepancy` = `True` ȘI `employer_active` = `True`) | `include_step:notify_active_employer_in_reges` | `clm.employment_history_proof.history_correction` | `active` |
| `rule.employment_history_proof.discrepancy_inactive.v1` | (`has_data_discrepancy` = `True` ȘI `employer_active` = `False`) | `require_confirmation:confirm_correction_route_for_inactive_employer` | `clm.employment_history_proof.history_inactive_employer_gap` | `in_review` |
| `rule.employment_history_proof.signed_extract.v1` | `needs_signed_electronic_extract` = `True` | `emit_advice:use_electronically_signed_reges_extract` | `clm.employment_history_proof.history_signed`, `clm.employment_history_proof.history_reges_formats` | `active` |

## Termene, praguri și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Document angajator | activitate, durată, salariu și vechime | `clm.employment_history_proof.history_employer` |
| Extras REGES | poate dovedi vechimea | `clm.employment_history_proof.history_extract` |
| Formate | PDF / XLSX / CSV și semnare electronică | `clm.employment_history_proof.history_reges_formats` |
| Insolvență/lichidare | maximum 60 zile calendaristice | `clm.employment_history_proof.history_insolvency` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.employment_history_proof.history_employer` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.employment_history_proof.history_extract` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.employment_history_proof.history_reges_formats` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/ajutor/ghid-de-utilizare-aplicatia-salariat/ |
| `clm.employment_history_proof.history_centralizer` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/ajutor/ghid-de-utilizare-aplicatia-salariat/ |
| `clm.employment_history_proof.history_signed` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/ajutor/ghid-de-utilizare-aplicatia-salariat/ |
| `clm.employment_history_proof.history_correction` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/ajutor/ghid-de-utilizare-aplicatia-salariat/ |
| `clm.employment_history_proof.history_insolvency` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.employment_history_proof.history_reges_access` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/ajutor/ghid-de-utilizare-aplicatia-salariat/ |
| `clm.employment_history_proof.history_legacy_gap` | `needs_confirmation` | `national_operational` | https://reges.inspectiamuncii.ro/ajutor/ghid-de-utilizare-aplicatia-salariat/ |
| `clm.employment_history_proof.history_inactive_employer_gap` | `needs_confirmation` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
