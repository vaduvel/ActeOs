===
# Gaps — ro.life.vehicle_stolen

| ID | Subiect | Status | De confirmat | Sursa oficială țintă | Comportament motor |
|---|---|---|---|---|---|
| `VST-G1` | Canalul sesizării fără urgență | `needs_confirmation` | unitatea de poliție competentă, forma sesizării și documentul eliberat | Poliția Română / IPJ competent | Emite competent_non_emergency_police_reporting_channel; nu prezintă petiția online drept plângere universală. |
| `VST-G2` | Notificarea asigurătorului | `needs_confirmation` | termenul, canalul și documentele prevăzute de polița CASCO/RCA sau de asigurător | contractul de asigurare / asigurătorul concret | Emite insurance_contract_notification_deadline și nu inventează un termen. |
| `VST-G3` | Recuperarea vehiculului | `needs_confirmation` | efectul recuperării asupra dosarului penal, al radierii și al evidențelor | Poliția competentă / SPCRPCIV | Oprește certitudinea traseului prin vehicle_recovery_status_before_deregistration. |
| `VST-G4` | Dovada substitutivă pentru documentele furate | `needs_confirmation` | denumirea și forma exactă acceptată de serviciul competent | SPCRPCIV competent | Cere dovadă substitutivă generică, fără formular inventat. |
| `VST-G5` | Canale locale în afara Timișului | `verified_with_local_gap` | programarea și modalitatea de depunere în județul competent | prefectura județului competent | Emite local_deregistration_channel_outside_pilot. |

## Reguli de publicare

- `needs_confirmation`: nu devine fapt și nu produce o obligație fermă fără sursă oficială directă.
- `verified_with_local_gap`: baza națională rămâne utilizabilă, dar canalul/documentația locală se confirmă pentru UAT-ul concret.
- `conflicting`: efectul critic este blocat până la soluționarea contradicției prin revizie umană.

===
