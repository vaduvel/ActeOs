---
event_id: ro.life.home_insurance_claim
title_ro: "Deschiderea unui dosar de daună pentru locuință"
reference_date: 2026-06-25
timezone: Europe/Bucharest
status: research_candidate_not_production_published
jurisdiction:
  - eu
  - ro
  - ro.tm
  - ro.tm.timisoara
---

# Deschiderea unui dosar de daună pentru locuință

## Outcome

Utilizatorul avizează corect dauna, obține documentele necesare, participă la constatare și urmărește despăgubirea.

## Scope and truth guard

Motorul separă PAD de polițele facultative și aplică termenele contractuale numai furnizorului confirmat.

> Acest card este candidat de research. Nicio regulă nu devine activă în producție înainte de captură imutabilă a sursei, review uman și aprobare explicită.

## Facts

| id | type | întrebare | motiv | sensibil | obligatoriu |
|---|---|---|---|---:|---:|
| `policy_kind` | `enum` | Ce poliță vrei să folosești? | PAD și polița facultativă au reguli diferite. | false | true |
| `insurer_id` | `enum` | Cine este asigurătorul? | Termenele și documentele facultative sunt contractuale. | false | true |
| `peril` | `enum` | Ce a produs paguba? | Riscul selectează autoritățile și termenul aplicabil. | false | true |
| `event_date` | `date` | Când s-a produs evenimentul? | Este necesar pentru calculul termenului. | true | true |
| `property_jurisdiction` | `jurisdiction_ref` | Unde se află locuința? | Canalele ISU/primărie sunt locale. | true | true |
| `danger_ongoing` | `boolean` | Mai există un pericol imediat? | Siguranța și limitarea pagubelor preced dosarul. | false | true |
| `authorities_notified` | `boolean` | Ai anunțat autoritățile competente? | Pentru unele riscuri documentul autorității este necesar. | false | true |
| `repairs_started` | `boolean` | Ai început reparațiile? | PAD cere constatarea înaintea reparațiilor. | false | true |
| `policy_valid_on_event_date` | `boolean` | Polița era valabilă la data evenimentului? | Acoperirea trebuie verificată contractual. | false | true |
| `ownership_documents_available` | `boolean` | Ai actele de proprietate? | Sunt cerute în dosarul PAD. | false | true |

## Gates

| prioritate | id | când | efect | cod | mesaj | claims |
|---:|---|---|---|---|---|---|
| 100 | `gate.immediate_safety` | danger_ongoing == true | `warn` | `ENSURE_SAFETY_FIRST` | Pune persoanele în siguranță și contactează serviciile de urgență înaintea dosarului. | `claim.home_insurance_claim.pad_notify_60_days` |
| 95 | `gate.pad_deadline` | policy_kind in [pad,both] and event is more than 60 days old | `needs_confirmation` | `PAD_60_DAY_WINDOW_EXCEEDED` | Termenul publicat de avizare PAD de 60 de zile poate fi depășit. | `claim.home_insurance_claim.pad_notify_60_days` |
| 90 | `gate.pad_authority_doc` | policy_kind in [pad,both] and peril in [natural_flood,landslide] and authorities_notified == false | `warn` | `NOTIFY_LOCAL_AUTHORITIES` | Pentru această daună PAD, anunță ISU/primăria și cere proces-verbal. | `claim.home_insurance_claim.pad_authorities_natural_flood_landslide` |
| 85 | `gate.repairs` | policy_kind in [pad,both] and repairs_started == true | `warn` | `REPAIRS_BEFORE_INSPECTION` | PAD publică regula că reparațiile se încep după constatare. | `claim.home_insurance_claim.pad_no_repairs_before_inspection` |
| 70 | `gate.unknown_insurer` | policy_kind in [facultative,both] and insurer_id in [other,unknown] | `needs_confirmation` | `CONTRACT_RULES_REQUIRED` | Termenul și actele poliței facultative trebuie confirmate din contract și pagina asigurătorului. | `claim.home_insurance_claim.allianz_notice_window`, `claim.home_insurance_claim.groupama_notice_48h` |

## Steps

### 1. Protejează persoanele și limitează paguba

- **Ce faci:** Ia măsuri rezonabile de siguranță fără a începe reparații definitive înaintea constatării, unde polița cere asta.
- **Până când:** `none`
- **Cum știi că e gata:** Pericolul este oprit/gestionat și ai documentat starea inițială.
- **Dacă eșuează:** Apelează serviciile de urgență pentru risc imediat.
- **Canale:** `channel.isu_timis`, `channel.primaria_tm_emergency`
- **Claims:** `claim.home_insurance_claim.pad_authorities_natural_flood_landslide`, `claim.home_insurance_claim.pad_no_repairs_before_inspection`

