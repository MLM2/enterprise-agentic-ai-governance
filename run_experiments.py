"""Run paired-seed Monte Carlo comparisons and write reproducible outputs."""
import argparse
import csv
import json
import math
import statistics
from pathlib import Path
from src.simulation import EXPERIMENTS, make_cases

ROOT = Path(__file__).resolve().parent

def run(n=1000, runs=30, seed=20261105, output=None):
    base = Path(output) if output else ROOT/'results'
    (base/'raw').mkdir(parents=True, exist_ok=True)
    (base/'summaries').mkdir(parents=True, exist_ok=True)
    rows = []
    for repeat in range(runs):
        cases = make_cases(n, seed + repeat)
        for name, (fn, modes) in EXPERIMENTS.items():
            for mode in modes:
                metrics = fn(cases, mode)
                rows.append({'experiment':name,'mode':mode,'run':repeat,'seed':seed+repeat,'cases':n,**metrics})
    fields = ['experiment','mode','run','seed','cases'] + sorted(set().union(*(r.keys() for r in rows)) - {'experiment','mode','run','seed','cases'})
    with (base/'raw'/'experiment_runs.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    summary=[]
    for name, (_, modes) in EXPERIMENTS.items():
        for mode in modes:
            subset=[r for r in rows if r['experiment']==name and r['mode']==mode]
            for metric in fields[5:]:
                vals=[float(r[metric]) for r in subset if metric in r]
                if not vals:continue
                mean=statistics.mean(vals)
                se=statistics.stdev(vals)/math.sqrt(len(vals)) if len(vals)>1 else 0
                summary.append(dict(experiment=name,mode=mode,metric=metric,mean=round(mean,4),ci95_low=round(mean-1.96*se,4),ci95_high=round(mean+1.96*se,4),runs=len(vals)))
    with (base/'summaries'/'summary.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
    metadata={'synthetic':True,'model':'deterministic rule-based simulation','n_per_run':n,'runs':runs,'base_seed':seed,'ci':'normal approximation to mean over independent seeds; descriptive only','limitations':'Rules and outcomes are design assumptions; no LLMs or real customers; no production validation.'}
    (base/'summaries'/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cases',type=int,default=1000);p.add_argument('--runs',type=int,default=30);p.add_argument('--seed',type=int,default=20261105);p.add_argument('--output');a=p.parse_args()
    result=run(a.cases,a.runs,a.seed,a.output)
    for r in result:
        if r['metric'] in ('review_minutes','missed_critical','unsafe_decisions','unauthorized_writes','duplicate_actions','unresolved','reconstructable'):
            print(f"{r['experiment']:16} {r['mode']:16} {r['metric']:22} {r['mean']:9.2f} [{r['ci95_low']:.2f}, {r['ci95_high']:.2f}]")
