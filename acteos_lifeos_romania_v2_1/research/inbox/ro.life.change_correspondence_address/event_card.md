# Event Card — ro.life.change_correspondence_address (life.change_correspondence_address)

**Titlu:** Îmi schimb adresa de corespondență  
**Batch:** B07_CHANGE_CORRESPONDENCE_ADDRESS  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul vrea ca una sau mai multe instituții să trimită comunicările la altă adresă. Evenimentul trebuie să distingă această preferință administrativă de schimbarea domiciliului ori înscrierea reședinței.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `change_scope` | enum | correspondence_only, domicile, residence |
| `target_institution` | enum | dfmt_timisoara, anaf, bank, insurer, health, other |
| `jurisdiction_id` | jurisdiction id | pilot Timișoara |
| `move_date` | date|null | ancoră doar pentru domiciliu/reședință |
| `days_per_month_at_new_address` | integer 0-31|null | prag reședință |
| `has_address_proof` | boolean | poate deveni cerință |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `request_dfmt_personal_data_correction` | corespondență-only + DFMT Timișoara | Atlas; câmp/documente de confirmat | `claim.correspondence.tm_dfmt_channel` |
| `contact_target_institution_for_correspondence_update` | alt destinatar | procedură instituție-specifică | `claim.correspondence.no_universal_channel` |
| `update_identity_card` | scope=domicile | 15 zile | `claim.identity.domicile_new_id_15d` |
| `register_residence` | scope=residence + peste 15 zile/lună | 15 zile | `claim.identity.residence_over_15d` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| DFMT Timișoara | Atlas — Corectarea datelor PF | `verified_with_local_gap` |
| alte instituții | canalul oficial propriu | `needs_confirmation` |
| domiciliu/reședință | SPCLEP competent | `verified_with_local_gap` |

## Note de guvernanță

- Adresa de corespondență nu este echivalată automat cu domiciliul sau reședința.
- Nu există propagare universală: fiecare destinatar se tratează separat.
- Canalul DFMT este confirmat, dar acceptarea câmpului exact și documentele rămân de verificat.
- Doar ramurile domiciliu/reședință activează termenele OUG 97/2005.

===
