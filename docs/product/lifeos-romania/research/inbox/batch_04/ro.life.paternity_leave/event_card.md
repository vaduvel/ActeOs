# Event Card — ro.life.paternity_leave (life.paternity_leave)

**Batch:** BATCH_04_CHILD_BIRTH_PARENTAL_BENEFITS  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Sunt tată și vreau concediul paternal după nașterea copilului.”

## Limită de domeniu

Acoperă dreptul legal față de angajator, durata, fereastra de 8 săptămâni, suplimentul de puericultură și protecțiile aferente. Nu confundă concediul paternal cu CCC.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `father_is_worker` | boolean | lucrător/categorie asimilată în sensul Legii 210/1999 | da |
| `child_birth_date` | date | ancoră pentru 8 săptămâni | da |
| `days_since_birth` | integer | calculat la data cererii | condiționat |
| `has_puericulture_certificate` | boolean | adaugă 5 zile lucrătoare | condiționat |
| `has_other_birth_leave_right` | boolean | învoire/permisie distinctă | condiționat |
| `mother_died_during_birth_or_puerperium` | boolean | activează restul concediului mamei | condiționat |
| `worker_category` | enum | `employee`, `public_servant`, `police`, `military`, `director_mandate`, altă categorie legală | condiționat |

## Traseu determinist

1. **verify_worker_status** — confirmă raportul de muncă/serviciu sau categoria asimilată — `verified`.
2. **collect_birth_and_puericulture_proof** — certificat de naștere și, dacă există, atestat — `verified`.
3. **request_paternity_leave** — depune cererea la angajator în primele 8 săptămâni — `verified`.
4. **return_with_preserved_rights** — revine în condiții cel puțin la fel de favorabile — `verified`.

## Canale oficiale

- Nu există pas local în pilot; traseul este național sau derulat prin angajator.

## Excluderi și hand-off

- CCC este un drept separat și are altă eligibilitate.
- Concediul de maternitate rămas după decesul mamei necesită calcul documentat separat.
- Regulamentele interne pot adăuga zile, dar nu reduc dreptul legal.

## Note de guvernanță

- Durata este în zile lucrătoare, nu calendaristice.
- Fereastra de 8 săptămâni se calculează de la data nașterii.
- Angajatorul este canalul operațional; nu există override local Timișoara.
