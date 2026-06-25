# UX flows și specificația ecranelor

## 1. Arhitectura informației

### Navigație principală Android

1. **Acasă** — intenții, trasee active, următorul termen.
2. **Trasee** — active, finalizate, arhivate.
3. **Dosar** — documente locale și statusuri.
4. **Setări** — localitate, notificări, confidențialitate, cont.

„Surse” nu este tab separat; este disponibil contextual din fiecare regulă și pas.

## 2. Flow end-to-end al cetățeanului

### E01 — Onboarding și controlul datelor

**Scop:** utilizatorul înțelege produsul înainte să ofere date.

Ecranul conține:

- „Îți construim traseul. Instituția decide.”
- „Documentele rămân pe telefon în mod implicit.”
- selectare județ/localitate;
- opțiune „folosește fără cont”;
- link către politica de confidențialitate.

**Acceptance:** traseul poate fi explorat fără cont, email sau număr de telefon.

### E02 — Acasă

Componente:

- search field „Ce vrei să rezolvi?”;
- buton microfon numai dacă serviciul este disponibil;
- card „Continuă traseul”;
- termen apropiat;
- categorii de viață;
- banner discret când o sursă critică necesită reverificare.

### E03 — Dezambiguizare intenție

Exemplu pentru „înscriu copilul”:

- creșă/antepreșcolar;
- grădiniță/preșcolar;
- clasa pregătitoare;
- transfer școlar;
- admitere liceu.

Nu se afișează răspuns generat liber; se mapează la `intent_id` controlat.

### E04 — Introducere traseu

Arată:

- rezultatul urmărit;
- ce poate și ce nu poate face aplicația;
- aproximarea numărului de pași;
- jurisdicția și anul;
- sursele de bază;
- buton „Începe”.

### E05 — Întrebări care schimbă ruta

Reguli UX:

- o singură întrebare principală pe ecran;
- „De ce întrebăm?” disponibil;
- progress semantic, nu procent fals;
- revenirea păstrează răspunsurile;
- orice răspuns sensibil are explicația retenției;
- opțiune „Nu știu” doar dacă motorul are ramură pentru necunoscut.

### E06 — Diagnosticul administrativ

Exemplu:

> Procedură: înscriere nouă la grădiniță  
> Nivel: preșcolar  
> Etapă aplicabilă la data de referință: etapa a II-a  
> Opțiuni în cerere: 3  
> Situații speciale identificate: program prelungit

Afișează ce informație locală lipsește și nu promite admiterea.

### E07 — Traseu general

Timeline cu pașii:

- pregătește opțiunile;
- pregătește documentele;
- validează cererea;
- urmărește rezultatul;
- pregătește documentele medicale;
- începe frecventarea.

Fiecare pas are status, termen, dependențe și sursă.

### E08 — Ecranul „Următorul pas”

Ordine fixă:

1. **Ce faci acum** — verb și acțiune.
2. **Până când** — termen și countdown accesibil.
3. **Ai nevoie de** — documente/date/originale.
4. **Este gata când** — dovada finalizării.
5. **Dacă nu merge** — remediere și contact.
6. Accordion: de ce, sursă, excepții, versiune.

Microcopy:

> Încarcă adeverințele de angajat ale părinților.  
> Le cerem deoarece ai ales program prelungit.  
> Dosar: 6 din 8 cerințe pregătite.  
> Nu pleca încă spre unitate.

### E09 — Dosar personalizat

Secțiuni:

- Necesare acum;
- Numai dacă se aplică;
- Necesare mai târziu;
- Nu se aplică situației tale.

Fiecare requirement are:

- nume simplu;
- motiv;
- emitent;
- format și originale;
- valabilitate;
- status;
- findings;
- provenance.

### E10 — Import și scanare

- CameraX/ML Kit document scanner sau Storage Access Framework.
- Preview înainte de analiză.
- mesaj „Analiza are loc pe telefon”.
- selectare tip document sugerat, cu confirmare.
- procesare fără upload implicit.

### E11 — Rezultat document

Exemple de findings:

