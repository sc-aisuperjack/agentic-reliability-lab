# Feature documentation standard

**Version:** 1.0.0  
**Created:** 2026-11-17  
**Last Updated:** 2026-11-17  
**Status:** Approved

## Purpose

Every new feature starts with a folder under `intent/`, for example `intent/customer-order-status/`. Keep its three documents separate:

- **intent.md — WHY:** Problem, desired outcome, business value, scope, exclusions, assumptions and measurable success.
- **spec.md — WHAT:** Observable, testable behaviour, failure cases, constraints and acceptance evidence. Given/When/Then scenarios are welcome but do not automatically run tests.
- **plan.md — HOW:** Implementation approach, affected components, trade-offs, test plan and delivery steps. Usually drafted after the intent and specification are reviewed.

An important architectural choice may also merit a `docs/adr/NNN-name.md` record explaining context, decision, alternatives and consequences.

## Required document header

Each feature document starts with:

```markdown
# INTENT-NNN — Descriptive feature title

**Status:** Draft
**Version:** 0.1.0
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Owner:** Engineering Lead
**Related Specification:** SPEC-NNN
```

Adapt the ID and related-document field for `SPEC-NNN` and `PLAN-NNN`. Replace the date placeholders with **actual ISO 8601 calendar dates** when creating or revising the document. Use **TBD** only for genuinely unknown targets, not for dates already known. Do not predate documents or invent earlier revision history.

## Status and version guidance

- **Draft:** Being written.
- **Proposed:** Ready for review, not yet authorised for implementation.
- **Approved:** Accepted as the current requirement/plan baseline.
- **Implemented:** Corresponding changes are delivered and verified; keep the approval history.
- **Superseded:** Replaced by a newer approved document.

Suggested document versions (a team convention, **not** an industry-mandated format):

- **0.1.0** initial draft; **0.2.0** substantial pre-approval revision.
- **1.0.0** first approved baseline.
- **1.1.0** compatible material revision after approval.
- **2.0.0** change that materially alters an approved contract or scope.
- Fixes limited to spelling/formatting need not change the document version; Git records those edits.

**Document versions are not application release versions.** Git commits track exact file history. Keep the `Last Updated` field accurate on meaningful document edits, and do not claim a document is approved unless the engineering lead has approved it. A status label alone does not enforce approval; use review and CI controls for that.

## Reusable templates

Copy the files in `intent/_templates/` into a **new** feature folder, replace placeholders, and begin with the intent. Do not copy an older feature's business rules into an unrelated specification.

## Requirements traceability

Use stable feature IDs (`INTENT-003`, `SPEC-003`, `PLAN-003` for the next feature, if available), and unique requirement IDs. Existing feature requirements currently run through `REQ-016`; start at `REQ-017` if creating new globally numbered requirements. Link requirements to test cases and actual results. Check IDs before reuse; numbering is a project convention.

## Legacy documents

The first two features predate this metadata convention. Preserve their historical statuses and content unless a separate documentation maintenance change is approved. Apply this standard to new or intentionally revised documents.
