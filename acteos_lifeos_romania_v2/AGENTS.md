# AGENTS.md — Instrucțiuni obligatorii pentru agenții de cod

## Misiune

Construiește ActeOS ca sistem administrativ sigur și explicabil, nu ca demo și nu ca chatbot juridic. Produsul trebuie să poată reproduce retrospectiv de ce a afișat un pas, folosind `ruleset_version`, `reference_date`, jurisdicția și claim-urile sursă.

## Principii care nu se negociază

1. **Event-first:** utilizatorul pornește de la un eveniment de viață.
2. **Deterministic runtime:** LLM-ul nu decide eligibilitate, acte, termene sau verdictul de pregătire.
3. **Evidence-gated:** regulile critice de producție au claim-uri aprobate.
4. **No silent conflict resolution:** conflictul este stare explicită.
5. **Local-first documents:** fișierele sensibile rămân pe dispozitiv implicit.
6. **Optional account:** experiența de bază funcționează fără cont.
7. **Official route first:** ruta gratuită și oficială nu poate fi ascunsă de parteneri.
8. **No synthetic production data:** testele sunt separate și marcate.
9. **API-first:** schimbarea contractelor precedă implementarea consumatorilor.
10. **Accessibility:** WCAG 2.2 AA ca țintă pentru web și principii echivalente native.

## Planificare și skill-uri

- `PLANS.md` definește când și cum se scrie un ExecPlan.
- `codex/EXECUTION_PLAN.md` este document viu și trebuie actualizat în aceeași schimbare cu implementarea.
- Pentru lucru multi-modul, migrații, contracte, reguli sau release este obligatoriu un milestone explicit, cu dovadă de validare și rollback.
- Skill-urile repo-scoped din `.agents/skills/` sunt proceduri operaționale obligatorii când descrierea lor se potrivește sarcinii.
- Nu marca un milestone complet doar pentru că există cod; completează-l numai când acceptance criteria și comenzile de validare au trecut.

## Stack de referință

- Mobile: Expo SDK 56, React Native 0.85, TypeScript, Expo Router, New Architecture.
- Admin: Next.js 16.2, TypeScript, App Router.
- API: Python 3.13, FastAPI 0.138.x, Pydantic v2.
- Database: PostgreSQL 18.x; deployment de referință Supabase EU.
- OpenAPI: 3.1.1.
- Rule engine: Python pur, fără I/O și fără acces direct la LLM.
- Worker: proces Python separat, aceeași bază de cod și coadă PostgreSQL.

Versiunile trebuie blocate în lockfiles după bootstrap; upgrade-urile se fac prin PR separat cu teste complete.

## Reguli de cod

- IDs publice: UUIDv7 sau UUID generate server-side; IDs canonice de domeniu: lowercase dotted/slugs stabile.
- Timp: UTC în DB, `Europe/Bucharest` la prezentare și reguli locale.
- Bani: integer minor units + currency, niciodată float.
- Condiții: AST tipat; niciodată `eval`, cod arbitrar sau propoziție liberă executată.
- Erori: envelope standard din OpenAPI; fără stack trace către client.
- PII: nu apare în loguri, analytics, exception breadcrumbs sau prompturi LLM.
- Orice operațiune de publicare a regulilor produce audit append-only.

## Teste minime la fiecare PR

- lint + typecheck;
- unit tests;
- schema/OpenAPI validation;
- migrations up/down unde este posibil;
- property tests pentru resolver dacă s-a schimbat;
- snapshot tests pentru copy critic;
- a11y checks pentru ecranele modificate;
- verificarea că `testdata` nu intră în build-ul de producție.

## Interdicții

- Nu crea microservicii noi fără ADR și dovadă operațională.
- Nu introduce un nou vendor dacă există o abstracție internă adecvată.
- Nu salva documente în cloud implicit.
- Nu prezenta compatibilitate sau șansă de succes ca probabilitate dacă nu există dataset valid.
- Nu implementa scraping care ignoră robots, termeni sau limitele instituției.
