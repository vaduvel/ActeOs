# Event Card — ro.life.return_from_parental_leave (life.return_from_parental_leave)

**Batch:** BATCH_04_CHILD_BIRTH_PARENTAL_BENEFITS  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau să revin la serviciu/activitate din concediul pentru creșterea copilului.”

## Limită de domeniu

Acoperă notificarea angajatorului, condițiile revenirii, raportarea modificării către autoritate și hand-off-ul către stimulentul de inserție. Nu înlocuiește litigii de muncă sau calcule salariale.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `is_employee` | boolean | există raport de muncă/serviciu | da |
| `planned_return_date` | date | ancoră notificare 30 zile | da |
| `days_until_return` | integer | calculat la data notificării | condiționat |
| `will_earn_taxable_income` | boolean | declanșează stimulentul | condiționat |
| `income_start_date` | date|null | ancoră 30/15 zile lucrătoare | condiționat |
| `child_birth_date` | date | pentru stimulent | condiționat |
| `child_has_disability` | boolean | pentru pragurile stimulentului | condiționat |
| `ccc_or_incentive_payment_active` | boolean | activează raportarea către primărie | condiționat |
| `both_parents_eligible` | boolean | controlează perioada rezervată | condiționat |
| `other_parent_reserved_period_taken` | boolean | cele 2 luni sunt rezolvate | condiționat |
| `employer_offers_less_favourable_conditions` | boolean | activează protecția la revenire | condiționat |

## Traseu determinist

1. **notify_employer_return** — trimite notificarea scrisă cu minimum 30 zile înainte — `verified`.
2. **verify_return_conditions** — compară postul și îmbunătățirile intervenite — `verified`.
3. **report_return_to_primaria** — comunică schimbarea în 15 zile lucrătoare când afectează plata — `verified_with_local_gap`.
4. **apply_insertion_incentive** — deschide subevenimentul pentru stimulent — `verified`.
5. **resolve_other_parent_reserved_period** — închide regula celor 2 luni dacă este aplicabilă — `verified`.

## Canale oficiale

- `ch.return_parental_leave.timisoara` — canal local pentru comunicarea schimbării/cererea de stimulent — documente dinamice

## Excluderi și hand-off

- Litigiile cu angajatorul sunt predate ITM/instanței/consilierii juridice.
- Stimulentul este evaluat în `life.reinsertion_incentive`.
- Încetarea definitivă a contractului la inițiativa salariatului este alt eveniment.

## Note de guvernanță

- 30 zile față de angajator sunt calendaristice; 30 și 15 zile față de beneficiu sunt lucrătoare.
- Revenirea nu anulează retroactiv drepturile; schimbarea se transmite autorității.
- Condițiile mai puțin favorabile produc warning și pas de contestare, nu verdict juridic automat.
