===
event_id: ro.life.military_enrollment
title_ro: Înscriere într-o formă de carieră militară
intent_id: ro.intent.enroll_in_military
category_id: military_national_defence
as_of: 2026-06-25
geography: national; competență locală prin centrul militar/unitatea cu posturi; detaliile Timiș nepublicate sunt gap
publication_status: research_verified_with_explicit_gaps
fixture_count: 22
rule_count: 23
claim_count: 9

## outcome_ro
Identificarea rutei militare exacte, verificarea criteriilor publicate și construirea dosarului aplicabil fără a amesteca SGP, rezervist voluntar și școli militare.

## routing_facts
- `goal`
- `age`
- `romanian_citizen`
- `stable_domicile_ro`
- `education_classes`
- `branch`
- `foreign_studies`
- `is_reservist`
- `comes_from_volunteer_reserve`
- `rv_category`
- `final_conviction_unrehabilitated`
- `has_military_training`
- `post_requires_driving`

## deterministic_branches
| goal / branch | result_ro | confidence |
|---|---|---|
| `soldier_professional` | dosar SGP + selecție + examen medical | verified |
| `volunteer_reservist` | centrul militar de domiciliu + dosar + selecție | verified |
| `military_school_or_other` | identificare rută înainte de dosar | needs_confirmation |

## competent_authorities
| authority | role | territory |
|---|---|---|
| Ministerul Apărării Naționale | recrutare și selecție | național |
| Unitatea militară cu post SGP | înscriere SGP | după post |
| Centrul militar de domiciliu | rezervist voluntar | județ/sector |

## stop_conditions
- Nu afișa eligibilitate când criteriile publicate sunt încălcate.
- Nu transforma seria din 7 septembrie 2026 într-o regulă permanentă.
- Nu reutiliza lista SGP pentru școli militare.

## source_index
| claim_id | publisher | confidence | official_url |
|---|---|---|---|
| `b18.military_enrollment.sgp_entry` | Ministerul Apărării Naționale — Recrutare MApN | verified | https://www.recrutaremapn.ro/sgp.php |
| `b18.military_enrollment.sgp_documents` | Ministerul Apărării Naționale — Recrutare MApN | verified | https://www.recrutaremapn.ro/sgp.php |
| `b18.military_enrollment.sgp_driving` | Ministerul Apărării Naționale — Recrutare MApN | verified | https://www.recrutaremapn.ro/sgp.php |
| `b18.military_enrollment.selection` | Ministerul Apărării Naționale — Recrutare MApN | verified | https://www.recrutaremapn.ro/selectie.php |
| `b18.military_enrollment.campaign_2026` | Ministerul Apărării Naționale — Recrutare MApN | verified | https://www.recrutaremapn.ro/sgp.php |
| `b18.military_enrollment.rv_entry` | Ministerul Apărării Naționale — Recrutare MApN | verified | https://www.recrutaremapn.ro/rezervist.php |
| `b18.military_enrollment.rv_conditions` | Ministerul Apărării Naționale — Recrutare MApN | verified | https://www.recrutaremapn.ro/rezervist.php |
| `b18.military_enrollment.rv_documents` | Ministerul Apărării Naționale — Recrutare MApN | verified | https://www.recrutaremapn.ro/rezervist.php |
| `b18.military_enrollment.other_paths_gap` | Ministerul Apărării Naționale — Recrutare MApN | needs_confirmation | https://www.recrutaremapn.ro/ |
===
