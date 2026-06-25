# Event Card — ro.life.marriage_planning

**Batch:** B03_MARRIAGE_PLANNING  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România + `RO-TM-TIMISOARA`  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Vreau să mă căsătoresc civil” / „Ce acte îmi trebuie pentru cununia civilă?”.

## Limita evenimentului

Acoperă depunerea declarației, fereastra legală, documentele de bază și variantele minor/cetățean străin. Nu acoperă ceremonia religioasă sau organizarea evenimentului privat.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `applicant_age` | `integer` | 0–120 | separă adultul de ruta specială 16–17 ani și de blocajul sub 16 ani |
| `partner_age` | `integer` | 0–120 | aceeași regulă pentru celălalt viitor soț |
| `prior_marriage_status` | `enum` | `never_married`, `ended`, `current_marriage` | dovada încetării sau impediment |
| `foreign_citizen_involved` | `boolean` | `true`, `false` | activează documente străine și verificarea formei |
| `territory_id` | `jurisdiction_id` | ex. `RO-TM-TIMISOARA` | alege canalul local fără a generaliza Timișoara |
| `desired_days_from_declaration` | `integer` | 0–365 | testează fereastra 11–30 zile |
| `surname_choice_known` | `boolean` | `true`, `false` | declarația trebuie să conțină numele după căsătorie |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| `ro.civil_status.marriage.file_declaration` | `mandatory` | — | declarație și dosar depuse |
| `ro.civil_status.marriage.resolve_special_route` | `conditional` | `ro.civil_status.marriage.file_declaration` | autorizări/documente speciale confirmate |
| `ro.civil_status.marriage.celebrate` | `mandatory` | `ro.civil_status.marriage.file_declaration` | căsătoria civilă înregistrată |

## Canale oficiale

- **Portal Legislativ — Legea nr. 119/1996** — reguli naționale: https://legislatie.just.ro/Public/DetaliiDocument/8624
- **Primăria Timișoara — Căsătorie** — pilot local: https://servicii.primariatm.ro/casatorie

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este un prag conservator de verificare pentru acest draft, nu data istorică presupusă a intrării în vigoare.
- Taxele, termenele sau documentele dinamice neconfirmate dintr-o sursă oficială curentă nu produc efect critic; ele apar ca `require_confirmation` și în `gaps.md`.
- Pentru alt UAT decât Timișoara, canalul local este marcat `verified_with_local_gap`; regula națională rămâne separată de operaționalizarea locală.

## Observație de integrare

Regulile de vârstă 16–17 și forma documentelor străine rămân `in_review`; motorul nu presupune automat apostilă, supralegalizare sau autorizarea aplicabilă.
