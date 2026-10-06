# Roadmap

## 1. Open Coordination Infrastructure Landscape Survey — current

Research existing open standards, protocols, and implementations before specifying or implementing OpenCoord. Compare maturity, governance, license, decentralization, interoperability, local/offline behavior where relevant, security, dependencies, and fit. Start with [standards/landscape.md](../standards/landscape.md).

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

## 2. Gap and profile decisions

Review research, document uncertainties, propose ADRs for significant conclusions, and decide whether a profile, integration, or new mechanism is actually needed.

## 3. Specification and conformance

Only after a justified gap exists, specify the smallest useful behavior. Add schemas and independent conformance cases before reference implementations where practical.

## 4. Dogfooding and independence

As real contributors arrive, evaluate project coordination needs as a conformance scenario. Document succession, responsibilities, releases, security response, and replaceable infrastructure as the project grows.
