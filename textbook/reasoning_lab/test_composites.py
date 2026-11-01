"""Composite inference limits and stale records, outside research custody."""
import json,shutil,subprocess,tempfile,unittest
from pathlib import Path
from textbook.reasoning_lab import composites as c

class CompositeBoundaries(unittest.TestCase):
    def test_shared_name_even_same_value_is_refused(self):
        with self.assertRaises(ValueError):c.native.CarrierState({'x':2}).tensor(c.native.CarrierState({'x':2}))
    def test_relay_order_and_baseline(self):
        s=c.state((4,2,9,6));b,t=c.apply_procedure(1,s);b2,t2=c.apply_procedure(2,s)
        self.assertEqual(c.fields(b),[4,2,2,6]);self.assertEqual(b,b2)
        self.assertEqual(c.fields(t),[4,3,3,6]);self.assertEqual(c.fields(t2),[4,3,2,6])
    def test_equal_shares_do_not_keep_paired_rows(self):
        row=c.network_case(1,3,0);self.assertEqual(row['answer'],'0');self.assertEqual(row['marks_changed'],2)
    def test_repeats_count_and_coarse_readout_hides(self):
        row=c.network_case(3,3,0);self.assertEqual(row['answer'],'1/2');self.assertEqual(row['marks_changed'],4)
        coarse=c.network_case(3,3,2);self.assertEqual(coarse['answer'],'0');self.assertEqual(coarse['b_fields_changed'],4)
    def test_available_graph_executes_nothing(self):
        self.assertEqual(c.graph_case(1,0)['executed_operations'],0)
    def test_constant_multiwrite_adds_edge_without_copy(self):
        self.assertEqual(c.graph_case(2,0)['answer'],'3')
        op=c.graph_operations(2)[-1];self.assertEqual(c.fields(op.apply(c.state((0,2,3,0)))),[0,7,8,0])
    def test_hidden_read_can_escape_graph(self):
        self.assertEqual(c.graph_case(3,1)['answer'],'unreachable')
        self.assertEqual(c.graph_operations(3)[-1].apply(c.state((0,2,0,0)))['b1'],2)
    def test_native_guards_have_scoped_limits(self):self.assertTrue(all(c.native_limits().values()))
    def test_nonnegative_teaching_inputs(self):
        for v in ((0,-1,0,0),(0,True,0,0),(0,1.5,0,0)):
            with self.assertRaises(ValueError):c.state(v)
    def test_population(self):
        self.assertEqual(c.check_population(),{'state_procedure_readout_cases':1134,'ordered_list_comparisons':5115,
            'graph_pair_distances':1024,'graph_permutations':1536,'composition_triples':64})
    def test_handlers(self):
        p=subprocess.run(['node',str(c.SOURCE/'test_composite_controls.mjs')],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)

class CompositeRecords(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.folder=Path(self.temp.name)
        for n in ('composites.json','composites.html'):shutil.copyfile(c.SOURCE/n,self.folder/n)
    def inject(self,fn):
        p=self.folder/'composites.json';d=json.loads(p.read_text(encoding='utf-8'));fn(d);p.write_text(json.dumps(d),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'packet differs'):c.check_recorded(self.folder)
    def test_share_equality_is_not_row_equality(self):self.inject(lambda d:d['cases']['1_3_0'].update(marks_changed=0))
    def test_relay_order_is_not_erased(self):self.inject(lambda d:d['cases']['0_2_0'].update(answer='1'))
    def test_graph_is_not_execution(self):self.inject(lambda d:d['graphs']['1_0'].update(executed_operations=1))
    def test_declared_reads_do_not_certify_callback(self):self.inject(lambda d:d['graphs']['3_1'].update(answer='1'))
    def test_constants_do_not_remove_declared_edge(self):self.inject(lambda d:d['graphs']['2_0'].update(answer='unreachable'))
    def test_no_generated_physical_observations(self):self.inject(lambda d:d.update(physical_observations=60))
    def test_stale_desk(self):
        p=self.folder/'composites.html';p.write_text(p.read_text(encoding='utf-8')+'stale',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'desk differs'):c.check_recorded(self.folder)

if __name__=='__main__':unittest.main()
