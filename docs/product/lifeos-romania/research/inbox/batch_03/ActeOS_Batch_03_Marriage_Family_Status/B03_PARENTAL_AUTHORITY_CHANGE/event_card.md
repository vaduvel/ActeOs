# Event Card — ro.life.parental_authority_change

**Batch:** B03_PARENTAL_AUTHORITY_CHANGE  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România + `RO-TM-TIMISOARA`  
**Data de referință și acces:** 2026-06-25

## Declanșator

„S-a schimbat autoritatea părintească și trebuie să dovedesc cine poate solicita actele copilului”.

## Limita evenimentului

Acoperă efectul documentului de autoritate asupra solicitării CEI pentru copil. Nu modelează integral procesul de modificare a autorității în instanță.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `authority_basis` | `enum` | `joint_parents`, `surviving_parent`, `sole_final_judgment`, `custody_final_judgment`, `presidential_order`, `other` | alege persoana și documentul doveditor |
| `court_document_final` | `boolean` | `true`, `false` | evită folosirea unui act judiciar neconfirmat |
| `child_age` | `integer` | 0–17 | separă ruta CEI opțională sub 14 ani de ruta 14+ |
| `request_child_cei` | `boolean` | `true`, `false` | determină dacă schimbarea are un efect administrativ imediat |
| `parents_disagree` | `boolean` | `true`, `false` | activează hotărârea definitivă cerută de lege |
| `territory_id` | `jurisdiction_id` | ex. `RO-TM-TIMISOARA` | păstrează contextul, deși canalul CEI este național |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| `ro.family.parental_authority.verify_document` | `mandatory` | — | temeiul solicitantului validat |
| `ro.identity.child.request_cei_under14` | `conditional` | `ro.family.parental_authority.verify_document` | cerere CEI sub 14 ani depusă corect |
| `ro.identity.child.request_document_age14plus` | `conditional` | `ro.family.parental_authority.verify_document` | ruta 14+ deschisă |

## Canale oficiale

- **Portal Legislativ — OUG nr. 97/2005** — temei național: https://legislatie.just.ro/Public/DetaliiDocument/63354
- **MAI — programări CEI** — canal național: https://hub.mai.gov.ro/
- **Primăria Timișoara — CEI** — informații operaționale: https://www.primariatm.ro/CI-electronic

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este un prag conservator de verificare pentru acest draft, nu data istorică presupusă a intrării în vigoare.
- Taxele, termenele sau documentele dinamice neconfirmate dintr-o sursă oficială curentă nu produc efect critic; ele apar ca `require_confirmation` și în `gaps.md`.
- Pentru alt UAT decât Timișoara, canalul local este marcat `verified_with_local_gap`; regula națională rămâne separată de operaționalizarea locală.

## Observație de integrare

Motorul nu deduce autoritatea părintească din declarații. Acceptă numai categoria documentului și solicită actul definitiv/expres prevăzut de sursa oficială.
