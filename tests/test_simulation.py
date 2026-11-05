import unittest
from src.simulation import make_cases, EXPERIMENTS
from run_experiments import run
from tempfile import TemporaryDirectory

class SimulationTests(unittest.TestCase):
    def test_repeatability(self):
        self.assertEqual(make_cases(100,42),make_cases(100,42))
    def test_every_critical_case_reviewed(self):
        cases=make_cases(5000,123)
        for mode in ('universal','risk_tiered','context_aware'):
            self.assertEqual(EXPERIMENTS['supervision'][0](cases,mode)['missed_critical'],0)
    def test_preaction_blocks_unauthorized(self):
        cases=make_cases(1000,17)
        self.assertEqual(EXPERIMENTS['authorization'][0](cases,'preaction')['unauthorized_writes'],0)
    def test_idempotency(self):
        cases=make_cases(1000,17)
        self.assertEqual(EXPERIMENTS['coordination'][0](cases,'idempotent')['duplicate_actions'],0)
    def test_output_reproducibility(self):
        with TemporaryDirectory() as a, TemporaryDirectory() as b:
            run(100,3,42,a);run(100,3,42,b)
            from pathlib import Path
            self.assertEqual((Path(a)/'raw/experiment_runs.csv').read_bytes(),(Path(b)/'raw/experiment_runs.csv').read_bytes())

if __name__=='__main__':unittest.main()
