# Open Coordination Infrastructure Landscape Survey

Status: research increment; findings are evidence-based candidates, not accepted CoordMesh dependencies or protocol decisions. Sources checked 2026-10-07. Standards and projects change; re-check status before relying on a version or license.

## Purpose and method

CoordMesh is exploring generic coordination mechanisms, not a new institution. This survey compares existing standards and projects against the candidate capability areas without treating the candidate names as protocol primitives. It prioritizes normative specifications, maintainers' governance and license documents, and official implementation documentation. It distinguishes a standard's defined behavior from what a particular deployment or implementation provides.

Disposition language:

- **REUSE candidate** — an existing standard or project appears to provide all or part of a needed capability; adoption is not yet a project decision.
- **PROFILE candidate** — a future, concrete interoperability scenario may need a documented, constrained subset or mapping of an existing standard. No CoordMesh profile is approved by this survey.
- **INVENT** — no item below currently justifies a new protocol mechanism. Use this classification only after a demonstrated gap survives comparison with reuse and profiling.
- **UNKNOWN / MORE RESEARCH** — evidence, requirements, implementation maturity, or licensing is insufficient for a decision.

The license remarks are screening observations, not legal advice. Check canonical source repositories and the licenses for the exact artifacts to be used. ValueFlows' canonical repository has moved from GitHub to Codeberg; the mirror says the RDF Turtle is its specification system of record and documents are CC BY-SA 4.0, but the canonical host was not directly readable in this survey. Its current governance and per-artifact licensing therefore remain to be confirmed.

## Summary capability map

| Capability under consideration | Evidence-backed candidates | Preliminary disposition | Main boundary / uncertainty |
| --- | --- | --- | --- |
| Resource, need/offer, commitment, agreement, proposal, economic event, accounting | ValueFlows; Credit Commons Protocol | **REUSE candidate:** ValueFlows for resource/process/economic semantics; Credit Commons only for nested mutual-credit ledgers. **PROFILE candidate:** constrain ValueFlows only if a concrete shared scenario needs predictable interoperability. | ValueFlows is a broad community vocabulary, not a universal coordination protocol. Credit Commons is a particular mutual-credit accounting protocol, not generic accounting. |
| Public entity / project discovery and profile interchange | Murmurations; Schema.org; JSON Schema | **REUSE candidate:** Murmurations for public, discoverable profiles/directories where appropriate; reuse shared fields/schemas. | The index is a discovery component; publicly indexed profiles are not suitable by default for private needs, access-control lists, or sensitive household inventories. |
| Event transport, synchronization, federation | Matrix; ActivityPub / ActivityStreams; Git (for source history) | **REUSE candidate:** Matrix or ActivityPub may carry an application’s events, depending on the interaction shape. **PROFILE candidate:** application-specific event vocabularies and authorization mapping may be needed. | Matrix rooms synchronize shared event/state graphs; ActivityPub distributes actor activities to inboxes. Neither defines CoordMesh resource/decision semantics or guarantees domain-level consensus. Git is version control, not a live coordination protocol. |
| Cryptographic identifiers, authentication, claims / attestations | DID Core; Verifiable Credentials (VC) Data Model 2.0; WebAuthn; OpenID Connect | **REUSE candidate:** distinct pieces for identifier syntax/resolution, signed claims, web login, and federation with an identity provider. | They solve different layers. DID methods vary; VCs do not define their transport; WebAuthn is relying-party scoped; OIDC depends on an issuer/identity provider. None supplies a universal trust policy. |
| Rights, permissions, duties, policy expressions | W3C ODRL 2.2; ValueFlows Agreement/Commitment and action vocabulary | **REUSE candidate:** ODRL for explicit policy permissions, prohibitions, duties, parties, assets, and constraints; ValueFlows for economic promises and observed flows. A profile is only a candidate if interoperability tests show a shared mapping is needed. | ODRL does not enforce real-world conduct or establish legal validity. The initial Three Neighbors mapping finds existing standards can express the baseline temporary-use case; cross-standard links and lifecycle semantics remain unsettled. |
| Data shape, geography, time | JSON Schema 2020-12; GeoJSON (RFC 7946); iCalendar (RFC 5545 and extensions) | **REUSE candidate:** format validation and established geographic/calendar interchange. **PROFILE candidate:** shared property meaning/units/availability semantics, if necessary. | Syntax validation is not shared domain meaning. Calendar busy/free times do not inherently mean an offer, permission, or commitment. Location sharing has privacy implications. |
| User-controlled data storage and application access | Solid Protocol; ActivityPods | **REUSE candidate:** Solid for web-based, permissioned access to data in Pods if that storage model is desired. | Solid Protocol remains a Community Group Report/draft in the source checked, with implementation interoperability evolving. It is not an offline synchronization or coordination domain model by itself. |
| Content-addressed storage / distributed application runtime | IPFS; Holochain | **UNKNOWN / MORE RESEARCH:** no present scenario requires either. | IPFS addresses/transfers content but persistence requires pinning/hosting; data/network are public by default. Holochain supplies an app framework and validation/DHT model with substantial architecture coupling. |
| Commerce discovery / transaction messaging | Beckn Protocol | **UNKNOWN / MORE RESEARCH:** relevant prior art for buyer/seller discovery and transaction flows; scope and licensing require careful review before adoption. | Its published “Code of sharing” applies CC BY-NC-SA 4.0 to protocol materials, a material reuse constraint for broadly reusable infrastructure. Commerce is only one application shape. |
| Payments / settlement | SEPA schemes and payment APIs | **UNKNOWN / MORE RESEARCH:** defer until a scenario requires settlement. | SEPA is a family of regulated payment schemes and bank infrastructure, not a generic decentralized accounting or agreement layer. Jurisdiction and provider dependencies matter. |

