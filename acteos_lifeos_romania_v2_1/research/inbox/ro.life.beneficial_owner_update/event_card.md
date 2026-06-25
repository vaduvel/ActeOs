# Event Card — ro.life.beneficial_owner_update

**Batch:** B13_BENEFICIAL_OWNER_UPDATE  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România; Registrul beneficiarilor reali  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Vreau să actualizez beneficiarul real al firmei” / „Trebuie să depun anual declarația de beneficiar real?”

## Limita evenimentului

Acoperă declarația determinată de o schimbare și obligația anuală specială pentru structurile de acționariat indicate de art. 56 alin. (1^3). Nu tratează registrul fiduciilor sau beneficiarii reali ai asociațiilor/fundațiilor.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `beneficial_owner_changed` | boolean | `true`, `false` | activează declarația la modificare |
| `days_since_change` | integer | 0+ | testează termenul de 15 zile |
| `high_risk_shareholding_chain` | boolean | `true`, `false` | separă obligația anuală specială de regula generală |
| `annual_statements_approved` | boolean | `true`, `false` | fixează triggerul termenului anual special |
| `days_since_annual_approval` | integer | 0+ | testează cele 15 zile de la aprobare |
| `identification_and_control_data_complete` | boolean | `true`, `false` | asigură câmpurile legale ale declarației |
| `submission_channel` | enum | `electronic`, `counter`, `post_courier` | selectează canalul oficial |
| `qualified_signature_available` | boolean | `true`, `false` | verifică pregătirea rutei electronice |
| `representative_used` | boolean | `true`, `false` | activează cerința privind reprezentarea |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| ro.business.bo.assess_trigger | mandatory | — | triggerul legal identificat |
| ro.business.bo.prepare_declaration | conditional | ro.business.bo.assess_trigger | declarație completă |
| ro.business.bo.file_declaration | conditional | ro.business.bo.prepare_declaration | actualizare în RBR |

## Canale oficiale

- **Portal Legislativ — Legea nr. 129/2019** — https://legislatie.just.ro/Public/DetaliiDocument/216157
- **ONRC — beneficiari reali** — https://www.onrc.ro/index.php/ro/inmatriculari/persoane-juridice/nume-colectiv?id=944

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este pragul de verificare al draftului, nu o afirmație despre data istorică de intrare în vigoare.
- Nicio sumă, taxă, reducere, penalitate sau listă de documente dinamică nu este calculată fără claim oficial aplicabil și fapt de intrare confirmat.
- Claim-urile `needs_confirmation`, `conflicting` ori `expired` nu pot produce singure un efect critic favorabil utilizatorului.
- Pentru alt UAT decât Timișoara, operaționalizarea locală rămâne `verified_with_local_gap`; regulile naționale sunt păstrate separat.

## Observație de integrare

Aplicația nu întreabă simplist «ai firmă?». Mai întâi separă schimbarea efectivă de obligația anuală specială și nu inventează o obligație anuală generală.
