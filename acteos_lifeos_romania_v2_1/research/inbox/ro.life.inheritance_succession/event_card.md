# Event Card — ro.life.inheritance_succession

**Batch:** B03_INHERITANCE_SUCCESSION  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România + `RO-TM-TIMISOARA`  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Trebuie să fac succesiunea” / „A rămas un imobil, un cont sau datorii după deces”.

## Limita evenimentului

Acest draft organizează faptele, documentul de deces, fluxul local de sesizare și punctele unde trebuie verificată procedura notarială. Nu publică termenul opțiunii succesorale, taxa ori competența notarului fără extragerea articolelor oficiale.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `death_certificate_available` | `boolean` | `true`, `false` | document de pornire pentru traseele ulterioare |
| `last_domicile_scope` | `enum` | `timisoara`, `timis_other`, `other_ro`, `abroad` | influențează sesizarea locală și competența ce trebuie verificată |
| `estate_may_exist` | `boolean` | `true`, `false` | arată dacă trebuie deschisă evaluarea masei succesorale |
| `heirs_disagree` | `boolean` | `true`, `false` | poate schimba ruta notarială/judiciară |
| `months_since_death` | `integer` | 0–n | declanșează verificarea urgentă a termenelor și fiscalității |
| `has_immovable_property` | `boolean` | `true`, `false` | adaugă verificările ANCPI și fiscale ulterioare |
| `territory_id` | `jurisdiction_id` | ex. `RO-TM-TIMISOARA` | nu generalizează fluxul local Timișoara |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| `ro.succession.estate.assess` | `mandatory` | — | bunuri, datorii și succesibili inventariați |
| `ro.succession.notary.confirm_competence` | `conditional` | `ro.succession.estate.assess` | notar și dosar confirmați oficial |
| `ro.succession.property.update_post_certificate` | `conditional` | `ro.succession.notary.confirm_competence` | pașii ANCPI/fiscali verificați |

## Canale oficiale

- **Portal Legislativ — Codul civil** — cadru național de extras atomic: https://legislatie.just.ro/Public/DetaliiDocument/109883
- **Primăria Timișoara — Evidența persoanelor** — sesizare succesorală locală: https://www.primariatm.ro/evidenta-persoanelor
- **Primăria Timișoara — Stare civilă** — colaborare locală: https://www.primariatm.ro/stare-civila

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este un prag conservator de verificare pentru acest draft, nu data istorică presupusă a intrării în vigoare.
- Taxele, termenele sau documentele dinamice neconfirmate dintr-o sursă oficială curentă nu produc efect critic; ele apar ca `require_confirmation` și în `gaps.md`.
- Pentru alt UAT decât Timișoara, canalul local este marcat `verified_with_local_gap`; regula națională rămâne separată de operaționalizarea locală.

## Observație de integrare

Acesta este intenționat cel mai conservator eveniment din batch: fără locator oficial complet pentru Codul civil și Legea notarilor, motorul oferă checklist de clarificare, nu concluzii juridice definitive.
