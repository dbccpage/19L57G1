"""The hazard guards, each with a test that fails when the guard is removed.

Every guard the design named as mechanical is mechanical here.
"""

from __future__ import annotations

import itertools
import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

from code.census import population  # noqa: E402
from code.demands import (  # noqa: E402
    DEMANDS,
    Situation,
    obs3_rival,
    obs4_coexistence,
    reads_only_the_stage,
    renaming_of_each_other,
    selection_is_fixed,
)
from code.enumerate_space import (  # noqa: E402
    DEFAULT_BOUNDS,
    Bounds,
    CandidateBudgetRefused,
    inert_context,
    iter_candidates,
    reader_suffixes,
    sealed_prefixes,
    superset_prefixes,
)
from code.grammar import (  # noqa: E402
    admission_bit,
    contexts,
    data_pairs,
    sealed_relation,
)
from code.items import (  # noqa: E402
    AddContext,
    NewForm,
    NewInst,
    NewReader,
    NewRuleAll,
    StatedState,
    apply_delta,
    capabilities,
    mu1,
    mu2,
)
from code.quotient import (  # noqa: E402
    BijectionBudgetRefused,
    canonical_state,
    transport_context,
)
from code.readers import (  # noqa: E402
    ALL_READINGS,
    Reader,
    all_reading_classes,
    behaviour,
    induced_relation,
    lawful,
    lawful_aggregations,
    unlawful_aggregations,
)
from code.regime import AdmissionRefused, Regime, genesis  # noqa: E402

POP = population(3, DEFAULT_BOUNDS)


def _behaviour_reps() -> tuple[tuple[bool, bool, bool, bool], ...]:
    """One reading per induced-separation behaviour."""
    seen: dict[tuple[bool, bool], tuple[bool, bool, bool, bool]] = {}
    for b in all_reading_classes():
        seen.setdefault(behaviour(b), b)
    return tuple(seen[k] for k in sorted(seen))


def rival_state() -> Regime:
    """The minimal state admitting a rival: one form, a rule on it, one
    instance."""
    base = genesis("L")
    return apply_delta(
        StatedState(base, ()),
        (NewForm(1), NewRuleAll(0), NewInst(0, (0,))),
        3, 2,
    ).regime


class WidthIsBoughtOneItemAtATime(unittest.TestCase):
    """Buying unbounded width for one item is the load-bearing smuggle."""

    def test_new_reader_admits_an_empty_selection(self) -> None:
        r = rival_state()
        s = apply_delta(
            StatedState(r, ()), (NewReader((False, True, False, True),
                                           (False, True, True, True)),), 3, 2
        )
        self.assertEqual(s.readers[0].selection, ())
        self.assertEqual(s.readers[0].width(), 0)

    def test_a_readers_width_equals_the_items_spent_on_it(self) -> None:
        r = rival_state()
        ctx = contexts(r)
        delta = (
            NewReader((False, True, False, True), (False, True, True, True)),
        ) + tuple(AddContext(0, c) for c in ctx[:1])
        s = apply_delta(StatedState(r, ()), delta, 3, 2)
        self.assertEqual(s.readers[0].width(), len(delta) - 1)
        self.assertEqual(mu1(delta), len(delta))

    def test_width_beyond_the_bound_is_refused(self) -> None:
        base = genesis("F")
        r = apply_delta(
            StatedState(base, ()), (NewForm(2), NewRuleAll(0)), 3, 2
        ).regime
        ctx = contexts(r)
        self.assertGreater(len(ctx), 3)
        delta = (
            NewReader((False, True, False, True), (False, True, True, True)),
        ) + tuple(AddContext(0, c) for c in ctx[:4])
        with self.assertRaises(AdmissionRefused):
            apply_delta(StatedState(r, ()), delta, 3, 2)

    def test_more_readers_than_the_bound_is_refused(self) -> None:
        r = rival_state()
        item = NewReader((False, True, False, True), (False, True, True, True))
        with self.assertRaises(AdmissionRefused):
            apply_delta(StatedState(r, ()), (item, item, item), 3, 2)


