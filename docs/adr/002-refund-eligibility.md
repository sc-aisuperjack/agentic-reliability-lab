# ADR-002 — Deterministic synthetic refund eligibility

**Status:** Approved for implementation.  
**Date:** 2026-11-17.  
**Related:** INTENT-002, SPEC-002, ADR-001, PLAN-002.

## Context

The deterministic router answers refund policy questions and tracks synthetic orders, but order-ID precedence sends some eligibility questions to tracking. Eligibility requires authorised order facts, the selected tenant's policy, an explicit assessment date, explainable outcomes and no financial action. Clients rely on existing response fields and decision values. Tenant selection is not authentication.

## Proposed decision

Recognise a narrow eligibility intent before tracking, preserving general policy and tracking routes and existing safety and handoff precedence. Look up the synthetic order, enforce tenant isolation before revealing facts, retrieve the selected tenant's structured policy, and assess explicit facts in a dedicated `refund_eligibility.py` module using 17 November 2026 for all demo assessments and inclusive tenant-specific calendar-day windows. `engine.py` orchestrates and traces operations. Keep policy rules in one authoritative location. Explicitly handle refunded, undelivered, expired, used and missing information. Short-circuit when evidence or authorisation is missing. Add an optional typed eligibility status to the existing response, retaining a readable answer, appropriate policy citation and truthful ordered trace. Preserve all 14 evaluations, expose SPEC-002 alongside SPEC-001, and update the frontend. Introduce no order mutation, refund operation, LLM or external service.

## Alternatives and trade-offs

- **Reuse the existing order or policy route:** fewer branches, but fails to distinguish policy explanation from order-specific assessment and risks breaking tracking.
- **Route every refund word to eligibility:** simpler, but breaks general policy questions by requesting an order ID. Narrow deterministic rules preserve known cases but have limited language coverage and mixed-intent ambiguity.
- **LLM classification or interpretation:** potentially broader language coverage, but adds nondeterminism, cost and security complexity outside ADR-001 and feature scope.
- **Answer text only or new decision literals:** text-only is fragile for clients and tests; new decision literals risk existing clients. An additive optional typed result preserves decisions, though strict consumers may reject new fields.
- **Wall clock or public date parameter:** a wall clock makes fixtures drift; a caller-selected date permits arbitrary outcomes. An injected fixed date is reproducible but becomes stale and must be disclosed; revisit for non-demo use.
- **Independent window constants and policy citation:** simple but prone to divergence. Keep the rule and authorised policy aligned via a shared source or consistency test, with review and tests for changes.

## Consequences

The workflow gains inspectable policy-grounded outcomes and regression evidence without financial action or removal of response fields. Fixtures, routing cases, boundaries and isolation need ongoing maintenance. Results depend on synthetic facts and narrow routing; the service remains stateless, tenant selection is not real access control, and the fixed date is not a production time source. The assessment returns the first applicable reason, prioritising already-refunded and known disqualifiers; missing fixture data cannot be corrected through this demo.
