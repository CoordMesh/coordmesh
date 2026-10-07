# Drill loan: two independent interpreters

**Status:** executable, non-normative Milestone 1 example. It is not a
CoordMesh protocol, SDK, profile, production application, or conformance
commitment. The shared expected state is a test vector, not a specification.

This demo runs two independent applications: Alice is implemented in C#/.NET
and Bob in Python. Alice publishes a ValueFlows JSON-LD offer. Bob reads it,
independently checks the ValueFlows terms, and writes a request. Alice reads
that request, writes a ValueFlows Agreement and Commitment plus a custody
handover event. Bob independently interprets those records and writes the
return event. Finally, Alice and Bob each parse the exchanged documents and
derive a final state. A small harness compares the two reports with the shared
conformance vector.

## Run it

Requirements: Python 3.9+ and .NET 10 SDK. No Python packages, NuGet packages,
accounts, network access, container runtime, or secrets are needed.

From the repository root:

```sh
python examples/drill-loan/run_scenario.py
```

The runner compiles Alice into a temporary build directory, runs Alice and Bob
as separate processes, and creates a temporary exchange directory. It removes
both directories when the run ends. The five `.jsonld` messages are ordinary
files. Pass `--keep` to retain them under a generated temporary path for
inspection. No message depends on a hidden service.

## Flow

```text
Alice (C#)                         Bob (Python)
    |                                  |
    |-- 01-offer.jsonld -------------->|  discovers Alice's drill offer
    |<-- 02-request.jsonld ------------|  requests 14:00-16:00 UTC
    |-- 03-acceptance.jsonld --------->|  Agreement + Commitment
    |-- 04-handover.jsonld ----------->|  Alice transfers custody to Bob
    |<-- 05-return.jsonld -------------|  Bob transfers custody to Alice
    |                                  |
    |-- Alice parses all messages      |-- Bob parses all messages
    |           both derive: returned to Alice
```

The mailbox is a temporary shared directory. The applications do not import
each other's source, a shared domain library, or a CoordMesh runtime. Each has
its own ValueFlows term references, JSON reader/writer, validation, and final
state derivation. Only the JSON-LD documents and the static expected-state
test vector are shared. The runner coordinates process order; it does not
interpret the scenario.

## Transport choice and limits

This example uses the host filesystem as a disposable handoff transport. No
transport service is required, so no `compose.yaml` or Matrix homeserver is
included. This keeps the executable test focused on independent interpretation
of the exchanged standard vocabulary. It demonstrates neither federation,
remote delivery, access control, nor offline reconciliation. Matrix remains a
candidate transport; this example makes no selection or claim about its
suitability. A Matrix version would be a separate transport adapter and must
carry the same ValueFlows documents without changing their domain terms.

## Standards and policy boundaries

### Standard-defined semantics used

- ValueFlows 0.11 RDF vocabulary terms identify `Intent`, `Agreement`,
  `Commitment`, `EconomicEvent`, `use`, `transfer-custody`, `satisfies`, and
  `clauseOf`.
- ValueFlows `use` denotes non-consumptive use. `transfer-custody` describes
  custody flow, not a transfer of legal ownership.
- [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) compact form carries stable
  IRIs for documents and references.

References: [ValueFlows formatted vocabulary](https://www.valueflo.ws/specification/all_vf/),
[ValueFlows actions](https://www.valueflo.ws/concepts/actions/), and the
[ValueFlows source-of-record RDF vocabulary](https://codeberg.org/valueflows/pages/src/branch/main/assets/all_vf.TTL).
The reviewed vocabulary is ValueFlows 0.11 at source revision
`21e3fedc78325fc3fe4f0ff525afefe2c4e03733` (the same revision recorded in the
[prior interoperability experiment](../../experiments/valueflows-three-neighbors/README.md)).
The example uses these existing terms; it does not define CoordMesh domain
semantics.

The documents use the ValueFlows vocabulary IRIs and JSON-LD context. The
applications use standard-library JSON parsers for this narrow example; they
do not claim to be general-purpose JSON-LD processors or validate arbitrary
JSON-LD expansion. Each independently checks the exact terms and relationships
used by this example.

### Example-specific application policy

- Alice's offer covers this one drill and the stated two-hour window.
- Bob's request identifies Alice as provider and Bob as receiver.
- Alice's published Commitment satisfying Bob's Intent is how this example
  records Alice's acceptance. ValueFlows does not prescribe the interaction or
  establish legal assent.
- The latest `transfer-custody` event by `hasPointInTime` determines the
  example's current custodian. This rule is only for this test; ValueFlows
  events are records, not proof that physical events occurred.
- All times are UTC. The date is fixed for repeatable output.

ODRL is not used: the example tests a planned ValueFlows use commitment and
observed custody flows. It does not add machine-readable usage rights, duties,
or enforcement conditions beyond the ValueFlows scenario. No cryptographic
identity, authentication, payment, inventory accounting, or trust score is
implemented. The `example.org` participant/resource IRIs are stable test
references, not verified identities or resolvable production records.

## Interoperability conventions observed

The smallest shared test assumptions are:

1. Use stable IRIs for the actors, drill, Intents, Agreement, Commitment, and
   Events in this scenario.
2. Map compact ValueFlows terms through the supplied JSON-LD context.
3. Use ValueFlows `satisfies` from Commitment to Bob's request and `clauseOf`
   from Commitment to the Agreement.
4. Interpret custody direction as provider → receiver for each
   `transfer-custody` event, and order those events by their stated time.

These are the document's standard terms plus this example's fixed identifier
and workflow choices. The experiment does not establish that all ValueFlows
implementations share a global identifier policy, that a JSON-LD API can
import the documents unchanged, or that the application rules belong in a
CoordMesh profile.

## Implementation independence

- Alice: `alice/Program.cs`, C#/.NET 10, `System.Text.Json` only.
- Bob: `bob/bob.py`, Python 3.9+, Python standard library only.
- Orchestration/assertions: `run_scenario.py`; launches each executable as a
  separate process and compares their output, without importing their logic.
- Expected state: [shared, non-normative conformance vector](../../tests/conformance/drill-loan/expected-state.json).

Each implementation duplicates the small set of scenario constants and
validations by design. This tests whether independently written readers agree;
it is not a recommended application architecture.
