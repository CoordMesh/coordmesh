# Candidate architecture: composition and conformance

**Status:** research synthesis; candidate architecture, not a normative
specification or accepted project-wide decision. Prepared 2026-10-07 from the
landscape survey, Three Neighbors scenario and mapping, implementation review,
and disposable interoperability experiment. See [architecture hypotheses](architecture.md)
and the linked evidence below. The proposed ADRs remain proposals.

## What is CoordMesh?

CoordMesh is an open project for making existing coordination infrastructure
work together across applications. Its leading candidate role is a
**composition and conformance layer**: identify suitable standards for each
capability, document how they can be used together, and publish focused
conformance scenarios where interoperability needs shared behavior. It may
eventually maintain narrow profiles and reference integrations when concrete
exchange tests demonstrate a need. The current evidence does not justify a
new domain protocol, a universal data model, or a mandated technology stack.

This describes the evidence-backed candidate direction. It does not select
ValueFlows, ODRL, Matrix, or any identity technology as a required dependency.

## Evaluate the candidate forms

| Candidate form | Evidence for it | Evidence against / boundary | Current assessment |
| --- | --- | --- | --- |
| **A. New protocol** | The interoperability experiment exposes different local IDs and a missing Event → Commitment `fulfills` relation in the inspected Bonfire model. Some capabilities require mapping across systems. | ValueFlows already covers the tested resource, intent, commitment, action, time, and event semantics; ODRL covers explicit policy terms. The Bonfire finding is implementation-specific and runtime interchange was not tested. There is no demonstrated semantic gap requiring new wire rules or primitives. | **Not justified now.** A downstream gap must survive native standards, composition, and adapter approaches before protocol work. |
| **B. Profile over existing standards** | ValueFlows plus ODRL offer a plausible composition for temporary use; stable identity references and policy/resource linking could need shared conventions. Matrix or ActivityPub may need application event mappings. | No cross-system runtime test has shown a convention that existing standards cannot express or an adapter cannot supply. Inventing a profile now would risk codifying one implementation's model or application policy. | **Candidate only.** Profile only a demonstrated, shared interoperability requirement. |
| **C. Composition / conformance layer** | Existing standards cover most demonstrated semantics. Research shows important boundaries between domain meaning, identity, policy, and transport. The source-based experiment identified a specific implementation mismatch suitable for an adapter/conformance test. | Does not itself ensure products implement or adopt the mappings; conformance scope and governance will need to be earned. | **Best-supported primary role.** Begin with research, explicit mappings, reusable scenarios, and independent conformance artifacts. |
| **D. Reference integration stack** | The hREA/Bonfire experiment shows that concrete mappings can test whether concepts survive different models. A small adapter or deployment can validate composition choices. | Full runtimes are costly; no deployment is needed to define the project. A reference stack could accidentally become the implicit specification or privilege a transport. | **Supporting tool, not project identity.** Build only a minimal disposable or optional integration when it answers a precise research question; publish its limits. |
| **E. Combination** | A composition/conformance core can publish a narrow profile if needed and use optional reference integrations to test it. | Combining all forms prematurely would grow a protocol and stack before an interoperability requirement exists. | **Justified combination:** C as the core role; selectively B and D when evidence triggers them. A remains out of scope absent a demonstrated gap. |

## Capability map

These are current dispositions for the capabilities examined so far, not
accepted dependencies. **REUSE** refers to an existing capability candidate,
not a project-wide adoption decision. **PROFILE candidate** names a possible
future constraint or mapping, not an approved profile. **COMPOSE** means
combine existing capabilities with explicit links. No item currently meets
the evidence threshold for **INVENT**.

