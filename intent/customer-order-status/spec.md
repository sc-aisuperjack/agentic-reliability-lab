# SPEC-003 — Customer Order Status

**Status:** Draft  
**Version:** 0.1.0  
**Created:** 2026-11-17  
**Last Updated:** 2026-11-17  
**Owner:** Engineering Lead  
**Related Intent:** INTENT-003  
**Related Plan:** PLAN-003

## Behavioural Requirements

### REQ-017 — Missing Order ID

WHEN a customer requests the status of an order AND no Order ID has been provided, THE SYSTEM SHALL ask the customer to provide their Order ID.

THE SYSTEM SHALL NOT retrieve or disclose any order information until the required Order ID is provided and the customer's authorisation to access that order has been confirmed.

### REQ-018 — Valid Order ID and Status Retrieval

WHEN a customer requests the status of an order AND provides a valid Order ID AND the customer is authorised to access that order, THE SYSTEM SHALL retrieve the current order status from the approved order information source.

THE SYSTEM SHALL present the retrieved status in a clear, friendly and understandable format.

THE SYSTEM SHALL NOT invent or assume an order status when the information is unavailable.

### REQ-019 — Invalid or Unknown Order ID

WHEN a customer requests the status of an order AND provides an invalid or unknown Order ID, THE SYSTEM SHALL inform the customer that the order could not be found or verified.

THE SYSTEM SHALL ask the customer to check the Order ID and try again.

THE SYSTEM SHALL NOT disclose information about other orders or customers.

THE SYSTEM SHALL NOT invent an order status or claim that an order exists without evidence.

### REQ-020 — Order Authorisation and Access Control

WHEN a customer provides an Order ID AND requests information about that order, THE SYSTEM SHALL verify that the order belongs to the authenticated customer or that the customer is otherwise authorised to access it.

WHEN the customer is not authorised to access the requested order, THE SYSTEM SHALL refuse to disclose its information.

THE SYSTEM SHALL provide a generic response that does not reveal whether the order exists or belongs to another customer.

THE SYSTEM SHALL NOT disclose order status, customer details, or other sensitive information without confirmed authorisation.

### REQ-021 — Order Information Source Unavailable

WHEN a customer requests the status of an order AND the approved order information source is unavailable, times out, or returns an error, THE SYSTEM SHALL inform the customer that the order status cannot currently be retrieved.

THE SYSTEM SHALL provide a clear and friendly message suggesting the customer try again later or contact customer service.

THE SYSTEM SHALL NOT invent an order status, present outdated information as current, or claim that the order does not exist.

THE SYSTEM SHALL NOT expose internal error messages, system details, or sensitive technical information to the customer.

### REQ-022 — Order Status Presentation

WHEN an authorised order status has been successfully retrieved, THE SYSTEM SHALL present the status in clear, customer-friendly language.

THE SYSTEM SHALL display the Order ID and its current status.

THE SYSTEM SHALL NOT display unnecessary personal information or internal system details.

### REQ-023 — Read-Only Order Status Enquiries

WHEN a customer requests the status of an order, THE SYSTEM SHALL retrieve and present order information without modifying the order.

THE SYSTEM SHALL NOT change order statuses, cancel orders, update delivery information, or perform any other order modification.

WHEN a customer requests an order modification, THE SYSTEM SHALL explain that the requested action is not supported by this feature.

## Acceptance Scenarios

### AC-001 — Missing Order ID (REQ-017)

Scenario: Customer does not provide an Order ID Given a customer has been authenticated When the customer asks for their order status And no Order ID has been provided Then the system asks for the Order ID And no order information is disclosed

### AC-002 — Valid Order Status (REQ-018, REQ-022)

Scenario: Customer requests an authorised order Given a customer has been authenticated And an order belongs to that customer When the customer requests its status using the Order ID Then the system retrieves the current order status And presents the Order ID and status clearly

### AC-003 — Unknown Order ID (REQ-019)

Scenario: Customer provides an unknown Order ID Given a customer has been authenticated When the customer provides an unknown Order ID Then the system asks the customer to check the Order ID And does not disclose other order information

### AC-004 — Unauthorised Order (REQ-020)

Scenario: Customer requests another customer's order Given a customer has been authenticated And the requested order belongs to another customer When the customer requests its status Then the system refuses to disclose order information And does not confirm whether the order exists

### AC-005 — Information Source Unavailable (REQ-021)

Scenario: Order information source is unavailable Given a customer has been authenticated And the order information source is unavailable When the customer requests an order status Then the system explains that the status cannot be retrieved And does not invent an order status

### AC-006 — Read-Only Operation (REQ-023)

Scenario: Customer requests an order modification Given a customer has been authenticated When the customer asks to cancel an order Then the system explains that cancellation is not supported And the order remains unchanged

## Constraints and Boundaries

- The feature must use synthetic customer and order data.
- Customers are assumed to be authenticated before accessing the feature.
- Order ownership and authorisation must be verified before disclosing order information.
- The existing application does not provide real customer authentication. Customer-level authorisation must be simulated for this demonstration.
- Order status information must come from an approved, authorised source.
- The system must not invent order information or expose sensitive customer data.
- The feature must be read-only and must not modify existing orders.
- Existing refund eligibility and customer support functionality must continue to work.
- Existing API contracts must remain backward compatible.
- No paid AI services or external production integrations may be introduced without approval.

## Acceptance Evidence

The following tests must demonstrate that each requirement has been satisfied.

| Requirement | Acceptance Test | Expected Result |
| --- | --- | --- |
| REQ-017 | AC-001 | Missing Order ID triggers clarification without disclosing order information. |
| REQ-018 | AC-002 | A valid, authorised Order ID returns the correct status. |
| REQ-019 | AC-003 | Invalid or unknown Order IDs are handled without disclosing sensitive information. |
| REQ-020 | AC-004 | Unauthorised order access is denied without revealing whether the order exists. |
| REQ-021 | AC-005 | An unavailable order source produces a clear error response without invented information. |
| REQ-022 | AC-002 | Order status is presented clearly with the Order ID and without unnecessary personal information. |
| REQ-023 | AC-006 | Order modification requests are rejected and existing order data remains unchanged. |

### Verification Requirements

- Automated tests must cover all seven behavioural requirements.
- Additional tests must cover malformed Order IDs, source timeouts and internal errors.
- All existing automated tests and behavioural evaluations must continue to pass.
- Backend tests must pass using pytest.
- Frontend TypeScript compilation and production build must succeed.
- No unauthorised order information may appear in customer-facing responses.
- Test results must provide evidence of successful execution.
- The feature must not be considered implemented until acceptance and regression tests have passed.

## Open Questions

The following questions must be resolved before implementation is approved:

1. How will authenticated customers and order ownership be represented using synthetic data?
2. What additional behaviour is required beyond the application's existing order-status lookup?
3. Which order statuses must the feature recognise and display?
4. What information should accompany the order status in the customer-facing response?
5. How will unavailable order information sources and timeouts be simulated for testing?
6. Should unknown and unauthorised Order IDs produce identical customer-facing responses?
7. How will the business measure the reduction in customer service enquiries?
8. Which system would provide live order information in a future production implementation?
