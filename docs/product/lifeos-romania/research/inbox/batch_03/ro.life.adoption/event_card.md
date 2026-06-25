# Event Card — ro.life.adoption

**Batch:** B03_ADOPTION  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România + `RO-TM-TIMISOARA`  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Vreau să adopt un copil” / „În ce etapă a adopției sunt și ce urmează?”.

## Limita evenimentului

Modelează informarea, evaluarea, potrivirea, încredințarea, postadopția și noul act de naștere. Nu inventează dosarul de atestare, termenele sau condițiile speciale.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `applicant_domicile_county` | `enum` | `timis`, `other_ro`, `abroad` | alege autoritatea teritorială și ruta transfrontalieră |
| `adoption_type` | `enum` | `domestic_general`, `spouse_child`, `international`, `unknown` | separă procedurile speciale |
| `workflow_stage` | `enum` | `information`, `evaluation`, `matching`, `placement`, `post_adoption`, `finalized` | determină pasul administrativ curent |
| `has_valid_attestation` | `boolean` | `true`, `false` | controlează accesul la etapa de potrivire |
| `child_identified` | `boolean` | `true`, `false` | separă așteptarea de potrivirea activă |
| `territory_id` | `jurisdiction_id` | ex. `RO-TM-TIMISOARA` | păstrează canalul local separat de regula națională |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| `ro.child_protection.adoption.information` | `mandatory` | — | informare și orientare oficială |
| `ro.child_protection.adoption.evaluate_applicant` | `conditional` | `ro.child_protection.adoption.information` | atestat evaluat |
| `ro.child_protection.adoption.match` | `conditional` | `ro.child_protection.adoption.evaluate_applicant` | potrivire gestionată instituțional |
| `ro.child_protection.adoption.monitor_placement` | `conditional` | `ro.child_protection.adoption.match` | raport de monitorizare |
| `ro.civil_status.birth_record.recreate_after_adoption` | `conditional` | `ro.child_protection.adoption.monitor_placement` | nou act de naștere |

## Canale oficiale

- **DGASPC Timiș — Adopții și Postadopții** — pilot județean: https://www.dgaspctm.ro/pages/serviciul-adoptii-si-postadoptii
- **DGASPC Timiș — Legislație protecția copilului** — registru oficial de acte: https://www.dgaspctm.ro/pages/legislatie-protectia-copilului
- **Portal Legislativ — Legea nr. 119/1996** — noul act de naștere: https://legislatie.just.ro/Public/DetaliiDocument/8624

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este un prag conservator de verificare pentru acest draft, nu data istorică presupusă a intrării în vigoare.
- Taxele, termenele sau documentele dinamice neconfirmate dintr-o sursă oficială curentă nu produc efect critic; ele apar ca `require_confirmation` și în `gaps.md`.
- Pentru alt UAT decât Timișoara, canalul local este marcat `verified_with_local_gap`; regula națională rămâne separată de operaționalizarea locală.

## Observație de integrare

Pagina DGASPC confirmă funcțiile și frecvența monitorizării; condițiile de atestare și procedurile speciale rămân `in_review` până la extragerea Legii nr. 273/2004 și HG nr. 579/2016.
