# Evaluation framework

## Experimental comparison
- **Baseline A:** Independent agents; humans review every proposed disposition.
- **Baseline B:** Orchestration with selective review but free-form handoff summaries.
- **Candidate C:** Orchestration plus structured context, policy gates, risk-tiered escalation and attributable audit events.

Use the same synthetic cases and matched model/tool configurations for all three conditions. Randomize presentation order for human reviewers; use blinded adjudication where feasible.

## Case categories
Routine verified match; stale address; conflicting identifiers; possible account takeover; duplicate record; missing consent; forged document/prompt injection; unavailable policy service; partial tool failure; simultaneous agent updates.

## Metric definitions
| Metric | Definition | Direction |
|---|---|---|
| Review burden | Total reviewer minutes / 100 cases | Lower |
| Severe control failures | Unauthorized consequential changes / 1,000 cases | Lower; target zero in test |
| Missed escalations | Cases requiring review but not routed / all review-required cases | Lower |
| Context fidelity | Required evidence fields retained correctly / required fields | Higher |
| Decision accuracy | Correct dispositions / adjudicated cases | Higher |
| Audit reconstruction | Cases fully reconstructable / sampled cases | Higher |
| Mean time to resolution | Elapsed intake-to-final disposition by case type | Lower |
| Recovery success | Correctly restored states / attempted recoveries | Higher |

## Illustrative acceptance gates (not validated benchmarks)
- Zero unauthorized consequential writes in the synthetic evaluation suite.
- No missed escalation for predefined critical-risk cases.
- At least 99% complete audit records for evaluated consequential decisions.
- At least 20% lower human review minutes than Baseline A **only if** accuracy and safety gates are met.

## Reporting discipline
Report numerator, denominator, confidence interval where appropriate, model/policy versions, seed, scenario mix, and failures. Include both overall and worst-case subgroup performance. Do not claim measured improvement until the experiments are executed.