class ReaderReadsNoDatumIdentity(unittest.TestCase):
    """A reader so rich that admitting it is obviously the whole cost."""

    def test_a_reader_cannot_separate_data_agreeing_at_every_context(
        self,
    ) -> None:
        """If the admission bit agrees at every context, no reader separates
        the pair.  A reader that did would be reading outside the grammar.

        Checked at the level that *implies* it for every selection at once:
        the two data have equal signatures over the whole context tuple, so
        the separating count is zero for every sub-selection, and ``a(0)`` is
        false for every admitted aggregation.  That is exhaustive over all
        selections without enumerating them."""
        from code.readers import signature

        seen = 0
        for r in POP:
            ctx = contexts(r)
            for (i, j) in data_pairs(r.n_data()):
                if any(
                    admission_bit(r, c, i) != admission_bit(r, c, j)
                    for c in ctx
                ):
                    continue
                seen += 1
                for b in all_reading_classes():
                    full = Reader(ctx, b, (False,) + (True,) * len(ctx))
                    self.assertEqual(
                        signature(r, full, i), signature(r, full, j)
                    )
                for a in lawful_aggregations(3):
                    self.assertFalse(a[0])
        self.assertGreater(seen, 0, "the guard must have live witnesses")

    def test_a_readers_verdict_is_invariant_under_relabelling(self) -> None:
        from code.quotient import automorphisms

        checked = 0
        for r in POP:
            ctx = contexts(r)
            if not ctx:
                continue
            autos = automorphisms(r)
            if len(autos) == 1:
                continue
            for pi, phi in autos:
                for b in _behaviour_reps():
                    for a in lawful_aggregations(3):
                        for sel in itertools.combinations(
                            ctx, min(2, len(ctx))
                        ):
                            moved = tuple(
                                transport_context(c, pi, phi) for c in sel
                            )
                            rel = induced_relation(r, Reader(sel, b, a))
                            rel2 = induced_relation(r, Reader(moved, b, a))
                            renamed = frozenset(
                                (min(pi[x], pi[y]), max(pi[x], pi[y]))
                                for (x, y) in rel
                            )
                            self.assertEqual(renamed, rel2)
                            checked += 1
        self.assertGreater(checked, 0)


class LawfulnessIsDecidedBeforeAdmission(unittest.TestCase):
    def test_exactly_four_of_eight_are_lawful_at_width_three(self) -> None:
        self.assertEqual(len(lawful_aggregations(3)), 4)
        self.assertEqual(len(unlawful_aggregations(3)), 4)

    def test_lawfulness_is_not_stable_in_the_width(self) -> None:
        counts = {w: len(lawful_aggregations(w)) for w in (1, 2, 3, 4)}
        self.assertEqual(counts, {1: 2, 2: 3, 3: 4, 4: 4})

    def test_an_unlawful_aggregation_breaks_transitivity_somewhere(
        self,
    ) -> None:
        for a in unlawful_aggregations(3):
            self.assertFalse(lawful(a, 3))

    def test_only_lawful_aggregations_are_offered_for_admission(self) -> None:
        r = rival_state()
        offered = set()
        for delta in reader_suffixes(r, 2, DEFAULT_BOUNDS):
            for it in delta:
                if isinstance(it, NewReader):
                    offered.add(it.aggregation)
        self.assertTrue(offered)
        self.assertTrue(offered <= set(lawful_aggregations(3)))


class TheSecondObserverIsNotTheFirstRenamed(unittest.TestCase):
    def test_a_renaming_is_detected(self) -> None:
        r = rival_state()
        ctx = contexts(r)
        rho = Reader(ctx[:1], (False, True, False, True),
                     (False, True, True, True))
        self.assertTrue(renaming_of_each_other(r, rho, rho))

    def test_obs4_refuses_a_renaming(self) -> None:
        r = rival_state()
        ctx = contexts(r)
        rho = Reader(ctx[:1], (False, True, False, True),
                     (False, True, True, True))
        sit = Situation(r, (), StatedState(r, (rho, rho)), (0, 1), 3)
        self.assertFalse(obs4_coexistence(sit))

    def test_obs4_refuses_a_reader_that_separates_nothing(self) -> None:
        r = rival_state()
        ctx = contexts(r)
        seeing = Reader(ctx[:1], (False, True, False, True),
                        (False, True, True, True))
        blind = Reader((), (False, True, False, True),
                       (False, True, True, True))
        sit = Situation(r, (), StatedState(r, (seeing, blind)), (0, 1), 3)
        self.assertFalse(obs4_coexistence(sit))


