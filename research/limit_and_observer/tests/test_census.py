"""The censuses, and the refusal of a vacuous finding.

A census is published before any finding, and a finding whose supporting
count is zero is refused **by name** rather than quietly dropped.
"""

from __future__ import annotations

import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

from code.census import (  # noqa: E402
    VacuousFindingRefused,
    admits_rival,
    capacity_census,
    chain_census,
    column_kernel,
    monotonicity_census,
    population,
    reading_axis_census,
    refuse_if_vacuous,
    sealed_is_a_reader,
    vacuity_census,
)
from code.enumerate_space import DEFAULT_BOUNDS  # noqa: E402
from code.grammar import contexts, sealed_relation  # noqa: E402
from code.items import (  # noqa: E402
    NewForm,
    NewInst,
    NewRuleAll,
    StatedState,
    apply_delta,
)
from code.quotient import canonical_regime  # noqa: E402
from code.regime import genesis  # noqa: E402


class ThePopulationIsRecomputed(unittest.TestCase):
    def test_depth_three_population_is_eighty_five(self) -> None:
        self.assertEqual(len(population(3, DEFAULT_BOUNDS)), 85)

    def test_the_population_is_quotiented(self) -> None:
        pop = population(3, DEFAULT_BOUNDS)
        keys = {canonical_regime(r) for r in pop}
        self.assertEqual(len(keys), len(pop))

    def test_both_sealed_bases_carry_no_context(self) -> None:
        """So they can carry the calibration and no observation finding
        whatever."""
        for reading in ("L", "F"):
            self.assertEqual(contexts(genesis(reading)), ())


class GrammarMonotonicity(unittest.TestCase):
    def test_no_move_shrinks_the_context_set(self) -> None:
        c = monotonicity_census(3, DEFAULT_BOUNDS)
        self.assertEqual(c["violations"], 0)
        # Every item offered at every state of the population.  This is not
        # the 243 of PREDICTIONS.md P-1: that figure counted moves only from
        # the states expanded during the breadth rounds, leaving the depth-3
        # frontier unexpanded.  The census expands all 85.  The miss is
        # recorded in STATUS.md and the prediction is not edited.
        self.assertEqual(c["moves"], 1067)
        self.assertEqual(c["enlarge"], 227)
        self.assertEqual(c["unchanged"], 840)
        self.assertEqual(c["enlarge"] + c["unchanged"], c["moves"])


class NonVacuity(unittest.TestCase):
    def test_the_census_is_published_before_any_finding(self) -> None:
        c = vacuity_census(3, DEFAULT_BOUNDS)
        self.assertEqual(c["states"], 85)
        self.assertEqual(c["with_a_context"], 80)
        self.assertEqual(c["admits_a_rival"], 6)
        self.assertEqual(c["carrier_ceiling_attained"], 22)
        self.assertEqual(c["collapsed_pair_and_a_context"], 58)
        self.assertGreater(c["two_distinct_kernels"], 0)
        self.assertGreater(c["two_incomparable_kernels"], 0)

    def test_a_zero_count_is_refused_by_name(self) -> None:
        with self.assertRaises(VacuousFindingRefused):
            refuse_if_vacuous("a finding with no support", 0)
        self.assertEqual(refuse_if_vacuous("a supported finding", 3), 3)

    def test_every_rival_state_has_the_forced_shape(self) -> None:
        """Form, uniform rule on it, explicit instance — by exhaustion, not
        by argument."""
        found = 0
        for r in population(3, DEFAULT_BOUNDS):
            if not admits_rival(r):
                continue
            found += 1
            self.assertTrue(r.forms)
            self.assertTrue(r.rules)
            self.assertTrue(r.insts)
        self.assertEqual(found, 6)

    def test_a_rival_state_has_a_sealed_collapsed_pair(self) -> None:
        for r in population(3, DEFAULT_BOUNDS):
            if admits_rival(r):
                self.assertNotEqual(
                    len(sealed_relation(r)),
                    r.n_data() * (r.n_data() - 1) // 2,
                )

    def test_column_kernels_are_computed_from_the_admission_bit(self) -> None:
        base = genesis("L")
        r = apply_delta(
            StatedState(base, ()),
            (NewForm(1), NewRuleAll(0), NewInst(0, (0,))), 3, 2,
        ).regime
        c = contexts(r)[0]
        self.assertEqual(column_kernel(r, c), frozenset())


class TheSealedObserverIsInTheAxis(unittest.TestCase):
    def test_no_mismatch_anywhere_in_the_population(self) -> None:
        c = sealed_is_a_reader(3, DEFAULT_BOUNDS)
        self.assertEqual(c["mismatches"], 0)
        self.assertEqual(c["checked"], 85)


class RivalDerivability(unittest.TestCase):
    """The rival is derived at two admitted data and ADMITTED at three.

    Not uniform, and the non-uniformity is the finding: PREDICTIONS.md P-15
    asserted DERIVED, and that holds at two data and fails at three."""

    def test_derived_at_two_data_admitted_at_three(self) -> None:
        from code.census import rival_derivability_census

        c = rival_derivability_census(DEFAULT_BOUNDS)
        self.assertEqual(c["L"]["verdict"], "DERIVED")  # type: ignore[index]
        self.assertEqual(
            c["L"]["combinations_matching"], ["complement"]  # type: ignore[index]
        )
        self.assertEqual(c["F"]["verdict"], "ADMITTED")  # type: ignore[index]
        self.assertEqual(c["F"]["combinations_matching"], [])  # type: ignore[index]
        self.assertEqual(c["L"]["n_data"], 2)  # type: ignore[index]
        self.assertEqual(c["F"]["n_data"], 3)  # type: ignore[index]


class ChainAndCapacity(unittest.TestCase):
    def test_no_chain_exceeds_the_carrier_ceiling(self) -> None:
        c = chain_census(3, DEFAULT_BOUNDS)
        self.assertEqual(c["chains_above_the_ceiling"], 0)
        self.assertEqual(c["carrier_ceiling_attained"], 26)

    def test_the_capacity_threshold_is_derived(self) -> None:
        c = capacity_census(3, DEFAULT_BOUNDS)
        self.assertEqual(c["carrier_threshold"], 8)
        self.assertEqual(
            c["block_ceiling_by_width"], {1: 2, 2: 4, 3: 8}
        )
        self.assertTrue(c["separating_reader_found"])

    def test_the_axis_census_reports_both_collapses(self) -> None:
        c = reading_axis_census(3)
        self.assertEqual(c["readings"], 16)
        self.assertEqual(c["complement_classes"], 8)
        self.assertEqual(c["induced_separation_behaviours"], 4)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
