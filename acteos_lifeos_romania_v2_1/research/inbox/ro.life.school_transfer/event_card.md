# Event Card — ro.life.school_transfer (life.school_transfer)

## Metadata

| field | value |
|---|---|
| batch_id | B05_EDUCATION_1 |
| title_ro | Transfer copilul la altă școală |
| trigger | transfer copilul la altă școală |
| reference_date | 2026-06-25 |
| reference_period | reguli consolidate verificate la 2026-06-25 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | verified_with_local_gap |
| production_status | not_published |
| conflict_policy | Nu a fost identificat conflict oficial nerezolvat; orice conflict ulterior blochează efectul critic. |

## Scope

Transfer între unități/formațiuni/profiluri în învățământul preuniversitar. Nu include reînmatricularea după retragere sau admiterea inițială în clasa a IX-a.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| student.level | enum | true | false | La ce nivel este elevul? | antepreschool, preschool, primary, middle, grade9, grade10, grade11, grade12, postsecondary |
| reference_date | date | true | false | La ce dată este solicitat transferul? | — |
| during_school_courses | boolean | true | false | Cererea este în timpul cursurilor? | — |
| same_track_profile | boolean | true | false | Se păstrează filiera/profilul/specializarea? | — |
| receiving_capacity_available | boolean | true | false | Există loc în efectivul legal? | — |
| isj_exception_approved | boolean | false | false | Există aprobarea excepțională a inspectoratului? | — |
| receiving_ca_approved | boolean | true | false | Consiliul de administrație primitor a aprobat? | — |
| outgoing_ca_opinion | boolean | true | false | Unitatea de plecare a emis avizul consultativ? | — |
| exception_reason | enum | false | true | Există un motiv excepțional? | none, domicile_change, medical, violence_protection, other_official |
| admission_average_meets_threshold | boolean | false | true | Pentru clasa a IX-a, media îndeplinește pragul? | — |
| receiving_school_id | string | true | false | Care este școala primitoare? | — |
| institution_procedure_verified | boolean | true | false | Procedura unității este verificată? | — |
| dual_program | boolean | false | false | Programul este organizat în sistem dual? | — |
| refusal_written | boolean | false | false | Refuzul unității primitoare a fost comunicat în scris? | — |
| school_record_received | boolean | false | true | Situația școlară a ajuns la unitatea primitoare? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.transfer.verify_rules | Verifică nivelul, perioada și condițiile | Ruta aplicabilă este identificată din ROFUIP și regulamentul unității. | claim.transfer.right_framework, claim.transfer.timing |
| step.transfer.check_capacity | Confirmă locul și efectivul clasei | Unitatea confirmă în scris existența locului sau aprobarea inspectoratului. | claim.transfer.capacity |
| step.transfer.difference_exams | Stabilește și promovează diferențele | Lista disciplinelor și rezultatele examenelor sunt comunicate de unitatea primitoare. | claim.transfer.difference_exams |
| step.transfer.submit_request | Depune cererea la unitatea primitoare | Cererea are număr de înregistrare. | claim.transfer.approvals, claim.transfer.institution_procedure |
| step.transfer.obtain_decisions | Obține hotărârile consiliilor de administrație | Există acordul primitor și avizul consultativ al unității de plecare. | claim.transfer.approvals |
| step.transfer.request_written_refusal | Solicită motivarea scrisă a refuzului | Refuzul motivat este primit și arhivat. | claim.transfer.approvals |
| step.transfer.records | Urmărește transferul situației școlare | Situația școlară a ajuns la unitatea primitoare. | claim.transfer.records |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.transfer.application | Cererea de transfer | mandatory | now | claim.transfer.approvals |
| req.transfer.exception_proof | Dovada motivului excepțional | conditional | now | claim.transfer.in_year_exceptions |
| req.transfer.difference_results | Dovada promovării examenelor de diferență | conditional | later | claim.transfer.difference_exams |
| req.transfer.ca_approval | Acordul consiliului de administrație primitor | mandatory | later | claim.transfer.approvals |
| req.transfer.outgoing_opinion | Avizul consultativ al unității de plecare | mandatory | later | claim.transfer.approvals |
| req.transfer.local_documents | Documentele stabilite de unitatea primitoare | conditional | now | claim.transfer.institution_procedure |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.transfer.rofuip | web | Portal Legislativ — ROFUIP consolidat | https://legislatie.just.ro/Public/DetaliiDocument/286955 | SOURCE_ONLY |
| ch.transfer.receiving_school | physical | Secretariatul unității primitoare | https://www.isj.tm.edu.ro/ | NOT_CONFIGURED |
| ch.transfer.isjtm | web | ISJ Timiș — canal de escaladare/competență | https://www.isj.tm.edu.ro/ | SOURCE_ONLY |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.transfer.right_framework | verified | national_normative | Art. 137 |
| claim.transfer.approvals | verified | national_normative | Art. 138 alin. (1) |
| claim.transfer.capacity | verified | national_normative | Art. 139 |
| claim.transfer.difference_exams | verified | national_normative | Art. 140 |
| claim.transfer.grade9 | verified | national_normative | Art. 141 alin. (1) lit. a) |
| claim.transfer.timing | verified | national_normative | Art. 144 alin. (1) |
| claim.transfer.in_year_exceptions | verified | national_normative | Art. 144 alin. (5) |
| claim.transfer.records | verified | national_normative | Art. 150 |
| claim.transfer.institution_procedure | verified_with_local_gap | national_normative | Art. 137 coroborat cu art. 2 |

## Release guard

- National effects may be evaluated only from claims marked `verified` and still fresh.
- Institution/UAT-specific dates, places, fees, criteria, schedules or document variants remain `verified_with_local_gap` or `needs_confirmation` until independently reviewed.
- This pack is research input; `rules.yaml` remains `draft`/`in_review` and is not an active ruleset.
