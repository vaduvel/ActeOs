# Event Card — ro.life.homeowners_association_registration (life.homeowners_association_registration)

**Titlu:** Mă înscriu sau actualizez datele la asociația de proprietari  
**Batch:** B07_HOMEOWNERS_ASSOCIATION_REGISTRATION  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Proprietarul unei unități dintr-un condominiu vrea să adere la o asociație deja existentă sau trebuie să comunice dobândirea proprietății ori schimbarea ocupanților. Înființarea unei asociații noi este exclusă din acest eveniment.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `is_owner` | boolean | membru poate fi proprietarul |
| `is_existing_association` | boolean | gate de scop |
| `previously_member` | boolean | evită aderarea duplicată |
| `wants_membership` | boolean | cerere voluntară |
| `is_new_owner` | boolean | obligație art. 33 alin. 6 |
| `ownership_acquisition_date` | date|null | 10 zile lucrătoare |
| `ownership_lost` | boolean | încetare membru |
| `has_occupancy_change` | boolean | ocupant/chiriaș/comodatar |
| `occupancy_change_date` | date|null | 10 zile calendaristice |
| `association_refuses_application` | boolean | îndrumare locală |
| `jurisdiction_id` | jurisdiction id | pilot Timișoara |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `submit_membership_request` | proprietar + asociație existentă + dorește aderarea | cerere scrisă + act adițional; fără termen legal verificat | `claim.association.later_enrollment` |
| `provide_new_owner_information` | nou proprietar | 10 zile lucrătoare | `claim.association.new_owner_10wd` |
| `notify_occupancy_change` | schimbare ocupanți/chiriași | 10 zile calendaristice | `claim.association.occupants_10d` |
| `membership_ends` | pierdere proprietate | încetare automată | `claim.association.membership_ends` |
| `request_local_association_guidance` | refuz/problemă Timișoara | compartiment local; remediu de confirmat | `claim.association.local_information` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| aderare | președinte/asociație | `verified` |
| formulare Timișoara | portal municipal | `verified_with_scope_gap` |
| îndrumare Timișoara | compartiment asociații de proprietari | `verified` |

## Note de guvernanță

- Chiriașul nu este tratat ca membru al asociației de proprietari.
- Comunicarea noului proprietar în 10 zile lucrătoare este distinctă de aderarea voluntară ca membru.
- Înființarea unei asociații noi este blocată ca eveniment greșit, nu improvizată aici.
- Portalul Timișoara este canal oficial, dar utilizarea lui pentru aderarea individuală rămâne de confirmat.
- Refuzul aderării nu primește automat un remediu juridic inventat.

===
