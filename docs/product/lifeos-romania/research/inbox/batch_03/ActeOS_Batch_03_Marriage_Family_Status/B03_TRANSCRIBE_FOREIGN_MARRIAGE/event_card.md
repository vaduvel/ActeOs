# Event Card — ro.life.transcribe_foreign_marriage

**Batch:** B03_TRANSCRIBE_FOREIGN_MARRIAGE  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România + `RO-TM-TIMISOARA`  
**Data de referință și acces:** 2026-06-25

## Declanșator

„M-am căsătorit în străinătate și vreau să transcriu certificatul în România”.

## Limita evenimentului

Acoperă efectul transcrierii, competența de bază, forma documentului străin, numele, căsătoria anterioară și blocajul legal expres. Nu presupune automat apostila sau taxa.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `romanian_citizen_involved` | `boolean` | `true`, `false` | determină dacă evenimentul de transcriere română este ținta corectă |
| `domicile_case` | `enum` | `common_timisoara`, `different_one_timisoara`, `other_ro`, `never_domiciled`, `consular` | alege competența și canalul |
| `certificate_origin` | `enum` | `eu`, `vienna_multilingual`, `other` | controlează apostila și traducerea |
| `surname_recorded` | `boolean` | `true`, `false` | activează declarația notarială privind numele |
| `months_since_foreign_registration` | `integer` | 0–n | semnalează verificarea termenului de 6 luni |
| `prior_marriage_exists` | `boolean` | `true`, `false` | activează dovada încetării căsătoriei anterioare |
| `same_sex_marriage` | `boolean` | `true`, `false` | aplică blocajul statutar actual fără ambiguitate |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| `ro.civil_status.foreign_marriage.determine_competence` | `mandatory` | — | oficiu competent identificat |
| `ro.civil_status.foreign_marriage.prepare_documents` | `mandatory` | `ro.civil_status.foreign_marriage.determine_competence` | forma actelor străine verificată |
| `ro.civil_status.foreign_marriage.transcribe` | `mandatory` | `ro.civil_status.foreign_marriage.prepare_documents` | căsătoria înscrisă în registrele române |

## Canale oficiale

- **Portal Legislativ — Legea nr. 119/1996** — reguli naționale: https://legislatie.just.ro/Public/DetaliiDocument/8624
- **Primăria Timișoara — Transcrieri certificate** — pilot local: https://servicii.primariatm.ro/transcrieri-certificate
- **Primăria Timișoara — Stare civilă** — atribuții locale: https://www.primariatm.ro/stare-civila

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este un prag conservator de verificare pentru acest draft, nu data istorică presupusă a intrării în vigoare.
- Taxele, termenele sau documentele dinamice neconfirmate dintr-o sursă oficială curentă nu produc efect critic; ele apar ca `require_confirmation` și în `gaps.md`.
- Pentru alt UAT decât Timișoara, canalul local este marcat `verified_with_local_gap`; regula națională rămâne separată de operaționalizarea locală.

## Observație de integrare

Conflictul dintre formularea locală arhivată și textul național privind reperul celor 6 luni este prezent în date și produce confirmare obligatorie; nu este rezolvat prin tăcere.
