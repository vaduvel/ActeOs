# Event Card — ro.life.register_pet (life.register_pet)

**Titlu:** Vreau să îmi înregistrez animalul de companie  
**Batch:** B09_REGISTER_PET  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul vrea identificarea și înregistrarea animalului; motorul aplică obligația națională verificată pentru câini și nu o extinde automat altor specii.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `species` | enum/string | dog/cat/ferret/exotic/other |
| `dog_has_microchip` | boolean | relevant pentru câine |
| `dog_registered_recs` | boolean | statut RECS |
| `microchip_code_available` | boolean | verificare publică |
| `dog_event` | enum | none/sale/purchase/loss/disappearance/theft/donation/death |
| `dog_event_date` | date\|null | ancora termenului de 7 zile |
| `dog_goes_to_public_space` | boolean | carnet asupra deținătorului |
| `jurisdiction_id` | jurisdiction id | filtru local pentru cabinet |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `identify_pet_registration_regime` | întotdeauna | separă câinele de alte specii | `claim.pet.recs_registry_scope` |
| `microchip_dog` | câine fără microcip | identificare obligatorie | `claim.pet.microchip_followed_by_recs` |
| `register_dog_in_recs` | câine neînregistrat | înregistrare exclusiv prin medic veterinar | `claim.pet.recs_operated_by_vets` |
| `notify_veterinarian_about_dog_event` | eveniment enumerat | notificare în 7 zile | `claim.pet.change_events_7d` |
| `verify_dog_by_microchip_code` | câine microcipat | consultă registrul public | `claim.pet.registry_lookup` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| național | medic veterinar licențiat RECS | `verified` |
| online | RomPetID — verificare după cod microcip | `verified` |
| Timiș | lista cabinetelor filtrată pe județ | `verified_with_local_gap` |

## Note de guvernanță

- Nu există o regulă națională universală modelată pentru orice animal de companie.
- Câinele se înregistrează prin medic veterinar; proprietarul nu operează direct RECS.
- Tariful este al cabinetului veterinar, nu o taxă națională fixă.
- Călătoria, pașaportul și regimul câinilor periculoși sunt proceduri distincte.

===
