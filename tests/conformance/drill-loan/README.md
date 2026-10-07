# Drill-loan executable conformance example

**Status:** exploratory, non-normative test artifact. It does not define a
CoordMesh profile or make conformance claims about third-party software.

Run `python examples/drill-loan/run_scenario.py` from the repository root. The
runner executes independent C# Alice and Python Bob applications and checks
each final interpretation against [expected-state.json](expected-state.json).

The assertions compare:

- Alice/Bob participant references and drill IRI;
- ValueFlows `use` action and fixed start/end interval;
- Agreement and Commitment identifiers;
- Commitment `satisfies` request and `clauseOf` Agreement references;
- handover and return `transfer-custody` Event IDs, directions, resource, and
  timestamps;
- returned final state and Alice as the last recorded custodian.

This is an example test vector. The filesystem handoff and acceptance/current
custodian rules are application-specific. ValueFlows terms supply the domain
semantics. The test does not validate legal effect, real-world event truth,
authentication, generic JSON-LD processing, or Matrix interoperability.
