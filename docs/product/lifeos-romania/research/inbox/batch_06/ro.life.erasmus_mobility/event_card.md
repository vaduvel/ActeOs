===
# Event Card — ro.life.erasmus_mobility (life.erasmus_mobility)

- batch_id: `B06_ERASMUS_MOBILITY`
- status: `research_inbox`
- publication_gate: `blocked_pending_human_review`
- pilot: `ro.tm.timisoara`
- accessed_at: `2026-06-25`
- title_ro: Vreau să aplic sau să finalizez o mobilitate Erasmus+

## Declanșator

Studentul explorează, aplică, a fost selectat, se află în mobilitate sau cere recunoașterea rezultatelor după întoarcere.

## Fapte cerute

| fact | tip | valori / observații |
|---|---|---|
| `home_institution` | `string` | UPT pentru pilot; altă instituție → gap instituțional |
| `mobility_type` | `enum` | study \| traineeship \| blended_short \| doctoral \| free_mover |
| `application_stage` | `enum` | exploring \| applying \| selected \| on_mobility \| returned |
| `call_year` | `string\|null` | anul academic al apelului |
| `host_documents_available` | `boolean\|null` | pentru recunoaștere |
| `claimed_grant_amount` | `number\|null` | declanșează confirmarea, nu devine adevăr |
| `call_matches_target_year` | `boolean\|null` | adevărat numai dacă apelul oficial este pentru anul universitar țintă |

## Reguli verificate

- Calitatea de student se menține pe durata mobilității.
- Recunoașterea creditelor se bazează pe documentele relevante ale instituției gazdă.
- Termenele, documentele de candidatură și grantul sunt call-specific; nu se reutilizează automat dintr-un an anterior.
- Pilot UPT: canal outgoing la DRI, Rectorat, Piața Victoriei nr. 2.

## Conflicte și limitări

- Nu a fost identificat un conflict normativ; principalul risc este folosirea unui apel vechi sau a unei sume neactualizate.

## Canal pilot Timiș/Timișoara

- UPT DRI — outgoing: +40 256 403 034, erasmus.outgoing@upt.ro.
- Pentru altă universitate, biroul Erasmus/relatii internaționale al instituției de origine.
- ANPCDEFP este administrator național al programului, nu înlocuiește procedura universității.

## Control de publicare

- source_claims: `8`
- rules: `12`
- golden_fixtures: `22`
- output_status: `draft_not_for_automatic_publication`
===
