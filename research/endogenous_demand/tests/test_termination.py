"""Run the termination-bound checks under this tree's own test step.

AuthorityEffect: None.

`verify_termination.py` is the Python evidence CL-ED-BOUND cites.  Until
2026-09-24 nothing in `verify.py` ran it: its suite ran only by hand with
`--unittest`, and the coverage step measured it at 0%, so `verify.py`
failed at coverage on main.  Importing its TestCase here makes the declared
runner (`unittest discover -s tests`) collect and run it.
"""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verify_termination as vt  # noqa: E402
from verify_termination import TestEndogenousDemandObstruction  # noqa: E402,F401


class TerminationGuards(unittest.TestCase):
    def test_small_carriers_have_no_pairs(self) -> None:
        self.assertEqual(vt.binom2(0), 0)
        self.assertEqual(vt.binom2(1), 0)
        self.assertEqual(vt.all_carrier_pairs(1), [])

    def test_invalid_initial_pair_is_refused_by_name(self) -> None:
        with self.assertRaisesRegex(ValueError, r"Invalid requirement pair \(1, 1\) for carrier 3"):
            vt.RegimeState.initial(3, [(1, 1)])

    def test_step_refuses_out_of_carrier_and_repeated_targets(self) -> None:
        state = vt.RegimeState.initial(3, [(0, 1)])
        outside = vt.endogenous_step(state, selector=lambda _candidates: (0, 3))
        self.assertFalse(outside.success)
        self.assertEqual(outside.state, state)
        repeated = vt.endogenous_step(state, selector=lambda _candidates: (0, 1))
        self.assertFalse(repeated.success)
        self.assertEqual(repeated.state, state)

    def test_empty_candidate_lists_select_nothing(self) -> None:
        for selector in (vt.select_minimum_response, vt.select_maximum_response,
                         vt.select_reverse_pair):
            with self.subTest(selector=selector.__name__):
                self.assertIsNone(selector([]))

    def test_step_guard_bounds_a_trace(self) -> None:
        trace = vt.run_endogenous_trace(vt.RegimeState.initial(5), max_steps_guard=3)
        self.assertEqual(trace.steps_taken, 3)
        self.assertFalse(trace.terminated)

    def test_report_runs_and_states_the_open_remainder(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(vt.main(), 0)
        self.assertIn("ALL VERIFICATION CHECKS PASSED", out.getvalue())
        self.assertIn("remains OPEN", out.getvalue())


if __name__ == "__main__":
    unittest.main()
