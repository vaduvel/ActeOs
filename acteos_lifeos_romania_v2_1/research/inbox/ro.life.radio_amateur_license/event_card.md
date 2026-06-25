===
event_id: ro.life.radio_amateur_license
title_ro: Certificarea și autorizarea ca radioamator
intent_id: ro.intent.obtain_radio_amateur_authorization
category_id: hobbies_permits
as_of: 2026-06-25
geography: procedură ANCOM națională; Direcția Regională Timișoara ca punct de depunere; conflict oficial de nomenclatură a claselor
publication_status: research_verified_with_explicit_gaps
fixture_count: 22
rule_count: 21
claim_count: 12

## outcome_ro
Alegerea rutei ANCOM corecte pentru examen, certificat, autorizație individuală, radioclub, repetor sau duplicat.

## routing_facts
- `goal`
- `desired_class`
- `is_minor`
- `applicant_age`
- `session_code`
- `region`
- `uses_old_srs_email`

## deterministic_branches
| goal / branch | result_ro | confidence |
|---|---|---|
| `take_exam` | înscriere la sesiune ANCOM | verified |
| `obtain_individual_authorization` | autorizație individuală | verified |
| `renew/duplicate` | formular dedicat + checklist de confirmat | needs_confirmation |
| `class IV / III restricted` | conflict explicit între două surse ANCOM | conflicting |

## competent_authorities
| authority | role | territory |
|---|---|---|
| ANCOM | examinare, certificare și autorizare | național |
| Direcția Regională ANCOM Timișoara | punct regional de depunere | vest/Timiș |

## stop_conditions
- Nu echivala automat clasa IV cu clasa III restrâns.
- Pentru solicitant sub 14 ani, afișează conflictul înainte de selectarea clasei.
- Nu utiliza adresa srs@ancom.ro după 18 iunie 2026.
- Nu reutiliza termenul unei sesiuni pentru altă sesiune.

## source_index
| claim_id | publisher | confidence | official_url |
|---|---|---|---|
| `b18.radio_amateur_license.current_classes` | ANCOM | conflicting | https://www.ancom.ro/category/autorizare-ro/radioamatori/ |
| `b18.radio_amateur_license.decision_classes` | ANCOM | conflicting | https://www.ancom.ro/wp-content/uploads/2010/07/DECIZIA_ANCOM_245_2017_PRIVIND_REGLEMENTAREA_SERVICIULUI_DE_AMATOR_CONSOLIDATA_31_martie_2022.pdf |
| `b18.radio_amateur_license.forms_channels` | ANCOM | verified | https://www.ancom.ro/category/autorizare-ro/radioamatori/ |
| `b18.radio_amateur_license.old_email_closed` | ANCOM | verified | https://www.ancom.ro/category/autorizare-ro/radioamatori/ |
| `b18.radio_amateur_license.exam_file_channels` | ANCOM | verified | https://www.ancom.ro/autorizare-ro/radioamatori/radioamatori-sesiuni-de-examinare/ |
| `b18.radio_amateur_license.exam_decision_rules` | ANCOM | verified | https://www.ancom.ro/wp-content/uploads/2010/07/DECIZIA_ANCOM_245_2017_PRIVIND_REGLEMENTAREA_SERVICIULUI_DE_AMATOR_CONSOLIDATA_31_martie_2022.pdf |
| `b18.radio_amateur_license.under14_class` | ANCOM | conflicting | https://www.ancom.ro/wp-content/uploads/2010/07/DECIZIA_ANCOM_245_2017_PRIVIND_REGLEMENTAREA_SERVICIULUI_DE_AMATOR_CONSOLIDATA_31_martie_2022.pdf |
| `b18.radio_amateur_license.results_contest_certificate` | ANCOM | verified | https://www.ancom.ro/wp-content/uploads/2010/07/DECIZIA_ANCOM_245_2017_PRIVIND_REGLEMENTAREA_SERVICIULUI_DE_AMATOR_CONSOLIDATA_31_martie_2022.pdf |
| `b18.radio_amateur_license.authorization` | ANCOM | verified | https://www.ancom.ro/wp-content/uploads/2010/07/DECIZIA_ANCOM_245_2017_PRIVIND_REGLEMENTAREA_SERVICIULUI_DE_AMATOR_CONSOLIDATA_31_martie_2022.pdf |
| `b18.radio_amateur_license.club_repeater` | ANCOM | verified | https://www.ancom.ro/wp-content/uploads/2010/07/DECIZIA_ANCOM_245_2017_PRIVIND_REGLEMENTAREA_SERVICIULUI_DE_AMATOR_CONSOLIDATA_31_martie_2022.pdf |
| `b18.radio_amateur_license.session_2026_07_16` | ANCOM | verified | https://www.ancom.ro/autorizare-ro/radioamatori/radioamatori-sesiuni-de-examinare/ |
| `b18.radio_amateur_license.fee_checklist_gap` | ANCOM | needs_confirmation | https://www.ancom.ro/category/autorizare-ro/radioamatori/ |
===
