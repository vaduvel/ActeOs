# Event Card — ro.life.study_equivalence_ro (life.study_equivalence_ro)

## Metadata

| field | value |
|---|---|
| batch_id | B05_EDUCATION_1 |
| title_ro | Echivalez studii făcute în străinătate |
| trigger | echivalez studii făcute în străinătate |
| reference_date | 2026-06-25 |
| reference_period | proceduri CNRED verificate la 2026-06-25 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | in_review |
| production_status | not_published |
| conflict_policy | Nu a fost identificat conflict oficial nerezolvat; orice conflict ulterior blochează efectul critic. |

## Scope

Recunoașterea/echivalarea în România a studiilor preuniversitare și universitare efectuate în străinătate. Rutele detaliate pentru bac și licență sunt modelate separat; profesiile reglementate sunt redirecționate către autoritatea competentă.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| study_level | enum | true | false | Ce studii/diplomă vrei să recunoști? | school_years, bac, vocational, postsecondary, bachelor, master, doctorate |
| applicant_citizenship | enum | true | false | Care este cetățenia solicitantului? | romanian, eu_eea_swiss, third_country |
| issuing_country_group | enum | true | false | În ce categorie intră statul emitent? | eu_eea_swiss, hague_apostille, bilateral_exempt, other |
| document_language | enum | true | false | În ce limbă este diploma? | romanian, english, french, spanish, italian, other |
| purpose | enum | true | false | Pentru ce folosești recunoașterea? | continue_studies, employment, regulated_profession, other |
| regulated_profession | boolean | true | false | Profesia este reglementată? | — |
| dossier_complete | boolean | true | false | Dosarul este complet? | — |
| authentication_complete | boolean | false | true | Apostila/supralegalizarea aplicabilă este făcută? | — |
| name_changed | boolean | false | true | Numele diferă față de diplomă? | — |
| procedure_channel | enum | true | false | Prin ce canal depui? | pcue, university, school_inspectorate, ministry_registry, mail_courier |
| reference_date | date | true | false | La ce dată verificăm? | — |
| decision_contested | boolean | false | false | Contești decizia de recunoaștere/echivalare? | — |
| fee_requested_by_channel | boolean | false | false | Canalul îți solicită plata unei taxe? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.eq.select_procedure | Selectează procedura CNRED/autoritatea competentă | Nivelul, scopul și autoritatea competentă sunt confirmate. | claim.eq.preuniversity_scope, claim.eq.university_scope, claim.eq.regulated_profession |
| step.eq.verify_authentication | Verifică apostila/supralegalizarea | Formalitatea aplicabilă statului emitent este confirmată. | claim.eq.bac_documents, claim.eq.bachelor_documents |
| step.eq.prepare_translation | Pregătește traducerea aplicabilă | Traducerea legalizată este disponibilă când limba nu este acceptată direct. | claim.eq.bac_documents, claim.eq.bachelor_documents |
| step.eq.prepare_dossier | Pregătește dosarul complet | Diploma, foaia matricolă/suplimentul și actele personale sunt prezente. | claim.eq.bac_documents, claim.eq.bachelor_documents |
| step.eq.submit | Depune prin canalul oficial | Există confirmare și număr de dosar. | claim.eq.bac_channels |
| step.eq.track_term | Urmărește termenul de soluționare | Termenul calculat de la completarea dosarului este monitorizat. | claim.eq.preuniversity_term, claim.eq.university_scope |
| step.eq.contest | Depune contestație, dacă este cazul | Contestația este înregistrată în termenul procedurii aplicabile. | claim.eq.bac_contest, claim.eq.bachelor_contest |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.eq.application | Cererea procedurii selectate | mandatory | now | claim.eq.bac_channels |
| req.eq.diploma | Diploma/actul de studii | mandatory | now | claim.eq.bac_documents, claim.eq.bachelor_documents |
| req.eq.transcript | Foaie matricolă/supliment la diplomă | conditional | now | claim.eq.bachelor_documents |
| req.eq.identity | Act de identitate | mandatory | now | claim.eq.bac_documents, claim.eq.bachelor_documents |
| req.eq.name_change | Dovada schimbării numelui | conditional | now | claim.eq.bac_documents, claim.eq.bachelor_documents |
| req.eq.translation | Traducere legalizată în limba română | conditional | now | claim.eq.bac_documents, claim.eq.bachelor_documents |
| req.eq.authentication | Apostilă/supralegalizare, după stat | conditional | now | claim.eq.bac_documents, claim.eq.bachelor_documents |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.eq.pre | web | CNRED — studii preuniversitare | https://cnred.edu.ro/studii-preuniversitare/ | DEEP_LINK |
| ch.eq.bac | web | CNRED — echivalare diplomă de bacalaureat | https://cnred.edu.ro/echivalarea-diplomei-de-bacalaureat-obtinuta-in-strainatate-de-cetatenii-romani/ | DEEP_LINK |
| ch.eq.uni | web | CNRED — studii universitare | https://cnred.edu.ro/studii-universitare/ | DEEP_LINK |
| ch.eq.bachelor | web | CNRED — echivalare studii de licență | https://cnred.edu.ro/echivalare-studii-superioare-de-licenta-efectuate-in-strainatate/ | DEEP_LINK |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.eq.preuniversity_scope | verified | national_operational | Studii preuniversitare — prezentarea procedurii |
| claim.eq.preuniversity_term | verified | national_operational | Studii preuniversitare — durata soluționării |
| claim.eq.university_scope | verified | national_operational | Studii universitare — durata soluționării |
| claim.eq.eu_automatic | verified | national_operational | Studii preuniversitare — recunoaștere automată |
| claim.eq.bac_channels | verified | national_operational | Echivalarea diplomei de bacalaureat — depunerea dosarului |
| claim.eq.bac_documents | verified | national_operational | Echivalarea diplomei de bacalaureat — acte necesare |
| claim.eq.bac_contest | verified | national_operational | Echivalarea diplomei de bacalaureat — contestații |
| claim.eq.bachelor_documents | verified | national_operational | Echivalarea studiilor superioare de licență — acte necesare |
| claim.eq.bachelor_contest | verified | national_operational | Echivalarea studiilor superioare de licență — contestații |
| claim.eq.regulated_profession | verified | national_operational | Echivalarea studiilor superioare de licență — profesii reglementate |
| claim.eq.fee_unverified | needs_confirmation | national_operational | Paginile oficiale consultate nu afișează un cuantum unic pentru toate procedurile și canalele |

## Release guard

- National effects may be evaluated only from claims marked `verified` and still fresh.
- Institution/UAT-specific dates, places, fees, criteria, schedules or document variants remain `verified_with_local_gap` or `needs_confirmation` until independently reviewed.
- This pack is research input; `rules.yaml` remains `draft`/`in_review` and is not an active ruleset.
