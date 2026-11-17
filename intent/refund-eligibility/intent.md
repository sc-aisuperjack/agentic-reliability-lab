# INTENT-002: Synthetic Refund Eligibility Agent

**Status:** Implemented  
**Version:** 1.0.0  
**Created:** 2026-11-17  
**Last Updated:** 2026-11-17  
**Owner:** Engineering Lead  
**Related Specification:** SPEC-002  
**Target Release:** Refund Eligibility Feature  
**Released:** 2026-11-17

## Problem

The existing application explains general refund policies and can look up synthetic orders.

It cannot determine whether a particular synthetic order satisfies the applicable refund policy.

## Desired outcome

A customer should be able to ask whether an order qualifies for a refund.

The application should retrieve the relevant order, check the selected tenant's policy, assess eligibility, and explain the outcome with evidence.

## Business value

- Reduce unnecessary manual eligibility checks.
- Provide consistent, policy-grounded decisions.
- Demonstrate controlled tool orchestration.
- Show traceable and testable business rules.

## In scope

- Atlas Retail and Beacon Commerce
- Synthetic order records
- Tenant-specific refund eligibility
- Missing-information handling
- Policy citations
- Execution tracing
- Automated evaluations
- React frontend integration

## Out of scope

- Real refund processing
- Payments
- Customer authentication
- Real order databases
- External commerce integrations
- Paid LLM inference

## Success criteria

A user can submit a refund eligibility question and receive a correct, explainable result based on the authorised synthetic data. All existing evaluations must continue to pass. New acceptance tests must demonstrate the eligibility behaviour.

## Non-functional requirements

- No new paid infrastructure.
- No real customer data.
- No unnecessary new dependencies.
- Python 3.14 compatibility.
- Maintain existing public API compatibility.
