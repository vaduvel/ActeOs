# 03A — Discovery Layer & Intent Atlas

## 1. Decizia de produs

Intrarea principală în ActeOS este **intenția administrativă a utilizatorului**: ceea ce vrea să obțină, schimbe, declare, înscrie, recupereze sau închidă. Interfața nu îl obligă să formuleze un „eveniment de viață”, să cunoască instituția ori denumirea oficială a procedurii.

Întrebarea principală este:

> **Ce vrei să rezolvi?**

Exemple: „vreau să schimb buletinul”, „înmatriculez o mașină”, „pașaport pentru copil”, „certificat fiscal”, „înscriere la grădiniță”.

Categoriile rămân vizibile pentru explorare. Utilizatorul poate fie să caute direct, fie să navigheze: `Home → categorie → intenție`.

## 2. Cele patru concepte care nu trebuie amestecate

| Concept | Întrebarea la care răspunde | Exemplu | Rol în sistem |
| --- | --- | --- | --- |
| Intent | Ce vrea omul să rezolve acum? | „Vreau să-mi schimb cartea de identitate” | intrare publică și ID canonic de discovery |
| Life event | Ce context mai larg poate declanșa mai multe nevoi? | „M-am mutat” | compoziție și recomandări conexe |
| Procedure component | Ce operațiune instituțională reutilizabilă este necesară? | declarare la taxe locale | nod intern al traseului |
| Journey | Ce pași se aplică situației concrete? | traseul personalizat pentru Daniel, Timișoara, data X | rezultat materializat și versionat |

Un intent poate fi direct (`schimb cartea de identitate`) sau compus (`rezolv toate formalitățile după mutare`). Un life event poate sugera mai multe intenturi, dar nu este obligatoriu ca utilizatorul să pornească de la el.

## 3. Arhitectura de navigație duală

### Calea A — utilizatorul știe ce vrea

`Home → query → Intent Resolver → confirmare candidat → fapte minime → Journey`

### Calea B — utilizatorul explorează

`Home → categorii → listă intenturi → intent → fapte minime → Journey`

### Calea C — context compus opțional

`Intent bundle / life event → intenturi copil recomandate → utilizatorul activează numai ce vrea → journeys coordonate`

Nicio cale nu sare peste confirmarea intentului canonic. Un model AI nu poate crea un intent nou și nu poate porni automat un traseu administrativ neconfirmat.

## 4. Home — ierarhia obligatorie

1. **Active cases / Astăzi**, dacă există termene ori pași activi.
2. Titlu: **„Ce vrei să rezolvi?”**
3. Câmp de căutare: **„Caută: buletin, mașină, pașaport, certificat…”**
4. Quick actions bazate pe catalogul publicat, nu hardcodate fără ID.
5. **Continuă de unde ai rămas**, dacă există cazuri locale.
6. **Explorează după categorie** — toate categoriile rămân accesibile.
7. Recente și favorite, numai după ce există istoric și consimțământ local.

Home nu este chatbot obligatoriu. Voice input și asistentul conversațional sunt adaptoare ale aceleiași căutări canonice.

## 5. Modelul canonic al unui Intent

Un `intent_type` conține minimum:

- `id`: ID stabil, de forma `ro.intent.<domain>.<action>`;
- `category_id`;
- `kind`: `direct_goal | bundle_goal`;
- `title_ro`: formulare orientată pe acțiune;
- `outcome_ro`: rezultatul pe care îl urmărește utilizatorul;
- `aliases_ro`: formulări și abrevieri acceptate;
- `negative_aliases_ro`: expresii care trebuie să reducă scorul sau să excludă candidatul;
- `linked_event_ids`: contexte de viață în care poate apărea;
- `journey_template_id` sau strategia de compoziție;
- `jurisdiction_scope`;
- `release_wave`, `research_status`, `production_status`;
- `availability_policy`;
- `search_boost` controlat editorial;
- `catalog_version` și audit de schimbare.

