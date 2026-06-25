# Event Card — ro.life.early_retirement (life.early_retirement)

**Batch:** BATCH_11_PENSIONS_HEALTH_ADMIN  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau să ies anticipat la pensie” sau „vreau să verific dacă pot cere pensie anticipată”.

## Limită de domeniu

Acoperă pensia anticipată din sistemul public potrivit Legii nr. 360/2023: fereastra de maximum 5 ani, stagiul eligibil, diminuarea și momentul plății. Nu modelează pensiile militare, pensiile de serviciu sau toate efectele transfrontaliere.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `standard_retirement_date` | date | data exactă din anexa nr. 5 | da |
| `months_before_standard` | integer | numărul lunilor de anticipare | da / derivat |
| `full_contributory_years_required` | decimal | stagiul complet aferent anexei | da / derivat |
| `qualifying_contributory_years` | decimal | stagiu contributiv după excluderile legale | da |
| `excess_stage_years` | decimal | ani peste stagiul complet pentru tabelul diminuării | da |
| `excluded_period_years` | decimal | contracte voluntare/retroactive sau alte perioade excluse | condiționat |
| `uses_other_age_reduction` | boolean | solicită o altă reducere de vârstă | da |
| `insured_category` | enum | categoria de activitate la data deciziei | condiționat |
| `insured_status_ended` | boolean | încetarea calității pentru începerea plății | condiționat |
| `conditions_met_date` | date | ancoră termen 30 zile | da |
| `application_date` | date | data înregistrării cererii | da |
| `jurisdiction_id` | jurisdiction_id | domiciliul solicitantului | da |

## Traseu determinist

1. **lookup_annex5_retirement_schedule** — stabilește vârsta standard și stagiul complet — `verified`.
2. **recalculate_qualifying_stage_without_excluded_periods** — elimină perioadele care nu deschid dreptul — `verified`.
3. **calculate_monthly_penalty_tier** — alege procentul din tabelul oficial — `verified`.
4. **prepare_early_retirement_application** — pregătește Anexa nr. 4 și dovezile — `verified`.
5. **submit_early_retirement_application** — depune la casa teritorială competentă — `verified_with_local_gap`.

## Canale oficiale

- `ch.cnpp.online_forms` — formularul oficial și serviciile electronice CNPP
- `ch.cjp_timisoara.contact` — CJP Timiș — contact local verificat, depunerea concretă de reconfirmat

## Excluderi și hand-off

- Nu se cumulează automat cu reducerile pentru condiții de muncă, handicap sau copii.
- Nu estimează cuantumul final fără punctajul oficial și numărul exact de luni.
- Cazurile cu stagii în alte state necesită coordonare internațională separată.

## Note de guvernanță

- Diminuarea este pe fiecare lună de anticipare; motorul trebuie să folosească numărul exact de luni, nu ani rotunjiți.
- Perioadele excluse la deschiderea dreptului pot fi valorificate ulterior în condițiile legii; nu sunt șterse din istoricul persoanei.
- Stagiul complet de 35 ani din regulile draft este parametrizat în producție după anexa nr. 5.
