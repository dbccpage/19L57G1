"""Unit coverage of the kernel's refusals, renderings and edge paths.

Every branch here is a refusal or a rendering that the population-scale tests
never reach: an ill-formed admission, a serialization corner, a JSON shape.
They are cheap and they are the difference between a suite that exercises the
happy path and one that exercises the code.
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
    control_family_functions,
    family_novel,
    family_stable,
    limf_control,
    population,
)
from code.demands import (  # noqa: E402
    COMBINATIONS,
    DEMANDS_BY_NAME,
    Situation,
    combination_values,
    limf_family_verdict,
    limg_growth,
    obs1_existence,
    obs2_sub_reader,
    obs3_rival,
    obs4_coexistence,
    obs5_derivability,
    reader_relations,
    renaming_of_each_other,
    selection_is_fixed,
    strict_split_chain_length,
)
from code.enumerate_space import (  # noqa: E402
    DEFAULT_BOUNDS,
    Bounds,
    admissible_shape,
    inert_context,
    iter_candidates,
    iter_sealed_items,
    reader_suffixes,
    sealed_prefixes,
    superset_prefixes,
)
from code.grammar import (  # noqa: E402
    collapsed_pairs,
    contexts,
    coverage_bit,
    data_pairs,
    plug,
    profile,
    sealed_derivable,
    sealed_relation,
    slot_tuples,
)
from code.items import (  # noqa: E402
    AddContext,
    NewDatum,
    NewForm,
    NewInst,
    NewReader,
    NewRuleAll,
    StatedState,
    apply_delta,
    canonical_delta,
    capabilities,
    delta_json,
    is_sealed_item,
    item_json,
    item_key,
    mu1,
    mu2,
    project,
    sealed_events,
)
from code.price import (  # noqa: E402
    Minimum,
    ResponseClass,
    price,
    price_many,
    satisfies_at,
)
from code.quotient import (  # noqa: E402
    canonical_regime,
    canonical_state,
    designated_pair,
    flatten_context,
    group_by_key,
    pair_orbits,
    serialize_reader,
    serialize_regime,
    transport_context,
)
from code.readers import (  # noqa: E402
    ADMISSION_ONLY_READING,
    BLIND,
    EITHER,
    Reader,
    SEALED_READING,
    UNCOVERED,
    all_aggregations,
    all_reading_classes,
    behaviour,
    complement,
    full_selection_reader,
    induced_blocks,
    induced_relation,
    iter_readers,
    lawful,
    lawful_aggregations,
    monotone_aggregations,
    reading_class,
    reads_at,
    sealed_as_reader,
    separates,
    separating_count,
    signature,
    state_lawful,
    unlawful_aggregations,
)
from code.regime import (  # noqa: E402
    EMPTY,
    AdmissionRefused,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    Regime,
    Supply,
    genesis,
    replay,
    step,
)

TINY = Bounds(
    max_items=3, max_sealed_items=2, max_reader_items=1,
    max_arity=1, w_max=3, max_readers=2,
)


def ruled_state() -> Regime:
    return apply_delta(
        StatedState(genesis("L"), ()),
        (NewForm(1), NewRuleAll(0), NewInst(0, (0,))), 3, 2,
    ).regime


class EventRefusals(unittest.TestCase):
    def test_supply_does_not_change_the_state(self) -> None:
        r = genesis("L")
        self.assertEqual(step(r, Supply("<z>")), r)

    def test_re_admitting_a_token_designates_rather_than_duplicates(
        self,
    ) -> None:
        r = genesis("L")
        self.assertEqual(step(r, AdmitDatum("<a>")), r)

    def test_a_zero_arity_form_is_refused(self) -> None:
        with self.assertRaises(AdmissionRefused):
            step(EMPTY, AdmitForm(0))

    def test_an_instance_on_an_unknown_form_is_refused(self) -> None:
        with self.assertRaises(AdmissionRefused):
            step(genesis("L"), AdmitInst(0, (0,)))

    def test_an_instance_of_the_wrong_arity_is_refused(self) -> None:
        r = step(genesis("L"), AdmitForm(2))
        with self.assertRaises(AdmissionRefused):
            step(r, AdmitInst(0, (0,)))

    def test_an_instance_naming_an_unadmitted_datum_is_refused(self) -> None:
        r = step(genesis("L"), AdmitForm(1))
        with self.assertRaises(AdmissionRefused):
            step(r, AdmitInst(0, (9,)))

    def test_a_rule_on_an_unknown_form_is_refused(self) -> None:
        with self.assertRaises(AdmissionRefused):
            step(genesis("L"), AdmitRuleAll(3))

    def test_a_requirement_out_of_range_is_refused(self) -> None:
        with self.assertRaises(AdmissionRefused):
            step(genesis("L"), Impose(0, 5))
        with self.assertRaises(AdmissionRefused):
            step(genesis("L"), Impose(1, 0))

    def test_an_unknown_reading_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            genesis("Z")

    def test_replay_from_a_base(self) -> None:
        r = replay((AdmitForm(1),), genesis("L"))
        self.assertEqual(r.forms, (1,))


class GrammarUnits(unittest.TestCase):
    def test_slot_tuples_enumerate_holes_first(self) -> None:
        self.assertEqual(
            list(slot_tuples(1, 2)), [(None,), (0,), (1,)]
        )

    def test_profile_of_a_datum(self) -> None:
        r = ruled_state()
        self.assertEqual(profile(r, 0), frozenset(contexts(r)))

    def test_derivable_by_coverage_alone(self) -> None:
        r = ruled_state()
        self.assertTrue(sealed_derivable(r, (0, (1,))))
        self.assertTrue(coverage_bit(r, contexts(r)[0]))

    def test_plug_fills_every_hole(self) -> None:
        self.assertEqual(plug((0, (None, 1)), 7), (0, (7, 1)))

    def test_data_pairs_and_collapsed_pairs(self) -> None:
        self.assertEqual(data_pairs(3), ((0, 1), (0, 2), (1, 2)))
        self.assertEqual(collapsed_pairs(ruled_state()), ((0, 1),))


class ItemUnits(unittest.TestCase):
    def test_item_key_orders_every_kind(self) -> None:
        items = [
            AddContext(0, (0, (None,))),
            NewReader(SEALED_READING, (False, True, True, True)),
            NewInst(0, (0,)),
            NewRuleAll(0),
            NewForm(1),
            NewDatum(),
        ]
        ordered = canonical_delta(tuple(items))
        self.assertEqual(
            [type(i).__name__ for i in ordered],
            ["NewDatum", "NewForm", "NewRuleAll", "NewInst", "NewReader",
             "AddContext"],
        )
        self.assertEqual(item_key(NewDatum())[0], 0)

    def test_is_sealed_item(self) -> None:
        self.assertTrue(is_sealed_item(NewDatum()))
        self.assertFalse(
            is_sealed_item(NewReader(SEALED_READING, (False, True)))
        )

    def test_sealed_events_number_fresh_data_by_position(self) -> None:
        evs = sealed_events(genesis("L"), (NewDatum(), NewDatum()))
        self.assertEqual([e.token for e in evs], ["w2", "w3"])  # type: ignore[union-attr]

    def test_project_returns_the_regime(self) -> None:
        s = StatedState(genesis("L"), ())
        self.assertIs(project(s), s.regime)

    def test_add_context_refusals(self) -> None:
        r = ruled_state()
        c = contexts(r)[0]
        reader = NewReader(ADMISSION_ONLY_READING, (False, True, True, True))
        with self.assertRaises(AdmissionRefused):
            apply_delta(StatedState(r, ()), (AddContext(0, c),), 3, 2)
        with self.assertRaises(AdmissionRefused):
            apply_delta(
                StatedState(r, ()),
                (reader, AddContext(0, (9, (None,)))), 3, 2,
            )
        with self.assertRaises(AdmissionRefused):
            apply_delta(
                StatedState(r, ()),
                (reader, AddContext(0, c), AddContext(0, c)), 3, 2,
            )

    def test_every_item_renders_to_json(self) -> None:
        delta = (
            NewDatum(), NewForm(1), NewRuleAll(0), NewInst(0, (0,)),
            NewReader(SEALED_READING, (False, True, True, True)),
            AddContext(0, (0, (None, 1))),
        )
        rendered = delta_json(delta)
        self.assertEqual(len(rendered), 6)
        kinds = [d["kind"] for d in rendered]
        self.assertEqual(
            kinds,
            ["datum", "form", "rule", "inst", "reader", "add_context"],
        )
        self.assertEqual(
            item_json(AddContext(1, (0, (None, 2))))["context"],
            [0, [-1, 2]],
        )

    def test_capabilities_counts_every_kind(self) -> None:
        caps = capabilities(
            (NewDatum(), NewForm(2), NewRuleAll(0), NewInst(0, (0, 0)),
             NewReader(SEALED_READING, (False, True)),
             AddContext(0, (0, (None, None))))
        )
        self.assertEqual(caps["new_data"], 1)
        self.assertEqual(caps["new_form_arity_sum"], 2)
        self.assertEqual(caps["new_readers"], 1)
        self.assertEqual(caps["new_reader_contexts"], 1)

    def test_the_measures_on_a_mixed_delta(self) -> None:
        delta = (NewForm(2), NewReader(SEALED_READING, (False, True)))
        self.assertEqual(mu1(delta), 2)
        self.assertEqual(mu2(delta), (2, 2))


class ReaderUnits(unittest.TestCase):
    def test_complement_and_reading_class(self) -> None:
        self.assertEqual(
            complement(SEALED_READING), (True, False, False, False)
        )
        self.assertEqual(
            reading_class(SEALED_READING),
            reading_class(complement(SEALED_READING)),
        )

    def test_behaviour_names_of_the_two_named_readings(self) -> None:
        self.assertEqual(behaviour(SEALED_READING), UNCOVERED)
        self.assertEqual(behaviour(ADMISSION_ONLY_READING), EITHER)
        self.assertEqual(behaviour((False, False, False, False)), BLIND)
        self.assertTrue(reads_at(ADMISSION_ONLY_READING, True))

    def test_aggregation_counts(self) -> None:
        self.assertEqual(len(all_aggregations(3)), 8)
        self.assertEqual(len(lawful_aggregations(3)), 4)
        self.assertEqual(len(unlawful_aggregations(3)), 4)
        self.assertEqual(len(monotone_aggregations(3)), 2)
        self.assertFalse(lawful((False, False, True, False), 3))

    def test_separating_count_and_separates(self) -> None:
        r = ruled_state()
        rho = Reader(
            contexts(r)[:1], ADMISSION_ONLY_READING,
            (False, True, True, True),
        )
        self.assertEqual(separating_count(r, rho, 0, 1), 1)
        self.assertTrue(separates(r, rho, 0, 1))
        self.assertEqual(signature(r, rho, 0), (True,))

    def test_a_count_beyond_the_aggregation_width_is_refused(self) -> None:
        r = ruled_state()
        rho = Reader(contexts(r)[:1], ADMISSION_ONLY_READING, (False,))
        with self.assertRaises(ValueError):
            separates(r, rho, 0, 1)

    def test_blocks_of_a_blind_reader(self) -> None:
        r = ruled_state()
        rho = Reader((), SEALED_READING, (False, True, True, True))
        self.assertEqual(induced_blocks(r, rho), 1)
        self.assertEqual(induced_relation(r, rho), frozenset())

    def test_state_lawful_on_a_small_carrier(self) -> None:
        r = ruled_state()
        rho = Reader(
            contexts(r)[:1], ADMISSION_ONLY_READING,
            (False, True, True, True),
        )
        self.assertTrue(state_lawful(r, rho))

    def test_full_selection_reader_and_sealed_as_reader(self) -> None:
        r = ruled_state()
        full = full_selection_reader(r, SEALED_READING, 1)
        self.assertEqual(full.selection, contexts(r))
        self.assertEqual(
            induced_relation(r, sealed_as_reader(r)), sealed_relation(r)
        )

    def test_iter_readers_respects_the_width_bound(self) -> None:
        r = ruled_state()
        self.assertEqual(list(iter_readers(r, 4, 3)), [])
        got = list(iter_readers(r, 1, 3))
        self.assertTrue(got)
        for rho in got:
            self.assertEqual(rho.width(), 1)
            self.assertIn(rho.aggregation, lawful_aggregations(3))
        unrestricted = list(iter_readers(r, 0, 3, lawful_only=False))
        self.assertGreater(len(unrestricted), 0)


class QuotientUnits(unittest.TestCase):
    def test_flatten_and_transport(self) -> None:
        self.assertEqual(flatten_context((0, (None, 1))), (0, (-1, 1)))
        self.assertEqual(
            transport_context((0, (None, 1)), (1, 0), (0,)), (0, (None, 0))
        )

    def test_serialize_regime_carries_requirements(self) -> None:
        r = step(genesis("L"), Impose(0, 1))
        key = serialize_regime(r, (0, 1), ())
        self.assertIn((0, 1), key[4])

    def test_serialize_reader_uses_the_complement_class(self) -> None:
        r = ruled_state()
        rho = Reader(
            contexts(r)[:1], ADMISSION_ONLY_READING,
            (False, True, True, True),
        )
        other = Reader(
            contexts(r)[:1], complement(ADMISSION_ONLY_READING),
            (False, True, True, True),
        )
        self.assertEqual(
            serialize_reader(rho, (0, 1), (0,)),
            serialize_reader(other, (0, 1), (0,)),
        )

    def test_pair_orbits_and_designated_pair(self) -> None:
        r = genesis("F")
        pairs = collapsed_pairs(r)
        orbits = pair_orbits(r, pairs)
        self.assertTrue(orbits)
        self.assertEqual(designated_pair(r, pairs), orbits[0][0])
        self.assertIsNone(designated_pair(r, ()))

    def test_group_by_key(self) -> None:
        a = StatedState(genesis("L"), ())
        grouped = group_by_key([(a, "x"), (a, "y")])
        self.assertEqual(list(grouped.values()), [["x", "y"]])

    def test_canonical_state_of_a_reader_bearing_state(self) -> None:
        r = ruled_state()
        rho = Reader(
            contexts(r)[:1], ADMISSION_ONLY_READING,
            (False, True, True, True),
        )
        k1 = canonical_state(StatedState(r, (rho,)))
        k2 = canonical_state(StatedState(r, ()))
        self.assertNotEqual(k1, k2)
        self.assertEqual(canonical_regime(r), canonical_regime(r))


class EnumerationUnits(unittest.TestCase):
    def test_admissible_shape_refuses_a_doubled_rule(self) -> None:
        base = genesis("L")
        self.assertFalse(
            admissible_shape(
                base, (NewForm(1), NewRuleAll(0), NewRuleAll(0))
            )
        )
        self.assertTrue(admissible_shape(base, (NewForm(1), NewRuleAll(0))))
        ruled = ruled_state()
        self.assertFalse(admissible_shape(ruled, (NewRuleAll(0),)))

    def test_inert_context_both_ways(self) -> None:
        r = ruled_state()
        c = contexts(r)[0]
        blind = (False, False, False, False)
        self.assertTrue(inert_context(r, blind, c))
        self.assertFalse(inert_context(r, ADMISSION_ONLY_READING, c))

    def test_zero_item_suffix_and_prefix(self) -> None:
        r = ruled_state()
        self.assertEqual(list(reader_suffixes(r, 0, DEFAULT_BOUNDS)), [()])
        self.assertEqual(
            list(reader_suffixes(r, 9, DEFAULT_BOUNDS)), []
        )
        self.assertEqual(
            list(sealed_prefixes(genesis("L"), 0, DEFAULT_BOUNDS)), [()]
        )

    def test_superset_at_zero_and_one(self) -> None:
        base = genesis("L")
        self.assertEqual(
            set(superset_prefixes(base, 0, TINY)),
            set(sealed_prefixes(base, 0, TINY)),
        )
        self.assertEqual(
            set(superset_prefixes(base, 1, TINY)),
            set(sealed_prefixes(base, 1, TINY)),
        )

    def test_one_item_alphabet_offers_no_rule_for_a_ruled_form(self) -> None:
        r = ruled_state()
        self.assertFalse(
            any(
                isinstance(i, NewRuleAll)
                for i in iter_sealed_items(r, DEFAULT_BOUNDS)
            )
        )

    def test_candidates_at_zero_items(self) -> None:
        got = list(iter_candidates(genesis("L"), 0, DEFAULT_BOUNDS))
        self.assertEqual(len(got), 1)
        self.assertEqual(got[0][0], ())


class DemandUnits(unittest.TestCase):
    def _sit(self, readers):  # type: ignore[no-untyped-def]
        r = ruled_state()
        return Situation(r, (), StatedState(r, tuple(readers)), (0, 1), 3)

    def test_no_reader_answers_nothing(self) -> None:
        sit = self._sit([])
        self.assertFalse(obs1_existence(sit))
        self.assertFalse(obs2_sub_reader(sit))
        self.assertFalse(obs3_rival(sit))
        self.assertFalse(obs4_coexistence(sit))
        self.assertFalse(obs5_derivability(sit))
        self.assertEqual(reader_relations(sit), [])

    def test_obs4_needs_a_designated_pair(self) -> None:
        r = ruled_state()
        rho = Reader(
            contexts(r)[:1], ADMISSION_ONLY_READING,
            (False, True, True, True),
        )
        self.assertFalse(
            obs4_coexistence(
                Situation(r, (), StatedState(r, (rho, rho)), None, 3)
            )
        )

    def test_obs4_needs_disagreement_at_the_designated_pair(self) -> None:
        r = ruled_state()
        rho = Reader(
            contexts(r)[:1], ADMISSION_ONLY_READING,
            (False, True, True, True),
        )
        self.assertFalse(obs4_coexistence(self._sit([rho, rho])))

    def test_renaming_of_readers_with_different_widths(self) -> None:
        r = ruled_state()
        a = Reader(contexts(r)[:1], ADMISSION_ONLY_READING,
                   (False, True, True, True))
        b = Reader((), ADMISSION_ONLY_READING, (False, True, True, True))
        self.assertFalse(renaming_of_each_other(r, a, b))

    def test_the_combination_set_is_declared_and_total(self) -> None:
        universe = frozenset({(0, 1)})
        sealed = frozenset()
        alone = combination_values(universe, sealed, None)
        self.assertEqual(set(alone), {"identity", "complement"})
        both = combination_values(universe, sealed, frozenset({(0, 1)}))
        self.assertEqual(set(both), set(COMBINATIONS))

    def test_obs5_reports_admitted_when_outside_the_set(self) -> None:
        """A three-datum state where the reader's relation is neither the
        sealed relation nor its complement."""
        base = genesis("F")
        r = apply_delta(
            StatedState(base, ()),
            (NewForm(1), NewRuleAll(0), NewInst(0, (0,))), 3, 2,
        ).regime
        rho = Reader(
            contexts(r)[:1], ADMISSION_ONLY_READING,
            (False, True, True, True),
        )
        sit = Situation(r, (), StatedState(r, (rho,)), (0, 1), 3)
        rel = induced_relation(r, rho)
        universe = frozenset(data_pairs(r.n_data()))
        expected = rel in set(
            combination_values(universe, sealed_relation(r), None).values()
        )
        self.assertEqual(obs5_derivability(sit), expected)

    def test_selection_is_fixed_rejects_a_foreign_item(self) -> None:
        class Foreign:
            pass

        self.assertFalse(selection_is_fixed((Foreign(),)))  # type: ignore[arg-type]

    def test_limg_needs_a_carrier_above_the_threshold(self) -> None:
        self.assertFalse(limg_growth(self._sit([])))

    def test_limf_is_false_on_a_well_formed_delta(self) -> None:
        r = ruled_state()
        sit = Situation(
            r, (NewForm(1),), StatedState(r, ()), (0, 1), 3
        )
        self.assertFalse(limf_family_verdict(sit))

    def test_chain_length_of_an_empty_selection(self) -> None:
        r = ruled_state()
        rho = Reader((), ADMISSION_ONLY_READING, (False, True, True, True))
        self.assertEqual(strict_split_chain_length(r, rho), 0)


class CensusUnits(unittest.TestCase):
    def test_capacity_census_skips_a_one_datum_state(self) -> None:
        c = capacity_census(1, DEFAULT_BOUNDS)
        self.assertGreater(c["states_considered"], 0)  # type: ignore[arg-type]

    def test_chain_census_at_depth_one(self) -> None:
        c = chain_census(1, DEFAULT_BOUNDS)
        self.assertEqual(c["chains_above_the_ceiling"], 0)

    def test_family_control_functions(self) -> None:
        self.assertEqual(len(control_family_functions()), 3)
        # Novelty over an EMPTY verdict sequence is vacuously true: there is
        # no stage verdict to differ from.  Recorded rather than hidden — it
        # is why LIM-F's positive control is evaluated on a non-empty
        # sequence, and why an empty run would prove nothing.
        self.assertTrue(
            family_novel((), control_family_functions()["not the first verdict"])
        )
        self.assertFalse(
            family_novel(
                (True,), control_family_functions()["not the last verdict"]
            )
            is None
        )
        self.assertTrue(
            family_stable(
                (False,) * 4, 2,
                control_family_functions()["no verdict was true"],
            )
        )
        self.assertEqual(len(limf_control((False,) * 4, 2)), 3)

    def test_population_at_depth_zero_is_the_two_bases(self) -> None:
        self.assertEqual(len(population(0, DEFAULT_BOUNDS)), 2)


class PriceUnits(unittest.TestCase):
    def test_an_empty_minimum_grades_empty(self) -> None:
        m = price(
            genesis("L"), "L", DEMANDS_BY_NAME["LIM-R"], "mu1", TINY
        )
        self.assertEqual(m.grade, "Empty")
        self.assertEqual(m.cost, (-1, -1))
        self.assertEqual(m.distinct_induced_relations, 0)

    def test_price_many_with_no_demands(self) -> None:
        self.assertEqual(
            price_many(genesis("L"), "L", (), ("mu1",), TINY), {}
        )

    def test_satisfies_at_on_a_reader_bearing_delta(self) -> None:
        base = genesis("L")
        delta = canonical_delta(
            (NewForm(1), NewRuleAll(0), NewInst(0, (0,)),
             NewReader(ADMISSION_ONLY_READING, (False, True, True, True)),
             AddContext(0, (0, (None,))))
        )
        self.assertTrue(
            satisfies_at(
                base, delta, DEMANDS_BY_NAME["OBS-3"], DEFAULT_BOUNDS
            )
        )

    def test_a_response_class_records_its_capabilities(self) -> None:
        d = (NewForm(1),)
        c = ResponseClass(("k",), d, (d,), capabilities(d))
        self.assertEqual(c.capability_vector["new_forms"], 1)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
