===
event_id: ro.life.weapon_permit
title_ro: Obținerea și administrarea permisului de armă
intent_id: ro.intent.obtain_or_manage_weapon_permit
category_id: hobbies_permits
as_of: 2026-06-25
geography: reguli naționale; canal local verificat pentru IPJ Timiș
publication_status: research_verified_with_explicit_gaps
fixture_count: 22
rule_count: 21
claim_count: 10

## outcome_ro
Identificarea procedurii AESP aplicabile și pregătirea dosarului fără a confunda autorizarea, prelungirea, duplicatul, radierea ori schimbarea domiciliului.

## routing_facts
- `goal`
- `weapon_category_known`
- `purpose_known`
- `permit_not_expired`
- `loss_reason`
- `days_since_transfer`
- `days_since_domicile_change`
- `domicile_county`

## deterministic_branches
| goal / branch | result_ro | confidence |
|---|---|---|
| `first_acquisition` | autorizare procurare la AESP teritorial | verified |
| `extend_permit` | cerere înainte de expirare | verified |
| `replace_document` | duplicat; publicare pentru furt/pierdere/distrugere | verified |
| `category_d_certificate` | certificat de deținător | verified |
| `strike_off_transferred_weapon` | radiere în 10 zile | verified |
| `change_domicile_in_permit` | notificare în 10 zile | verified |

## competent_authorities
| authority | role | territory |
|---|---|---|
| Structura Arme, Explozivi și Substanțe Periculoase competentă teritorial | primire și soluționare | domiciliu/reședință |
| IPJ Timiș — Serviciul AESP | canal pilot local | județul Timiș |

## stop_conditions
- Nu prezenta un checklist unic pentru toate categoriile și scopurile.
- Blochează ruta standard de prelungire dacă permisul este deja expirat.
- Afișează urgent depășirea termenelor de 10 zile.
- Nu extrapola taxele unor servicii la permisul de armă în general.

## source_index
| claim_id | publisher | confidence | official_url |
|---|---|---|---|
| `b18.weapon_permit.first_route` | Poliția Română | verified | https://politiaromana.ro/ro/utile/documente-eliberari-acte/formulare-tipizate-privind-activitatea-directiei-arme-explozivi-si-substante-periculoase |
| `b18.weapon_permit.authorization_90_days` | Poliția Română | verified | https://politiaromana.ro/ro/utile/documente-eliberari-acte/formulare-tipizate-privind-activitatea-directiei-arme-explozivi-si-substante-periculoase |
| `b18.weapon_permit.extension_route` | Poliția Română | verified | https://politiaromana.ro/ro/utile/documente-eliberari-acte/formulare-tipizate-privind-activitatea-directiei-arme-explozivi-si-substante-periculoase |
| `b18.weapon_permit.replacement` | Poliția Română | verified | https://politiaromana.ro/ro/utile/documente-eliberari-acte/formulare-tipizate-privind-activitatea-directiei-arme-explozivi-si-substante-periculoase |
| `b18.weapon_permit.category_d` | Poliția Română | verified | https://politiaromana.ro/ro/utile/documente-eliberari-acte/formulare-tipizate-privind-activitatea-directiei-arme-explozivi-si-substante-periculoase |
| `b18.weapon_permit.strike_off` | Poliția Română | verified | https://politiaromana.ro/ro/utile/documente-eliberari-acte/formulare-tipizate-privind-activitatea-directiei-arme-explozivi-si-substante-periculoase |
| `b18.weapon_permit.domicile_change` | Poliția Română | verified | https://politiaromana.ro/ro/utile/documente-eliberari-acte/formulare-tipizate-privind-activitatea-directiei-arme-explozivi-si-substante-periculoase |
| `b18.weapon_permit.medical` | Poliția Română | verified | https://politiaromana.ro/ro/utile/documente-eliberari-acte/formulare-tipizate-privind-activitatea-directiei-arme-explozivi-si-substante-periculoase |
| `b18.weapon_permit.timis_channel` | Inspectoratul de Poliție Județean Timiș | verified | https://tm.politiaromana.ro/ro/i-p-j-timis/servicii-judetene/serviciul-arme-explozivi-si-substante-periculoase |
| `b18.weapon_permit.checklist_scope_gap` | Poliția Română | needs_confirmation | https://politiaromana.ro/ro/utile/documente-eliberari-acte/formulare-tipizate-privind-activitatea-directiei-arme-explozivi-si-substante-periculoase |
===
