# Research gaps — B03_INHERITANCE_SUCCESSION

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Termenul opțiunii succesorale și calculul lui | `needs_confirmation` | articolul exact, punctul de pornire și excepțiile | Codul civil consolidat, articol atomic |
| 2 | Competența notarului | `needs_confirmation` | regula ultimului domiciliu, excepțiile și cazurile transfrontaliere | Legea nr. 36/1995 consolidată + Regulamentul notarial |
| 3 | Dosarul notarial complet | `needs_confirmation` | actele pentru succesibili, bunuri, datorii și reprezentare | UNNPR / Camera Notarilor Publici Timișoara / notar competent |
| 4 | Taxele și onorariile | `needs_confirmation` | onorariul minimal, impozitul și efectul finalizării după 2 ani | Codul fiscal + Ordinul onorariilor notariale 2026 |
| 5 | Declarația fiscală și intabularea după certificat | `needs_confirmation` | termene, formulare și taxe | ANCPI/OCPI Timiș + DFMT/UAT |
| 6 | Succesiune cu ultim domiciliu în străinătate | `needs_confirmation` | Regulamentul UE, legea aplicabilă și certificatul european | e-Justice UE + legislație națională |

## Politica truth-guard

Fluxul local de sesizare este verificat. Termenele, taxele, competența și dosarul notarial rămân explicit `in_review`; nicio valoare uzuală din practică nu a fost introdusă ca fapt.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
