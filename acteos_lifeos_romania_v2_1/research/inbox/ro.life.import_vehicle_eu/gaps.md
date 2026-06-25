===
# Gaps — ro.life.import_vehicle_eu

| ID | Subiect | Status | De confirmat | Sursa oficială țintă | Comportament motor |
|---|---|---|---|---|---|
| `IEU-G1` | Procedura certificatului TVA | `needs_confirmation` | formularul, canalul ANAF, termenul și situațiile de neplată/regularizare | ANAF | Cere certificatul verificat, fără a calcula TVA sau a inventa canalul. |
| `IEU-G2` | Tarife și dosar RAR | `needs_confirmation` | operațiunile RAR exacte, tarifele și documentele suplimentare pentru cazul concret | RAR | Păstrează ruta RAR și cere confirmare înaintea unei liste exhaustive. |
| `IEU-G3` | Traduceri acte străine | `needs_confirmation` | ce acte se traduc și în ce formă | RAR / DGPCI | Emite foreign_document_translation_requirements. |
| `IEU-G4` | Canale locale în afara Timișului | `verified_with_local_gap` | programarea și procedura locală | prefectura județului competent | Emite local_channel_outside_pilot. |

## Reguli de publicare

- `needs_confirmation`: nu devine fapt și nu produce o obligație fermă fără sursă oficială directă.
- `verified_with_local_gap`: baza națională rămâne utilizabilă, dar canalul/documentația locală se confirmă pentru UAT-ul concret.
- `conflicting`: efectul critic este blocat până la soluționarea contradicției prin revizie umană.

===
