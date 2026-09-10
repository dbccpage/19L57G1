"""Unit tests for the multi-depth retained-record enablement ladder.

Pins monotonicity, strict inclusion of depth classes, renaming invariance
across 1,152 sweep runs, and audits Lean 4 axioms.
AuthorityEffect: None.
"""

from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import multi_depth as md  # noqa: E402
import verify_lean  # noqa: E402


class TestMultiDepthLadder(unittest.TestCase):
    def test_windows_extraction(self) -> None:
        tape = (10, 20, 30, 40, 50)
        self.assertEqual(
            md.windows(2, tape),
            ((10, 20), (20, 30), (30, 40), (40, 50)),
        )
        self.assertEqual(
            md.windows(3, tape),
            ((10, 20, 30), (20, 30, 40), (30, 40, 50)),
        )
        self.assertEqual(md.windows(5, tape), ((10, 20, 30, 40, 50),))
        self.assertEqual(md.windows(6, tape), ())

    def test_functional_definition(self) -> None:
        # Repeating 0 -> 1 -> 0 -> 1:
        # window length 2: (0, 1), (1, 0), (0, 1), (1, 0)
        # 0 is always followed by 1, 1 is always followed by 0 -> functional in 1 entry
        self.assertTrue(md.functional(1, (0, 1, 0, 1, 0, 1)))

        # 0 followed by 1 and 0 followed by 2:
        # not functional in 1 entry
        self.assertFalse(md.functional(1, (0, 1, 0, 2)))
        # But (0, 1) is followed by 0, (1, 0) is followed by 2 -> functional in 2 entries!
        self.assertTrue(md.functional(2, (0, 1, 0, 2)))

    def test_monotonicity_across_tapes(self) -> None:
        test_tapes = [
            (0, 1, 0, 1, 0, 1),
            (0, 1, 2, 0, 1, 0),
            (0, 1, 2, 3, 0, 1, 2, 0),
            (1, 2, 3, 1, 2, 4, 1, 2, 3),
            (0, 0, 0, 0),
            (0, 1, 2, 3, 4, 5, 6),
        ]
        for tape in test_tapes:
            self.assertTrue(md.check_monotonicity(tape, max_k=8))

    def test_strict_ladder_inclusions(self) -> None:
        """For each k from 1 to 5, twist_tape(k) meets ceiling k + 1
        while breaking ceiling k."""
        for k in range(1, 6):
            tape = md.twist_tape(k)
            self.assertTrue(
                md.functional(k + 1, tape),
                f"twist_tape({k}) failed ceiling {k + 1}",
            )
            self.assertFalse(
                md.functional(k, tape),
                f"twist_tape({k}) should break ceiling {k}",
            )

    def test_renaming_invariance_1152_runs(self) -> None:
        """1,152 is the depth-1 renaming sweep, not the ladder check."""
        sweep = md.run_sweep_verification()
        self.assertEqual(sweep["sweep_runs_checked"], 1152)
        self.assertEqual(sweep["invariance_failures"], 0)
        self.assertTrue(sweep["invariance_verified"])

    def test_runner_exits_nonzero_when_lean_fails(self) -> None:
        import run_multi_depth as runner

        with tempfile.TemporaryDirectory() as tmp:
            argv = ["run_multi_depth.py", "--out", tmp]
            with mock.patch.object(sys, "argv", argv), mock.patch.object(
                runner.verify_lean, "main", return_value=1
            ), mock.patch.object(
                runner.md,
                "run_sweep_verification",
                return_value={"sweep_runs_checked": 0, "invariance_failures": 0},
            ):
                rc = runner.main()
            self.assertEqual(rc, 1)
            receipt = json.loads((pathlib.Path(tmp) / "multi_depth.json").read_text(encoding="utf-8"))
            self.assertFalse(receipt["lean_verification"]["audit_passed"])
            self.assertEqual(receipt["lean_verification"]["axioms"], "BUILD_FAILED")

    def test_lean_audit_clean(self) -> None:
        rc = verify_lean.main()
        self.assertEqual(rc, 0, "Lean 4 audit failed")


if __name__ == "__main__":
    unittest.main()
