# Research gaps — B13_PAY_FINE

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Contul IBAN și beneficiarul concret | `needs_confirmation` | datele din procesul-verbal și canalul oficial al autorității | procesul-verbal + pagina autorității |
| 2 | Derogările din legi speciale | `needs_confirmation` | dacă regula OG nr. 2/2001 este modificată pentru domeniul amenzii | actul sancționator indicat în procesul-verbal |
| 3 | Instanța competentă și taxa judiciară | `needs_confirmation` | instanța, modalitatea de depunere și cuantumul taxei | OG nr. 2/2001 + OUG nr. 80/2013 |
| 4 | Efectul plății asupra plângerii | `needs_confirmation` | raportul dintre plata redusă, restituire și admiterea plângerii | jurisprudență și procedura autorității |
| 5 | Plata amenzilor rutiere prin canale locale | `verified_with_local_gap` | cont, beneficiar și eventuale platforme | MAI / UAT / ghișeul.ro |

## Politica truth-guard

Formula este arătată doar când toate faptele bazei sunt confirmate. Suma, IBAN-ul și destinatarul nu sunt inventate sau deduse din exemple.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale`, `expired` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