No **INVENT** decision is justified. No project-wide **PROFILE** or **REUSE** decision is accepted by this survey. The strongest immediate finding is that several proposed primitives substantially overlap existing vocabularies and should not be recreated from their names alone.

## Gaps to test (not established gaps)

The evidence points to questions at the intersections of existing systems, not yet to a missing base protocol:

- **Resource-use agreement composition:** initial mapping finds ValueFlows can represent the non-consumptive use flow, availability/time bounds, promises, custody transfers, and observed events; ODRL can express a permission and constrained duties over a physical asset. Existing standards can represent the baseline scenario, but a deterministic cross-standard mapping, care/remedy terms, and early termination semantics remain unresolved. No genuine gap or required profile is established.
- **Private, local discovery:** Murmurations supports public profile discovery; Matrix supports federated room events. Neither finding proves a need for a new discovery system. Test whether an application can keep household inventory and needs private while selectively sharing them and working through intermittent connectivity.
- **Decision authority and offline concurrency:** existing event/storage systems distribute and synchronize data, but their transport-level event authorization is not a generic agreement or human decision rule. Test whether any concrete scenario requires cross-transport semantics for proposals, consent, amendments, revocation, or concurrent offline changes.
- **Identity recovery across contexts:** DID, VC, WebAuthn, and OIDC address distinct layers. Recovery, key rotation, and cross-issuer trust for a local group remain open questions, but are not evidence for inventing an identity mechanism.

These are investigation targets only. A gap becomes an INVENT candidate only after a scenario demonstrates a required behavior, existing standards are shown inadequate, and profiling/composition is insufficient.

## Findings by area

### 1. Resource, need, agreement, decision, and accounting concepts

**ValueFlows is the strongest semantic prior art found for the current candidate primitives.** Its technology-agnostic RDF vocabulary covers Agents, Economic Resources and Resource Specifications, Intents, Commitments, Agreements, Proposals, Plans, Processes, and Economic Events. Intents can represent potential future offers or requests; Commitments represent promises; proposals group related intents; Agreements relate commitments. Economic Events describe observed resource flows. Its `use` action specifically describes non-consumptive use: the resource remains after use and may be unavailable while in use. `transferCustody` models physical custody/control transfer without itself transferring rights. Time fields, commitments, and resource accountability add relevant detail. This substantially overlaps the bootstrap candidates Entity/Relationship, Resource, Need/Capability, Agreement, Proposal, Event, and Accounting; the exact mappings need care (for example, ValueFlows Agent is not a cryptographic identity, and an Intent is not necessarily a CoordMesh “Need”).

The vocabulary is broad and layered (knowledge, plan, observation), intentionally extensible, and not itself a transport, trust framework, or general-purpose federation protocol. A small application may use only a subset. The Three Neighbors mapping found it adequate for a basic use-flow/resource/commitment/event model, while ODRL supplies explicit policy permissions and duties. A shared profile is not yet evidenced as necessary; whether a narrow mapping improves interoperability remains open.

