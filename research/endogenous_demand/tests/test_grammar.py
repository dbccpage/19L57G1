"""Python mirror of the reqs channel, both readings."""

from __future__ import annotations

from pathlib import Path
import sys
from unittest import mock
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

import grammar as gr  # noqa: E402
from derivation.model import AdmitDatum, EMPTY, Impose, Supply, replay  # noqa: E402


class ConstructorCases(unittest.TestCase):
    def test_only_impose_writes_reqs(self) -> None:
        cases = gr.constructor_cases()
        writers = sorted(name for name, row in cases.items() if bool(row["changed"]))
        self.assertEqual(writers, ["Impose"])
        for name, row in cases.items():
            self.assertEqual(bool(row["changed"]), bool(row["is_impose"]), name)

    def test_empty_reqs_at_genesis(self) -> None:
        self.assertEqual(EMPTY.reqs, frozenset())
        self.assertTrue(gr.prefix_without_impose()["empty_reqs"])


class Readings(unittest.TestCase):
    def test_both_readings_write_reqs_by_impose(self) -> None:
        replays = gr.reading_replays()
        self.assertEqual(set(replays), {"L", "F"})
        self.assertEqual(replays["L"]["impose_events"], [[0, 1]])
        self.assertEqual(replays["F"]["impose_events"], [[1, 2]])
        for name, row in replays.items():
            self.assertEqual(row["impose_events"], row["reqs"], name)
            self.assertTrue(row["last_is_impose"], name)
            self.assertIsNone(row["e2_violation"], name)


class E2Guard(unittest.TestCase):
    def test_empty_history_does_not_extend(self) -> None:
        self.assertFalse(gr.last_event_extends_reqs(()))
        self.assertIsNone(gr.e2_violation(()))

    def test_impose_extends_and_is_not_an_e2_violation(self) -> None:
        history = (Supply("a"), AdmitDatum("a"), Supply("b"), AdmitDatum("b"), Impose(0, 1))
        self.assertTrue(gr.last_event_extends_reqs(history))
        self.assertTrue(gr.is_impose(history[-1]))
        self.assertIsNone(gr.e2_violation(history))

    def test_admit_does_not_extend(self) -> None:
        history = (Supply("a"), AdmitDatum("a"))
        self.assertFalse(gr.last_event_extends_reqs(history))
        self.assertIsNone(gr.e2_violation(history))

    def test_injected_non_impose_growth_is_named(self) -> None:
        history = (Supply("a"),)
        with mock.patch("grammar.last_event_extends_reqs", return_value=True):
            named = gr.e2_violation(history)
        self.assertIsNotNone(named)
        assert named is not None
        self.assertIn("Supply", named)
        self.assertIn("E2:", named)

    def test_record_shape(self) -> None:
        record = gr.grammar_record()
        self.assertEqual(record["outcome"], "B")
        self.assertEqual(record["class"], "C_reqs")
        self.assertEqual(record["reqs_writers"], ["Impose"])
        self.assertEqual(record["readings"], ["L", "F"])
        self.assertEqual(gr.reqs_of(()), frozenset())


class ReplayIdentity(unittest.TestCase):
    def test_imposes_in_skips_non_impose(self) -> None:
        history = (Supply("a"), AdmitDatum("a"), Impose(0, 0))
        # Impose(0,0) is ill-formed for step, but imposes_in still records it.
        self.assertEqual(gr.imposes_in(history), ((0, 0),))
        self.assertEqual(replay(history[:-1]).reqs, frozenset())


if __name__ == "__main__":
    unittest.main()