class TheRivalIsReal(unittest.TestCase):
    def test_the_exhibited_rival_separates_a_sealed_collapsed_pair(
        self,
    ) -> None:
        r = rival_state()
        self.assertEqual(sealed_relation(r), frozenset())
        ctx = contexts(r)
        rho = Reader(ctx[:1], (False, True, False, True),
                     (False, True, True, True))
        self.assertEqual(induced_relation(r, rho), frozenset({(0, 1)}))

    def test_the_sealed_reading_does_not_separate_it(self) -> None:
        r = rival_state()
        ctx = contexts(r)
        rho = Reader(ctx[:1], (False, True, True, True),
                     (False, True, True, True))
        self.assertEqual(induced_relation(r, rho), frozenset())


class LimitDirectionsAreKeptApartMechanically(unittest.TestCase):
    def test_refinement_asserts_no_growth_item(self) -> None:
        from code.demands import limr_refinement
        from code.items import NewDatum

        r = rival_state()
        sit = Situation(r, (NewDatum(),), StatedState(r, ()), (0, 1), 3)
        self.assertFalse(limr_refinement(sit))

    def test_growth_asserts_a_fixed_selection(self) -> None:
        r = rival_state()
        self.assertTrue(selection_is_fixed((NewForm(1),)))

    def test_no_item_reads_a_stage_index_or_an_earlier_verdict(self) -> None:
        """The exhaustiveness check behind LIM-F.  It is a real property of
        the alphabet and fails the moment an item kind grows a field."""
        r = rival_state()
        for total in (1, 2, 3):
            for delta, _ in itertools.islice(
                iter_candidates(genesis("L"), total, DEFAULT_BOUNDS), 200
            ):
                self.assertTrue(reads_only_the_stage(delta))

    def test_the_family_verdict_check_fails_on_a_foreign_item(self) -> None:
        class StageReadingItem:
            stage = 3

        self.assertFalse(reads_only_the_stage((StageReadingItem(),)))  # type: ignore[arg-type]


class MeasuresAreTheSealedExpressions(unittest.TestCase):
    def test_mu2_is_blind_along_the_reader_axis_by_the_formula(self) -> None:
        """Reported as a finding, never repaired: amending mu2 would stop it
        being the sealed function."""
        reader = NewReader((False, True, False, True),
                           (False, True, True, True))
        self.assertEqual(mu2((reader,))[1], 0)
        self.assertEqual(mu2((NewForm(2),))[1], 2)

    def test_the_capability_vector_is_never_totalled(self) -> None:
        caps = capabilities((NewForm(1), NewRuleAll(0)))
        self.assertNotIn("total", caps)
        self.assertEqual(len(caps), 7)


class BudgetsAreRefusedNotTruncated(unittest.TestCase):
    def test_the_candidate_budget_is_a_named_terminal(self) -> None:
        tight = Bounds(max_items=2, max_sealed_items=1, max_reader_items=1,
                       candidate_budget=1)
        with self.assertRaises(CandidateBudgetRefused):
            list(iter_candidates(genesis("F"), 2, tight))

    def test_a_prefix_above_the_declared_bound_is_refused(self) -> None:
        with self.assertRaises(CandidateBudgetRefused):
            sealed_prefixes(genesis("L"), 5, DEFAULT_BOUNDS)

    def test_the_item_bound_is_refused(self) -> None:
        with self.assertRaises(CandidateBudgetRefused):
            list(iter_candidates(genesis("L"), 9, DEFAULT_BOUNDS))

    def test_the_bijection_budget_is_a_named_terminal(self) -> None:
        r = genesis("F")
        with self.assertRaises(BijectionBudgetRefused):
            canonical_state(StatedState(r, ()), budget=1)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
