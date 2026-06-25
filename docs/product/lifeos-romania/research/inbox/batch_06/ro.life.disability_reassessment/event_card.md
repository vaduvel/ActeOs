===
# Event Card — ro.life.disability_reassessment (life.disability_reassessment)

- batch_id: `B06_DISABILITY_REASSESSMENT`
- status: `research_inbox`
- publication_gate: `blocked_pending_human_review`
- pilot: `ro.tm.timisoara`
- accessed_at: `2026-06-25`
- title_ro: Trebuie să fac reevaluarea certificatului de handicap

## Declanșator

Certificatul copilului sau adultului urmează să expire, există agravare/convocare ori este necesară revizuirea separată a PIRIS.

## Fapte cerute

| fact | tip | valori / observații |
|---|---|---|
| `person_type` | `enum` | child \| adult |
| `certificate_validity` | `enum` | fixed \| permanent |
| `reassessment_reason` | `enum` | expiry \| aggravation \| authority_summons \| piris_revision \| transition_to_adult |
| `county` | `string` | TM pentru pilot |
| `expiry_date` | `date\|null` | obligatorie pentru calculul termenului la certificat determinat |
| `previous_degree` | `enum\|null` | severe \| accentuated \| medium \| mild |
| `home_evaluation_requested` | `boolean\|null` | pentru adultul încadrat anterior grav |
| `certificate_expiry_state` | `enum\|null` | active \| due \| expired; calculat din expiry_date |

## Reguli verificate

- Adultul cu certificat determinat se prezintă cu cel puțin 30 de zile înainte de expirare.
- Pentru copil, solicitarea reevaluării se face cu cel puțin 60 de zile înainte de expirare și dosarul include certificatul în vigoare.
- Certificatul permanent nu generează reevaluare periodică; reevaluarea rămâne posibilă la agravare sau convocare pentru suspiciuni justificate.
- Adultul încadrat anterior în grad grav poate cere evaluare periodică la domiciliu.
- În pilotul Timiș, revizuirea PIRIS este tratată ca rută separată de reevaluarea certificatului.

## Conflicte și limitări

- Nu a fost identificat conflict normativ; termenele de 30 și 60 de zile se aplică unor categorii diferite și nu se combină.

## Canal pilot Timiș/Timișoara

- Adult Timiș: DGASPC Timiș, Piața Regina Maria nr. 3, Timișoara.
- Copil Timiș: Serviciul de Evaluare Complexă a Copilului, tel. 0256/494497.
- În afara Timișului: DGASPC competentă, marcată `verified_with_local_gap`.

## Control de publicare

- source_claims: `12`
- rules: `17`
- golden_fixtures: `22`
- output_status: `draft_not_for_automatic_publication`
===
