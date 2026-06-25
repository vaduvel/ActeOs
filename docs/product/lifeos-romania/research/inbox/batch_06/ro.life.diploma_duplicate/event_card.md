===
# Event Card — ro.life.diploma_duplicate (life.diploma_duplicate)

- batch_id: `B06_DIPLOMA_DUPLICATE`
- status: `research_inbox`
- publication_gate: `blocked_pending_human_review`
- pilot: `ro.tm.timisoara`
- accessed_at: `2026-06-25`
- title_ro: Am nevoie de un duplicat al diplomei / actului de studii

## Declanșator

Utilizatorul nu mai poate folosi actul de studii original ori acesta conține o eroare imputabilă emitentului.

## Fapte cerute

| fact | tip | valori / observații |
|---|---|---|
| `education_level` | `enum` | preuniversity \| higher_education |
| `duplicate_reason` | `enum` | lost \| stolen \| destroyed \| damaged \| issuer_error |
| `archive_location` | `enum` | issuing_school \| national_archives \| destroyed_or_lost \| unknown |
| `approval_date` | `date\|null` | data aprobării cererii preuniversitare |
| `pickup_by` | `enum` | holder \| proxy |
| `name_changed_after_original` | `boolean` | dacă numele s-a schimbat după original |
| `institution_requests_issuance_fee` | `boolean` | doar pentru controlul taxei universitare |

## Reguli verificate

- Preuniversitar: pierdere/furt/distrugere → declarație notarială/consulară, dovadă Monitorul Oficial Partea a III-a, copie legalizată stare civilă, două fotografii 3x4 și aprobarea ISJ.
- Preuniversitar: termenul verificat este de maximum 30 de zile de la aprobarea cererii, nu de la depunere.
- Învățământ superior: emitentul trebuie să fie instituția acreditată, iar ministerul indică eliberare gratuită; procedura concretă rămâne instituțională.

## Conflicte și limitări

- PDF-ul oficial din 2016 conține și trimiteri fiscale istorice; nicio taxă preuniversitară nu este publicată automat fără text consolidat actual.

## Canal pilot Timiș/Timișoara

- Preuniversitar: unitatea emitentă/deținătoarea arhivei; dacă arhiva este la Arhivele Naționale, inspectoratul școlar.
- Universitar: instituția de învățământ superior acreditată care a emis actul.
- Canalul exact ISJ Timiș și orice programare/taxă locală rămân de confirmat.

## Control de publicare

- source_claims: `12`
- rules: `13`
- golden_fixtures: `22`
- output_status: `draft_not_for_automatic_publication`
===
