# INTENT-003 — Customer Order Status

**Status:** Approved\
**Version:** 1.0.0\
**Created:** 2026-11-17  
**Last Updated:** 2026-11-17  
**Owner:** Engineering Lead  
**Related Specification:** SPEC-003  
**Target Release:** TBD

## Problem

Customers need a simple way to find out the current status of their orders without contacting customer service.

The existing application supports basic synthetic order lookups, but the business wants a more natural conversational experience where customers can ask about their orders and receive clear status information.

Routine order-status enquiries can consume valuable customer service time and create unnecessary effort for customers.

## Desired Outcome

Customers should be able to ask for the status of their order through a conversational interface and receive an accurate, understandable response.

If an order ID has not been provided, the system should request it before proceeding.

The customer should receive the information without requiring human assistance whenever possible.

## Business Value

- **Reduced customer service workload:** Fewer telephone calls and routine enquiries about order status.
- **Improved customer experience:** Customers can obtain order information quickly and conveniently.
- **Operational efficiency:** Customer service representatives can focus on more complex enquiries.
- **Improved accessibility:** Customers can request order information through a simple conversation.

## In Scope

- Customers can request their current order status using natural language.
- The system can request an order ID when one has not been provided.
- Customers can provide their order ID during the conversation.
- The system retrieves the current status of the requested order from an approved data source.
- The system presents the order status in a clear, friendly and understandable format.
- The system handles missing, invalid or unavailable order information appropriately.
- Order information must only be disclosed to authorised customers.

## Out of Scope

- Developing a new customer authentication system.
- Changing or cancelling orders.
- Updating order information.
- Requesting detailed delivery tracking or delivery arrangements.
- Processing refunds or returns.
- Integrating real customer order databases as part of the initial synthetic demonstration.

## Assumptions and Dependencies

- Customers are assumed to have already completed authentication and identity verification before accessing this feature.
- The existing application currently uses synthetic order information.
- An approved order-information source must be available for retrieving order statuses.
- Access to real customer order information will require verified authentication and authorisation controls before production use.
- The feature depends on the availability and accuracy of the underlying order information.

## Success Criteria

The feature will be considered successful when:

- Customers can request their order status through natural language.
- Customers can provide an order ID and receive the correct available status.
- The system requests an order ID when one is missing.
- Customers receive a clear response when an order cannot be found or its status is unavailable.
- The system does not disclose order information outside authorised access.
- The business can measure how many order-status enquiries are resolved without human assistance.

**Business impact objective:** Reduce the number of routine customer service telephone calls relating to order-status enquiries.

A measurable reduction target should be agreed with the business before launch.

## Open Questions

- What additional capabilities are required beyond the application's existing synthetic order lookup?
- Which order statuses must be supported?
- What format should be used to present order-status information?
- What should happen if the customer provides an invalid or unknown order ID?
- Which existing system will provide order information in a production environment?
- How will the business measure the reduction in customer service enquiries?
