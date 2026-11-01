"""Premise failures in the induction teaching examples."""
import unittest
from textbook.reasoning_lab import induction as i

class InductionBoundaries(unittest.TestCase):
    def test_changed_start_is_not_erased(self):
        self.assertEqual(i.count_after(1,2,0),1)
        self.assertNotEqual(i.count_after(1,2,4),2*4)
    def test_late_rule_agrees_then_differs(self):
        self.assertEqual([i.delayed(3,n) for n in range(4)],[0,2,4,6])
        self.assertNotEqual(i.delayed(3,4),8)
    def test_counts_require_declared_domain(self):
        for v in (-1,True,0.5):
            with self.assertRaises(ValueError):i.count_after(0,2,v)
    def test_states_and_rounds_differ(self):
        self.assertTrue(i.strict_bounded((0,1,2,3),3))
        self.assertFalse(i.strict_bounded((0,1,2,3,4),3))
    def test_repeat_breaks_strictness(self):
        self.assertFalse(i.strict_bounded((0,1,2,2),2))
    def test_empty_history_keeps_nonempty_base(self):
        base=i.model.replay([i.model.AdmitDatum('kept')])
        self.assertEqual(i.model.replay([],base),base)
    def test_changed_event_kind_not_covered(self):
        self.assertNotEqual(i.model.replay([i.model.Supply('x'),i.model.AdmitDatum('fresh')]),i.model.EMPTY)
    def test_native_repeat_is_not_fresh_admission(self):
        base=i.model.replay([i.model.AdmitDatum('kept')])
        self.assertEqual(i.model.step(base,i.model.AdmitDatum('kept')),base)
        self.assertNotEqual(i.model.step(base,i.model.AdmitDatum('new')),base)
    def test_declared_population(self):
        self.assertEqual(i.check_population(),dict(counter_cases=390,delayed_rule_comparisons=104,
            bounded_candidate_traces=5461,strictly_increasing_traces=16,supply_histories=63,new_demand_histories=16))

if __name__=='__main__':unittest.main()
