# Event Card — ro.life.home_fire_flood (life.home_fire_flood)

## Metadata

| field | value |
|---|---|
| batch_id | B15_VEHICLES_2_MISC |
| title_ro | Pașii după incendiu, inundație sau dezastru la locuință |
| trigger | locuința a fost afectată de incendiu, apă, cutremur ori alunecare de teren și trebuie gestionate urgența și dosarul de daună |
| reference_date | 2026-06-25 |
| reference_period | 2026 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | in_review |
| production_status | not_published |
| conflict_policy | Orice conflict oficial nerezolvat blochează efectul critic; motorul nu alege arbitrar o sursă. |

## Scope

Trierea siguranței, diferențierea riscurilor PAD de cele facultative, notificarea și pregătirea documentelor pentru dauna locuinței. Exclude evaluarea tehnică a structurii, stabilirea despăgubirii și litigiile cu asigurătorul sau persoana responsabilă.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| hazard | enum | true | false | Ce s-a întâmplat la locuință? | fire, natural_flood, plumbing_flood, earthquake, landslide, unknown |
| danger_active | boolean | true | true | Pericolul este încă activ? | — |
| people_safe | boolean | true | true | Toate persoanele sunt într-un loc sigur? | — |
| emergency_services_contacted | boolean | true | true | Au fost contactate serviciile de urgență sau autoritățile competente? | — |
| event_date | date | true | false | La ce dată s-a produs evenimentul? | — |
| reference_date | date | true | false | La ce dată verificăm situația? | — |
| days_since_event | number | true | false | Câte zile au trecut de la eveniment? | — |
| pad_valid | boolean | true | true | Exista o poliță PAD valabilă la data evenimentului? | — |
| facultative_policy | enum | true | true | Există o poliță facultativă valabilă? | yes, no, unknown |
| insurer_notified | boolean | true | true | Asigurătorul/PAD a fost notificat? | — |
| authority_report_available | boolean | true | true | Ai procesul-verbal sau documentul autorității privind evenimentul? | — |
| insurer_inspection_done | boolean | true | true | A fost făcută constatarea de către asigurător? | — |
| repairs_started | boolean | true | true | Au început lucrările de reparație? | — |
| identity_document_available | boolean | true | true | Ai actul de identitate disponibil? | — |
| ownership_docs_available | boolean | true | true | Ai actele de proprietate sau un document alternativ acceptabil? | — |
| contents_damage_only | boolean | true | true | Dauna privește numai bunurile din interior? | — |
| target_uat | string | true | true | În ce UAT se află locuința? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.home.ensure_safety | Pune oamenii în siguranță și urmează instrucțiunile autorităților | Pericolul imediat este gestionat și persoanele sunt în siguranță. | claim.home.emergency_official, claim.home.safety_first |
| step.home.notify_authorities | Anunță autoritățile competente | ISU/autoritatea locală a fost informată când procedura o cere. | claim.home.authority_report |
| step.home.obtain_report | Solicită documentul care atestă evenimentul | Procesul-verbal sau documentul autorității este disponibil. | claim.home.authority_report, claim.home.claim_documents |
| step.home.notify_pad | Avizează dauna PAD | Notificarea conține datele poliței și ale evenimentului și este trimisă în termen. | claim.home.notify_60d, claim.home.notice_contents |
| step.home.notify_facultative | Notifică asigurătorul facultativ | Dosarul pentru incendiu, apă din instalații sau bunuri este deschis conform contractului. | claim.home.pad_scope, claim.home.pad_exclusions |
| step.home.prepare_documents | Pregătește documentele dosarului | Actul de identitate, actele de proprietate și documentele autorităților sunt disponibile. | claim.home.claim_documents |
| step.home.wait_inspection | Așteaptă constatarea înainte de reparații | Daunele sunt constatate și raportul este semnat înainte de lucrările definitive. | claim.home.inspection_5d, claim.home.repair_after_inspection |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.home.valid_pad | PAD valabilă la data evenimentului | mandatory_for_pad_claim | at_event_date | claim.home.notice_contents |
| req.home.identity | Act de identitate | mandatory_for_pad_notice | at_notice | claim.home.notice_contents, claim.home.claim_documents |
| req.home.ownership | Act de proprietate sau document alternativ acceptabil | mandatory_for_claim_file | during_claim_file | claim.home.claim_documents |
| req.home.authority_report | Document al autorității privind evenimentul | conditional | during_claim_file | claim.home.authority_report, claim.home.claim_documents |
| req.home.facultative_contract | Contractul și condițiile poliței facultative | conditional | before_facultative_claim | claim.home.pad_scope, claim.home.pad_exclusions |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.home.emergency_112 | phone | Numărul unic pentru urgențe — 112 | tel:112 | DEEP_LINK |
| ch.home.pad_claim | web | PAD — anunță dauna | https://www.padrom.ro/daune-pad/ | DEEP_LINK |
| ch.home.pad_verify | web | PAD — verifică autenticitatea poliței | https://www.padrom.ro/verifica-pad/ | DEEP_LINK |
| ch.home.fiipregatit | web | FiiPregătit — ghiduri oficiale DSU | https://fiipregatit.ro/ | DEEP_LINK |
| ch.home.facultative_insurer | web | Canalul oficial al asigurătorului facultativ | — | USER_SELECTED_OFFICIAL_CHANNEL |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.home.emergency_official | verified | national_operational | Pagina „FiiPregătit”, secțiunea despre proiect |
| claim.home.pad_scope | verified | institution | Pagina „Ce este PAD?”, rândurile 36-38 |
| claim.home.pad_mandatory | verified | institution | Pagina „Ce este PAD?”, rândul 55 |
| claim.home.pad_exclusions | verified | institution | Pagina „Ce este PAD?”, rândul 42 |
| claim.home.safety_first | verified | institution | Pagina „Daune PAD”, rândul 44 |
| claim.home.notify_60d | verified | institution | Pagina „Daune PAD”, rândurile 45 și 55 |
| claim.home.authority_report | verified | institution | Pagina „Daune PAD”, rândurile 49-53 |
| claim.home.notice_contents | verified | institution | Pagina „Daune PAD”, rândurile 59-64 |
| claim.home.inspection_5d | verified | institution | Pagina „Daune PAD”, rândurile 66-67 |
| claim.home.claim_documents | verified | institution | Pagina „Daune PAD”, rândurile 72-87 |
| claim.home.repair_after_inspection | verified | institution | Pagina „Daune PAD”, rândul 91 |

## Release guard

- Efectele naționale pot fi evaluate numai din claim-uri `verified`, încă aplicabile și suficient de proaspete.
- Datele de instituție/UAT, taxele, programările, documentele contractuale și procedurile dependente de stat ori asigurător rămân `verified_with_local_gap`, `needs_confirmation` sau `conflicting` până la revizuire.
- `rules.yaml` este material de cercetare în starea `draft`; nu reprezintă un ruleset publicat.
