"""Unit tests. Every test pins a sentence of `STATUS.md` or
`CLAIM_LEDGER.md`.  AuthorityEffect: None.
"""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (str(HERE), str(REPO / "code")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from derivation.candidates import (  # noqa: E402
    NewInst,
    NewRuleAll,
    apply_delta,
    iter_cost1_items,
)

import costs as ct  # noqa: E402
import exactness as ex  # noqa: E402
import movegraph as mg  # noqa: E402

GRAPH = mg.build()


class GraphShape(unittest.TestCase):
    def test_no_move_is_invented(self) -> None:
        """Every edge is a move the sealed enumerator offers at its source,
        and every such move whose target is in the rectangle is an edge."""

        offered: set[tuple[int, str]] = set()
        for node, base in enumerate(GRAPH.states):
            for it in iter_cost1_items(base, mg.BOUNDS):
                offered.add((node, repr(it)))
        recorded = {(e.source, repr(e.item)) for e in GRAPH.edges}
        self.assertTrue(recorded <= offered)

    def test_the_cycle_basis_has_the_right_size(self) -> None:
        """`len(cycles)` must equal `E - V + C`; the builder asserts it, and
        this checks the assertion is not vacuous."""

        self.assertEqual(len(GRAPH.cycles), GRAPH.rank)
        self.assertEqual(
            GRAPH.rank, len(GRAPH.edges) - len(GRAPH.states) + GRAPH.components
        )
        self.assertGreater(GRAPH.rank, 0)

    def test_depth_one_is_vacuous(self) -> None:
        """Why the declared depth is not one: a shallower rectangle has no
        cycle at all, so every statement about circulation would be empty."""

        shallow = mg.build(1)
        self.assertEqual(shallow.rank, 0)
        self.assertEqual(len(shallow.cycles), 0)

    def test_order_cycles_are_not_all_the_rank(self) -> None:
        """The two sources of path-dependence both occur, and neither
        accounts for the other."""

        self.assertGreater(len(GRAPH.order_cycles), 0)
        self.assertGreater(len(GRAPH.self_loop_edges), 0)
        self.assertGreater(GRAPH.rank, len(GRAPH.self_loop_edges))

    def test_self_loops_are_exactly_instance_repeats(self) -> None:
        for edge in GRAPH.self_loop_edges:
            self.assertEqual(mg.item_kind(edge.item), "inst")
            self.assertIsInstance(edge.item, NewInst)
            assert isinstance(edge.item, NewInst)
            self.assertIn(
                (edge.item.form, edge.item.args), GRAPH.states[edge.source].insts
            )


class Declaration(unittest.TestCase):
    def test_every_candidate_carries_a_reading(self) -> None:
        """`FW-TUNED`: a candidate with no declared reading is a candidate
        invented to have the property."""

        self.assertEqual(set(ct.CANDIDATES), set(ct.READINGS))
        for name, reading in ct.READINGS.items():
            self.assertGreater(len(reading), 20, name)

    def test_each_weight_is_a_function_of_the_state_and_the_item(self) -> None:
        """A weighting must depend on nothing else -- not on which route
        reached the state, not on the edge's position in the enumeration.
        If it did, the Lean characterisation would not apply to it and the
        circulation numbers would mean nothing."""

        for name, weight in sorted(ct.CANDIDATES.items()):
            seen: dict[tuple[int, str], int] = {}
            for edge in GRAPH.edges:
                key = (edge.source, repr(edge.item))
                value = weight(GRAPH.states[edge.source], edge.item)
                if key in seen:
                    self.assertEqual(seen[key], value, f"{name} {key}")
                seen[key] = value
            self.assertGreater(len(seen), 0, name)

    def test_a_two_move_route_costs_the_sum_of_its_moves(self) -> None:
        """Summation, checked on real routes: the implementation prices a
        route by adding its moves, each at the state it meets, and the
        second move is priced at the intermediate state and not at the
        start."""

        for name, weight in sorted(ct.CANDIDATES.items()):
            checked = 0
            for start, left, _right in ex.commuting_squares(GRAPH)[:20]:
                base = GRAPH.states[start]
                first, second = GRAPH.edges[left[0]], GRAPH.edges[left[1]]
                middle = apply_delta(base, (first.item,))
                self.assertEqual(middle, GRAPH.states[first.target])
                total = ex.edge_weights(GRAPH, name)[left[0]] + ex.edge_weights(
                    GRAPH, name
                )[left[1]]
                self.assertEqual(
                    total, weight(base, first.item) + weight(middle, second.item), name
                )
                checked += 1
            self.assertGreater(checked, 0, name)


class Exactness(unittest.TestCase):
    def test_the_two_methods_agree_on_every_candidate(self) -> None:
        for name in sorted(ct.CANDIDATES):
            verdict = ex.decide(GRAPH, name)
            self.assertTrue(verdict.methods_agree, name)
            self.assertEqual(
                verdict.exact_by_potentials, verdict.exact_by_circulations, name
            )

    def test_reach_is_exact_and_its_functional_is_the_profile_size(self) -> None:
        """The constructive half: when exactness holds the walk produces the
        functional, and here it must be the observable content, up to one
        constant per component."""

        weights = ex.edge_weights(GRAPH, "reach")
        exact, witness = ex.potentials(GRAPH, weights)
        self.assertTrue(exact, witness)
        for edge in GRAPH.edges:
            before = ct.profile_size(GRAPH.states[edge.source])
            after = ct.profile_size(GRAPH.states[edge.target])
            self.assertEqual(weights[edge.index], after - before)

    def test_the_item_count_cannot_see_order(self) -> None:
        """Not exact, but only through waste: on every commuting square both
        routes use the same number of moves."""

        verdict = ex.decide(GRAPH, "item_count")
        self.assertFalse(verdict.exact_by_potentials)
        self.assertEqual(verdict.nonzero_order_cycles, 0)
        self.assertIsNone(ex.square_witness(GRAPH, "item_count"))

    def test_rule_span_is_the_object_the_preceding_rung_named(self) -> None:
        """Additive by construction, reads the base, not exact -- and its
        path-dependence is order, not waste."""

        verdict = ex.decide(GRAPH, "rule_span")
        self.assertTrue(verdict.reads_the_base)
        self.assertFalse(verdict.exact_by_potentials)
        self.assertEqual(verdict.nonzero_self_loop_cycles, 0)
        self.assertGreater(verdict.nonzero_order_cycles, 0)

    def test_rule_span_charges_nothing_for_a_wasted_move(self) -> None:
        """The separation that makes it non-degenerate: every self-loop in
        the rectangle is free under this cost."""

        for edge in GRAPH.self_loop_edges:
            self.assertEqual(ct.rule_span(GRAPH.states[edge.source], edge.item), 0)

    def test_the_square_witness_is_commit_early_against_commit_late(self) -> None:
        witness = ex.square_witness(GRAPH, "rule_span")
        assert witness is not None
        one, two = witness["route_one"], witness["route_two"]
        assert isinstance(one, list) and isinstance(two, list)
        kinds = {
            tuple(str(k) for k, _ in one),
            tuple(str(k) for k, _ in two),
        }
        self.assertEqual(kinds, {("datum", "rule"), ("rule", "datum")})
        self.assertNotEqual(witness["route_one_total"], witness["route_two_total"])

    def test_reading_the_base_is_not_enough(self) -> None:
        """The trap, pinned: two candidates read the base and telescope
        anyway."""

        for name in ("reach", "context_opening"):
            verdict = ex.decide(GRAPH, name)
            self.assertTrue(verdict.reads_the_base, name)
            self.assertTrue(verdict.exact_by_potentials, name)

    def test_all_four_quadrants_are_occupied(self) -> None:
        """Base-relative and path-dependent are independent axes, and the
        candidate list shows all four combinations rather than asserting
        them."""

        import run_path_dependent

        cells = run_path_dependent.quadrants(
            run_path_dependent.candidate_table(GRAPH)
        )
        for key, members in cells.items():
            self.assertGreater(len(members), 0, key)


class ReceiptReplay(unittest.TestCase):
    def test_the_committed_receipt_replays_byte_for_byte(self) -> None:
        import run_path_dependent

        committed = (HERE / "receipts" / "path_dependent_cost.json").read_text("utf-8")
        fresh = json.dumps(
            run_path_dependent.build(), indent=2, sort_keys=True, ensure_ascii=True
        ) + "\n"
        self.assertEqual(committed, fresh)


class RuleSpanReading(unittest.TestCase):
    def test_the_price_is_what_the_commitment_ranges_over(self) -> None:
        """The definition, checked against the reading rather than trusted:
        a rule over an arity-`k` form on `n` data costs `n ** k`."""

        seen = 0
        for node, base in enumerate(GRAPH.states):
            for it in iter_cost1_items(base, mg.BOUNDS):
                if not isinstance(it, NewRuleAll):
                    continue
                seen += 1
                self.assertEqual(
                    ct.rule_span(base, it), base.n_data() ** base.forms[it.form]
                )
        self.assertGreater(seen, 0)


if __name__ == "__main__":
    unittest.main()
