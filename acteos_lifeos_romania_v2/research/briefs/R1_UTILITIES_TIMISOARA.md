# Deep Research Brief — Schimb titular utilități după mutare

## Event

`ro.life.change_electricity_holder / gas / water / heat`

## Territory and reference

România → Timiș → Timișoara. Cercetarea trebuie să precizeze data de referință și să nu amestece ani/perioade.

## Scope variants

- electricitate, gaz, apă/canal, termoficare
- proprietar/chiriaș/moștenire
- index, contract, acte, dovada proprietății
- canale online/fizice și termene
- separarea operatorului de distribuție de furnizor

## Official source targets

- Aquatim
- Colterm
- PPC/ENGIE/E.ON și operatorii relevanți
- ANRE pentru reguli generale

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
