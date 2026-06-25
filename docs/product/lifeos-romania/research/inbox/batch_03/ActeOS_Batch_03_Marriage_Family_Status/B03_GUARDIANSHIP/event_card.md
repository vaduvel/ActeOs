# Event Card — ro.life.guardianship

**Batch:** B03_GUARDIANSHIP  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România + `RO-TM-TIMISOARA`  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Am fost numit tutore / ocrotitor și trebuie să fiu luat în evidență” sau „Trebuie să obțin măsura de ocrotire”.

## Limita evenimentului

Separă instituirea judiciară, încă necercetată complet, de luarea în evidență post-hotărâre la Autoritatea Tutelară Timișoara pentru minori și adulți.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `protected_person_type` | `enum` | `minor`, `adult` | alege lista oficială distinctă |
| `court_judgment_final` | `boolean` | `true`, `false` | separă instanța de evidența post-hotărâre |
| `territory_id` | `jurisdiction_id` | ex. `RO-TM-TIMISOARA` | lista de documente este locală |
| `guardian_married` | `boolean` | `true`, `false` | activează acordul soțului din lista locală |
| `protected_person_age` | `integer` | 0–n | pentru minor activează actul de identitate la 14 ani |
| `online_submission` | `boolean` | `true`, `false` | alege canalul online/ghișeu |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| `ro.court.guardianship.obtain_final_judgment` | `conditional` | — | măsură de ocrotire definitivă |
| `ro.tutelary_authority.minor.register_guardianship` | `conditional` | `ro.court.guardianship.obtain_final_judgment` | tutela minorului luată în evidență |
| `ro.tutelary_authority.adult.register_protection` | `conditional` | `ro.court.guardianship.obtain_final_judgment` | adultul ocrotit luat în evidență |

## Canale oficiale

- **Primăria Timișoara — Evidență tutelă minori** — pilot local: https://servicii.primariatm.ro/evidenta-tutela-minori
- **Primăria Timișoara — Persoane ocrotite legal** — pilot local: https://servicii.primariatm.ro/persoane-ocrotite-legal
- **Portal Legislativ — Codul civil** — ruta judiciară de extras: https://legislatie.just.ro/Public/DetaliiDocument/109883

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este un prag conservator de verificare pentru acest draft, nu data istorică presupusă a intrării în vigoare.
- Taxele, termenele sau documentele dinamice neconfirmate dintr-o sursă oficială curentă nu produc efect critic; ele apar ca `require_confirmation` și în `gaps.md`.
- Pentru alt UAT decât Timișoara, canalul local este marcat `verified_with_local_gap`; regula națională rămâne separată de operaționalizarea locală.

## Observație de integrare

Listele locale sunt folosite numai după hotărârea definitivă. Motorul nu confundă Autoritatea Tutelară cu instanța care instituie măsura.