| Capability | Current state | Existing standards/projects and evidence | Boundary / unresolved point |
| --- | --- | --- | --- |
| Participant / agent representation | **REUSE** | ValueFlows `Agent` | Agent records do not prove key control or identify a human by themselves. Cross-system IDs and person/organization claims remain open. |
| Resources | **REUSE** | ValueFlows `EconomicResource`, `ResourceSpecification` | Resource identity, accountability, type, quantity, and physical/legal rights must not be conflated. Local ID mappings need evidence. |
| Needs / offers / intents | **REUSE** | ValueFlows `Intent`, `Proposal` | The terms cover planned flows and offer/request patterns; discovery, audience, privacy, matching, and ranking are application behavior. |
| Commitments | **REUSE** | ValueFlows `Commitment`, `satisfies` / `satisfiedBy` | This represents planned/promised economic flows, not automatically machine-enforced authorization or consent. Implementation support differs. |
| Agreements | **REUSE** | ValueFlows `Agreement`; ODRL `Agreement` policy | The names serve different purposes: ValueFlows groups/relates commitments; ODRL expresses policy terms. Linking them is not standardized by the evidence reviewed. |
| Economic events | **REUSE** | ValueFlows `EconomicEvent`, `fulfills` | ValueFlows represents observed flows. The pinned Bonfire model lacked the event-to-commitment link; hREA exposed it. This is an implementation difference, not grounds to redefine event semantics. |
| Rights / duties / constraints | **COMPOSE** | ODRL 2.2 for permissions, prohibitions, duties, constraints; ValueFlows for flows, resources, and commitments | Baseline temporary use is representable across them conceptually. Stable party/resource links, legal effect, enforcement, lifecycle, and shared mappings are unresolved. |
| Authentication | **REUSE** | WebAuthn for relying-party authentication; OpenID Connect for identity-provider login/federation; DID methods may support decentralized identifiers | These solve different tasks. No universal identity/authentication method is selected or required. |
| Attestations / credentials | **REUSE** | W3C Verifiable Credentials Data Model 2.0; DID Core where a DID is useful | Issuer trust, status/revocation, presentation policy, and claims acceptable in a context remain application or ecosystem policy. No global reputation score. |
| Communication / federation | **REUSE** | Matrix for shared room/event synchronization; ActivityPub for actor-directed activity delivery | These are different transport/federation models. Neither defines CoordMesh domain agreement or consent. Selection is scenario-dependent; Matrix remains a hypothesis. |
| Discovery | **UNRESOLVED** | Murmurations supports public profile/directory discovery; ValueFlows Proposal/Intent gives structured inputs | Private/local discovery of sensitive household needs and resources is not solved by public indexing. No requirement for a new discovery protocol is evidenced. |
| Synchronization | **REUSE** | Matrix synchronization and room state; ActivityPub delivery; Git for source artifacts/history | Transport synchronization does not establish domain-level agreement, resolve every concurrent update, or prove offline operation. Scenario and platform behavior need evaluation. |
| Offline operation | **UNRESOLVED** | Git demonstrates offline history exchange for source artifacts; Matrix clients can maintain local state under some models | No end-user coordination scenario has established required offline writes, conflict semantics, or recovery behavior. Do not infer a general offline protocol from local caches. |
| Decision / consent | **APPLICATION POLICY** | ValueFlows/ODRL may record proposals, promises, policy terms, and parties; neither transfers authority to AI | Who decides, how assent is evidenced, delegation scope, quorum, veto, amendments, and revocation depend on affected participants and application context. |
| Accounting | **REUSE** | ValueFlows models economic events and resource flows; Credit Commons is prior art for nested mutual-credit ledgers | ValueFlows records flows but is not a universal ledger/settlement system. Credit Commons is specific to mutual credit; no payment or currency need is established. |
| Conformance | **COMPOSE** | ValueFlows vocabulary/JSON-LD and existing schemas; project principle of spec-first testing | No demonstrated hREA/Bonfire shared conformance suite or validated JSON-LD API exchange was found. CoordMesh may publish cross-standard scenario fixtures and mappings; a normative suite awaits a justified profile. |

No entry is classified **INVENT**. “Unresolved” is not evidence that a new
mechanism is needed. In particular, the inspected Bonfire `fulfills` omission
is a product/model limitation and should first be addressed or tested through
its own API/adapter/conformance path.

## Layer boundaries

### 1. Domain semantics

Use existing domain vocabularies such as ValueFlows for participants,
resources, intents, commitments, agreements, and observed economic flows.
CoordMesh should map and test selected subsets only when a scenario needs
interoperability. Do not make these semantics depend on Matrix rooms, GitHub
issues, or a specific database.

### 2. Transport and federation

Matrix, ActivityPub, or another system may carry or synchronize records.
Transport identifies how data is delivered and replicated; it does not decide
whether the record is valid consent, a fulfilled duty, or a human-approved
decision. Keep transports replaceable and compare them against actual
interaction requirements.

### 3. Identity and authentication

Authentication establishes that a key, device, account, or identity-provider
session is being used in a defined context. Credentials and attestations carry
claims made by issuers. Neither automatically establishes that a claim is
true, a person has a universal identity, or a participant agrees to a
transaction. Use established standards and contextual trust policy.

### 4. Policy and authorization

ODRL can express policy permissions, prohibitions, duties, and constraints;
systems still need to identify parties/assets and decide how policies are
interpreted and enforced. ValueFlows commitments describe economic promises.
Their mapping to access control, legal rights, or runtime authorization must
not be assumed. CoordMesh has no accepted authorization engine.

### 5. Application behavior

Matching, ranking, disclosure, scheduling, consent collection, decision
rules, cancellation, dispute handling, presentation, and user experience
belong to applications or explicitly scoped delegations unless future
evidence demonstrates a shared cross-application requirement. AI may assist;
affected participants retain authority by default.

### 6. CoordMesh-specific responsibilities

