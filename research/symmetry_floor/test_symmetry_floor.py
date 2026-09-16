"""Tests for the floor, the exit, and the thread.

Every claim in ``KERNEL.md`` and ``CLAIM_LEDGER.md`` is decided by a test here.
Nothing is asserted in prose that is not settled by a run.
"""

from __future__ import annotations

import unittest

import carrier
import floor
import thread


class TestCarrier(unittest.TestCase):
    def test_round_trip(self) -> None:
        for text in ("<>", "<|>", "<a>", "<a|b>", "<aab>", "<a||b>"):
            self.assertEqual(carrier.render(carrier.parse(text)), text)

    def test_parse_refuses_a_glyph_outside_the_carrier(self) -> None:
        with self.assertRaises(ValueError):
            carrier.parse("<a|b|c>")

    def test_renamings_are_their_own_inverse(self) -> None:
        for form in carrier.generation(4):
            for name in ("relabel", "reflect"):
                self.assertEqual(carrier.apply(name, carrier.apply(name, form)), form)

    def test_renamings_commute(self) -> None:
        for form in carrier.generation(4):
            self.assertEqual(
                carrier.relabel(carrier.reflect(form)),
                carrier.reflect(carrier.relabel(form)),
            )

    def test_ways_count_divides_four(self) -> None:
        for form in carrier.generation(4):
            self.assertIn(len(carrier.ways(form)), (1, 2, 4))
            self.assertEqual(len(carrier.ways(form)) * len(carrier.held(form)), 4)

    def test_generation_is_the_whole_of_its_size(self) -> None:
        for k in range(6):
            forms = carrier.generation(k)
            self.assertEqual(len(forms), 3**k)
            self.assertTrue(all(carrier.size(f) == k for f in forms))

    def test_mirror_of_the_minimal_boundary_is_the_same_object(self) -> None:
        """``<a|b>`` cannot tell itself from its reflection once glyphs are forgotten."""
        here = carrier.parse("<a|b>")
        self.assertEqual(
            carrier.name_of(here), carrier.name_of(carrier.reflect(here))
        )


class TestFloor(unittest.TestCase):
    def setUp(self) -> None:
        self.big = floor.closed_carrier(2, 3)
        self.small = floor.closed_carrier(1, 1)

    def test_every_constructed_rule_holds_the_floor(self) -> None:
        built = 0
        for source in self.big:
            for target in self.big:
                if not carrier.held(source) <= carrier.held(target):
                    continue
                rule = floor.rule_carrying(source, target)
                if rule is None:
                    continue
                built += 1
                self.assertTrue(floor.holds_the_floor(rule, self.big))
        self.assertGreater(built, 20000)

    def test_containment_is_necessary_and_sufficient(self) -> None:
        self.assertEqual(floor.containment_matches_constructibility(self.big), [])

    def test_exhaustion_over_every_map(self) -> None:
        """Counted by index arithmetic, without consulting the characterisation."""
        self.assertEqual(len(self.small), 8)
        counted = floor.counted_rule_count(self.small)
        predicted = floor.predicted_rule_count(self.small)
        self.assertEqual(counted, predicted)
        self.assertEqual(counted, 128)

    def test_a_rule_that_reads_glyphs_is_not_a_rule_of_this_kind(self) -> None:
        """Negative: a map that reads which glyph is which fails both tests.

        It breaks the floor, which is the point -- such a map is exactly what is
        excluded by the explicit renaming-equivariance premise.  It also shows
        that merely being a function of the inscription does not imply that
        premise.
        """
        empty = carrier.parse("<>")
        leaked = carrier.parse("<a>")
        reads_glyphs = lambda x: leaked if x == empty else x
        self.assertFalse(floor.agrees_with_renamings(reads_glyphs, self.big))
        self.assertFalse(floor.holds_the_floor(reads_glyphs, self.big))

    def test_price_of_a_break(self) -> None:
        price = floor.price_of_a_break(self.big)
        self.assertEqual(price.to_break_every_renaming, 4)
        for cost in price.to_break_one_renaming.values():
            self.assertEqual(cost, 2)


class TestThread(unittest.TestCase):
    def test_step_agrees_with_the_renamings(self) -> None:
        probe = [s for k in range(5) for s in carrier.generation(k)]
        self.assertEqual(thread.step_agrees_with_renamings(probe), [])

    def test_step_raises_the_size_by_exactly_one(self) -> None:
        for k in range(5):
            for form in carrier.generation(k):
                for later in thread.step(form):
                    self.assertEqual(carrier.size(later), k + 1)

    def test_the_thread_is_unique_at_every_generation(self) -> None:
        for k in range(9):
            self.assertTrue(thread.thread_is_unique(k))

    def test_the_thread_is_exactly_distance_zero(self) -> None:
        for k in range(8):
            for form in carrier.generation(k):
                self.assertEqual(
                    len(carrier.held(form)) == len(carrier.RENAMINGS),
                    thread.distance(form) == 0,
                )

    def test_distance_never_falls(self) -> None:
        for k in range(8):
            self.assertEqual(thread.distance_never_falls(k), [])

    def test_a_break_does_not_ratchet(self) -> None:
        """What is held still can rise again, even though the thread cannot."""
        returns = thread.held_can_return(2)
        self.assertTrue(returns)
        for before, after in returns:
            self.assertLess(len(carrier.held(before)), len(carrier.held(after)))
            self.assertGreater(thread.distance(after), 0)

    def test_first_break_and_its_cost(self) -> None:
        self.assertEqual(
            [c for c in carrier.objects(1) if len(carrier.held(c)) == 1], []
        )
        broken = [c for c in carrier.objects(2) if len(carrier.held(c)) == 1]
        self.assertEqual(len(broken), 1)
        self.assertEqual(len(carrier.ways(broken[0])), 4)

    def test_object_count_closed_form(self) -> None:
        for k in range(11):
            self.assertEqual(
                thread.object_count(k), thread.object_count_closed_form(k)
            )

    def test_the_world_does_not_remember(self) -> None:
        """By generation 8 almost nothing has a single possible past."""
        self.assertEqual(thread.single_past_count(8), 3)
        self.assertEqual(thread.object_count(8), 1681)

    def test_composite_renaming_needs_an_even_data_count(self) -> None:
        """A centre datum would have to be its own exchange, and none is."""
        for k in range(9):
            for form in carrier.generation(k):
                if "relabel.reflect" in carrier.held(form):
                    self.assertEqual(carrier.data_count(form) % 2, 0)

    def test_reflection_alone_tolerates_an_odd_data_count(self) -> None:
        """Separating the two: reflection has a centre available, the composite does not."""
        odd = [
            form
            for k in range(6)
            for form in carrier.generation(k)
            if "reflect" in carrier.held(form) and carrier.data_count(form) % 2 == 1
        ]
        self.assertTrue(odd)


if __name__ == "__main__":
    unittest.main()
