# Event Card — ro.life.sold_home (life.sold_home)

**Titlu:** Am vândut o locuință  
**Batch:** B07_SOLD_HOME  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul înstrăinează un imobil. Evenimentul verifică forma autentică, situația asociației, certificatul energetic și scoaterea din evidența fiscală locală.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `transfer_date` | date | data vânzării |
| `is_real_estate` | boolean | imobil |
| `is_condominium` | boolean | unitate în condominiu |
| `association_exists` | boolean | asociație existentă |
| `association_has_president_admin` | boolean | poate elibera adeverința |
| `association_certificate_request_date` | date|null | ancoră 3 zile lucrătoare |
| `association_certificate_issue_date` | date|null | validitate 30 zile |
| `latest_bill_age_months` | integer|null | alternativa fără asociație |
| `debts_exist` | boolean | datorii |
| `buyer_accepts_debts` | boolean | acceptare expresă |
| `energy_certificate_available` | boolean | certificat |
| `seller_was_association_member` | boolean | încetare membru |
| `jurisdiction_id` | jurisdiction id | UAT imobil |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `request_association_sale_certificate` | condominiu cu asociație funcțională | emitere în 3 zile lucrătoare; valabilitate 30 zile | `claim.association.certificate_issue_3wd` |
| `prepare_no_association_declaration_and_bill` | fără asociație/conducere | declarație + factură recentă | `claim.association.no_association_alternative` |
| `hand_over_energy_certificate_original` | vânzare imobil | original către cumpărător | `claim.energy.original_to_buyer` |
| `remove_home_from_local_tax_record` | Timișoara | Atlas; termen de confirmat | `claim.tm.sell_remove_channel` |
| `membership_ends` | fost membru | încetare automată la pierderea proprietății | `claim.association.membership_ends` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| vânzare | notar public | `verified` |
| adeverință asociație | președinte/administrator | `verified` |
| certificat fiscal local | DFMT Atlas/fără cont Atlas | `verified` |
| scoatere evidență | DFMT Atlas | `verified_with_deadline_gap` |

## Note de guvernanță

- Adeverința asociației are două termene distincte: 3 zile lucrătoare pentru emitere și 30 zile calendaristice valabilitate.
- Alternativa fără asociație nu este aplicată când asociația funcționează.
- Datoriile nu sunt ignorate; preluarea trebuie acceptată expres.
- Termenul scoaterii din evidența DFMT nu este inventat.

===
