# SPEC-001 — Behavioural contract

**Status:** approved for demonstration.

| Requirement | Behaviour | Acceptance evidence |
|---|---|---|
| REQ-001 | SHALL only answer when authorised tenant policy evidence exists, including source citation. | EV-001, EV-002, EV-003, EV-004 |
| REQ-002 | SHALL deny a synthetic order lookup when the tenant does not match. | EV-007, EV-014 |
| REQ-003 | SHALL abstain when authorised evidence or synthetic records do not exist. | EV-009, EV-013 |
| REQ-004 | SHALL expose ordered decisions and tool traces for each run. | test_trace_present |
| REQ-005 | SHALL block known instruction-override phrases. | EV-008 |
| REQ-006 | SHALL run verifiable evaluations without paid model inference. | test_all_acceptance_scenarios_pass and GitHub CI |

Additional cases: missing order reference produces clarification (EV-005); valid synthetic order uses a lookup (EV-006); explicit human request produces simulated handoff without claiming a real ticket (EV-010); policy results remain tenant-specific (EV-011, EV-012).

## Known limitations
- Deterministic keyword routing is not an LLM agent.
- Known-phrase instruction blocking is not comprehensive prompt-injection defence.
- Valid citation references do not guarantee semantic entailment.
- Tenant selection is public; it is not authentication or authorisation for real customer data.
