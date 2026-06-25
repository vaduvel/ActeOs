# Event Card — ro.life.contest_fine (life.contest_fine)

**Batch:** BATCH_11_PENSIONS_HEALTH_ADMIN  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau să contest o amendă contravențională”.

## Limită de domeniu

Acoperă plângerea împotriva procesului-verbal contravențional în cadrul general al OG nr. 2/2001: termen, instanță alternativă, suspendare, taxă și probe. Orice act special este verificat înainte de rutare definitivă.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `has_contravention_process_verbal` | boolean | există proces-verbal contravențional | da |
| `communication_date` | date | data înmânării/comunicării | da |
| `days_since_communication` | integer | zile calculate de la ancoră | da / derivat |
| `offense_place` | jurisdiction_id | locul săvârșirii faptei | da |
| `contravenient_domicile_or_seat` | jurisdiction_id | domiciliu/sediu | da |
| `chosen_venue_basis` | enum | offense_place / contravenient_domicile_or_seat | da |
| `special_statute_checked` | boolean | actul special a fost verificat | da |
| `complainant_role` | enum | contravenient / injured_third_party / confiscated_goods_owner | da |
| `complaint_filed` | boolean | plângerea a fost depusă | da |
| `pv_contains_appeal_term_and_court` | boolean | mențiunile căii de atac există | da |

## Traseu determinist

1. **verify_contravention_process_verbal** — confirmă natura actului și comunicarea — `verified`.
2. **verify_special_contravention_statute** — verifică derogările actului special — `verified_with_local_gap`.
3. **choose_competent_district_court** — alege una dintre instanțele alternative — `verified`.
4. **prepare_contravention_complaint** — redactează motivele și adună probele — `verified`.
5. **pay_fee_and_file_complaint** — achită taxa de 20 lei și depune în termen — `verified`.

## Canale oficiale

- `ch.portal.just.ro.courts` — portalul instanțelor pentru identificarea judecătoriei
- `ch.competent_district_court` — registratura instanței competente; canalul concret se verifică

## Excluderi și hand-off

- Nu tratează contestația unei decizii fiscale, a unei decizii de pensie sau a unui act administrativ fără proces-verbal contravențional.
- Nu presupune că orice viciu al procesului-verbal produce automat nulitate.
- Nu ignoră derogările din legislația contravențională specială.

## Note de guvernanță

- Termenul este ancorat la înmânare/comunicare, nu la data înscrisă pe procesul-verbal în orice situație.
- Competența este alternativă între locul faptei și domiciliul/sediul contravenientului.
- Plata amenzii nu este modelată aici ca renunțare automată la plângere.