The candidate project can own the **interoperability work product**: capability
maps, evidence and uncertainty records, cross-standard mapping documentation,
small scenario fixtures, versioned profiles only when justified, and
independent conformance cases for those profiles. Optional reference adapters
can test a mapping but cannot silently define it. CoordMesh should specify as
little as possible and keep every profile replaceable by upstream standards
where they later meet the need.

## Smallest defensible core

At this stage the core is a project method and set of artifacts, not a runtime
protocol:

1. State a concrete coordination scenario and the required interoperable
semantics.
2. Map each requirement to existing standards and distinguish standard
semantics from product behavior and application policy.
3. Test a narrow exchange using primary specifications and independent
implementation evidence, including loss, identity mappings, and uncertainty.
4. If a shared behavior remains necessary, publish the narrowest profile and
   conformance examples that close that demonstrated gap.
5. Maintain optional adapters or a reference integration only where they
   validate the profile or reveal further evidence.

The first example is the Three Neighbors drill-use scenario. It shows the
ValueFlows semantic model is substantially reusable and that implementation
exchange details remain uneven. Its present model-based experiment is not a
conformance claim.

## What CoordMesh should not own

On current evidence, CoordMesh should not own:

- a replacement universal domain ontology or a new offer/resource/commitment
  system;
- a mandated transport, federation network, Matrix deployment, or
  GitHub-specific protocol;
- cryptography, a global identity authority, or mandatory state identity;
- a universal trust/reputation score, person ranking, or social credit;
- a universal policy engine, legal contract form, enforcement mechanism, or
  decision/voting process;
- payments, tokens, currencies, or a settlement ledger;
- institutions such as governments, companies, cooperatives, municipalities,
  or CommonCell as foundational entities;
- a required application, hosting stack, distributed database, blockchain,
  or microservice architecture.

These exclusions are evidence-bounded architectural guardrails, not claims
that applications cannot use such systems as adapters or participants.

## Open questions

- Can a real, reproducible adapter exchange preserve ValueFlows IDs and
  Event → Commitment `fulfills` across current hREA and Bonfire releases?
- Which ValueFlows artifacts and APIs are stable/released for independent
  implementations, and what exact versions can be exchanged?
- Is a shared ODRL-to-ValueFlows mapping required by more than one application,
  and which party/resource identifiers would it use?
- What private/local discovery and offline continuity behavior is actually
  required by a scenario, and which existing transports/storage systems can
  deliver it?
- Which identity and credential combinations fit local, organizational, and
  anonymous participation without creating a central authority?
- What does useful conformance evidence look like when the underlying
  standards are independently versioned and optional?
- Can any future profile be upstreamed to an existing standard instead of
  maintained by CoordMesh?

These questions do not imply that CoordMesh must answer all of them before it
can publish a narrowly scoped profile. They identify evidence that could
change the architecture.

## Research-phase exit criterion

The landscape/research phase may exit for a **specific first profile** only
when a documented scenario demonstrates all of the following:

1. Two or more independent participants or implementations need to exchange a
   named piece of coordination data or behavior.
2. The required semantics and authority boundary are precise enough to test,
   including identity references, time/units where relevant, privacy,
   consent, and error/unknown cases that affect interoperability.
3. A reproducible exchange or implementation-level experiment shows a
   concrete loss, ambiguity, unsupported mapping, or incompatibility at
   pinned standards and product versions.
4. Native standards, existing serialization, configuration, adapters, and
   application policy have each been evaluated; the problem cannot be
   addressed adequately by using them or upstreaming a correction.
5. The affected communities can review the proposed shared behavior, and an
   ADR records why CoordMesh should maintain it, the alternatives, ownership,
   versioning, and compatibility consequences.
6. A minimal fixture and conformance cases can distinguish conforming from
   non-conforming behavior independently of one reference implementation.

If the evidence points to a missing semantic mechanism that cannot be supplied
by a profile/composition, the same gate applies with an additional documented
gap analysis and a separate ADR proposal. Security/privacy review is required
where the mechanism changes those properties. No new protocol is justified
merely because implementations use different internal models.

This gate is not currently passed. The Bonfire `fulfills` difference is one
implementation-model observation, with no live exchange or cross-product
conformance proof. Continue targeted evidence work before normative profile or
protocol design.

## Evidence base

- [Open Coordination Infrastructure Landscape Survey](../standards/landscape.md)
- [Three Neighbors scenario and ValueFlows/ODRL mapping](../scenarios/three-neighbors/README.md)
- [ValueFlows implementation interoperability review](../standards/valueflows-implementation-interoperability.md)
- [Non-normative hREA/Bonfire model projection experiment](../experiments/valueflows-three-neighbors/README.md)
- [Project principles](principles.md), [architecture hypotheses](architecture.md),
  and proposed [ADR 0001](../adr/0001-spec-first-development.md),
  [ADR 0002](../adr/0002-reuse-profile-invent.md), and
  [ADR 0003](../adr/0003-matrix-transport-hypothesis.md)
