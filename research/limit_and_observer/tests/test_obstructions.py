"""The three limit obstructions, each with its positive control.

An obstruction without a positive control is a demand nothing finite could
meet, and is reported OPEN rather than as an obstruction.  Each control below
exhibits an object showing the demand's tests can be passed at all.
"""

from __future__ import annotations

import itertools
import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

from code.census import (  # noqa: E402
    capacity_census,
    chain_census,
    limf_control,
    population,
    control_family_functions,
    family_novel,
    family_stable,
)
from code.demands import (  # noqa: E402
    DEMANDS_BY_NAME,
    Situation,
    limf_family_verdict,
    limg_growth,
    limr_refinement,
    reads_only_the_stage,
    strict_split_chain_length,
)
from code.enumerate_space import DEFAULT_BOUNDS  # noqa: E402
from code.grammar import contexts, data_pairs  # noqa: E402
from code.items import (  # noqa: E402
    AddContext,
    NewDatum,
    NewForm,
    NewInst,
    NewReader,
    NewRuleAll,
    StatedState,
    apply_delta,
)
from code.readers import (  # noqa: E402
    Reader,
    UNCOVERED,
    behaviour as behaviour_of,
    monotone_aggregations,
    all_reading_classes,
    induced_blocks,
    induced_relation,
    lawful_aggregations,
    signature,
)
from code.regime import Regime, genesis  # noqa: E402

POP = population(3, DEFAULT_BOUNDS)


def _reps():  # type: ignore[no-untyped-def]
    from code.readers import behaviour

    seen: dict[tuple[bool, bool], object] = {}
    for b in all_reading_classes():
        seen.setdefault(behaviour(b), b)
    return tuple(seen[k] for k in sorted(seen))


