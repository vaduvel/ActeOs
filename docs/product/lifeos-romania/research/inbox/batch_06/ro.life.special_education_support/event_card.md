===
# Event Card — ro.life.special_education_support (life.special_education_support)

- batch_id: `B06_SPECIAL_EDUCATION_SUPPORT`
- status: `research_inbox`
- publication_gate: `blocked_pending_human_review`
- pilot: `ro.tm.timisoara`
- accessed_at: `2026-06-25`
- title_ro: Am nevoie de sprijin de educație specială / orientare școlară

## Declanșator

Părintele, reprezentantul legal ori școala urmărește evaluarea, orientarea/reorientarea sau contestarea certificatului pentru un copil/elev cu CES.

## Fapte cerute

| fact | tip | valori / observații |
|---|---|---|
| `county` | `string` | TM pentru pilot; alt județ → gap local |
| `request_type` | `enum` | initial_orientation \| reorientation \| appeal \| counseling_only |
| `child_enrolled` | `boolean` | dacă elevul frecventează deja o unitate |
| `signed_acknowledgement_date` | `date\|null` | pentru termenul contestației |
| `certificate_issue_date` | `date\|null` | pentru transmiterea certificatului |
| `case_manager_appointment_date` | `date\|null` | pentru termenul PSI |
| `appeal_deadline_state` | `enum\|null` | within \| outside \| uncertain; rezultat calculat cu calendarul de zile lucrătoare |

## Reguli verificate

- Cererea de orientare și dosarul se depun la CJRAE/CMBRAE.
- Reorientarea adaugă certificatul anterior și, în pilotul Timiș, PSI plus raportul de monitorizare, după caz.
- Contestația: 5 zile lucrătoare de la luarea la cunoștință; soluționare: 30 de zile de la depunere.
- Pilot Timiș: CEOSP, Piața Regina Maria nr. 3; primire dosare luni și miercuri 9:00–15:00.

## Conflicte și limitări

- Pagina locală Timiș rezumă valabilitatea certificatului până la finalul nivelului; regula națională verificată este „minimum un an școlar sau până la finalizarea nivelului”. Se aplică textul normativ.

## Canal pilot Timiș/Timișoara

- CJRAE/CMBRAE din județul copilului.
- Pilot: CEOSP/COSP Timiș, Piața Regina Maria nr. 3, Timișoara; instituția programează evaluarea după depunerea dosarului.

## Control de publicare

- source_claims: `12`
- rules: `14`
- golden_fixtures: `22`
- output_status: `draft_not_for_automatic_publication`
===
