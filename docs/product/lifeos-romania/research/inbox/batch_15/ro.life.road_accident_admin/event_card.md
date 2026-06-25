# Event Card — ro.life.road_accident_admin (life.road_accident_admin)

## Metadata

| field | value |
|---|---|
| batch_id | B15_VEHICLES_2_MISC |
| title_ro | Actele și notificările după un accident rutier |
| trigger | s-a produs un accident sau o avariere care trebuie declarată și instrumentată |
| reference_date | 2026-06-25 |
| reference_period | 2026 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | verified_with_local_gap |
| production_status | not_published |
| conflict_policy | Orice conflict oficial nerezolvat blochează efectul critic; motorul nu alege arbitrar o sursă. |

## Scope

Trierea urgenței, constatarea amiabilă ori declararea la poliție, notificarea RCA și obținerea documentului pentru reparație. Nu stabilește culpa, despăgubirea sau strategia într-un dosar penal/civil.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| injuries | enum | true | true | Există persoane rănite? | yes, no, unknown |
| death | boolean | true | true | Există un deces? | — |
| dangerous_goods | boolean | true | false | Este implicat un vehicul cu mărfuri periculoase? | — |
| material_damage_only | boolean | true | false | Sunt numai pagube materiale? | — |
| vehicles_count | integer | true | false | Câte vehicule sunt implicate? | — |
| amicable_agreement_possible | boolean | true | false | Părțile pot și doresc constatare amiabilă? | — |
| own_vehicle_only | boolean | true | false | Este avariat numai propriul vehicul? | — |
| casco_available | boolean | true | false | Există asigurare facultativă aplicabilă? | — |
| event_context | enum | true | false | Avarierea s-a produs într-un accident de circulație? | road_accident, other_damage |
| hours_since_event | number | true | false | Câte ore au trecut de la eveniment/constatare? | — |
| moved_to_safety | boolean | false | false | Vehiculul a fost scos de pe carosabil când era posibil? | — |
| alcohol_consumed_after | boolean | true | true | S-a consumat alcool/substanțe după accident înainte de testare? | — |
| rca_insurer_notified | boolean | true | false | Asigurătorul RCA a fost notificat? | — |
| working_days_since_event | number | true | false | Câte zile lucrătoare au trecut? | — |
| reference_date | date | true | false | La ce dată verificăm? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.acc.emergency | Protejează persoanele și anunță urgența | 112 și poliția sunt anunțate; locul și urmele nu sunt modificate nelegal. | claim.acc.injury_emergency |
| step.acc.move_safe | Scoate vehiculele din carosabil când este posibil | Zona este eliberată și vehiculele sunt semnalizate. | claim.acc.material_move_report |
| step.acc.police_24h | Declară accidentul la poliția competentă | Prezentarea are loc în maximum 24 de ore când nu se aplică o excepție. | claim.acc.material_move_report, claim.acc.material_exceptions |
| step.acc.amicable | Completează constatarea amiabilă | Formularul este completat pentru exact două vehicule și numai pagube materiale. | claim.acc.amicable_scope |
| step.acc.notify_insurer | Notifică asigurătorul RCA | Notificarea și informațiile au fost transmise în 5 zile lucrătoare. | claim.acc.rca_notice_5wd |
| step.acc.obtain_repair_document | Obține documentul pentru reparație | Există constatare de la poliție sau asigurător. | claim.acc.repair_document |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.acc.call_112 | Apel 112 și anunțarea poliției | conditional | immediately | claim.acc.injury_emergency |
| req.acc.police_report | Prezentare la poliția competentă | conditional | within_24_hours | claim.acc.material_move_report, claim.acc.other_damage_24h |
| req.acc.amicable_two_vehicles | Exact două vehicule și numai prejudicii materiale | conditional | for_amicable | claim.acc.amicable_scope |
| req.acc.rca_notice | Notificarea asigurătorului RCA | mandatory | within_5_working_days | claim.acc.rca_notice_5wd |
| req.acc.repair_document | Document de constatare pentru reparație | mandatory | before_repair | claim.acc.repair_document |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.acc.112 | phone | Serviciul de urgență 112 | tel:112 | DEEP_LINK |
| ch.acc.police | web | Poliția Română — informații | https://politiaromana.ro/ | SOURCE_ONLY |
| ch.acc.rca | external | Asigurătorul RCA din poliță | — | USER_PROVIDED |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.acc.injury_emergency | verified | national_normative | OUG nr. 195/2002, art. 77 |
| claim.acc.no_alcohol_after | verified | national_normative | OUG nr. 195/2002, art. 78 |
| claim.acc.material_move_report | verified | national_normative | OUG nr. 195/2002, art. 79 alin. (1) |
| claim.acc.material_exceptions | verified | national_normative | OUG nr. 195/2002, art. 79 alin. (2) |
| claim.acc.other_damage_24h | verified | national_normative | OUG nr. 195/2002, art. 80 |
| claim.acc.amicable_scope | verified | national_normative | Legea nr. 132/2017, art. 17 |
| claim.acc.rca_notice_5wd | verified | national_normative | Legea nr. 132/2017, art. 15 |
| claim.acc.repair_document | verified | national_normative | OUG nr. 195/2002, art. 80^1 |

## Release guard

- Efectele naționale pot fi evaluate numai din claim-uri `verified`, încă aplicabile și suficient de proaspete.
- Datele de instituție/UAT, taxele, programările, documentele contractuale și procedurile dependente de stat ori asigurător rămân `verified_with_local_gap`, `needs_confirmation` sau `conflicting` până la revizuire.
- `rules.yaml` este material de cercetare în starea `draft`; nu reprezintă un ruleset publicat.
