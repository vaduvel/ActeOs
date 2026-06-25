# Event Card — ro.life.parental_leave_benefit (life.parental_leave_benefit)

**Batch:** BATCH_04_CHILD_BIRTH_PARENTAL_BENEFITS  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau concediu și indemnizație pentru creșterea copilului (CCC).”

## Limită de domeniu

Acoperă eligibilitatea OUG 111/2010, durata, formula, dosarul, termenele față de autoritate și notificarea angajatorului. Nu calculează veniturile fiscale fără documente și nu decide autenticitatea acestora.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `eligible_months_in_last_24` | integer | 0–24, incluzând perioade asimilate confirmate | da |
| `child_birth_date` | date | ancoră durată și depunere | da |
| `child_has_disability` | boolean | durată până la 3 ani | da |
| `children_count_in_birth` | integer | 1+ pentru supliment naștere multiplă | condiționat |
| `both_parents_eligible` | boolean | activează cele 2 luni rezervate | condiționat |
| `had_maternity_leave` | boolean | alege ancora termenului de 60 zile lucrătoare | condiționat |
| `maternity_leave_end_date` | date | obligatorie dacă a existat maternitate | condiționat |
| `is_employee` | boolean | controlează traseul angajatorului | condiționat |
| `planned_parental_leave_start` | date | ancoră notificare 10 zile | condiționat |
| `has_assimilated_periods` | boolean | perioade asimilate de verificat | condiționat |

## Traseu determinist

1. **verify_eligibility_periods** — numără veniturile și perioadele asimilate — `verified`.
2. **calculate_formula_inputs** — pregătește baza pentru 85%, minim și plafon — `verified`.
3. **notify_employer_parental_leave** — notifică angajatorul cu minimum 10 zile înainte — `verified`.
4. **prepare_parental_leave_application** — adună actele art. 13 — `verified`.
5. **submit_parental_leave_benefit** — depune prin primăria de domiciliu/reședință — `verified_with_local_gap`.
6. **plan_other_parent_two_months** — rezervă perioada celuilalt părinte dacă ambii sunt eligibili — `verified`.

## Canale oficiale

- `ch.parental_benefit.timisoara_online` — portalul Primăriei Timișoara pentru cerere și documente; matricea exactă este dinamică

## Excluderi și hand-off

- Concediul de maternitate este tratat în `life.maternity_leave`.
- Stimulentul de inserție este tratat în `life.reinsertion_incentive`.
- Revenirea efectivă la angajator este tratată în `life.return_from_parental_leave`.

## Note de guvernanță

- Motorul nu deduce luni eligibile din text liber; cere valori și documente cu proveniență.
- Minimul legat de ISR se calculează numai cu valoarea oficială valabilă la data dreptului.
- Regula celor 2 luni se aplică numai dacă ambii părinți îndeplinesc condițiile.
