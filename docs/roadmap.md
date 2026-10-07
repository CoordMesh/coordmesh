# Roadmap

## 1. Research and architecture synthesis — completed

Research existing open standards, protocols, and implementations before specifying or implementing CoordMesh. Compare maturity, governance, license, decentralization, interoperability, local/offline behavior where relevant, security, dependencies, and fit. Start with [standards/landscape.md](../standards/landscape.md).

Focused work items:

1. Survey standards and open-source projects relevant to decentralized coordination.
2. Build the REUSE / PROFILE / INVENT capability map.
3. Evaluate Matrix capabilities and architectural boundaries.
4. Evaluate ValueFlows and similar resource/economic coordination models.
5. Evaluate identity, attestation, and credential standards.
6. Refine Three Neighbors based on research.
7. Identify the smallest genuinely missing protocol slice.
8. Define a first conformance scenario only after preceding research.

When GitHub is configured, create these as focused issues rather than expanding a speculative backlog.

The initial survey, ValueFlows/ODRL scenario mapping, implementation review,
model projection experiment, and [candidate architecture synthesis](candidate-architecture.md)
complete this bounded research/architecture milestone. The synthesis remains
a candidate, not an accepted ADR. The model projection was not a live exchange;
the research-phase exit criterion for a profile or protocol has not been met.
This completion does not claim that the standards landscape is exhaustive.
The [drill-loan example](../examples/drill-loan/README.md) now provides a
small executable check of independent ValueFlows JSON-LD interpretation over
a temporary filesystem mailbox. It does not test Matrix, federation, or
third-party implementation conformance.

## 2. Targeted gap validation and profile decisions — next phase

Close a specific evidence question from the synthesis using pinned versions and
reproducible exchange evidence. Recheck the hREA/Bonfire `fulfills` and external
identifier findings against their current released interfaces, then decide
whether an adapter experiment is sufficient or a shared profile is genuinely
needed. Do not expand the survey or draft a profile by default. Follow the
research-phase exit criterion in the candidate architecture before proposing
normative behavior. Significant conclusions may receive a Proposed ADR; do not
accept architecture without project review.

## 3. Specification and conformance

Only after a justified gap exists, specify the smallest useful behavior. Add schemas and independent conformance cases before reference implementations where practical.

## 4. Dogfooding and independence

As real contributors arrive, evaluate project coordination needs as a conformance scenario. Document succession, responsibilities, releases, security response, and replaceable infrastructure as the project grows.
