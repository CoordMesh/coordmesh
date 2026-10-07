# ValueFlows Implementation Interoperability Review

Status: research evidence, not a CoordMesh dependency or profile decision. Sources checked 2026-10-07. Source-level review only; no live hREA-to-Bonfire exchange was run.

## Scope and method

This review compares the published ValueFlows vocabulary with two open-source implementations that expose concrete code/API evidence:

- **hREA** — Holochain-based ValueFlows/REA building blocks with a JavaScript GraphQL adapter.
- **Bonfire ValueFlows extension** — relational/Bonfire implementation with an optional GraphQL API and ActivityPub federation.

The implementation links below point to their public repositories and reviewed source files. The hREA source is the `sprout` branch (the repository's default branch when checked); Bonfire source is `main`. These are mutable branches, not release-pinned snapshots. hREA's repository showed activity through 2026-10-07; this does not establish that every branch feature is released. Bonfire's README is older than parts of its current source and is not treated as a complete feature inventory.

“Portable” below means the two implementations appear to use the same ValueFlows semantic/property or canonical action identifier. It does not mean that a round-trip between the two has been demonstrated.

## Comparison

| Three Neighbors concern | ValueFlows vocabulary | hREA evidence | Bonfire evidence | Portability assessment |
| --- | --- | --- | --- | --- |
| `use` a drill without consuming it | Core `use` Action; intended as non-consumptive. A use flow may make a resource unavailable while it is in use. | Built-in `use` action uses no accounting/on-hand effect. API exposes Action and flow effort quantity. | Built-in Action id is `use`, with no resource/on-hand quantity effect; code describes the tool as existing after use. | **Semantics and action slug are portable in the inspected code.** Internal inventory effects and UI treatment are implementation behavior. |
| Hand over / return custody without transferring rights | Core `transfer-custody` Action has custody/control effects without full rights transfer. | Built-in `transfer_custody` maps to the `transfer-custody` ID, with on-hand transfer and no accounting effect. | Action registry includes `transfer-custody`, `noEffect` resource effect and `decrementIncrement` on-hand effect. | **Semantics and identifier align.** This records an economic flow; neither action by itself encodes consent, care, or a loan's legal terms. |
| Bound use by time | Intent, Commitment, and EconomicEvent have temporal fields such as `hasBeginning`, `hasEnd`, and/or `hasPointInTime`; use effort can also have a quantity/unit. | GraphQL API documents planned start/end on Intent and Commitment and beginning/end/point-in-time on EconomicEvent; Holochain records use timestamps. Current integrity code validates temporal consistency. | Models store the fields as `utc_datetime_usec`; Intent and Commitment models include beginning/end and point-in-time. Commitment query source still has a TODO for start/end filters. | **The field meanings are portable; the whole scheduling behavior is not demonstrated.** Scalar encoding/precision, filtering, conflict handling, and whether an interval actually reserves the tool are implementation/application behavior. |
| Publish an offer/request | An Intent is a potential flow before agreement; provider indicates an offer and receiver a request. Proposal publishes one or more intents and can be directed to agents. | GraphQL `Intent` exposes `provider`, `receiver`, `availableQuantity`, time bounds, and `publishedIn`; Proposal has `publishes`, reciprocal intents, `proposedTo`, and time bounds. | Intent stores provider/receiver, available quantity, time bounds, proposal join, and virtual `is_offer` / `is_need` conveniences. Proposal and proposed-intent association are modeled separately. | **Core properties are portable; UI/query and audience conventions differ.** Bonfire defaults created intents to public in the reviewed changeset; this is not a ValueFlows rule. |
| Discover/match the request with an offer | ValueFlows supplies structured Intent/Proposal data and the Intent–Commitment relation; the vocabulary does not specify a mandated matching algorithm or conversation. | hREA describes needs matching in its project overview and exposes the relevant records/relations. No interoperability test with Bonfire was located. | ActivityPub federation tests cover publishing and receiving Intent-like activities. Proposal/Intent federation tests exist; they test Bonfire's ActivityPub behavior, not hREA compatibility. | **The data model is portable; discovery, ranking, privacy, and user conversation remain implementation/application behavior.** |
| Intent becomes a Commitment | An Intent may be satisfied by one or more Commitments (`satisfiedBy`/`satisfies`). This is a relationship between planning records, not a required mutation or automatic state transition. | Commitment API accepts `satisfies`; Intent API exposes `satisfiedBy`. Current validation covers action, temporal, and quantity rules. | Commitment and Intent are stored as distinct models; satisfaction has its own relation module/API. | **Relationship semantics are portable.** The workflow that decides when to create the Commitment, how to split/partially satisfy an Intent, and how to close stale listings is not prescribed. |
| Commitment is fulfilled by an observed EconomicEvent | A Commitment is a promised flow; EconomicEvent records an observed flow and may link through `fulfills`. The event may also satisfy an Intent where no Commitment was made. | Commitment and EconomicEvent GraphQL APIs expose the relationships; current Holochain integrity code validates action/temporal/quantity constraints and references. | Bonfire has Commitment and EconomicEvent models and event creation/federation tests. In the reviewed EconomicEvent model, fields/relations for `fulfills`, `satisfies`, and `realizationOf` are still marked TODO; no persisted Commitment fulfillment relation was found in the inspected model. | **Specification semantics are portable; implementation support is uneven.** This is an implementation gap in the reviewed Bonfire extension snapshot, not evidence of a ValueFlows specification gap. Recheck later source/release state. |
| Exchange records between systems | RDF class/property IRIs are the vocabulary-level identifiers. JSON-LD can serialize RDF-shaped data. GraphQL APIs are implementation-facing conventions. | Uses Holochain entry/action hashes internally and a GraphQL adapter; API field names are ValueFlows-like. | Uses Bonfire pointer/relational IDs, optional GraphQL, and ActivityPub activities; tests exercise JSON objects such as `ValueFlows:Intent` and actor/activity routing. | **No cross-implementation wire compatibility is established.** Similar GraphQL names and common action slugs help, but identifiers, relation encodings, custom scalars, and ActivityPub/Holochain transport differ. |

### What existing serialization and APIs do—and do not—solve

The ValueFlows vocabulary defines RDF terms and IRIs. Its published examples use JSON-LD; JSON Schema documents cover a useful core subset. The separate GraphQL reference is described by the ValueFlows mirror as maintained mostly by projects using it and “somewhat out of sync.” The ontology therefore supplies shared semantics and RDF identifiers, but does not itself require a particular GraphQL schema, HTTP API, event transport, identifier strategy, or update workflow.

hREA's GraphQL adapter and Bonfire's optional GraphQL API expose overlapping field names and relations, which is useful practical prior art. However, the APIs are not proven to be wire-compatible by a shared versioned schema or cross-implementation conformance suite located in this review. Bonfire's ActivityPub path adds another envelope and URI identity convention; hREA's core storage/network path is Holochain. JSON-LD/RDF is the most direct existing semantic interchange route identified, but no tested complete export/import mapping between these two products was found.

## Specification, implementation, and policy boundaries

- **Specification coverage:** `use`, `transfer-custody`, temporal flow fields, provider/receiver, Proposal/Intent publication, `satisfies`, `fulfills`, Commitments, and EconomicEvents exist in the ValueFlows model. These are not gaps to be recreated in CoordMesh.
- **Implementation difference:** hREA's inspected API/source exposes more complete intent/commitment/event relations and actively validates entries. Bonfire's current source implements many of the same models and has ActivityPub/GraphQL tests, but the reviewed EconomicEvent model still marks several linking relationships TODO. The Bonfire README feature list omits Commitment/Agreement even though current source contains a Commitment model; its README should therefore not be read as authoritative current completeness evidence.
- **Serialization/API uncertainty:** no test demonstrated hREA records exported and imported by Bonfire without loss. ValueFlows JSON-LD and the overlapping GraphQL conventions are candidate tools, not proof of implementation conformance.
- **Application policy:** who can see an offer, matching/ranking, whether accepting an offer constitutes assent, whether use is reserved during an interval, who can cancel/extend, care/condition requirements, and notice/dispute practices are not settled just by selecting ValueFlows classes. Bonfire's public-by-default behavior is not a portable protocol requirement.
- **Not a specification gap:** absence of automatic Intent-to-Commitment conversion is not a gap; ValueFlows relates separate planned/promised/observed records and leaves the human/application workflow open. Bonfire's presently incomplete event-to-commitment relation is an implementation limitation. A failed implementation should not be repaired by inventing new CoordMesh primitives.

## Is a CoordMesh profile justified?

**Not on this evidence.** Both implementations use the same core action identifiers and ValueFlows field semantics for the drill's use and time interval. Existing RDF/JSON-LD and GraphQL conventions offer plausible interchange routes. The evidence does reveal different transports, local IDs, and uneven relation support, but no cross-implementation scenario has yet established which subset needs a stable interoperability contract. A profile drafted now would risk specifying implementation details or application policy before an actual exchange test.

A profile should be reconsidered only after a concrete, participant-approved test requires multiple independent systems to exchange the Three Neighbors data and the test identifies a specific ambiguity or lossy mapping that cannot be resolved by using ValueFlows RDF terms, JSON-LD, or existing API conventions. At that point profile scope should be limited to the demonstrated mapping and accompanied by conformance cases.

### Follow-up model projection experiment

The non-normative [Three Neighbors ValueFlows model projection experiment](../experiments/valueflows-three-neighbors/README.md) maps a small JSON-LD-shaped fixture to the inspected hREA and Bonfire model shapes. It demonstrates a pinned-source Bonfire implementation limitation for EconomicEvent → Commitment `fulfills`, while leaving runtime JSON-LD/API interoperability untested. This evidence does not change the conclusion above: it does not yet justify a CoordMesh profile.

## Licensing and governance check

### ValueFlows

- The current generated ontology page identifies ontology version `0.11` and explicitly declares **CC BY-SA 4.0**. That is evidence for the ontology artifact; it should not be assumed to license every software implementation, GraphQL package, generated schema, or supporting document.
- The project identifies Codeberg as its canonical repository; the GitHub repository is a read-only/synchronization mirror. The canonical Codeberg `valueflows/valueflows` README confirms RDF Turtle as the source-of-record specification and says the implementer-maintained GraphQL reference is somewhat out of sync. Its root `LICENSE.txt` is CC BY-SA 4.0, consistent with the generated ontology metadata. The source-of-record Turtle itself is hosted in the separate `valueflows/pages` repository, so its own exact notice should still be checked before copying that file.
- The public ValueFlows site credits named authors and committers and describes an evolving community vocabulary. The canonical repository README invites issue/PR contributions and discussion in a public Matrix room; the inspected repository root had no `CONTRIBUTING`, governance charter, or formal decision/voting rules. No project-specific patent grant for the ontology was found. Treat formal governance and patent assurances as **UNKNOWN / MORE RESEARCH**, rather than assuming W3C-like process from the vocabulary's RDF form.
- Software artifacts have their own terms: hREA's inspected `LICENSE` grants Apache License 2.0; GitHub's hREA repository metadata returned “Other / NOASSERTION” despite the checked-in Apache notice. Bonfire's repository LICENSE is AGPL-3.0, while its README says “version 3 ... or any later version” and a current source file carries `AGPL-3.0-only`; resolve that notice difference with maintainers before relying on code. Preserve each exact artifact notice and re-check before use.

### ODRL

- ODRL Information Model 2.2 and Vocabulary & Expression 2.2 are W3C Recommendations with W3C's permissive document-license rules. The Information Model's status section records that it was produced by the Permissions & Obligations Expression Working Group under the W3C Patent Policy and links its patent-disclosure record. The W3C ODRL repository says reports use the W3C Software and Document License; contributions to specifications use the W3C CLA; its test-suite contributions use BSD 3-Clause. Check the notice and patent disclosures for the exact artifact copied or adapted; these are distinct IP processes, not one blanket license for all ODRL implementations.
- ODRL's current public evolution venue is the W3C ODRL Community Group, whose published objectives include maintaining the 2.2 recommendations/errata, supporting profiles, and planning future major enhancements. The July 2026 W3C workshop report records consensus to pursue an ODRL 3.0 Working Group; the corresponding repository charter was still labelled a draft when checked 2026-10-07. Do not treat the proposed Working Group as already chartered.
- The workshop report explicitly distinguishes ODRL policy expression from software policy processing and says processor behavior is not sufficiently standardized. Thus ODRL 2.2 is a stable expression model, but generic machine enforcement/evaluation interoperability is not implied. This reinforces the earlier caution about not interpreting a policy as physical-world enforcement or legal effect.

## Primary sources

### ValueFlows specification and serialization

- [ValueFlows ontology metadata and vocabulary](https://www.valueflo.ws/specification/vfspec/) — version 0.11, ontology license metadata, RDF terms; [canonical repository README](https://codeberg.org/valueflows/valueflows/src/branch/master/README.md) and [repository LICENSE.txt](https://codeberg.org/valueflows/valueflows/src/branch/master/LICENSE.txt).
- [Actions](https://www.valueflo.ws/concepts/actions/), [flows](https://www.valueflo.ws/concepts/flows/), [offers and requests](https://www.valueflo.ws/concepts/proposals/) — `use`, custody-transfer, planning/observation, matching boundaries.
- [JSON Schemas](https://www.valueflo.ws/specification/json-schemas/) and [ValueFlows repository move notice](https://github.com/valueflows/valueflows) — serialization and source-of-record context.
- [ValueFlows status](https://www.valueflo.ws/introduction/status/) and [contributors](https://www.valueflo.ws/introduction/contributors/) — current project status and public contributor record.

### hREA

- [hREA repository](https://github.com/h-REA/hREA/tree/sprout), [Apache license notice](https://github.com/h-REA/hREA/blob/sprout/LICENSE), and [GraphQL API documentation](https://docs.hrea.io/reference/graphql-api-reference/).
- [Intent API](https://docs.hrea.io/reference/graphql-api-reference/intent/), [Commitment API](https://docs.hrea.io/reference/graphql-api-reference/commitment/), [EconomicEvent API](https://docs.hrea.io/reference/graphql-api-reference/economic-event/), and [Proposal API](https://docs.hrea.io/reference/graphql-api-reference/proposal/).
- [Built-in action implementation](https://github.com/h-REA/hREA/blob/sprout/dnas/hrea/zomes/coordinator/hrea/vf_actions/src/builtins.rs), [Commitment integrity model](https://github.com/h-REA/hREA/blob/sprout/dnas/hrea/zomes/integrity/hrea/src/rea_commitment.rs), and [EconomicEvent integrity model](https://github.com/h-REA/hREA/blob/sprout/dnas/hrea/zomes/integrity/hrea/src/rea_economic_event.rs).

### Bonfire ValueFlows extension

- [Bonfire ValueFlows extension](https://github.com/bonfire-networks/bonfire_valueflows) and its [AGPL-3.0 notice](https://github.com/bonfire-networks/bonfire_valueflows/blob/main/LICENSE).
- [Intent model](https://github.com/bonfire-networks/bonfire_valueflows/blob/main/lib/planning/intent/intent.ex), [Commitment model](https://github.com/bonfire-networks/bonfire_valueflows/blob/main/lib/planning/commitment/commitment.ex), [EconomicEvent model](https://github.com/bonfire-networks/bonfire_valueflows/blob/main/lib/economic_event/event.ex), and [action registry](https://github.com/bonfire-networks/bonfire_valueflows/blob/main/lib/knowledge/action/actions.ex).
- [Intent federation tests](https://github.com/bonfire-networks/bonfire_valueflows/blob/main/test/planning/intent_federate.exs) and [EconomicEvent federation tests](https://github.com/bonfire-networks/bonfire_valueflows/blob/main/test/economic_event/event_federate_test.exs).

### ODRL

- [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/) and [Vocabulary & Expression 2.2](https://www.w3.org/TR/odrl-vocab/) — Recommendations, document license, and patent-policy status.
- [ODRL Community Group](https://www.w3.org/community/odrl/), [ODRL repository license](https://github.com/w3c/odrl/blob/master/LICENSE.md), and [W3C Workshop on the Future of ODRL report](https://www.w3.org/2026/ODRLWS/report.html).
- [ODRL 3.0 draft Working Group charter materials](https://github.com/w3c/odrl/tree/master/w3c-wg-draft-charter-2026) — draft status only as of the review date.
