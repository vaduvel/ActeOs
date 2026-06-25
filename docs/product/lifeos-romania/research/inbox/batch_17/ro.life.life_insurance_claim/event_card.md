---
event_id: ro.life.life_insurance_claim
title_ro: "Deschiderea unui dosar de daună la asigurarea de viață"
reference_date: 2026-06-25
timezone: Europe/Bucharest
status: research_candidate_not_production_published
jurisdiction:
  - eu
  - ro
  - ro.tm
  - ro.tm.timisoara
---

# Deschiderea unui dosar de daună la asigurarea de viață

## Outcome

Evenimentul este notificat prin canalul oficial, iar solicitantul pregătește formularul și documentele contractuale.

## Scope and truth guard

Nu există un dosar național unic; motorul aplică numai procedura asigurătorului și contractului identificat.

> Acest card este candidat de research. Nicio regulă nu devine activă în producție înainte de captură imutabilă a sursei, review uman și aprobare explicită.

## Facts

| id | type | întrebare | motiv | sensibil | obligatoriu |
|---|---|---|---|---:|---:|
| `insurer_id` | `enum` | La ce asigurător este polița? | Procedura și documentele sunt specifice contractului. | false | true |
| `event_type` | `enum` | Ce eveniment vrei să notifici? | Formularul și actele depind de eveniment. | false | true |
| `claimant_role` | `enum` | În ce calitate depui? | Asiguratul, beneficiarul sau reprezentantul pot avea documente diferite. | false | true |
| `event_date` | `date` | Când s-a produs evenimentul? | Termenul contractual poate curge de la eveniment, externare sau diagnostic. | true | true |
| `discharge_date` | `date` | Când a avut loc externarea? | Pentru fluxul NN de spitalizare termenul publicat se raportează la externare/intervenție. | true | false |
| `policy_number_known` | `boolean` | Ai numărul poliței? | Ajută asigurătorul să identifice contractul. | false | true |
| `beneficiary_known` | `boolean` | Este cunoscut beneficiarul? | În caz de deces, calitatea trebuie dovedită conform contractului. | true | false |
| `iban_available` | `boolean` | Ai IBAN pentru plată? | Unii furnizori îl cer în pregătirea dosarului. | true | false |
| `event_documents_available` | `boolean` | Ai documentele medicale/civile ale evenimentului? | Sunt necesare evaluării. | false | true |

## Gates

| prioritate | id | când | efect | cod | mesaj | claims |
|---:|---|---|---|---|---|---|
| 100 | `gate.provider_unknown` | insurer_id in [other,unknown] | `needs_confirmation` | `POLICY_CONDITIONS_REQUIRED` | Nu există un termen sau dosar universal pentru toate asigurările de viață. | `claim.life_insurance_claim.nn_death_invalidity_soon`, `claim.life_insurance_claim.allianz_death_docs`, `claim.life_insurance_claim.groupama_preparation` |
| 90 | `gate.nn_hospital_window` | insurer_id == nn and event_type in [hospitalization,surgery] and more than 72 hours since discharge/intervention | `needs_confirmation` | `NN_72H_WINDOW_MAY_BE_EXCEEDED` | Termenul operațional publicat de NN poate fi depășit. | `claim.life_insurance_claim.nn_hospital_72h` |
| 80 | `gate.missing_policy` | policy_number_known == false | `warn` | `POLICY_NUMBER_MISSING` | Poți începe contactul, dar identificarea dosarului poate necesita date suplimentare. | `claim.life_insurance_claim.groupama_preparation` |
| 70 | `gate.docs_missing` | event_documents_available == false | `needs_confirmation` | `EVENT_DOCUMENTS_MISSING` | Dosarul nu poate fi evaluat complet fără documentele evenimentului cerute de contract. | `claim.life_insurance_claim.nn_form_and_docs`, `claim.life_insurance_claim.allianz_death_docs`, `claim.life_insurance_claim.groupama_preparation` |

## Steps

### 1. Identifică polița și calitatea ta

- **Ce faci:** Găsește asigurătorul, numărul poliței și calitatea de asigurat/beneficiar/reprezentant.
- **Până când:** `none`
- **Cum știi că e gata:** Asigurătorul și polița sunt identificate sau ai suficiente date pentru căutarea contractului.
- **Dacă eșuează:** Contactează asigurătorul cu datele persoanei asigurate.
- **Canale:** `channel.nn_claim`, `channel.allianz_life_claim`, `channel.groupama_life_claim`
- **Claims:** `claim.life_insurance_claim.groupama_preparation`, `claim.life_insurance_claim.allianz_death_docs`

### 2. Notifică evenimentul

- **Ce faci:** Folosește canalul oficial și formularul aferent evenimentului.
- **Până când:** `none`
- **Cum știi că e gata:** Ai număr de dosar sau confirmarea scrisă a notificării.
- **Dacă eșuează:** Dacă nu primești confirmare, contactează call center-ul oficial.
- **Canale:** `channel.nn_claim`, `channel.allianz_life_claim`, `channel.groupama_life_claim`
- **Claims:** `claim.life_insurance_claim.nn_death_invalidity_soon`, `claim.life_insurance_claim.nn_hospital_72h`, `claim.life_insurance_claim.allianz_death_channels`, `claim.life_insurance_claim.groupama_phone`

### 3. Completează formularul și documentele

