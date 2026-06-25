# Deep Research Brief — Cumpărare/vânzare vehicul înmatriculat în România

## Event

`ro.life.bought_used_vehicle_ro + ro.life.sold_vehicle_ro`

## Territory and reference

România → Timiș → Timișoara. Cercetarea trebuie să precizeze data de referință și să nu amestece ani/perioade.

## Scope variants

- persoană fizică vs juridică
- contract, fiscal, declarare locală, RCA, ITP și transcriere
- ordinea exactă și termenele
- județ diferit, numere păstrate/schimbate
- leasing/moștenire excluse sau separate
- canale și programări Timiș

## Official source targets

- DGPCI/MAI
- RAR
- Direcția Fiscală Timișoara
- legislație fiscală și rutieră
- asigurător/BAAR numai pentru informații oficiale relevante

## Required model

Pentru fiecare variantă: facts, gates, steps, requirements, deadlines, official channels, source claims, freshness, conflicts și gaps. Fiecare step răspunde: ce fac / până când / ce îmi trebuie / cum știu că e gata / ce fac dacă eșuează.

## Critical constraints

- citează exact și atașează locator;
- un claim per obligație independentă;
- marchează explicit practica locală nepublicată ca gap;
- nu deduce obligații conexe doar pentru că „de obicei” sunt făcute;
- integrarea este `DEEP_LINK` până la dovada accesului tehnic și contractual;
- rezultatul intră în `research/inbox`, nu direct în production.

## Output

Urmează integral `research/RESEARCH_BRIEF_TEMPLATE.md` și JSON Schemas din `contracts/jsonschema/`.
