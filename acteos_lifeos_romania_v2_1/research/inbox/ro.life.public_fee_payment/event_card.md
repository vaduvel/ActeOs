# Event Card — ro.life.public_fee_payment (life.public_fee_payment)

**Titlu:** Vreau să plătesc o taxă sau un impozit public  
**Batch:** B09_PUBLIC_FEE_PAYMENT  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul dorește să achite o obligație publică identificată, printr-un canal oficial și cu suma/referința verificate.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `authority_id` | string | instituția emitentă |
| `fee_type` | enum/string | tipul obligației |
| `amount_known` | boolean | cuantum verificat |
| `payment_reference_known` | boolean | identificator verificat |
| `institution_enrolled_ghiseul` | boolean | instituție înrolată |
| `prefer_no_authentication` | boolean | canal fără cont |
| `payment_prompt_received_by_message` | boolean | risc phishing |
| `jurisdiction_id` | jurisdiction id | pentru reguli locale |
| `payer_type` | enum | natural_person/legal_person |
| `atlas_account_exists` | boolean | cont local |
| `pays_full_2026_year` | boolean | condiție bonificație |
| `payment_date_on_or_before_2026_03_31` | boolean | limită bonificație |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `identify_public_fee_obligation` | întotdeauna | identifică emitentul și tipul | `claim.payment.generic_amount_deadline_gap` |
| `pay_via_ghiseul_ro` | instituție înrolată și sumă cunoscută | plătește prin canal național | `claim.payment.ghiseul.enrolled_institutions` |
| `check_timisoara_atlas_obligation` | Timișoara | verifică/plătește în Atlas | `claim.tm.payment.atlas_scope` |
| `request_legal_person_atlas_account` | PJ fără cont | creează acces Atlas | `claim.tm.payment.pj_account` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| național | Ghișeul.ro | `verified` |
| Timișoara | DFMT Atlas | `verified_with_local_gap` |
| emitent specific | portal/cont oficial | `needs_confirmation` |

## Note de guvernanță

- Nu se plătește o sumă neverificată.
- Un mesaj cu link nu substituie verificarea în portalul oficial.
- Bonificația 10% este limitată la taxele și condițiile din HCL 719/2025.

===
