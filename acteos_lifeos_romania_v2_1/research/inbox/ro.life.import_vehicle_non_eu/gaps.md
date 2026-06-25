===
# Gaps — ro.life.import_vehicle_non_eu

| ID | Subiect | Status | De confirmat | Sursa oficială țintă | Comportament motor |
|---|---|---|---|---|---|
| `INE-G1` | Tarif vamal și baza de calcul | `needs_confirmation` | codul TARIC, valoarea în vamă, cursul, taxele și TVA pentru vehiculul concret | Autoritatea Vamală Română / TARIC UE | Emite customs_rate_and_import_vat_amount; nu calculează din presupuneri. |
| `INE-G2` | Scutiri și regimuri speciale | `needs_confirmation` | eligibilitatea, documentele și decizia pentru mutare de reședință, bunuri personale sau alte scutiri | Autoritatea Vamală Română | Emite customs_relief_eligibility. |
| `INE-G3` | EORI și reprezentare vamală | `needs_confirmation` | dacă este necesar EORI și forma mandatului vamal | Autoritatea Vamală Română | Nu introduce EORI ca document obligatoriu universal. |
| `INE-G4` | Traduceri/legalizări | `needs_confirmation` | cerințele per document și țara emitentă | RAR / DGPCI / autoritatea emitentă | Emite foreign_document_translation_requirements. |
| `INE-G5` | Operațiuni și tarife RAR | `needs_confirmation` | lista și costurile pentru omologare/CIV/autenticitate | RAR | Nu afișează tarif RAR fără sursă directă. |

## Reguli de publicare

- `needs_confirmation`: nu devine fapt și nu produce o obligație fermă fără sursă oficială directă.
- `verified_with_local_gap`: baza națională rămâne utilizabilă, dar canalul/documentația locală se confirmă pentru UAT-ul concret.
- `conflicting`: efectul critic este blocat până la soluționarea contradicției prin revizie umană.

===
