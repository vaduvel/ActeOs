# Event Card — ro.life.child_birth (life.child_birth)

**Batch:** BATCH_04_CHILD_BIRTH_PARENTAL_BENEFITS  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„S-a născut copilul” — eveniment-orchestrator care deschide numai subtraseele aplicabile, fără a dubla procedurile specializate.

## Limită de domeniu

Include trierea imediată după naștere și hand-off-ul către înregistrare, alocație și concedii. Nu înlocuiește asistența medicală, stabilirea filiației în litigiu, transcrierea completă a unui act străin sau procedura de deces.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `birth_country` | country_code | `ro` sau cod ISO țară | da |
| `birth_outcome` | enum | `live_alive`, `stillborn`, `live_died_within_30d` | da |
| `birth_date` | date | data nașterii | da |
| `death_date` | date | cerut numai pentru `live_died_within_30d` | condiționat |
| `birth_registered` | boolean | există act/certificat românesc | condiționat |
| `father_is_worker` | boolean | raport de muncă/serviciu sau categorie asimilată | condiționat |
| `mother_insured_for_maternity` | boolean | eligibilitate OUG 158/2005 | condiționat |
| `wants_parental_leave` | boolean | intenție de CCC/indemnizație | condiționat |
| `children_count` | integer | numărul copiilor din naștere | condiționat |

## Traseu determinist

1. **route_birth_registration** — alege termenul corect după rezultatul nașterii — `verified`.
2. **route_birth_benefits** — deschide alocația numai după înregistrarea copilului viu — `verified`.
3. **route_employment_leaves** — deschide concediile relevante după statutul părinților — `verified`.
4. **route_foreign_birth** — trimite către evenimentul de transcriere/înregistrare consulară — `needs_confirmation`.

## Canale oficiale

- `ch.birth_registration.timisoara` — Serviciul online/ghișeul de înregistrare a nașterii al Primăriei Timișoara; se atașează în subeveniment.

## Excluderi și hand-off

- Nașterea în străinătate este predată către `life.transcribe_foreign_birth`.
- Litigiile de filiație/nume sunt predate instanței sau tutelei, după caz.
- Decesul copilului deschide și evenimentul separat `life.family_death`.

## Note de guvernanță

- Evenimentul nu acordă drepturi; doar construiește graful subevenimentelor.
- Ramurile pentru copil născut mort nu includ alocație sau CCC.
- Eligibilitatea fiecărui beneficiu se reevaluează în subevenimentul propriu.
