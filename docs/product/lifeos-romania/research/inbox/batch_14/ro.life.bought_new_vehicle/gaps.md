===
# Gaps — ro.life.bought_new_vehicle

| ID | Subiect | Status | De confirmat | Sursa oficială țintă | Comportament motor |
|---|---|---|---|---|---|
| `BNV-G1` | Lista interactivă DFMT | `verified_with_local_gap` | documentele exacte pentru declararea fiscală, în funcție de cumpărare/leasing și reprezentare | DFMT / platforma Atlas | Afișează canalul verificat, dar nu inventează lista locală de acte. |
| `BNV-G2` | Canale în afara pilotului | `verified_with_local_gap` | programarea, sediul și fluxul fiecărui județ | prefectura județului competent / DGPCI | Emite local_channel_outside_pilot. |
| `BNV-G3` | Disponibilitatea combinației și termenul de emitere | `needs_confirmation` | disponibilitatea numărului și timpul de eliberare | DGPCI / SPCRPCIV competent | Nu promite termen sau combinație. |
| `BNV-G4` | Taxe locale conexe | `needs_confirmation` | orice taxă UAT distinctă de tarifele naționale publicate | UAT competent | Nu adaugă taxe locale fără sursă. |

## Reguli de publicare

- `needs_confirmation`: nu devine fapt și nu produce o obligație fermă fără sursă oficială directă.
- `verified_with_local_gap`: baza națională rămâne utilizabilă, dar canalul/documentația locală se confirmă pentru UAT-ul concret.
- `conflicting`: efectul critic este blocat până la soluționarea contradicției prin revizie umană.

===
