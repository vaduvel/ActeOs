# Event Card — ro.life.driving_licence_foreign_exchange (life.driving_licence_foreign_exchange)

## Metadata

| field | value |
|---|---|
| batch_id | B15_VEHICLES_2_MISC |
| title_ro | Preschimbarea permisului străin cu unul românesc |
| trigger | titularul dorește schimbarea unui permis emis de alt stat |
| reference_date | 2026-06-25 |
| reference_period | 2026 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | in_review |
| production_status | not_published |
| conflict_policy | Orice conflict oficial nerezolvat blochează efectul critic; motorul nu alege arbitrar o sursă. |

## Scope

Verificarea eligibilității și pregătirea depunerii personale pentru preschimbarea unui permis național străin. Exclude obținerea prin examen, recunoașterea dreptului de a conduce fără preschimbare și permisele diplomatice/militare neconfirmate.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| issuing_country | string | true | false | Ce stat a emis permisul? | — |
| country_eligibility_verified | boolean | true | false | Statul și tipul permisului sunt verificate în anexa oficială aplicabilă? | — |
| licence_type | enum | true | false | Ce tip de document ai? | national, international, provisional, learner, unknown |
| licence_status | enum | true | false | Care este starea permisului? | valid, expired, suspended, cancelled, lost, stolen, unknown |
| residence_in_romania | boolean | true | false | Ai domiciliu sau reședință în România? | — |
| target_county | string | true | false | În ce județ ai domiciliul/reședința? | — |
| original_licence_available | boolean | true | false | Ai permisul original? | — |
| translation_required | boolean | true | false | Este necesară traducerea în română pentru documentele tale? | — |
| translation_available | boolean | true | false | Ai traducerea conformă? | — |
| new_administrative_validity_requested | boolean | true | false | Soliciți o nouă valabilitate administrativă? | — |
| medical_certificate_available | boolean | true | true | Ai fișa medicală de la unitate autorizată? | — |
| identity_and_residence_proof | boolean | true | true | Ai actul de identitate și dovada adresei? | — |
| criminal_record_route_ready | boolean | true | true | Este pregătită verificarea/certificatul de cazier aplicabil cetățeniei tale? | — |
| fee_verified_for_timis | boolean | true | false | Ai verificat contravaloarea curentă pentru Timiș? | — |
| electronic_id | boolean | false | true | Deții carte electronică de identitate? | — |
| appointment_booked | boolean | true | false | Ai programare la SPCRPCIV Timiș? | — |
| reference_date | date | true | false | La ce dată verificăm? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.dlf.verify_eligibility | Verifică eligibilitatea statului și documentului | Statul emitent și tipul permisului sunt confirmate în ordinul și anexa aplicabilă. | claim.dlf.country_specific |
| step.dlf.prepare_docs | Pregătește permisul, traducerile și actele de identitate | Originalele și traducerile condiționale sunt complete. | claim.dlf.original_translation, claim.dlf.identity_residence |
| step.dlf.prepare_record | Pregătește cererea și verificarea cazierului | Ruta de cazier corespunzătoare cetățeniei este confirmată. | claim.dlf.application_record |
| step.dlf.medical | Obține fișa medicală când ceri valabilitate nouă | Fișa medicală este valabilă și emisă de unitate autorizată. | claim.dlf.medical_new_validity |
| step.dlf.book_timis | Fă programarea pentru preschimbare în Timiș | Programarea HUB MAI este confirmată. | claim.dlf.timis_appointment |
| step.dlf.submit_personally | Depune personal dosarul | Dosarul este înregistrat la serviciul județean competent. | claim.dlf.personal_county |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.dlf.original | Permisul național străin original | conditional | at_submission | claim.dlf.original_translation, claim.dlf.loss_eu |
| req.dlf.translation | Traducere în română, când este necesară | conditional | at_submission | claim.dlf.original_translation, claim.dlf.loss_eu |
| req.dlf.identity_residence | Identitate și domiciliu/reședință în România | mandatory | at_submission | claim.dlf.identity_residence |
| req.dlf.application | Cerere și verificarea cazierului | mandatory | at_submission | claim.dlf.application_record |
| req.dlf.medical | Fișă medicală pentru valabilitate nouă | conditional | at_submission | claim.dlf.medical_new_validity |
| req.dlf.payment | Dovada plății contravalorii permisului | mandatory | before_submission | claim.dlf.fee_89 |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.dlf.timis | web | HUB MAI — programare Timiș | https://hub.mai.gov.ro/dgpci/programari/create?judet=TM | DEEP_LINK |
| ch.dlf.timis_info | web | SPCRPCIV Timiș — informații | https://tm.prefectura.mai.gov.ro/permise-auto-si-inmatriculari/ | SOURCE_ONLY |
| ch.dlf.order_info | web | Pagina oficială cu trimitere la OMAI nr. 163/2011 | https://b.prefectura.mai.gov.ro/permise-auto-si-inmatriculari/ | SOURCE_ONLY |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.dlf.personal_county | verified_with_local_gap | county | Secțiunea 6, rândurile 356-358 |
| claim.dlf.original_translation | verified_with_local_gap | county | Secțiunea 6, rândurile 358-360 |
| claim.dlf.country_specific | verified_with_local_gap | county | Secțiunea 6, rândurile 360-361 |
| claim.dlf.loss_eu | verified_with_local_gap | county | Secțiunea 6, rândurile 362-363 |
| claim.dlf.identity_residence | verified_with_local_gap | county | Secțiunea 6, rândul 364 |
| claim.dlf.application_record | verified_with_local_gap | county | Secțiunea 6, rândurile 365-369 |
| claim.dlf.medical_new_validity | verified_with_local_gap | county | Secțiunea 6, rândurile 370-371 |
| claim.dlf.fee_89 | verified_with_local_gap | county | Secțiunea 3, rândul 150 |
| claim.dlf.timis_appointment | verified_with_local_gap | county | Anunț, rândurile 176-184 |
| claim.dlf.eid_address | verified_with_local_gap | county | Anunț, rândurile 161-162 |

## Release guard

- Efectele naționale pot fi evaluate numai din claim-uri `verified`, încă aplicabile și suficient de proaspete.
- Datele de instituție/UAT, taxele, programările, documentele contractuale și procedurile dependente de stat ori asigurător rămân `verified_with_local_gap`, `needs_confirmation` sau `conflicting` până la revizuire.
- `rules.yaml` este material de cercetare în starea `draft`; nu reprezintă un ruleset publicat.
