# Event Card — ro.life.vehicle_leasing_end (life.vehicle_leasing_end)

## Metadata

| field | value |
|---|---|
| batch_id | B15_VEHICLES_2_MISC |
| title_ro | Trecerea vehiculului pe numele meu după leasing |
| trigger | contractul de leasing s-a încheiat și proprietatea trebuie transcrisă |
| reference_date | 2026-06-25 |
| reference_period | 2026 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | verified_with_local_gap |
| production_status | not_published |
| conflict_policy | Orice conflict oficial nerezolvat blochează efectul critic; motorul nu alege arbitrar o sursă. |

## Scope

Transferul administrativ al unui vehicul deja înmatriculat în România, după dobândirea proprietății la finalul leasingului. Exclude înmatricularea inițială, importul și litigiile contractuale cu finanțatorul.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| acquisition_date | date | true | false | La ce dată ai dobândit proprietatea după leasing? | — |
| final_leasing_document_received | boolean | true | false | Ai primit documentul final care dovedește transferul proprietății? | — |
| ownership_document_registered_local_tax | boolean | true | false | Documentul de proprietate este înregistrat la organul fiscal local? | — |
| submission_channel | enum | true | false | Cum depui transcrierea? | in_person, online |
| tax_clearance_certificate_available | boolean | false | false | Ai certificatul de atestare fiscală? | — |
| target_uat | string | true | false | În ce UAT ai domiciliul/sediul? | — |
| rca_status | enum | true | false | RCA este valabilă? | valid, expired, unknown |
| itp_status | enum | true | false | ITP este valabil? | valid, expired, cancelled, unknown |
| plans_public_road_use | boolean | true | false | Vrei să circuli pe drum public înainte de finalizarea dosarului? | — |
| electronic_id | boolean | false | true | Deții carte electronică de identitate? | — |
| reference_date | date | true | false | La ce dată verificăm situația? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.vle.obtain_lessor_docs | Obține actele finale de la finanțator | Documentul de transfer și orice acte predate de finanțator sunt disponibile. | claim.vle.transcription_90d |
| step.vle.register_local_tax | Înregistrează dobândirea în evidența fiscală locală | Documentul de proprietate apare în evidența fiscală locală. | claim.vle.inperson_fiscal_record |
| step.vle.choose_channel | Alege canalul de transcriere | Canalul la ghișeu sau online este stabilit și cerința fiscală aferentă este îndeplinită. | claim.vle.inperson_fiscal_record, claim.vle.online_fiscal_certificate |
| step.vle.book_timis | Fă programarea în Timiș | Există confirmare HUB MAI sau bon de ordine, după caz. | claim.vle.timis_submission, claim.vle.timis_appointment |
| step.vle.submit_transcription | Depune transcrierea dreptului de proprietate | Cererea este înregistrată înainte de expirarea termenului de 90 de zile. | claim.vle.transcription_90d |
| step.vle.verify_roadworthiness | Verifică ITP și RCA înainte de circulație | ITP și RCA sunt confirmate valabile. | claim.vle.no_road_without_itp_rca |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.vle.ownership_document | Documentul care atestă transferul proprietății | mandatory | now | claim.vle.transcription_90d, claim.vle.inperson_fiscal_record |
| req.vle.local_tax_registration | Înregistrarea documentului în evidența fiscală locală | mandatory | before_submission | claim.vle.inperson_fiscal_record |
| req.vle.tax_certificate_online | Certificat de atestare fiscală pentru fluxul online | conditional | before_submission | claim.vle.online_fiscal_certificate |
| req.vle.valid_itp | ITP valabil pentru circulație | conditional | before_public_road_use | claim.vle.no_road_without_itp_rca |
| req.vle.valid_rca | RCA valabilă pentru circulație | conditional | before_public_road_use | claim.vle.no_road_without_itp_rca |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.vle.timis_appointment | web | HUB MAI — programare Timiș | https://hub.mai.gov.ro/dgpci/programari/create?judet=TM | DEEP_LINK |
| ch.vle.dgpci | web | DGPCI — servicii online | https://dgpci.mai.gov.ro/ | DEEP_LINK |
| ch.vle.timis_info | web | SPCRPCIV Timiș — informații oficiale | https://tm.prefectura.mai.gov.ro/permise-auto-si-inmatriculari/ | SOURCE_ONLY |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.vle.transcription_90d | verified | national_normative | OUG nr. 195/2002, art. 11 alin. (4) |
| claim.vle.fiscal_notice_5wd | verified | national_normative | OUG nr. 195/2002, art. 11 alin. (4^1) |
| claim.vle.inperson_fiscal_record | verified_with_local_gap | county | Anunț OUG nr. 7/2026, rândurile 118-122 |
| claim.vle.online_fiscal_certificate | verified_with_local_gap | county | Anunț OUG nr. 7/2026, rândul 122 |
| claim.vle.timis_submission | verified_with_local_gap | county | Anunț, rândurile 139-142 |
| claim.vle.timis_appointment | verified_with_local_gap | county | Anunț, rândurile 176-184 |
| claim.vle.eid_address | verified_with_local_gap | county | Anunț, rândurile 161-162 |
| claim.vle.no_road_without_itp_rca | verified | national_normative | OUG nr. 195/2002, art. 10 alin. (1) |

## Release guard

- Efectele naționale pot fi evaluate numai din claim-uri `verified`, încă aplicabile și suficient de proaspete.
- Datele de instituție/UAT, taxele, programările, documentele contractuale și procedurile dependente de stat ori asigurător rămân `verified_with_local_gap`, `needs_confirmation` sau `conflicting` până la revizuire.
- `rules.yaml` este material de cercetare în starea `draft`; nu reprezintă un ruleset publicat.
