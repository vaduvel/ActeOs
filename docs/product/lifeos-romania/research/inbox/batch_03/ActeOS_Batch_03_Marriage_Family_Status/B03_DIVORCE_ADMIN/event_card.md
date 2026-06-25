# Event Card — ro.life.divorce_admin

**Batch:** B03_DIVORCE_ADMIN  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România + `RO-TM-TIMISOARA`  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Vreau divorț administrativ” sau „Am divorțat și trebuie să actualizez actele”.

## Limita evenimentului

Separă etapa de inițiere a divorțului administrativ de etapa ulterioară unui divorț definitiv. Ruta notarială și cea judiciară sunt semnalate, dar nu sunt detaliate fără propriile surse.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `workflow_stage` | `enum` | `seeking_divorce`, `divorce_final` | separă eligibilitatea procedurală de actualizarea actelor |
| `spouses_agree` | `boolean` | `true`, `false` | condiție a rutei administrative locale cercetate |
| `has_minor_children` | `boolean` | `true`, `false` | exclude ruta administrativă locală cercetată |
| `parallel_divorce_request` | `boolean` | `true`, `false` | evită deschiderea unei proceduri paralele |
| `name_changed_after_divorce` | `boolean` | `true`, `false` | declanșează înlocuirea actului de identitate după definitivare |
| `territory_id` | `jurisdiction_id` | ex. `RO-TM-TIMISOARA` | taxa, competența și canalul sunt locale |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| `ro.civil_status.divorce.check_admin_eligibility` | `mandatory` | — | ruta administrativă acceptată sau exclusă explicabil |
| `ro.civil_status.divorce.file_admin_request` | `conditional` | `ro.civil_status.divorce.check_admin_eligibility` | cerere depusă și termen de reflecție pornit |
| `ro.identity.document.replace_after_divorce` | `conditional` | — | act actualizat după schimbarea numelui |

## Canale oficiale

- **Primăria Timișoara — Divorț** — pilot local: https://servicii.primariatm.ro/divort
- **Primăria Timișoara — Stare civilă** — atribuții locale curente: https://www.primariatm.ro/stare-civila
- **Portal Legislativ — OUG nr. 97/2005** — actualizare identitate: https://legislatie.just.ro/Public/DetaliiDocument/63354

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este un prag conservator de verificare pentru acest draft, nu data istorică presupusă a intrării în vigoare.
- Taxele, termenele sau documentele dinamice neconfirmate dintr-o sursă oficială curentă nu produc efect critic; ele apar ca `require_confirmation` și în `gaps.md`.
- Pentru alt UAT decât Timișoara, canalul local este marcat `verified_with_local_gap`; regula națională rămâne separată de operaționalizarea locală.

## Observație de integrare

Cuantumul de 745 lei rămâne numai dovada conținutului paginii arhivate; motorul solicită taxa curentă și nu o afișează ca valoare 2026.
