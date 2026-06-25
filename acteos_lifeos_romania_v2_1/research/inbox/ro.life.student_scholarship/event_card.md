# Event Card — ro.life.student_scholarship (life.student_scholarship)

## Metadata

| field | value |
|---|---|
| batch_id | B05_EDUCATION_1 |
| title_ro | Solicit bursă de student |
| trigger | solicit bursă de student |
| reference_date | 2026-06-25 |
| reference_period | cadru verificat la 2026-06-25; cuantum 2026-2027 neconfirmat |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | verified_with_local_gap |
| production_status | not_published |
| conflict_policy | Nu a fost identificat conflict oficial nerezolvat; orice conflict ulterior blochează efectul critic. |

## Scope

Burse universitare, cu reguli deterministe detaliate pentru bursa socială în instituții de stat. Celelalte tipuri rămân dependente de metodologia instituției și de ordinul anual al cuantumurilor.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| institution_sector | enum | true | false | Universitatea este de stat sau privată? | state, private |
| scholarship_type | enum | true | false | Ce bursă soliciți? | social, performance, study, dual, master_didactic, doctoral, occasional_social |
| study_mode | enum | true | false | Care este forma de învățământ? | full_time, part_time, distance |
| funding_place | enum | true | false | Locul este bugetat sau cu taxă? | budget, fee |
| student_age | integer | true | true | Ce vârstă are studentul? | — |
| promoted | boolean | true | true | Studentul este promovabil? | — |
| social_category | enum | true | true | Care este baza socială? | income, orphan, single_parent, placement, medical, none |
| income_below_threshold | boolean | false | true | Venitul mediu aplicabil este sub pragul legal? | — |
| no_family_income | boolean | false | true | Familia declară venit zero? | — |
| parent_abroad | boolean | false | true | Un părinte lucrează/locuiește în străinătate? | — |
| institution_method_verified | boolean | true | false | Metodologia și calendarul universității sunt verificate? | — |
| reference_date | date | true | false | La ce dată verificăm? | — |
| academic_year | string | true | false | Pentru ce an universitar verificăm bursa? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.sch.select_type | Selectează tipul de bursă | Tipul și cadrul juridic aplicabil sunt confirmate. | claim.sch.scope, claim.sch.social_fulltime_budget |
| step.sch.verify_eligibility | Verifică eligibilitatea socială | Forma, finanțarea, vârsta, promovabilitatea și categoria sunt validate. | claim.sch.social_fulltime_budget, claim.sch.social_age, claim.sch.social_categories |
| step.sch.calculate_income | Calculează venitul pe perioada și gospodăria corectă | Calculul are documente suport și respectă grupa de vârstă. | claim.sch.income_age_method |
| step.sch.verify_institution_method | Verifică metodologia și calendarul universității | Există URL oficial, termen, listă de documente și cuantum curent. | claim.sch.announcement_15_days, claim.sch.institution_method |
| step.sch.prepare_dossier | Pregătește dosarul | Cererea, declarațiile și actele categoriei sunt complete. | claim.sch.documents_inquiry |
| step.sch.submit | Depune cererea în termen | Există număr/confirmare de depunere. | claim.sch.announcement_15_days |
| step.sch.check_result | Verifică lista și contestația instituțională | Rezultatul și, dacă este cazul, contestația sunt arhivate. | claim.sch.institution_method |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.sch.application | Cerere de bursă socială | mandatory | now | claim.sch.documents_inquiry |
| req.sch.income_declaration | Declarația veniturilor nete permanente | mandatory | now | claim.sch.documents_inquiry |
| req.sch.data_consent | Acord privind prelucrarea datelor | mandatory | now | claim.sch.documents_inquiry |
| req.sch.category_documents | Actele care dovedesc categoria socială/medicală | conditional | now | claim.sch.social_categories |
| req.sch.social_inquiry | Anchetă socială | conditional | now | claim.sch.documents_inquiry |
| req.sch.institution_documents | Documentele suplimentare prevăzute de metodologia instituției | conditional | now | claim.sch.institution_method |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.sch.order | web | Ministerul Educației — Ordinul nr. 6.463/2023 actualizat 2026 | https://www.edu.ro/sites/default/files/fisiere%20articole/Ordin_6463_2023_reactualizat_2026.pdf | SOURCE_ONLY |
| ch.sch.facilities | web | Ministerul Educației — facilități studenți | https://www.edu.ro/facilitati-studenti | SOURCE_ONLY |
| ch.sch.institution | web | Portalul oficial al universității selectate | https://admitere.uvt.ro/ | NOT_CONFIGURED |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.sch.scope | verified | national_normative | Ordin, art. 1; anexă, titlu și art. 1 |
| claim.sch.social_fulltime_budget | verified | national_normative | Art. 10 alin. (8) |
| claim.sch.social_age | verified | national_normative | Art. 10 alin. (8) |
| claim.sch.no_academic_extra | verified | national_normative | Art. 10 alin. (6) |
| claim.sch.social_categories | verified | national_normative | Art. 10 alin. (9) |
| claim.sch.income_age_method | verified | national_normative | Art. 12 alin. (1)-(2) |
| claim.sch.documents_inquiry | verified | national_normative | Art. 13 alin. (2) |
| claim.sch.announcement_15_days | verified | national_normative | Art. 19 alin. (3) |
| claim.sch.amount_2025_26_only | verified_with_local_gap | national_operational | Cadru normativ — Ordinul nr. 6.633/2025 |
| claim.sch.institution_method | verified_with_local_gap | national_normative | Art. 10 alin. (2), (5) și art. 19 alin. (2) |

## Release guard

- National effects may be evaluated only from claims marked `verified` and still fresh.
- Institution/UAT-specific dates, places, fees, criteria, schedules or document variants remain `verified_with_local_gap` or `needs_confirmation` until independently reviewed.
- This pack is research input; `rules.yaml` remains `draft`/`in_review` and is not an active ruleset.
