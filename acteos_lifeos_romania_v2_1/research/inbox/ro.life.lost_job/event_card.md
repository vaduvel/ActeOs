---
schema_version: "3.0.0"
batch_id: "batch10.lost_job"
event_type_id: "ro.life.lost_job"
reference_date: "2026-06-25"
pilot_jurisdiction: "ro.tm.timisoara"
research_status: "verified_with_local_gap"
---

# Event card

## Identitate

| Câmp | Valoare |
|---|---|
| Eveniment | `ro.life.lost_job` |
| Titlu | Pașii administrativi după pierderea locului de muncă |
| Scop | Strânge documentele, verifică încetarea și decide separat ruta de șomaj sau contestație. |
| Autoritate | Fostul angajator, Inspecția Muncii / REGES-ONLINE, AJOFM și instanța competentă |
| Pilot local | România; AJOFM Timiș pentru pilot |
| Data evaluării | `2026-06-25` |

## Fapte necesare

| Fact | Tip | Valori / sens | Obligatoriu |
|---|---|---|---|
| `termination_reason_class` | enum | non_imputable_confirmed \| imputable_confirmed \| unknown | da |
| `termination_form` | enum | dismissal \| fixed_term_expiry \| other | da |
| `has_written_termination_document` | boolean | Documentul de încetare este disponibil. | da |
| `document_states_reason` | boolean | Decizia de concediere arată motivele. | da |
| `document_states_contest_deadline_and_court` | boolean | Decizia indică termenul și instanța de contestare. | da |
| `received_history_proof` | boolean | Adeverința/extrasul de vechime a fost primit. | da |
| `wants_unemployment_benefit` | boolean | Persoana urmărește indemnizația de șomaj. | da |
| `filing_window` | enum | within_first_10_days \| after_10_days_within_12_months \| after_12_months | da |
| `wants_to_challenge` | boolean | Persoana intenționează să conteste concedierea. | da |
| `has_unused_leave` | boolean | Există concediu de odihnă neefectuat. | da |
| `unused_leave_compensated` | boolean | Compensarea a fost inclusă la încetare. | da |
| `reges_record_checked` | boolean | Încetarea a fost verificată în REGES. | da |

## Reguli deterministe

