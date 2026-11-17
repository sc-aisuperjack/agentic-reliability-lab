# SPEC-002: Refund Eligibility

Status: Proposed
Related intent: INTENT-002

## Behavioural requirements

REQ-007: Refund intent recognition
WHEN a user asks about refund eligibility for an order,
THE SYSTEM SHALL route the request to the refund eligibility workflow.

REQ-008: Missing order reference
WHEN a refund eligibility question lacks an order ID,
THE SYSTEM SHALL request clarification.

REQ-009: Tenant isolation
WHEN an order belongs to another tenant,
THE SYSTEM SHALL deny access without exposing the order's details.

REQ-010: Policy selection
WHEN evaluating an order,
THE SYSTEM SHALL use the selected tenant's authorised refund policy.

REQ-011: Eligibility assessment
WHEN the order is delivered, unused, and within the permitted return period,
THE SYSTEM SHALL classify it as eligible.

REQ-012: Ineligible orders
WHEN the item is used, outside the return period, or not yet delivered,
THE SYSTEM SHALL return the applicable ineligibility reason.

REQ-013: Missing evidence
WHEN required order or condition information is unavailable,
THE SYSTEM SHALL ask for clarification or abstain rather than assume eligibility.

REQ-014: Refund execution boundary
THE SYSTEM SHALL NOT issue a refund, change an order, or claim a financial action has occurred.

REQ-015: Explainability
THE SYSTEM SHALL include the relevant policy reference and ordered execution trace when making an eligibility determination.

REQ-016: Regression protection
THE SYSTEM SHALL preserve existing refund-policy answers, order tracking and other supported workflows.

## Evaluation rules

- Use a fixed synthetic evaluation date of 2026-11-17.
- Treat the permitted return window as inclusive.
- Atlas: eligible through day 30.
- Beacon: eligible through day 14.
- Do not infer unused condition from delivery status.
- Do not infer a delivery date when it is missing.
- Existing orders must retain their original tenant.
- All test records must be clearly fictional.

## Test fixture requirements

Extend the existing synthetic order records with explicit delivery dates and item-condition data where appropriate.

Include fixtures representing:

- Eligible Atlas order
- Expired Atlas order
- Used Atlas order
- Missing condition information
- Eligible Beacon order
- Expired Beacon order
- Already-refunded order
- Cross-tenant order
- Unknown order

## Output requirements

The user-facing response must distinguish:

- Eligible
- Ineligible
- Needs more information
- Already refunded
- Blocked or unsupported

The API must preserve its existing response fields.

Any additional structured eligibility result should remain backward compatible.

## Acceptance

The feature is complete only when:

- All new acceptance tests pass.
- All existing acceptance tests pass.
- All existing API tests pass.
- The frontend builds successfully.
- The execution trace reflects real operations.
- The solution creates no real refunds.
