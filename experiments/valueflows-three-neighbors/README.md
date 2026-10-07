# Three Neighbors ValueFlows model projection experiment

**Status:** non-normative research experiment. This is not a CoordMesh profile,
protocol, conformance test, or claim that either implementation accepts the
fixture. No hREA or Bonfire code was changed.

## Question and result

Can one small ValueFlows representation of Alice lending Bob a drill survive
mapping to two independently developed implementations?

This experiment validates the fixture's linked identifiers and projects its
fields onto the documented hREA and Bonfire model shapes. It does **not** run
either server or invoke either API. Running both complete stacks and testing
their persistence and exchange was disproportionate for this bounded research
step: hREA requires a Holochain conductor and DNA, while Bonfire requires its
Elixir/Phoenix application and dependencies. The projection therefore tests
model-level representability, not runtime interoperability.

The main result is mixed. Resource, actor, action, and time values can be
represented by both model families, though local identifiers and relation
encodings need mappings. Intent-to-Commitment satisfaction exists in both,
directly in hREA and as a Bonfire `Satisfaction` relation. The inspected
Bonfire EconomicEvent model has no persisted `fulfills` relation to a
Commitment; hREA does. This is a concrete **implementation limitation at the
pinned Bonfire revision**, not a ValueFlows vocabulary gap. The experiment
does not establish that all JSON-LD fields are accepted by either API.

## Reproduce

Requires Python 3.9+ and only the standard library:

```sh
python project_models.py
```

The script reads `fixture.jsonld`, checks unique IDs, local references,
date-time syntax, `use`, Intent → Commitment `satisfies`, interval consistency,
and EconomicEvent → Commitment `fulfills`; then prints JSON projections for
the inspected model shapes. It exits non-zero if those fixture checks fail.
The generated local ID labels are symbolic placeholders, not valid hREA
ActionHashes, Bonfire ULIDs, or API credentials. The script is a small
reproducible mapping aid, not a JSON-LD processor: it does not expand RDF,
validate against an API schema, persist records, or assert conformance.

## Fixture and procedure

`fixture.jsonld` is a deliberately small RDF/JSON-LD-shaped graph using the
ValueFlows vocabulary IRI prefix and stable example IRIs. It contains:

1. Alice and Bob as `Agent`s.
2. One `EconomicResource` drill, with its stable fixture IRI also used as its
   `trackingIdentifier`.
3. A pre-matched, time-bounded `Intent` with action `use`, Alice as provider,
   and Bob as receiver. It represents the result of offer/request discovery;
   it does not attempt to specify a matching workflow.
4. A corresponding `Commitment` that `satisfies` the Intent.
5. An observed bounded `use` `EconomicEvent` that `fulfills` the Commitment.
6. Separate `transfer-custody` events for handover and return.

The mapping procedure is:

1. Parse and structurally check the fixture with the script.
2. Map ValueFlows action IRIs to the implementations' canonical action slugs.
3. Map fixture subject IRIs to symbolic implementation-local IDs.
4. Map common fields to hREA's GraphQL/model field concepts and Bonfire's
   inspected Ecto model attributes; encode Intent → Commitment as a Bonfire
   `Satisfaction` relation.
5. Compare fields and links against the pinned source model definitions.

No transformed output is fed back into an implementation. The symbolic IDs
make relationship preservation visible while highlighting that real import
requires ID creation/resolution. For Bonfire, the Commitment's `satisfies`
edge is represented by the Satisfaction join record, while the observed use
event's `fulfills` edge has no corresponding field/relation in the inspected
EconomicEvent model and is omitted from that projection.

## Revisions and primary evidence

Source snapshots were inspected on 2026-10-07. Exact refs below make the
research reproducible; this experiment did not check out or build those
projects.