### 2. Anunță autoritățile și cere documentul evenimentului

- **Ce faci:** Pentru inundație naturală sau alunecare PAD, contactează ISU/primăria și solicită proces-verbal.
- **Până când:** `none`
- **Cum știi că e gata:** Ai număr de înregistrare/proces-verbal sau dovada solicitării.
- **Dacă eșuează:** Dacă nu știi autoritatea, folosește contactele locale oficiale.
- **Canale:** `channel.isu_timis`, `channel.primaria_tm_emergency`
- **Claims:** `claim.home_insurance_claim.pad_authorities_natural_flood_landslide`, `claim.home_insurance_claim.isu_timis_contact`, `claim.home_insurance_claim.timisoara_emergency_contact`

### 3. Avizează dauna la asigurător

- **Ce faci:** Folosește canalul oficial și comunică polița, data, riscul și pagubele.
- **Până când:** `none`
- **Cum știi că e gata:** Ai număr de dosar/confirmare de avizare.
- **Dacă eșuează:** Dacă portalul nu funcționează, folosește telefonul sau canalul alternativ oficial.
- **Canale:** `channel.pad_claim`, `channel.allianz_claim`, `channel.groupama_claim`
- **Claims:** `claim.home_insurance_claim.pad_notify_60_days`, `claim.home_insurance_claim.allianz_notice_window`, `claim.home_insurance_claim.groupama_notice_48h`

### 4. Pregătește dosarul de daună

- **Ce faci:** Adună actul de identitate, polița, actele de proprietate și documentele autorităților/daunei.
- **Până când:** `none`
- **Cum știi că e gata:** Asigurătorul confirmă că dosarul este complet sau comunică exact ce lipsește.
- **Dacă eșuează:** Încarcă numai documentele cerute pentru polița concretă.; Păstrează originalele.
- **Canale:** `channel.pad_claim`, `channel.allianz_claim`, `channel.groupama_claim`
- **Claims:** `claim.home_insurance_claim.pad_notification_docs`, `claim.home_insurance_claim.pad_core_file_docs`, `claim.home_insurance_claim.groupama_notice_48h`

### 5. Participă la constatare

- **Ce faci:** Permite inspectorului să constate avariile înaintea reparațiilor definitive.
- **Până când:** `none`
- **Cum știi că e gata:** Raportul de constatare este semnat/primit.
- **Dacă eșuează:** Dacă nu ești contactat, urmărește dosarul la asigurător.
- **Canale:** `channel.pad_claim`, `channel.allianz_claim`, `channel.groupama_claim`
- **Claims:** `claim.home_insurance_claim.pad_inspection_five_days`, `claim.home_insurance_claim.pad_no_repairs_before_inspection`

### 6. Urmărește finalizarea și plata

- **Ce faci:** Verifică dacă dosarul a fost declarat complet și urmărește decizia/plata.
- **Până când:** `none`
- **Cum știi că e gata:** Ai decizia de despăgubire și dovada plății sau motivarea refuzului.
- **Dacă eșuează:** Folosește procedura oficială de reclamații a asigurătorului.
- **Canale:** `channel.pad_claim`, `channel.allianz_claim`, `channel.groupama_claim`
- **Claims:** `claim.home_insurance_claim.pad_payment_after_complete_file`

## Requirements

| id | titlu | obligație | timing | forme | verificări | claims |
|---|---|---|---|---|---|---|
| `req.policy` | Polița de asigurare | `mandatory` | `now` | original, copy, electronic | exists, readable, correct_document_type, date_within_window | `claim.home_insurance_claim.pad_notification_docs` |
| `req.identity` | Actul de identitate | `mandatory` | `now` | copy, original, electronic | exists, readable, not_expired, names_consistent | `claim.home_insurance_claim.pad_notification_docs`, `claim.home_insurance_claim.pad_core_file_docs` |
| `req.property_title` | Acte privind dreptul asupra locuinței | `mandatory` | `now` | copy, original, certified_copy | exists, readable, names_consistent, address_consistent | `claim.home_insurance_claim.pad_core_file_docs` |
| `req.authority_report` | Proces-verbal/document al autorității | `conditional` | `now` | original, copy, electronic | exists, readable, correct_document_type, date_within_window, address_consistent | `claim.home_insurance_claim.pad_authorities_natural_flood_landslide`, `claim.home_insurance_claim.pad_core_file_docs`, `claim.home_insurance_claim.allianz_notice_window` |
| `req.damage_evidence` | Dovezi ale pagubelor | `mandatory` | `now` | electronic, copy | exists, readable, date_within_window, user_confirmed | `claim.home_insurance_claim.pad_core_file_docs`, `claim.home_insurance_claim.groupama_notice_48h` |

