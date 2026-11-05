"""Render summary figures; no seaborn or hard-coded visual styling."""
import csv
from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
rows=list(csv.DictReader((ROOT/'results/summaries/summary.csv').open()))
out=ROOT/'results/figures';out.mkdir(exist_ok=True,parents=True)
plots=[('supervision','review_minutes','Supervisory workload','Minutes per 1,000 cases','supervision_workload.png'),('context','unsafe_decisions','Unsafe context decisions','Count per 1,000 cases','context_decisions.png'),('authorization','unauthorized_writes','Unauthorized side effects','Count per 1,000 cases','authorization.png'),('coordination','unresolved','Unresolved coordination failures','Count per 1,000 cases','coordination.png'),('accountability','reconstructable','Reconstructable decision traces','Count per 1,000 cases','accountability.png')]
for experiment,metric,title,ylabel,filename in plots:
    d=[r for r in rows if r['experiment']==experiment and r['metric']==metric]
    fig,ax=plt.subplots(figsize=(7,4.3))
    ax.bar([r['mode'].replace('_','\n') for r in d],[float(r['mean']) for r in d])
    ax.set_title(title+' (synthetic simulation)');ax.set_ylabel(ylabel)
    fig.tight_layout();fig.savefig(out/filename,dpi=160);plt.close(fig)
print('Wrote',len(plots),'figures to',out)
