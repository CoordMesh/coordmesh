# Architecture and open hypotheses

## Boundary

OpenCoord may ultimately be a small integration and profile layer connecting existing systems for communication/federation, identity and credentials, resource/economic models, payments, geography, scheduling, and distributed storage or compute. It need not replace these systems and may require little custom code.

Keep any domain model independent of transport. If Matrix proves suitable, it may be a first event/transport/federation adapter, not an unquestionable foundation. GitHub is current project hosting only and has no protocol meaning.

## Candidate concepts

Entity, Identity, Trust/Attestation, Relationship, Resource, Need, Capability, Rights/Permissions, Agreement, Proposal, Decision, Accounting, and Event are research hypotheses, not accepted primitives. Investigate whether ValueFlows or other standards already cover these concepts before defining anything.

## Capability decision vocabulary

- **REUSE:** adopt an existing standard or project directly when it adequately solves the need.
- **PROFILE:** specify a constrained/interoperable use of an existing standard.
- **INVENT:** add a new mechanism only after documenting the gap and justification.
- **UNKNOWN / MORE RESEARCH:** evidence does not yet justify a decision.

Never invent cryptography. Implementations must not silently define semantics. Prefer specification → schema → conformance tests → implementation where appropriate.

## Open hypotheses

- A Matrix adapter could provide event synchronization and federation while preserving a transport-independent domain model.
- ValueFlows or related vocabularies may cover much of resource, process, and economic coordination.
- Identity should distinguish cryptographic continuity from claims made by issuers; DID and VC standards may provide relevant building blocks without requiring a universal identity authority.
- Offline/local operation and later synchronization may be important properties, but requirements and tradeoffs need scenario-based research.
- OpenCoord itself may chiefly profile and connect standards rather than define a large protocol.

These remain open until supported by the landscape survey and reviewed ADRs.
