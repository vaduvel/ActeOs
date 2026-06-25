# Event Card — ro.life.inherited_home (life.inherited_home)

**Titlu:** Am moștenit o locuință  
**Batch:** B07_INHERITED_HOME  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul dobândește sau urmează să dobândească un imobil prin moștenire. Evenimentul separă opțiunea succesorală de finalizarea procedurii, competența notarială, actele, fiscalitatea, evidența locală și relația cu asociația.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `death_date` | date | ancoră pentru legea aplicabilă și termene |
| `deceased_last_domicile_country` | country code | competență |
| `deceased_last_domicile_uat` | jurisdiction id | canal teritorial |
| `deceased_is_romanian` | boolean | transcriere deces străin |
| `death_certificate_issued_abroad` | boolean | certificat străin |
| `requester_has_legitimate_interest` | boolean | calitate pentru cerere |
| `successor_attends_personally` | boolean | procură |
| `has_will` | boolean | testament |
| `succession_completed` | boolean | activează post-procedură |
| `completion_within_2_years` | boolean|null | derivat temporal |
| `ownership_effective_date` | date|null | ancoră de confirmat pentru asociație |
| `includes_real_estate` | boolean | impozit/evidență |
| `is_condominium` | boolean | Legea 196/2018 |
| `jurisdiction_id` | jurisdiction id | UAT imobil |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `confirm_successoral_option_status` | deces înainte/după 01.10.2011 | 6 luni / 1 an; nu termen de finalizare | `claim.inheritance.pre_2011_option_6m` |
| `open_notarial_succession` | ultimul domiciliu în România | notar competent + dosar | `claim.inheritance.last_domicile_competence` |
| `transcribe_foreign_death` | român + certificat străin | eveniment copil | `claim.inheritance.foreign_death_transcription` |
| `pay_succession_transfer_tax_at_notary` | după 2 ani + imobil | 1% potrivit UNNPR; confirmare | `claim.inheritance.tax_after_2y_1pct` |
| `declare_inherited_home_for_local_tax` | imobil Timișoara + succesiune finalizată | Atlas; termen/documente de confirmat | `claim.inheritance.tm_local_tax_channel` |
| `notify_association_after_inheritance` | condominiu | 10 zile lucrătoare; ancoră de confirmat | `claim.association.new_owner_10wd` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| succesiune | birou notarial competent | `verified` |
| pilot Timiș | Camera Notarilor Publici Timișoara | `verified` |
| evidență fiscală Timișoara | DFMT Atlas | `verified_with_local_gap` |
| asociație | președinte/administrator | `verified_with_anchor_gap` |

## Note de guvernanță

- Termenul de opțiune succesorală nu este prezentat ca termen pentru finalizarea întregii proceduri.
- Data exactă de 1 octombrie 2011 rămâne `needs_confirmation`, deoarece formularea paginii oficiale verificate folosește «înainte» și «după».
- Regimul fiscal de 2 ani/1% este păstrat `in_review` până la fixarea articolului consolidat din Codul fiscal.
- Pentru ultim domiciliu în străinătate nu se extrapolează competența națională simplă.
- Termenul fiscal local și ancora asociației pentru moștenire nu sunt ghicite.

===
