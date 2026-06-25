# Event Card — ro.life.vat_registration

**Batch:** B13_VAT_REGISTRATION  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România; administrare fiscală centrală ANAF  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Vreau să înregistrez firma în scopuri de TVA” / „Am depășit plafonul și trebuie să mă înregistrez.”

## Limita evenimentului

Acoperă alegerea controlată a rutei de actualizare a vectorului fiscal și folosirea formularului 700. Nu calculează plafonul legal și nu decide singur eligibilitatea pentru regimuri speciale.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `already_vat_registered` | boolean | `true`, `false` | separă înregistrarea nouă de modificarea statutului existent |
| `registration_reason` | enum | `threshold_confirmed_exceeded`, `voluntary_confirmed`, `special_intra_eu`, `not_applicable`, `unknown` | alege temeiul fără a ghici plafonul |
| `fiscal_vector_update_needed` | boolean | `true`, `false` | determină ruta formularului 700 |
| `form700_access_available` | boolean | `true`, `false` | previne folosirea unei versiuni vechi |
| `electronic_submission_ready` | boolean | `true`, `false` | formularul 700 este o rută electronică |
| `effective_date_confirmed` | boolean | `true`, `false` | data efectivă schimbă completarea și obligațiile ulterioare |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| ro.tax.vat.confirm_basis | mandatory | — | temeiul și data efectivă confirmate |
| ro.tax.vat.prepare_form700 | conditional | ro.tax.vat.confirm_basis | formularul curent pregătit |
| ro.tax.vat.file_electronically | conditional | ro.tax.vat.prepare_form700 | vector fiscal actualizat |
| ro.tax.vat.special_route | conditional | ro.tax.vat.confirm_basis | regimul special separat corect |

## Canale oficiale

- **ANAF — formular 700** — https://static.anaf.ro/static/10/Anaf/Declaratii_R/700.html
- **ANAF — formular 301** — https://static.anaf.ro/static/10/Anaf/Declaratii_R/301.html

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este pragul de verificare al draftului, nu o afirmație despre data istorică de intrare în vigoare.
- Nicio sumă, taxă, reducere, penalitate sau listă de documente dinamică nu este calculată fără claim oficial aplicabil și fapt de intrare confirmat.
- Claim-urile `needs_confirmation`, `conflicting` ori `expired` nu pot produce singure un efect critic favorabil utilizatorului.
- Pentru alt UAT decât Timișoara, operaționalizarea locală rămâne `verified_with_local_gap`; regulile naționale sunt păstrate separat.

## Observație de integrare

Interfața nu afișează un plafon numeric din memorie. Utilizatorul trebuie să confirme temeiul cu date fiscale curente sau cu un profesionist înainte de efectul critic.
