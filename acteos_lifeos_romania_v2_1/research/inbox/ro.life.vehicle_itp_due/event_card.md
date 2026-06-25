# Event Card — ro.life.vehicle_itp_due (life.vehicle_itp_due)

## Metadata

| field | value |
|---|---|
| batch_id | B15_VEHICLES_2_MISC |
| title_ro | Inspecția tehnică periodică a vehiculului |
| trigger | ITP se apropie de termen sau nu este confirmată |
| reference_date | 2026-06-25 |
| reference_period | 2026 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | verified_with_local_gap |
| production_status | not_published |
| conflict_policy | Orice conflict oficial nerezolvat blochează efectul critic; motorul nu alege arbitrar o sursă. |

## Scope

Determinarea valabilității și periodicității ITP și pregătirea inspecției într-o stație autorizată. Exclude omologarea, certificarea modificărilor constructive și inspecțiile RAR speciale.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| vehicle_use | enum | true | false | Ce categorie/utilizare are vehiculul? | private_passenger, taxi, rental, ride_hailing, passenger_over_8, goods_le_3_5, goods_gt_3_5, ambulance, motorcycle, motorhome, driving_school, historic, trailer_le_3_5, other |
| vehicle_age_years | number | true | false | Câți ani are vehiculul? | — |
| first_itp | boolean | true | false | Este prima ITP? | — |
| itp_due_date | date | false | false | Ce dată de expirare apare în act/verificarea RAR? | — |
| itp_status | enum | true | false | Care este starea ITP? | valid, due_soon, expired, cancelled, unknown |
| plans_public_road_use | boolean | true | false | Vrei să circuli pe drum public? | — |
| reference_date | date | true | false | La ce dată verificăm? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.itp.check_date | Verifică data exactă a ITP | Data din anexa certificatului sau verificarea RAR este salvată. | claim.itp.date_source |
| step.itp.identify_period | Identifică periodicitatea aplicabilă | Categoria, utilizarea și vechimea vehiculului sunt confirmate. | claim.itp.six_months, claim.itp.one_year, claim.itp.two_years, claim.itp.passenger_12_years |
| step.itp.book_station | Alege o stație ITP autorizată | Stația aleasă este autorizată pentru categoria vehiculului. | claim.itp.authorized_station |
| step.itp.complete | Efectuează ITP înainte de expirare | Inspecția este finalizată și valabilitatea este actualizată. | claim.itp.required, claim.itp.certificate_automatic |
| step.itp.stop_road_use | Oprește circulația pe drum public | Vehiculul nu mai este folosit pe drum public până la restabilirea ITP. | claim.itp.no_road_expired |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.itp.valid_status | ITP valabil pentru circulația pe drum public | mandatory | before_public_road_use | claim.itp.no_road_expired |
| req.itp.authorized_station | Stație ITP autorizată | mandatory | for_inspection | claim.itp.authorized_station |
| req.itp.vehicle_category | Categoria și utilizarea corectă a vehiculului | mandatory | before_period_calculation | claim.itp.six_months, claim.itp.one_year, claim.itp.two_years |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.itp.verify | web | RAR — verificare ITP | https://prog.rarom.ro/rarpol/rarpol.asp | DEEP_LINK |
| ch.itp.info | web | RAR — informații ITP | https://www.rarom.ro/?page_id=776 | SOURCE_ONLY |
| ch.itp.rntr | pdf | RAR — RNTR 1 | https://www.rarom.ro/cs-uploads/RNTR%201.pdf | SOURCE_ONLY |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.itp.required | verified | national_normative | OUG nr. 195/2002, art. 9 alin. (4) |
| claim.itp.no_road_expired | verified | national_normative | OUG nr. 195/2002, art. 10 alin. (1) |
| claim.itp.authorized_station | verified | national_normative | OUG nr. 195/2002, art. 9 alin. (5) |
| claim.itp.six_months | verified | national_operational | RNTR 1, art. 5 alin. (1) |
| claim.itp.one_year | verified | national_operational | RNTR 1, art. 5 alin. (1) |
| claim.itp.two_years | verified | national_operational | RNTR 1, art. 5 alin. (1) |
| claim.itp.passenger_12_years | verified | national_operational | RNTR 1, art. 5 alin. (1) |
| claim.itp.first_new_passenger | verified | national_operational | RNTR 1, art. 5 alin. (2) |
| claim.itp.first_motorhome | verified | national_operational | RNTR 1, art. 5 alin. (2) |
| claim.itp.date_source | verified | national_operational | Pagina „Certificat de Inspecție Tehnică Periodică” |
| claim.itp.certificate_automatic | verified | national_operational | Pagina „Certificat de Inspecție Tehnică Periodică” |

## Release guard

- Efectele naționale pot fi evaluate numai din claim-uri `verified`, încă aplicabile și suficient de proaspete.
- Datele de instituție/UAT, taxele, programările, documentele contractuale și procedurile dependente de stat ori asigurător rămân `verified_with_local_gap`, `needs_confirmation` sau `conflicting` până la revizuire.
- `rules.yaml` este material de cercetare în starea `draft`; nu reprezintă un ruleset publicat.