Intent Atlas este taxonomie de produs. El nu declară acte, taxe sau termene și nu are nevoie de claim juridic pentru sinonime. Journey-ul și regulile administrative continuă să fie evidence-gated.

## 6. Reguli de authoring pentru Intent Atlas

1. Titlul începe cu un verb sau exprimă clar obiectivul.
2. Două intenturi se separă dacă produc trasee, fapte inițiale ori rezultate fundamental diferite.
3. Sinonimele și greșelile comune nu creează ID-uri noi.
4. Un intent direct nu este duplicat doar fiindcă poate apărea într-un bundle.
5. Un intent bundle explică ce intenturi copil poate activa și nu le marchează automat completate.
6. Aliasurile nu includ afirmații administrative neverificate.
7. Fiecare alias ambiguu are test de disambiguare.
8. Un intent retras rămâne rezolvabil istoric, dar nu apare în discovery public.

## 7. Intent Resolver — pipeline determinist

```text
query brut
→ validare lungime și limbă
→ normalizare română
→ exact title/alias lookup
→ prefix și token lookup
→ lexical ranking
→ filtre availability/jurisdiction/production status
→ negative alias penalties
→ deduplicare pe intent_id
→ maximum 3 candidați
→ praguri de încredere și diferență între scoruri
→ confirmarea utilizatorului
```

Resolverul de intent nu decide acte, eligibilitate sau termene. El selectează doar un ID canonic publicat.

## 8. Normalizarea textului românesc

Normalizerul este versionat și testat. El aplică:

- Unicode NFKC;
- lowercase/casefold;
- echivalență cu/fără diacritice la căutare, fără a altera copy-ul afișat;
- normalizarea cratimelor, apostrofurilor și spațiilor;
- tokenizare stabilă;
- expandarea controlată a abrevierilor: `CI`, `CEI`, `CIV`, `RCA`, `ITP`, `DRPCIV/DGPCI`, `SPCLEP`, `PFA`, `SRL`;
- corecții numai dintr-un dicționar aprobat, nu autocorrect liber;
- păstrarea tokenilor numerici relevanți;
- eliminarea datelor sensibile înainte de orice fallback extern.

## 9. Ranking v1

Scorul final este reproductibil pentru aceeași versiune de index și aceleași filtre. Semnale implicite:

| Semnal | Greutate de referință |
| --- | ---: |
| titlu exact normalizat | 1.00 |
| alias exact | 0.96 |
| prefix de titlu/alias | 0.82 |
| acoperire tokeni / BM25 lexical | 0.55 |
| categorie selectată | +0.12 |
| disponibil în jurisdicție | +0.10 |
| intent recent/favorit local | max +0.06 |
| popularitate agregată | max +0.04 |
| negative alias | -0.40 până la excludere |
| indisponibil / nepublicat | exclus |

Popularitatea nu poate depăși o potrivire lexicală mai bună. Sponsorizarea nu este semnal de ranking.

### Praguri

- `high`: scor ≥ 0.82 și diferență față de locul 2 ≥ 0.08;
- `ambiguous`: minimum doi candidați peste 0.55 și diferență < 0.08;
- `low`: cel mai bun scor între 0.35 și 0.55;
- `no_result`: sub 0.35.

Chiar și la `high`, utilizatorul confirmă intentul înaintea creării cazului. Nu există auto-start tăcut.

## 10. AI/semantic fallback

Fallback-ul semantic este opțional și dezactivat implicit. Dacă este activat:

- primește text redacționat;
- poate returna numai ID-uri din catalogul publicat;
- maximum 5 candidați intră în gate-ul determinist;
- fiecare ID este revalidat pentru disponibilitate și jurisdicție;
- răspunsul modelului nu modifică scoring-ul administrativ;
- modelul, versiunea, latența și modul sunt în trace;
- indisponibilitatea vendorului revine la căutarea locală;
- query-ul brut nu este păstrat în analytics.

## 11. Disambiguare

