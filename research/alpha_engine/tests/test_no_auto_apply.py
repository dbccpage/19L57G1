"""A unique minimum remains a proposal; uniqueness is not a license."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

from derivation.candidates import Bounds, NewForm, NewInst  # noqa: E402
from derivation.engine import READING_L  # noqa: E402
from derivation.model import replay  # noqa: E402

from driver_a import explore, refuse_auto_apply  # noqa: E402
from evaluate import evaluate  # noqa: E402
from harness import (  # noqa: E402
    EvalResult,
    Node,
    RetainedClass,
    UniqueDeltaAutoApplyError,
    apply_unique_delta,
    make_license,
)
from search_policy import record_census  # noqa: E402


class NoAutoApply(unittest.TestCase):
    def test_apply_unique_delta_is_refused(self) -> None:
        base = replay(READING_L.genesis)
        node = Node(history=READING_L.genesis, regime=base, license=None)
        delta = (NewForm(1), NewInst(0, (0,)))
        key = (2, (1,), ((0, (0,)),), (), ((0, 1),))
        result = EvalResult(
            measure="mu1",
            cost=(2, -1),
            raw_minima=(delta,),
            retained=(RetainedClass(key, (delta,)),),
            found=True,
            max_items=2,
            max_arity=2,
        )
        with self.assertRaises(UniqueDeltaAutoApplyError):
            apply_unique_delta(node, result)
        with self.assertRaises(UniqueDeltaAutoApplyError):
            refuse_auto_apply(node, result)
        self.assertIsNone(node.license)
        self.assertEqual(node.regime, base)

    def test_unique_mu2_class_is_not_applied_without_a_license(self) -> None:
        base = replay(READING_L.genesis)
        node = Node(history=READING_L.genesis, regime=base, license=None)
        result = evaluate(base, READING_L.target, "mu2", Bounds(2, 2))
        self.assertTrue(result.found)
        self.assertEqual(len(result.retained), 1)
        keys = tuple(item.key for item in result.retained)
        census = record_census(keys, (), (), keys)
        denied = make_license(granter="test", scope="mu2", authorized=())
        explored = explore(node, result, denied, census, READING_L.target)
        self.assertEqual(explored.children, ())
        self.assertEqual(node.regime, base)
        self.assertEqual(node.history, READING_L.genesis)
        self.assertIsNone(node.license)

    def test_licensed_sole_class_is_still_an_apply(self) -> None:
        base = replay(READING_L.genesis)
        node = Node(history=READING_L.genesis, regime=base, license=None)
        result = evaluate(base, READING_L.target, "mu2", Bounds(2, 2))
        self.assertTrue(result.found)
        self.assertEqual(len(result.retained), 1)
        key = result.retained[0].key
        keys = (key,)
        census = record_census(keys, keys, (), ())
        license = make_license(granter="test", scope="mu2", authorized=keys)
        explored = explore(node, result, license, census, READING_L.target)
        self.assertEqual(len(explored.children), 1)
        self.assertEqual(node.regime, base)
        self.assertIsNone(node.license)
        child = explored.children[0]
        self.assertEqual(child.license, license)
        self.assertGreater(len(child.history), len(node.history))


if __name__ == "__main__":
    unittest.main()