ValueFlows is community-developed rather than a W3C Recommendation or IETF RFC. Its official specification describes the RDF source as the system of record. The former GitHub repository redirects contributors to the canonical Codeberg project and identifies documentation licensing as CC BY-SA 4.0; canonical governance, activity, and exact licenses for vocabulary/data artifacts should be confirmed directly before implementation. ValueFlows describes the vocabulary as building on decades of academic work and field implementations, while noting known and unknown edge cases and ongoing evolution. An implementations page lists software using the vocabulary. This is evidence of practical use, not proof of independent conformance or stable coverage for every concept.

**Credit Commons is narrower prior art:** its protocol connects independently controlled mutual-credit ledgers recursively. Its own project site calls the current implementation a proof of concept and explicitly says it is not secure to normal financial software standards. That warning rules it out as a financial implementation choice on present evidence, but its accounting model is relevant if CoordMesh later needs interoperable mutual-credit accounting. It is not a reason to add currency or accounting to the Three Neighbors scenario.

**Beckn** defines open-network commerce messaging and domain-specific specification layers. It is relevant to discovery and transaction messaging, but the protocol’s own sharing terms state CC BY-NC-SA 4.0 for the published knowledge materials. Its non-commercial restriction is incompatible with assuming unrestricted reuse for infrastructure intended for any application. Treat as comparative prior art unless license review identifies an applicable alternative; do not copy its materials into CoordMesh.

### 2. Event transport, federation, and synchronization

**Matrix.** The Matrix specification describes federated homeservers, rooms, extensible message and state events, event graphs, synchronization, and optional end-to-end encryption. The client-server API supports lightweight clients that load from the server and heavyweight clients that maintain persistent local state. This makes Matrix a credible transport/event candidate for a connected group and makes it relevant to recovery after partial server/network loss. It does not promise an application works offline: client behavior, cached data, ability to submit events, federation reachability, and conflict handling still matter. Matrix room state resolution and event authorization are Matrix rules, not human agreement semantics. End-to-end encryption is optional and does not hide all metadata or decide what a participant should trust.

The Matrix specification is licensed Apache-2.0. Evolution uses a public Matrix Spec Change process and a Spec Core Team under the Matrix.org Foundation, a UK Community Interest Company. Synapse is an established open-source homeserver maintained by Element and offered under AGPL-3.0-or-later or a commercial license; this illustrates why transport-spec reuse and implementation-license choice must be assessed separately. Other homeservers exist with different maturity and licenses. Server operations have real resource, administration, domain, abuse, and federation dependencies. **Disposition:** REUSE candidate for event synchronization/federation; PROFILE candidate only for an app’s domain event types and mapping to room membership/power levels. Keep the domain model independent, as Proposed ADR 0003 says.

**ActivityPub / ActivityStreams.** ActivityPub is a W3C Recommendation for client-server and server-server federation built around Actors, Activities, Objects, inboxes, and outboxes. Servers deliver activities to target actors by resolving inboxes and posting activities. This is a natural fit for actor-addressed publication and delivery, and useful prior art for announcements, offers, or notifications. It is a different model from Matrix’s replicated shared room state: an ActivityPub delivery does not itself make every participant hold a shared authoritative state, settle conflicts, or express group decision authority. The Recommendation is mature, but interoperability and deployed behavior vary across services and extensions. **Disposition:** REUSE candidate for actor/activity exchange where its delivery model fits; PROFILE candidate for shared coordination vocabulary and security expectations only after a scenario demonstrates the need.

**Git** provides distributed version control: content-addressed objects and histories can be cloned and exchanged, including offline work followed by synchronization. This is excellent for source artifacts, specifications, and reviewable proposals (including this project’s own work), not a generic current-state store for resource availability, expiring needs, personal access rights, or real-time coordination. Merge conflicts and forge workflow are not consensus about real-world decisions. **Disposition:** REUSE directly for source history; not a CoordMesh runtime dependency based on current scenarios.

### 3. Identity, authentication, and claims

These technologies must not be conflated:

