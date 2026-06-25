# Event Resolver Spec

Event Resolver are voie sa faca:
- clasificare intentie din text;
- propunere de event_type candidates;
- selectie intrebari minime;
- explicatie conversationala.

Event Resolver NU are voie sa faca:
- sa decida eligibilitate;
- sa inventeze acte;
- sa modifice route output;
- sa ascunda `needs_confirmation`.

## Output
```json
{
  "candidates": [{"event_type_id":"life.moved", "confidence":0.91}],
  "required_facts": ["move.new_address", "user.owns_vehicle"],
  "unsafe_to_resolve": false
}
```
