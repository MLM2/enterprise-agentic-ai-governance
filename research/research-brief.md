# Research brief: Supervising agentic AI at enterprise scale

## Research question
How can enterprises coordinate many autonomous processes while preserving operational context, controlling human supervisory burden, and retaining accountability for consequential decisions?

## Problem definition
Agents can initiate tool calls, hand off tasks, and generate decisions faster than human reviewers can examine every intermediate step. Unbounded autonomy creates risks of context loss across handoffs, cascading errors, alert fatigue, unclear ownership, unauthorized actions, and incomplete audit trails.

## Hypotheses
- **H1 — Risk-tiered supervision:** Reviewing only policy-defined consequential or low-confidence decisions reduces review load without increasing severe control failures relative to reviewing every step.
- **H2 — Context provenance:** Structured, versioned case context reduces handoff errors and rework compared with free-form conversation summaries.
- **H3 — Pre-action policy gates:** Authorization checks before irreversible tool actions reduce unauthorized state changes compared with post-hoc monitoring alone.
- **H4 — Decision accountability:** A named business owner, recorded policy version, and trace ID for each consequential decision improve investigation and remediation speed.

## Proposed method
Use a synthetic identity case dataset with routine, ambiguous, conflicting, and adversarial cases. Compare three orchestration designs: (A) independent agents with manual review of all outputs, (B) orchestrated agents with selective review but no structured context provenance, and (C) orchestrated agents with risk-tiered review, signed/versioned context references, pre-action gates, and decision logging. Hold cases and underlying model configurations constant where feasible; repeat trials with controlled random seeds and record uncertainty.

## Primary outcomes
Human review minutes per 100 cases; severe unauthorized-action rate; missed escalation rate; context omission rate; incorrect identity disposition rate; mean time to reconstruct a decision; time to resolve exceptions; successful rollback rate. Report both mean and tail outcomes and separate false positives from false negatives.

## Interpretation
A reduction in human review volume alone is not success. A design passes only if safety-critical controls meet predetermined limits and review burden decreases without material deterioration in decision quality. Any claimed benefit must be based on observed test results, not this proposal.

## Threats to validity
Synthetic cases may underrepresent real operational ambiguity; model behavior may drift; test labels may be imperfect; reviewers may adapt to interfaces; policies vary by jurisdiction and institution. Independent review, sensitivity analysis, and production shadow testing would be needed before adoption.

## Research extensions
Investigate adaptive review budgets, uncertainty calibration, agent-to-agent provenance, policy-as-code, cross-agent memory poisoning, human factors in escalation queues, and evidence retention under privacy constraints.
