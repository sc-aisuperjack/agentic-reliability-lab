# PLAN-003 — Customer Order Status

**Status:** Approved\
**Version:** 1.0.0\
**Created:** 2026-11-17\
**Last Updated:** 2026-11-17\
**Owner:** Engineering Lead\
**Related Intent:** [INTENT-003](intent.md)\
**Related Specification:** [SPEC-003](spec.md)\
**Approval:** Approved

The Engineering Lead approved the dedicated endpoint, separate synthetic fixtures, public demo persona selector, browser-managed continuation, initial statuses and identical customer-facing responses for unknown and unauthorised orders. Approval was given on 2026-11-17.

## Current System and Constraints

- `POST /api/agent/run` accepts one message and an optional tenant (Atlas by default). The deterministic engine checks instruction overrides and handoff requests before keyword routing. It answers tenant-scoped policy questions with citations, assesses synthetic refund eligibility and abstains when evidence is missing.
- The existing order branch recognises phrases such as “Where is my order?” and “Track order ORD-1001”. It prompts for a missing ID, normalises matching references to `ORD-<digits>`, and reads the shared `ORDERS` dictionary before checking tenant membership. The response includes the status and fixture detail. There is no customer identity or ownership check. Unknown and cross-tenant requests have different answers, decisions and traces. There is no source failure path.
- The React playground keeps a visible transcript locally and submits only the current message and tenant. A bare ID following an order prompt reaches the backend without context and currently routes to the unsupported fallback.
- Existing tests and EV-001–EV-023 cover policy grounding, safety, handoff, legacy status lookup and refund eligibility. The refund regression suite pins the exact legacy status answer for ORD-1001. EV-007, EV-013 and EV-014 pin the legacy distinction between blocked and unknown orders. EV-011 pins an informational cancellation-policy answer.

## Proposed Approach

### Customer identity and authorisation

Add a dedicated `POST /api/order-status/run` demo endpoint using the existing response envelope. Give the playground an explicit Customer Order Status mode alongside the existing support workflow. Label the control “Demo persona” and explain beside it that anyone can choose a fictional customer to simulate an authenticated request. Use the same terminology in API documentation, examples and traces. Avoid sign-in language, verified identity indicators and claims of production access protection.

The backend validates the selector against a synthetic allowlist and derives the fixture tenant and customer key. Missing or unrecognised personas fail closed before source access with a generic response. These checks enforce ownership rules within the selected fixture context. Persona selection provides no proof of caller identity or production security boundary. A future production integration must derive the customer identity from a trusted, verified upstream principal and enforce server-side authorisation before status retrieval. The public selector is confined to synthetic fixtures.

Use a dedicated approved fixture set with IDs disjoint from the legacy order and refund fixtures. Include at least two customers in one tenant and at least one customer in another tenant. Expose a read-only source operation scoped by tenant, customer key and canonical Order ID. In the fixture adapter, select the authorised partition before retrieving a status. Return only the canonical ID and current status. A scoped miss produces the same result for unknown, same-tenant foreign and cross-tenant IDs. Keep protected fixtures inaccessible through the legacy support route, refund route, quick-start data and evaluation output for a different persona. The existing support playground remains a tenant-scoped synthetic demonstration and must be labelled accordingly.

### Requirements and conversation flow

| Requirement | Proposed change |
| --- | --- |
| REQ-017 | Recognise natural-language status requests. If the turn has no ID, prompt for one, return an explicit continuation indicator and make zero order-source calls. |
| REQ-018 | Resolve the synthetic persona and fetch the current status using the scoped source operation. A missing or unsupported status takes the unavailable response path. |
| REQ-019 | Distinguish missing input from a malformed ID. Use the same check-and-retry copy for malformed and unknown IDs. Validate before source access and ask for a single ID when multiple distinct references are present. Propose case-insensitive `ORD` with the existing optional hyphen or space and four to six ASCII digits, normalised to hyphenated uppercase and checked as a complete reference. |
| REQ-020 | Require the resolved tenant and customer scope on every lookup. Use the same HTTP status, decision, answer, citations and trace semantics for valid-format unknown and out-of-scope IDs. Keep raw IDs, ownership and record details out of all denial response fields. The per-run UUID remains independent of the result. |
| REQ-021 | Map source unavailability, timeout and adapter errors to friendly retry-later or customer-service copy. Keep exceptions and sensitive values out of the API response and rendered trace. Read the current fixture on each attempt. |
| REQ-022 | Display the canonical ID and a friendly label for the source status. Start with the approved statuses Delivered, Processing and Refunded. Omit fixture notes, delivery dates and personal details. |
| REQ-023 | Handle direct cancellation, status-change and delivery-update requests before status lookup, including mixed status-and-mutation requests. Explain that the requested action is unsupported and perform zero source calls. Preserve informational cancellation-policy questions on the existing support route. |

