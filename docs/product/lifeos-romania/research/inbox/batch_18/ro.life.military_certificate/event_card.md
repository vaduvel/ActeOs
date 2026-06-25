===
event_id: ro.life.military_certificate
title_ro: Obținerea sau înlocuirea unui document militar
intent_id: ro.intent.obtain_military_document
category_id: military_national_defence
as_of: 2026-06-25
geography: național; emitentul depinde de stadiu și domiciliu; mecanica locală Timiș rămâne gap
publication_status: research_verified_with_explicit_gaps
fixture_count: 22
rule_count: 10
claim_count: 5

## outcome_ro
Identificarea exactă a documentului militar și trimiterea la emitentul competent, fără confundarea legitimației cu livretul ori adeverința.

## routing_facts
- `goal`
- `transitioning_now`
- `already_in_reserve_or_retired`
- `source_from_mapn`
- `is_military_pensioner`
- `loss_type`
- `purpose`

## deterministic_branches
| goal / branch | result_ro | confidence |
|---|---|---|
| `reserve_retired_id` | structura de trecere sau centrul militar | verified |
| `replace_lost_reserve_retired_id` | declarare nulitate + înlocuire | verified |
| `military_booklet` | confirmare la centrul militar | needs_confirmation |
| `military_status_attestation` | confirmare denumire și checklist | needs_confirmation |

## competent_authorities
| authority | role | territory |
|---|---|---|
| Ministerul Apărării Naționale | reguli legitimație | național |
| Structura care inițiază trecerea | emitere la trecere | instituțional |
| Centrul militar de domiciliu | cereri ulterioare | județ/sector |

## stop_conditions
- Nu numi orice act «certificat militar».
- Nu publica un dosar pentru livret fără confirmare.
- Nu presupune eligibilitatea MApN pentru alte sisteme.

## source_index
| claim_id | publisher | confidence | official_url |
|---|---|---|---|
| `b18.military_certificate.reserve_id_scope` | Ministerul Apărării Naționale | verified | https://www.mapn.ro/rezervisti_militari/index.php |
| `b18.military_certificate.reserve_id_issuer` | Ministerul Apărării Naționale | verified | https://www.mapn.ro/rezervisti_militari/index.php |
| `b18.military_certificate.reserve_id_loss` | Ministerul Apărării Naționale | verified | https://www.mapn.ro/rezervisti_militari/index.php |
| `b18.military_certificate.booklet_gap` | Ministerul Apărării Naționale | needs_confirmation | https://www.mapn.ro/rezervisti_militari/index.php |
| `b18.military_certificate.attestation_gap` | Ministerul Apărării Naționale | needs_confirmation | https://www.mapn.ro/rezervisti_militari/index.php |
===
