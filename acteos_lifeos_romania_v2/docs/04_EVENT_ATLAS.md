# 04 — Event Atlas

## 1. Rolul atlasului

Event Atlas definește vocabularul produsului. El nu este o listă de meniuri și nici copia nomenclatorului statului. Este harta schimbărilor și obiectivelor pe care utilizatorul le recunoaște în propria viață și care pot declanșa obligații administrative.

## 2. Granularitate

Un `life_event_type` trebuie să fie suficient de stabil încât să poată fi recunoscut în limbaj natural și suficient de larg încât să compună mai multe proceduri. „M-am mutat” este eveniment. „Completez formularul X” este pas. „Schimb cartea de identitate” poate fi eveniment direct sau obligație copil a mutării.

### Reguli de modelare

- un eveniment descrie o schimbare, pierdere, dobândire, expirare sau obiectiv;
- un pas descrie o acțiune din traseu;
- o cerință descrie un act, o informație sau o condiție necesară pasului;
- un eveniment umbrelă poate declanșa evenimente copil;
- două evenimente se separă dacă au fapte, calendar sau instituții fundamental diferite;
- sinonimele nu creează event types distincte;
- evenimentele recurente, precum plata unei amenzi sau obținerea unui cazier, sunt acceptate chiar dacă nu sunt „eveniment de viață” în sens sociologic.

## 3. Taxonomia de nivel 1

1. Identitate și documente
2. Casă, adresă și utilități
3. Vehicule și mobilitate
4. Familie, copii și stare civilă
5. Educație
6. Muncă și protecție socială
7. Sănătate, dizabilitate și îngrijire
8. Taxe, bani și sancțiuni
9. Firmă și activitate independentă
10. Proprietate, construcții și urbanism
11. Străinătate, rezidență și cetățenie
12. Juridic, urgențe și participare civică

Taxonomia completă și machine-readable se află în `data/event_taxonomy.yaml`.

## 4. Modelul de relații

Fiecare eveniment poate avea:

- `parent_event_id`: eveniment umbrelă;
- `triggered_event_ids`: evenimente potențial declanșate;
- `mutually_exclusive_with`: variante care nu pot coexista;
- `requires_assets`: persoană, vehicul, proprietate, firmă;
- `default_jurisdiction_scope`: national/county/uat/institution;
- `frequency_band`: high/medium/low;
- `pain_band`: high/medium/low;
- `maintenance_cost`: high/medium/low;
- `research_status`: not_started/in_progress/approved/blocked;
- `release_wave`: R1A/R1B/R2/R3/later.

## 5. Life Graph

Pentru personalizare, produsul modelează un graf minim al vieții administrative:

- persoane și relații: self, spouse, child, dependent, representative;
- adrese: domiciliu, reședință, adresă de corespondență;
- active: vehicul, proprietate, firmă;
- documente: tip, titular, emitent, expirare, locație locală;
- evenimente: occurrence cu dată și jurisdicție;
- journeys: instanțe de traseu;
- obligații: active, finalizate, expirate, blocate.

Datele din graf sunt opționale. Utilizatorul poate crea un Journey fără profil permanent.

## 6. Scorul de prioritate

Pentru ordinea de research și implementare:

`priority = 0.25*frequency + 0.25*pain + 0.20*multi_step + 0.15*cross_institution + 0.10*verifiability + 0.05*commercial_fit - maintenance_penalty`

Scorurile sunt relative, 1–5. Nu sunt prezentate utilizatorului și nu pretind statistici oficiale dacă nu există dataset.

## 7. Wedge-uri R1

### W1 — Mutare

Valoare: compune identitate, vehicul, taxe locale, utilități, școală/medic și firmă dacă se aplică. Demonstrează motorul de evenimente compuse.

### W2 — Auto buy/sell

Valoare: volum mare, multe dependențe, diferențe persoană/firma/import/leasing și durere ridicată.

### W3 — Identitate

Valoare: frecvent, urgent, ușor de explicat și legat de expirări.

### W4 — Taxe locale și certificat fiscal

Valoare: transversal pentru auto și proprietate; bun pentru integrarea canalelor oficiale.

### W5 — Acte pierdute

Valoare: urgență, ordine critică a pașilor și potențial anti-fraudă.

### W6 — Household

Valoare: retenție și administrarea documentelor familiei, fără a transforma produsul într-o rețea socială.

## 8. Reguli de navigație în atlas

- Home afișează maximum 8 shortcut-uri, determinate de prioritate și context local.
- Căutarea caută titlu, sinonime și trigger phrases.
- Un utilizator poate porni direct de la o procedură; sistemul îi sugerează evenimentul umbrelă dacă există obligații conexe.
- Când două evenimente sunt posibile, se cere alegere; nu se pornește o rută arbitrară.
- Un eveniment nou nu intră în producție până când are event card, facts, research brief, fixtures și owner operațional.
