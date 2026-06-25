# Event Card — ro.life.tax_decision_contest

**Batch:** B13_TAX_DECISION_CONTEST  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România; autorități fiscale centrale și pilot local Timișoara  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Vreau să contest o decizie fiscală.”

## Limita evenimentului

Ajută la clasificarea actului, păstrarea dovezii comunicării, structurarea motivelor și verificarea termenului înscris. Nu promite un termen hardcodat, nu stabilește competența și nu oferă consultanță juridică individuală.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `act_type` | enum | `tax_decision`, `other_tax_admin_act`, `enforcement_act`, `unknown` | alege calea procedurală |
| `days_since_communication` | integer | >= 0 | măsoară urgența față de data comunicării |
| `act_instruction_deadline_days` | integer | termenul citit din act sau 0 | evită inventarea termenului |
| `within_instruction_window` | boolean | `true`, `false` | rezultatul comparației făcute de utilizator cu termenul din act |
| `receiving_authority_known` | boolean | `true`, `false` | previne trimiterea la organ greșit |
| `grounds_ready` | boolean | `true`, `false` | verifică existența motivelor |
| `evidence_ready` | boolean | `true`, `false` | inventariază înscrisurile |
| `suspension_requested` | boolean | `true`, `false` | deschide verificarea unei proceduri distincte |
| `issuing_authority_scope` | enum | `central_anaf`, `local_timisoara`, `other_local`, `unknown` | selectează instrucțiunile autorității emitente |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| ro.tax.contest.classify_act | mandatory | — | actul și calea procedurală clasificate |
| ro.tax.contest.verify_deadline | mandatory | ro.tax.contest.classify_act | termen verificat din act și lege |
| ro.tax.contest.prepare | conditional | ro.tax.contest.verify_deadline | contestație motivată și semnată |
| ro.tax.contest.suspension | conditional | ro.tax.contest.classify_act | remediul de suspendare evaluat separat |

## Canale oficiale

- **Codul de procedură fiscală — forma consolidată** — https://legislatie.just.ro/Public/DetaliiDocument/170005

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este pragul de verificare al draftului, nu o afirmație despre data istorică de intrare în vigoare.
- Nicio sumă, taxă, reducere, penalitate sau listă de documente dinamică nu este calculată fără claim oficial aplicabil și fapt de intrare confirmat.
- Claim-urile `needs_confirmation`, `conflicting` ori `expired` nu pot produce singure un efect critic favorabil utilizatorului.
- Pentru alt UAT decât Timișoara, operaționalizarea locală rămâne `verified_with_local_gap`; regulile naționale sunt păstrate separat.

## Observație de integrare

Motorul folosește termenul introdus din act doar ca indiciu de lucru. Până la validarea articolului consolidat, nu afișează un countdown juridic verde.
