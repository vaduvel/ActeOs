# Event Card — ro.life.bought_home (life.bought_home)

**Titlu:** Am cumpărat o locuință  
**Batch:** B07_BOUGHT_HOME  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul dobândește prin vânzare un teren, o casă sau o unitate de clădire. Evenimentul acoperă actul autentic, certificatul energetic, asociația, evidența fiscală locală și mutarea efectivă.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `transfer_date` | date | data transferului dreptului |
| `is_real_estate` | boolean | teren/construcție/unitate |
| `is_condominium` | boolean | aplică Legea 196/2018 |
| `received_energy_certificate_original` | boolean | original primit la vânzare |
| `seller_debts_exist` | boolean | datorii asociație/utilități |
| `buyer_expressly_accepts_debts` | boolean | acceptare în act |
| `jurisdiction_id` | jurisdiction id | UAT-ul imobilului |
| `moves_in` | boolean | mutare efectivă |
| `changes_domicile` | boolean | locuință principală |
| `move_date` | date|null | ancoră identitate |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `complete_authentic_notarial_transfer` | imobil | act autentic | `claim.notary.immovable_authentic` |
| `obtain_energy_certificate_original` | original lipsă | predare de la vânzător | `claim.energy.original_to_buyer` |
| `notify_association_as_new_owner` | condominiu | 10 zile lucrătoare | `claim.association.new_owner_10wd` |
| `declare_home_for_local_tax` | imobil în Timișoara | Atlas; termen de confirmat | `claim.tm.buy_declare_channel` |
| `update_identity_for_new_domicile` | se mută și schimbă domiciliul | 15 zile | `claim.identity.domicile_new_id_15d` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| transfer | notar public | `verified` |
| impozit local Timișoara | DFMT Atlas | `verified_with_deadline_gap` |
| asociație | președinte/administrator | `verified` |
| identitate | SPCLEP competent | `verified_with_local_gap` |

## Note de guvernanță

- Termenul fiscal local nu este ghicit din practici ale altor UAT-uri.
- Apartenența la asociație și simpla obligație de comunicare a noului proprietar sunt două lucruri distincte.
- Preluarea datoriilor trebuie să fie expresă; motorul nu o presupune.
- Cumpărarea fără mutare nu declanșează schimbarea domiciliului.

===
