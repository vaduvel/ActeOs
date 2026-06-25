---
event_id: ro.life.bank_account_open
title_ro: "Deschiderea unui cont bancar"
reference_date: 2026-06-25
timezone: Europe/Bucharest
status: research_candidate_not_production_published
jurisdiction:
  - eu
  - ro
  - ro.tm
  - ro.tm.timisoara
---

# Deschiderea unui cont bancar

## Outcome

Utilizatorul depune o cerere completă la banca aleasă și primește contul/IBAN-ul ori un refuz.

## Scope and truth guard

Motorul separă obligația legală KYC și contul cu servicii de bază de condițiile comerciale ale fiecărui furnizor.

> Acest card este candidat de research. Nicio regulă nu devine activă în producție înainte de captură imutabilă a sursei, review uman și aprobare explicită.

### Note de domeniu

- Acoperire provider operațională inițială: ING, BT, CEC.
- Datele sunt candidate de research; cer aprobare curator înainte de activare.

## Facts

| id | type | întrebare | motiv | sensibil | obligatoriu |
|---|---|---|---|---:|---:|
| `account_type` | `enum` | Ce fel de cont vrei să deschizi? | Contul cu servicii de bază are o regulă legală distinctă de termen. | false | true |
| `provider_id` | `enum` | La ce bancă vrei contul? | Cerințele comerciale și fluxurile online diferă între furnizori. | false | true |
| `channel_preference` | `enum` | Vrei online sau la unitate? | Cerințele tehnice și documentele pot diferi. | false | true |
| `age` | `integer` | Ce vârstă ai? | Unele fluxuri online oficiale cercetate sunt numai pentru persoane majore. | true | true |
| `citizenship` | `enum` | Ce cetățenie ai? | Eligibilitatea fluxului online poate depinde de cetățenie. | true | true |
| `residence_country` | `string` | În ce țară locuiești? | Unele fluxuri online sunt limitate rezidenților din România. | true | true |
| `valid_identity_document` | `boolean` | Ai un act de identitate valabil? | Identificarea este obligatorie înainte de deschiderea contului. | true | true |
| `can_complete_kyc` | `boolean` | Poți finaliza verificarea identității? | Fără KYC, contul nu poate fi deschis. | true | true |
| `has_camera_device` | `boolean` | Ai telefon sau dispozitiv cu cameră? | Este necesar pentru unele fluxuri online. | false | false |
| `has_internet` | `boolean` | Ai conexiune la internet? | Este necesară pentru fluxul online. | false | false |
| `is_existing_customer` | `boolean` | Ești deja clientul băncii? | Unele fluxuri de onboarding se adresează clienților noi. | false | false |
| `tax_residency_known` | `boolean` | Îți cunoști rezidența fiscală? | Banca poate solicita informații suplimentare în cadrul KYC. | true | false |

## Gates

| prioritate | id | când | efect | cod | mesaj | claims |
|---:|---|---|---|---|---|---|
| 100 | `gate.kyc_possible` | can_complete_kyc == false | `block` | `KYC_UNAVAILABLE` | Contul nu poate fi deschis până când banca nu îți poate verifica identitatea. | `claim.bank_account_open.no_account_without_kyc` |
| 80 | `gate.provider_selected` | provider_id in [other, undecided] | `needs_confirmation` | `PROVIDER_RULES_REQUIRED` | Cerințele exacte trebuie confirmate la banca aleasă; nu există un dosar bancar unic pentru toate băncile. | `claim.bank_account_open.kyc_before_relationship` |
| 70 | `gate.online_eligibility` | channel_preference == online and provider-specific eligibility is not met | `warn` | `ONLINE_FLOW_MAY_BE_UNAVAILABLE` | Fluxul online cercetat poate să nu fie disponibil; verifică deschiderea la unitate. | `claim.bank_account_open.ing_online_eligibility`, `claim.bank_account_open.bt_online_eligibility`, `claim.bank_account_open.cec_online_prerequisites` |

## Steps

### 1. Alege banca și tipul de cont

- **Ce faci:** Compară produsul standard cu contul de plăți cu servicii de bază și selectează banca.
- **Până când:** `none`
- **Cum știi că e gata:** Ai selectat provider_id și account_type.
- **Dacă eșuează:** Dacă nu știi ce tip alegi, marchează «nesigur» și cere explicația diferențelor.
- **Canale:** `channel.ing_account`, `channel.bt_account`, `channel.cec_account`
- **Claims:** `claim.bank_account_open.basic_account_ten_days`, `claim.bank_account_open.ing_online_eligibility`, `claim.bank_account_open.bt_online_eligibility`, `claim.bank_account_open.cec_online_prerequisites`

### 2. Pregătește identificarea

- **Ce faci:** Folosește un act de identitate valabil și completează informațiile cerute pentru cunoașterea clientelei.
- **Până când:** `none`
- **Cum știi că e gata:** Banca a putut verifica identitatea și a confirmat că solicitarea este completă.
- **Dacă eșuează:** Corectează fotografiile sau datele.; Mergi la o unitate dacă verificarea online eșuează.
- **Canale:** `channel.ing_account`, `channel.bt_account`, `channel.cec_account`
- **Claims:** `claim.bank_account_open.kyc_before_relationship`, `claim.bank_account_open.no_account_without_kyc`

