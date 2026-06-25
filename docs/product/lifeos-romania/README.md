# LifeOS România — Workbook canonic

**Versiune workbook:** 1.0.0  
**Data:** 25 iunie 2026  
**Statut:** sursă de adevăr pentru produs și gardă de implementare.

## Ce este acest workbook

Acesta este pachetul canonic pentru **LifeOS România**, evoluția produsului anterior „Waze pentru birocrație". Schimbarea de direcție: produsul nu mai este organizat după *proceduri* sau *instituții*, ci după **evenimente de viață**. Utilizatorul descrie ce i s-a întâmplat („m-am mutat", „mi-am cumpărat o mașină", „mi s-a născut copilul"), iar aplicația generează **graful complet de obligații administrative** care decurg din acel eveniment, personalizat, temporal, teritorial și verificat.

Motorul determinist construit anterior **nu se aruncă**: procedura atomică (fostul *intent*) rămâne cărămida pe care motorul o rezolvă. Evenimentul de viață devine un strat nou de **orchestrare** deasupra procedurilor.

## Index

| Fișier | Conținut |
|---|---|
| `CODEX_START_HERE.md` | Punct de intrare, mod de lucru, garduri de adevăr |
| `00_PRODUCT_MANIFEST.md` | Manifestul de produs și cele 12 angajamente |
| `01_SCOPE_RELEASES.md` | Scope, R1/R2/R3, gating de publicare |
| `02_PRD.md` | Cerințe de produs, jobs-to-be-done, NFR, metrici |
| `03_UX_FLOWS.md` | Fluxuri UX: „Ce s-a întâmplat?" → graf de proceduri |
| `04_DOMAIN_MODEL.md` | Model de domeniu: LifeEvent, Intent, orchestrator |
| `05_RULE_ENGINE_SPEC.md` | Motorul determinist + orchestratorul de evenimente |
| `06_LIFE_EVENT_CATALOG.md` | Catalogul de evenimente, taxonomie și frecvență |
| `07_SOURCE_GOVERNANCE.md` | Guvernanța surselor și curatoriere |
| `16_PHASE_PROMPTS.md` | Fazele de implementare în ordine |
| `19_SOURCE_REGISTRY.json` | Registru de surse oficiale reale (R1) |
| `20_CANONICAL_DECISIONS.md` | ADR-uri canonice |

## Reguli de bază

1. Acest workbook este sursa de adevăr. Orice deviație necesită un ADR în `docs/adr/`.
2. Nu inventa instituții, documente, termene, taxe, coduri sau URL-uri. Tot ce este "verified" trebuie legat de o sursă oficială reală.
3. Conținutul procedural se activează incremental; produsul refuză să expună trasee neverificate (`REQUIRES_HUMAN_CURATION`).
