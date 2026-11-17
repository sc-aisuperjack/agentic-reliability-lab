# ADR-001 — Deterministic baseline first

**Status:** Accepted. **Date:** 2026-11-17.

## Context
A publicly shareable agentic engineering reference should be reliable, inspectable and inexpensive to host. Exposing a paid LLM API key anonymously would add abuse and billing risks.

## Decision
Use a static React UI, independently deployed FastAPI, deterministic policy-based workflow and synthetic data. Be transparent that this is not generative reasoning.

## Alternatives
- Streamlit-only: simpler but does not demonstrate a separate API boundary.
- LLM-first routing: richer natural language, but non-deterministic results, inference charges, prompt-injection and API-key abuse risks.

## Consequences
Pros: real executable workflow, reproducible evaluations, straightforward CI and no required model bill.
Cons: narrower language behaviour and not yet evidence of LLM agent orchestration.
Upgrade path: separate DecisionEngine interface for optional LLM routing, with budgets, tool permissions, independent tests and strong auth before real multi-tenancy.
