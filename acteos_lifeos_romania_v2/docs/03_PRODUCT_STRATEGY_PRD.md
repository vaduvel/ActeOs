# 03 — Product Strategy & PRD

## 1. Context și oportunitate

O procedură singulară, precum înscrierea la grădiniță, este utilă dar sezonieră. Produsul devine recurent când înțelege evenimentele care generează mai multe obligații și când păstrează continuitatea administrativă a unei persoane sau familii: mutare, vehicul, documente, taxe, naștere, muncă, proprietate, firmă și expirări.

Wedge-ul nu este „catalog de acte”. Wedge-ul este **orchestrarea personalizată a evenimentelor cu frecvență și fricțiune ridicate**, pornind din Timișoara și extinzând baza națională.

## 2. Segmente inițiale

### P1 — Adult activ, 25–45 ani

Are mașină, chirie sau proprietate, schimbă jobul, adresa și furnizorii. Valoare: ordine, timp economisit, notificări și document vault.

### P2 — Familie cu copii

Gestionează documentele mai multor persoane, educație, beneficii, pașapoarte și sănătate. Valoare: household graph, termene și partajare controlată.

### P3 — Persoană cu alfabetizare administrativă redusă

Nu știe instituțiile sau vocabularul. Valoare: limbaj natural, pași simpli, telefon/adresă exactă și explicații.

### P4 — Român care revine sau pleacă în străinătate

Are acte emise în sisteme diferite, traduceri, transcrieri și consulate. Valoare mare, dar complexitate ridicată; intră după consolidarea motorului.

### P5 — Micro-antreprenor

Evenimentele personale se intersectează cu firma: domiciliu/sediu, administrator, vehicul, taxe. R2, nu nucleu R1.

## 3. Jobs-to-be-done

- „Când mi se întâmplă X, spune-mi tot ce decurge din asta, nu doar primul formular.”
- „Spune-mi ce contează pentru cazul meu și elimină restul.”
- „Ajută-mă să nu ajung cu dosarul incomplet.”
- „Spune-mi exact unde și pe ce canal rezolv.”
- „Amintește-mi înainte să expire sau să treacă termenul.”
- „Arată-mi sursa ca să pot verifica singur.”
- „Când informația nu este sigură, spune-mi ce întrebare să pun instituției.”

## 4. Scope R1

### R1A — fundația și primele trasee

1. M-am mutat în Timișoara / mi-am schimbat adresa.
2. Am cumpărat o mașină second-hand deja înmatriculată în România.
3. Am vândut o mașină.
4. Cartea de identitate este expirată / pierdută / furată / schimb adresă.
5. Am nevoie de certificat fiscal sau declarare la taxe locale.
6. Mi-am pierdut mai multe acte simultan.

### R1B — extensii de tracțiune

7. Schimb titularul la utilități.
8. Obțin cazier judiciar.
9. Reînnoiesc/obțin pașaport.
10. Mi s-a născut copilul — traseu administrativ de bază.
11. Înscriere grădiniță și clasa pregătitoare, folosind research-ul verificat.
12. Plătesc sau clarific o amendă și canalul oficial.

## 5. În afara scope-ului R1

- depunerea automată în numele utilizatorului fără integrare oficială;
- plăți intermediate de ActeOS;
- semnătură electronică proprie;
- autentificare ROeID presupusă;
- autenticitate document din fotografie;
- marketplace deschis;
- predicții de admitere sau de acceptare a dosarului;
- consultanță juridică personalizată;
- construirea unei baze naționale complete înainte de validarea operațională locală.

## 6. Suprafețe de produs

### Mobile

- Home: input „Ce s-a întâmplat?” + evenimente rapide + obligații apropiate;
- clarificare candidat eveniment;
- triage facts;
- Journey Dashboard;
- detaliu pas și cerință;
- Document Vault local;
- Calendar și notificări;
- Household / persoane / active;
- surse și încredere;
- feedback „mi s-a cerut altceva”.

### Admin web

- registry de surse și snapshot-uri;
- claim editor atomic;
- rule composer tipat;
- simulator de trasee;
- conflict/gap queue;
- freshness dashboard;
- approval și ruleset publish;
- feedback triage;
- audit explorer.

### Backend

- clasificare candidat;
- case/facts;
- resolver;
- journey materialization;
- document readiness metadata;
- notifications;
- content operations;
- audit și observability.

## 7. Cerințe funcționale

