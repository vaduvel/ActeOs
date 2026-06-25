===
# Event Card — ro.life.disability_certificate (life.disability_certificate)

- batch_id: `B06_DISABILITY_CERTIFICATE`
- status: `research_inbox`
- publication_gate: `blocked_pending_human_review`
- pilot: `ro.tm.timisoara`
- accessed_at: `2026-06-25`
- title_ro: Vreau certificat de încadrare în grad de handicap

## Declanșator

Copilul sau adultul are nevoie de evaluare și de emiterea certificatului, ori adultul contestă certificatul comunicat.

## Fapte cerute

| fact | tip | valori / observații |
|---|---|---|
| `person_type` | `enum` | child \| adult |
| `request_type` | `enum` | initial \| appeal |
| `county` | `string` | TM pentru pilot |
| `requester_role` | `enum\|null` | self \| family \| legal_representative \| assistant \| ngo |
| `previous_degree` | `enum\|null` | severe \| accentuated \| medium \| mild \| none |
| `home_evaluation_requested` | `boolean\|null` | relevant pentru adult încadrat anterior grav |
| `certificate_issued` | `boolean\|null` | activează pasul PIRIS/valabilitate |

## Reguli verificate

- Adultul este încadrat de comisia de evaluare pe baza raportului de evaluare complexă; copilul, de comisia pentru protecția copilului.
- Certificatul adultului este scutit de taxa de timbru și poate fi contestat în 30 de zile calendaristice de la comunicare.
- Pentru copil, art. 44 din Ordinul nr. 1.305/2016 stabilește dosarul minim național.
- Valabilitatea obișnuită a certificatului copilului este 6 luni–2 ani, cu excepțiile legale modelate separat.
- Evaluarea la domiciliu este verificată pentru adultul încadrat anterior în grad grav, la cerere.

## Conflicte și limitări

- Nu a fost identificat un conflict normativ; lista completă a dosarului adultului și operațiunile locale rămân dependente de DGASPC competentă.

## Canal pilot Timiș/Timișoara

- Adult Timiș: DGASPC Timiș, Piața Regina Maria nr. 3, Timișoara, program conform paginii oficiale.
- Copil Timiș: Serviciul de Evaluare Complexă a Copilului, tel. 0256/494497, cu programare.
- Contestația adultului: Comisia superioară de evaluare a persoanelor adulte cu handicap.

## Control de publicare

- source_claims: `14`
- rules: `16`
- golden_fixtures: `22`
- output_status: `draft_not_for_automatic_publication`
===
