# Event Card — ro.life.reinsertion_incentive (life.reinsertion_incentive)

**Batch:** BATCH_04_CHILD_BIRTH_PARENTAL_BENEFITS  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Revin la venituri și vreau stimulentul de inserție.”

## Limită de domeniu

Acoperă stimulentul de inserție din OUG 111/2010, pragurile de vârstă, ne-cumularea cu indemnizația CCC, fereastra de 30 zile lucrătoare și notificarea schimbărilor.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `ccc_entitled` | boolean | persoană îndreptățită la CCC | da |
| `taxable_income_started` | boolean | a început realizarea de venituri eligibile | da |
| `income_start_date` | date|null | ancoră pentru 30 zile lucrătoare | da |
| `child_birth_date` | date | ancoră praguri și durată | da |
| `child_age_months_at_income_start` | integer|null | calculat la începerea veniturilor | condiționat |
| `child_has_disability` | boolean | prag 1 an și durate 3/4 ani | da |
| `ccc_natural_end_reached` | boolean | copilul a ajuns la 2/3 ani | condiționat |
| `ccc_indemnity_currently_paid` | boolean | declanșează suspendarea/ne-cumularea | condiționat |
| `relevant_change_occurred` | boolean | modificare ce afectează plata | condiționat |
| `change_date` | date | ancoră termen 15 zile lucrătoare | condiționat |

## Traseu determinist

1. **classify_incentive_tier** — alege pragul de 1.500 sau 650 lei după vârsta copilului — `verified`.
2. **notify_employer_return** — se coordonează cu evenimentul de revenire la muncă — `verified`.
3. **suspend_ccc_indemnity** — evită cumulul cu indemnizația CCC — `verified`.
4. **apply_insertion_incentive** — depune cererea în 30 zile lucrătoare — `verified_with_local_gap`.
5. **report_incentive_change** — notifică modificările în 15 zile lucrătoare — `verified`.

## Canale oficiale

- `ch.insertion_incentive.timisoara` — flux local de beneficii copil; selecția exactă pentru stimulent trebuie verificată în portal

## Excluderi și hand-off

- Revenirea contractuală la angajator este în `life.return_from_parental_leave`.
- Calculul eligibilității CCC este în `life.parental_leave_benefit`.
- Veniturile neimpozabile sau excepțiile fiscale necesită analiză separată.

## Note de guvernanță

- Denumirea juridică este «stimulent de inserție»; aliasul de produs păstrează `reinsertion_incentive`.
- Pragul exact este strict: înainte de 6/12 luni pentru 1.500 lei; la sau după prag intră ramura 650 lei.
- Nu se permite verdict simultan de plată CCC și stimulent.
