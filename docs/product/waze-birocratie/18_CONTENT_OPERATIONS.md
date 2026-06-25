# Content operations handbook

## 1. Product truth is an operation

The application is not correct because it was correct at launch. Every journey needs an owner, sources, review rhythm, tests and an emergency withdrawal path.

## 2. Roles

- **Source operator:** registers/fetches sources; cannot publish.
- **Content curator:** converts evidence into typed claims/rules.
- **Legal reviewer:** verifies authority, competence, temporal applicability and conflict resolution.
- **Publisher:** verifies gates and promotes bundles.
- **Security/privacy reviewer:** reviews sources, documents and data handling when relevant.
- **Incident commander:** coordinates critical rule failures.

For high/critical rules, author and final approver are different people.

## 3. Source onboarding checklist

- official publisher and authority identified;
- canonical HTTPS URL;
- jurisdiction and competence;
- normative or operational status;
- update cadence/freshness class;
- robots/terms and permitted retrieval;
- final URL/redirect behavior;
- document type and parser;
- fallback official contact;
- owner and SLA;
- first snapshot reviewed manually.

## 4. Claim requirements

Every claim contains:

- atomic statement;
- exact evidence excerpt;
- locator in immutable snapshot;
- publisher and authority;
- territory;
- effective start/end;
- confidence;
- extractor and verifier;
- affected rule paths.

Do not combine multiple obligations into one claim if they can change independently.

## 5. Rule authoring checklist

- stable ID and intent;
- explicit scope and dates;
- typed facts;
- typed predicates;
- steps and dependencies;
- mandatory/conditional/later requirements;
- accepted forms: original/copy/electronic/certified;
- readiness checks;
- deadline model;
- completion evidence;
- recovery actions;
- official channel;
- claim links for every critical assertion;
- risk class and freshness threshold;
- golden fixtures.

## 6. Legal/source conflict resolution

Evaluate in order:

1. Is each source authentic and current?
2. What is its legal/administrative rank?
3. Is the issuer competent for the subject and territory?
4. Is it effective at the evaluation date?
5. Is one rule a lawful special rule or explicit derogation?
6. Is the difference only operational detail permitted by the superior rule?
7. Can the conflict be resolved with another official source or written confirmation?

If not resolved, mark `conflicting`, block a green readiness verdict and give the user an exact confirmation question.

## 7. Change severity

- **Cosmetic:** spelling/layout; no route effect.
- **Explanatory:** wording/context; no requirement effect.
- **Operational:** address, schedule, link, submission method.
- **Critical:** eligibility, required document, deadline, fee, legal basis, selection criterion, completion evidence.

Critical changes page the content owner, freeze affected publication when unsafe, and require two reviews.

## 8. Freshness defaults

These are defaults, overridable with justification:

- active admission/registration calendar: 7 days during campaign, 30 days otherwise;
- required-document page: 30 days during campaign, 90 days otherwise;
- institution address/program: 30 days;
- stable law: 180 days plus change monitoring;
- explanatory evergreen content: 365 days.

A failed fetch does not extend freshness.

## 9. Feedback verification

User feedback is a signal. Triage flow:

1. deduplicate;
2. assess urgency and affected scope;
3. request optional evidence without demanding unnecessary personal data;
4. check official sources/contact institution;
5. create/update claim and tests;
6. publish through normal gates;
7. inform reporter if consent exists;
8. record cause and prevention.

A clerk's verbal request is not automatically a valid rule. It may expose an undocumented operational practice or an unlawful demand; both require confirmation.

## 10. R1 content certification

For preschool and primary journeys, certification report includes:

- source inventory and snapshot hashes;
- jurisdiction matrix;
- branch coverage;
- critical claim provenance coverage;
- boundary-date tests;
- local gaps;
- reviewer identities/roles;
- rule and bundle hashes;
- canary dates/results;
- known limitations and user-facing copy.

## 11. Monthly operations review

- stale and near-stale rules;
- fetch failure rates;
- critical change lead time;
- confirmed feedback incidents;
- false-block and missed-requirement rates;
- first-time acceptance sample;
- unresolved conflicts;
- owner capacity and cost per maintained journey;
- journeys that should be suspended or retired.

## 12. Neutrality and partners

External providers may be listed only in a separate optional help layer. The free official/self-service route remains first and complete. A commercial relationship cannot:

- change legal requirements;
- create a fake mandatory step;
- hide a free route;
- affect confidence;
- rank a provider as if endorsed by an authority;
- use document or journey data for targeting without separate informed consent.
