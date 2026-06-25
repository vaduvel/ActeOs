# Event Card — ro.life.tax_refund_request

**Batch:** B13_TAX_REFUND_REQUEST  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** Național pentru cadrul fiscal; pilot operațional Municipiul Timișoara  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Vreau să recuperez sau să compensez o sumă plătită la fisc.”

## Limita evenimentului

Separă restituirea de compensare și identifică autoritatea competentă. Pentru Timișoara indică Atlas; pentru ANAF și alte UAT păstrează canalul și termenul ca neconfirmate.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `authority_scope` | enum | `central_anaf`, `local_timisoara`, `other_local`, `unknown` | identifică organul fiscal competent |
| `refund_or_compensation` | enum | `refund`, `compensation`, `unknown` | alege rezultatul cerut |
| `refund_basis_evidence_available` | boolean | `true`, `false` | verifică dovada dreptului la sumă |
| `known_outstanding_debts` | boolean|string | `true`, `false`, `unknown` | poate schimba ordinea operațiunilor |
| `request_already_submitted` | boolean | `true`, `false` | separă pregătirea de urmărirea cererii |
| `bank_account_available` | boolean | `true`, `false` | semnalează datele de plată ce pot fi cerute |
| `territory_id` | jurisdiction id | ex. `RO-TM-TIMISOARA` | previne folosirea procedurii Timișoara în alt UAT |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| ro.tax.refund.identify_authority | mandatory | — | buget și organ fiscal identificate |
| ro.tax.refund.prepare_refund | conditional | ro.tax.refund.identify_authority | cerere de restituire pregătită |
| ro.tax.refund.prepare_compensation | conditional | ro.tax.refund.identify_authority | cerere de compensare pregătită |
| ro.tax.refund.track | conditional | ro.tax.refund.prepare_refund | cerere urmărită pe dovada depunerii |

## Canale oficiale

- **Timișoara — cererea de restituire** — https://servicii.primariatm.ro/dfmt-pj-cerere-restituire
- **Timișoara — cererea de compensare** — https://servicii.primariatm.ro/dfmt-pj-cerere-compensare
- **Codul de procedură fiscală** — https://legislatie.just.ro/Public/DetaliiDocument/170005

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este pragul de verificare al draftului, nu o afirmație despre data istorică de intrare în vigoare.
- Nicio sumă, taxă, reducere, penalitate sau listă de documente dinamică nu este calculată fără claim oficial aplicabil și fapt de intrare confirmat.
- Claim-urile `needs_confirmation`, `conflicting` ori `expired` nu pot produce singure un efect critic favorabil utilizatorului.
- Pentru alt UAT decât Timișoara, operaționalizarea locală rămâne `verified_with_local_gap`; regulile naționale sunt păstrate separat.

## Observație de integrare

«Restituire» și «compensare» nu sunt sinonime. Motorul nu decide automat ordinea lor când există datorii, fiindcă regula materială trebuie validată separat.
