# 06 — UX Bible

## 1. Principiul central

Interfața nu expune arhitectura administrației. Expune următoarea acțiune corectă. Complexitatea rămâne în resolver, ruleset și source layer.

## 2. Arhitectura informației mobile

Navigație principală cu maximum cinci zone:

1. **Acasă** — eveniment nou și „Ce urmează”.
2. **Trasee** — active, viitoare, finalizate.
3. **Acte** — vault local, expirări și readiness.
4. **Calendar** — termene și remindere.
5. **Profil** — household, active, confidențialitate și setări.

Pentru utilizatorul anonim, Profil poate fi minimal și datele rămân locale.

## 3. Home

Home are două intrări egale:

1. **Search / intent resolver** — „Ce vrei să rezolvi?”;
2. **Browse categories** — pentru utilizatorul care vrea să exploreze.

Ordinea ecranului:

- Astăzi și cazuri active, dacă există;
- search field + voice adapter opțional;
- quick actions publicate;
- Continuă de unde ai rămas;
- categorii;
- recente/favorite locale.

Home nu obligă utilizatorul să descrie un eveniment și nu pornește automat un caz.

## 4. Intent discovery și clarificare

- query-ul se normalizează local;
- rezultatele provin numai din Intent Atlas publicat;
- maximum trei candidați;
- ambiguitatea produce o alegere explicită;
- no-result oferă categorii și feedback;
- AI fallback este opțional, catalog-gated și nu apare ca autoritate;
- intentul confirmat intră apoi în triage.


Dacă există un candidat dominant:

> Am înțeles: **Ți-ai schimbat adresa de domiciliu**.

Utilizatorul confirmă. Dacă există ambiguitate, afișăm maximum trei opțiuni, fiecare cu diferența concretă. Exemplu:

- „M-am mutat și vreau domiciliu nou”;
- „Stau temporar și vreau reședință/flotant”;
- „Doar schimb titularul la utilități”.

Nu afișăm procent LLM. Afișăm motivul diferenței.

## 5. Triage

### Reguli

- o întrebare per ecran când riscul de eroare este mare;
- întrebările simple pot fi grupate maximum trei;
- fiecare întrebare are „De ce întrebăm?”;
- faptele sensibile sunt marcate și pot fi omise;
- progresul arată câte decizii mai sunt, nu un procent fictiv;
- răspunsurile sunt editabile înainte și după rezolvare.

### Tipuri de control

- boolean: Da/Nu/Nu știu;
- enum: carduri cu descrieri;
- date: picker + explicație a datei relevante;
- adresă: selectare structurată, fără autocomplete neoficial în R1;
- document: scanare opțională, niciodată obligatorie pentru a vedea ruta.

## 6. Journey Dashboard

Above the fold:

- status și numele demersului;
- **Următorul pas**;
- deadline sau „nu există termen confirmat”;
- readiness: număr concret, de exemplu `3 din 5 cerințe gata`;
- butonul principal aferent pasului;
- mesaj de încredere dacă există conflict/staleness.

Sub fold:

- timeline complet;
- acte necesare acum și mai târziu;
- ce s-a schimbat de la ultima rezolvare;
- canale oficiale;
- surse.

Nu folosim scor global 86% dacă pașii nu sunt comparabili. Readiness este per pas și bazat pe cerințe explicite.

## 7. Standardul unui pas

Fiecare ecran de pas răspunde în această ordine:

1. **Ce faci acum** — verb + obiect.
2. **Până când** — dată/fereastră sau necunoscut explicit.
3. **Ce îți trebuie** — mandatory înaintea conditional.
4. **Cum termini** — completion evidence.
5. **Ce faci dacă nu merge** — recovery actions.
6. **De ce** — explicație și surse.
7. **Cât de sigur este** — verified/stale/conflicting.

## 8. Cerințe și documente

Cardul unui document conține:

- denumirea exactă;
- cine îl emite;
- original/copie/electronic;
- valabilitate confirmată;
- moment: acum/mai târziu;
- criteriile de readiness;
- starea locală;
- sursa cerinței.

„Încarcă document” este opțional dacă utilizatorul dorește doar checklist.

## 9. Trust UI

### Verified

„Verificat din surse oficiale la 24 iunie 2026.”

### Stale

„Informația nu a mai putut fi reconfirmată după 30 de zile. Verifică înainte să pleci.”

### Needs confirmation

„Unitatea nu publică clar forma acceptată. Sună și întreabă: «Acceptați documentul semnat electronic sau cereți originalul?»”

### Conflicting

„Două surse oficiale active indică cerințe diferite. Nu continuăm cu verdict verde.”

Starea de încredere nu este ascunsă într-un tooltip.

## 10. Offline și erori

- Journey-urile materializate rămân disponibile offline;
- acțiunile locale se pun în outbox și se sincronizează idempotent;
- sursele externe indisponibile nu șterg progresul;
- dacă rezolvarea nouă nu este posibilă offline, se explică exact de ce;
- mesajele de eroare nu spun doar „ceva nu a mers”.

Exemplu:

> Nu putem verifica acum programul instituției. Traseul și actele tale rămân disponibile. Încearcă din nou înainte de deplasare.

## 11. Copy guide

### Folosim

- „Ia cu tine actul în original.”
- „Cere număr de înregistrare.”
- „Nu solicita încă avizul; ar expira înainte de începere.”
- „Nu putem confirma această cerință.”

### Evităm

- „Se va proceda la...”
- „În vederea...”
- „Utilizatorul este rugat...”
- „Cu succes!” pentru acțiuni care nu sunt încă finalizate oficial.

## 12. Flow canonic: Ana vrea să își actualizeze actele după mutare

1. Ana scrie „vreau să schimb domiciliul în cartea de identitate”.
2. Sistemul diferențiază domiciliu permanent, reședință temporară și simpla schimbare a utilităților.
3. Ana selectează domiciliu permanent.
4. Triage întreabă: proprietar/chiriaș/luată în spațiu; are vehicul; are copii; este administrator de firmă; mutare din altă localitate.
5. Resolverul generează module: identitate, taxe locale, vehicul, utilități și eventual școală/firmă.
6. Dashboardul arată un singur next best action și dependențele.
7. Ana adaugă actele local; readiness semnalează că dovada spațiului locativ lipsește.
8. Când regula locală de program se schimbă, journey-ul este recalculat și pasul afectat primește `needs_review`.
9. După deplasare, Ana marchează rezultatul și poate raporta dacă i s-a cerut altceva.

## 13. Admin UX

Adminul nu este un CMS generic. Fluxul este:

`Source → Snapshot → Claim → Rule draft → Simulation → Review → Publish → Monitor`.

Ecranul de publicare trebuie să arate:

- claim-uri lipsă;
- reguli expirate;
- conflicte nerezolvate;
- fixtures afectate;
- diff față de ruleset-ul activ;
- impact estimate pe journeys active;
- reviewer și motiv.

## 14. Accesibilitate

- contrast și text scalabil;
- target tactil minimum 44×44 puncte echivalente;
- screen reader labels semantice;
- ordinea focusului urmează ordinea acțiunilor;
- statusurile au text și icon, nu doar culoare;
- reduced motion;
- formulare cu erori inline și sumar;
- limbaj român fără abrevieri neexplicate;
- testare cu TalkBack, VoiceOver și tastatură pentru admin.

## 15. Analytics UX

Nu trimitem query-ul brut, adrese, nume, tipul sau titularul documentului ori imagini. Analytics folosesc `intent_type_id`, `category_id`, score band și stări agregabile. Replay-ul și screen recording-ul sunt dezactivate pe ecranele cu date sensibile.
