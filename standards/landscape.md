# Open Coordination Infrastructure Landscape Survey

Status: initial research frame; no capability decisions accepted. Last checked: 2026-10-07. Findings below are leads for a systematic survey, not endorsements or dependency decisions.

## Method

For each capability, compare candidate standards and active implementations. Use primary sources where possible: normative specifications, governance documents, license files, source repositories, security documentation, and conformance/implementation evidence. Record maturity and date checked. Assess governance, license, decentralization, interoperability, local/offline behavior where relevant, security model, dependencies, and CoordMesh fit. Separate standard properties from implementation properties. Every capability receives REUSE, PROFILE, INVENT, or UNKNOWN/MORE RESEARCH with rationale and evidence. No implementation should precede a documented gap.

## Initial research leads

| Capability area | Candidates to investigate | Preliminary disposition |
| --- | --- | --- |
| Resource, process, economic coordination | ValueFlows; PLANET/Open Co-op; Beckn | UNKNOWN — compare semantic coverage and governance |
| Event transport and federation | Matrix; ActivityPub/ActivityStreams; Git; Openmesh | UNKNOWN — compare interaction models, sync, offline behavior, security, implementations |
| Identity, authentication, claims | DID Core; Verifiable Credentials; WebAuthn; OpenID Connect/OAuth; Murmurations; Solid/ActivityPods | UNKNOWN — distinguish key continuity, authentication, discovery, issuer claims, and trust |
| Data representation and interchange | JSON Schema; GeoJSON; iCalendar | UNKNOWN — likely reused where suitable; profile only for shared semantics |
| Distributed storage/compute | IPFS; Holochain | UNKNOWN — establish whether needed at all |
| Payments and settlement | SEPA and relevant payment APIs | UNKNOWN — jurisdictional and operational suitability requires focused research |
| Access, agreements, proposals, decisions, accounting | Existing standards and vocabularies across the above | UNKNOWN — do not infer these require new primitives |

## Early source observations

- The [Matrix Specification](https://spec.matrix.org/latest/) defines APIs for synchronizing extensible events across a federated network; rooms replicate event history among participating homeservers. This is evidence of transport/event capabilities, not evidence that Matrix should own CoordMesh domain semantics. **Lead classification: UNKNOWN; inspect exact boundaries and implementations.**
- [Verifiable Credentials Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/) is a W3C Recommendation describing issuer, holder, and verifier roles for claims. It is relevant to attestations, but does not by itself establish a universal identity system or CoordMesh trust policy. **Lead classification: REUSE candidate for claim representation; profile fit UNKNOWN.**
- ActivityPub is a W3C Recommendation for federated social data exchange; investigate its actor/inbox/outbox model and operational ecosystem before comparing it with Matrix for coordination event semantics.
- ValueFlows is a key research lead because its vocabulary addresses resource flows and economic processes. Its scope and overlap with each candidate CoordMesh concept must be assessed against current specifications and implementations before any primitive is accepted.

## Capability map (not yet decided)

No capability is yet classified as an accepted CoordMesh REUSE, PROFILE, or INVENT decision. Use the table above as a research queue, then add evidence-backed rows with primary source, date, maturity, license, governance, deployment properties, limitations, and decision rationale.

## Source starting points

- [Matrix Specification](https://spec.matrix.org/latest/)
- [W3C Verifiable Credentials Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/)
- [W3C DID Core](https://www.w3.org/TR/did-core/)
- [W3C ActivityPub](https://www.w3.org/TR/activitypub/)
- [ValueFlows](https://valueflo.ws/)

This list is intentionally incomplete; survey additional candidates and remove irrelevant ones based on evidence.
