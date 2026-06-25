# Event Card — ro.life.birth_registration (life.birth_registration)

**Batch:** BATCH_04_CHILD_BIRTH_PARENTAL_BENEFITS  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau să înregistrez nașterea și să obțin certificatul de naștere românesc.”

## Limită de domeniu

Acoperă nașterile produse în România, inclusiv termenele speciale și înregistrarea tardivă. Nașterile produse în străinătate sunt în afara acestui eveniment și se predau către transcriere/înregistrare consulară.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `registration_case` | enum | `live_alive`, `stillborn`, `live_died_within_30d`, `found_child`, `abandoned_in_maternity` | da |
| `birth_date` | date | data nașterii | da |
| `death_date` | date | obligatorie la `live_died_within_30d` | condiționat |
| `finding_or_abandonment_date` | date | obligatorie pentru caz special | condiționat |
| `days_since_birth` | integer | calculat din date | condiționat |
| `parents_marital_status` | enum | `married`, `unmarried`, `unknown` | condiționat |
| `parents_have_different_surnames` | boolean | controlează declarația de nume | condiționat |
| `father_recognises_at_registration` | boolean | recunoaștere paternitate la înregistrare | condiționat |
| `request_date` | date | ancoră pentru termenul autorității la tardiv | condiționat |

## Traseu determinist

1. **determine_deadline** — alege termenul legal după tipul cazului — `verified`.
2. **collect_core_documents** — certificat medical și acte de identitate — `verified`.
3. **resolve_name_and_filiation** — include declarațiile condiționate de stare civilă — `verified`.
4. **declare_birth** — depune declarația prin autoritatea de stare civilă — `verified`.
5. **collect_certificate** — ridică certificatul după întocmirea actului — `verified_with_local_gap`.
6. **late_registration** — aplică aprobările și termenele suplimentare dacă este tardiv — `verified`.

## Canale oficiale

- `ch.birth_registration.timisoara` — serviciul oficial al Primăriei Timișoara pentru înregistrarea nașterii
- `ch.birth_certificate_pickup.timisoara` — ridicare fără programare, de către unul dintre părinți, conform paginii locale

## Excluderi și hand-off

- Actul străin se procesează în `life.transcribe_foreign_birth`.
- Neînțelegerile asupra numelui copilului pot necesita instanța de tutelă.
- Expertiza medico-legală pentru lipsa certificatului medical este un traseu special.

## Note de guvernanță

- Nu se afișează o taxă: absența unei taxe nu a fost confirmată printr-un claim oficial explicit.
- Termenele de 30 zile, 3 zile și 24 ore sunt mutual exclusive după `registration_case`.
- Documentele străine și traducerile se adaugă numai prin reguli confirmate pentru cazul concret.
