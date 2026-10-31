"""Clock scope boundaries and stale teaching artifacts."""
from dataclasses import replace
import json
from pathlib import Path
import shutil,subprocess,tempfile,unittest
from textbook.reasoning_lab import clocks as c

class ClockBoundaries(unittest.TestCase):
    def test_source_clock_schedules_are_different(self):
        self.assertEqual(c.timeline(0,0,3)['answer'],'3')
        self.assertEqual(c.timeline(0,1,3)['answer'],'3/2')
        self.assertEqual(c.timeline(1,0,3)['answer'],'2')
    def test_zero_slow_change_refuses_ratio(self):
        self.assertEqual(c.timeline(0,0,1)['answer'],'refuse')
        self.assertEqual(c.timeline(0,1,1)['answer'],'1')
        self.assertEqual(c.timeline(1,0,0)['answer'],'refuse')
    def test_offsets_are_not_elapsed_changes(self):
        row=c.timeline(1,0,2,offsets=(10,3))
        self.assertEqual(row['rows'][-1]['values'][2:],[14,5]);self.assertEqual(row['answer'],'2')
    def test_negative_horizon_is_rejected(self):
        for bad in (-1,True,1.5):
            with self.assertRaises(ValueError):c.countdown(bad)
    def test_finite_window_excludes_its_next_index(self):
        row=c.countdown(3);self.assertEqual([r['index'] for r in row['rows']],[0,1,2])
        self.assertEqual(row['next'],{'index':3,'left':1,'right':0})
    def test_period_labels_are_not_configuration(self):
        state=replace(c.setup(0),clock_fast=c.native.ClockSubsystem(0,7))
        with self.assertRaisesRegex(ValueError,'periods'):c.checked_python(state)
    def test_native_scope_controls(self):
        self.assertTrue(c.native_limits()['hidden_clocks_can_differ_with_same_register_future'])
    def test_population(self):
        self.assertEqual(c.check_population(),{'clock_runs':1944,'python_readout_comparisons':25920,'countdown_horizons':33})
    def test_handlers(self):
        p=subprocess.run(['node',str(c.SOURCE/'test_clock_controls.mjs')],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)

class ClockRecords(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.folder=Path(self.temp.name)
        for n in ('clocks.json','clocks.html'):shutil.copyfile(c.SOURCE/n,self.folder/n)
    def inject(self,fn):
        p=self.folder/'clocks.json';d=json.loads(p.read_text(encoding='utf-8'));fn(d);p.write_text(json.dumps(d),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'packet differs'):c.check_recorded(self.folder)
    def test_no_silent_clock_bridge(self):self.inject(lambda d:d['cases']['0_0_3'].update(answer='2'))
    def test_empty_comparison_does_not_predict_next(self):self.inject(lambda d:d['countdowns']['0'].update(answer='yes'))
    def test_finite_agreement_is_not_all_future(self):self.inject(lambda d:d['countdowns']['3']['next'].update(right=1))
    def test_zero_updates_are_not_positive_rate(self):self.inject(lambda d:d['cases']['1_0_0'].update(answer='2'))
    def test_observations_are_not_generated(self):self.inject(lambda d:d.update(physical_observations=28))
    def test_stale_desk(self):
        p=self.folder/'clocks.html';p.write_text(p.read_text(encoding='utf-8')+'stale',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'desk differs'):c.check_recorded(self.folder)

if __name__=='__main__':unittest.main()
