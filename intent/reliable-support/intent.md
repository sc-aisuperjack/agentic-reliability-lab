# INTENT-001 — Reliable customer support demonstration

**Status:** approved for reference implementation.

## Why
Agentic workflows are difficult to assess from a chat transcript alone. Engineers need to inspect decisions, tools, evidence, tenancy boundaries and reliability safeguards.

## Outcome
Provide an interactive demo where a visitor submits synthetic customer questions, inspects traces and evaluates correctness against versioned cases.

## Scope
- React/TypeScript UI with an independent Python FastAPI backend
- Explicit routing, tenant-scoped synthetic knowledge and order records
- Clarification, escalation, abstention, trace evidence, policy safeguards
- Automated evaluation, engineering tests and GitHub Actions

## Exclusions
No real customer data or accounts; no actual ticket creation; no authenticated tenancy; no proprietary Vozara or Centrica implementation; no paid LLM required. The deterministic baseline is not generative AI.
