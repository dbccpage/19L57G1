"""Tests for declared search policy extensions: bounded priority, constraint pruning, and cost budgeting."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

from derivation.candidates import Bounds  # noqa: E402
from derivation.engine import READING_L  # noqa: E402
from derivation.iso import CanonKey  # noqa: E402
from derivation.model import Impose, replay  # noqa: E402

from driver_a import UnlicensedExploreError, explore  # noqa: E402
from evaluate import evaluate  # noqa: E402
from harness import Node, make_license  # noqa: E402
from search_policy import (  # noqa: E402
    CensusError,
    FabricatedClassError,
    _PriorityScoreKey,
    declared_bounded_priority,
    declared_constraint_pruned,
    declared_cost_budgeted,
)


class TestBoundedPriorityPolicy(unittest.TestCase):
    def setUp(self) -> None:
        self.base = replay(READING_L.genesis)
        self.result = evaluate(self.base, READING_L.target, "mu1", Bounds(2, 2))
        self.retained = tuple(item.key for item in self.result.retained)
        self.assertEqual(len(self.retained), 3)

    def test_bounded_priority_with_priority_fn(self) -> None:
        # Assign descending priority scores to keys
        scores = {self.retained[0]: 10, self.retained[1]: 30, self.retained[2]: 20}
        policy = declared_bounded_priority(
            self.retained,
            bound=2,
            priority_fn=lambda k: scores[k],
        )
        self.assertEqual(len(policy.subset()), 2)
        # Key with score 30 and key with score 20 must be in explored
        self.assertIn(self.retained[1], policy.subset())
        self.assertIn(self.retained[2], policy.subset())
        self.assertNotIn(self.retained[0], policy.subset())
        census = policy.census()
        self.assertEqual(len(census.explored), 2)
        self.assertEqual(len(census.pruned), 0)
        self.assertEqual(len(census.open_keys), 1)
        self.assertEqual(census.open_keys, (self.retained[0],))
        self.assertEqual(
            len(census.explored) + len(census.pruned) + len(census.open_keys),
            census.tie_set_size,
        )

    def test_bounded_priority_with_score_fn_alias(self) -> None:
        scores = {self.retained[0]: 5, self.retained[1]: 15, self.retained[2]: 25}
        policy = declared_bounded_priority(
            self.retained,
            bound=1,
            score_fn=lambda k: scores[k],
        )
        self.assertEqual(policy.subset(), (self.retained[2],))
        census = policy.census()
        self.assertEqual(len(census.open_keys), 2)

    def test_bounded_priority_default_canonical_order(self) -> None:
        ordered = tuple(sorted(self.retained))
        policy = declared_bounded_priority(self.retained, bound=1)
        self.assertEqual(policy.subset(), (ordered[0],))
        self.assertEqual(policy.census().open_keys, ordered[1:])

    def test_bounded_priority_tie_breaking(self) -> None:
        ordered = tuple(sorted(self.retained))
        # Equal score for first two keys
        scores = {ordered[0]: 100, ordered[1]: 100, ordered[2]: 50}
        policy = declared_bounded_priority(
            self.retained,
            bound=1,
            priority_fn=lambda k: scores[k],
        )
        # Tie between ordered[0] and ordered[1] must be broken by canonical key ascending
        self.assertEqual(policy.subset(), (ordered[0],))

    def test_bounded_priority_comparator_not_implemented(self) -> None:
        key_obj = _PriorityScoreKey(10, self.retained[0])
        self.assertIs(key_obj.__lt__("not_a_key"), NotImplemented)

    def test_bounded_priority_zero_bound(self) -> None:
        policy = declared_bounded_priority(self.retained, bound=0)
        self.assertEqual(policy.subset(), ())
        census = policy.census()
        self.assertEqual(len(census.explored), 0)
        self.assertEqual(len(census.open_keys), 3)

    def test_bounded_priority_excess_bound(self) -> None:
        policy = declared_bounded_priority(self.retained, bound=10)
        self.assertEqual(len(policy.subset()), 3)
        self.assertEqual(len(policy.census().open_keys), 0)

    def test_bounded_priority_negative_bound(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            declared_bounded_priority(self.retained, bound=-1)
        self.assertIn("cannot be negative", str(ctx.exception))

    def test_bounded_priority_custom_justification(self) -> None:
        policy = declared_bounded_priority(
            self.retained, bound=1, justification="custom priority rationale"
        )
        self.assertEqual(policy.justification, "custom priority rationale")

    def test_bounded_priority_empty_retained(self) -> None:
        policy = declared_bounded_priority((), bound=2)
        self.assertEqual(policy.subset(), ())
        census = policy.census()
        self.assertEqual(census.tie_set_size, 0)
        self.assertEqual(census.explored, ())
        self.assertEqual(census.open_keys, ())
        self.assertEqual(census.pruned, ())

    def test_bounded_priority_duplicate_retained_raises_census_error(self) -> None:
        duplicate_keys = (self.retained[0], self.retained[0], self.retained[1])
        with self.assertRaises(CensusError) as ctx:
            declared_bounded_priority(duplicate_keys, bound=1)
        self.assertIn("retained keys must be distinct", str(ctx.exception))


class TestConstraintPrunedPolicy(unittest.TestCase):
    def setUp(self) -> None:
        self.base = replay(READING_L.genesis)
        self.result = evaluate(self.base, READING_L.target, "mu1", Bounds(2, 2))
        self.retained = tuple(item.key for item in self.result.retained)
        self.ordered = tuple(sorted(self.retained))

    def test_constraint_pruned_predicate_true(self) -> None:
        target_prune = self.ordered[0]
        policy = declared_constraint_pruned(
            self.retained,
            predicate=lambda k: k == target_prune,
            prune_if=True,
        )
        census = policy.census()
        self.assertEqual(census.pruned, (target_prune,))
        self.assertEqual(census.explored, (self.ordered[1], self.ordered[2]))
        self.assertEqual(census.open_keys, ())
        self.assertEqual(
            len(census.explored) + len(census.pruned) + len(census.open_keys),
            3,
        )

    def test_constraint_pruned_predicate_false_pruning(self) -> None:
        # Keep only ordered[2], prune those that evaluate to False
        target_viable = self.ordered[2]
        policy = declared_constraint_pruned(
            self.retained,
            predicate=lambda k: k == target_viable,
            prune_if=False,
        )
        census = policy.census()
        self.assertEqual(census.explored, (target_viable,))
        self.assertEqual(census.pruned, (self.ordered[0], self.ordered[1]))
        self.assertEqual(census.open_keys, ())

    def test_constraint_pruned_with_bound(self) -> None:
        # Prune ordered[0], 2 viable keys, explore only 1
        policy = declared_constraint_pruned(
            self.retained,
            predicate=lambda k: k == self.ordered[0],
            bound=1,
        )
        census = policy.census()
        self.assertEqual(census.pruned, (self.ordered[0],))
        self.assertEqual(census.explored, (self.ordered[1],))
        self.assertEqual(census.open_keys, (self.ordered[2],))
        self.assertEqual(len(census.explored) + len(census.pruned) + len(census.open_keys), 3)

    def test_constraint_pruned_no_predicate_no_pruned_keys(self) -> None:
        policy = declared_constraint_pruned(self.retained, bound=2)
        census = policy.census()
        self.assertEqual(census.pruned, ())
        self.assertEqual(len(census.explored), 2)
        self.assertEqual(len(census.open_keys), 1)

    def test_constraint_pruned_explicit_pruned_keys(self) -> None:
        policy = declared_constraint_pruned(
            self.retained,
            pruned_keys=(self.ordered[1],),
        )
        census = policy.census()
        self.assertEqual(census.pruned, (self.ordered[1],))
        self.assertEqual(census.explored, (self.ordered[0], self.ordered[2]))
        self.assertEqual(census.open_keys, ())

    def test_constraint_pruned_foreign_key_raises_fabricated_class(self) -> None:
        fake_key: CanonKey = (999, (), (), (), ())
        with self.assertRaises(FabricatedClassError):
            declared_constraint_pruned(
                self.retained,
                pruned_keys=(fake_key,),
            )

    def test_constraint_pruned_duplicate_pruned_keys_raises_census_error(self) -> None:
        with self.assertRaises(CensusError) as ctx:
            declared_constraint_pruned(
                self.retained,
                pruned_keys=(self.ordered[0], self.ordered[0]),
            )
        self.assertIn("duplicate a key", str(ctx.exception))

    def test_constraint_pruned_negative_bound(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            declared_constraint_pruned(self.retained, bound=-1)
        self.assertIn("cannot be negative", str(ctx.exception))

    def test_constraint_pruned_all_pruned(self) -> None:
        policy = declared_constraint_pruned(
            self.retained,
            predicate=lambda k: True,
        )
        census = policy.census()
        self.assertEqual(census.explored, ())
        self.assertEqual(census.open_keys, ())
        self.assertEqual(len(census.pruned), 3)

    def test_constraint_pruned_custom_justification(self) -> None:
        policy = declared_constraint_pruned(
            self.retained, justification="custom constraint rationale"
        )
        self.assertEqual(policy.justification, "custom constraint rationale")

    def test_constraint_pruned_empty_retained(self) -> None:
        policy = declared_constraint_pruned(())
        census = policy.census()
        self.assertEqual(census.tie_set_size, 0)
        self.assertEqual(census.explored, ())
        self.assertEqual(census.pruned, ())
        self.assertEqual(census.open_keys, ())


class TestCostBudgetedPolicy(unittest.TestCase):
    def setUp(self) -> None:
        self.base = replay(READING_L.genesis)
        self.result = evaluate(self.base, READING_L.target, "mu1", Bounds(2, 2))
        self.retained = tuple(item.key for item in self.result.retained)
        self.ordered = tuple(sorted(self.retained))

    def test_cost_budgeted_exact_rational_fractions(self) -> None:
        # Assign fractional costs: 1/4, 1/3, 1/2
        costs = {
            self.ordered[0]: Fraction(1, 4),
            self.ordered[1]: Fraction(1, 3),
            self.ordered[2]: Fraction(1, 2),
        }
        # Budget 1/4 + 1/3 = 7/12 exactly funds the first two
        budget = Fraction(7, 12)
        policy = declared_cost_budgeted(self.retained, costs, budget)
        census = policy.census()
        self.assertEqual(census.explored, (self.ordered[0], self.ordered[1]))
        self.assertEqual(census.open_keys, (self.ordered[2],))
        self.assertEqual(census.pruned, ())
        self.assertEqual(len(census.explored) + len(census.pruned) + len(census.open_keys), 3)

    def test_cost_budgeted_with_callable_cost_fn(self) -> None:
        costs = {
            self.ordered[0]: Fraction(2, 5),
            self.ordered[1]: Fraction(1, 5),
            self.ordered[2]: Fraction(4, 5),
        }
        # Ordered by cost: ordered[1] (1/5), ordered[0] (2/5), ordered[2] (4/5)
        # Budget 3/5 funds ordered[1] and ordered[0] (1/5 + 2/5 = 3/5)
        policy = declared_cost_budgeted(
            self.retained,
            cost_fn=lambda k: costs[k],
            budget=Fraction(3, 5),
        )
        census = policy.census()
        self.assertEqual(census.explored, (self.ordered[0], self.ordered[1]))
        self.assertEqual(census.open_keys, (self.ordered[2],))

    def test_cost_budgeted_with_strings_and_ints(self) -> None:
        costs: dict[CanonKey, int | str] = {
            self.ordered[0]: "1/2",
            self.ordered[1]: 1,
            self.ordered[2]: "3/2",
        }
        policy = declared_cost_budgeted(self.retained, costs, budget="2")
        # 1/2 + 1 = 1.5 <= 2; 1.5 + 1.5 = 3 > 2
        census = policy.census()
        self.assertEqual(census.explored, (self.ordered[0], self.ordered[1]))
        self.assertEqual(census.open_keys, (self.ordered[2],))

    def test_cost_budgeted_zero_budget_refusal(self) -> None:
        costs = {k: Fraction(1, 1) for k in self.ordered}
        policy = declared_cost_budgeted(self.retained, costs, budget=0)
        self.assertEqual(policy.subset(), ())
        census = policy.census()
        self.assertEqual(len(census.explored), 0)
        self.assertEqual(len(census.open_keys), 3)

    def test_cost_budgeted_zero_cost_funded_under_zero_budget(self) -> None:
        costs = {
            self.ordered[0]: Fraction(0),
            self.ordered[1]: Fraction(1),
            self.ordered[2]: Fraction(1),
        }
        policy = declared_cost_budgeted(self.retained, costs, budget=0)
        self.assertEqual(policy.subset(), (self.ordered[0],))
        census = policy.census()
        self.assertEqual(len(census.explored), 1)
        self.assertEqual(len(census.open_keys), 2)

    def test_cost_budgeted_tie_breaking(self) -> None:
        # All keys have identical cost 1
        costs = {k: 1 for k in self.ordered}
        # Budget 2 funds exactly the first 2 in canonical order
        policy = declared_cost_budgeted(self.retained, costs, budget=2)
        self.assertEqual(policy.subset(), (self.ordered[0], self.ordered[1]))
        self.assertEqual(policy.census().open_keys, (self.ordered[2],))

    def test_cost_budgeted_refuses_float(self) -> None:
        costs = {k: Fraction(1, 2) for k in self.ordered}
        with self.assertRaises(TypeError) as ctx:
            declared_cost_budgeted(self.retained, costs, budget=0.5)  # type: ignore[arg-type]
        self.assertIn("float is not exact", str(ctx.exception))
        with self.assertRaises(TypeError) as ctx2:
            declared_cost_budgeted(
                self.retained,
                {self.ordered[0]: 0.25, self.ordered[1]: 1, self.ordered[2]: 1},  # type: ignore[dict-item]
                budget=1,
            )
        self.assertIn("float is not exact", str(ctx2.exception))

    def test_cost_budgeted_negative_budget_raises(self) -> None:
        costs = {k: 1 for k in self.ordered}
        with self.assertRaises(ValueError) as ctx:
            declared_cost_budgeted(self.retained, costs, budget=-1)
        self.assertIn("cannot be negative", str(ctx.exception))

    def test_cost_budgeted_negative_cost_raises(self) -> None:
        costs = {self.ordered[0]: -1, self.ordered[1]: 1, self.ordered[2]: 1}
        with self.assertRaises(ValueError) as ctx:
            declared_cost_budgeted(self.retained, costs, budget=1)
        self.assertIn("cannot be negative", str(ctx.exception))

    def test_cost_budgeted_custom_justification(self) -> None:
        costs = {k: 1 for k in self.ordered}
        policy = declared_cost_budgeted(
            self.retained, costs, budget=1, justification="custom budget rationale"
        )
        self.assertEqual(policy.justification, "custom budget rationale")

    def test_cost_budgeted_empty_retained(self) -> None:
        policy = declared_cost_budgeted((), {}, budget=5)
        census = policy.census()
        self.assertEqual(census.tie_set_size, 0)
        self.assertEqual(census.explored, ())
        self.assertEqual(census.open_keys, ())
        self.assertEqual(census.pruned, ())


class TestDriverAMultiKeyIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.base = replay(READING_L.genesis)
        self.node = Node(history=READING_L.genesis, regime=self.base, license=None)
        self.result = evaluate(self.base, READING_L.target, "mu1", Bounds(2, 2))
        self.retained = tuple(item.key for item in self.result.retained)
        self.assertEqual(len(self.retained), 3)

    def test_driver_a_multi_key_bounded_priority(self) -> None:
        policy = declared_bounded_priority(self.retained, bound=2)
        license = make_license(
            granter=policy.policy_id,
            scope="C3-L-mu1-multi",
            authorized=policy.subset(),
            source=self.node,
            target=READING_L.target,
            measure="mu1",
            bounds=Bounds(2, 2),
        )
        out = explore(self.node, self.result, license, policy.census(), READING_L.target)
        self.assertEqual(len(out.children), 2)
        self.assertTrue(out.leftover_are_observations)
        self.assertEqual(len(out.leftover_pairs), 2)
        # Base node must be unmutated
        self.assertEqual(self.node.regime, self.base)
        self.assertIsNone(self.node.license)
        # Child nodes must have license and extended history
        for child in out.children:
            self.assertEqual(child.license, license)
            self.assertGreater(len(child.history), len(self.node.history))
            self.assertEqual(replay(child.history), child.regime)
            self.assertIsInstance(child.history[len(self.node.history)], Impose)

    def test_driver_a_multi_key_constraint_pruned(self) -> None:
        ordered = tuple(sorted(self.retained))
        policy = declared_constraint_pruned(
            self.retained,
            predicate=lambda k: k == ordered[0],
            bound=2,
        )
        license = make_license(
            granter=policy.policy_id,
            scope="C3-L-mu1-pruned",
            authorized=policy.subset(),
            source=self.node,
            target=READING_L.target,
            measure="mu1",
            bounds=Bounds(2, 2),
        )
        out = explore(self.node, self.result, license, policy.census(), READING_L.target)
        self.assertEqual(len(out.children), 2)
        self.assertEqual(out.census.pruned, (ordered[0],))
        self.assertEqual(len(out.census.explored), 2)

    def test_driver_a_multi_key_cost_budgeted(self) -> None:
        costs = {k: 1 for k in self.retained}
        policy = declared_cost_budgeted(self.retained, costs, budget=2)
        license = make_license(
            granter=policy.policy_id,
            scope="C3-L-mu1-cost",
            authorized=policy.subset(),
            source=self.node,
            target=READING_L.target,
            measure="mu1",
            bounds=Bounds(2, 2),
        )
        out = explore(self.node, self.result, license, policy.census(), READING_L.target)
        self.assertEqual(len(out.children), 2)

    def test_driver_a_all_keys_explored(self) -> None:
        policy = declared_bounded_priority(self.retained, bound=3)
        license = make_license(
            granter=policy.policy_id,
            scope="C3-L-mu1-all",
            authorized=policy.subset(),
            source=self.node,
            target=READING_L.target,
            measure="mu1",
            bounds=Bounds(2, 2),
        )
        out = explore(self.node, self.result, license, policy.census(), READING_L.target)
        self.assertEqual(len(out.children), 3)

    def test_driver_a_zero_explored_keys_typed_refusal(self) -> None:
        policy = declared_bounded_priority(self.retained, bound=0)
        license = make_license(
            granter=policy.policy_id,
            scope="C3-L-mu1-zero",
            authorized=policy.subset(),
            source=self.node,
            target=READING_L.target,
            measure="mu1",
            bounds=Bounds(2, 2),
        )
        out = explore(self.node, self.result, license, policy.census(), READING_L.target)
        self.assertEqual(len(out.children), 0)
        self.assertEqual(self.node.regime, self.base)
        self.assertIsNone(self.node.license)

    def test_driver_a_unlicensed_key_in_multi_explore_rejected(self) -> None:
        policy = declared_bounded_priority(self.retained, bound=2)
        # License authorizes only the first explored key
        license = make_license(
            granter=policy.policy_id,
            scope="C3-L-mu1-partial-auth",
            authorized=policy.subset()[:1],
            source=self.node,
            target=READING_L.target,
            measure="mu1",
            bounds=Bounds(2, 2),
        )
        with self.assertRaises(UnlicensedExploreError) as ctx:
            explore(self.node, self.result, license, policy.census(), READING_L.target)
        self.assertIn("only licensed keys", str(ctx.exception))

    def test_driver_a_fabricated_class_in_license_rejected(self) -> None:
        policy = declared_bounded_priority(self.retained, bound=1)
        fake_key: CanonKey = (999, (), (), (), ())
        license = make_license(
            granter=policy.policy_id,
            scope="C3-L-mu1-forged",
            authorized=(fake_key,),
            source=self.node,
            target=READING_L.target,
            measure="mu1",
            bounds=Bounds(2, 2),
        )
        with self.assertRaises(FabricatedClassError):
            explore(self.node, self.result, license, policy.census(), READING_L.target)


class TestCensusInvarianceProperty(unittest.TestCase):
    def test_census_partition_invariance_across_policies(self) -> None:
        base = replay(READING_L.genesis)
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        retained = tuple(item.key for item in result.retained)
        retained_set = frozenset(retained)

        policies = [
            declared_bounded_priority(retained, bound=0),
            declared_bounded_priority(retained, bound=1),
            declared_bounded_priority(retained, bound=2),
            declared_bounded_priority(retained, bound=3),
            declared_bounded_priority(retained, bound=5),
            declared_constraint_pruned(retained, predicate=lambda k: False),
            declared_constraint_pruned(retained, predicate=lambda k: True),
            declared_constraint_pruned(retained, predicate=lambda k: k == retained[0], bound=1),
            declared_cost_budgeted(retained, {k: Fraction(1, 2) for k in retained}, budget=Fraction(1, 2)),
            declared_cost_budgeted(retained, {k: Fraction(1, 2) for k in retained}, budget=Fraction(1)),
            declared_cost_budgeted(retained, {k: Fraction(1, 2) for k in retained}, budget=Fraction(2)),
        ]

        for p in policies:
            c = p.census()
            # Invariant 1: sum of bucket lengths equals tie_set_size
            self.assertEqual(
                len(c.explored) + len(c.pruned) + len(c.open_keys),
                c.tie_set_size,
            )
            # Invariant 2: tie_set_size equals len(retained)
            self.assertEqual(c.tie_set_size, len(retained))
            # Invariant 3: union of buckets equals retained set
            self.assertEqual(
                set(c.explored) | set(c.pruned) | set(c.open_keys),
                retained_set,
            )
            # Invariant 4: pairwise disjoint
            self.assertEqual(set(c.explored) & set(c.pruned), set())
            self.assertEqual(set(c.explored) & set(c.open_keys), set())
            self.assertEqual(set(c.pruned) & set(c.open_keys), set())
            # Invariant 5: subset() matches explored
            self.assertEqual(p.subset(), c.explored)


if __name__ == "__main__":
    unittest.main()
