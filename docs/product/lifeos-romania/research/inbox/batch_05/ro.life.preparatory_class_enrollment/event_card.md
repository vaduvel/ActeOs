# Event Card — ro.life.preparatory_class_enrollment (life.preparatory_class_enrollment)

## Metadata

| field | value |
|---|---|
| batch_id | B05_EDUCATION_1 |
| title_ro | Înscriu copilul în clasa pregătitoare |
| trigger | înscriu copilul în clasa pregătitoare |
| reference_date | 2026-06-25 |
| reference_period | an școlar 2026-2027 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | verified_with_local_gap |
| production_status | not_published |
| conflict_policy | Nu a fost identificat conflict oficial nerezolvat; orice conflict ulterior blochează efectul critic. |

## Scope

Înscrierea în clasa pregătitoare în învățământul de stat; include ruta de vârstă, recomandare/evaluare, circumscripție și calendar. Nu substituie procedurile școlilor private care nu urmează calendarul public.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| child.birth_date | date | true | true | Care este data nașterii copilului? | — |
| reference_date | date | true | false | La ce dată verificăm traseul? | — |
| school_choice | enum | true | false | Alegi școala de circumscripție sau alta? | catchment, other |
| child_attended_kindergarten | boolean | true | false | Copilul a frecventat grădinița? | — |
| child_returned_from_abroad | boolean | false | true | Copilul s-a întors din străinătate? | — |
| recommendation_positive | boolean | false | true | Există recomandare pozitivă pentru clasa pregătitoare? | — |
| cjrae_evaluation_positive | boolean | false | true | Evaluarea CJRAE este favorabilă? | — |
| target_school_id | string | true | false | Care este școala aleasă? | — |
| online_application | boolean | true | false | Cererea a fost completată online? | — |
| local_catchment_verified | boolean | true | false | Circumscripția exactă este verificată? | — |
| defer_requested | boolean | false | true | Soliciți amânarea înscrierii în clasa pregătitoare? | — |
| age_cohort | enum | false | true | În ce cohortă de vârstă se află copilul? | six_by_aug31, six_sep_dec, under_six_by_dec31 |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.prep.determine_age_route | Determină ruta de vârstă | Copilul este încadrat în cohorta până la 31 august sau 1 septembrie-31 decembrie. | claim.prep.age.august, claim.prep.age.september_december |
| step.prep.obtain_recommendation | Obține recomandarea grădiniței | Recomandarea este emisă și favorabilă. | claim.prep.age.september_december |
| step.prep.cjrae_evaluation | Solicită evaluarea CJRAE | Există rezultatul evaluării și acesta este favorabil. | claim.prep.evaluation.cjrae |
| step.prep.verify_catchment | Verifică circumscripția și locurile | Adresa completă este mapată la școala arondată dintr-un dataset oficial curent. | claim.prep.catchment, claim.prep.timis.catchments |
| step.prep.prepare_dossier | Pregătește dosarul | Cererea și toate actele aplicabile sunt prezente. | claim.prep.dossier_validation |
| step.prep.submit_validate | Depune și validează cererea | Cererea este validată și are confirmare/număr de înregistrare. | claim.prep.calendar.application, claim.prep.dossier_validation |
| step.prep.check_result | Verifică rezultatul | Rezultatul primei sau celei de-a doua etape este salvat. | claim.prep.calendar.stage2_result |
| step.prep.unresolved_route | Solicită soluționarea situației rămase | ISJ a repartizat copilul sau a comunicat soluția. | claim.prep.calendar.unresolved |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.prep.application | Cerere-tip de înscriere | mandatory | now | claim.prep.dossier_validation |
| req.prep.parent_id | Act identitate părinte/reprezentant | mandatory | now | claim.prep.dossier_validation |
| req.prep.birth_certificate | Certificatul de naștere al copilului | mandatory | now | claim.prep.dossier_validation |
| req.prep.recommendation | Recomandarea pentru înscriere | conditional | now | claim.prep.age.september_december |
| req.prep.cjrae_result | Rezultatul evaluării CJRAE/CMBRAE | conditional | now | claim.prep.evaluation.cjrae |
| req.prep.criteria_documents | Documente pentru criteriile școlii ne-arondată | conditional | now | claim.prep.catchment |
| req.prep.divorce_judgment | Hotărâre definitivă privind autoritatea părintească | conditional | now | claim.prep.dossier_validation |
| req.prep.defer_request | Cerere scrisă și documente justificative pentru amânare | conditional | now | claim.prep.defer |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.prep.edu_faq | web | Ministerul Educației — FAQ clasa pregătitoare 2026-2027 | https://www.edu.ro/intrebari_raspunsuri_inscriere_invatamant_primar | DEEP_LINK |
| ch.prep.calendar | web | Portal Legislativ — Ordinul nr. 3.334/2026 | https://legislatie.just.ro/Public/DetaliiDocument/307906 | SOURCE_ONLY |
| ch.prep.isjtm | web | ISJ Timiș — înscriere învățământ primar 2026-2027 | https://www.isj.tm.edu.ro/inscrieri/inscrierea-in-invatamantul-primar/anul-2026-2027 | SOURCE_ONLY |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.prep.calendar.application | verified | national_normative | Anexă, completarea și validarea cererilor |
| claim.prep.calendar.stage2 | verified | national_normative | Anexă, etapa a II-a — colectarea cererilor |
| claim.prep.calendar.unresolved | verified | national_normative | Anexă, soluționarea situațiilor rămase |
| claim.prep.age.august | verified | national_operational | Secțiunea vârsta de înscriere |
| claim.prep.age.september_december | verified | national_operational | Secțiunea recomandare/evaluare |
| claim.prep.evaluation.cjrae | verified | national_operational | Secțiunea evaluarea dezvoltării |
| claim.prep.defer | verified | national_operational | Secțiunea amânarea înscrierii |
| claim.prep.catchment | verified | national_operational | Secțiunea alegerea școlii |
| claim.prep.dossier_validation | verified | national_operational | Secțiunea completare online și documente |
| claim.prep.timis.catchments | verified_with_local_gap | county | Pagina 2026-2027, secțiunile circumscripții/locuri/CJRAE |
| claim.prep.calendar.stage2_result | verified | national_normative | Anexă, etapa a II-a — afișarea listelor finale |

## Release guard

- National effects may be evaluated only from claims marked `verified` and still fresh.
- Institution/UAT-specific dates, places, fees, criteria, schedules or document variants remain `verified_with_local_gap` or `needs_confirmation` until independently reviewed.
- This pack is research input; `rules.yaml` remains `draft`/`in_review` and is not an active ruleset.
