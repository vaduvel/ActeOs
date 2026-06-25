# Event Card — ro.life.preschool_enrollment (life.preschool_enrollment)

## Metadata

| field | value |
|---|---|
| batch_id | B05_EDUCATION_1 |
| title_ro | Înscriu copilul la grădiniță |
| trigger | înscriu copilul la grădiniță |
| reference_date | 2026-06-25 |
| reference_period | an școlar 2026-2027 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | verified_with_local_gap |
| production_status | not_published |
| conflict_policy | Nu a fost identificat conflict oficial nerezolvat; orice conflict ulterior blochează efectul critic. |

## Scope

Înscriere/reînscriere la nivel preșcolar; interval național de vârstă 3–6 ani. Nu acoperă servicii private care nu urmează metodologia publică fără confirmare instituțională.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| child.birth_date | date | true | true | Care este data nașterii copilului? | — |
| reference_date | date | true | false | La ce dată verificăm traseul? | — |
| enrollment_mode | enum | true | false | Este reînscriere sau înscriere nouă? | reenrollment, new_enrollment |
| target_unit_id | string | true | false | La ce unitate dorești înscrierea? | — |
| program_type | enum | true | false | Ce program dorești? | normal, extended, weekly |
| submission_channel | enum | true | false | Cum depui cererea? | physical, email, post |
| same_unit_continuity | boolean | false | false | Copilul continuă în aceeași unitate? | — |
| criteria_invoked | boolean | false | true | Invoci criterii de departajare? | — |
| parents_divorced | boolean | false | true | Părinții sunt divorțați? | — |
| local_dataset_verified | boolean | true | false | Datele locale ale unității sunt verificate? | — |
| age_band | enum | false | false | În ce interval oficial de vârstă se încadrează copilul? | 3 luni–3 ani, 3–6 ani |
| age_eligible | boolean | false | false | Vârsta este eligibilă pentru nivelul ales? | — |
| application_accepted | boolean | false | false | Cererea a fost acceptată? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.preschool.identify_stage | Identifică etapa activă | Etapa este determinată din data de referință și modul de înscriere. | claim.preschool.calendar.stage1, claim.preschool.calendar.stage2, claim.preschool.calendar.adjustment |
| step.preschool.verify_unit | Verifică unitatea, locurile și criteriile | Există URL oficial, dată de verificare și confirmare pentru unitatea aleasă. | claim.preschool.choice_free_places, claim.preschool.local_publication_duty, claim.preschool.timis.local_dataset |
| step.preschool.prepare_dossier | Pregătește dosarul personalizat | Documentele obligatorii și condiționale aplicabile sunt prezente. | claim.preschool.dossier |
| step.preschool.submit | Depune cererea în fereastra activă | Există dovadă de depunere și dată. | claim.preschool.calendar.stage1_collection, claim.preschool.calendar.stage2_collection |
| step.preschool.validate | Validează cererea la unitate | Cererea este validată și există număr/confirmare de înregistrare. | claim.preschool.validation |
| step.preschool.medical | Pregătește documentele medicale la momentul corect | Adeverința clinică și avizul sunt valabile la începerea frecventării. | claim.preschool.medical |
| step.preschool.check_result | Verifică rezultatul și ruta următoare | Rezultatul este salvat; dacă cererea este respinsă, etapa următoare este identificată. | claim.preschool.calendar.stage1_result, claim.preschool.calendar.stage2_result, claim.preschool.calendar.adjustment |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.preschool.application | Cerere-tip cu trei opțiuni | mandatory | now | claim.preschool.dossier |
| req.preschool.birth_certificate | Copie certificat de naștere | mandatory | now | claim.preschool.dossier |
| req.preschool.parent_ids | Copii acte identitate părinți/reprezentant | mandatory | now | claim.preschool.dossier |
| req.preschool.employment | Adeverințe de angajat/concediu creștere | conditional | now | claim.preschool.dossier |
| req.preschool.criteria | Documente pentru criteriile invocate | conditional | now | claim.preschool.selection.criteria |
| req.preschool.remote_declaration | Declarație de veridicitate pentru e-mail/poștă | conditional | now | claim.preschool.dossier |
| req.preschool.parental_authority | Dovada autorității părintești/locuinței minorului | conditional | now | claim.preschool.dossier |
| req.preschool.originals | Originalele actelor pentru validare | mandatory | now | claim.preschool.validation |
| req.preschool.medical | Adeverință clinică și aviz epidemiologic/vaccinare | mandatory | later | claim.preschool.medical |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.preschool.edu_faq | web | Ministerul Educației — ghid oficial 2026-2027 | https://www.edu.ro/inscriere_invatamant_prescolar_anteprescolar_faq | DEEP_LINK |
| ch.preschool.calendar | web | Portal Legislativ — Ordinul nr. 3.707/2026 | https://legislatie.just.ro/Public/DetaliiDocument/309970 | SOURCE_ONLY |
| ch.preschool.isjtm | web | ISJ Timiș — portal oficial; pagina locală 2026-2027 trebuie confirmată | https://www.isj.tm.edu.ro/ | SOURCE_ONLY |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.preschool.calendar.reenrollment | verified | national_normative | Anexă, etapa de reînscrieri |
| claim.preschool.calendar.stage1 | verified | national_normative | Anexă, etapa I |
| claim.preschool.calendar.stage2 | verified | national_normative | Anexă, etapa a II-a |
| claim.preschool.calendar.adjustment | verified | national_normative | Anexă, etapa de ajustări |
| claim.preschool.age_range | verified | national_operational | Secțiunea „Ce copii pot fi înscriși” |
| claim.preschool.choice_free_places | verified | national_operational | Secțiunea „În ce unitate” |
| claim.preschool.selection.criteria | verified | national_operational | Secțiunea criterii de departajare |
| claim.preschool.dossier | verified | national_operational | Secțiunea „Ce documente conține dosarul” |
| claim.preschool.validation | verified | national_operational | Secțiunea validarea dosarului |
| claim.preschool.medical | verified | national_operational | Secțiunea documente medicale |
| claim.preschool.timis.local_dataset | expired | county | Titlul paginii oficiale ISJ Timiș |
| claim.preschool.calendar.stage1_collection | verified | national_normative | Anexă, etapa I — colectarea cererilor |
| claim.preschool.calendar.stage1_result | verified | national_normative | Anexă, etapa I — afișarea rezultatului |
| claim.preschool.calendar.stage2_collection | verified | national_normative | Anexă, etapa a II-a — colectarea cererilor |
| claim.preschool.calendar.stage2_result | verified | national_normative | Anexă, etapa a II-a — afișarea rezultatului |
| claim.preschool.local_publication_duty | verified | national_normative | Art. 13 alin. (1)-(2) |

## Release guard

- National effects may be evaluated only from claims marked `verified` and still fresh.
- Institution/UAT-specific dates, places, fees, criteria, schedules or document variants remain `verified_with_local_gap` or `needs_confirmation` until independently reviewed.
- This pack is research input; `rules.yaml` remains `draft`/`in_review` and is not an active ruleset.
