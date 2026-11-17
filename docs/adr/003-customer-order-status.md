# ADR-003 — Customer-scoped synthetic order status

**Status:** Accepted
**Version:** 1.0.0
**Created:** 2026-11-17
**Last Updated:** 2026-11-17
**Decision Owner:** Engineering Lead
**Related:** INTENT-003, SPEC-003, PLAN-003

## Context

The legacy synthetic support workflow checks tenant membership. Existing clients and evaluations depend on that workflow. Feature 003 requires a customer-scoped read and a follow-up Order ID.

## Decision

Provide a dedicated order-status endpoint and disjoint synthetic order fixtures. Resolve a public demo persona through a server-owned allowlist and scope each read by tenant and customer. Persona selection simulates authentication using fictional data and offers no production security boundary.

Use a browser-managed continuation hint for the next turn. Validate and normalise a single Order ID before querying the scoped source. Return equivalent customer-facing results for unknown and unauthorised orders. Present the canonical ID and the current Delivered, Processing or Refunded status. Translate source failures into safe retry guidance and reject order modifications.

## Alternatives Considered

- Extending the legacy endpoint and reusing fixtures would require migrating or closing tenant-only access paths.
- Server-side sessions would own continuity at the cost of storing and expiring sessions.
- Trusted sign-in would establish a production identity and requires a separate integration design.

## Consequences

The legacy workflow keeps its contract. The demo has separate fixtures and continuation ends when the browser state resets. Production requires verified upstream identity, an approved source and its own review. Real business-impact measurement belongs to that integration.

## Approval

**Approved By:** Engineering Lead
**Approval Date:** 2026-11-17
