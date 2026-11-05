# Worked scenario: Customer identity change with conflicting evidence

**Synthetic demonstration only; no real customer data or production banking system.**

## Case
A customer requests a change to the recovery phone number. The session is authenticated, but a recent device change and mismatch between a submitted identity document and the authoritative customer profile raise account-takeover concerns.

## Agent responsibilities
1. **Intake agent:** Creates case C-1042, tags requested write as high impact, records consent and source references.
2. **Evidence agent:** Retrieves authorized identity attributes and document-validation signals; stores references rather than duplicating sensitive content.
3. **Risk agent:** Notes device change and attribute conflict; returns evidence-based uncertainty, not a final authorization.
4. **Policy agent:** Applies current policy and detects that the proposed phone-number write requires step-up verification and human review.
5. **Orchestrator:** Preserves shared case context and pauses the write while creating a reviewer task.

## Decision path
- Proposed action: update recovery phone number.
- Policy gate: **DENY AUTOMATIC WRITE / ESCALATE** because high-impact recovery attribute change has unresolved conflicting evidence.
- Human reviewer receives source references, disagreement summary, policy version, and proposed next steps.
- Reviewer requests independent verification; until completed, existing recovery settings remain unchanged.
- After successful verification and documented approval, the authorized service performs the scoped change; independent read-back verifies the new state.

## Example audit event (illustrative)
```json
{
  "case_id": "C-1042",
  "action": "update_recovery_phone",
  "policy_version": "identity-change-v0.1",
  "decision": "ESCALATE_AND_BLOCK_WRITE",
  "reason_codes": ["HIGH_IMPACT_ACTION", "CONFLICTING_EVIDENCE"],
  "human_owner_role": "identity_operations_reviewer",
  "evidence_refs": ["synthetic:doc-17", "synthetic:device-04"],
  "write_executed": false
}
```

## What this demonstrates
The value is not that an AI agent made a faster decision; it is that multiple agents maintained a coherent case record, stopped an unsafe state change, minimized unnecessary human attention on routine cases, and preserved a reconstructable chain of accountability.

## Tests to run
Replace the evidence with a clean match; inject a malicious instruction into an uploaded document; remove the policy service; replay a duplicate write; create two competing agent updates. For each, verify expected block/allow behavior and audit completeness.
