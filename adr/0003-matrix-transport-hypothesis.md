# ADR 0003: Matrix as a transport hypothesis

- Status: Proposed
- Date: 2026-10-07

## Context

Matrix appears to provide federated event synchronization, extensible events, rooms, and optional end-to-end encryption. A transport may help test coordination, but transport coupling could constrain independent applications.

## Proposal

Evaluate Matrix as a first transport/event/federation candidate while keeping any CoordMesh domain semantics transport-independent. This ADR records a hypothesis for research, not an implementation commitment or requirement.

## Consequences

The survey must compare Matrix with relevant alternatives, inspect exact boundaries and offline/local behavior, and verify licensing, governance, security, and implementation maturity before selection.
