# Research gaps — R1_MOVED_HOME (de rezolvat inainte de promovare in productie)

| # | Gap | Status | Ce trebuie confirmat | Sursa tinta |
|---|---|---|---|---|
| G1 | Termen legal actualizare certificat inmatriculare la schimbarea domiciliului | needs_confirmation | termenul exact (sursele secundare spun 30 zile, neoficial) | OUG 195/2002, RNTR, lista oficiala DRPCIV (dgpci.mai.gov.ro) |
| G2 | Cuantum si articol exact al sanctiunii contraventionale | verified_with_local_gap | reconfirmare 40-80 lei din textul consolidat curent OUG 97/2005 | legislatie.just.ro DetaliiDocument/63354 |
| G3 | Procedura concreta de actualizare adresa la CEI si impactul asupra termenului de 15 zile | needs_confirmation | cum se actualizeaza adresa fara act nou; mai exista obligatie de prezentare? | carteadeidentitate.gov.ro, DEP Timisoara |
| G4 | Locator exact HG 295/2021 art. 57 + lista completa documente | partial | numar exact articol + lista oficiala integrala | legislatie.just.ro HG 295/2021 |
| G5 | 'extras de carte funciara nu mai vechi de 30 de zile' valabil pentru Timisoara | needs_confirmation | confirmarea regulii locale pentru dovada adresei | primariatm.ro/dovada-adresa-domiciliu |
| G6 | Viza de resedinta (flotant): documente, valabilitate, taxa | needs_confirmation | lista oficiala + valabilitate | primariatm.ro evidenta persoanelor, OUG 97/2005 |
| G7 | Transfer dosar fiscal local (DITL/DFMT) la mutare in alt UAT | not_started | proceduri si termene transfer fiscal vehicul/proprietate | dfmt.ro, servicii.primariatm.ro |
| G8 | Medic de familie / CNAS actualizare la mutare | not_started | daca exista obligatie/termen sau e optional | cnas.ro |

## Regula de promovare

Niciun claim `needs_confirmation` nu produce o regula critica `active`. `rule.moved.vehicle_address_update` si `rule.moved.residence_visa` raman `in_review` pana la inchiderea G1/G6. Promovarea in ruleset activ necesita: claim verificat + reviewer independent + golden fixtures verzi (vezi production_gate).
