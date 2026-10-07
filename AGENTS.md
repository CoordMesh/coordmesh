# Agent guide

## Purpose

CoordMesh is independent open infrastructure for decentralized coordination. It explores generic mechanisms that applications can compose; it does not prescribe institutions. Read [README](README.md), [vision](docs/vision.md), [principles](docs/principles.md), [architecture](docs/architecture.md), [governance](GOVERNANCE.md), and [roadmap](docs/roadmap.md) for project context.

## Source of truth and next work

This repository is the project source of truth. The initial research/architecture milestone and the non-normative executable drill-loan interoperability example are documented. The next work is targeted gap validation as described in [the roadmap](docs/roadmap.md); do not restart broad landscape research unless a specific evidence question requires it. Check project issues for current sequencing. Do not assume the originating conversation is available.

## Invariants

- Mechanisms, not institutions; do not make institutions foundational protocol concepts.
- Integrate before inventing; classify proposals REUSE, PROFILE, INVENT, or UNKNOWN.
- Never invent cryptography. Do not implement before research identifies a gap.
- Keep domain concepts transport-independent. Matrix is a candidate, not an accepted foundation.
- No universal human ranking or social credit. Prefer contextual claims and attestations.
- AI may advise, but affected participants retain authority unless they narrowly delegate it.
- No permanent founder, NOverhead, forge, service, or infrastructure privilege.
- Do not assume a legal entity or add application-specific requirements to the protocol.

## Decisions and uncertainty

Significant decisions belong in `adr/` using the template in `adr/README.md`. ADRs start Proposed unless evidence and review support acceptance. Agents may propose ADRs but must not silently overturn Accepted decisions. Record assumptions with confidence and evidence; record unresolved matters as questions or UNKNOWN rather than inventing certainty.

## Research

Prefer primary sources: normative specifications, governance pages, source repositories, licenses, security documentation, and implementation/conformance evidence. Record links and date checked. Assess maturity, governance, license, decentralization, interoperability, local/offline behavior where relevant, security, dependencies, and fit. Distinguish standard capabilities from implementation properties and marketing claims.

## Autonomy and review

Agents may autonomously improve documentation, research, scenario clarity, link hygiene, and proposed ADRs. Human/project review is required before accepting project-wide architecture or governance, creating compatibility commitments, introducing a novel protocol primitive, changing security or privacy posture, or making external organizational/account/domain/legal commitments. Do not create external entities or accounts. When evidence is insufficient, preserve the uncertainty.

## Development order

Use specification → schema → conformance tests → implementation where appropriate. An implementation is not the implicit specification. Keep changes minimal and avoid speculative issues or empty framework structure.
