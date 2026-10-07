# Three Neighbors

Status: exploratory scenario, refined by the initial standards survey on 2026-10-07. This is a test of future specifications, not a protocol requirement or complete design.

Alice, Bob, and Carol represent three neighboring households. Alice has a drill and a trailer. Bob needs temporary access to a drill. All three households need a lawn mower.

The scenario asks whether future infrastructure can support:

1. Alice describing an available resource.
2. Bob describing a need.
3. Discovery of a useful match.
4. Alice and Bob establishing an agreement that governs temporary use.
5. The three participants describing a shared need.
6. A future extension for proposing and managing a jointly acquired resource.

Do not infer a particular identity model, matching algorithm, institution, payment, governance mechanism, or data schema from this example. The participants remain authoritative for consequential decisions unless they explicitly delegate narrowly defined authority. AI may suggest matches and alternatives.

Use the scenario to test existing standards first and identify the smallest actual gap. Refine it after research.

## Initial ValueFlows and ODRL mapping

This mapping is a research result, not an adopted CoordMesh profile or protocol design. It uses the current ValueFlows vocabulary and ODRL 2.2. “Covered” means the standard defines a relevant representation; it does not establish legal validity, consent, enforcement, application behavior, or conformance between implementations.

### Participants, resources, and discovery

| Scenario semantic | Existing representation | Classification | Boundary / evidence |
| --- | --- | --- | --- |
| Alice, Bob, and Carol act as participants | ValueFlows `Agent` (with `Person` available for persons); ODRL `assigner` and `assignee` parties can identify policy roles | **covered through an existing standard composition** | A stable cross-standard identifier can link the parties, but ValueFlows does not define cryptographic identity or prove that an agent controls a key. Identity and claims remain separate questions. |
| Alice's drill and trailer are distinct physical items, with a kind/type and possibly a location | ValueFlows `ResourceSpecification` describes a kind; `EconomicResource` describes an actual resource, with quantity, location, and accountability properties | **covered directly** | `primaryAccountable` describes primary rights/responsibilities and is sometimes thought of as ownership; it should not be silently equated with legal title. |
| Alice offers the drill for temporary use; Bob requests use | ValueFlows `Intent` with the `use` action, published through a `Proposal` with offer/request purpose; `availableQuantity` can express available amount | **covered directly** | `use` describes a non-consumptive flow: the tool exists after use and may be unavailable while in use. Sharing visibility and private household discovery are not settled by this vocabulary. |
| Bob's request is matched with Alice's offer | ValueFlows intents can be matched and related to a `Commitment`; `satisfies` relates a commitment to an intent | **covered directly** | The vocabulary supplies the coordination concepts, not a required matching algorithm, ranking, disclosure policy, or consent decision. Those remain **unresolved**. |

### Temporary drill use

| Required semantic | ValueFlows representation | ODRL representation / composition | Classification and result |
| --- | --- | --- | --- |
| Promise that Bob may use Alice's drill | An `Agreement` can group reciprocal commitments; a `Commitment` is a planned/promised economic flow between agents and can use the `use` action | An ODRL `Agreement` policy can name parties, target an asset, and state a `Permission` for an action | **covered through an existing standard composition** for the explicit policy-right plus economic-promise reading. ValueFlows alone can represent an agreed planned use flow, but the reviewed vocabulary does not clearly define that commitment as an independently machine-interpretable authorization or permission rule. |
| Specify exactly which drill and which Bob | Link the ValueFlows `EconomicResource` and agents to ODRL's target asset and parties | ODRL assets may be physical artifacts; `assigner`/`assignee` identify policy parties | **covered through an existing standard composition** at the conceptual level; the cross-standard identifier and mapping convention are **unresolved**. |
| Limit use to a stated time window | ValueFlows `hasBeginning` / `hasEnd` can bound intents and commitments; the `use` action may make the resource unavailable during the process | ODRL constraints include date/time operands that can constrain a permission | **covered directly** in either vocabulary for a fixed interval. A profile is not shown to be necessary for this basic meaning. Time zones, precision, and conflicting updates still need application choices. |
| Set place, permitted purpose, or other conditions | ValueFlows can state flow/process context and resource location, but this does not by itself define every access condition | ODRL constraints can express conditions when the operand and comparison semantics are defined | **unresolved**; a CoordMesh profile is only a candidate if applications need shared, machine-interpretable terms. Generic ODRL extensibility does not make an undefined term interoperable. |
| Bob returns the drill / physical custody goes back to Alice | ValueFlows `transferCustody` models a physical custody/control transfer without itself transferring rights; an `EconomicEvent` can record the observed transfer | ODRL can express a duty, but its core action vocabulary does not define a specific “return this physical item to its prior custodian” action | **covered through an existing standard composition**: ValueFlows can model the custody transfer/commitment, while ODRL can express the obligation in policy terms. A standard mapping between them is **unresolved**. |
| Care for the drill, return it undamaged, or address loss/damage | ValueFlows can record economic events and resource changes; ODRL has duties and constraints | The precise condition, evidence, responsibility, and remedy require shared terms and rules beyond the generic classes | **unresolved**. A profile or application agreement may be appropriate if a concrete interoperable use case specifies these terms. The evidence does not establish a genuine protocol gap. |
| Record handover, use, return, and completion | ValueFlows `EconomicEvent` records an observed flow; `finished` and temporal properties can indicate a completed commitment/process | ODRL expresses policy, not the event history that proves a physical handover occurred | **covered through an existing standard composition**: use ValueFlows for planned/observed flows and ODRL for terms. A record is not proof that the real-world event happened as described. |
| End access at the scheduled end | ValueFlows time bounds and ODRL date constraints express a planned expiration | Both can describe the fixed end of the permission/flow | **covered directly** for scheduled expiry. |
| End early, extend, revoke, or handle notice/consent | ValueFlows `finished` marks a commitment/process as finished, and temporal end fields describe an end time; the reviewed vocabulary does not define who may terminate early or under what process | The reviewed ODRL 2.2 information model and core vocabulary do not define a lifecycle workflow for terminating/revoking an existing agreement or permission | **unresolved**. This is not classified as a genuine gap: the scenario has not established a required termination workflow, and other contract/lifecycle mechanisms have not been exhaustively surveyed. |
| Decide whether to accept the match or terms | Neither vocabulary transfers decision authority to software | Policies and commitments can record terms, not prove informed human assent or signature | **unresolved**. The scenario's human-authority principle still applies; signature, evidence, and legal effect need separate research if required. |