- **DID Core 1.0** (W3C Recommendation) defines DID syntax, a data model, verification methods, and resolution operations. A DID is method-dependent: creation, control, resolution, and supporting infrastructure are determined in part by the DID method. DID Core does not establish that identifiers are person-bound, persistent forever, private, or accepted by a counterparty. **REUSE candidate** for interoperable identifier representation only if a use case benefits from it; no custom DID method is justified.
- **Verifiable Credentials Data Model 2.0** is a W3C Recommendation defining issuer, holder, verifier, credentials, presentations, and claims. It deliberately does not define a single credential transfer protocol or universal issuer trust. Verifiers still need policy to decide whether an issuer, proof, subject, and claim are suitable for a use. It is a strong **REUSE candidate** for contextual claims such as membership or resource access when credential exchange is useful, not a required identity layer. VC 2.1 was a Working Draft dated 2026-09-30 when checked; this survey relies on stable 2.0 unless a future task intentionally evaluates the draft.
- **WebAuthn Level 3** became a W3C Recommendation on 2026-08-25. It lets a web relying party authenticate through public-key credentials scoped to that relying party. It is a **REUSE candidate** for web sign-in and phishing-resistant authenticator ceremonies, not portable identity across unrelated relying parties, organizational claims, or social trust.
- **OpenID Connect Core 1.0** defines authentication on top of OAuth 2.0 and conveys End-User claims. It is mature and widely deployed for login/federated identity-provider use. It is a **REUSE candidate** for web application authentication when relying on an identity provider is acceptable; that is a deployment choice and not a CoordMesh-wide authority.

Cryptographic key continuity, authentication to a service, and third-party claims about a participant are distinct capabilities. No universal score or central issuer follows from these standards. **UNKNOWN:** a concrete recovery, pairwise identity, key rotation, issuer policy, and privacy model for offline local groups has not been chosen or demonstrated as missing.

### 4. Rights, permissions, agreements, and duties

**ODRL 2.2** is a W3C Recommendation defining an information model and vocabulary for policies: Permissions, Prohibitions, Duties/Obligations, parties, assets, constraints, and policy types including Agreement. Assets may be physical artifacts. Its core `use` action and date/time constraints are relevant to temporary access. A policy document cannot by itself enforce a physical-world promise, determine whether consent was valid, or adjudicate a disagreement. Standard vocabularies for actions and constraints are essential to interoperability. **REUSE candidate** for policy representation; a **PROFILE candidate** only if a concrete scenario requires shared action/asset/constraint terms.

### Three Neighbors result: refine, do not decide architecture

