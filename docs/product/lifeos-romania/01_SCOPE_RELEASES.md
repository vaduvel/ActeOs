# Scope, release-uri și limite — LifeOS România

## 1. Strategia de livrare

Platforma este construită complet ca infrastructură (eveniment → orchestrator → proceduri → motor determinist), dar conținutul procedural este activat incremental. Nu este „demo": produsul refuză să expună evenimente sau proceduri neverificate.

## 2. R1 — Evenimentele de frecvență mare (🔥)

**Decizie canonică:** R1 acoperă **toate evenimentele marcate 🔥** din `06_LIFE_EVENT_CATALOG.md`, pe toate domeniile (auto, identitate, mutări/domiciliu, utilități, copii/familie, taxe locale, acte pierdute, sănătate de bază, muncă de bază, firmă de bază).

**Acoperire geografică:**

- Pașii **naționali** (ex. DRPCIV/înmatriculare, ANAF/SPV, evidența persoanelor, pașapoarte, RAR/ITP, ANPIS, CNAS) se livrează la nivel **național**.
- Pașii **locali** (taxe locale, utilități, parcări, circumscripții, programări locale) se livrează ca **pilot Timișoara / județul Timiș**. Restul UAT-urilor rămân `REQUIRES_HUMAN_CURATION` până la curatoriere locală.

Un eveniment poate fi `production` la nivel național chiar dacă pașii lui locali sunt verificați doar pentru Timiș; pentru alte localități, nodurile locale apar ca `verified_with_local_gap` sau `needs_confirmation`, niciodată inventate.

## 3. Ce intră în R1 tehnic

- Android nativ, română, `minSdk 26`, `targetSdk` curent stabil.
- Navigare fără cont pentru explorare; cont opțional pentru sincronizare, notificări, backup.
- Câmp unic **„Ce s-a întâmplat?"** cu interpretare în limbaj natural către un catalog controlat de evenimente (fără a transforma text liber în obligație).
- Selectare județ/localitate și dată de referință.
- **Orchestrator de eveniment**: compune procedurile, ordonează graful, partajează faptele, detectează dependențe și cicluri.
- Pentru fiecare procedură: chestionar ramificat, rezolvare deterministă, timeline, checklist, cerințe `acum` / `dacă se aplică` / `mai târziu`.
- Import foto/PDF prin Storage Access Framework; OCR și verificări formale locale.
- Surse, nivel de încredere, ultima verificare și conflicte vizibile.
- Remindere locale și push opțional; deep-link allowlisted către canalul oficial.
- Feedback „mi s-a cerut altceva" cu flux de re-verificare.
- Portal curator pentru evenimente, proceduri, surse, snapshot, hash, diff și SLA de review.
- Audit, metrics, logs fără PII, feature flags.

## 4. Ce nu intră în R1

- Depunerea automată în numele utilizatorului fără integrare oficială.
- Plăți procesate de aplicație.
- ROeID/autentificare oficială înainte de acord și testare cu ADR.
- Predicții prezentate ca certitudini.
- Validarea autenticității documentelor fără registru oficial.
- Marketplace de agenții; chatbot liber din internet; iOS (API rămâne compatibil cu un client ulterior).

## 5. R2 — frecvență medie (⭐)

Firme & antreprenoriat, sănătate extinsă, educație (echivalări, examene), pașapoarte avansate, muncă extinsă, mobilitate internațională uzuală.

## 6. R3 — frecvență redusă, mare valoare (🏔️)

Construcții/urbanism, succesiuni, divorț, adopții, cetățenie, executări silite, situații de criză complexe. Se adaugă **fără a schimba modelul**.

## 7. Gating pentru publicarea unui eveniment sau a unei proceduri

Un nod (procedură) poate deveni `production` numai dacă: are proprietar de conținut; are cel puțin o sursă oficială pentru fiecare cerință critică; toate claim-urile sunt legate de fragmente verificabile; toate regulile sunt executabile (fără text liber); pragul de prospețime nu este depășit; conflictele critice sunt rezolvate sau blocante în UI; fiecare ramură este testată; există flux de remediere și contact oficial; schimbările cu risc mare au review în doi.

Un **eveniment** poate deveni `production` doar dacă graful lui este aciclic, toate procedurile obligatorii sunt publicabile (sau marcate explicit ca opționale/condiționale), iar dependențele dintre proceduri au justificare.