### 3. Trimite cererea

- **Ce faci:** Trimite cererea prin canalul oficial al băncii și păstrează confirmarea.
- **Până când:** `none`
- **Cum știi că e gata:** Ai confirmarea că cererea completă a fost primită.
- **Dacă eșuează:** Dacă nu primești confirmare, contactează banca prin canalul oficial.
- **Canale:** `channel.ing_account`, `channel.bt_account`, `channel.cec_account`
- **Claims:** `claim.bank_account_open.basic_account_ten_days`, `claim.bank_account_open.ing_online_eligibility`, `claim.bank_account_open.bt_online_eligibility`, `claim.bank_account_open.cec_online_prerequisites`

### 4. Primește decizia și activează contul

- **Ce faci:** Verifică decizia băncii, contractul, IBAN-ul și modalitatea de activare.
- **Până când:** `none`
- **Cum știi că e gata:** Ai contractul/confirmarea, IBAN-ul și accesul activat sau un refuz motivat.
- **Dacă eșuează:** Pentru contul de bază, urmărește termenul legal de 10 zile lucrătoare de la cererea completă.; Pentru alte produse, confirmă termenul contractual.
- **Canale:** `channel.ing_account`, `channel.bt_account`, `channel.cec_account`
- **Claims:** `claim.bank_account_open.basic_account_ten_days`

## Requirements

| id | titlu | obligație | timing | forme | verificări | claims |
|---|---|---|---|---|---|---|
| `req.valid_identity` | Act de identitate valabil | `mandatory` | `now` | original, electronic | exists, readable, correct_document_type, not_expired, names_consistent | `claim.bank_account_open.kyc_before_relationship`, `claim.bank_account_open.no_account_without_kyc` |
| `req.kyc_information` | Informațiile KYC solicitate de bancă | `mandatory` | `now` | electronic, declaration | exists, field_present, user_confirmed | `claim.bank_account_open.kyc_before_relationship` |
| `req.camera_device` | Dispozitiv cu cameră | `conditional` | `now` | electronic | user_confirmed | `claim.bank_account_open.cec_online_prerequisites`, `claim.bank_account_open.ing_online_eligibility` |
| `req.internet_connection` | Conexiune la internet | `conditional` | `now` | electronic | user_confirmed | `claim.bank_account_open.cec_online_prerequisites` |

## Official channels

| id | tip | etichetă | URL | integrare | teritoriu |
|---|---|---|---|---|---|
| `channel.ing_account` | `web` | ING — deschidere cont | https://ing.ro/persoane-fizice/carduri-si-conturi/pachete-conturi-curente | `DEEP_LINK` | ro |
| `channel.bt_account` | `web` | Banca Transilvania — cont online | https://www.bancatransilvania.ro/cont-online | `DEEP_LINK` | ro |
| `channel.cec_account` | `web` | CEC Bank — cont online | https://www.cec.ro/BunVenit/cont-bancar-online | `DEEP_LINK` | ro |

## Source claims

| claim_id | afirmație | sursă | confidence | locator |
|---|---|---|---|---|
| `claim.bank_account_open.kyc_before_relationship` | Banca trebuie să verifice identitatea clientului înaintea stabilirii relației de afaceri. | `law_129_2019` | `verified` | Art. 11 alin. (8); forma consolidată accesată la 25.06.2026 |
| `claim.bank_account_open.no_account_without_kyc` | Dacă măsurile de cunoaștere a clientelei nu pot fi aplicate, entitatea nu trebuie să deschidă contul. | `law_129_2019` | `verified` | Art. 11 alin. (9); forma consolidată accesată la 25.06.2026 |
| `claim.bank_account_open.basic_account_ten_days` | Pentru contul de plăți cu servicii de bază, deschiderea sau refuzul se face în cel mult 10 zile lucrătoare după cererea completă. | `law_258_2017` | `verified` | Art. 43; după primirea unei cereri complete |
| `claim.bank_account_open.ing_online_eligibility` | Deschiderea online la ING este prezentată pentru cetățean român, rezident în România, peste 18 ani, cu act valabil. | `ing_account` | `verified` | Secțiunea «Cum îți faci cont?» / «Cum pot să devin client ING?» |
| `claim.bank_account_open.bt_online_eligibility` | Fluxul online BT Pay este prezentat pentru persoane majore, cu act românesc valabil și care nu sunt deja clienți eligibili pe acel flux. | `bt_account` | `verified` | Secțiunea de eligibilitate pentru deschiderea contului online |
| `claim.bank_account_open.cec_online_prerequisites` | Fluxul online CEC necesită act de identitate, dispozitiv cu cameră și conexiune la internet. | `cec_account` | `verified_with_local_gap` | Secțiunea «De ce ai nevoie» pentru contul online |

## Freshness

critical:
  review_due_at: '2026-07-25'
  hard_expiry_at: '2026-09-23'
  on_expiry: needs_confirmation
operational:
  review_due_at: '2026-08-24'
  hard_expiry_at: '2026-12-22'
  on_expiry: warn
normative:
  review_due_at: '2026-12-22'
  hard_expiry_at: '2027-06-25'
  on_expiry: needs_confirmation
