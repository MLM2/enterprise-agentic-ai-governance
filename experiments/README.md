# Experimental protocol

## Objective
Compare governance mechanisms on the *same* synthetic identity cases, holding case mix and failure injections constant within each run. The unit of replication is a generated batch of 1,000 cases; 30 batches use independent pseudorandom seeds.

## Models and assumptions
The agents are **deterministic rule functions**, not LLMs. Risk labels are assumed correct. Every human review costs 3.5 minutes; automatic decisions cost 0.12 minutes. Case features are independently generated with fixed probabilities; they are not estimated from a bank's actual traffic. The versioned context, recovery and logging modes have stipulated capabilities. Some failures and audit outcomes are assigned by case ID modulo, making their rates particularly artificial. Consequently, differences are demonstrations of specified control logic, not empirical estimates of real-world improvements.

## Hypotheses and falsification opportunities
1. Tiered review reduces review minutes. This is expected by construction. **Next falsification test:** inject misclassified high-risk cases, calibrate error rates and measure safety-workload Pareto curves.
2. Context provenance lowers unsafe action counts. **Next:** vary source integrity, recovery coverage and false provenance.
3. Pre-action authorization prevents unauthorized side effects. **Next:** simulate policy engine failures, stale entitlements and bypass attempts.
4. Idempotency and bounded recovery reduce duplicates and unresolved errors. **Next:** simulate partial writes and retry races.
5. Correlated logging improves reconstructability. **Next:** test dropped logs, malicious tampering and independent incident reconstruction.

## Evaluation
Paired case generation means differences between policies should be calculated per seed, not treated as independent samples. Reported 95% intervals in summary.csv are descriptive normal-approximation confidence intervals for each mode's mean across 30 seeds, **not** uncertainty about real-world performance. Zero observed misses cannot demonstrate zero underlying failure probability; some zeros are enforced by implementation.

## Reproduce
From repository root (Python 3.10+):

```bash
python -m unittest discover -s tests -v
python run_experiments.py --cases 1000 --runs 30 --seed 20261105
python make_figures.py
```

No external packages are needed to run the experiments. Figures require matplotlib (`pip install -r requirements.txt`). The generated CSVs and figures are committed as an example execution. Inspect `results/summaries/metadata.json` for run parameters.

## Privacy and security
All cases are synthetic, no names, PII, credentials, customer data or real system connections. This is not a banking control certification or a fairness assessment.
