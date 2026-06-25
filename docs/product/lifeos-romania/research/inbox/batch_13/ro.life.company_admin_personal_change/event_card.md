# Event Card — ro.life.company_admin_personal_change

**Batch:** B13_COMPANY_ADMIN_PERSONAL_CHANGE  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România; operațiune ONRC națională  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Vreau să schimb numele, actul de identitate sau administratorul firmei.”

## Limita evenimentului

Acoperă mențiunea ONRC pentru modificarea datelor de identificare ale aceluiași administrator și/sau înlocuirea administratorului. Nu tratează schimbarea sediului, cesiunea părților sociale ori autorizările sectoriale independente.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `change_scope` | enum | `same_person_identification_data`, `administrator_replacement`, `both`, `unknown` | separă actualizarea persoanei de numirea unui administrator nou |
| `days_since_modifying_act` | integer | 0+ | testează fereastra generală ONRC de 15 zile |
| `submission_channel` | enum | `counter`, `post_courier`, `electronic` | determină canalul și cerințele de semnare |
| `qualified_signature_available` | boolean | `true`, `false` | ruta electronică cere semnătură calificată |
| `representative_used` | boolean | `true`, `false` | activează dovada împuternicirii |
| `beneficial_owner_affected` | boolean | `true`, `false` | poate declanșa declarația de beneficiar real |
| `documents_ready` | enum | `complete`, `incomplete`, `unknown` | previne depunerea unui dosar respingibil |
| `tariff_note_obtained` | boolean | `true`, `false` | evită inventarea unui tarif dinamic |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| ro.business.onrc.identify_change | mandatory | — | tipul mențiunii stabilit |
| ro.business.onrc.prepare_admin_change | mandatory | ro.business.onrc.identify_change | dosar pregătit |
| ro.business.onrc.file_admin_change | mandatory | ro.business.onrc.prepare_admin_change | mențiune depusă |
| ro.business.onrc.update_beneficial_owner | conditional | ro.business.onrc.identify_change | beneficiar real actualizat, dacă este afectat |

## Canale oficiale

- **ONRC — modificarea datelor de identificare** — https://www.onrc.ro/index.php/ro/mentiuni/persoane-juridice/modificarea-datelor-de-identificare
- **ONRC — schimbarea membrilor organelor de conducere** — https://www.onrc.ro/index.php/ro/mentiuni/persoane-juridice/schimbarea-membrilor-organelor-de-conducere-si-de-control

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este pragul de verificare al draftului, nu o afirmație despre data istorică de intrare în vigoare.
- Nicio sumă, taxă, reducere, penalitate sau listă de documente dinamică nu este calculată fără claim oficial aplicabil și fapt de intrare confirmat.
- Claim-urile `needs_confirmation`, `conflicting` ori `expired` nu pot produce singure un efect critic favorabil utilizatorului.
- Pentru alt UAT decât Timișoara, operaționalizarea locală rămâne `verified_with_local_gap`; regulile naționale sunt păstrate separat.

## Observație de integrare

`change_scope: unknown` nu este ghicit. Interfața trebuie să ceară utilizatorului dacă este aceeași persoană cu date noi sau o persoană nouă.
