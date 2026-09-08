"""The extension on the sealed carrier: positive controls, the exhibits, and
one named negative case per claim it tests."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

import ignition as ig  # noqa: E402
from derivation.candidates import NewInst, delta_events, response_valid_naive  # noqa: E402
from derivation.model import AdmitDatum, Impose, Regime, Supply, certify, replay  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
ROOT_L = replay(ig.READINGS["L"].genesis)
ROOT_F = replay(ig.READINGS["F"].genesis)


def opening_children(reading_name: str, measure: str) -> list[Regime]:
    reading = ig.READINGS[reading_name]
    root = replay(reading.genesis)
    return [s.child for s in ig.fire(root, measure, ig.BOUNDS, [reading.target])]


class RootFamilies(unittest.TestCase):
    """The starting-state corrections, confirmed by execution."""

    def test_sealed_challenge_three_families(self) -> None:
        expect = {("L", "mu1"): (3, 6), ("F", "mu1"): (5, 10), ("L", "mu2"): (1, 2), ("F", "mu2"): (1, 2)}
        for (name, measure), (classes, raw) in expect.items():
            reading = ig.READINGS[name]
            steps = ig.fire(replay(reading.genesis), measure, ig.BOUNDS, [reading.target])
            self.assertEqual((len(steps), steps[0].raw_minima), (classes, raw), (name, measure))

    def test_singleton_family_is_accepted(self) -> None:
        """Positive control: one class under mu2 is a family of one, kept."""
        steps = ig.fire(ROOT_L, "mu2", ig.BOUNDS, [(0, 1)])
        self.assertEqual(len(steps), 1)
        self.assertTrue(ig.retains_all_classes(steps, ROOT_L, (0, 1), "mu2"))
        self.assertEqual(steps[0].cost, (2, 1))

    def test_every_offered_response_is_valid_and_rule_free(self) -> None:
        for name in ("L", "F"):
            for measure in ("mu1", "mu2"):
                reading = ig.READINGS[name]
                root = replay(reading.genesis)
                for s in ig.fire(root, measure, ig.BOUNDS, [reading.target]):
                    self.assertTrue(response_valid_naive(root, reading.target, s.delta))
                    self.assertTrue(ig.rule_free(s.child))
                    self.assertTrue(ig.good(s.child))
                    self.assertTrue(certify(reading.genesis + s.events, s.child))


class GrowthAndDemand(unittest.TestCase):
    """The Lean characterization of growth, executed."""

    def test_growth_creates_exactly_the_unmentioned_pairs(self) -> None:
        for name in ("L", "F"):
            for measure in ("mu1", "mu2"):
                for child in opening_children(name, measure):
                    record = ig.growth_demand_record(child)
                    self.assertTrue(record["characterization_holds"], (name, measure))
                    self.assertTrue(record["old_verdicts_unchanged"])
                    count = int(str(record["new_demand_count"]))
                    self.assertEqual(count, len(ig.unmentioned_data(child)))
                    if not ig.demands(child):
                        # the at-most-one theorem applies at a fixpoint only
                        self.assertLessEqual(count, 1)
                    else:
                        # reading F's opening states keep two unmentioned data,
                        # so growth there creates two demands: not a fixpoint
                        self.assertGreaterEqual(count, 1)

    def test_the_three_tied_classes_answer_growth_differently(self) -> None:
        """Input-directed behaviour: the unary mark leaves one datum
        unmentioned, the link none, the self-loop one."""
        counts = [ig.growth_demand_record(c)["new_demand_count"] for c in opening_children("L", "mu1")]
        self.assertEqual(sorted(int(str(c)) for c in counts), [0, 1, 1])

    def test_two_growths_always_create_the_fresh_pair_demand(self) -> None:
        for name in ("L", "F"):
            for child in opening_children(name, "mu1"):
                n = child.n_data()
                twice = ig.grow(ig.grow(child).child).child
                self.assertIn((n, n + 1), ig.demands(twice))

    def test_growth_alone_is_not_activity_and_a_fire_is(self) -> None:
        child = opening_children("L", "mu2")[0]
        grown = ig.grow(child).child
        self.assertFalse(ig.is_activity(child, grown))
        self.assertFalse(ig.is_inert(child, grown))
        fired = ig.fire(grown, "mu2")[0]
        self.assertTrue(ig.is_activity(grown, fired.child))


class Exhibits(unittest.TestCase):
    def test_linked_episodes_certify_and_fire_repeatedly(self) -> None:
        for name in ("L", "F"):
            record = ig.linked_episodes(ig.READINGS[name], "mu2", 10)
            branches = record["branches"]
            assert isinstance(branches, list)
            for branch in branches:
                assert isinstance(branch, dict)
                self.assertTrue(branch["certified"])
                self.assertTrue(branch["final_good"])
                self.assertGreaterEqual(int(str(branch["fires"])), 2)
                self.assertTrue(branch["every_fire_is_activity"])
                self.assertTrue(branch["no_grow_is_activity"])
                families = branch["fire_families"]
                assert isinstance(families, list)
                self.assertTrue(all(int(str(f)) >= 1 for f in families))

    def test_removing_the_closure_law_removes_activity(self) -> None:
        record = ig.disabled_components(ig.READINGS["L"], "mu2", 6)
        no_closure = record["no_closure"]
        assert isinstance(no_closure, dict)
        self.assertEqual(no_closure["kinds"], ["grow"])
        self.assertFalse(no_closure["any_activity"])
        self.assertGreater(int(str(no_closure["final_demands"])), 0)

    def test_removing_the_growth_law_stops_at_the_fixpoint(self) -> None:
        record = ig.disabled_components(ig.READINGS["L"], "mu2", 6)
        no_growth = record["no_growth"]
        assert isinstance(no_growth, dict)
        self.assertTrue(no_growth["stopped_at_fixpoint"])
        self.assertEqual(no_growth["kinds"], [])
        both = record["both_laws"]
        assert isinstance(both, dict)
        self.assertGreaterEqual(int(str(both["fires"])), 1)

    def test_route_pair_has_one_endpoint_two_totals_and_one_future(self) -> None:
        record = ig.route_pair()
        self.assertTrue(record["endpoints_equal"])
        self.assertEqual((record["span_total_early"], record["span_total_late"]), (2, 3))
        self.assertTrue(record["continuations_agree"])

    def test_fixpoint_census_over_the_closed_exports(self) -> None:
        census = ig.fixpoint_census(REPO)
        for name in ("closed_L", "closed_F"):
            block = census[name]
            assert isinstance(block, dict)
            self.assertGreater(int(str(block["fixpoints"])), 0)
            self.assertTrue(block["all_good"])
            self.assertTrue(block["all_characterizations_hold"])
            self.assertTrue(block["all_two_growths_demand"])
            histogram = block["one_growth_demand_histogram"]
            assert isinstance(histogram, dict)
            self.assertTrue(set(histogram) <= {"0", "1"})


class NegativeCases(unittest.TestCase):
    """Each applied only to the claim it tests."""

    def test_hidden_supplied_comparison_reads_the_presentation(self) -> None:
        child = opening_children("L", "mu2")[0]
        grown = ig.grow(child).child
        other = ig.represent(grown, tuple(reversed(grown.data)))
        self.assertEqual(ig.demands(grown), ig.demands(other))
        self.assertNotEqual(ig.glyph_demands(grown), ig.glyph_demands(other))

    def test_dropped_tied_alternative_is_detected(self) -> None:
        truncated = ig.fire_first_class_only(ROOT_L, (0, 1), "mu1")
        self.assertFalse(ig.retains_all_classes(truncated, ROOT_L, (0, 1), "mu1"))
        self.assertTrue(ig.retains_all_classes(ig.fire_at(ROOT_L, (0, 1), "mu1"), ROOT_L, (0, 1), "mu1"))

    def test_precomputed_script_is_not_input_dependent(self) -> None:
        states = [ig.grow(c).child for c in opening_children("L", "mu1") if ig.demands(ig.grow(c).child)]
        self.assertGreaterEqual(len(states), 2)
        conditional = [(s, ig.fire(s, "mu2")[0].events) for s in states]
        script = ig.scripted_events(conditional[0][1])
        scripted = [(s, ig.scripted_events(script)) for s in states]
        self.assertTrue(ig.input_dependent(conditional))
        self.assertFalse(ig.input_dependent(scripted))

    def test_unrepresented_growth_fails_certification(self) -> None:
        child = opening_children("L", "mu2")[0]
        history = ig.READINGS["L"].genesis + ig.fire(ROOT_L, "mu2", ig.BOUNDS, [(0, 1)])[0].events
        self.assertTrue(certify(history, child))
        self.assertFalse(certify(history, ig.phantom_grow(child)))
        step = ig.grow(child)
        self.assertTrue(certify(history + step.events, step.child))

    def test_inert_event_is_not_activity(self) -> None:
        child = opening_children("L", "mu2")[0]
        after = replay((Supply("anything"),), child)
        self.assertTrue(ig.is_inert(child, after))
        self.assertFalse(ig.is_activity(child, after))

    def test_invalid_demand_translation_is_refused(self) -> None:
        child = opening_children("L", "mu2")[0]
        grown = ig.grow(child).child
        # datum 0 is marked and datum 2 is fresh: separated, not a demand
        self.assertTrue(ig.verdicts(grown)[(0, 2)])
        with self.assertRaisesRegex(ig.IgnitionError, "not a demand"):
            ig.fire_at(grown, (0, 2), "mu2")
        with self.assertRaisesRegex(ig.IgnitionError, "not an ordered pair"):
            ig.fire_at(child, (1, 0), "mu2")
        with self.assertRaisesRegex(ig.IgnitionError, "already a standing requirement"):
            ig.fire_at(child, (0, 1), "mu2")
        imposed = replay((Impose(*ig.demands(grown)[0]),), grown)
        with self.assertRaisesRegex(ig.IgnitionError, "already a standing requirement"):
            ig.fire_at(imposed, ig.demands(grown)[0], "mu2")

    def test_regressing_response_is_rejected(self) -> None:
        base, target, delta = ig.regressing_response_example()
        self.assertFalse(response_valid_naive(base, target, delta))
        augmented = replay((Impose(*target),) + delta_events(base, delta), base)
        self.assertTrue(ig.verdicts(augmented)[target])
        self.assertFalse(ig.requirements_separated(augmented))
        self.assertNotIn(delta, [s.delta for s in ig.fire_at(base, target, "mu1")])

    def test_name_collision_is_refused_not_absorbed(self) -> None:
        colliding = Regime(("a", "g2"), (), frozenset(), frozenset(), frozenset())
        with self.assertRaisesRegex(ig.IgnitionError, "collides"):
            ig.grow(colliding)
        absorbed = replay((Supply("g2"), AdmitDatum("g2")), colliding)
        self.assertEqual(absorbed, colliding)

    def test_rule_bearing_base_is_refused(self) -> None:
        base = Regime(("a", "b"), (1,), frozenset(), frozenset({0}), frozenset())
        with self.assertRaisesRegex(ig.IgnitionError, "rule-free"):
            ig.fire_at(base, (0, 1), "mu1")

    def test_selection_outside_the_family_is_refused(self) -> None:
        with self.assertRaisesRegex(ig.IgnitionError, "outside the family"):
            ig.drive(ig.READINGS["L"].genesis, "mu2", 1, [5], root_targets=[(0, 1)])

    def test_a_minimum_never_carries_a_rule_or_an_unused_form(self) -> None:
        for child in opening_children("L", "mu1"):
            grown = ig.grow(ig.grow(child).child).child
            for s in ig.fire(grown, "mu1"):
                self.assertTrue(ig.rule_free(s.child))
                used = {f for (f, _) in s.child.insts}
                self.assertEqual(used, set(range(len(s.child.forms))))
                self.assertTrue(any(isinstance(it, NewInst) for it in s.delta))


if __name__ == "__main__":
    unittest.main()