Keep narrow conversation state in the playground. When the backend returns `awaiting_order_id`, the next request includes optional `continuation: "order_status"` and the message as typed. The API checks safety and recognisable new intent before using the continuation. While pending, it accepts a bare ID or a reply such as “it's ORD-3101”. A malformed or unverified ID keeps the prompt active so the customer can retry. Success, source failure, a recognised topic change, a modification request, a safety block or a handoff clears it. The browser also clears it on persona or mode change and ignores late responses from the old context. Outside a pending exchange, a bare ID prompts the customer to state what they need. API clients can supply the continuation as a routing hint. It carries no session evidence, permissions or previous order data, and every turn independently resolves the persona and checks ownership. Reuse the existing safety and handoff precedence.

## Affected Files and Components

| File or component | Proposed change |
| --- | --- |
| `backend/app/main.py`, `backend/app/models.py` | Register the dedicated route and define its request and response models. Keep the continuation field specific to the new response model. Add SPEC-003 to the existing specification metadata with requirement-to-test links. |
| `backend/app/order_status.py` (new), `backend/app/order_status_fixtures.py` (new) | Implement routing for the customer status workflow, ID parsing, scoped read-only adapter, error translation and presentation. Define personas and disjoint synthetic ownership fixtures. |
| `backend/app/engine.py` | Reuse existing safety checks, response and trace construction where practical. Limit any extraction to helpers with preserved legacy behaviour. |
| `backend/app/evaluations.py` | Add status scenarios with fresh evaluation IDs and preserve existing cases, expected results and evaluation response schema. Keep customer-level privacy assertions in API tests. |
| `frontend/src/App.tsx` | Add the mode, persona selector, continuation handling and scoped transcript and trace updates. Wire synthetic examples to the appropriate mode and persona. Render SPEC-003 using the existing additional-specification view. |
| `backend/tests/test_order_status.py` (new), `backend/tests/test_api.py` | Add source and API coverage for the acceptance scenarios and isolation across routes. Verify SPEC-003 evidence and the existing API contract. |
| `docs/adr/` | Record the approved identity, endpoint and fixture boundary using the repository ADR template after review. |

## Alternatives and Trade-offs

- **Dedicated endpoint and separate fixtures (recommended).** Preserves the existing API and exact legacy examples while isolating customer-level access. Adds a mode and another fixture set to maintain. The project then has two clearly labelled synthetic lookup experiences.
- **Add optional identity to the existing endpoint and reuse its fixtures.** Gives users one lookup interface, but omitted identity would leave the same records reachable via the tenant-only route. Closing that path would change existing callers, evaluation expectations and the pinned answer. This option needs an explicitly approved migration covering both status and refund access.
- **Server-side conversation sessions.** Provide server-controlled continuity across requests and tabs, at the cost of session storage, expiry, lifecycle and deployment decisions. The proposed browser-held routing hint supports the one required follow-up with less data. Continuation ends on reload, and API callers manage their own conversational context.
- **Trusted sign-in or signed demo sessions.** Could verify a caller or bind a session to a persona, with additional provisioning and lifecycle requirements. A backend-validated demo selector is sufficient to exercise ownership rules with synthetic fixtures. Production access requires a trusted upstream identity, an approved source and a separate design review.

## Implementation Sequence

1. After approval, record the architecture decision and establish a baseline from the existing pytest suite, behavioural evaluations and frontend build.
2. Add fixture identity and source contract tests, including same-tenant denial, cross-tenant denial and fixture separation. Implement the scoped read-only source.
3. Add API acceptance tests, then implement routing, ID continuation, safe response mapping and specification traceability. Add behavioural evaluation cases.
4. Connect the playground and exercise the full two-turn flow, including context changes while a response is pending. Run the complete verification suite and record results against the requirements.

