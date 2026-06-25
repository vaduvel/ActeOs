# Event Card — ro.life.family_death

**Batch:** B03_FAMILY_DEATH  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România + `RO-TM-TIMISOARA`  
**Data de referință și acces:** 2026-06-25

## Declanșator

„A decedat o persoană din familie” și trebuie să rezolv actele imediate, ajutorul de deces și succesiunea.

## Limita evenimentului

Acoperă înregistrarea decesului, ramurile CNPP pentru ajutor și legătura cu succesiunea. Pentru soț/soție deschide traseul extins dedicat pensiei de urmaș.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `death_registered` | `boolean` | `true`, `false` | arată dacă starea civilă a fost deja rezolvată |
| `days_since_death` | `integer` | 0–n | detectează depășirea termenului general |
| `death_cause` | `enum` | `natural`, `violent`, `accident`, `suicide`, `body_found` | activează dovada specială |
| `deceased_benefit_status` | `enum` | `direct_eligible`, `noninsured_family_member`, `not_eligible`, `unknown` | selectează ramura CNPP fără presupuneri |
| `paid_funeral_expenses` | `boolean` | `true`, `false` | determină dovada solicitantului |
| `estate_may_exist` | `boolean` | `true`, `false` | deschide evaluarea succesiunii |
| `relation_to_deceased` | `enum` | `spouse`, `parent`, `child`, `sibling`, `other` | activează traseul de soț supraviețuitor |
| `territory_id` | `jurisdiction_id` | ex. `RO-TM-TIMISOARA` | alege canalul local și sesizarea succesorală |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| `ro.civil_status.death.register_family_member` | `conditional` | — | deces înregistrat |
| `ro.social_insurance.death_benefit.assess_family` | `conditional` | `ro.civil_status.death.register_family_member` | eligibilitate și dosar CNPP verificate |
| `ro.succession.case.assess` | `conditional` | `ro.civil_status.death.register_family_member` | traseu succesoral deschis |

## Canale oficiale

- **Primăria Timișoara — Deces** — pilot local: https://servicii.primariatm.ro/deces
- **CNPP — Ajutorul de deces** — național: https://www.cnpp.ro/ajutorul-de-deces
- **Primăria Timișoara — Evidența persoanelor** — sesizare succesorală: https://www.primariatm.ro/evidenta-persoanelor

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este un prag conservator de verificare pentru acest draft, nu data istorică presupusă a intrării în vigoare.
- Taxele, termenele sau documentele dinamice neconfirmate dintr-o sursă oficială curentă nu produc efect critic; ele apar ca `require_confirmation` și în `gaps.md`.
- Pentru alt UAT decât Timișoara, canalul local este marcat `verified_with_local_gap`; regula națională rămâne separată de operaționalizarea locală.

## Observație de integrare

Enum-ul `deceased_benefit_status` trebuie alimentat de un chestionar ghidat sau confirmare CNPP; nu se deduce din relația de rudenie.
