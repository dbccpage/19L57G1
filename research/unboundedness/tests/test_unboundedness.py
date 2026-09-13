"""Unit tests for Target 1 unboundedness and gap analysis.

AuthorityEffect: None.
"""

import unittest
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "code"))
sys.path.insert(0, str(REPO_ROOT / "research" / "unboundedness"))

from derivation.engine import READING_F, READING_L
from unboundedness import (
    run_driver_trajectory,
    verify_closed_system_termination,
    verify_xstep_gap,
)


class TestUnboundedness(unittest.TestCase):
    def _assert_trajectory_unbounded(self, res):
        """Shared assertions for unbounded trajectory tests."""
        self.assertEqual(res["final_depth"], 30)
        self.assertGreaterEqual(res["final_data"], 10)
        self.assertTrue(res["all_states_distinct"])
        self.assertFalse(res["terminal_no_response_encountered"])
        # Check data monotonicity
        traj = res["trajectory"]
        data_seq = [step["data"] for step in traj]
        for i in range(len(data_seq) - 1):
            self.assertLessEqual(data_seq[i], data_seq[i + 1])

    def test_trajectory_unbounded_reading_l(self):
        res = run_driver_trajectory(READING_L, "mu2", target_depth=30)
        self._assert_trajectory_unbounded(res)

    def test_trajectory_unbounded_reading_f(self):
        res = run_driver_trajectory(READING_F, "mu2", target_depth=30)
        self._assert_trajectory_unbounded(res)

    def test_xstep_driver_gap(self):
        gap = verify_xstep_gap()
        self.assertTrue(gap["gap_exists"])
        self.assertEqual(gap["mark_delta_cost"], [2, 1])
        self.assertEqual(gap["subsequent_block_min_cost"], [1, 0])
        self.assertTrue(gap["all_min_responses_are_single_instance"])

    def test_closed_system_terminates(self):
        term = verify_closed_system_termination()
        self.assertEqual(term["L"]["termination_depth"], 1)
        self.assertEqual(term["L"]["collapsed_pairs_remaining"], 0)
        self.assertEqual(term["F"]["termination_depth"], 3)
        self.assertEqual(term["F"]["collapsed_pairs_remaining"], 0)


if __name__ == "__main__":
    unittest.main()
