"""Tests for the retained-record reader and history-dependent execution.

AuthorityEffect: None.
"""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO / "code"))
sys.path.insert(0, str(ROOT.parent / "setting_translation"))
sys.path.insert(0, str(ROOT.parent / "represented_execution"))
sys.path.insert(0, str(ROOT))

import control as ct  # noqa: E402
import reader as rd  # noqa: E402
import runner as rn  # noqa: E402
import translation as tr  # noqa: E402


def demo_setting() -> rd.Recorded:
    """A 2-state setting with flip (op 0) and id (op 1).

    AuthorityEffect: None.
    """
    base = tr.FiniteSetting(
        2, tr.NONE, tr.NONE, tr.NONE, 0, 1,
        ((1, 0), (0, 1))
    )
    # At active 0: if previous is 0, op 0 (flip) enabled; if previous is 1, op 1 (id) enabled.
    hctrl = frozenset({(0, 0, 0), (1, 0, 1)})
    return rd.Recorded(base, hctrl)


class TestReader(unittest.TestCase):
    """Unit tests for the retained-record reader.

    AuthorityEffect: None.
    """

    def test_previous_reading_from_tape(self) -> None:
        """Test previous datum extraction across different tape lengths.

        AuthorityEffect: None.
        """
        C = demo_setting()
        self.assertEqual(rd.nops(C), len(C.F.ops))
        self.assertEqual(rd.nops(C), len(tr.encode(C.F).forms) - 3)
        g = rd.rprogram(C)
        s_initial = ct.State(g, 2, 0, (0,), 0, 5)
        # On tape with 1 entry, previous returns active datum
        self.assertEqual(rd.previous(s_initial), 0)

        s_step1 = ct.State(g, 2, 0, (1, 0), 1, 4)
        # On tape with 2 entries, previous returns second-to-last datum
        self.assertEqual(rd.previous(s_step1), 1)

        s_step2 = ct.State(g, 2, 0, (0, 1, 0), 2, 3)
        self.assertEqual(rd.previous(s_step2), 1)

    def test_history_dependent_futures_exhibit(self) -> None:
        """Exhibit two states with the same active datum and tapes of length 2
        yielding different enablements, successors, and futures.

        AuthorityEffect: None. Requires ``len(tape) >= 2``.
        """
        C = demo_setting()
        g = rd.rprogram(C)
        s1 = ct.State(g, 2, 0, (0, 0), 0, 5)
        s2 = ct.State(g, 2, 0, (1, 0), 0, 5)

        # Same active datum
        self.assertEqual(s1.active, s2.active)
        self.assertEqual(s1.active, 0)

        # Different tapes and different previous data
        self.assertNotEqual(s1.tape, s2.tape)
        self.assertEqual(rd.previous(s1), 0)
        self.assertEqual(rd.previous(s2), 1)
        self.assertNotEqual(rd.previous(s1), rd.previous(s2))

        # Different enablements
        read1 = rd.record_reader(s1)
        read2 = rd.record_reader(s2)
        self.assertEqual(read1, (0,))
        self.assertEqual(read2, (1,))
        self.assertNotEqual(read1, read2)

        # Different successors
        succ1 = rd.rsuccessors(s1)
        succ2 = rd.rsuccessors(s2)
        self.assertEqual(len(succ1), 1)
        self.assertEqual(len(succ2), 1)
        self.assertEqual(succ1[0].active, 1)  # flip 0 -> 1
        self.assertEqual(succ2[0].active, 0)  # id 0 -> 0
        self.assertNotEqual(succ1[0].active, succ2[0].active)

        # Different deterministic steps / futures
        next1 = rn.step_det_of(rd.record_reader, s1)
        next2 = rn.step_det_of(rd.record_reader, s2)
        self.assertIsInstance(next1, ct.State)
        self.assertIsInstance(next2, ct.State)
        assert isinstance(next1, ct.State) and isinstance(next2, ct.State)
        self.assertEqual(next1.active, 1)
        self.assertEqual(next2.active, 0)
        self.assertNotEqual(next1.active, next2.active)
        self.assertNotEqual(next1.tape, next2.tape)

    def test_simulation_soundness_and_completeness(self) -> None:
        """Test simulation and reflection against reference step rstep.

        AuthorityEffect: None.
        """
        C = demo_setting()
        g = rd.rprogram(C)
        for prev in (0, 1):
            s = ct.State(g, 2, 0, (prev, 0), 0, 3)
            succs = rd.rsuccessors(s)
            # Soundness: each successor realises rstep
            for s_prime in succs:
                matched = any(rd.rstep(C, prev, 0, k, s_prime.active) for k in range(rd.nops(C)))
                self.assertTrue(matched)
            # Completeness: each valid rstep is realised by a successor
            for k in range(rd.nops(C)):
                y = C.F.ops[k][0]
                if rd.rstep(C, prev, 0, k, y):
                    self.assertTrue(any(s_prime.active == y for s_prime in succs))

    def test_twist_history_dependence(self) -> None:
        """Test a 3-point setting where returns to datum 0 branch differently.

        AuthorityEffect: None.
        """
        # Setting with 3 points, cycle (0), constant 0 (1), climb (2)
        base = tr.FiniteSetting(
            3, tr.NONE, tr.NONE, tr.NONE, 0, 1,
            ((1, 2, 0), (0, 0, 0), (1, 2, 2))
        )
        # Enablement: (0, 0) -> op 0 (cycle); (0, 1) -> op 1 (const 0); (1, 0) -> op 1 (const 0)
        hctrl = frozenset({(0, 0, 0), (0, 1, 1), (1, 0, 1)})
        C = rd.Recorded(base, hctrl)
        s = rd.rinit(C, 0, 3)
        # Run 3 steps: 0 -> 1 -> 0 -> 0
        s1 = rn.step_det_of(rd.record_reader, s)
        assert isinstance(s1, ct.State)
        self.assertEqual(s1.active, 1)
        self.assertEqual(s1.tape, (0, 1))

        s2 = rn.step_det_of(rd.record_reader, s1)
        assert isinstance(s2, ct.State)
        self.assertEqual(s2.active, 0)
        self.assertEqual(s2.tape, (0, 1, 0))

        # At step 2, active is 0, but previous is 1 (not 0)
        self.assertEqual(s2.active, s.active)
        self.assertNotEqual(rd.previous(s2), rd.previous(s))

        s3 = rn.step_det_of(rd.record_reader, s2)
        assert isinstance(s3, ct.State)
        self.assertEqual(s3.active, 0)
        self.assertEqual(s3.tape, (0, 1, 0, 0))

        # First exit from 0 was to 1; second exit from 0 was to 0
        self.assertEqual(s1.active, 1)
        self.assertEqual(s3.active, 0)
        self.assertNotEqual(s1.active, s3.active)

    def test_lean_reader_axioms(self) -> None:
        """Verify that lake env lean Reader.lean uses only {propext, Quot.sound}.

        AuthorityEffect: None.
        """
        lean_dir = ROOT / "lean"
        result = subprocess.run(
            ["lake", "env", "lean", "Reader.lean"],
            cwd=lean_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False
        )
        self.assertEqual(result.returncode, 0, f"lake env lean Reader.lean failed:\n{result.stdout}\n{result.stderr}")
        allowed = {"propext", "Quot.sound"}
        found_reports = 0
        for line in (result.stdout + result.stderr).splitlines():
            m_used = re.search(r"'(.+?)' depends on axioms: \[(.*?)\]", line)
            m_none = re.search(r"'(.+?)' does not depend on any axioms", line)
            if m_used:
                name = m_used.group(1)
                axioms = [a.strip() for a in m_used.group(2).split(",") if a.strip()]
                self.assertTrue(set(axioms) <= allowed, f"Disallowed axiom in {name}: {axioms}")
                found_reports += 1
            elif m_none:
                found_reports += 1
        self.assertGreaterEqual(found_reports, 15, "Expected at least 15 axiom reports from Reader.lean")


if __name__ == "__main__":
    unittest.main()
