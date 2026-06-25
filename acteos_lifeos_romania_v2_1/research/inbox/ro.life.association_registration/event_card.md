===
event_id: ro.life.association_registration
title_ro: Înregistrarea unei asociații
intent_id: ro.intent.register_association
category_id: ong_associations
as_of: 2026-06-25
geography: rută legală națională; mecanica Judecătoriei Timișoara este gap local
publication_status: research_verified_with_explicit_gaps
fixture_count: 22
rule_count: 14
claim_count: 10

## outcome_ro
Pregătirea dosarului și depunerea la judecătoria sediului, cu ramuri pentru denumire, aport imobiliar, beneficiar real și activități speciale.

## routing_facts
- `goal`
- `founder_count`
- `seat_county`
- `immovable_contribution`
- `founders_only_natural`
- `management_only_natural`
- `beneficiaries_identifiable_from_file`
- `legal_person_founder`
- `foreign_documents`
- `religious_activities`
- `name_has_national_or_roman`
- `name_confuses_public_authority`
- `no_activity_at_seat`
- `regulated_activities`

## deterministic_branches
| goal / branch | result_ro | confidence |
|---|---|---|
| `register_association` | judecătoria sediului + registrul ONG | verified |
| `seat_county=timis` | mecanică locală de confirmat | verified_with_local_gap |

## competent_authorities
| authority | role | territory |
|---|---|---|
| Judecătoria sediului | înscriere | circumscripția sediului |
| Ministerul Justiției | dovada denumirii | național |
| Secretariatul General al Guvernului | acord denumire specială | național |

## stop_conditions
- Blochează sub trei fondatori.
- Blochează denumirea confundabilă cu autorități.
- Nu începe activități reglementate fără autorizație.
- Nu inventa mecanica locală.

## source_index
| claim_id | publisher | confidence | official_url |
|---|---|---|---|
| `b18.association_registration.founders_court` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
| `b18.association_registration.statute_form` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
| `b18.association_registration.filing_documents` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
| `b18.association_registration.bo_exemption` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
| `b18.association_registration.seat_no_activity` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
| `b18.association_registration.name_rules` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
| `b18.association_registration.judge_appeal` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
| `b18.association_registration.regulated` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
| `b18.association_registration.fee` | Portal Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/149314 |
| `b18.association_registration.local_gap` | Portal Legislativ — Ministerul Justiției | verified_with_local_gap | https://legislatie.just.ro/Public/DetaliiDocument/20740 |
===