class RefinementIsObstructedAtTheCarrier(unittest.TestCase):
    """LIM-R.  The proof: the block count starts at one, rises by at least
    one at every strict split, and never exceeds the carrier."""

    def test_a_strict_split_raises_the_block_count_for_monotone_only(
        self,
    ) -> None:
        """The proof's hypothesis, and exactly how far it reaches.

        For a **monotone** lawful aggregation the block count never falls when
        a context is added, which is what the chain bound needs.  For the other
        two lawful aggregations it can fall, and the next test exhibits one."""
        checked = 0
        for r in POP:
            ctx = contexts(r)
            for b in _reps():
                for a in monotone_aggregations(3):
                    for w in range(1, min(3, len(ctx)) + 1):
                        for sel in itertools.combinations(ctx, w):
                            before = induced_blocks(
                                r, Reader(sel[:-1], b, a)  # type: ignore[arg-type]
                            )
                            after = induced_blocks(
                                r, Reader(sel, b, a)  # type: ignore[arg-type]
                            )
                            self.assertGreaterEqual(after, before)
                            checked += 1
        self.assertGreater(checked, 0)

    def test_a_non_monotone_aggregation_can_lower_the_block_count(
        self,
    ) -> None:
        """COUNTERMODEL, and a narrowing of this tree's own first statement
        of the refinement proof.

        Under the parity aggregation two data separated at one context are
        **identified** once a second context also tells them apart, so the
        block count falls from 2 to 1.  The block-count proof therefore covers
        the monotone aggregations only; for the other two the chain bound is a
        bounded computation over the declared population and is reported as
        one."""
        parity = (False, True, False, True)
        self.assertIn(parity, lawful_aggregations(3))
        self.assertNotIn(parity, monotone_aggregations(3))
        base = genesis("L")
        r = apply_delta(
            StatedState(base, ()), (NewForm(2), NewInst(0, (0, 0))), 3, 2
        ).regime
        ctx = contexts(r)
        sel = ((0, (None, None)), (0, (None, 0)))
        for c in sel:
            self.assertIn(c, ctx)
        # a reading that reads where coverage is absent; this regime declares
        # no rule, so a covered-only reading would read nothing here
        b = next(
            x for x in all_reading_classes()
            if behaviour_of(x) == UNCOVERED
        )
        one = induced_blocks(r, Reader(sel[:1], b, parity))
        two = induced_blocks(r, Reader(sel, b, parity))
        self.assertEqual((one, two), (2, 1))

    def test_the_chain_bound_still_holds_for_every_lawful_aggregation(
        self,
    ) -> None:
        """The obstruction survives the narrowing, as a computation.

        The proof reaches the monotone aggregations; this checks the bound
        itself over the whole population for all four, which is the evidence
        the non-monotone half rests on."""
        for r in POP:
            ctx = contexts(r)
            n = r.n_data()
            for b in _reps():
                for a in lawful_aggregations(3):
                    for w in range(0, min(3, len(ctx)) + 1):
                        for sel in itertools.combinations(ctx, w):
                            m = strict_split_chain_length(
                                r, Reader(sel, b, a)  # type: ignore[arg-type]
                            )
                            self.assertLessEqual(m, max(n - 1, 0))

    def test_no_chain_exceeds_the_carrier_minus_one(self) -> None:
        for r in POP:
            ctx = contexts(r)
            if not ctx:
                continue
            for b in _reps():
                for a in lawful_aggregations(3):
                    for w in range(0, min(3, len(ctx)) + 1):
                        for sel in itertools.combinations(ctx, w):
                            m = strict_split_chain_length(
                                r, Reader(sel, b, a)  # type: ignore[arg-type]
                            )
                            self.assertLessEqual(m, max(r.n_data() - 1, 0))

    def test_the_demand_is_unsatisfiable_at_every_state(self) -> None:
        for r in POP:
            ctx = contexts(r)
            for b in _reps():
                for a in lawful_aggregations(3):
                    for w in range(0, min(3, len(ctx)) + 1):
                        for sel in itertools.combinations(ctx, w):
                            state = StatedState(
                                r, (Reader(sel, b, a),)  # type: ignore[arg-type]
                            )
                            sit = Situation(r, (), state, None, 3)
                            self.assertFalse(limr_refinement(sit))

    def test_the_short_circuit_agrees_with_the_unabridged_search(
        self,
    ) -> None:
        """LIM-R skips the chain search when no reader is wider than the
        carrier.  That is an equivalence, not a heuristic, and it is checked
        against the unabridged computation rather than asserted."""
        checked = 0
        for r in POP:
            ctx = contexts(r)
            n = r.n_data()
            for b in _reps():
                for a in lawful_aggregations(3):
                    for w in range(0, min(3, len(ctx)) + 1):
                        for sel in itertools.combinations(ctx, w):
                            rho = Reader(sel, b, a)  # type: ignore[arg-type]
                            state = StatedState(r, (rho,))
                            short = limr_refinement(
                                Situation(r, (), state, None, 3)
                            )
                            full = (
                                strict_split_chain_length(r, rho) > n
                            )
                            self.assertEqual(short, full)
                            checked += 1
        self.assertGreater(checked, 0)

    def test_a_chain_is_never_longer_than_the_selection(self) -> None:
        """The lemma the short-circuit rests on."""
        for r in POP:
            ctx = contexts(r)
            for b in _reps():
                for a in lawful_aggregations(3):
                    for w in range(0, min(3, len(ctx)) + 1):
                        for sel in itertools.combinations(ctx, w):
                            rho = Reader(sel, b, a)  # type: ignore[arg-type]
                            self.assertLessEqual(
                                strict_split_chain_length(r, rho), w
                            )

    def test_the_positive_control_the_ceiling_is_attained(self) -> None:
        """Without attainment the obstruction would be vacuous."""
        c = chain_census(3, DEFAULT_BOUNDS)
        self.assertGreater(c["carrier_ceiling_attained"], 0)  # type: ignore[arg-type]
        self.assertEqual(c["chains_above_the_ceiling"], 0)

    def test_growth_does_not_lift_it(self) -> None:
        """The threshold is stated relative to the carrier and the ceiling
        tracks the carrier, so admitting data raises both together.

        Scope, so that this is not read as more than it is: **two** growth
        items on **one** exhibited regime.  What covers *any* number of growth
        items is the Lean theorem
        ``refinement_obstruction_survives_growth``, and what covers every
        carrier the population reaches is ``chain_census``.  LO-10 in
        ``CLAIM_LEDGER.md`` reports all three separately for that reason."""
        r = genesis("F")
        state = apply_delta(
            StatedState(r, ()), (NewForm(1), NewInst(0, (0,))), 3, 2
        ).regime
        for extra in range(0, 3):
            grown = apply_delta(
                StatedState(state, ()), tuple(NewDatum() for _ in range(extra)),
                3, 2,
            ).regime
            ctx = contexts(grown)
            best = 0
            for b in _reps():
                for a in lawful_aggregations(3):
                    for w in range(0, min(3, len(ctx)) + 1):
                        for sel in itertools.combinations(ctx, w):
                            best = max(
                                best,
                                strict_split_chain_length(
                                    grown, Reader(sel, b, a)  # type: ignore[arg-type]
                                ),
                            )
            self.assertLessEqual(best, grown.n_data() - 1)
            self.assertLess(best, grown.n_data())


