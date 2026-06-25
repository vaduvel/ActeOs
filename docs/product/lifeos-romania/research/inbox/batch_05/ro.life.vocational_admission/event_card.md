# Event Card — ro.life.vocational_admission (life.vocational_admission)

## Metadata

| field | value |
|---|---|
| batch_id | B05_EDUCATION_1 |
| title_ro | Înscriere la învățământ profesional/dual |
| trigger | înscriere la învățământ profesional sau dual |
| reference_date | 2026-06-25 |
| reference_period | admitere 2026-2027 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | verified_with_local_gap |
| production_status | not_published |
| conflict_policy | Nu a fost identificat conflict oficial nerezolvat; orice conflict ulterior blochează efectul critic. |

## Scope

Două ramuri distincte: absolvent de clasa a VIII-a spre clasa a IX-a tehnologic/dual și absolvent cu nivel 3 spre calificare duală nivel 4. Procedurile instituționale și operatorii se confirmă separat.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| entry_path | enum | true | false | Din ce rută intră candidatul? | grade8_to_grade9, level3_to_level4 |
| study_form | enum | true | false | Ce formă urmărește? | day, evening |
| reference_date | date | true | false | La ce dată verificăm? | — |
| previously_enrolled | boolean | true | false | A fost deja înmatriculat pe ruta vizată? | — |
| level3_certificate | boolean | false | true | Are certificat de calificare nivel 3? | — |
| same_training_field | boolean | false | false | Calificarea nivel 3 este din același domeniu? | — |
| age_within_day_limit | boolean | false | true | Respectă limita de vârstă a formei de zi? | — |
| school_situation_closed | boolean | false | true | Situația școlară este încheiată și promovată? | — |
| target_program_id | string | true | false | Ce program/unitate alege? | — |
| unit_procedure_verified | boolean | true | false | Procedura unității este verificată? | — |
| pilot_unit | boolean | false | false | Unitatea este nominalizată într-un pilot? | — |
| unit_tests_required | boolean | false | false | Unitatea organizează probe de admitere? | — |
| admitted | boolean | false | true | Candidatul este declarat admis? | — |
| evaluation_national_taken | boolean | false | true | Candidatul a susținut Evaluarea Națională? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.voc.select_path | Selectează ruta și forma | Este stabilit dacă se aplică admiterea de clasa a IX-a sau nivel 3→4. | claim.voc.grade8.framework, claim.voc.level4.scope |
| step.voc.verify_eligibility | Verifică eligibilitatea | Certificatul, domeniul, vârsta și situația școlară sunt confirmate. | claim.voc.level4.day_eligibility, claim.voc.level4.evening_eligibility, claim.voc.level4.no_sheet |
| step.voc.verify_offer | Verifică oferta, operatorul și procedura | Programul, locurile, operatorul și probele au surse oficiale curente. | claim.voc.unit_procedure, claim.voc.timis.offer |
| step.voc.obtain_sheet | Obține și depune fișa de înscriere | Fișa este emisă și înregistrată. | claim.voc.level4.calendar, claim.voc.level4.no_sheet |
| step.voc.take_tests | Susține probele prevăzute de unitate | Rezultatul final al probelor este publicat. | claim.voc.level4.calendar, claim.voc.unit_procedure |
| step.voc.submit_dossier | Depune dosarul la unitatea admisă | Înmatricularea este confirmată de unitate. | claim.voc.level4.calendar, claim.voc.grade8.calendar |
| step.voc.second_stage | Folosește etapa a II-a pentru locurile rămase | Cererea și repartizarea din etapa a II-a sunt confirmate. | claim.voc.level4.calendar |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.voc.registration_sheet | Fișa de înscriere | mandatory | now | claim.voc.level4.calendar |
| req.voc.level3_certificate | Certificatul de calificare profesională nivel 3 | conditional | now | claim.voc.level4.day_eligibility |
| req.voc.identity_birth | Act identitate și certificat de naștere | mandatory | later | claim.voc.level4.calendar |
| req.voc.unit_documents | Documentele stabilite de procedura unității | conditional | now | claim.voc.unit_procedure |
| req.voc.test_result | Rezultatul probelor de admitere, dacă sunt organizate | conditional | later | claim.voc.unit_procedure |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.voc.grade8 | web | Portal Legislativ — admitere clasa a IX-a 2026-2027 | https://legislatie.just.ro/Public/DetaliiDocument/301910 | SOURCE_ONLY |
| ch.voc.level4 | web | Portal Legislativ — Ordinul nr. 6.422/2025 | https://legislatie.just.ro/Public/DetaliiDocument/302690 | DEEP_LINK |
| ch.voc.isjtm | web | ISJ Timiș — oferta și procedurile locale | https://www.isj.tm.edu.ro/examene-nationale/admitere | SOURCE_ONLY |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.voc.grade8.framework | verified | national_normative | Art. 1-2 și anexele |
| claim.voc.grade8.calendar | verified | national_normative | Anexa nr. 1, secțiunea G |
| claim.voc.level4.scope | verified | national_normative | Art. 1 |
| claim.voc.level4.day_eligibility | verified | national_normative | Art. 5 |
| claim.voc.level4.evening_eligibility | verified | national_normative | Art. 6 |
| claim.voc.level4.prior_enrolled | verified | national_normative | Art. 8 |
| claim.voc.level4.calendar | verified | national_normative | Calendar, etapa I |
| claim.voc.level4.no_sheet | verified | national_normative | Anexă, eliberarea fișelor în etapa I |
| claim.voc.unit_procedure | verified | national_normative | Anexă, 27 februarie-2 martie 2026 |
| claim.voc.pilot_exception | verified_with_local_gap | national_normative | Anexa/aria ordinului |
| claim.voc.timis.offer | verified_with_local_gap | county | Pagina oficială admitere |
| claim.voc.grade8.no_en | verified | national_normative | Art. 2 alin. (26)-(27) |

## Release guard

- National effects may be evaluated only from claims marked `verified` and still fresh.
- Institution/UAT-specific dates, places, fees, criteria, schedules or document variants remain `verified_with_local_gap` or `needs_confirmation` until independently reviewed.
- This pack is research input; `rules.yaml` remains `draft`/`in_review` and is not an active ruleset.
