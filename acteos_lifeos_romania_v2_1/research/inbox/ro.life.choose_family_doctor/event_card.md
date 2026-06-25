# Event Card — ro.life.choose_family_doctor (life.choose_family_doctor)

**Batch:** BATCH_11_PENSIONS_HEALTH_ADMIN  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau să mă înscriu la un medic de familie” pentru prima înscriere sau după o perioadă fără medic.

## Limită de domeniu

Acoperă alegerea unui medic de familie aflat în contract, cererea și utilizarea cardului ori a excepțiilor. Capacitatea curentă a cabinetului rămâne o confirmare locală.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `insurance_status` | enum | insured / uninsured | da |
| `already_on_gp_list` | boolean | este deja înscris la un medic | da |
| `age` | integer | vârsta solicitantului | da |
| `card_exception` | boolean | neemis/refuz/duplicat/copil 0–18 | da |
| `chosen_doctor_in_contract` | boolean | apare în lista oficială | da |
| `doctor_accepts_new_patients_confirmed` | boolean | capacitate confirmată la cabinet | da |
| `jurisdiction_id` | jurisdiction_id | județul/localitatea | da |

## Traseu determinist

1. **search_official_provider_list** — caută un medic contractat în lista CJAS — `verified`.
2. **confirm_doctor_accepts_new_patients** — confirmă disponibilitatea direct la cabinet — `verified_with_local_gap`.
3. **prepare_registration_request** — pregătește cererea și cardul/excepția — `verified`.
4. **submit_registration_request_to_chosen_doctor** — adresează cererea medicului ales — `verified`.

## Canale oficiale

- `ch.cnas.provider_lists` — listele oficiale ale furnizorilor contractați
- `ch.cjas_timisoara.contact` — CJAS Timiș — contact local verificat

## Excluderi și hand-off

- Nu garantează că un cabinet are locuri disponibile.
- Nu substituie traseul de schimbare dacă persoana este deja înscrisă.
- Nu tratează alegerea unui medic specialist din ambulatoriu.

## Note de guvernanță

- Cererea se adresează medicului ales, nu se depune implicit la CNAS central.
- Atât persoanele asigurate, cât și cele neasigurate pot fi înscrise potrivit normelor citate.
- Statutul contractual și disponibilitatea sunt două verificări diferite.
