# Event Card — ro.life.spouse_death

**Batch:** B03_SPOUSE_DEATH  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România + `RO-TM-TIMISOARA`  
**Data de referință și acces:** 2026-06-25

## Declanșator

„A decedat soțul / soția” și trebuie să rezolv înregistrarea, ajutorul de deces, pensia de urmaș și eventual succesiunea.

## Limita evenimentului

Acoperă primele trasee administrative verificabile. Nu decide automat eligibilitatea financiară pentru pensia de urmaș și nu calculează cuantumuri dinamice.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `death_registered` | `boolean` | `true`, `false` | arată dacă mai este necesară înregistrarea de stare civilă |
| `days_since_death` | `integer` | 0–n | separă termenul general de înregistrarea tardivă |
| `death_cause` | `enum` | `natural`, `violent`, `accident`, `suicide`, `body_found` | activează dovada poliției/parchetului |
| `deceased_pension_condition` | `enum` | `eligible`, `not_eligible`, `unknown` | selectează verificarea CNPP fără a presupune statutul |
| `paid_funeral_expenses` | `boolean` | `true`, `false` | ajutorul se leagă de dovada cheltuielilor |
| `survivor_profile` | `enum` | `standard_age`, `invalidity`, `temporary_6m`, `child_under7`, `unknown`, `none` | alege ramura CNPP de verificat |
| `estate_may_exist` | `boolean` | `true`, `false` | declanșează evenimentul de succesiune |
| `territory_id` | `jurisdiction_id` | ex. `RO-TM-TIMISOARA` | alege canalul local de stare civilă și sesizarea succesorală |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| `ro.civil_status.death.register_spouse` | `conditional` | — | certificat de deces și autorizație emise |
| `ro.social_insurance.death_benefit.claim` | `conditional` | `ro.civil_status.death.register_spouse` | cerere CNPP depusă |
| `ro.social_insurance.survivor_pension.assess` | `conditional` | `ro.civil_status.death.register_spouse` | ruta de pensie de urmaș verificată |
| `ro.succession.case.assess` | `conditional` | `ro.civil_status.death.register_spouse` | eveniment de succesiune deschis |

## Canale oficiale

- **Primăria Timișoara — Deces** — pilot local: https://servicii.primariatm.ro/deces
- **CNPP — Ajutorul de deces** — național: https://www.cnpp.ro/ajutorul-de-deces
- **CNPP — Pensia de urmaș** — național: https://www.cnpp.ro/pensia-de-urmas
- **Primăria Timișoara — Evidența persoanelor** — sesizare succesorală locală: https://www.primariatm.ro/evidenta-persoanelor

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este un prag conservator de verificare pentru acest draft, nu data istorică presupusă a intrării în vigoare.
- Taxele, termenele sau documentele dinamice neconfirmate dintr-o sursă oficială curentă nu produc efect critic; ele apar ca `require_confirmation` și în `gaps.md`.
- Pentru alt UAT decât Timișoara, canalul local este marcat `verified_with_local_gap`; regula națională rămâne separată de operaționalizarea locală.

## Observație de integrare

Selectorul `survivor_profile` indică ramura care trebuie verificată; nu înlocuiește calculul CNPP al condițiilor de venit, durată a căsătoriei sau invaliditate.
