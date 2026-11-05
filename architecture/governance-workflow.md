# Governance workflow

1. **Intake:** Create case ID and classify action criticality.
2. **Plan:** Orchestrator assigns bounded tasks to authorized agents.
3. **Gather:** Agents retrieve minimally necessary evidence with provenance.
4. **Reconcile:** Context service flags contradictions, missing sources and stale records.
5. **Evaluate:** Policy gate checks authority, action constraints and evidence sufficiency.
6. **Escalate:** High-risk or contested cases go to named human owner with summarized evidence and uncertainties.
7. **Execute:** Authorized tool performs scoped, idempotent change; record outcome.
8. **Verify:** Independent check confirms expected system state.
9. **Audit:** Retain decision event, policy version, responsible actor, evidence references and remediation path.
10. **Learn:** Review false escalations, misses, drift and workload; update thresholds through change control.

**No silent approval:** Timeouts and unavailability cannot be treated as consent for consequential actions.
