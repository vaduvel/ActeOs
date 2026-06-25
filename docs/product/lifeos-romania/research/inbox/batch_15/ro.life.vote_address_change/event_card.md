# Event Card — ro.life.vote_address_change (life.vote_address_change)

## Metadata

| field | value |
|---|---|
| batch_id | B15_VEHICLES_2_MISC |
| title_ro | Votarea după schimbarea domiciliului sau reședinței |
| trigger | alegătorul și-a schimbat adresa și vrea să știe unde și cum votează |
| reference_date | 2026-06-25 |
| reference_period | 2026 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | in_review |
| production_status | not_published |
| conflict_policy | Orice conflict oficial nerezolvat blochează efectul critic; motorul nu alege arbitrar o sursă. |

## Scope

Verificarea secției și a regulilor de domiciliu/reședință pentru alegeri locale, parlamentare și prezidențiale. Scrutinele europene și referendumurile rămân ramuri separate până la verificarea actului electoral curent.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| election_type | enum | true | false | Pentru ce tip de scrutin verifici? | local, parliamentary, presidential, european, referendum, unknown |
| address_kind | enum | true | true | Ai schimbat domiciliul sau ai stabilit reședința? | domicile, residence |
| residence_established_date | date | false | true | La ce dată a fost stabilită reședința? | — |
| election_date | date | true | false | Care este data scrutinului? | — |
| reference_date | date | true | false | La ce dată verificăm? | — |
| register_request_submitted | boolean | true | false | Ai depus cererea de înscriere la reședință în Registrul Electoral? | — |
| same_uat_as_registered_domicile | boolean | true | true | În ziua votului ești în aceeași UAT cu domiciliul? | — |
| mobility_reduced | boolean | true | true | Ai mobilitate redusă? | — |
| residence_registration_completed | boolean | true | true | Reședința este înscrisă valabil în act/evidențe? | — |
| target_uat | string | true | true | Care este UAT-ul noii adrese? | — |
| residence_over_6_months | boolean | false | false | La data scrutinului, reședința este stabilită de mai mult de 6 luni? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.vote.identify_election | Identifică regulile scrutinului | Tipul și data scrutinului sunt confirmate din actul oficial. | claim.vote.local_uat, claim.vote.parliamentary_45d, claim.vote.presidential_other_uat |
| step.vote.register_residence | Stabilește reședința, dacă aceasta este ruta aleasă | Mențiunea de reședință este valabilă. | claim.vote.timis_residence |
| step.vote.request_register | Depune cererea pentru Registrul Electoral când este necesar | Cererea este depusă în termenul de 45 de zile aplicabil. | claim.vote.local_residence_6m_45d, claim.vote.parliamentary_45d |
| step.vote.check_section | Verifică secția în Registrul Electoral | Secția de votare și adresa sunt salvate înainte de scrutin. | claim.vote.registry |
| step.vote.use_supplementary | Folosește lista suplimentară în condițiile scrutinului | Secția acceptă alegătorul conform regulii aplicabile. | claim.vote.presidential_other_uat |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.vote.valid_residence | Reședință valabil înregistrată | conditional | before_register_request | claim.vote.local_residence_6m_45d, claim.vote.parliamentary_45d |
| req.vote.register_request | Cerere pentru înscrierea la reședință | conditional | no_later_than_45_days_before | claim.vote.local_residence_6m_45d, claim.vote.parliamentary_45d |
| req.vote.identity | Act de identitate valabil la vot | mandatory | on_election_day | claim.vote.local_uat, claim.vote.presidential_same_uat |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.vote.registry | web | AEP — Registrul Electoral | https://www.registrulelectoral.ro/ | DEEP_LINK |
| ch.vote.timis_residence | web | Primăria Timișoara — viză de flotant | https://servicii.primariatm.ro/viza-flotant | DEEP_LINK |
| ch.vote.aep | web | Autoritatea Electorală Permanentă | https://www.roaep.ro/ | SOURCE_ONLY |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.vote.registry | verified | national_operational | Pagina principală Registrul Electoral |
| claim.vote.local_uat | verified | national_normative | Legea nr. 115/2015, art. 85 |
| claim.vote.local_residence_6m_45d | verified | national_normative | Legea nr. 115/2015, art. 18 |
| claim.vote.local_under6m | verified | national_normative | Legea nr. 115/2015, art. 18 |
| claim.vote.parliamentary_45d | verified | national_normative | Legea nr. 208/2015, art. 42 |
| claim.vote.presidential_other_uat | verified | national_normative | Legea nr. 370/2004, art. 44 |
| claim.vote.presidential_same_uat | verified | national_normative | Legea nr. 370/2004, art. 44 |
| claim.vote.reduced_mobility | verified | national_normative | Legea nr. 370/2004, art. 44 |
| claim.vote.timis_residence | verified_with_local_gap | local | Serviciul „Viză de flotant” |

## Release guard

- Efectele naționale pot fi evaluate numai din claim-uri `verified`, încă aplicabile și suficient de proaspete.
- Datele de instituție/UAT, taxele, programările, documentele contractuale și procedurile dependente de stat ori asigurător rămân `verified_with_local_gap`, `needs_confirmation` sau `conflicting` până la revizuire.
- `rules.yaml` este material de cercetare în starea `draft`; nu reprezintă un ruleset publicat.
