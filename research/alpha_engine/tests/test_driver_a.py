"""Driver A expands licensed keys onto a new Node; leftovers are observations."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

from derivation.candidates import Bounds  # noqa: E402
from derivation.engine import READING_L  # noqa: E402
from derivation.model import Impose, replay  # noqa: E402
from derivation.observe import collapsed_pairs  # noqa: E402

from driver_a import apply_licensed, explore, three_phase_record  # noqa: E402
from evaluate import evaluate  # noqa: E402
from harness import Node, leftover_as_demand, LeftoverIsNotDemandError, make_license  # noqa: E402
from search_policy import declared_explore_first, record_census  # noqa: E402


class DriverA(unittest.TestCase):
    def test_licensed_apply_writes_a_new_node(self) -> None:
        base = replay(READING_L.genesis)
        node = Node(history=READING_L.genesis, regime=base, license=None)
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        keys = tuple(item.key for item in result.retained)
        policy = declared_explore_first(keys)
        license = make_license(
            granter=policy.policy_id,
            scope="C3-L-mu1",
            authorized=policy.subset(),
        )
        child = apply_licensed(
            node, result, license, policy.subset()[0], READING_L.target
        )
        self.assertIsNotNone(child)
        assert child is not None
        self.assertIsNone(node.license)
        self.assertEqual(node.regime, base)
        self.assertEqual(child.license, license)
        self.assertGreater(len(child.history), len(node.history))
        self.assertIsInstance(child.history[len(node.history)], Impose)
        self.assertEqual(replay(child.history), child.regime)
        leftovers = collapsed_pairs(child.regime)
        with self.assertRaises(LeftoverIsNotDemandError):
            leftover_as_demand(leftovers)

    def test_explore_does_not_mutate_the_declared_base(self) -> None:
        base = replay(READING_L.genesis)
        node = Node(history=READING_L.genesis, regime=base, license=None)
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        keys = tuple(item.key for item in result.retained)
        census = record_census(keys, (keys[0],), (), keys[1:])
        license = make_license(
            granter="test",
            scope="C3-L-mu1",
            authorized=(keys[0],),
        )
        out = explore(node, result, license, census, READING_L.target)
        self.assertEqual(len(out.children), 1)
        self.assertTrue(out.leftover_are_observations)
        self.assertEqual(node.regime, base)
        self.assertEqual(node.history, READING_L.genesis)
        self.assertIsNone(node.license)

    def test_three_phase_record_counts(self) -> None:
        record = three_phase_record()
        self.assertEqual(record["authority_effect"], "None")
        self.assertEqual(record["driver_b"], "OPEN")
        self.assertIs(record["auto_apply_unique_delta"], False)
        self.assertEqual(record["field_layout_is_not_temporal_proof"], True)
        folds = record["folds"]
        assert isinstance(folds, list)
        self.assertEqual(len(folds), 2)
        l_fold, f_fold = folds
        assert isinstance(l_fold, dict)
        assert isinstance(f_fold, dict)
        l_eval = l_fold["evaluation"]
        f_eval = f_fold["evaluation"]
        assert isinstance(l_eval, dict)
        assert isinstance(f_eval, dict)
        self.assertEqual(l_eval["retained_class_count"], 3)
        self.assertEqual(f_eval["retained_class_count"], 5)
        self.assertIs(l_eval["mutated_declared_base"], False)
        self.assertIs(f_eval["mutated_declared_base"], False)
        self.assertEqual(l_eval["grades_as_license"], False)
        self.assertEqual(
            l_fold["compute_order"],
            [
                "evaluate",
                "wrap_raw_minima_as_proposal",
                "present",
                "license",
                "explore",
            ],
        )
        self.assertIs(l_fold["auto_apply_unique_delta"], False)
        l_auth = l_fold["authorization"]
        assert isinstance(l_auth, dict)
        self.assertIs(l_auth["sole_class_license_is_apply"], False)
        l_census = l_fold["census"]
        assert isinstance(l_census, dict)
        self.assertEqual(l_census["tie_set_size"], 3)
        self.assertTrue(l_census["sum_equals_tie_set"])
        proposal = l_fold["proposal"]
        assert isinstance(proposal, dict)
        self.assertEqual(proposal["changes_admitted_state"], False)

    def test_driver_source_has_no_visit_count_or_ucb(self) -> None:
        text = (
            Path(__file__).resolve().parents[1] / "driver_a.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("UCB", text)
        self.assertNotIn("visit_count", text)
        self.assertNotIn("rollout", text)


if __name__ == "__main__":
    unittest.main()
