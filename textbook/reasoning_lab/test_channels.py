"""Selected channel claims, actual controls and stale-record refusals."""
from fractions import Fraction as F
from pathlib import Path
import json,shutil,subprocess,tempfile,unittest
from textbook.reasoning_lab import channels as c

class ChannelBoundaries(unittest.TestCase):
    def test_order_is_not_bracketing(self):self.assertEqual(c.order_case(1,2)['answer'],'no')
    def test_both_rows_define_equality(self):self.assertEqual(c.order_case(0,1)['answer'],'yes')
    def test_normalized_rows(self):
        with self.assertRaises(c.native.UnnormalizedDistributionError):c.make_channel(((F(1,4),F(1,4)),(0,1)))
    def test_exact_book_input_guard(self):
        for v in (True,0.1,-1,2):
            with self.assertRaises(ValueError):c.exact(v)
    def test_declared_binary_shape(self):
        with self.assertRaises(ValueError):c.make_channel(((1,0),))
    def test_postprocessor_cannot_split_equal_records(self):self.assertEqual(c.record_case(0,1)['processed'],[1,1])
    def test_invertible_processing_retains_difference(self):self.assertEqual(c.record_case(1,1)['answer'],'yes')
    def test_reset_can_lose_difference(self):self.assertEqual(c.record_case(1,2)['answer'],'no')
    def test_limits_and_changed_tasks(self):self.assertTrue(all(c.limits().values()));self.assertEqual(c.practice()['changed_tasks_checked'],7)
    def test_population(self):self.assertEqual(c.check_population(),dict(quarter_grid_compositions=625,output_distributions=3125,named_associative_triples=216,deterministic_pair_comparisons=96))
    def test_actual_controls(self):
        p=subprocess.run(['node',str(c.SOURCE/'test_channel_controls.mjs')],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)

class ChannelRecords(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.folder=Path(self.temp.name)
        for n in ('channels.json','channels.html'):shutil.copyfile(c.SOURCE/n,self.folder/n)
    def inject(self,fn):
        p=self.folder/'channels.json';d=json.loads(p.read_text(encoding='utf-8'));fn(d);p.write_text(json.dumps(d),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'packet differs'):c.check_recorded(self.folder)
    def test_swap_is_not_associativity(self):self.inject(lambda d:d['orders']['1_2'].update(answer='yes'))
    def test_reverse_rows_retained(self):self.inject(lambda d:d['orders']['1_2'].update(reverse_rows=d['orders']['1_2']['forward_rows']))
    def test_no_new_stored_distinction(self):self.inject(lambda d:d['records']['0_1'].update(answer='yes'))
    def test_fixed_input_distribution_not_channel_identity(self):self.inject(lambda d:d['native_limits'].update(one_preparation_does_not_identify_channel=False))
    def test_native_float_helper_limit_retained(self):self.inject(lambda d:d['native_limits'].update(native_binary_helper_accepts_exact_binary_float_value=False))
    def test_models_not_observations(self):self.inject(lambda d:d.update(physical_observations=45))
    def test_stale_desk(self):
        p=self.folder/'channels.html';p.write_text(p.read_text(encoding='utf-8')+'stale',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'desk differs'):c.check_recorded(self.folder)

if __name__=='__main__':unittest.main()
