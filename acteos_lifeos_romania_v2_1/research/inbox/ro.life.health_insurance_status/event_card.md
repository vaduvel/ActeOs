===
# Event Card — ro.life.health_insurance_status (life.health_insurance_status)

- batch_id: `B06_HEALTH_INSURANCE_STATUS`
- status: `research_inbox`
- publication_gate: `blocked_pending_human_review`
- pilot: `ro.tm.timisoara`
- accessed_at: `2026-06-25`
- title_ro: Vreau să verific sau să corectez calitatea de asigurat

## Declanșator

Persoana verifică dacă figurează ca asigurată, primește un rezultat negativ/neclar sau are nevoie să identifice ruta de dobândire/corectare.

## Fapte cerute

| fact | tip | valori / observații |
|---|---|---|
| `can_use_online_check` | `boolean` | dacă utilizatorul poate accesa SIUI |
| `status_result` | `enum` | insured \| not_insured \| portal_unavailable \| unknown |
| `insurance_category` | `enum\|null` | employee \| student_18_26 \| no_employment_or_taxable_income \| other |
| `age` | `integer\|null` | pentru ruta student |
| `education_form` | `enum\|null` | day \| part_time \| distance |
| `county` | `string\|null` | TM pentru pilot |
| `d212_period_state` | `enum\|null` | active \| elapsed; calculat din data depunerii |
| `status_result_freshness` | `enum\|null` | fresh \| stale; data verificării raportată la data curentă |

## Reguli verificate

- Verificarea se face în aplicația SIUI indicată de CNAS; de la 1 martie 2025 CNAS publică adresa curentă.
- Un rezultat `not_insured` cere identificarea categoriei și a documentelor; nu explică singur cauza.
- Pentru categoria fără venituri descrisă de CNAS, D212 acordă calitatea pentru 12 luni de la depunere; suma actuală trebuie verificată la ANAF.
- Pentru tinerii 18–26 la zi sunt necesare CI și document valabil de elev/student, cu verificarea condițiilor de venit.

## Conflicte și limitări

- FAQ CNAS conține un exemplu monetar din 2022; acesta nu este folosit pentru cuantumul din 2026 și este tratat ca informație învechită.

## Canal pilot Timiș/Timișoara

- SIUI — verificare calitate asigurat.
- CAS teritorială pentru corectare și documente.
- Pilot Timiș: CAS Timiș, str. Corbului nr. 4, tel. 0736-110007.

## Control de publicare

- source_claims: `7`
- rules: `16`
- golden_fixtures: `22`
- output_status: `draft_not_for_automatic_publication`
===
