# Event Card — ro.life.vehicle_rca_due (life.vehicle_rca_due)

## Metadata

| field | value |
|---|---|
| batch_id | B15_VEHICLES_2_MISC |
| title_ro | Încheierea sau reînnoirea RCA |
| trigger | RCA expiră, este necunoscută ori trebuie suspendată/închisă legal |
| reference_date | 2026-06-25 |
| reference_period | 2026 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | verified_with_local_gap |
| production_status | not_published |
| conflict_policy | Orice conflict oficial nerezolvat blochează efectul critic; motorul nu alege arbitrar o sursă. |

## Scope

Verificarea, reînnoirea, suspendarea condiționată sau încetarea RCA la transferul proprietății. Exclude calculul primei, alegerea comercială a asigurătorului și instrumentarea completă a daunelor.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| owner_or_user | boolean | true | false | Ești proprietarul sau utilizatorul legal al vehiculului? | — |
| rca_status | enum | true | false | Care este starea RCA? | valid, expiring, expired, unknown |
| rca_expiry_date | date | false | false | La ce dată expiră RCA? | — |
| registration_suspended | boolean | true | false | Înmatricularea este suspendată? | — |
| parked_private_off_public | boolean | true | false | Vehiculul este imobilizat într-un spațiu privat, în afara domeniului public? | — |
| ownership_transferred | boolean | true | false | Proprietatea vehiculului a fost transferată? | — |
| insurer_notified_transfer | boolean | false | false | Asigurătorul a fost notificat cu documentele transferului? | — |
| plans_public_road_use | boolean | true | false | Vrei să utilizezi vehiculul pe drum public? | — |
| reference_date | date | true | false | La ce dată verificăm? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.rca.verify | Verifică polița și data expirării | Starea și data sunt confirmate în poliță sau baza oficială. | claim.rca.aida_channel |
| step.rca.compare_offers | Alege și încheie RCA înainte de expirare | Noua poliță are începutul de valabilitate corect și nu lasă pauză. | claim.rca.maintain, claim.rca.duration |
| step.rca.suspend_request | Solicită suspendarea efectelor RCA, dacă ești eligibil | Înmatricularea este suspendată și vehiculul este imobilizat privat. | claim.rca.suspension_conditions |
| step.rca.notify_transfer | Notifică asigurătorul despre transfer | Notificarea și actele justificative au fost primite de asigurător. | claim.rca.transfer_end |
| step.rca.stop_road_use | Nu utiliza vehiculul pe drum public | Vehiculul rămâne în afara drumului public până la RCA valabilă. | claim.rca.no_public_road |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.rca.valid_policy | RCA valabilă | mandatory | continuous_for_vehicle_use | claim.rca.maintain |
| req.rca.suspended_registration | Înmatriculare suspendată pentru suspendarea RCA | conditional | before_suspension_request | claim.rca.suspension_conditions |
| req.rca.private_immobilization | Imobilizare în spațiu privat | conditional | during_rca_suspension | claim.rca.suspension_conditions |
| req.rca.transfer_documents | Documente justificative ale transferului | conditional | with_transfer_notice | claim.rca.transfer_end |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.rca.aida | web | AIDA — verificare poliță RCA | https://www.aida.info.ro/polite-rca | DEEP_LINK |
| ch.rca.asf | web | ASF — informații asigurări | https://asfromania.ro/ro/ | SOURCE_ONLY |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.rca.maintain | verified | national_normative | Legea nr. 132/2017, art. 3 |
| claim.rca.reminder_30d | verified | national_normative | Legea nr. 132/2017, art. 18 alin. (8) |
| claim.rca.duration | verified | national_normative | Legea nr. 132/2017, art. 5 |
| claim.rca.suspension_conditions | verified | national_normative | Legea nr. 132/2017, art. 6 |
| claim.rca.transfer_end | verified | national_normative | Legea nr. 132/2017, art. 7 |
| claim.rca.no_public_road | verified | national_normative | OUG nr. 195/2002, art. 10 |
| claim.rca.aida_channel | verified | institution | Pagina „Verificare poliță RCA” |

## Release guard

- Efectele naționale pot fi evaluate numai din claim-uri `verified`, încă aplicabile și suficient de proaspete.
- Datele de instituție/UAT, taxele, programările, documentele contractuale și procedurile dependente de stat ori asigurător rămân `verified_with_local_gap`, `needs_confirmation` sau `conflicting` până la revizuire.
- `rules.yaml` este material de cercetare în starea `draft`; nu reprezintă un ruleset publicat.
