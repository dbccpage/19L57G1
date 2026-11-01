"""P204 claim boundaries and stale teaching records."""
from fractions import Fraction as F
from pathlib import Path
import json,shutil,subprocess,tempfile,unittest
from textbook.reasoning_lab import valuations as v

class ValuationBoundaries(unittest.TestCase):
    def test_unit_response_is_not_state_normalization(self):
        self.assertEqual(v.effect((1,1)).vector,(1,1));self.assertEqual(v.native.evaluate(v.effect((1,1)),v.state(F(3,4))),1)
    def test_multiply_before_adding(self):self.assertEqual(v.pairing_case(2,3)['answer'],'5/8')
    def test_outcome_order_needs_correspondence(self):self.assertTrue(v.native_limits()['outcome_order_is_part_of_space_identity'])
    def test_strict_caller_mapping(self):
        for mapping in ({0:True,1:0},{0:0.5,1:0.5},{0:1,1:0,99:2}):
            with self.assertRaises(ValueError):v.checked_weights(v.SPACE,mapping)
    def test_joint_choices_are_separate(self):
        p=v.mixture_and_square();self.assertEqual(p['independent_half_half'],'1/2');self.assertEqual(p['coordinated_matching'],'1')
    def test_square_recipes_keep_distinct_weights(self):
        p=v.mixture_and_square();self.assertNotEqual(*p['square_weights']);self.assertEqual(p['square_center'],['1/4']*4)
    def test_selected_branch_is_not_full_sum(self):
        p=v.branch_case(0,0,0);self.assertEqual(p['answer'],'1/2');self.assertEqual(p['rows'][0]['conditional'],'1')
    def test_zero_branch_has_no_conditional_ratio(self):self.assertEqual(v.branch_case(0,2,0)['rows'][1]['conditional'],'undefined')
    def test_native_limits_and_changed_practice(self):self.assertTrue(all(v.native_limits().values()));self.assertEqual(v.practice()['changed_tasks_checked'],8)
    def test_population(self):
        self.assertEqual(v.check_population(),{'pairings':125,'state_mixtures':3125,'complete_partition_comparisons':21875,
            'square_and_indicator_decompositions':35,'bilinear_mixtures':25})
    def test_actual_handlers(self):
        p=subprocess.run(['node',str(v.SOURCE/'test_valuation_controls.mjs')],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)

class ValuationRecords(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.folder=Path(self.temp.name)
        for n in ('valuations.json','valuations.html'):shutil.copyfile(v.SOURCE/n,self.folder/n)
    def inject(self,fn):
        p=self.folder/'valuations.json';d=json.loads(p.read_text(encoding='utf-8'));fn(d);p.write_text(json.dumps(d),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'packet differs'):v.check_recorded(self.folder)
    def test_wrong_pairing(self):self.inject(lambda d:d['cases']['2_3'].update(answer='3/4'))
    def test_selection_is_not_full_sum(self):self.inject(lambda d:d['branches']['0_0_0'].update(answer='1'))
    def test_zero_branch_is_not_ratio_zero(self):self.inject(lambda d:d['branches']['0_2_0']['rows'][1].update(conditional='0'))
    def test_square_recipe_weights_remain_distinct(self):self.inject(lambda d:d['mixtures']['square_weights'].__setitem__(1,d['mixtures']['square_weights'][0]))
    def test_native_Nat_weights_are_not_arbitrary_rationals(self):self.inject(lambda d:d['native_limits'].update(lean_binary_Nat_normalized_weights_are_endpoints=False))
    def test_models_are_not_observations(self):self.inject(lambda d:d.update(physical_observations=44))
    def test_stale_desk(self):
        p=self.folder/'valuations.html';p.write_text(p.read_text(encoding='utf-8')+'stale',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'desk differs'):v.check_recorded(self.folder)

if __name__=='__main__':unittest.main()
