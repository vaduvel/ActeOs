# Event Card — ro.life.administrative_petition (life.administrative_petition)

## Metadata

| field | value |
|---|---|
| batch_id | B15_VEHICLES_2_MISC |
| title_ro | Depunerea și urmărirea unei petiții administrative |
| trigger | persoana vrea să formuleze o cerere, reclamație, sesizare sau propunere către o autoritate publică |
| reference_date | 2026-06-25 |
| reference_period | 2026 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | verified_with_local_gap |
| production_status | not_published |
| conflict_policy | Orice conflict oficial nerezolvat blochează efectul critic; motorul nu alege arbitrar o sursă. |

## Scope

Redactarea, depunerea, redirecționarea și urmărirea termenului unei petiții în sensul OG nr. 27/2002. Exclude solicitările de informații publice din Legea nr. 544/2001, plângerile contravenționale și contestațiile administrative cu procedură specială.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| petition_kind | enum | true | false | Ce fel de petiție trimiți? | request, complaint, referral, proposal |
| submission_channel | enum | true | false | Cum trimiți petiția? | written, email, online_form |
| identified | boolean | true | true | Petiția include datele tale de identificare? | — |
| harassment_subject | enum | true | true | Petiția anonimă privește o formă de hărțuire exceptată de lege? | none, sex_based, moral, unknown |
| criminal_indications | boolean | true | true | Sunt descrise indicii privind o posibilă infracțiune sexuală dintre cele prevăzute de lege? | — |
| competent_authority | boolean | true | false | Autoritatea aleasă este competentă pentru problemă? | — |
| registration_date | date | true | false | La ce dată a fost înregistrată petiția? | — |
| reference_date | date | true | false | La ce dată verificăm situația? | — |
| days_since_registration | number | true | false | Câte zile au trecut de la înregistrarea la autoritatea competentă? | — |
| complexity_extension | boolean | true | false | Autoritatea a comunicat o prelungire pentru cercetare amănunțită? | — |
| domain | enum | true | false | Petiția este în domeniul energiei sau gazelor naturale? | energy_gas, other |
| extension_notice_received | boolean | true | false | Ai primit notificarea prealabilă privind prelungirea? | — |
| duplicate_same_issue | boolean | true | false | Ai mai trimis aceleiași autorități o petiție cu aceeași problemă? | — |
| prior_answer_received | boolean | true | false | Ai primit deja răspuns la petiția inițială? | — |
| response_received | boolean | true | false | Ai primit răspuns la petiția curentă? | — |
| response_has_legal_basis | boolean | false | false | Răspunsul indică temeiul legal al soluției? | — |
| target_authority | enum | true | false | Cărei autorități îi trimiți petiția? | timis_prefecture, other |
| attachment_present | boolean | true | true | Atașezi un fișier? | — |
| attachment_extension | enum | false | true | Ce extensie are atașamentul? | pdf, doc, docx, zip, rar, jpeg, jpg, png, other |
| attachment_size_mb | number | false | true | Ce dimensiune are atașamentul, în MB? | — |
| attachment_filename_has_diacritics | boolean | false | true | Denumirea fișierului conține diacritice? | — |
| submission_confirmation_received | boolean | true | false | Ai primit confirmarea de trimitere/înregistrare? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.pet.choose_authority | Identifică autoritatea competentă | Obiectul petiției este corelat cu atribuțiile autorității. | claim.pet.forward_5d |
| step.pet.prepare | Redactează și identifică petiția | Petiția conține obiectul, situația și datele de identificare, exceptând cazurile anonime protejate de lege. | claim.pet.definition, claim.pet.anonymous_archived, claim.pet.anonymous_harassment |
| step.pet.submit | Trimite și păstrează dovada înregistrării | Există număr, mesaj sau altă dovadă a înregistrării. | claim.pet.definition, claim.pet.timis_confirmation |
| step.pet.follow_forwarding | Urmărește redirecționarea dacă autoritatea este greșită | Există notificarea privind autoritatea competentă și noua dată de înregistrare. | claim.pet.forward_5d, claim.pet.answer_30d |
| step.pet.track_deadline | Urmărește termenul legal de răspuns | Termenul de 30 de zile sau prelungirea notificată este calculată de la data corectă. | claim.pet.answer_30d, claim.pet.extension |
| step.pet.review_response | Verifică răspunsul primit | Răspunsul indică soluția și temeiul legal. | claim.pet.response_legal_basis |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.pet.identity | Date de identificare ale petiționarului | mandatory_unless_statutory_exception | before_submission | claim.pet.anonymous_archived, claim.pet.anonymous_harassment |
| req.pet.content | Obiect și conținut clar al petiției | mandatory | before_submission | claim.pet.definition, claim.pet.timis_form |
| req.pet.registration_proof | Dovada înregistrării sau confirmării | operational | after_submission | claim.pet.answer_30d, claim.pet.timis_confirmation |
| req.pet.timis_attachment | Atașament compatibil cu formularul Timiș | conditional | before_online_submission | claim.pet.timis_attachment |
| req.pet.extension_notice | Notificarea prealabilă a prelungirii | conditional | before_extended_deadline | claim.pet.extension |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.pet.timis_form | web | Prefectura Timiș — formular oficial de petiții | https://tm.prefectura.mai.gov.ro/petitii/ | DEEP_LINK |
| ch.pet.official_registry | web | Portalul instituției publice competente | — | USER_SELECTED_OFFICIAL_CHANNEL |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.pet.definition | verified | national_normative | OG nr. 27/2002, art. 2 |
| claim.pet.forward_5d | verified | national_normative | OG nr. 27/2002, art. 6^1 |
| claim.pet.anonymous_archived | verified | national_normative | OG nr. 27/2002, art. 7 alin. (1) |
| claim.pet.anonymous_harassment | verified | national_normative | OG nr. 27/2002, art. 7 alin. (2)-(3) |
| claim.pet.criminal_referral | verified | national_normative | OG nr. 27/2002, art. 7 alin. (4) |
| claim.pet.answer_30d | verified | national_normative | OG nr. 27/2002, art. 8 |
| claim.pet.extension | verified | national_normative | OG nr. 27/2002, art. 9 |
| claim.pet.duplicate | verified | national_normative | OG nr. 27/2002, art. 10 |
| claim.pet.response_legal_basis | verified | national_normative | OG nr. 27/2002, art. 13 |
| claim.pet.timis_form | verified_with_local_gap | county | Formular petiții, rândurile 100-120 |
| claim.pet.timis_attachment | verified_with_local_gap | county | Formular petiții, rândul 122 |
| claim.pet.timis_confirmation | verified_with_local_gap | county | Formular petiții, rândul 124 |

## Release guard

- Efectele naționale pot fi evaluate numai din claim-uri `verified`, încă aplicabile și suficient de proaspete.
- Datele de instituție/UAT, taxele, programările, documentele contractuale și procedurile dependente de stat ori asigurător rămân `verified_with_local_gap`, `needs_confirmation` sau `conflicting` până la revizuire.
- `rules.yaml` este material de cercetare în starea `draft`; nu reprezintă un ruleset publicat.
