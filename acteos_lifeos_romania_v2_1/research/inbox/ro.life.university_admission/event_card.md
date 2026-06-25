# Event Card — ro.life.university_admission (life.university_admission)

## Metadata

| field | value |
|---|---|
| batch_id | B05_EDUCATION_1 |
| title_ro | Mă înscriu la facultate |
| trigger | mă înscriu la facultate |
| reference_date | 2026-06-25 |
| reference_period | admitere universitară 2026-2027 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | verified_with_local_gap |
| production_status | not_published |
| conflict_policy | Nu a fost identificat conflict oficial nerezolvat; orice conflict ulterior blochează efectul critic. |

## Scope

Admitere la cicluri universitare. Cadrul național stabilește eligibilitatea și limitele, iar universitatea stabilește calendarul, probele, actele și taxele. Pilot local: instituții din Timișoara.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| cycle | enum | true | false | Pentru ce ciclu aplici? | short_cycle, bachelor, master, doctorate |
| selected_institution_id | string | true | false | La ce universitate aplici? | — |
| selected_program_id | string | true | false | La ce program aplici? | — |
| entry_diploma_available | boolean | true | true | Ai diploma/adeverința de acces? | — |
| cumulative_ects | integer | false | true | Pentru doctorat, câte credite ECTS cumulate ai? | — |
| citizenship_category | enum | true | false | Care este categoria de cetățenie? | romanian, eu_eea_swiss, uk_wa_family, third_country |
| requested_funding | enum | true | false | Soliciți buget sau taxă? | budget, fee |
| already_budget_funded_same_cycle | boolean | false | true | Ai beneficiat deja de buget în același ciclu? | — |
| simultaneous_program_count_after_enrollment | integer | true | true | La câte programe ai fi înmatriculat simultan? | — |
| institution_rules_verified | boolean | true | false | Regulamentul 2026 și calendarul sunt verificate? | — |
| online_submission_requested | boolean | false | false | Dorești înscriere online? | — |
| reference_date | date | true | false | La ce dată verificăm admiterea? | — |
| foreign_diploma | boolean | false | false | Diploma de acces este emisă în străinătate? | — |
| recognition_document_available | boolean | false | true | Ai documentul de recunoaștere/echivalare? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.uni.choose_program | Alege instituția și programul | Programul este în oferta oficială 2026-2027 și are capacitate publicată. | claim.uni.institution_regulation, claim.uni.publication_six_months |
| step.uni.verify_eligibility | Verifică diploma de acces și condițiile | Ciclul și actul de studii eligibil sunt confirmate. | claim.uni.bachelor_eligibility, claim.uni.cycles |
| step.uni.verify_regulation | Verifică regulamentul, calendarul, probele și taxele | Toate valorile instituționale au URL oficial și dată de verificare. | claim.uni.publication_six_months, claim.uni.timisoara.channels |
| step.uni.prepare_dossier | Pregătește dosarul instituțional | Documentele cerute de program sunt complete. | claim.uni.institution_regulation |
| step.uni.submit | Depune și achită numai prin canalul oficial | Există confirmare de înscriere și dovada plății, dacă este aplicabilă. | claim.uni.online, claim.uni.institution_regulation |
| step.uni.take_exam | Susține probele programului | Rezultatul/nota este publicată în portalul oficial. | claim.uni.publication_six_months |
| step.uni.confirm_place | Confirmă locul și finanțarea | Locul este confirmat, actul original depus dacă este buget și contractul semnat. | claim.uni.budget_original, claim.uni.concurrent_programs |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.uni.entry_diploma | Diploma/adeverința care permite accesul la ciclu | mandatory | now | claim.uni.bachelor_eligibility, claim.uni.cycles |
| req.uni.institution_dossier | Documentele cerute de regulamentul instituției | mandatory | now | claim.uni.institution_regulation |
| req.uni.original_budget | Actul de studii în original pentru confirmarea locului bugetat | conditional | later | claim.uni.budget_original |
| req.uni.recognition | Atestat/adeverință de recunoaștere a studiilor din străinătate | conditional | now | claim.uni.budget_original |
| req.uni.fee_proof | Dovada taxei de înscriere stabilite de instituție | conditional | now | claim.uni.publication_six_months |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.uni.methodology | web | Ministerul Educației — metodologia-cadru admitere | https://www.edu.ro/sites/default/files/fisiere%20articole/OM_3693_2024.pdf | SOURCE_ONLY |
| ch.uni.uvt | web | UVT — portal oficial admitere | https://admitere.uvt.ro/ | DEEP_LINK |
| ch.uni.upt | web | UPT — portal oficial admitere | https://www.upt.ro/admitere | DEEP_LINK |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.uni.bachelor_eligibility | verified | national_operational | Secțiunea „Admiterea” |
| claim.uni.institution_regulation | verified | national_normative | Art. 3 alin. (1) |
| claim.uni.publication_six_months | verified | national_normative | Art. 3 alin. (5) și art. 9 alin. (2) |
| claim.uni.online | verified | national_normative | Art. 4 alin. (3) |
| claim.uni.sessions_deadline | verified | national_normative | Art. 9 alin. (1) |
| claim.uni.cycles | verified | national_normative | Art. 10 alin. (1)-(4) |
| claim.uni.concurrent_programs | verified | national_normative | Art. 14 alin. (1)-(2) |
| claim.uni.budget_original | verified | national_normative | Art. 14 alin. (3) |
| claim.uni.eu_equal_conditions | verified | national_normative | Art. 11 alin. (1) |
| claim.uni.timisoara.channels | verified_with_local_gap | institution | Portal oficial admitere |

## Release guard

- National effects may be evaluated only from claims marked `verified` and still fresh.
- Institution/UAT-specific dates, places, fees, criteria, schedules or document variants remain `verified_with_local_gap` or `needs_confirmation` until independently reviewed.
- This pack is research input; `rules.yaml` remains `draft`/`in_review` and is not an active ruleset.
