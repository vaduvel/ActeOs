# Workbook execution checklist

## Before Codex starts

- [ ] Mount this folder in the target repository.
- [ ] Paste `15_CODEX_MASTER_PROMPT.md` into Codex.
- [ ] Confirm the environment can install pinned toolchains.
- [ ] Do not provide production credentials in chat or commit them.

## Human inputs that code cannot legitimately invent

- [ ] Product/repository name and domains.
- [ ] EU hosting providers and contracts.
- [ ] Curator identities and OIDC tenant.
- [ ] Production signing keys and Android Play Console access.
- [ ] Local Timiș/Timișoara official sources, units, criteria, addresses and circumscription data.
- [ ] Formal approvals for ROeID, ANAF or payment integrations.
- [ ] Legal review/DPIA and privacy contacts.

Codex must implement safe `NOT_CONFIGURED` states for these, not block the rest of the build and not simulate access.

## Phase tracking

- [ ] P0 Foundation
- [ ] P1 Contracts and persistence
- [ ] P2 Rule engine
- [ ] P3 Content pipeline
- [ ] P4 API and journeys
- [ ] P5 Curator portal
- [ ] P6 Android experience
- [ ] P7 Local documents
- [ ] P8 Verified R1 content
- [ ] P9 Security/operations
- [ ] P10 Release

## Final acceptance

- [ ] `make test-all` passes.
- [ ] `make build-all` passes.
- [ ] Preschool and primary rule certifications pass.
- [ ] No critical stale rule is public.
- [ ] Android critical flow passes TalkBack and 200% font scale.
- [ ] Documents stay local by default.
- [ ] Source-to-screen provenance is visible.
- [ ] Curator two-person rule and rollback are proven.
- [ ] Restore and security verification are complete.
- [ ] Known limitations are public and honest.