- **Blocant:** „Actul de identitate este expirat.”
- **Blocant:** „Lipsește pagina 2.”
- **Avertisment:** „Actul expiră înainte de termenul estimat al depunerii.”
- **Confirmare:** „Nu am putut confirma prezența semnăturii. Verifică vizual.”
- **Informativ:** „Numele copilului a fost citit; confirmă-l înainte de salvare.”

Nu se afișează „document autentic”.

### E12 — Sursa regulii

Bottom sheet:

- emitent;
- titlu;
- URL oficial allowlisted;
- fragment justificativ;
- rang juridic/administrativ;
- teritoriu;
- `effective_from`/`effective_to`;
- ultima verificare;
- status conflict;
- „Raportează o problemă”.

### E13 — Ghid de depunere

- instituție și unitate;
- adresă verificată;
- program cu freshness separat;
- necesitatea programării;
- originale și copii;
- taxe și canal oficial;
- text sugerat pentru solicitare;
- dovada pe care utilizatorul trebuie să o primească;
- buton „Deschide canalul oficial”.

### E14 — Recalculare

Arată diff:

- pas nou;
- pas eliminat;
- document devenit necesar;
- termen schimbat;
- sursa care a declanșat schimbarea.

Utilizatorul confirmă aplicarea noii rute; versiunea veche rămâne în audit local.

### E15 — Feedback de teren

Formular scurt:

- tip problemă;
- instituție/unitate;
- data vizitei;
- ce i s-a cerut sau ce a fost greșit;
- dovadă opțională, cu redacție locală;
- consimțământ pentru upload dacă atașează.

Mesaj final:

> Raportarea ta nu schimbă automat regula. Echipa o verifică în sursa oficială.

### E16 — Finalizare

- rezultat și dată;
- număr de înregistrare/confirmare păstrat local;
- următorul pas dacă există;
- feedback „acceptat din prima?”;
- opțiune arhivare și ștergere documente.

## 3. Flow-ul Anei — grădiniță

1. Ana scrie „Vreau să înscriu copilul la grădiniță”.
2. Motorul selectează `ro.education.preschool.enrollment`.
3. Întrebări: data nașterii, deja înscris, localitate, program, situația părinților, criterii speciale, metoda de depunere.
4. Motorul calculează nivelul, etapa temporală, documentele și opțiunile.
5. Ana vede că ordinea depunerii nu oferă prioritate și că cererea are trei opțiuni.
6. Alege unități numai din registry-ul local verificat; dacă registry-ul nu este complet, aplicația spune asta.
7. Dosarul include actele standard și ramurile pentru program prelungit/divorț/email.
8. Scannerul verifică formal documentele.
9. Aplicația îi spune când să obțină avizul epidemiologic, evitând emiterea prea devreme.
10. La validare, îi amintește să prezinte originalele.
11. Salvează numărul de înregistrare.
12. Dacă nu primește loc, ruta trece la etapa următoare și importă numai locurile oficial publicate.

## 4. Flow curator

1. Curatorul înregistrează sursa și frecvența.
2. Workerul descarcă un snapshot, păstrând URL, headers, hash și moment.
3. Diff-ul clasifică schimbarea: cosmetică, informativă, procedurală, critică.
4. Extractorul AI propune claim-uri și reguli cu citate.
5. Validatorul respinge schema incompletă sau condiții text libere.
6. Curatorul verifică claim cu claim.
7. Un reviewer secund aprobă modificările de risc mare.
8. Sistemul rulează impact analysis și testele aferente.
9. Se publică un bundle canary.
10. După monitorizare, bundle-ul devine general; rollback-ul rămâne disponibil.

## 5. Stări goale și erori

- **Nu găsim intenția:** sugerăm categorii și contact oficial; nu improvizăm.
- **Nu există date locale:** arătăm baza națională și lista clară de informații ce trebuie confirmate local.
- **Sursa este indisponibilă:** folosim ultima versiune numai dacă politica de freshness permite; altfel blocăm afirmația critică.
- **Conflict de surse:** pasul afectat este `needs_confirmation`, nu „safe”.
- **OCR eșuat:** documentul rămâne utilizabil manual; solicităm confirmare, nu respingere automată.
- **Offline:** traseul cache-uit este disponibil cu timestamp; linkurile și informațiile volatile sunt marcate.