- **Ce faci:** Încarcă formularul și documentele medicale/civile cerute pentru evenimentul și contractul concret.
- **Până când:** `none`
- **Cum știi că e gata:** Asigurătorul confirmă primirea și comunică dacă dosarul este complet.
- **Dacă eșuează:** Răspunde solicitărilor suplimentare prin canalul oficial.
- **Canale:** `channel.nn_claim`, `channel.allianz_life_claim`, `channel.groupama_life_claim`
- **Claims:** `claim.life_insurance_claim.nn_form_and_docs`, `claim.life_insurance_claim.allianz_death_docs`, `claim.life_insurance_claim.groupama_preparation`

### 4. Urmărește evaluarea și plata

- **Ce faci:** Verifică statusul, decizia și modalitatea de virare a indemnizației.
- **Până când:** `none`
- **Cum știi că e gata:** Ai decizia oficială și plata sau motivarea refuzului.
- **Dacă eșuează:** Folosește procedura de reclamații/contestații a asigurătorului.
- **Canale:** `channel.nn_claim`, `channel.allianz_life_claim`, `channel.groupama_life_claim`
- **Claims:** `claim.life_insurance_claim.nn_form_and_docs`, `claim.life_insurance_claim.groupama_preparation`

## Requirements

| id | titlu | obligație | timing | forme | verificări | claims |
|---|---|---|---|---|---|---|
| `req.policy_reference` | Polița sau datele contractului | `mandatory` | `now` | original, copy, electronic, declaration | exists, readable, field_present, names_consistent | `claim.life_insurance_claim.groupama_preparation`, `claim.life_insurance_claim.allianz_death_docs` |
| `req.claimant_identity` | Actul de identitate al solicitantului | `mandatory` | `now` | copy, original, electronic | exists, readable, not_expired, names_consistent | `claim.life_insurance_claim.groupama_preparation`, `claim.life_insurance_claim.allianz_death_docs` |
| `req.event_form` | Formularul asigurătorului | `mandatory` | `now` | electronic, original, copy | exists, correct_document_type, field_present, has_signature | `claim.life_insurance_claim.nn_form_and_docs` |
| `req.death_certificate` | Certificatul de deces | `conditional` | `now` | original, copy, certified_copy, electronic | exists, readable, correct_document_type, names_consistent, date_within_window | `claim.life_insurance_claim.allianz_death_docs` |
| `req.medical_documents` | Documente medicale ale evenimentului | `conditional` | `now` | original, copy, electronic | exists, readable, correct_document_type, names_consistent, date_within_window, has_signature, has_stamp | `claim.life_insurance_claim.nn_form_and_docs`, `claim.life_insurance_claim.groupama_preparation` |
| `req.iban` | IBAN pentru indemnizație | `conditional` | `now` | electronic, copy, declaration | exists, readable, names_consistent, user_confirmed | `claim.life_insurance_claim.groupama_preparation` |

## Official channels

| id | tip | etichetă | URL | integrare | teritoriu |
|---|---|---|---|---|---|
| `channel.nn_claim` | `email` | NN — EvenimenteAsigurate@nn.ro | mailto:EvenimenteAsigurate@nn.ro | `DEEP_LINK` | ro |
| `channel.allianz_life_claim` | `phone` | Allianz-Țiriac — 021 201 91 80 | tel:+40212019180 | `DEEP_LINK` | ro |
| `channel.groupama_life_claim` | `phone` | Groupama — 0374 110 110 | tel:+40374110110 | `DEEP_LINK` | ro |

## Source claims

| claim_id | afirmație | sursă | confidence | locator |
|---|---|---|---|---|
| `claim.life_insurance_claim.nn_death_invalidity_soon` | NN indică anunțarea decesului sau invalidității cât mai curând după producerea evenimentului. | `nn_life` | `verified` | Secțiunea «În caz de deces sau invaliditate» |
| `claim.life_insurance_claim.nn_hospital_72h` | NN indică pentru spitalizare/intervenție chirurgicală notificarea în 72 de ore de la externare sau intervenție. | `nn_life` | `verified` | Secțiunea spitalizare/intervenție chirurgicală |
| `claim.life_insurance_claim.nn_form_and_docs` | NN cere formularul corespunzător și documentele menționate în acesta, transmise la EvenimenteAsigurate@nn.ro. | `nn_life` | `verified` | Secțiunile de notificare NN |
| `claim.life_insurance_claim.allianz_death_channels` | Allianz-Țiriac indică notificarea decesului online sau la 021.201.91.80. | `allianz_life` | `verified` | Secțiunea despre notificarea evenimentului |
| `claim.life_insurance_claim.allianz_death_docs` | Pentru Life Plan sunt publicate ca documente de bază certificatul de deces, actele beneficiarilor și polița; termenul exact rămâne în condițiile contractuale. | `allianz_life` | `verified` | Secțiunea documente necesare |
| `claim.life_insurance_claim.groupama_preparation` | Groupama indică pregătirea numărului poliței, IBAN-ului, copiei actului de identitate și documentelor evenimentului înainte de notificare. | `groupama_life` | `verified` | Secțiunea pregătire notificare |
| `claim.life_insurance_claim.groupama_phone` | Groupama publică numărul 0374 110 110 pentru asistență privind daunele de viață. | `groupama_life` | `verified` | Pagina daune asigurări de viață |

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
