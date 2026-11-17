# PLAN-002 — Synthetic refund eligibility

**Status:** Implemented  
**Version:** 1.0.0  
**Created:** 2026-11-17  
**Last Updated:** 2026-11-17  
**Owner:** Engineering Lead  
**Related Intent:** INTENT-002  
**Related Specification:** SPEC-002  
**Approval:** Approved

## Approved decisions

Use `backend/app/refund_eligibility.py` for calculations and keep orchestration and traces in `engine.py`. Store structured tenant-specific policies in one authoritative location, including the window and citation text. All demo assessments use 17 November 2026. Enforce tenant isolation before revealing any order information. Explicitly handle refunded, undelivered, expired, used and missing evidence; never infer condition. Preserve existing API contracts and add an optional structured result. Retain all 14 evaluations and protect general policy and tracking behavior. Update the frontend and expose SPEC-002 alongside SPEC-001. No paid dependencies, external services or refund execution.

## Current implementation and contracts

`backend/app/knowledge.py` holds tenant articles, three fictional orders and keyword routing. An order ID plus order/tracking language takes precedence over refund terms, so an order-specific refund question can become tracking. General refund questions retrieve a tenant article. `backend/app/engine.py` handles known instruction overrides and handoff before routing, then retrieves an authorised order or a cited policy. It does not assess eligibility. Public tenant selection is not real authentication.

`POST /api/agent/run` accepts `message` (1–2000 characters) and `tenant` (`atlas` or `beacon`, default `atlas`). Its response fields are `run_id`, `mode`, `decision` (`answered`, `clarification`, `abstained`, `escalated`, `blocked`), `intent`, `answer`, `tenant`, `citations` (source_id, title, quote), `evidence_count` and ordered `trace` (stage, tool, outcome, detail). Preserve these fields and decision literals. `POST /api/evaluations/run` returns total, passed, failed, pass_rate and result records (id, name, category, expected, actual, passed, explanation). `GET /api/knowledge` returns tenant article identifiers and titles; `GET /api/specifications` currently describes SPEC-001; `GET /health` describes the synthetic deterministic service. Preserve their contracts. The React frontend consumes the run, evaluation and specifications endpoints and displays answer, citations and trace; its evaluation copy hard-codes 14 cases.

`backend/app/evaluations.py` contains EV-001–EV-014 and checks decision and optional citation only. `backend/tests/test_engine.py` and `test_api.py` cover existing evaluations, API validation, tenant isolation and a precise policy trace; the API test assumes exactly 14 evaluations. ADR-001 establishes deterministic synthetic operation without paid inference.

## Proposed routing and workflow

1. Retain validation, known injection blocking and explicit handoff precedence. Before existing order-ID precedence, recognise a narrow `refund_eligibility` intent: refund/return language combined with a question about qualification or a particular order, including eligibility without an ID. Keep general policy questions such as “Can I return an item?” and “What is the refund policy?” on `refund`, and tracking-only questions on `order`. Test representative phrases; mixed-intent ambiguity and limited language coverage remain risks.
2. Extract the existing `ORD` syntax. If absent, request a fictional ID. For an unknown ID abstain; for a cross-tenant record block before exposing facts in answer, citations, trace or structured output. After authorisation, retrieve the selected tenant's refund policy. Missing policy must not lead to a decision based on another tenant or invented evidence.
3. Assess explicit order facts only. Never infer unused condition from delivery or a date from tracking text. With delivery date, delivered status and unused condition, compare calendar days against the fixed date: Atlas day 30 and Beacon day 14 are inclusive. Missing evidence causes clarification or abstention. Distinguish already refunded; never mutate an order or execute or claim a refund. Cite the authorised policy when making an eligibility determination. Keep policy windows and citation text consistent via a shared source or explicit consistency test.
4. Record intake, routing, authorised lookup, policy retrieval, assessment and validation only when performed and in actual order. Short-circuited traces must not claim later work occurred or leak cross-tenant details.

## Fixtures and clock

