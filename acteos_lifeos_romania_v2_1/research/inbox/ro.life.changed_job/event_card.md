---
schema_version: "3.0.0"
batch_id: "batch10.changed_job"
event_type_id: "ro.life.changed_job"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "verified"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.changed_job` |
| Titlu | Schimbarea locului de muncă |
| Scop | Coordonează încetarea vechiului raport, documentele de vechime și pornirea noului job. |
| Autoritate | Angajatorii implicați, Inspecția Muncii / REGES-ONLINE și AJOFM |
| Pilot local | România; AJOFM Timiș pentru suport local |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `old_end_method` | enum | resignation \| nonpersonal_dismissal \| other | da |
| `role_level` | enum | execution \| management | da |
| `notice_waived_or_employer_breach` | boolean | Situație documentată pentru demisie fără preaviz/renunțare la preaviz. | da |
| `received_termination_document` | boolean | Documentul de încetare primit. | da |
| `received_history_proof` | boolean | Adeverință/extras privind activitatea și vechimea. | da |
| `has_new_offer` | boolean | Există un nou raport de muncă pregătit. | da |
| `workplace_or_profession_changed` | boolean | Schimbare relevantă pentru examenul de medicina muncii. | da |
| `medical_file_copy_available` | boolean | Copia dosarului medical de la locul anterior este disponibilă. | da |
| `wants_employment_services` | boolean | Solicită servicii AJOFM pentru schimbarea jobului. | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.changed_job.route.v1` | adevărat | `include_step:close_previous_employment_record`<br>`include_step:collect_termination_and_history_documents`<br>`include_step:prepare_new_employment_start` | `clm.changed_job.history_employer`, `clm.changed_job.cim_written` | `active` |
| `rule.changed_job.resignation_execution.v1` | (`old_end_method` = `resignation` ȘI `role_level` = `execution` ȘI `notice_waived_or_employer_breach` = `False`) | `emit_advice:resignation_notice_max_20_working_days` | `clm.changed_job.resignation_notice` | `active` |
| `rule.changed_job.resignation_management.v1` | (`old_end_method` = `resignation` ȘI `role_level` = `management` ȘI `notice_waived_or_employer_breach` = `False`) | `emit_advice:resignation_notice_max_45_working_days` | `clm.changed_job.resignation_notice` | `active` |
| `rule.changed_job.resignation_without_notice.v1` | (`old_end_method` = `resignation` ȘI `notice_waived_or_employer_breach` = `True`) | `emit_advice:resignation_without_notice_document_basis` | `clm.changed_job.resignation_waiver` | `active` |
| `rule.changed_job.dismissal_notice.v1` | `old_end_method` = `nonpersonal_dismissal` | `emit_advice:dismissal_notice_min_20_working_days` | `clm.changed_job.dismissal_notice` | `active` |
| `rule.changed_job.missing_termination_document.v1` | `received_termination_document` = `False` | `include_requirement:termination_document_from_previous_employer` | `clm.changed_job.termination_decision` | `active` |
| `rule.changed_job.missing_history_proof.v1` | `received_history_proof` = `False` | `include_requirement:employment_activity_and_seniority_document`<br>`include_step:request_history_document_or_reges_extract` | `clm.changed_job.history_employer`, `clm.changed_job.history_extract` | `active` |
| `rule.changed_job.new_offer.v1` | `has_new_offer` = `True` | `include_step:verify_new_contract_before_start`<br>`trigger_child_event:ro.life.started_job` | `clm.changed_job.cim_written`, `clm.changed_job.cim_register` | `active` |
| `rule.changed_job.employment_services.v1` | `wants_employment_services` = `True` | `include_step:register_for_employment_services`<br>`attach_channel:ajofm_by_domicile_or_residence`<br>`emit_advice:employed_person_can_seek_job_change_support` | `clm.changed_job.jobseeker_change` | `active` |
| `rule.changed_job.occupational_exam.v1` | `workplace_or_profession_changed` = `True` | `include_step:complete_new_occupational_health_exam` | `clm.changed_job.occupational_change` | `active` |
| `rule.changed_job.medical_file_missing.v1` | (`workplace_or_profession_changed` = `True` ȘI `medical_file_copy_available` = `False`) | `include_requirement:copy_of_previous_occupational_medical_file` | `clm.changed_job.occupational_file` | `active` |

## Termene, praguri și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Preaviz demisie — execuție | maximum 20 zile lucrătoare | `clm.changed_job.resignation_notice` |
| Preaviz demisie — conducere | maximum 45 zile lucrătoare | `clm.changed_job.resignation_notice` |
| Preaviz concediere neimputabilă | minimum 20 zile lucrătoare | `clm.changed_job.dismissal_notice` |
| Dovada vechimii | document angajator sau extras REGES | `clm.changed_job.history_employer` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.changed_job.cim_written` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.changed_job.cim_register` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.changed_job.history_employer` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.changed_job.history_extract` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.changed_job.dismissal_notice` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/ajutor/intrebari-frecvente/ |
| `clm.changed_job.resignation_notice` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/ajutor/intrebari-frecvente/ |
| `clm.changed_job.resignation_waiver` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/ajutor/intrebari-frecvente/ |
| `clm.changed_job.termination_decision` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/informatii-utile/detalii-incetare/ |
| `clm.changed_job.occupational_change` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/82130 |
| `clm.changed_job.occupational_file` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/82130 |
| `clm.changed_job.jobseeker_change` | `verified` | `county` | https://www.anofm.ro/timis/inregistrarea-somerilor/ |
