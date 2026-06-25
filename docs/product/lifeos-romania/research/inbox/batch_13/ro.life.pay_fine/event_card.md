# Event Card — ro.life.pay_fine

**Batch:** B13_PAY_FINE  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România; regula națională OG nr. 2/2001  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Vreau să plătesc o amendă și să verific reducerea.”

## Limita evenimentului

Distinge regula generală de excepția 2026 pentru construcții/urbanism, verifică fereastra de 15 zile și canalul de plată. Nu calculează suma dacă lipsește baza legală sau cuantumul relevant.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `fine_domain` | enum | `general`, `construction_urbanism`, `traffic`, `other_special` | selectează formula legală |
| `days_since_delivery` | integer | >= 0 | verifică fereastra de 15 zile |
| `pv_mentions_reduced_payment` | boolean | `true`, `false` | mențiunea din procesul-verbal este critică |
| `minimum_amount_known` | boolean | `true`, `false` | regula generală folosește minimul legal |
| `applied_amount_known` | boolean | `true`, `false` | regula specială folosește amenda aplicată |
| `construction_exception_applies` | boolean|string | `true`, `false`, `unknown` | exclude sau blochează reducerea specială |
| `budget_destination` | enum | `state`, `local`, `unknown` | alege contul și canalul corect |
| `payment_channel_preference` | enum | `online`, `bank`, `treasury`, `cashier`, `unknown` | atașează doar canalul compatibil |
| `wants_to_contest` | boolean | `true`, `false` | activează traseul plângerii |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| ro.fine.read_process_verbal | mandatory | — | data comunicării, actul și bugetul identificate |
| ro.fine.determine_reduced_amount_basis | conditional | ro.fine.read_process_verbal | minimul legal sau amenda aplicată identificate |
| ro.fine.pay | mandatory | ro.fine.determine_reduced_amount_basis | plată în contul oficial și dovadă păstrată |
| ro.fine.complain | conditional | ro.fine.read_process_verbal | plângere depusă în termenul aplicabil |

## Canale oficiale

- **OG nr. 2/2001 — forma consolidată** — https://legislatie.just.ro/Public/DetaliiDocument/29779

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este pragul de verificare al draftului, nu o afirmație despre data istorică de intrare în vigoare.
- Nicio sumă, taxă, reducere, penalitate sau listă de documente dinamică nu este calculată fără claim oficial aplicabil și fapt de intrare confirmat.
- Claim-urile `needs_confirmation`, `conflicting` ori `expired` nu pot produce singure un efect critic favorabil utilizatorului.
- Pentru alt UAT decât Timișoara, operaționalizarea locală rămâne `verified_with_local_gap`; regulile naționale sunt păstrate separat.

## Observație de integrare

Din 27 martie 2026, pentru anumite amenzi de construcții/urbanism, «jumătate» nu mai are aceeași bază ca regula generală. Motorul le separă explicit.