Keep IDs, tenant ownership, status and tracking detail of ORD-1001 (Atlas delivered), ORD-1002 (Atlas processing) and ORD-2001 (Beacon refunded). Add explicit ISO delivery dates and condition values (`unused`, `used`, or unknown) where appropriate, consistent with existing tracking text. Add clearly fictional unique records for eligible and expired Atlas and Beacon, used Atlas, missing condition, boundary dates and missing delivery date. Use ORD-2001 for already refunded, existing opposite-tenant records for isolation, and an unallocated ID for unknown. At 2026-11-17, Atlas day 30 is 2026-10-18 and day 31 is 2026-10-17; Beacon day 14 is 2026-11-03 and day 15 is 2026-11-02. Never assign unused merely because a record is delivered.

Inject an internal assessment date into the workflow, with a named `date(2026, 11, 17)` constant for all demo assessments and evaluations. Do not expose a caller-controlled date on the public request. Tests pass explicit dates for boundaries and repeatability, without wall-clock or timezone dependence. UUIDs remain variable: compare semantic fields and trace, not whole responses or run IDs. Display the assessment date so the fixed demo clock is clear; it will become stale.

## Proposed additive response

Add optional `eligibility` to `RunResponse`, defaulting to null outside the workflow, containing `status` (`eligible`, `ineligible`, `needs_more_information`, `already_refunded`, `blocked_or_unsupported`) and assessment date when an authorised assessment occurs. Do not include order facts in blocked results. Preserve `decision`: answered for eligible, ineligible or already refunded; clarification for missing information the user can supply; abstained for unknown/missing evidence or unsupported policy; blocked for tenant denial. The answer itself must clearly distinguish outcomes for existing clients. An additive field works with the current frontend but could affect strict external consumers. Update frontend types and presentation to support it and offer fictional examples, without suggesting a refund was issued.

## Implementation sequence and affected files

Extend policy and fixtures in `backend/app/knowledge.py`; add the typed result in `backend/app/models.py`; implement calculations in `backend/app/refund_eligibility.py` and routing in `backend/app/engine.py`; extend `backend/app/evaluations.py` while retaining EV-001–EV-014; add tests in `backend/tests/test_engine.py` and `backend/tests/test_api.py`; update `frontend/src/App.tsx` and expose SPEC-002 alongside SPEC-001 through `backend/app/main.py`. Update `README.md` as appropriate. No dependency, CI or Render changes are planned.

## Acceptance and regression tests

| Requirements | Proposed evidence |
| --- | --- |
| REQ-007, 008, 016 | Table-driven eligibility routing with and without ID and phrase variants; general policy, tracking, cancellation, shipping, safety and handoff regressions; missing ID clarifies. Keep all 14 existing evaluations. |
| REQ-009, 010, 015 | Both cross-tenant directions deny without details anywhere in serialized response; authorised outcomes cite the selected tenant's policy and trace real operations in order. |
| REQ-011, 012 | Both tenants: inside window, inclusive final day, first expired day; eligible, used and not-delivered cases. Assert status and reason, not only `answered`. |
| REQ-013 | Missing condition, missing date, unknown ID and missing policy never yield eligible; no inferred evidence. |
| REQ-014 | Already refunded is distinct; no outcome claims execution. Compare fixture state before and after runs. |
| API/UI | Preserve fields, decision values, validation, policy answers, tracking and the existing policy trace; serialize the optional result and build the frontend. |

Extend evaluations to check status, relevant citation, reason and appropriate trace while preserving report shape and old case IDs. Replace the exact total assertion with assertions that all existing cases remain and all cases pass, without weakening their checks. Verify using `python -m pytest -q` in `backend` and `npm run build` in `frontend` with existing dependencies, inspect the evaluation report and changed-file diff, and report actual results and tooling limitations. No results are claimed here.

## Unresolved questions and risks

- The implementation prioritises already-refunded, then undelivered, future-date inconsistency, expired window and used condition, followed by missing evidence. Future dates need clarification and missing policy abstains. It reports the first applicable reason rather than every conflicting reason.
- The API is stateless. Missing fixture facts cannot be supplied through a trusted data source in this demo; the user must resubmit after the synthetic record is corrected.
- Keyword routing cannot understand all natural language or every mixed tracking/eligibility question.
- Strict external consumers might reject the additive optional response field; their existence is unknown.
- Future-date handling and refunded precedence are workflow rules, not claims explicitly made by the cited policy. Public tenant selection remains unsuitable for real customer data.