**Answer to “ValueFlows alone?”** ValueFlows alone can express the participants/resources, offer and request intents, a non-consumptive use flow, its planned time bounds, reciprocal commitments, custody-transfer promises/events, and event records. For this scenario's thin operational model, it is substantial prior art and no new CoordMesh primitive is indicated. However, ValueFlows alone does not clearly provide the separate machine-readable permission semantics and constrained duties asked for here, nor an early-termination procedure. ODRL can express permissions, prohibitions, duties, parties, assets, and time constraints; composing it with ValueFlows gives a plausible representation of the baseline temporary-use arrangement. No CoordMesh profile is yet required by demonstrated evidence. If independent implementations need deterministic links between ODRL assets/parties/permissions and ValueFlows resources/agents/commitments/events, a narrow profile may become useful and should first be tested with examples.

### Shared mower need and possible acquisition

| Scenario semantic | ValueFlows mapping | Classification | Boundary / evidence |
| --- | --- | --- | --- |
| Alice, Bob, and Carol each need a mower | Each agent can publish a `use` or acquisition `Intent` in a request `Proposal`; three separate intents avoid presuming a new collective agent | **covered directly** | Whether one shared need is a group statement, three compatible needs, or a delegated representative is an application choice, not resolved by this scenario. |
| Discover that the needs overlap and assess a shared option | Intents and proposals provide structured inputs; a later proposal/commitment can relate to intents | **covered directly** for the inputs; matching and group decision rules are **unresolved** | No voting, governance, purchasing authority, or mandatory collective entity follows from the model. |
| Propose a jointly acquired mower and later record purchase/custody | Proposals, reciprocal commitments, and economic events can describe planned and observed flows; a resource can have accountability and location | **covered through an existing standard composition** | Cost allocation, legal ownership, shared access rights, maintenance, liability, and decision authority are not automatically supplied by these classes. They remain **unresolved** application semantics. |

### Research refinement

The initial landscape treated the drill mapping and the boundary between ValueFlows commitments and ODRL policy as open. Primary specifications refine that hypothesis: the baseline scenario is representable by existing standards, with ValueFlows especially strong for economic/resource flows and ODRL for explicit policy permissions and duties. There is no evidence here for an **INVENT** decision. This does not accept ValueFlows, ODRL, a profile, or any architecture as a CoordMesh dependency. The concrete remaining question is whether implementations need a shared cross-standard mapping, particularly for physical return, condition/remedies, and early termination. No accepted ADR or architecture decision is changed by this research.

### Primary sources for this mapping

- [ValueFlows formatted vocabulary](https://www.valueflo.ws/specification/all_vf/) — normative vocabulary descriptions for Agent, Agreement, Commitment, EconomicEvent, EconomicResource, Intent, Proposal, ResourceSpecification, accountability, and time fields.
- [ValueFlows actions](https://www.valueflo.ws/concepts/actions/) — `use` describes non-consumptive use and temporary unavailability; `transferCustody` transfers physical custody without rights.
- [ValueFlows flows and intents](https://www.valueflo.ws/concepts/flows/) and [offers and requests](https://www.valueflo.ws/concepts/proposals/) — planned, promised, observed flows; proposal and intent relationships.
- [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/) and [ODRL Vocabulary & Expression](https://www.w3.org/TR/odrl-vocab/) — policy types, parties/assets, permissions, prohibitions, duties, constraints, and core actions.
