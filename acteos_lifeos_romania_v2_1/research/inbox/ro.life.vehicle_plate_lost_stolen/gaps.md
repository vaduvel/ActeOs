===
# Gaps — ro.life.vehicle_plate_lost_stolen

| ID | Subiect | Status | De confirmat | Sursa oficială țintă | Comportament motor |
|---|---|---|---|---|---|
| `VPL-G1` | Configurații B/C/D și disponibilitatea tipului D | `needs_confirmation` | numărul de plăcuțe pentru vehiculul concret și disponibilitatea tehnică actuală a tipului D | DGPCI / SPCRPCIV | Emite nonstandard_plate_pair_configuration; pentru D emite și confirmarea disponibilității. |
| `VPL-G2` | Sancțiunea pentru depășirea termenului | `needs_confirmation` | consecința juridică actuală a depășirii celor 30 de zile | legislatie.just.ro / Poliția Română | Marchează overdue fără a inventa amendă. |
| `VPL-G3` | Canalul raportării furtului fără urgență | `needs_confirmation` | unitatea competentă și forma sesizării | Poliția Română / IPJ competent | Nu recomandă petiția online ca echivalent universal al plângerii. |
| `VPL-G4` | Canale în afara pilotului | `verified_with_local_gap` | programarea și ridicarea plăcuțelor | prefectura județului competent | Emite local_channel_outside_pilot. |

## Reguli de publicare

- `needs_confirmation`: nu devine fapt și nu produce o obligație fermă fără sursă oficială directă.
- `verified_with_local_gap`: baza națională rămâne utilizabilă, dar canalul/documentația locală se confirmă pentru UAT-ul concret.
- `conflicting`: efectul critic este blocat până la soluționarea contradicției prin revizie umană.

===
