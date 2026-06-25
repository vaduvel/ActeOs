===
event_id: ro.life.domestic_violence_protection_order
title_ro: Obținerea unui ordin de protecție pentru violență domestică
intent_id: ro.intent.obtain_domestic_violence_protection
category_id: domestic_violence_protection
as_of: 2026-06-25
geography: reguli naționale; identificarea judecătoriei după competența legală; mecanica locală Timișoara rămâne de confirmat
publication_status: research_verified_with_explicit_gaps
fixture_count: 22
rule_count: 19
claim_count: 13

## outcome_ro
Direcționarea rapidă către intervenția de urgență, ordinul provizoriu al poliției sau ordinul judecătoresc și gestionarea termenelor de atac ori a încălcării.

## routing_facts
- `goal`
- `immediate_danger`
- `imminent_risk`
- `prior_order_expired_within_5_years`
- `competence_basis`
- `order_communicated`
- `decision_with_parties_cited`
- `county`

## deterministic_branches
| goal / branch | result_ro | confidence |
|---|---|---|
| `emergency_help` | 112 și siguranță imediată | verified |
| `request_provisional_order` | evaluare poliție pentru risc iminent | verified |
| `request_court_order` | cerere la judecătoria competentă | verified |
| `contest/appeal` | termene de 48 ore / 3 zile | verified |
| `report_order_breach` | sesizarea poliției; încălcarea este infracțiune | verified |

## competent_authorities
| authority | role | territory |
|---|---|---|
| Poliția Română | intervenție, evaluare și ordin provizoriu; executare/supraveghere | național |
| Parchetul de pe lângă judecătoria competentă | confirmarea ordinului provizoriu | competent teritorial |
| Judecătoria competentă | ordin de protecție și contestația OPP | domiciliul/reședința victimei sau locul faptelor |

## stop_conditions
- În pericol imediat, afișează 112 înaintea pașilor administrativi.
- Nu promite emiterea ordinului provizoriu; poliția evaluează riscul.
- Nu calcula termenul de apel fără ancora corectă.
- Nu inventa programul sau registratura de gardă a instanței locale.

## source_index
| claim_id | publisher | confidence | official_url |
|---|---|---|---|
| `b18.domestic_violence_protection_order.emergency_112` | Poliția Română | verified | https://politiaromana.ro/ro/prevenire/violenta-domestica/ordinul-de-protectie-provizoriu |
| `b18.domestic_violence_protection_order.provisional_trigger` | Poliția Română | verified | https://politiaromana.ro/ro/prevenire/violenta-domestica/ordinul-de-protectie-provizoriu |
| `b18.domestic_violence_protection_order.provisional_measures` | Poliția Română | verified | https://politiaromana.ro/ro/prevenire/violenta-domestica/ordinul-de-protectie-provizoriu |
| `b18.domestic_violence_protection_order.provisional_duration_flow` | Poliția Română | verified | https://politiaromana.ro/ro/prevenire/violenta-domestica/ordinul-de-protectie-provizoriu |
| `b18.domestic_violence_protection_order.provisional_contest` | Poliția Română | verified | https://politiaromana.ro/ro/prevenire/violenta-domestica/ordinul-de-protectie-provizoriu |
| `b18.domestic_violence_protection_order.court_competence_fee` | Portalul Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/44014 |
| `b18.domestic_violence_protection_order.applicants_form` | Portalul Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/44014 |
| `b18.domestic_violence_protection_order.legal_aid_72h` | Portalul Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/44014 |
| `b18.domestic_violence_protection_order.duration_repeat` | Portalul Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/44014 |
| `b18.domestic_violence_protection_order.appeal_3_days` | Portalul Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/44014 |
| `b18.domestic_violence_protection_order.execution_breach` | Portalul Legislativ — Ministerul Justiției | verified | https://legislatie.just.ro/Public/DetaliiDocument/44014 |
| `b18.domestic_violence_protection_order.court_measures` | Poliția Română | verified | https://politiaromana.ro/ro/prevenire/violenta-domestica/ordinul-de-protectie |
| `b18.domestic_violence_protection_order.local_filing_gap` | Portalul Legislativ — Ministerul Justiției | verified_with_local_gap | https://legislatie.just.ro/Public/DetaliiDocument/44014 |
===
