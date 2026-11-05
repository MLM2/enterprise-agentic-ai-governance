"""Deterministic, synthetic identity governance experiments. No real customer data or LLM calls."""
import random
from dataclasses import dataclass

@dataclass(frozen=True)
class Case:
    id: int
    risk: str
    ambiguous: bool
    context_missing: bool
    policy_conflict: bool
    unauthorized: bool
    credential_expired: bool
    failure: str

RISKS = ('low', 'medium', 'high', 'critical')

def make_cases(n: int, seed: int):
    rng = random.Random(seed)
    result = []
    for i in range(n):
        risk = rng.choices(RISKS, weights=[.55, .27, .14, .04])[0]
        result.append(Case(i, risk, rng.random()<.14, rng.random()<.16,
                           rng.random()<.08, rng.random()<.08, rng.random()<.06,
                           rng.choices(['none','duplicate','timeout','delay','conflict'],[.68,.09,.09,.08,.06])[0]))
    return result

def exp_supervision(cases, mode):
    reviews = missed = 0
    minutes = 0.
    for c in cases:
        if mode == 'universal':
            review = True
        elif mode == 'risk_tiered':
            review = c.risk in ('high','critical')
        else:
            review = c.risk in ('high','critical') or c.ambiguous or c.context_missing or c.policy_conflict
        reviews += review
        minutes += 3.5 if review else 0.12
        missed += int(c.risk == 'critical' and not review)
    return dict(reviews=reviews, review_minutes=round(minutes,2), missed_critical=missed)

def exp_context(cases, mode):
    errors = recovered = missing = 0
    for c in cases:
        if not c.context_missing: continue
        missing += 1
        if mode == 'unversioned':
            errors += 1
        elif mode == 'versioned':
            # An explicit source record is recoverable for some, not all, missing fields.
            if c.id % 4 == 0: errors += 1
            else: recovered += 1
        else:
            # An unresolved missing field blocks consequential decisions instead of guessing.
            recovered += 1  # safely contained, not reconstructed
    return dict(context_events=missing, unsafe_decisions=errors, recovered_or_contained=recovered)

def exp_authorization(cases, mode):
    unauthorized_writes = false_denials = blocked = 0
    for c in cases:
        bad = c.unauthorized or c.credential_expired
        if mode == 'posthoc':
            unauthorized_writes += int(bad)
        elif mode == 'preaction':
            blocked += int(bad)
        else:
            blocked += int(bad)
            # Conservative fallback blocks a small subset of valid, ambiguous requests.
            false_denials += int(not bad and c.ambiguous and c.id % 5 == 0)
    return dict(unauthorized_writes=unauthorized_writes, blocked=blocked, false_denials=false_denials)

def exp_coordination(cases, mode):
    duplicate_actions = unresolved = recovered = 0
    for c in cases:
        f = c.failure
        if f == 'none': continue
        if mode == 'naive':
            duplicate_actions += int(f == 'duplicate')
            unresolved += int(f in ('timeout','delay','conflict'))
        elif mode == 'idempotent':
            unresolved += int(f in ('timeout','delay','conflict'))
            recovered += int(f == 'duplicate')
        else:
            # Deduplication, bounded retry and explicit conflict escalation.
            recovered += int(f in ('duplicate','timeout','delay'))
            unresolved += int(f == 'conflict')
    return dict(duplicate_actions=duplicate_actions, unresolved=unresolved, recovered=recovered)

def exp_accountability(cases, mode):
    reconstructable = attributable = 0
    for c in cases:
        if mode == 'minimal':
            ok = c.id % 5 == 0
            who = c.id % 4 == 0
        elif mode == 'correlated':
            ok = c.id % 10 != 0
            who = c.id % 12 != 0
        else:
            ok = who = True
        reconstructable += ok
        attributable += who
    return dict(reconstructable=reconstructable, attributable=attributable)

EXPERIMENTS = {
    'supervision': (exp_supervision, ['universal','risk_tiered','context_aware']),
    'context': (exp_context, ['unversioned','versioned','fail_closed']),
    'authorization': (exp_authorization, ['posthoc','preaction','conservative']),
    'coordination': (exp_coordination, ['naive','idempotent','recovery']),
    'accountability': (exp_accountability, ['minimal','correlated','complete']),
}