| ID | Cerință | Prioritate |
|---|---|---|
| FR-001 | Utilizatorul poate descrie evenimentul în limbaj natural | Must |
| FR-002 | Sistemul returnează maximum 3 candidați explicați când clasificarea nu este sigură | Must |
| FR-003 | Triage-ul solicită numai fapte care pot modifica ruta | Must |
| FR-004 | Utilizatorul poate continua anonim și local | Must |
| FR-005 | Resolverul materializează un Journey din ruleset activ | Must |
| FR-006 | Fiecare pas arată acțiune, termen, cerințe, finalizare și recovery | Must |
| FR-007 | Cerințele sunt mandatory/conditional/optional și now/later | Must |
| FR-008 | Fiecare obligație critică expune claim-urile aprobate | Must |
| FR-009 | Starea stale/conflicting/needs_confirmation este vizibilă | Must |
| FR-010 | Utilizatorul poate marca progresul și încărca dovada locală | Must |
| FR-011 | Document readiness rulează verificări formale configurate | Must |
| FR-012 | Sistemul nu afirmă autenticitate fără verificator autorizat | Must |
| FR-013 | Journey poate fi recalculat fără pierderea progresului compatibil | Must |
| FR-014 | Canalele oficiale sunt filtrate după pas și jurisdicție | Must |
| FR-015 | Utilizatorul poate raporta respingere sau cerință diferită | Must |
| FR-016 | Curatorul poate crea claim, regulă și ruleset fără deploy | Must |
| FR-017 | Reviewerul trebuie să aprobe înainte de publicare | Must |
| FR-018 | Auditul reține cine, ce și de ce a publicat | Must |
| FR-019 | Household permite gestionarea persoanelor și activelor | Should |
| FR-020 | Notificările se generează pentru deadline, expiry și rule change | Should |
| FR-021 | Cloud sync pentru vault este opt-in separat | Should |
| FR-022 | Partajarea unui Journey este granulară și revocabilă | Could |
| FR-023 | Ajutorul partener poate fi solicitat, separat de ruta oficială | Could |

## 8. Cerințe non-funcționale

| ID | Cerință |
|---|---|
| NFR-001 | Resolver P95 sub 500 ms pentru ruleset încărcat și fără conector extern |
| NFR-002 | Journey deschis offline din cache local sub 250 ms pe dispozitiv mediu |
| NFR-003 | Orice rezultat are `trace_id`, `ruleset_version` și `reference_date` |
| NFR-004 | Disponibilitate țintă R1: 99,5% pentru API-ul de bază |
| NFR-005 | RPO DB maxim 15 minute; RTO operațional maxim 4 ore pentru R1 |
| NFR-006 | Zero PII în loguri și analytics by design |
| NFR-007 | Admin MFA obligatoriu și RBAC least privilege |
| NFR-008 | OpenAPI și JSON Schemas validate în CI |
| NFR-009 | WCAG 2.2 AA pentru admin/web; echivalent nativ pentru mobil |
| NFR-010 | O regulă critică hard-expired nu poate produce `ready` |
| NFR-011 | Datele sintetice nu pot ajunge în environment production |
| NFR-012 | Migrațiile DB sunt forward-safe și au plan de rollback/roll-forward |

## 9. Funnel de produs

1. `event_input_started`
2. `event_candidate_selected`
3. `triage_started`
4. `triage_completed`
5. `journey_generated`
6. `first_step_viewed`
7. `requirement_ready`
8. `official_channel_opened`
9. `outcome_reported`
10. `first_submission_accepted` sau `rejection_reported`

PII și textul liber nu intră în analytics. Se păstrează doar event_type, stare, timpi și coduri agregabile.

## 10. Gates de lansare R1

- toate traseele R1 au minimum 20 fixtures deterministe, inclusiv negative și boundary dates;
- 100% obligații critical au claim activ sau sunt explicit blocate;
- adminul poate retrage o regulă fără release mobil;
- niciun fișier din `testdata/` nu este inclus în bundle production;
- document deletion este testată end-to-end;
- journey recalculation păstrează progresul doar dacă semantic step key rămâne compatibil;
- feedback-ul de respingere creează automat ticket de reverificare;
- ruta oficială este afișată înaintea opțiunilor comerciale;
- copy-ul critic este revizuit de content designer și accessibility review.

## 11. Ipoteze de validat

- evenimentele compuse generează valoare percepută mai mare decât procedurile izolate;
- reminder-ele și household-ul cresc retenția fără dark patterns;
- utilizatorii plătesc mai degrabă pentru dosar urmărit/familie decât pentru abonament generic;
- un pilot local disciplinat este mai credibil decât acoperire națională superficială;
- integrarea partenerilor funcționează doar dacă neutralitatea este demonstrabilă.
