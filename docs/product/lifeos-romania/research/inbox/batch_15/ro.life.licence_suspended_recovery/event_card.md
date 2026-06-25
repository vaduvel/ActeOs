# Event Card — ro.life.licence_suspended_recovery (life.licence_suspended_recovery)

## Metadata

| field | value |
|---|---|
| batch_id | B15_VEHICLES_2_MISC |
| title_ro | Recuperarea permisului după suspendare |
| trigger | permisul este suspendat și titularul trebuie să îndeplinească testul, plata sau termenul aplicabil |
| reference_date | 2026-06-25 |
| reference_period | 2026 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | verified_with_local_gap |
| production_status | not_published |
| conflict_policy | Orice conflict oficial nerezolvat blochează efectul critic; motorul nu alege arbitrar o sursă. |

## Scope

Determinarea testului obligatoriu, a eligibilității pentru reducerea perioadei, a autorității competente la data testului și a condițiilor de recuperare. Exclude contestarea procesului-verbal și dosarele penale individuale.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| suspension_reason | enum | true | false | Care este motivul suspendării? | alcohol, priority_accident, overtaking_accident, red_light_accident, wrong_way_accident, points, speed, other, criminal_case_180 |
| suspension_end_date | date | true | false | Care este data comunicată pentru finalul suspendării? | — |
| reference_date | date | true | false | La ce dată verificăm? | — |
| wants_reduction | boolean | true | false | Vrei reducerea perioadei? | — |
| licence_age_years | number | true | false | De cât timp deții permisul? | — |
| test_passed | boolean | true | false | Ai promovat testul? | — |
| all_local_traffic_fines_paid | boolean | true | true | Sunt achitate toate amenzile rutiere datorate bugetului local? | — |
| no_ro_domicile | boolean | true | true | Nu ai domiciliul în România? | — |
| triggering_fine_paid | boolean | true | true | Este achitată amenda care a determinat suspendarea? | — |
| repeated_15_points_12m | boolean | true | false | Ai repetat cumulul de 15 puncte în intervalul legal de excludere? | — |
| period_already_increased | boolean | true | false | Perioada a fost deja majorată conform legii? | — |
| aggregated_serious_period | boolean | true | false | Suspendarea rezultă din cumularea unor perioade grave excluse de la reducere? | — |
| mandatory_test_completed | boolean | true | false | Ai susținut/promovat testul obligatoriu înainte de expirare? | — |
| notice_received_for_points | boolean | false | false | Ai primit înștiințarea pentru suspendarea prin puncte? | — |
| licence_surrendered | boolean | false | false | Ai predat permisul în termen? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.lsr.read_decision | Verifică motivul și perioada din actul oficial | Motivul, începutul și sfârșitul suspendării sunt confirmate. | claim.lsr.mandatory_test, claim.lsr.reduction_exclusions |
| step.lsr.test | Susține testul când este obligatoriu sau pentru reducere | Testul de 15 întrebări este promovat cu minimum 13 răspunsuri corecte. | claim.lsr.test_score, claim.lsr.mandatory_test |
| step.lsr.pay_fines | Achită amenzile cerute pentru reducere | Dovada fiscală necesară situației este disponibilă. | claim.lsr.reduction_conditions, claim.lsr.no_ro_domicile_fine |
| step.lsr.request_reduction | Depune cererea de reducere | Condițiile cumulative sunt demonstrate și nu există excluderi. | claim.lsr.reduction_conditions, claim.lsr.reduction_exclusions |
| step.lsr.choose_test_authority | Mergi la autoritatea competentă la data testului | Până la 30 iunie este poliția rutieră; din 1 iulie este SPCRPCIV. | claim.lsr.location_until_june, claim.lsr.location_from_july |
| step.lsr.surrender | Predă permisul la termen în cazul aplicabil | Predarea este înregistrată în termen. | claim.lsr.surrender_5d |
| step.lsr.recover | Ridică permisul după îndeplinirea condițiilor | Perioada este expirată și condițiile speciale sunt îndeplinite. | claim.lsr.mandatory_test, claim.lsr.plus_30 |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.lsr.test | Promovarea testului | conditional | before_expiry_or_reduction_request | claim.lsr.mandatory_test, claim.lsr.reduction_conditions, claim.lsr.test_score |
| req.lsr.fines | Plata amenzilor cerute pentru reducere | conditional | before_reduction_request | claim.lsr.reduction_conditions, claim.lsr.no_ro_domicile_fine |
| req.lsr.one_year_licence | Permis deținut cel puțin un an | conditional | for_reduction | claim.lsr.reduction_conditions |
| req.lsr.no_exclusion | Nicio excludere legală de la reducere | conditional | for_reduction | claim.lsr.reduction_exclusions |
| req.lsr.surrender | Predarea permisului în termen | conditional | within_notice_term | claim.lsr.surrender_5d |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.lsr.police | web | Poliția Română — structură rutieră | https://politiaromana.ro/ | SOURCE_ONLY |
| ch.lsr.timis_spcrpciv | web | SPCRPCIV Timiș | https://tm.prefectura.mai.gov.ro/permise-auto-si-inmatriculari/ | SOURCE_ONLY |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.lsr.reduction_conditions | verified | national_normative | OUG nr. 195/2002, art. 104 alin. (1) |
| claim.lsr.no_ro_domicile_fine | verified | national_normative | OUG nr. 195/2002, art. 104 alin. (1) |
| claim.lsr.reduction_exclusions | verified | national_normative | OUG nr. 195/2002, art. 104 alin. (2) |
| claim.lsr.mandatory_test | verified | national_normative | OUG nr. 195/2002, art. 106^1 |
| claim.lsr.plus_30 | verified | national_normative | OUG nr. 195/2002, art. 106^1 |
| claim.lsr.location_until_june | verified | national_normative | Dispoziție tranzitorie OUG nr. 195/2002 |
| claim.lsr.location_from_july | verified | national_normative | Dispoziție tranzitorie OUG nr. 195/2002 |
| claim.lsr.test_score | verified | national_normative | HG nr. 1391/2006, art. 219 |
| claim.lsr.surrender_5d | verified | national_normative | OUG nr. 195/2002, art. 103 |

## Release guard

- Efectele naționale pot fi evaluate numai din claim-uri `verified`, încă aplicabile și suficient de proaspete.
- Datele de instituție/UAT, taxele, programările, documentele contractuale și procedurile dependente de stat ori asigurător rămân `verified_with_local_gap`, `needs_confirmation` sau `conflicting` până la revizuire.
- `rules.yaml` este material de cercetare în starea `draft`; nu reprezintă un ruleset publicat.
