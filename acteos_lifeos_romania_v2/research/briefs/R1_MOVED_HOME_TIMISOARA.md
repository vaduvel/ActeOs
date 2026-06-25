# Deep Research Brief — Mutare domiciliu/reședință în Timișoara

## Event

`ro.life.moved_home`

## Territory and reference

România → Timiș → Timișoara. Cercetarea trebuie să precizeze data de referință și să nu amestece ani/perioade.

## Scope variants

- carte de identitate vs reședință/flotant
- dovada spațiului locativ și variante proprietar/chiriaș/primire în spațiu
- vehicul și actualizarea înregistrărilor
- declarare imobil/vehicul la taxe locale
- schimb titular utilități
- implicații copil/școală/medic/firmă doar unde există obligație confirmată

## Official source targets

- MAI/DGEP/HUB MAI
- SPCLEP Timișoara
- Direcția Fiscală Timișoara
- DGPCI/DRPCIV
- furnizori oficiali de utilități
- ONRC/ANAF numai pentru variante aplicabile

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
