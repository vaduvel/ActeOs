# Event Card — ro.life.change_name_admin_court (life.change_name_admin_court)

## Metadata

| field | value |
|---|---|
| batch_id | B15_VEHICLES_2_MISC |
| title_ro | Schimbarea legală a numelui |
| trigger | persoana dorește schimbarea numelui pe cale administrativă, cu intervenția instanței numai unde legea o cere |
| reference_date | 2026-06-25 |
| reference_period | 2026 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | in_review |
| production_status | not_published |
| conflict_policy | Orice conflict oficial nerezolvat blochează efectul critic; motorul nu alege arbitrar o sursă. |

## Scope

Schimbarea administrativă a numelui și ramurile limitate în care instanța de tutelă ori contenciosul administrativ devin necesare. Exclude schimbarea numelui produsă direct prin căsătorie/divorț și rectificarea erorilor din actele de stare civilă.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| applicant_age | integer | true | true | Ce vârstă are persoana al cărei nume se schimbă? | — |
| citizenship_status | enum | true | true | Care este statutul de cetățenie relevant? | romanian, stateless_with_ro_domicile, other |
| domicile_uat | string | true | true | Care este UAT-ul de domiciliu? | — |
| ever_had_ro_domicile | boolean | true | true | A existat vreodată domiciliu în România? | — |
| serious_ground_documented | boolean | true | true | Motivul temeinic este descris și susținut cu documente? | — |
| is_minor | boolean | true | true | Solicitantul este minor? | — |
| filed_by_tutor | boolean | false | true | Cererea este depusă de tutore? | — |
| parents_agree | boolean | false | true | Părinții sunt de acord asupra schimbării? | — |
| one_parent_application | boolean | false | true | Cererea este făcută de un singur părinte? | — |
| other_parent_consent_available | boolean | false | true | Există acordul celuilalt părinte în forma cerută? | — |
| minor_signed_if_14plus | boolean | false | true | Minorul de cel puțin 14 ani a semnat cererea? | — |
| mo_extract_published | boolean | true | false | Extrasul cererii a fost publicat în Monitorul Oficial? | — |
| mo_extract_age_days | integer | false | false | Câte zile are extrasul Monitorului Oficial? | — |
| opposition_period_elapsed | boolean | true | false | Au trecut cele 30 de zile pentru opoziții? | — |
| opposition_received | boolean | true | true | A fost formulată opoziție? | — |
| stage2_documents_complete | boolean | true | true | Dosarul final este complet? | — |
| disposition_result | enum | true | false | Care este starea dispoziției? | pending, approved, rejected |
| days_since_approval_notice | integer | false | false | Câte zile au trecut de la informarea privind admiterea? | — |
| appointment_booked | boolean | true | false | Ai programare locală? | — |
| reference_date | date | true | false | La ce dată verificăm? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.name.check_route | Confirmă ruta administrativă sau intervenția instanței | Motivul, vârsta și reprezentarea indică ruta corectă. | claim.name.admin_route, claim.name.minor_court |
| step.name.prepare_initial | Pregătește cererea și documentele inițiale | Identitatea, actele de stare civilă și dovezile motivului sunt complete. | claim.name.documents, claim.name.criminal_record_14 |
| step.name.publish_mo | Publică extrasul în Monitorul Oficial | Extrasul este publicat și are cel mult un an la dosarul final. | claim.name.documents |
| step.name.wait_opposition | Așteaptă termenul pentru opoziții | Au trecut 30 de zile de la publicare. | claim.name.opposition_30 |
| step.name.book_timis | Fă programarea în Timișoara | Programarea locală este confirmată. | claim.name.timis_appointment |
| step.name.submit_final | Depune dosarul complet | Serviciul competent a înregistrat toate documentele. | claim.name.filing_place, claim.name.documents |
| step.name.receive_disposition | Primește și confirmă dispoziția | Dispoziția este comunicată și, dacă este admisă, confirmată în 90 de zile. | claim.name.disposition_30, claim.name.pickup_90 |
| step.name.challenge | Contestă respingerea pe calea legală | Contestația este pregătită în baza actului comunicat. | claim.name.rejection_challenge |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.name.identity_civil | Act de identitate și certificate de stare civilă originale | mandatory | at_submission | claim.name.documents |
| req.name.mo_extract | Extras Monitorul Oficial de cel mult un an | mandatory | final_file | claim.name.documents |
| req.name.criminal_record | Cazier judiciar pentru solicitantul de cel puțin 14 ani | conditional | final_file | claim.name.criminal_record_14 |
| req.name.court_approval | Încuviințarea/hotărârea instanței de tutelă | conditional | before_submission | claim.name.minor_court |
| req.name.other_parent_consent | Acordul celuilalt părinte | conditional | before_submission | claim.name.other_parent_consent |
| req.name.minor_signature | Semnătura minorului de cel puțin 14 ani | conditional | on_application | claim.name.minor_14_signs |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.name.timis_archive | web | Primăria Timișoara — procedură arhivată | https://arhiva.primariatm.ro/schimbare-nume.html | SOURCE_ONLY |
| ch.name.law | web | Portal Legislativ — Legea nr. 119/1996 | https://legislatie.just.ro/Public/DetaliiDocument/8624 | SOURCE_ONLY |
| ch.name.court | external | Instanța de tutelă competentă | https://portal.just.ro/ | SOURCE_ONLY |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.name.admin_route | verified | national_normative | Legea nr. 119/1996, art. 41^1 |
| claim.name.filing_place | verified | national_normative | Legea nr. 119/1996, art. 41^3 alin. (1) |
| claim.name.documents | verified | national_normative | Legea nr. 119/1996, art. 41^3 alin. (2) |
| claim.name.criminal_record_14 | verified | national_normative | Legea nr. 119/1996, art. 41^3 alin. (2) lit. e) |
| claim.name.minor_court | verified | national_normative | Legea nr. 119/1996, art. 41^4 alin. (1) |
| claim.name.other_parent_consent | verified | national_normative | Legea nr. 119/1996, art. 41^4 alin. (2) |
| claim.name.minor_14_signs | verified | national_normative | Legea nr. 119/1996, art. 41^4 alin. (3) |
| claim.name.opposition_30 | verified | national_normative | Legea nr. 119/1996, art. 41^10 alin. (1) |
| claim.name.disposition_30 | verified | national_normative | Legea nr. 119/1996, art. 41^12 alin. (2) |
| claim.name.pickup_90 | verified | national_normative | Legea nr. 119/1996, art. 41^13 alin. (4)-(5) |
| claim.name.rejection_challenge | verified | national_normative | Legea nr. 119/1996, art. 41^15 alin. (1)-(2) |
| claim.name.timis_appointment | verified_with_local_gap | local | Pagina „Schimbare nume” |
| claim.name.local_60_conflict | conflicting | local | Pagina „Schimbare nume” |
| claim.name.local_no_fee_unverified | needs_confirmation | local | Pagina „Schimbare nume” |

## Release guard

- Efectele naționale pot fi evaluate numai din claim-uri `verified`, încă aplicabile și suficient de proaspete.
- Datele de instituție/UAT, taxele, programările, documentele contractuale și procedurile dependente de stat ori asigurător rămân `verified_with_local_gap`, `needs_confirmation` sau `conflicting` până la revizuire.
- `rules.yaml` este material de cercetare în starea `draft`; nu reprezintă un ruleset publicat.
