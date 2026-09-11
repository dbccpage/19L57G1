"""Evaluation writes no Event onto the declared base and persists no events."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

from derivation.candidates import Bounds  # noqa: E402
from derivation.engine import READING_F, READING_L  # noqa: E402
from derivation.model import AdmitDatum, Impose, replay  # noqa: E402

from evaluate import (  # noqa: E402
    declared_base_mutated,
    evaluate,
    persist_eval_events_on_base,
)
from harness import EvalResult, EvaluationPersistedEventError  # noqa: E402


class EvaluationEvents(unittest.TestCase):
    def test_declared_base_is_unchanged(self) -> None:
        hist = READING_L.genesis
        base = replay(hist)
        before = base
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        self.assertEqual(base, before)
        self.assertEqual(replay(hist), base)
        self.assertEqual(base.reqs, before.reqs)
        self.assertTrue(result.found)
        self.assertEqual(len(result.retained), 3)

    def test_persisting_eval_events_on_the_declared_base_is_refused(self) -> None:
        hist = READING_L.genesis
        base = replay(hist)
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        with self.assertRaises(EvaluationPersistedEventError):
            persist_eval_events_on_base(
                base, result, (Impose(READING_L.target[0], READING_L.target[1]),)
            )
        self.assertEqual(replay(hist), base)
        self.assertEqual(base.reqs, frozenset())

    def test_declared_base_mutated_is_a_comparison(self) -> None:
        hist = READING_L.genesis
        before = replay(hist)
        other = replay(hist + (AdmitDatum("x"),))
        self.assertFalse(declared_base_mutated(before, before, hist))
        self.assertTrue(declared_base_mutated(before, other, hist))

    def test_eval_result_does_not_persist_delta_events(self) -> None:
        base = replay(READING_F.genesis)
        result = evaluate(base, READING_F.target, "mu1", Bounds(2, 2))
        self.assertFalse(hasattr(result, "delta_events"))
        self.assertFalse(hasattr(result, "events"))
        self.assertIsInstance(result, EvalResult)
        self.assertEqual(len(result.retained), 5)
        self.assertNotIn("Tie", type(result).__name__)
        self.assertNotIn("Unique", type(result).__name__)

    def test_no_valid_response_is_an_eval_result_not_none(self) -> None:
        base = replay(READING_L.genesis)
        result = evaluate(
            base, READING_L.target, "mu1", Bounds(max_items=0, max_arity=1)
        )
        self.assertIsInstance(result, EvalResult)
        self.assertIsNotNone(result)
        self.assertFalse(result.found)
        self.assertEqual(result.retained, ())
        self.assertEqual(replay(READING_L.genesis), base)

    def test_unknown_measure_is_refused(self) -> None:
        base = replay(READING_L.genesis)
        with self.assertRaises(ValueError):
            evaluate(base, READING_L.target, "mu3", Bounds(2, 2))

    def test_evaluate_source_does_not_import_partial_decide(self) -> None:
        text = (
            Path(__file__).resolve().parents[1] / "evaluate.py"
        ).read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                self.assertNotIn("partial_decide", stripped)
                self.assertNotIn("delta_events", stripped)


if __name__ == "__main__":
    unittest.main()