| Regulă | Condiție | Efecte | Surse | Stare |
|---|---|---|---|---|
| `rule.lost_job.route.v1` | adevărat | `include_step:collect_termination_document`<br>`include_step:obtain_employment_history_proof`<br>`include_step:verify_termination_in_reges`<br>`include_step:assess_unemployment_route` | `clm.lost_job.termination_decision`, `clm.lost_job.history_employer`, `clm.lost_job.history_extract` | `active` |
| `rule.lost_job.missing_termination_document.v1` | `has_written_termination_document` = `False` | `include_requirement:written_termination_document` | `clm.lost_job.termination_decision` | `active` |
| `rule.lost_job.dismissal_missing_reason.v1` | (`termination_form` = `dismissal` ȘI `document_states_reason` = `False`) | `include_requirement:dismissal_decision_with_reasons`<br>`emit_warning:dismissal_decision_missing_reasons` | `clm.lost_job.termination_decision` | `active` |
| `rule.lost_job.dismissal_missing_contest_info.v1` | (`termination_form` = `dismissal` ȘI `document_states_contest_deadline_and_court` = `False`) | `include_requirement:dismissal_decision_with_contest_deadline_and_court`<br>`emit_warning:contest_information_missing` | `clm.lost_job.termination_decision` | `active` |
| `rule.lost_job.missing_history.v1` | `received_history_proof` = `False` | `include_requirement:employment_activity_and_seniority_document`<br>`include_step:request_history_document_or_reges_extract` | `clm.lost_job.history_employer`, `clm.lost_job.history_extract` | `active` |
| `rule.lost_job.benefit_nonimputable.v1` | (`wants_unemployment_benefit` = `True` ȘI `termination_reason_class` = `non_imputable_confirmed`) | `trigger_child_event:ro.life.unemployment_benefit`<br>`include_step:prepare_unemployment_benefit_application` | `clm.lost_job.unemp_reason`, `clm.lost_job.unemp_conditions` | `active` |
| `rule.lost_job.benefit_imputable.v1` | (`wants_unemployment_benefit` = `True` ȘI `termination_reason_class` = `imputable_confirmed`) | `emit_warning:unemployment_benefit_nonimputable_condition_not_met` | `clm.lost_job.unemp_reason` | `active` |
| `rule.lost_job.benefit_unknown.v1` | (`wants_unemployment_benefit` = `True` ȘI `termination_reason_class` = `unknown`) | `require_confirmation:confirm_termination_reason_for_unemployment` | `clm.lost_job.unemp_reason` | `in_review` |
| `rule.lost_job.benefit_first_10_days.v1` | (`wants_unemployment_benefit` = `True` ȘI `filing_window` = `within_first_10_days`) | `emit_advice:file_within_10_days_for_start_from_termination` | `clm.lost_job.unemp_timing` | `active` |
| `rule.lost_job.benefit_after_10_before_12_months.v1` | (`wants_unemployment_benefit` = `True` ȘI `filing_window` = `after_10_days_within_12_months`) | `emit_advice:benefit_starts_from_application_date` | `clm.lost_job.unemp_timing` | `active` |
| `rule.lost_job.benefit_after_12_months.v1` | (`wants_unemployment_benefit` = `True` ȘI `filing_window` = `after_12_months`) | `block:unemployment_application_forfeiture_window_exceeded` | `clm.lost_job.unemp_timing` | `active` |
| `rule.lost_job.challenge.v1` | `wants_to_challenge` = `True` | `include_step:verify_contest_deadline_and_competent_court`<br>`emit_warning:act_immediately_on_contest_deadline` | `clm.lost_job.termination_decision` | `active` |
| `rule.lost_job.unused_leave_not_compensated.v1` | (`has_unused_leave` = `True` ȘI `unused_leave_compensated` = `False`) | `include_requirement:cash_compensation_for_unused_annual_leave_at_termination` | `clm.lost_job.unused_leave` | `active` |
| `rule.lost_job.reges_not_checked.v1` | `reges_record_checked` = `False` | `include_step:download_reges_extract_and_verify_termination` | `clm.lost_job.history_extract` | `active` |

## Termene, praguri și canale critice

| Element | Valoare modelată | Claim |
|---|---|---|
| Motiv eligibil șomaj | încetare din motive neimputabile | `clm.lost_job.unemp_reason` |
| Cerere în 10 zile | drept de la data încetării | `clm.lost_job.unemp_timing` |
| Termen maxim cerere | 12 luni | `clm.lost_job.unemp_timing` |
| Concediu neefectuat | compensabil în bani la încetare | `clm.lost_job.unused_leave` |

## Index surse

| Claim | Încredere | Nivel | URL |
|---|---|---|---|
| `clm.lost_job.termination_decision` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/informatii-utile/detalii-incetare/ |
| `clm.lost_job.history_employer` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.lost_job.history_extract` | `verified` | `national_normative` | https://legislatie.just.ro/Public/DetaliiDocument/128647 |
| `clm.lost_job.unemp_reason` | `verified` | `county` | https://www.anofm.ro/timis/indemnizatie-de-somaj-pentru-persoanele-cu-experienta-in-munca/ |
| `clm.lost_job.unemp_conditions` | `verified` | `county` | https://www.anofm.ro/timis/indemnizatie-de-somaj-pentru-persoanele-cu-experienta-in-munca/ |
| `clm.lost_job.unemp_timing` | `verified` | `county` | https://www.anofm.ro/timis/indemnizatie-de-somaj-pentru-persoanele-cu-experienta-in-munca/ |
| `clm.lost_job.unused_leave` | `verified` | `national_operational` | https://reges.inspectiamuncii.ro/ajutor/intrebari-frecvente/ |