| Project/artifact | Ref inspected | Relevant evidence |
| --- | --- | --- |
| ValueFlows ontology/pages | `valueflows/pages` `21e3fedc78325fc3fe4f0ff525afefe2c4e03733` (ontology version 0.11) | [Turtle source](https://codeberg.org/valueflows/pages/src/branch/main/assets/all_vf.TTL), [formatted vocabulary](https://www.valueflo.ws/specification/all_vf/), [actions](https://www.valueflo.ws/concepts/actions/) |
| hREA | `valueflows/hrea` `sprout` `8c99160bbf6c4ffab0b4d05a3edf8ec629c09ab4` | [GraphQL API](https://github.com/h-REA/hREA/tree/sprout/modules/vf-graphql), [REA types](https://github.com/h-REA/hREA/tree/sprout/dnas/rea_commons/zomes/rea_integrity/src/types), [action definitions](https://github.com/h-REA/hREA/tree/sprout/dnas/rea_commons/zomes/rea_integrity/src/validation) |
| Bonfire ValueFlows | `bonfire-networks/bonfire_valueflows` `main` `e1977a8cfd177dc856f40b125f6d6d07f22ac757` | [models](https://github.com/bonfire-networks/bonfire_valueflows/tree/main/lib), [EconomicEvent model](https://github.com/bonfire-networks/bonfire_valueflows/blob/main/lib/bonfire/valueflows/economic_event.ex), [Satisfaction relation](https://github.com/bonfire-networks/bonfire_valueflows/tree/main/lib/bonfire/valueflows), [action registry](https://github.com/bonfire-networks/bonfire_valueflows/tree/main/lib/bonfire/valueflows) |

The URLs above are convenient source locations and can move with branches; the
SHAs are the revision identifiers used in the review. The prior
[implementation interoperability review](../../standards/valueflows-implementation-interoperability.md)
contains the broader source-by-source licensing, governance, and capability
survey. ValueFlows is the vocabulary being projected, not an implementation
dependency selected by this experiment.

## Semantic comparison

Classifications describe only the inspected field/model mapping, not a claim
of successful end-to-end import. “Equivalent representation” preserves the
meaning through a different local representation; “recoverable with
implementation-specific knowledge” needs an adapter/ID map. “Unsupported” is
absence from the inspected model, not a claim that the implementation could
never add it.

| Semantic / fixture data | hREA projection | Bonfire projection | Evidence-based interpretation |
| --- | --- | --- | --- |
| Stable IDs for Agents, resource, Intent, Commitment, Events | **recoverable with implementation-specific knowledge** | **recoverable with implementation-specific knowledge** | Fixture IRIs are not the native Holochain ActionHashes or Bonfire local IDs. Actor/event/intent/commitment IRIs need an import map or implementation-supported external identifier. The drill IRI can additionally be retained as `trackingIdentifier`, but that does not make all local references globally identical. |
| Alice/Bob actor references and roles | **equivalent representation** | **equivalent representation** | `provider`/`receiver` references map to local agent references. The source actor IRI itself requires local identity resolution; this test does not prove a shared identity namespace. |
| Drill identity | **equivalent representation** | **equivalent representation** | Resource records and `trackingIdentifier` exist. Native resource references remain local IDs; retaining the fixture identifier is a mapping convention, not proof of automatic resolution. |
| `use` action | **equivalent representation** | **equivalent representation** | ValueFlows action IRI maps to built-in slug `use` in each implementation. The identifier is common; runtime accounting effects were not executed here. |
| `transfer-custody` handover and return actions | **equivalent representation** | **equivalent representation** | Both action registries contain this slug; direction is encoded with provider/receiver, resource, and event. The event does not itself specify the agreement or prove physical custody changed. |
| Fixed start/end interval | **equivalent representation** | **equivalent representation** | Values map to hREA timestamps and Bonfire UTC microsecond datetime attributes. Their model can represent the instants; actual precision, timezone normalization, validation, and persistence were not tested. |
| Intent → Commitment | **equivalent representation** | **equivalent representation** | hREA exposes Commitment `satisfies`/Intent `satisfiedBy`; Bonfire models the relationship using `Satisfaction(satisfies_id, satisfied_by_id)`. This is a different encoding but same relation direction in this example. |
| Commitment → observed use Event (`fulfills`) | **preserved exactly** | **unsupported** | hREA EconomicEvent exposes `fulfills` references. No equivalent field/relation exists in the pinned Bonfire EconomicEvent model; inspected source marks fulfillment-related links TODO. Bonfire’s Commitment-to-Intent Satisfaction join is not a substitute for Event-to-Commitment fulfillment. |
| Stable event links among handover/use/return | **recoverable with implementation-specific knowledge** | **recoverable with implementation-specific knowledge** | Event identifiers and common resource/actor references can be mapped, but the fixture asserts chronology and identity only; neither schema mapping proves causal or workflow ordering. |
| Intent as input to scenario | **equivalent representation** | **equivalent representation** | This fixture starts with a pre-matched Intent carrying provider and receiver; it tests no distinct offer/request pair, Proposal, discovery, privacy, or selection semantics. |
| Temporal use actually reserves the drill | **ambiguous** | **ambiguous** | A time interval is representable. Whether it blocks another booking, constitutes permission, or is enforced is application behavior and outside these model projections. |

The hREA projection uses ValueFlows-shaped GraphQL/model concepts, not a captured
GraphQL request accepted by a running endpoint. The Bonfire projection follows
the Ecto model attributes and join relation, not a persisted database row. The
input JSON-LD fixture and the projected field names therefore should not be
read as validated API serialization formats.

## What the experiment establishes

### 1. ValueFlows specification limitation

No limitation in the ValueFlows subset used here is demonstrated. The
vocabulary has relevant terms for agents, resources, Intent, Commitment,
EconomicEvent, the `use` and `transfer-custody` actions, temporal bounds,
Intent satisfaction, and event fulfillment. This is consistent with the
existing scenario mapping. This experiment does not test every cardinality,
unit, quantity, Agreement, or policy semantic.

### 2. Serialization/interchange limitation

The RDF/JSON-LD-shaped fixture provides stable vocabulary IRIs and explicit
references, but this experiment did not use a JSON-LD processor, canonicalize
RDF, or demonstrate a shared import/export contract. A JSON-LD document can
carry the graph; it does not by itself define either product's accepted API
payload, native ID creation, conflict policy, or exact round-trip behavior.
The local ID resolution and field encodings need adapter knowledge in the
projections.

### 3. Implementation limitation

At the pinned Bonfire source revision, the model does not represent the
fixture's EconomicEvent → Commitment `fulfills` relation. hREA does. This is a
concrete implementation difference and one lossy mapping in the modeled
exchange. It is not evidence that Bonfire's ActivityPub or GraphQL path has
been exercised here, nor that a different Bonfire version lacks support.

### 4. Application-policy differences

Matching, who may publish/discover an Intent, whether acceptance is assent,
whether the interval reserves the drill, what early termination means, and
how an observed event is trusted remain policy/workflow questions. This
experiment neither classifies them as protocol gaps nor invents terms for
them.

## Does this change the case for a CoordMesh profile?

It strengthens the case for **testing a concrete exchange subset**, because a
real model-level difference now appears: the pinned Bonfire model cannot
retain the event-to-commitment `fulfills` link represented by the fixture and
hREA model. It does **not** yet justify a CoordMesh profile. The evidence is
limited to source-shaped projection, the difference is currently attributable
to one implementation, and no runtime adapter, shared JSON-LD contract, or
cross-product conformance test has shown that a profile is the appropriate
remedy. No solution is proposed. Revisit after the Bonfire model evolves or a
real consumer requires this link across systems; distinguish adapter support
from vocabulary extension if that happens.

## Limitations and next evidence

- No hREA or Bonfire process, endpoint, database, ActivityPub transport, or
  Holochain network was run.
- No released versions were selected; exact development-branch SHAs were
  inspected. Features at those revisions may not be packaged releases.
- The projections are a manual, explicit adapter sketch and not official
  project adapters or conformance artifacts.
- JSON-LD syntax is parsed as JSON only; no RDF expansion/validation library
  is used, and this fixture is not validated against ValueFlows JSON Schema.
- No concurrency, partial fulfillment, event ordering, cancellation,
  permissions, quantity, or signatures are tested.
- Bonfire's unsupported event link is scoped to the pinned source model. It
  should be rechecked against later code before drawing a product-wide claim.

The next useful research step is to decide whether to run a narrow, isolated
adapter/runtime spike for the `fulfills` link and external-ID mapping, or first
check current released Bonfire/hREA APIs for changes since these pinned refs.
That is evidence gathering only; it does not pre-authorize a CoordMesh profile.
