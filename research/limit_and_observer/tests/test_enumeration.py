"""The enumerator, certified rather than trusted.

The prefix enumerator is certified by **set equality** against an
independently written superset construction one coordinate wider in each
direction.  The two pruning lemmas are cross-checked against the unpruned
enumeration.
"""

from __future__ import annotations

import itertools
import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

from code.demands import DEMANDS_BY_NAME, Situation  # noqa: E402
from code.enumerate_space import (  # noqa: E402
    DEFAULT_BOUNDS,
    Bounds,
    inert_context,
    iter_candidates,
    reader_suffixes,
    sealed_prefixes,
    superset_prefixes,
)
from code.grammar import contexts  # noqa: E402
from code.items import (  # noqa: E402
    AddContext,
    NewReader,
    StatedState,
    apply_delta,
    canonical_delta,
    item_key,
    mu1,
)
from code.readers import (  # noqa: E402
    Reader,
    all_reading_classes,
    behaviour,
    induced_relation,
    lawful_aggregations,
)
from code.regime import genesis  # noqa: E402


class PrefixEnumeratorIsCertified(unittest.TestCase):
    """Set equality against an independently written superset."""

    def test_prefixes_equal_the_superset_construction(self) -> None:
        for reading in ("L", "F"):
            base = genesis(reading)
            for k in (0, 1, 2, 3):
                mine = set(sealed_prefixes(base, k, DEFAULT_BOUNDS))
                theirs = set(superset_prefixes(base, k, DEFAULT_BOUNDS))
                self.assertEqual(
                    mine, theirs,
                    f"reading {reading} at {k} items: "
                    f"only in breadth {sorted(mine - theirs, key=str)[:3]}; "
                    f"only in superset {sorted(theirs - mine, key=str)[:3]}",
                )

    def test_the_superset_is_genuinely_wider(self) -> None:
        """The certification is worth something only if the superset really
        offers items the breadth search cannot reach on its own."""
        base = genesis("L")
        wide = superset_prefixes(base, 2, DEFAULT_BOUNDS)
        self.assertTrue(wide)
        # a form index one beyond what the base declares is in the universe
        from code.items import NewRuleAll

        universe_has_wider = any(
            isinstance(it, NewRuleAll) and it.form >= len(base.forms)
            for d in wide for it in d
        )
        self.assertTrue(universe_has_wider or len(base.forms) == 0)

    def test_every_prefix_has_exactly_its_item_count(self) -> None:
        for k in (0, 1, 2, 3):
            for d in sealed_prefixes(genesis("F"), k, DEFAULT_BOUNDS):
                self.assertEqual(mu1(d), k)

    def test_prefixes_are_canonically_ordered(self) -> None:
        for k in (1, 2, 3):
            for d in sealed_prefixes(genesis("F"), k, DEFAULT_BOUNDS):
                self.assertEqual(d, canonical_delta(d))
                self.assertEqual(
                    list(d), sorted(d, key=item_key)
                )


class PruningIsSoundForMinima(unittest.TestCase):
    """Each pruning lemma, cross-checked against the unpruned enumeration."""

    def test_an_inert_context_changes_no_verdict(self) -> None:
        """The lemma itself: adding an inert context leaves the induced
        relation identical, so no minimum candidate contains one."""
        from code.census import population

        checked = 0
        for r in population(2, DEFAULT_BOUNDS):
            ctx = contexts(r)
            for b in all_reading_classes():
                inert = [c for c in ctx if inert_context(r, b, c)]
                live = [c for c in ctx if not inert_context(r, b, c)]
                if not inert or not live:
                    continue
                for a in lawful_aggregations(3):
                    without = induced_relation(r, Reader((live[0],), b, a))
                    with_inert = induced_relation(
                        r, Reader((live[0], inert[0]), b, a)
                    )
                    self.assertEqual(without, with_inert)
                    checked += 1
        self.assertGreater(checked, 0, "the lemma must have live witnesses")

    def test_pruned_and_unpruned_minima_agree(self) -> None:
        """The whole point: pruning may drop candidates, but never changes
        the *minimum* item count at which a demand is answered."""
        from code.price import price

        tight = Bounds(
            max_items=4, max_sealed_items=3, max_reader_items=2,
            max_arity=1, w_max=3, max_readers=2,
        )
        for name in ("OBS-1", "OBS-2"):
            for reading in ("L", "F"):
                a = price(genesis(reading), reading,
                          DEMANDS_BY_NAME[name], "mu1", tight, prune=True)
                b = price(genesis(reading), reading,
                          DEMANDS_BY_NAME[name], "mu1", tight, prune=False)
                self.assertEqual(a.cost, b.cost, f"{name}/{reading}")
                self.assertLessEqual(
                    len(a.raw_minima), len(b.raw_minima)
                )

    def test_unpruned_suffixes_are_a_superset_of_pruned_ones(self) -> None:
        base = genesis("L")
        r = apply_delta(
            StatedState(base, ()),
            tuple(sealed_prefixes(base, 2, DEFAULT_BOUNDS))[0], 3, 2
        ).regime
        for s in (1, 2):
            pruned = set(reader_suffixes(r, s, DEFAULT_BOUNDS, prune=True))
            full = set(reader_suffixes(r, s, DEFAULT_BOUNDS, prune=False))
            self.assertTrue(pruned <= full)


class SuffixesAreWellFormed(unittest.TestCase):
    def test_every_suffix_has_exactly_its_item_count(self) -> None:
        base = genesis("F")
        for prefix, r in sealed_prefixes(base, 2, DEFAULT_BOUNDS).items():
            for s in (0, 1, 2, 3):
                for suffix in itertools.islice(
                    reader_suffixes(r, s, DEFAULT_BOUNDS), 50
                ):
                    self.assertEqual(mu1(suffix), s)

    def test_a_suffix_buys_one_reader_before_its_contexts(self) -> None:
        base = genesis("F")
        r = apply_delta(
            StatedState(base, ()),
            tuple(sealed_prefixes(base, 2, DEFAULT_BOUNDS))[0], 3, 2
        ).regime
        for suffix in itertools.islice(
            reader_suffixes(r, 3, DEFAULT_BOUNDS), 200
        ):
            readers = [i for i in suffix if isinstance(i, NewReader)]
            adds = [i for i in suffix if isinstance(i, AddContext)]
            self.assertTrue(readers)
            for it in adds:
                self.assertLess(it.reader, len(readers))

    def test_candidates_apply_without_refusal(self) -> None:
        for total in (0, 1, 2, 3):
            for delta, state in itertools.islice(
                iter_candidates(genesis("L"), total, DEFAULT_BOUNDS), 300
            ):
                self.assertEqual(mu1(delta), total)
                self.assertLessEqual(len(state.readers), 2)
                for rho in state.readers:
                    self.assertLessEqual(rho.width(), 3)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