The [scenario mapping](../scenarios/three-neighbors/README.md#initial-valueflows-and-odrl-mapping) refines the earlier open hypothesis. ValueFlows alone can describe offers/requests, matching inputs, a non-consumptive use flow, temporal bounds, commitments, custody transfers, and observed flows. It does not clearly give those commitments the separate, explicit policy semantics for permitted/prohibited use and constrained duties that ODRL defines. ODRL alone does not provide ValueFlows' resource/economic flow model or event history. Composing them represents the baseline temporary drill-use arrangement without inventing a CoordMesh primitive. Their shared identifiers and action/duty mappings are not standardized by this research, so **PROFILE remains conditional**, not a decision. The reviewed ODRL core and ValueFlows vocabulary also leave early-termination procedures, assent evidence, detailed condition/remedy semantics, and legal effect unresolved. These are not established protocol gaps because requirements and possible complementary standards have not been exhausted. No accepted ADR or architecture decision changes.

### 5. Discovery, structured data, geography, and time

**Murmurations** defines profile schemas and a distributed data-sharing/discovery pattern. A profile describes a person, project, organization, event, or other node; schemas use JSON Schema and shared field libraries; nodes may host their own profile over HTTP while index services track profile locations for aggregators. The project documents multiple index operation and synchronization patterns and presents an open source tool ecosystem. This is useful prior art for discovering public organizations/resources/capabilities and reusing common fields. Index availability and freshness remain deployment properties; profiles submitted to open indexes are public data and are inappropriate for private household inventories without a separate access design. It is a project protocol, not a standards-body Recommendation; governance and license for each software/service and schema artifact need direct review. **REUSE candidate** for public directory/discovery integrations, not a universal entity model.

**JSON Schema 2020-12** is the current released JSON Schema specification checked. It validates JSON document structure and constraints, not shared meaning or protocol behavior. Reuse it for schemas if JSON is selected; profile terminology remains a separate concern.

**GeoJSON (RFC 7946)** is an IETF Standards Track geospatial data interchange format. It can represent points, polygons, and other geographic feature data; it does not provide access-controlled discovery or privacy rules. **iCalendar (RFC 5545)** and extensions represent calendar components and scheduling data. They may carry event times or availability inputs but do not alone describe resource inventory, rights, an offer, or a commitment. These are **REUSE candidates** for specific interchange needs; semantic mappings, granularity, time zones, and privacy need scenario-level treatment.

### 6. Storage, local operation, and execution platforms

**Solid Protocol** specifies interoperable HTTP interactions for clients and servers managing data in Pods, with web identifiers, authentication, authorization, data formats, notifications, and query interfaces. The protocol inspected is a W3C Community Group Report/draft rather than a W3C Recommendation. ActivityPods is an open-source application framework combining ActivityPub-compatible apps with Solid Pods, but its own conformance page says it does not yet support all defined Solid standards. Solid is a **REUSE candidate** if personal data custody and permissioned app access becomes a requirement. Its maturity and cross-implementation conformance should be evaluated for any intended feature; it does not itself provide a generic peer-to-peer event log or guarantee offline operation.

**IPFS** provides content addressing, routing, and transfer over peer-to-peer networks. A content identifier verifies/addresses bytes, but does not imply data will remain available: persistence depends on a node retaining/pinning the content or another persistence service. Network routing and content identifiers can be public; encryption and access control are application responsibilities. It is **UNKNOWN / MORE RESEARCH** because no current CoordMesh requirement calls for content-addressed storage.

**Holochain** is a framework/runtime for agent source chains, application-defined validation, and a DHT that distributes public entries and validation among peers. Its local-first model may permit local writes and queued synchronization in particular app architectures. This is a substantial application architecture rather than an interchange standard; app code, validation rules, and network availability are dependencies. It is **UNKNOWN / MORE RESEARCH**, not an assumed base layer.

### 7. Early candidate review and exclusions

- **PLANET / The Open Co-op:** PLANET has been described as a collaborative effort or “open source operating system” for regenerative collaboration, with the 2026 project update pointing to the First Person Project stack. Available material does not establish one stable normative protocol covering the CoordMesh candidates. Track its component standards and specifications independently; **UNKNOWN / MORE RESEARCH** for PLANET as a protocol dependency.
- **Openmesh:** the name is ambiguous across unrelated projects and no canonical specification was established in this pass. Remove it from the active shortlist until a precise project URL and capability are identified.
- **SEPA / payment infrastructure:** defer analysis until an application scenario needs settlement. Existing bank payment schemes are external institutional infrastructure that could be integrated through adapters; they are neither generic accounting nor a decentralized coordination substrate.
- **Universal “trust” or reputation:** none of the reviewed candidates justifies a global person score. Prefer issuer/context-specific claims and verifier policy, consistent with CoordMesh principles.

## Three Neighbors: standards test points (not requirements)

| Scenario question | Existing candidate / finding | Remaining uncertainty |
| --- | --- | --- |
| Alice describes her drill as available; Bob requests short-term access | ValueFlows ResourceSpecification/EconomicResource and `use` Intents/Proposals express resource, offer, request, and non-consumptive use. | Private discovery, condition, location granularity, and matching behavior. |
| Alice and Bob record temporary-use terms | ValueFlows Agreement/Commitment plus ODRL Agreement/Policy can express promises, policy permission/duties, and fixed time bounds. | Cross-standard mappings, detailed care/remedy conditions, assent/evidence, early termination, and disputes. No profile is yet established as necessary. |
| Alice, Bob, and Carol express a shared mower need | Separate ValueFlows request Intents/Proposals can represent each participant without presuming a legal organization. | How an application recognizes a shared need and what decision rule participants choose. |
| They later propose and manage joint acquisition | ValueFlows Proposal/Commitment/EconomicEvent can describe a proposal, planned flows, and observed purchase/resource flows. | Human authorization, legal ownership, custody, cost allocation, liability, and legal consequences remain application questions. |
| Useful match discovery | ValueFlows provides structured intents/proposals and relationships; app query/matching may operate over disclosed data; AI may assist. | Ranking, privacy, and authorization are not dictated by the vocabulary. A match suggestion is not consent or a decision. |

## Candidate next research questions

1. Evaluate cross-implementation ValueFlows use of `use`, `transferCustody`, time bounds, and intent-to-commitment mappings; confirm current canonical governance and per-artifact licensing before relying on artifacts.
2. Test whether ODRL asset/party/action identifiers can be linked reproducibly to ValueFlows resources/agents/commitments/events; profile only if an interoperability test demonstrates ambiguity.
3. Clarify whether the scenario requires early termination, condition/remedy, evidence of assent, or any legal effect; research complementary standards only for requirements participants actually adopt.
4. Test public discovery (Murmurations/ActivityPub/Matrix) separately from private household state and access-controlled data.
5. Evaluate specific Matrix and ActivityPub implementations and conformance behavior, including ordinary online operation, offline reads/writes, reconnection, and event authorization.
6. Seek a concrete scenario before researching payment, distributed storage, blockchain-like or app-runtime dependencies further.

## Primary-source references

### Economic coordination and commerce

- [ValueFlows specification overview](https://www.valueflo.ws/specification/spec-overview/) and [formatted vocabulary](https://www.valueflo.ws/specification/all_vf/) — ontology scope, source-of-record description, concepts.
- [ValueFlows flows and intents](https://www.valueflo.ws/concepts/flows/) and [offers and requests](https://www.valueflo.ws/concepts/proposals/) — Intent, Commitment, Proposal semantics.
- [ValueFlows actions](https://www.valueflo.ws/concepts/actions/) — non-consumptive `use` and custody-transfer semantics.
- [ValueFlows status](https://www.valueflo.ws/introduction/status/) and [implementations](https://www.valueflo.ws/appendix/usedfor/) — field history, known evolution, and applications/libraries using the vocabulary.
- [ValueFlows GitHub mirror](https://github.com/valueflows/valueflows) — repository move notice, source-of-record and documentation license notice; canonical repository is [Codeberg](https://codeberg.org/valueflows/valueflows).
- [PLANET overview](https://open.coop/planet/) and [2026 PLANET/Open Co-op update](https://open.coop/2026/06/26/update-on-planet-and-the-open-co-op/).
- [Beckn protocol sharing terms](https://becknprotocol.io/sharing/) and [community/governance](https://becknprotocol.io/community/).
- [Credit Commons Protocol](https://creditcommons.org/) — scope, open API, implementation status, and stated security limitations.

### Federation and synchronization

- [Matrix Specification](https://spec.matrix.org/latest/) — architecture, federation, extensible events, encryption module, APIs, license.
- [Matrix client-server API](https://spec.matrix.org/v1.19/client-server-api/) — persistent local client state option and synchronization behavior.
- [Matrix governance](https://matrix.org/foundation/about/) and [Spec Change process](https://spec.matrix.org/proposals/).
- [Matrix rooms and events](https://matrix.org/docs/matrix-concepts/rooms_and_events/) — per-room homeserver replicas and synchronization.
- [Synapse source repository](https://github.com/element-hq/synapse) — an implementation example and its AGPL/commercial licensing terms.
- [W3C ActivityPub Recommendation](https://www.w3.org/TR/activitypub/) and [ActivityStreams 2.0](https://www.w3.org/TR/activitystreams-core/).
- [Git data model](https://git-scm.com/docs/gitdatamodel) and [Git user manual](https://git-scm.com/docs/user-manual).

### Identity, claims, policy, and serialization

- [DID Core 1.0](https://www.w3.org/TR/did-core/).
- [Verifiable Credentials Data Model 2.0](https://www.w3.org/TR/2025/REC-vc-data-model-2.0-20250515/) and [Data Model 2.1 Working Draft](https://www.w3.org/TR/2026/WD-vc-data-model-2.1-20260930/).
- [Web Authentication Level 3](https://www.w3.org/TR/webauthn-3/) and [W3C publication history](https://www.w3.org/standards/history/webauthn-3/).
- [OpenID Connect Core 1.0, second errata](https://openid.net/specs/openid-connect-core-1_0-errata2.html).
- [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/) and [ODRL Vocabulary & Expression](https://www.w3.org/TR/odrl-vocab/).
- [JSON Schema specification](https://json-schema.org/specification) and [2020-12 release](https://json-schema.org/draft/2020-12/).
- [GeoJSON RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946); [iCalendar RFC 5545](https://datatracker.ietf.org/doc/html/rfc5545); [iCalendar availability RFC 7953](https://datatracker.ietf.org/doc/html/rfc7953).

### Discovery, storage, and local-first systems

- [Murmurations protocol and developer documentation](https://murmurations.network/developers/), [common terms](https://docs.murmurations.network/about/common-terms), and [schema guidance](https://docs.murmurations.network/guides/create-a-schema).
- [Solid Protocol technical report](https://solidproject.org/TR/2024/protocol-20240512) and [Solid Community Group](https://www.w3.org/groups/cg/solid/).
- [ActivityPods](https://activitypods.org/) and its [Solid conformance status](https://activitypods.org/specs/solid).
- [IPFS content addressing](https://docs.ipfs.tech/concepts/content-addressing/), [persistence](https://docs.ipfs.tech/concepts/persistence/), and [privacy/encryption](https://docs.ipfs.tech/concepts/privacy-and-encryption/).
- [Holochain DHT](https://developer.holochain.org/concepts/4_dht/), [data validation](https://developer.holochain.org/concepts/7_validation/), and [working with data](https://developer.holochain.org/build/working-with-data/).
