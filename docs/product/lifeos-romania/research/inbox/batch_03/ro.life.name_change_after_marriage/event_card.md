# Event Card — ro.life.name_change_after_marriage

**Batch:** B03_NAME_CHANGE_AFTER_MARRIAGE  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România + `RO-TM-TIMISOARA`  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Mi-am schimbat numele după căsătorie” / „Ce acte trebuie actualizate?”.

## Limita evenimentului

Produce traseul verificat pentru actul de identitate și deschide doar verificări explicite pentru pașaport, permis și documentele vehiculului; nu inventează termenele acestor ramuri.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `name_changed` | `boolean` | `true`, `false` | obligația de înlocuire este declanșată de schimbarea efectivă a numelui |
| `identity_document_type` | `enum` | `cei`, `cis`, `ci_legacy` | alege canalul și competența operațională |
| `has_passport` | `boolean` | `true`, `false` | adaugă verificarea datelor din pașaport |
| `has_driving_licence` | `boolean` | `true`, `false` | adaugă verificarea datelor din permis |
| `owns_vehicle` | `boolean` | `true`, `false` | adaugă verificarea datelor titularului vehiculului |
| `territory_id` | `jurisdiction_id` | ex. `RO-TM-TIMISOARA` | separă canalul local CIS/CI de canalul național CEI |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| `ro.identity.document.replace_after_name_change` | `mandatory` | — | act de identitate actualizat |
| `ro.travel.passport.review_name` | `conditional` | `ro.identity.document.replace_after_name_change` | ruta oficială pentru pașaport confirmată |
| `ro.mobility.licence.review_name` | `conditional` | `ro.identity.document.replace_after_name_change` | ruta DGPCI confirmată |
| `ro.vehicle.registration.review_holder_name` | `conditional` | `ro.identity.document.replace_after_name_change` | datele vehiculului verificate |

## Canale oficiale

- **Portal Legislativ — OUG nr. 97/2005** — obligație națională: https://legislatie.just.ro/Public/DetaliiDocument/63354
- **MAI — programări CEI** — canal național: https://hub.mai.gov.ro/
- **Primăria Timișoara — CEI** — pilot local: https://www.primariatm.ro/CI-electronic
- **Primăria Timișoara — CIS** — pilot local: https://www.primariatm.ro/ci-simpla

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este un prag conservator de verificare pentru acest draft, nu data istorică presupusă a intrării în vigoare.
- Taxele, termenele sau documentele dinamice neconfirmate dintr-o sursă oficială curentă nu produc efect critic; ele apar ca `require_confirmation` și în `gaps.md`.
- Pentru alt UAT decât Timișoara, canalul local este marcat `verified_with_local_gap`; regula națională rămâne separată de operaționalizarea locală.

## Observație de integrare

Doar înlocuirea actului de identitate și termenul de 15 zile sunt efecte critice verificate. Celelalte documente sunt pași de verificare, nu obligații declarate fără sursă.