class GrowthIsObstructedAtTheWidth(unittest.TestCase):
    """LIM-G.  The proof: equal signatures force ``s = 0`` and ``a(0)`` is
    false, so the non-separation relation is coarser than signature equality
    and has at most ``2 ** w`` blocks."""

    def test_equal_signatures_are_never_separated(self) -> None:
        checked = 0
        for r in POP:
            ctx = contexts(r)
            for b in _reps():
                for a in lawful_aggregations(3):
                    for w in range(0, min(3, len(ctx)) + 1):
                        for sel in itertools.combinations(ctx, w):
                            rho = Reader(sel, b, a)  # type: ignore[arg-type]
                            rel = induced_relation(r, rho)
                            for (i, j) in data_pairs(r.n_data()):
                                if signature(r, rho, i) == signature(
                                    r, rho, j
                                ):
                                    self.assertNotIn((i, j), rel)
                                    checked += 1
        self.assertGreater(checked, 0)

    def test_blocks_never_exceed_two_to_the_width(self) -> None:
        for r in POP:
            ctx = contexts(r)
            for b in _reps():
                for a in lawful_aggregations(3):
                    for w in range(0, min(3, len(ctx)) + 1):
                        for sel in itertools.combinations(ctx, w):
                            k = induced_blocks(
                                r, Reader(sel, b, a)  # type: ignore[arg-type]
                            )
                            self.assertLessEqual(k, 2 ** w)

    def test_a_carrier_above_the_threshold_identifies_some_pair(self) -> None:
        """The pigeonhole, exhibited: build a carrier larger than two to the
        width and check that every fixed-selection reader identifies a pair.

        **This exhibit is outside the declared candidate space, deliberately
        and by necessity.**  It takes eight sealed items where
        ``max_sealed_items`` is 4, because the threshold needs a carrier of 9
        and the declared space reaches 6 in reading L and 7 in reading F.  That
        is why LIM-G's empty price row is a fact about the item bound rather
        than about readers: the receipt records this exhibit by name under
        ``obstructions.LIM-G.positive_control`` and says so."""
        base = genesis("F")
        wide = apply_delta(
            StatedState(base, ()),
            (NewForm(1), NewRuleAll(0)) + tuple(NewDatum() for _ in range(6)),
            3, 2,
        ).regime
        self.assertGreater(wide.n_data(), 2 ** 3)
        ctx = contexts(wide)
        universe = frozenset(data_pairs(wide.n_data()))
        for b in _reps():
            for a in lawful_aggregations(3):
                for w in range(0, min(3, len(ctx)) + 1):
                    for sel in itertools.combinations(ctx, w):
                        rel = induced_relation(
                            wide, Reader(sel, b, a)  # type: ignore[arg-type]
                        )
                        self.assertNotEqual(rel, universe)

    def test_the_demand_is_unsatisfiable_within_the_population(self) -> None:
        for r in POP:
            ctx = contexts(r)
            for b in _reps():
                for a in lawful_aggregations(3):
                    for w in range(0, min(3, len(ctx)) + 1):
                        for sel in itertools.combinations(ctx, w):
                            state = StatedState(
                                r, (Reader(sel, b, a),)  # type: ignore[arg-type]
                            )
                            self.assertFalse(
                                limg_growth(
                                    Situation(r, (), state, None, 3)
                                )
                            )

    def test_the_positive_control_a_separating_reader_exists_below_it(
        self,
    ) -> None:
        c = capacity_census(3, DEFAULT_BOUNDS)
        self.assertTrue(c["separating_reader_found"])
        self.assertEqual(c["carrier_threshold"], 8)


class TheFamilyVerdictIsObstructed(unittest.TestCase):
    """LIM-F.  The content is the exhaustiveness check; the core implication
    is definition-level and is reported as such."""

    def test_no_admitted_item_reads_beyond_its_stage(self) -> None:
        from code.enumerate_space import iter_candidates

        for total in (1, 2, 3, 4):
            for delta, _ in itertools.islice(
                iter_candidates(genesis("F"), total, DEFAULT_BOUNDS), 400
            ):
                self.assertTrue(reads_only_the_stage(delta))

    def test_the_demand_is_unsatisfiable(self) -> None:
        from code.enumerate_space import iter_candidates

        for total in (1, 2, 3):
            for delta, state in itertools.islice(
                iter_candidates(genesis("L"), total, DEFAULT_BOUNDS), 300
            ):
                self.assertFalse(
                    limf_family_verdict(
                        Situation(genesis("L"), delta, state, (0, 1), 3)
                    )
                )

    def test_the_positive_control_passes(self) -> None:
        """Hand-supplied metatheory functions, never admitted, showing the
        stability and novelty tests can be passed at all."""
        control = limf_control((False,) * 16, 12)
        self.assertTrue(any(control.values()))
        self.assertTrue(control["not the first verdict"])

    def test_novelty_is_satisfiable_exactly_on_a_constant_sequence(
        self,
    ) -> None:
        """A two-valued verdict cannot differ from every member of a sequence
        containing both values.  Definition-level, and labelled so."""
        mixed = (True, False, True)
        for f in control_family_functions().values():
            self.assertFalse(family_novel(mixed, f))
        constant = (False,) * 5
        self.assertTrue(
            any(family_novel(constant, f)
                for f in control_family_functions().values())
        )

    def test_stability_holds_on_the_declared_window(self) -> None:
        values = (False,) * 16
        f = control_family_functions()["not the first verdict"]
        self.assertTrue(family_stable(values, 12, f))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
