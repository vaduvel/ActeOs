# Guvernanța surselor — LifeOS România

## 1. Principiu

Nimic publicat ca `verified` fără o sursă oficială trasabilă. Registrul `19_SOURCE_REGISTRY.json` conține doar surse verificate manual. Restul conținutului de reguli rămâne `REQUIRES_HUMAN_CURATION`.

## 2. Ierarhia autorității

1. Legislație primară și secundară (lege, OUG, HG, ordine de ministru).
2. Portaluri oficiale ale autorității competente (gov.ro, mai.gov.ro, anaf.ro etc.).
3. Pagini oficiale locale (primării, DFMT, CJAS, AJPIS) pentru pași locali.
4. Niciodată forum/blog/agregator drept sursă primară.

## 3. Clase de prospețime

- **A (volatil):** programe, taxe, disponibilitate ghișee, sloturi — reverificare frecventă; fail-closed pe stale.
- **B (semi-stabil):** liste de documente, pași procedurali — reverificare periodică.
- **C (stabil):** baze legale, competențe — reverificare rară.

Fiecare autoritate din registru are o `freshness_class` implicită; claim-urile pot suprascrie per câmp.

## 4. Ciclul de curatoriere

1. Capturare snapshot al sursei (URL + dată + hash conținut).
2. Extragere `SourceClaim` tipat (cerință/termen/canal/taxă) cu citare.
3. Doi curatori (two-person rule) pentru promovare la `verified`.
4. Legare claim → `RuleVersion` → bundle publicat.
5. Eveniment: claim-uri și pentru includerea procedurii și pentru fiecare `depends_on` critic.

## 5. Pilot teritorial

R1: pașii naționali (DRPCIV, ANAF, pașapoarte, RAR, CNAS, CEI) acoperă toată țara. Pașii locali sunt verificați doar pentru **Timișoara/Timiș** (DFMT, Primăria Timișoara). Pentru alte UAT-uri, nodul local apare ca `verified_with_local_gap` sau `needs_confirmation`, cu îndrumare către portalul local — niciodată informație inventată.

## 6. Conflicte și retrageri

La conflict între surse, se aplică ierarhia din modelul de domeniu; fără verdict, starea rămâne `conflicting`. La retragerea unei surse, claim-urile derivate trec în `withdrawn` și bundle-urile afectate se reevaluează.