## Verification Plan

| Acceptance scenario | Planned automated evidence in `backend/tests/test_order_status.py` |
| --- | --- |
| AC-001 / REQ-017 | `test_missing_id_prompts_without_lookup` checks the prompt and continuation indicator, absence of order information, and zero adapter calls. |
| AC-002 / REQ-018, REQ-022 | `test_authorised_order_displays_id_and_current_status` covers direct and two-turn requests, verifies the source call scope, checks the approved labels and ensures the answer contains only intended order fields. Vary the source result to prove the response uses the current read. |
| AC-003 / REQ-019 | `test_unknown_or_malformed_id_allows_retry` covers both paths, confirms malformed IDs skip the source, checks safe retry copy and verifies that a subsequent valid ID succeeds. Include multiple IDs and parser boundary cases. |
| AC-004 / REQ-020 | `test_foreign_order_matches_unknown_response` compares the entire normalised response for same-tenant foreign, cross-tenant and unknown IDs, excluding the generated run UUID. Check invalid personas fail closed and protected fixture IDs cannot be read through legacy status or refund routes. |
| AC-005 / REQ-021 | `test_source_failure_returns_safe_unavailable_response` injects unavailable, timeout and internal-error outcomes through the adapter, plus missing or unsupported status. Assert retry guidance and absence of fabricated status, existence claims, exception details and stale results. |
| AC-006 / REQ-023 | `test_order_modification_is_unsupported_and_read_only` covers cancellation, status changes and delivery updates, including a pending follow-up and mixed requests. Assert explanatory copy, zero source calls and identical fixture contents before and after. |

- Run `python -m pytest -q` from `backend/` and verify `POST /api/evaluations/run` reports zero failures and retains EV-001–EV-023. Preserve existing tests, including the legacy order answer, cancellation article, refund evidence and trace order, tenant boundaries, request validation, handoff and instruction blocking.
- Run `npm ci` and `npm run build` from `frontend/`. The build runs TypeScript compilation and Vite. Manually exercise the browser flow from prompt to bare-ID response, including bad-ID retry, new topic, persona and mode switch, a delayed response, and the visible simulated-persona wording. Record the browser and observed results.
- **Frontend verification limits.** The repo has no frontend test runner. A successful build checks compilation and bundling. Manual browser checks depend on the reviewer and environment and provide limited repeatability across browsers, network conditions and race sequences. They do not provide a CI regression gate for the interaction. The automated backend tests still cover AC-001 through AC-006.
- **Enterprise verification upgrade.** In a separately approved follow-up, add automated browser tests against a synthetic test environment and run them in CI. Cover the two-turn flow, invalid-ID retries, equivalent denial responses, source failures and context resets. Use controlled response timing to make stale-response races reproducible. Expand to supported browsers and automated accessibility checks, and retain traces or screenshots on CI failure.
- Record actual command results and acceptance evidence during authorised implementation. This planning review did not execute the suites.

## Risks and Unresolved Decisions

- **Access boundary and compatibility.** If customer-level authorisation is required across every existing lookup path, approve a migration first. Verify fixture IDs stay disjoint and the customer API cannot derive permissions from a tenant field, message text or continuation.
- **Error privacy.** The approved identical customer-facing response applies to the answer, decision and trace. Current structured outputs disclose that distinction on the legacy path. The fixture comparison tests cover observable response fields. Production timing and enumeration resistance would need their own design.
- **Conversation and routing.** Broad keyword matches can misroute cancellation-policy questions and refund enquiries, especially when a continuation is pending. Test explicit examples and keep the legacy router's public behaviour covered.
- **Data and presentation.** Use the approved fixture source, initial statuses and ID-and-status-only display. Exercise outages through injected adapter outcomes.
- **Business-impact measurement deferred.** The demo retains functional acceptance tests for AC-001 through AC-006. Measurement of real self-service resolution rates or changes in customer service enquiry volume is deferred to a future production integration. That work will require a live order source, trusted identity, agreed measurement definitions, a baseline and target, and approved instrumentation. Synthetic test results establish functional behaviour only.

## Release Boundary

The Engineering Lead has authorised implementation of these requirements and architectural choices. The authorised implementation scope would cover the components and verification above. Production data or authentication integration, paid services, Render configuration changes, and committing, pushing, merging or deploying require separate approval.