Ecranul de clarificare trebuie să răspundă: „Care dintre acestea vrei să rezolvi?” și să arate maximum trei rezultate. Exemplu pentru „cazier”:

- Obțin cazier judiciar;
- Obțin cazier fiscal;
- Verific situația unei firme — dacă acest intent există și este publicat.

Fiecare card arată rezultat, categorie și o propoziție diferențiatoare. Nu solicităm fapte personale până când intentul nu este confirmat.

## 12. No-result și recovery

La zero rezultate:

1. păstrăm query-ul local în sesiune;
2. sugerăm reformulare și categorii apropiate;
3. oferim „Nu găsesc ce caut”;
4. utilizatorul poate trimite feedback fără date personale;
5. feedback-ul intră în coada editorială `intent_gap`, nu creează automat un intent;
6. nu inventăm un răspuns administrativ generic.

## 13. Categorii

Categoriile sunt suprafață de explorare, nu clasificare juridică. Ele pot conține intenturi directe și bundle-uri. Ordinea este editorială și poate folosi utilitate locală, fără sponsorizare ascunsă.

Lista inițială:

- Identitate și documente;
- Casă, adresă și utilități;
- Vehicule și mobilitate;
- Familie, copii și stare civilă;
- Educație;
- Muncă și protecție socială;
- Sănătate și îngrijire;
- Taxe, bani și sancțiuni;
- Firmă și activitate independentă;
- Proprietate, construcții și urbanism;
- Străinătate, rezidență și cetățenie;
- Juridic, urgențe și participare civică.

## 14. Istoric, favorite și personalizare

- Recentele sunt locale implicit.
- Favoritele sunt alegerea explicită a utilizatorului.
- Personalizarea nu ascunde catalogul complet.
- Un intent recent poate primi maximum boost-ul configurat.
- Istoricul poate fi șters independent de cazuri și documente.
- O persoană nu este profilată comercial după demersurile căutate.

## 15. Analytics și confidențialitate

Evenimente permise:

- `discovery_home_viewed`;
- `intent_query_started`;
- `intent_results_shown` cu bucket de rezultate, nu text brut;
- `intent_candidate_selected`;
- `intent_disambiguation_shown`;
- `intent_no_result` cu hash rotativ/feature vector non-reversibil, dacă privacy review aprobă;
- `category_opened`;
- `intent_started`;
- `intent_abandoned`.

Interzis implicit: query brut, CNP, nume, adresă, număr de înmatriculare, conținut OCR sau combinații care pot reidentifica persoana.

## 16. Contracte API publice

- `GET /v1/discovery/home`;
- `GET /v1/categories`;
- `GET /v1/intents`;
- `POST /v1/intents/resolve-query`;
- `GET /v1/intents/{intent_type_id}`;
- `POST /v1/cases` cu `intent_type_id` obligatoriu.

`/v1/life-events/classify` rămâne temporar compatibil, este marcat deprecated și nu este folosit de noul Home.

## 17. Persistență

Entități noi:

- `content.intent_categories`;
- `content.intent_types`;
- `content.intent_aliases`;
- `content.intent_event_links`;
- `app.intent_query_feedback`;
- `app.cases.intent_type_id`;
- `app.cases.event_context_ids`.

Search index-ul local este derivat din catalogul publicat, semnat/versionat și poate fi reconstruit. Nu este sursă de adevăr.

## 18. Acceptance criteria v2.1

- căutarea funcționează offline pentru catalogul livrat;
- query-urile cu și fără diacritice produc aceeași ordine;
- aliasul exact este stabil și testat;
- maximum trei candidați sunt afișați;
- un rezultat ambiguu cere confirmare;
- niciun intent nepublicat nu poate fi returnat;
- un AI fallback nu poate introduce ID necunoscut;
- categoriile rămân disponibile fără query;
- Home păstrează „Continuă de unde ai rămas”;
- query-ul brut nu apare în logs/analytics;
- `intent_type_id`, resolver version și index version intră în trace;
- pornirea unui Journey se face numai după confirmarea intentului.
