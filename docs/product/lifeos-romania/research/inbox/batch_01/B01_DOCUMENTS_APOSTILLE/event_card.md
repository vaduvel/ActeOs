# Event Card — ro.life.documents_apostille (life.documents_apostille)

**Batch:** B01_DOCUMENTS_APOSTILLE  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Am un document românesc pe care trebuie să îl folosesc în străinătate și vreau să știu dacă trebuie apostilat.”

## Limita evenimentului

Determină mai întâi dacă apostila este necesară și autoritatea competentă. Nu tratează orice «ștampilă pentru străinătate» ca apostilă și nu trimite automat utilizatorul la prefectură.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `destination_scope` | `enum` | `eu`, `hague`, `non_hague`, `unknown` | da |
| `destination_country` | `string` | statul de destinație | da |
| `document_category` | `enum` | `administrative`, `judicial`, `notarial`, `private`, `identity_document`, `passport` | da |
| `document_subject` | `enum` | `birth`, `marriage`, `death`, `name`, `domicile`, `citizenship`, `criminal_record`, `fiscal`, `qualification`, `studies`, `other` | da |
| `issuance_format` | `enum` | `paper_original`, `digitally_signed_original`, `scan` | da |
| `requester_role` | `enum` | `holder`, `legal_representative`, `spouse`, `relative_degree_1`, `relative_degree_2`, `other`, `proxy`, `lawyer`, `institution_delegate` | da |
| `hub_account_validated` | `boolean` | cont HUB validat | condițional |
| `holder_or_relative_domicile_timisoara` | `boolean` | criteriu competență Timiș | condițional |
| `issuer_headquarters_county` | `boolean` | sediul emitentului în județ | condițional |
| `convention_status_known` | `boolean` | regimul destinației verificat | da |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `determine_apostille_authority` | autoritate competentă identificată | tip document și destinație |
| `obtain_apostille` | apostilă emisă | original, competență, solicitant |
| `submit_to_prefecture_apostille_office` | dosar administrativ depus | document eligibil prefecturii |

## Reguli-cheie verificate

- În UE, pentru documentele publice acoperite, apostila nu este cerută pentru autenticitate.
- Pentru state non-Haga fără tratat aplicabil se verifică supralegalizarea, nu apostila.
- Prefectura apostilează acte oficiale administrative; tribunalul și camera notarilor au competențe distincte.
- Originalul electronic semnat digital poate fi apostilat online în HUB; o simplă scanare nu este original electronic.

## Canal pilot Timișoara / Timiș

Instituția Prefectului — Județul Timiș. Certificatele de stare civilă și cazier pot fi apostilate la orice prefectură; pentru alte acte se verifică domiciliul titularului/rudei sau sediul emitentului.

## Guvernanță

Lista statelor Convenției și tratatele bilaterale sunt date volatile și nu sunt înghețate în regulă. `destination_scope` trebuie alimentat dintr-un registru verificat la data cererii.
