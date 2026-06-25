# Scope, release-uri și limite

## 1. Strategia de livrare

Platforma este construită complet ca infrastructură, dar conținutul procedural este activat incremental. Acest lucru nu înseamnă „demo”; înseamnă că produsul refuză să expună trasee neverificate.

### R1 — Verticală de producție: Educație

**Publicabil la lansare:**

1. Înscriere/reînscriere antepreșcolar și preșcolar, bază națională 2026-2027, cu override-uri și surse locale pentru Timiș/Timișoara.
2. Înscriere în clasa pregătitoare, bază națională 2026-2027, cu circumscripții și informații locale Timiș importate și verificate.

**Implementat dar ascuns până la completarea datelor locale:**

3. Admitere la liceu 2026-2027: motor de preferințe, validare coduri și avertizare de listă riscantă. Activarea cere broșura județeană curentă, codurile și locurile verificate.

### R2 — Viață personală

- carte electronică de identitate și situații de schimbare;
- pașaport adult/minor;
- schimbare nume după căsătorie;
- duplicate stare civilă;
- beneficii pentru copil.

### R3 — Proprietate, auto și fiscal

- declarare proprietate și taxe locale;
- certificat fiscal;
- transcriere/înmatriculare/radiere auto;
- schimbare date vehicul/permis;
- autorizații uzuale;
- trasee ANAF strict în limitele serviciilor oficiale disponibile.

## 2. Ce intră în R1 tehnic

- Android nativ, limba română, Android 8+ (`minSdk 26`), `targetSdk` curent stabil la bootstrap.
- Navigare fără cont pentru explorare și traseu local.
- Cont opțional pentru sincronizare, notificări și backup.
- Selectare județ/localitate și data de referință.
- Căutare intenție prin text; vocea este enhancement, nu dependență.
- Chestionar ramificat, rezolvare deterministică, timeline și checklist.
- Dosar personalizat cu cerințe `acum`, `dacă se aplică`, `mai târziu`.
- Import foto/PDF prin Storage Access Framework.
- OCR și verificări formale locale.
- Surse, nivel de încredere, ultima verificare și conflicte vizibile.
- Remindere locale și push opțional.
- Deep-link către canal oficial; fără simularea unei integrări inexistente.
- Feedback „mi s-a cerut altceva” cu dovadă opțională și flux de re-verificare.
- Portal curator complet.
- Worker de surse, snapshot, hash, diff și SLA de review.
- Audit, metrics, logs fără PII și feature flags.

## 3. Ce nu intră în R1

- Depunerea automată în numele utilizatorului în lipsa unei integrări oficiale.
- Plăți procesate de aplicație.
- Autentificare ROeID înainte de acordul și testarea formală cu ADR.
- Predicții de admitere prezentate ca probabilități certe.
- Validarea autenticității documentelor fără registru oficial.
- Marketplace de agenții.
- Chatbot liber care răspunde din internet.
- iOS; arhitectura API rămâne compatibilă cu un client ulterior.

## 4. Gating pentru publicarea unei călătorii

O călătorie poate deveni `production` numai dacă:

- are proprietar de conținut;
- are cel puțin o sursă oficială pentru fiecare cerință critică;
- toate claim-urile sunt legate de span-uri sau fragmente verificabile;
- toate regulile sunt executabile, fără condiții text libere;
- pragul de prospețime nu este depășit;
- conflictele critice sunt rezolvate sau blocante în UI;
- fiecare ramură este acoperită de teste;
- există flow de remediere și contact oficial;
- review-ul este aprobat de două roluri pentru schimbările cu risc mare.
