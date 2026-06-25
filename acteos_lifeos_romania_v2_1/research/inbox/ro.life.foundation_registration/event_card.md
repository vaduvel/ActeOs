===
event_id: ro.life.foundation_registration
title_ro: Înregistrarea unei fundații
intent_id: ro.intent.register_foundation
category_id: ong_associations
as_of: 2026-06-25
geography: rută legală națională; mecanica Judecătoriei Timișoara este gap local
publication_status: research_verified_with_explicit_gaps
fixture_count: 22
rule_count: 17
claim_count: 7

## outcome_ro
Pregătirea fundației, verificarea pragului patrimonial și depunerea dosarului la judecătoria sediului.

## routing_facts
- `goal`
- `founder_count`
- `fundraising_only_for_other_ngos`
- `initial_assets_multiple`
- `seat_county`
- `immovable_contribution`
- `founders_only_natural`
- `board_only_natural`
- `beneficiaries_identifiable_from_file`
- `foreign_documents`
- `religious_activities`
- `name_has_national_or_roman`
- `name_confuses_public_authority`
- `no_activity_at_seat`
- `regulated_activities`

## deterministic_branches
| goal / branch | result_ro | confidence |
|---|---|---|
| `standard foundation` | prag 10x salariul minim brut | verified |
| `exclusive fundraising` | prag special 2x | verified |
| `seat_county=timis` | mecanică locală de confirmat | verified_with_local_gap |

## competent_authorities
| authority | role | territory |
|---|---|---|
| Judecătoria sediului | înscriere | circumscripția sediului |
| Ministerul Justiției | dovada denumirii | național |
| Secretariatul General al Guvernului | acord denumire specială | național |

## stop_conditions
- Blochează lipsa fondatorului.
- Blochează patrimoniul sub prag.
- Nu aplica pragul 2x în afara scopului exclusiv.
- Nu inventa valoarea în lei fără salariul minim curent.

## source_index
| claim_id | publisher | confidence | official_url |
|---|---|---|---|
| `b18.foundation_registration.founders_court` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
| `b18.foundation_registration.assets` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
| `b18.foundation_registration.statute` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
| `b18.foundation_registration.documents` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
| `b18.foundation_registration.association_rules` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
| `b18.foundation_registration.fee` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/149314 |
| `b18.foundation_registration.local_gap` | Portal Legislativ — Ministerul Justiției | verified_with_local_gap | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
===
