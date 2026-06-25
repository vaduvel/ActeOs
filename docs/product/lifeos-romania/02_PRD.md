# Product Requirements Document — LifeOS România

## 1. Obiectivul produsului

Reducerea drumurilor administrative inutile și creșterea ratei de finalizare a evenimentelor de viață, transformând regulile publice într-un graf personalizat, temporal, teritorial și explicabil de proceduri declanșate de un eveniment.

## 2. Jobs to be done

### Cetățean

- Când mi se întâmplă ceva în viață, vreau să văd **toate** obligațiile administrative care decurg, în ordinea corectă, ca să nu descopăr la ghișeu că mai trebuia ceva.
- Când pregătesc dosarul unei proceduri din lanț, vreau să știu ce îmi lipsește și ce e doar condițional.
- Când o informație e incertă, vreau să văd întrebarea exactă, nu o presupunere.
- Când mă apropii de un termen, vreau să fiu avertizat și să văd alternativa.
- Când termin un pas, vreau ca pașii dependenți să se deblocheze automat.

### Curator

- Vreau să definesc un eveniment ca o compoziție de proceduri cu dependențe și condiții de aplicabilitate.
- Când o sursă se schimbă, vreau diff-ul și impactul asupra procedurilor și a evenimentelor care le includ.
- Când public, vreau să pot reproduce, audita și reveni la versiunea anterioară.

### Operator produs

- Vreau să văd ce reguli se apropie de expirare, ce conflicte sunt deschise, ce feedback indică respingeri reale și ce evenimente au cea mai mare rată de abandon.

## 3. Personaje de referință

- **Mihai — m-am mutat:** un eveniment care atinge evidența persoanelor (CI), DRPCIV (talon), DFMT (taxe locale), utilități și medicul de familie. Nu știe ordinea; LifeOS i-o dă.
- **Ana — mi-am cumpărat o mașină:** transcriere → impozit local → certificat fiscal → RCA → ITP → înmatriculare DRPCIV. Vrea un singur flux.
- **Elena — mi s-a născut copilul:** certificat de naștere → CNP → alocație → indemnizație → medic de familie → creșă/grădiniță.
- **Radu — curator:** compune și verifică evenimente și proceduri, blochează publicarea dacă dovada e slabă.

## 4. Capabilități funcționale

### FR-00 Descoperirea evenimentului

- Câmp unic „Ce s-a întâmplat?" cu interpretare NL către un catalog controlat de evenimente.
- Dezambiguizare prin întrebări scurte (ai mașină? ai firmă? ai copii?).
- Niciun text liber nu devine direct obligație.

### FR-01 Orchestrarea evenimentului

- Selectarea procedurilor aplicabile evenimentului pe baza faptelor.
- Construirea grafului orientat de proceduri cu dependențe (`depends_on`), faze și condiții.
- Detectarea ciclurilor și a dependențelor moarte; sortare topologică stabilă.
- Fapte partajate: o dată introduse, propagate la toate procedurile relevante.
- `event_plan_hash` reproductibil.

### FR-02 Context și jurisdicție

- Județ, UAT, instituție, dată de referință, an procedural.
- Fapte tipate cu motiv și durată de păstrare.

### FR-03 Rezolvarea procedurii (reutilizează motorul existent)

- Bundle publicat per intent/jurisdicție/timp; predicate tipate; sortare topologică a pașilor; output cu `route_hash`, surse și stări de încredere.

### FR-04 Checklist și timeline (per procedură și agregat pe eveniment)

- Statusuri: `not_started`, `ready`, `blocked`, `in_progress`, `submitted`, `completed`, `not_applicable`.
- Vedere agregată pe eveniment: progres total, următorul pas deblocat, blocaje.

### FR-05 Dosar și document readiness

- Import local, clasificare, OCR, câmpuri extrase, findings (`blocking`/`warning`/`info`/`unknown`).
- `authenticity_status` separat de `readiness_status`.
- Un document încărcat o dată poate satisface cerințe în mai multe proceduri ale aceluiași eveniment (cu consimțământ).

### FR-06 Surse și explicabilitate

- Confidence: `verified`, `verified_with_local_gap`, `needs_confirmation`, `conflicting`, `expired`. Fără procent decorativ.

### FR-07 Canal oficial; FR-08 Recalculare; FR-09 Feedback de teren; FR-10 Portal curator

- Ca în modelul anterior, extinse cu nivelul eveniment: recalcularea unui fapt poate re-planifica graful; feedback-ul poate viza un nod sau o dependență; portalul permite compunerea de evenimente.

## 5. Cerințe non-funcționale

- Route resolve p95 < 400 ms cu bundle în cache; event-plan p95 < 700 ms pentru evenimente cu ≤ 15 proceduri.
- Rezolvarea și planificarea sunt pur deterministe, fără call extern.
- Offline util pentru evenimentele și documentele descărcate.
- Zero secrete în client sau repo. Disponibilitate țintă API R1: 99.5%.
- WCAG 2.2 AA portal; accesibilitate Android, font scaling 200%; localizare RO completă.
- Telemetria nu conține CNP, nume, adrese, OCR raw sau imagini.

## 6. North Star și metrici

**North Star:** procentul de evenimente de viață duse la capăt fără drum administrativ inutil și fără obligație omisă de produs.

Metrici secundare: drumuri inutile evitate; timp de la eveniment la dosar gata; rată de abandon per eveniment; reguli critice expirate expuse (țintă zero); procent de pași cu provenance complet; procent de documente procesate exclusiv local.

## 7. Evenimente analytics fără PII

`life_event_selected`, `event_plan_resolved`, `procedure_opened`, `question_answered` (cu `question_id`), `route_resolved`, `requirement_marked_ready`, `document_analysis_started` (tip generic), `finding_created` (cod), `official_channel_opened`, `event_recalculated`, `procedure_completed`, `life_event_completed`. Toate cu consent, dezactivabile.
