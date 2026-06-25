===
event_id: ro.life.military_reserve_status
title_ro: Verificarea sau actualizarea statutului în rezerva militară
intent_id: ro.intent.check_or_update_military_reserve_status
category_id: military_national_defence
as_of: 2026-06-25
geography: național; competență operațională la centrul militar de domiciliu; checklist local Timiș neconfirmat
publication_status: research_verified_with_explicit_gaps
fixture_count: 22
rule_count: 10
claim_count: 4

## outcome_ro
Direcționarea către recrutare, verificarea evidenței, actualizarea datelor ori obținerea legitimației, fără confundarea rutelor.

## routing_facts
- `goal`
- `rv_category`
- `age`
- `changed_data`
- `change_type`
- `purpose`

## deterministic_branches
| goal / branch | result_ro | confidence |
|---|---|---|
| `become_volunteer_reservist` | sub-traseu recrutare | verified |
| `verify_status` | confirmare la centrul militar | needs_confirmation |
| `update_personal_data` | notificare + checklist | needs_confirmation |
| `reserve_retired_id` | sub-traseu document militar | verified |

## competent_authorities
| authority | role | territory |
|---|---|---|
| Ministerul Apărării Naționale | reguli de recrutare și evidență | național |
| Centrul militar de domiciliu | recrutare/confirmare/actualizare | județ/sector |

## stop_conditions
- Nu prezenta verificarea generică drept procedură complet verificată.
- Nu inversa limitele de 50 și 55 ani.
- Nu confunda legitimația cu evidența militară.

## source_index
| claim_id | publisher | confidence | official_url |
|---|---|---|---|
| `b18.military_reserve_status.rv_entry` | Ministerul Apărării Naționale — Recrutare MApN | verified | https://www.recrutaremapn.ro/rezervist.php |
| `b18.military_reserve_status.rv_limits` | Ministerul Apărării Naționale — Recrutare MApN | verified | https://www.recrutaremapn.ro/rezervist.php |
| `b18.military_reserve_status.reserve_id` | Ministerul Apărării Naționale | verified | https://www.mapn.ro/rezervisti_militari/index.php |
| `b18.military_reserve_status.status_gap` | Ministerul Apărării Naționale | needs_confirmation | https://www.mapn.ro/rezervisti_militari/index.php |
===
