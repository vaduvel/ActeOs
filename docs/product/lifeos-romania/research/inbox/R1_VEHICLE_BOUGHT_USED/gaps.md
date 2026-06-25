# Research gaps — R1_VEHICLE_BOUGHT_USED

| # | Gap | Status | De confirmat | Sursa tinta |
|---|---|---|---|---|
| GV1 | Termen 90 zile transcriere | needs_confirmation | temei + cuantum din Ordinul MAI 1501/2006 | legislatie.just.ro / Ordin 1501/2006 |
| GV2 | Taxa certificat inmatriculare (37 vs 49 lei) | needs_confirmation | tariful oficial curent | tarife DRPCIV |
| GV3 | Sanctiunea pentru depasirea termenului fiscal de 30 zile | partial | cuantum amenda Cod Fiscal | L227/2015, art. sanctiuni |
| GV4 | Lista exacta formular declaratie fiscala vehicul la DFMT Timisoara | needs_confirmation | formular ITL + pasi pe dfmt.ro | dfmt.ro |
| GV5 | Sanctiunea pentru depasirea termenului de transcriere | not_started | exista/cuantum | Ordin 1501/2006 |
| GV6 | Cazuri vehicul din UE/non-UE (prima inmatriculare) | out_of_scope | eveniment separat | DRPCIV / RAR |

## Politica truth-guard

Termenul de 90 de zile (critic) este `in_review` cu `require_confirmation`; nu se afiseaza ferm pana la confirmarea din Ordinul 1501/2006. Termenul fiscal de 30 de zile este `verified` (Cod Fiscal + multiple DITL).
