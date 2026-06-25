===
# Event Card — ro.life.health_card_blocked (life.health_card_blocked)

- batch_id: `B06_HEALTH_CARD_BLOCKED`
- status: `research_inbox`
- publication_gate: `blocked_pending_human_review`
- pilot: `ro.tm.timisoara`
- accessed_at: `2026-06-25`
- title_ro: Cardul meu de sănătate este blocat sau nu funcționează

## Declanșator

Cardul național nu mai validează serviciul, PIN-ul a fost introdus greșit, este uitat ori cardul/cititorul are o problemă.

## Fapte cerute

| fact | tip | valori / observații |
|---|---|---|
| `issue_type` | `enum` | pin_blocked \| forgotten_pin \| reader_error \| physically_damaged \| not_activated \| card_unavailable |
| `failed_pin_attempts` | `integer` | blocarea verificată apare după 5 încercări consecutive |
| `emergency_service` | `boolean` | urgențele nu necesită card |
| `provider_present` | `boolean\|null` | ruta publicată este inițiată de medic/furnizor |
| `county` | `string\|null` | pentru escaladarea la CAS |
| `needs_cas_guidance` | `boolean\|null` | atașează canalul local |

## Reguli verificate

- După cinci introduceri greșite consecutive ale PIN-ului, cardul se blochează.
- Procedura publicată este inițiată de medic/furnizor prin helpdesk-ul 021.202.6995, cu tichet.
- Serviciile medicale de urgență nu necesită utilizarea cardului.
- O eroare de cititor sau un PIN uitat nu este transformat automat în „card blocat”.

## Conflicte și limitări

- Nu a fost identificat conflict oficial; procedura publică nu descrie complet cazul PIN uitat sau o rută self-service.

## Canal pilot Timiș/Timișoara

- Furnizorul medical aflat în contract, care inițiază tichetul la helpdesk CNAS.
- Helpdesk CNAS card blocat: 021.202.6995.
- CAS Timiș pentru îndrumare locală: str. Corbului nr. 4, tel. 0736-110007.

## Control de publicare

- source_claims: `6`
- rules: `14`
- golden_fixtures: `22`
- output_status: `draft_not_for_automatic_publication`
===
