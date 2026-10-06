# ADR 0001: Spec-first development

- Status: Proposed
- Date: 2026-10-07

## Context

Interoperable infrastructure needs behavior independent of any single implementation. The project also has no confirmed protocol gap yet.

## Proposal

Where appropriate, develop in the order specification → schema → conformance tests → implementation. Use independent implementations to validate interoperability when the project reaches that stage.

## Consequences

This may delay implementation while research proceeds, but reduces the risk that a reference implementation silently becomes the specification. Some integrations may need no CoordMesh schema or code.

## Open questions

Which artifact forms and conformance methods fit each capability? Decide only when a concrete gap is established.
