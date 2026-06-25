===
# Event Card — ro.life.health_card_lost (life.health_card_lost)

- batch_id: `B06_HEALTH_CARD_LOST`
- status: `research_inbox`
- publication_gate: `blocked_pending_human_review`
- pilot: `ro.tm.timisoara`
- accessed_at: `2026-06-25`
- title_ro: Mi-am pierdut / mi-a fost furat cardul de sănătate

## Declanșator

Asiguratul are nevoie de un card duplicat după pierdere, furt, distrugere, schimbarea numelui sau date eronate.

## Fapte cerute

| fact | tip | valori / observații |
|---|---|---|
| `replacement_reason` | `enum` | lost \| stolen \| destroyed \| name_changed \| data_error |
| `insured_county` | `string` | județul casei în evidența căreia se află asiguratul |
| `requester_role` | `enum` | holder \| legal_representative \| authorized_person |
| `submission_channel` | `enum\|null` | in_person \| email \| postal |
| `new_card_requested` | `boolean\|null` | activează adeverința de înlocuire |
| `asks_card_validity` | `boolean\|null` | expune conflictul CNAS 5 ani vs 7 ani |
| `replacement_certificate_validity_state` | `enum\|null` | valid \| expired; calculat față de termenul verificat de 3 luni |

## Reguli verificate

- Duplicatul pentru pierdere/furt/nume schimbat folosește cerere tip, copie CI și dovada plății de 20,36 lei.
- Documentele pot fi transmise prin e-mail la CAS competentă, dar adresa și formatele locale trebuie confirmate.
- Înlocuirea pentru date eronate este gratuită.
- Adeverința de înlocuire este valabilă trei luni de la eliberare.

## Conflicte și limitări

- Două pagini CNAS active indică valabilitatea cardului ca 5 ani, respectiv 7 ani; durata rămâne `conflicting` și nu este afișată automat.

## Canal pilot Timiș/Timișoara

- CAS în evidența căreia se află asiguratul.
- Pilot Timiș: CAS Timiș, Timișoara, str. Corbului nr. 4, tel. 0736-110007, site castm.

## Control de publicare

- source_claims: `10`
- rules: `14`
- golden_fixtures: `22`
- output_status: `draft_not_for_automatic_publication`
===
