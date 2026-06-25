# Event Card — ro.life.change_family_doctor (life.change_family_doctor)

**Batch:** BATCH_11_PENSIONS_HEALTH_ADMIN  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau să îmi schimb medicul de familie”.

## Limită de domeniu

Acoperă regula de 6 luni, excepțiile, cererea de transfer, cardul și transferul fișei medicale. Disponibilitatea medicului nou este confirmare locală.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `months_since_registration` | integer | luni de la înscrierea la medicul actual | da |
| `early_change_reason` | enum | motivul schimbării înainte de 6 luni | da |
| `insurance_status` | enum | insured / uninsured | da |
| `age` | integer | vârsta persoanei | da |
| `card_exception` | boolean | neemis/refuz/duplicat/copil 0–18 | da |
| `new_doctor_in_contract` | boolean | medicul nou este contractat | da |
| `new_doctor_accepts_transfer_confirmed` | boolean | acceptarea transferului este confirmată | da |
| `transfer_request_submitted` | boolean | cererea a fost depusă | da |
| `jurisdiction_id` | jurisdiction_id | localitatea/județul | da |

## Traseu determinist

1. **verify_six_month_rule_or_exception** — verifică termenul ori excepția legală — `verified`.
2. **select_new_contracted_doctor** — alege medicul nou și confirmă acceptarea — `verified_with_local_gap`.
3. **submit_transfer_request_to_new_doctor** — depune cererea și cardul/excepția — `verified`.
4. **monitor_medical_record_transfer** — urmărește notificarea și copia fișei — `verified`.

## Canale oficiale

- `ch.cnas.provider_lists` — lista oficială a furnizorilor contractați
- `ch.cjas_timisoara.contact` — CJAS Timiș — contact local

## Excluderi și hand-off

- Nu solicită utilizatorului să recupereze originalul fișei medicale.
- Nu consideră orice nemulțumire drept excepție înainte de 6 luni.
- Nu garantează acceptarea transferului de către cabinetul nou.

## Note de guvernanță

- Cererea se depune la medicul nou, care gestionează notificarea medicului anterior.
- Termenele pentru notificare și fișă sunt în zile lucrătoare.
- Pentru mutarea domiciliului, excepția citată cere mutarea dintr-o localitate în alta.