## Official channels

| id | tip | etichetă | URL | integrare | teritoriu |
|---|---|---|---|---|---|
| `channel.pad_claim` | `web` | PAD — anunță dauna | https://www.padrom.ro/daune-pad/ | `DEEP_LINK` | ro |
| `channel.allianz_claim` | `web` | Allianz-Țiriac — notifică o daună | https://www.allianztiriac.ro/ro_RO/persoane-fizice/asigurari-persoane-fizice-locuinta-si-bunuri/my-home.html | `DEEP_LINK` | ro |
| `channel.groupama_claim` | `web` | Groupama — daune proprietăți | https://www.groupama.ro/daune/daune-proprietati | `DEEP_LINK` | ro |
| `channel.isu_timis` | `physical` | ISU Timiș — Str. Înfrățirii nr. 13, Timișoara | https://isutm.igsu.ro/ | `SOURCE_ONLY` | ro, ro.tm |
| `channel.primaria_tm_emergency` | `phone` | Primăria Timișoara — situații de urgență, 0256 969 | tel:+40256969 | `DEEP_LINK` | ro, ro.tm, ro.tm.timisoara |

## Source claims

| claim_id | afirmație | sursă | confidence | locator |
|---|---|---|---|---|
| `claim.home_insurance_claim.pad_notify_60_days` | Dauna PAD trebuie avizată cât mai repede, dar nu mai târziu de 60 de zile de la eveniment. | `pad_daune` | `verified` | Secțiunile cutremur și inundație/alunecare |
| `claim.home_insurance_claim.pad_authorities_natural_flood_landslide` | Pentru inundație naturală sau alunecare de teren, PAD indică anunțarea ISU/primăriei și solicitarea unui proces-verbal. | `pad_daune` | `verified` | Pașii 3–4 pentru inundație/alunecare |
| `claim.home_insurance_claim.pad_notification_docs` | Pentru avizare, asiguratul trebuie să aibă polița PAD valabilă și actul de identitate. | `pad_daune` | `verified` | Secțiunea «Ce trebuie să conțină o avizare?» |
| `claim.home_insurance_claim.pad_inspection_five_days` | După înștiințarea scrisă, reprezentantul asigurătorului vine pentru constatare în maximum 5 zile. | `pad_daune` | `verified` | Secțiunea «Cum se efectuează constatarea?» |
| `claim.home_insurance_claim.pad_core_file_docs` | Dosarul PAD include documente de la autorități, copie act de identitate și copie acte de proprietate. | `pad_daune` | `verified` | Secțiunea «Ce acte sunt necesare»; actele de proprietate sunt enumerate separat |
| `claim.home_insurance_claim.pad_no_repairs_before_inspection` | Lucrările de reparație trebuie începute numai după constatarea avariilor de către reprezentantul asigurătorului. | `pad_daune` | `verified` | Atenționarea de la finalul listei de acte |
| `claim.home_insurance_claim.pad_payment_after_complete_file` | PAID indică plata în maximum 5 zile după primirea dosarului finalizat de la asigurător. | `pad_info` | `verified` | Secțiunea despre plata după deschiderea dosarului |
| `claim.home_insurance_claim.allianz_notice_window` | Pentru My Home, Allianz-Țiriac indică notificarea scrisă în 5 zile lucrătoare, respectiv 24 de ore pentru furt. | `allianz_home` | `verified` | Secțiunea obligații după producerea riscului |
| `claim.home_insurance_claim.groupama_notice_48h` | Groupama indică notificarea daunei de proprietate în 48 de ore și publică o listă minimă de documente. | `groupama_home` | `verified` | Secțiunea de avizare daune proprietăți |
| `claim.home_insurance_claim.isu_timis_contact` | ISU Timiș publică datele oficiale de contact pentru județul Timiș. | `isu_timis` | `verified` | Pagina oficială de contact |
| `claim.home_insurance_claim.timisoara_emergency_contact` | Primăria Timișoara publică pagina și contactele Comitetului Local pentru Situații de Urgență. | `primaria_tm_emergency` | `verified` | Pagina «Situații de urgență» |

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
