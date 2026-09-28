"""Tests of the runs, the census readings and the runner of continuation two.

Every reading is shown to give each of its outcomes on a run that should
give it, and every guard is shown to fire by name on the defect it
exists to catch: a replay that does not replay, a merge whose labels
disagree, a merge the budget leaves unchecked, a node the key procedure
cannot key, a receipt carrying an environment value, a receipt that
drifted.  The full class is too slow to build under coverage, so the
runner is exercised on named subsets; the committed receipts are
checked against the full class by `run_forward.py --check`, which the
workflow runs outside coverage.
"""

from __future__ import annotations

import copy
import gzip
import json
import pathlib
import sys
import tempfile
import unittest
from typing import Any, Optional
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import fwd_runs as fr  # noqa: E402

# `fwd_runs` puts sibling trees on the path and each of them carries its
# own `verify_pins`, `check_coverage` and `test_*`; this tree goes back to
# the front first.  See the note in `fwd_runs.py`.
if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))

import fwd_census as fc  # noqa: E402
import run_forward as rf  # noqa: E402
from engine_decl import EState, SwitchMarker, engine_named  # noqa: E402
from observables import ObservableGuardError  # noqa: E402
from derivation.iso import IsoBudgetError  # noqa: E402
from derivation.model import EMPTY, AdmitInst, Regime  # noqa: E402

L, F = fr.run_readings()
RECEIPTS = HERE / "receipts"

_CACHE: dict[tuple[str, str], fr.Run] = {}


def run_of(name: str, reading: str = "L", **bounds: int) -> fr.Run:
    key = (name, reading + repr(sorted(bounds.items())))
    if key not in _CACHE:
        _CACHE[key] = fr.build_run(engine_named(name), L if reading == "L" else F, **bounds)
    return _CACHE[key]


def synthetic(edges: list[tuple[int, int, str, bool, bool]], terminals: dict[int, str], n: int) -> fr.Run:
    """A run graph with dummy states, for the readings' edge cases: each
    edge is (parent, child, kind, changing, datum_round)."""
    run = fr.Run(engine_named("E1/mu1/V1/halt"), "L")
    state = EState(EMPTY, "plain")
    for index in range(n):
        node = fr.Node(index, 0, (), state, (("k", index), "plain"), ())
        node.terminal = terminals.get(index, "")
        node.expanded = node.terminal == ""
        run.nodes.append(node)
    for parent, child, kind, changing, datum in edges:
        run.edges.append(
            fr.Edge(parent, child, kind, "", None, (), (), (), EMPTY, False, changing, datum, False, ())
        )
    return run


# ---------------------------------------------------------------------------
# The runs
# ---------------------------------------------------------------------------


class RunShapeTests(unittest.TestCase):
    def test_the_deep_run_of_e4_under_mu2_at_l(self) -> None:
        run = run_of("E4/mu2/V1/halt")
        terminals = {k: sum(1 for n in run.nodes if n.terminal == k) for k in fr.TERMINALS}
        self.assertEqual((len(run.nodes), len(run.edges)), (23, 30))
        self.assertEqual(terminals, {"FIXPOINT": 7, "REFUSAL": 0, "BOUND": 1, "GUARD": 0})
        self.assertEqual(fr.closure_kind(run), "NOT_CLOSED")
        self.assertTrue(fr.carries_forward(run))
        self.assertEqual(fr.replay_mismatches(run), [])
        self.assertEqual(run.quotient_defects, [])
        self.assertEqual(max(node.stage for node in run.nodes), fr.ROUND_BOUND)

    def test_a_halting_quiet_engine_is_one_fixpoint(self) -> None:
        run = run_of("E1/mu1/V1/halt")
        self.assertEqual(len(run.nodes), 1)
        self.assertEqual(run.nodes[0].terminal, fr.FIXPOINT)
        self.assertEqual(fr.closure_kind(run), "TERMINATES")
        self.assertFalse(fr.carries_forward(run))

    def test_a_quiet_engine_with_both_rules_cycles(self) -> None:
        run = run_of("E7/mu1/V1/growth+switch")
        self.assertEqual((len(run.nodes), len(run.edges)), (6, 10))
        self.assertEqual(fr.closure_kind(run), "CYCLES")
        self.assertTrue(all(run.edges[i].kind == "switch" for i in fr.cyclic_edges(run)))

    def test_growth_stops_at_four_data(self) -> None:
        run = run_of("E8/mu1/V1/growth", "F")
        self.assertEqual([n.state.regime.n_data() for n in run.nodes], [3, 4])
        self.assertEqual(run.nodes[-1].terminal, fr.FIXPOINT)

    def test_the_round_bound_and_the_node_guard_bite(self) -> None:
        bounded = run_of("E4/mu2/V1/halt", round_bound=2)
        self.assertTrue(any(n.terminal == fr.BOUND and n.stage == 2 for n in bounded.nodes))
        guarded = run_of("E4/mu1/V1/halt", node_guard=5)
        self.assertTrue(any(n.terminal == fr.GUARD for n in guarded.nodes))
        self.assertFalse(fr.is_closed(guarded))
        self.assertEqual(
            len(fr.frontier(guarded)),
            sum(1 for n in guarded.nodes if n.terminal in (fr.BOUND, fr.GUARD)),
        )

    def test_a_frontier_reached_through_a_switch_does_not_carry_forward(self) -> None:
        run = run_of("E1/mu2/V1/switch", round_bound=3)
        self.assertFalse(fr.is_closed(run))
        self.assertFalse(fr.carries_forward(run))

    def test_a_response_carries_its_moves(self) -> None:
        run = run_of("E4/mu2/V1/halt", "F", round_bound=1)
        responses = [e for e in run.edges if e.kind == "response"]
        self.assertTrue(responses)
        self.assertTrue(all(len(e.moved) == 2 for e in responses))
        self.assertTrue(all(e.changing and not e.datum_round for e in responses))

    def test_the_element_count(self) -> None:
        self.assertEqual(fr.elements(EMPTY), 0)
        regime = run_of("E4/mu2/V1/halt").nodes[1].state.regime
        self.assertEqual(fr.elements(regime), 2 + 1 + 1)

    def test_all_runs_over_a_named_subset(self) -> None:
        runs = fr.all_runs([engine_named("E8/mu1/V1/halt")])
        self.assertEqual(sorted(runs), [("E8/mu1/V1/halt", "F"), ("E8/mu1/V1/halt", "L")])


class GuardTests(unittest.TestCase):
    """Every guard of the run builder fires by name."""

    def test_a_node_the_key_procedure_cannot_key_is_a_guard(self) -> None:
        real = fr.state_key

        def flaky(state: EState) -> Any:
            if state.regime.n_data() == 3:
                raise IsoBudgetError("probe budget")
            return real(state)

        with mock.patch.object(fr, "state_key", flaky):
            run = fr.build_run(engine_named("E8/mu1/V1/growth"), L)
        guarded = [n for n in run.nodes if n.budget_guard]
        self.assertEqual(len(guarded), 1)
        self.assertIn("key budget", guarded[0].budget_guard)
        self.assertEqual(guarded[0].terminal, fr.GUARD)
        self.assertIn(None, [v["demands"] for v in fr.node_values(run)])

    def test_an_observable_budget_is_a_guard(self) -> None:
        def refuse(rule_name: str, state: EState) -> Any:
            raise ObservableGuardError("probe observable budget")

        with mock.patch.object(fr, "state_demands", refuse):
            run = fr.build_run(engine_named("E4/mu1/V1/halt"), L)
        self.assertEqual(len(run.nodes), 1)
        self.assertEqual(run.nodes[0].terminal, fr.GUARD)
        self.assertIn("observable budget", run.nodes[0].budget_guard)

    def test_a_merge_whose_labels_disagree_is_a_named_defect(self) -> None:
        """NEGATIVE: the quotient check bites.  A label function that
        reads the regime's data tokens is not carried by the isomorphism,
        and every merge it sees is reported."""

        after = run_of("E4/mu2/V1/halt").edges[0].after
        renamed = Regime(("x", "y"), after.forms, after.insts, after.rules, after.reqs)

        def token_reader(rule: Any, regime: Regime, i: int, j: int) -> str:
            return "apart" if regime.data == after.data else "same"

        with mock.patch.object(fr, "label_of", token_reader):
            defects = fr._label_defects("E4", "plain", after, renamed)
        self.assertTrue(defects)
        self.assertIn("reads", defects[0])

    def test_a_merge_with_no_witness_is_named(self) -> None:
        defects = fr._label_defects(
            "E4", "plain", run_of("E4/mu2/V1/halt").edges[0].after, EMPTY
        )
        self.assertEqual(defects, ["no isomorphism witness for a merge"])

    def test_defects_found_at_a_merge_are_recorded_on_the_run(self) -> None:
        with mock.patch.object(fr, "_label_defects", lambda *a: ["probe defect"]):
            run = fr.build_run(engine_named("E4/mu2/V1/halt"), L, round_bound=2)
        self.assertTrue(run.quotient_defects)
        self.assertIn("probe defect", run.quotient_defects[0])

    def test_a_merge_the_budget_leaves_unchecked_is_recorded(self) -> None:
        def refuse(*args: Any) -> list[str]:
            raise ObservableGuardError("probe budget")

        with mock.patch.object(fr, "_label_defects", refuse):
            run = fr.build_run(engine_named("E4/mu2/V1/halt"), L, round_bound=2)
        self.assertTrue(run.unchecked_merges)
        self.assertEqual(run.quotient_defects, [])

    def test_a_refused_demand_is_a_refusal(self) -> None:
        with mock.patch.object(fr, "least_responses", lambda *a, **k: None):
            run = fr.build_run(engine_named("E4/mu1/V1/halt"), L)
        self.assertEqual(run.nodes[0].terminal, fr.REFUSAL)
        self.assertEqual(len(run.nodes[0].refused), 1)

    def test_the_refusal_shapes_are_counted(self) -> None:
        """A refused apart demand whose pair is held collapsed through a
        third datum is TRANSITIVE; any other is counted by its kind."""
        run = fr.build_run(engine_named("E4/mu1/V1/growth"), F)
        shapes = rf.refusal_shapes(run)
        self.assertGreater(shapes["apart_transitive"], 0)
        self.assertEqual(shapes["apart_other"], 0)
        forced = fr.build_run(engine_named("E4/mu1/V1/halt"), L, round_bound=1)
        forced.nodes[0].refused = (("apart", (0, 1)),)
        self.assertEqual(rf.refusal_shapes(forced), {"apart_transitive": 0, "apart_other": 1, "same": 0})
        forced.nodes[0].refused = (("same", (0, 1)),)
        self.assertEqual(rf.refusal_shapes(forced), {"apart_transitive": 0, "apart_other": 0, "same": 1})

    def test_replay_mismatches_are_named(self) -> None:
        """NEGATIVE: the replay check bites on a node, an edge's regime,
        and an edge's child."""
        def fresh() -> fr.Run:
            return fr.build_run(engine_named("E4/mu2/V1/halt"), L, round_bound=2)

        run = fresh()
        run.nodes[1].history = run.nodes[0].history
        found = fr.replay_mismatches(run)
        self.assertTrue(any("node 1" in line for line in found))
        self.assertTrue(any("does not replay" in line for line in found))
        run = fresh()
        run.nodes[1].history = run.nodes[1].history + (AdmitInst(9, (0,)),)
        self.assertTrue(any("node 1 does not replay" in line for line in fr.replay_mismatches(run)))
        run = fresh()
        run.edges[1].after = EMPTY
        self.assertTrue(any("reaches another regime" in line for line in fr.replay_mismatches(run)))
        run = fresh()
        run.nodes[2].key = ("tampered", "plain")
        found = fr.replay_mismatches(run)
        self.assertTrue(any("does not reach its child node" in line for line in found))
        self.assertEqual(fr.replay_mismatches(fresh()), [])

    def test_a_key_budget_at_replay_is_a_mismatch(self) -> None:
        run = fr.build_run(engine_named("E4/mu2/V1/halt"), L, round_bound=1)

        def refuse(state: EState) -> Any:
            raise IsoBudgetError("probe")

        with mock.patch.object(fr, "state_key", refuse):
            found = fr.replay_mismatches(run)
        self.assertTrue(found)

    def test_an_automorphism_budget_leaves_no_value(self) -> None:
        def refuse(regime: Regime, budget: int) -> Any:
            raise IsoBudgetError("probe")

        with mock.patch.object(fr, "automorphisms", refuse):
            values = fr.node_values(run_of("E1/mu1/V1/halt"))
        self.assertIsNone(values[0]["symmetry"])


# ---------------------------------------------------------------------------
# The readings
# ---------------------------------------------------------------------------


class ReachesTests(unittest.TestCase):
    def test_holds_at_the_root(self) -> None:
        run = run_of("E1/mu1/V1/halt")
        self.assertEqual(fc.every_run_reaches(run, lambda v: True, lambda e: False).status, fc.HOLDS)

    def test_fails_at_a_fixpoint_with_its_path(self) -> None:
        run = run_of("E1/mu1/V1/halt")
        out = fc.every_run_reaches(run, lambda v: False, lambda e: False)
        self.assertEqual(out.status, fc.FAILS)
        self.assertEqual(out.witness, ((0,), fr.FIXPOINT))

    def test_fails_on_a_cycle(self) -> None:
        run = run_of("E7/mu1/V1/switch")
        out = fc.every_run_reaches(run, lambda v: False, lambda e: False)
        self.assertEqual(out.status, fc.FAILS)
        self.assertEqual(out.witness[1], "cycle")

    def test_undecided_when_every_avoiding_path_is_cut(self) -> None:
        run = run_of("E1/mu2/V1/switch", round_bound=4)
        out = fc.every_run_reaches(run, lambda v: False, lambda e: False)
        self.assertEqual(out.status, fc.UNDECIDED)

    def test_holds_through_an_edge(self) -> None:
        run = run_of("E4/mu2/V1/halt", "F", round_bound=2)
        out = fc.every_run_reaches(run, lambda v: False, lambda e: e.kind == "response")
        self.assertEqual(out.status, fc.HOLDS)

    def test_holds_when_every_successor_holds(self) -> None:
        run = synthetic([(0, 1, "switch", False, False), (0, 2, "switch", False, False)], {1: fr.FIXPOINT, 2: fr.FIXPOINT}, 3)
        out = fc.every_run_reaches(run, lambda v: v in (1, 2), lambda e: False)
        self.assertEqual(out.status, fc.HOLDS)


class ViolatesTests(unittest.TestCase):
    def test_fails_with_the_first_edge(self) -> None:
        run = run_of("E4/mu2/V1/halt", round_bound=3)
        out = fc.no_edge_violates(run, lambda i, e: i == 1)
        self.assertEqual(out.status, fc.FAILS)
        self.assertEqual(out.witness[1], 1)

    def test_holds_on_a_closed_run_and_at_bound_otherwise(self) -> None:
        self.assertEqual(fc.no_edge_violates(run_of("E7/mu1/V1/switch"), lambda i, e: False).status, fc.HOLDS)
        self.assertEqual(
            fc.no_edge_violates(run_of("E4/mu2/V1/halt"), lambda i, e: False).status, fc.HOLDS_AT_BOUND
        )

    def test_an_unreadable_edge_is_undecided(self) -> None:
        out = fc.no_edge_violates(run_of("E7/mu1/V1/switch"), lambda i, e: None)
        self.assertEqual(out.status, fc.UNDECIDED)


class OneValueTests(unittest.TestCase):
    def test_holds_on_a_closed_acyclic_run(self) -> None:
        out = fc.one_value_per_node(run_of("E8/mu1/V1/growth"), lambda e, v: v + 1)
        self.assertEqual(out.status, fc.HOLDS)

    def test_a_changing_cycle_fails(self) -> None:
        out = fc.one_value_per_node(run_of("E7/mu1/V1/switch"), lambda e, v: v + 1)
        self.assertEqual(out.status, fc.FAILS)

    def test_a_cycle_that_changes_nothing_is_undecided(self) -> None:
        run = run_of("E7/mu1/V1/switch")
        out = fc.one_value_per_node(run, lambda e, v: v + int(e.changing))
        self.assertEqual(out.status, fc.UNDECIDED)
        self.assertTrue(fc.supplementary_condensation(run, lambda e, v: v + int(e.changing)))
        self.assertIsNone(fc.supplementary_condensation(run, lambda e, v: v + 1))

    def test_holds_at_bound_on_an_open_run(self) -> None:
        run = run_of("E4/mu2/V1/halt")
        out = fc.one_value_per_node(run, lambda e, v: v + int(e.changing))
        self.assertEqual(out.status, fc.HOLDS_AT_BOUND)
        self.assertIsNone(fc.supplementary_condensation(run, lambda e, v: v))

    def test_two_short_paths_fail(self) -> None:
        run = synthetic(
            [(0, 1, "switch", False, False), (1, 2, "switch", False, False), (0, 2, "switch", False, False)],
            {2: fr.FIXPOINT},
            3,
        )
        out = fc.one_value_per_node(run, lambda e, v: v + 1)
        self.assertEqual(out.status, fc.FAILS)
        self.assertEqual(out.witness[:2], (2, 1))

    def test_two_paths_beyond_fifteen_fail(self) -> None:
        """A closed acyclic run whose two paths to one node both run past
        fifteen edges and carry two values: only the exact pass sees it."""
        edges = [(i, i + 1, "switch", False, False) for i in range(20)]
        edges.append((0, 21, "switch", False, False))
        edges.append((21, 20, "switch", True, False))
        run = synthetic(edges, {20: fr.FIXPOINT}, 22)
        out = fc.one_value_per_node(run, lambda e, v: v + int(e.changing) * 100)
        self.assertEqual(out.status, fc.FAILS)
        self.assertEqual(out.note, "two paths beyond fifteen")

    def test_a_changing_cycle_beyond_fifteen_fails(self) -> None:
        """A closed run whose only changing cycle lies past fifteen edges:
        the layered pass cannot see it, the cycle check does."""
        edges = [(i, i + 1, "switch", False, False) for i in range(16)]
        edges += [(16, 17, "growth", True, False), (17, 16, "switch", False, False)]
        run = synthetic(edges, {}, 18)
        out = fc.one_value_per_node(run, lambda e, v: v + int(e.changing))
        self.assertEqual(out.status, fc.FAILS)
        self.assertEqual(out.note, "a changing cycle")
        self.assertEqual(out.witness[0][0], 0)

    def test_a_path_is_found_only_through_allowed_nodes(self) -> None:
        run = synthetic([(0, 1, "switch", False, False)], {1: fr.FIXPOINT}, 3)
        self.assertEqual(fc._path_to(run, 1, lambda v: True, lambda e: True), [0, 1])
        self.assertEqual(fc._path_to(run, 1, lambda v: v != 0, lambda e: True), [])
        self.assertEqual(fc._path_to(run, 2, lambda v: True, lambda e: True), [])

    def test_a_disconnected_component_is_harmless(self) -> None:
        run = synthetic([(1, 2, "switch", False, False)], {0: fr.FIXPOINT, 2: fr.FIXPOINT}, 3)
        self.assertEqual(fc.one_value_per_node(run, lambda e, v: v + 1).status, fc.HOLDS)


class StageTests(unittest.TestCase):
    def facts(self, name: str, reading: str = "L") -> fc.RunFacts:
        run = run_of(name, reading)
        return fc.facts_of(run, fr.node_values(run))

    def test_forced_and_not_forced(self) -> None:
        halt, e4 = self.facts("E1/mu1/V1/halt"), self.facts("E4/mu2/V1/halt")
        self.assertEqual(fc.stage_verdict([halt, e4], "two", 0), {"verdict": "FORCED", "value": 0})
        verdict = fc.stage_verdict([halt, e4], "two", 1)
        self.assertEqual(verdict["verdict"], "NOT_FORCED")
        self.assertEqual(len(verdict["witnesses"]), 2)

    def test_the_fixpoint_persists(self) -> None:
        pops = fc.populations(run_of("E1/mu1/V1/halt"))
        self.assertEqual([p for p, _ in pops], [frozenset({0})] * (fr.ROUND_BOUND + 1))
        self.assertTrue(all(c for _, c in pops))

    def test_a_guard_makes_later_rounds_incomplete(self) -> None:
        run = run_of("E4/mu1/V1/halt", node_guard=5)
        pops = fc.populations(run)
        self.assertFalse(all(c for _, c in pops))
        facts = fc.facts_of(run, fr.node_values(run))
        late = [k for k, (_, c) in enumerate(pops) if not c]
        self.assertEqual(fc.stage_verdict([facts], "branching", late[0])["verdict"], "UNDECIDED")

    def test_a_missing_value_is_undecided(self) -> None:
        facts = self.facts("E1/mu1/V1/halt")
        facts.values[0]["symmetry"] = None
        self.assertEqual(fc.stage_verdict([facts], "symmetry", 0), {"verdict": "UNDECIDED"})


class ForcedOverTests(unittest.TestCase):
    def test_every_verdict(self) -> None:
        h, b, f, u = (fc.Outcome(s) for s in (fc.HOLDS, fc.HOLDS_AT_BOUND, fc.FAILS, fc.UNDECIDED))
        self.assertEqual(fc.forced_over([("a", "L", h)])["verdict"], "FORCED")
        self.assertEqual(fc.forced_over([("a", "L", h), ("b", "L", b)]), {"verdict": "FORCED_AT_BOUND", "at_bound": 1})
        self.assertEqual(fc.forced_over([("a", "L", u), ("b", "L", h)]), {"verdict": "OPEN", "undecided": 1})
        failing = fc.forced_over([("a", "L", h), ("b", "F", fc.Outcome(fc.FAILS, ((0, 1), "x")))])
        self.assertEqual(failing["first_failing"], ["b", "F"])
        self.assertEqual(failing["witness"], [[0, 1], "x"])
        self.assertEqual(fc.forced_over([])["verdict"], "OPEN")
        self.assertEqual(f.status, fc.FAILS)


class IsomorphismTests(unittest.TestCase):
    def test_the_decision_and_the_search_agree(self) -> None:
        a, b, c = run_of("E1/mu1/V1/halt"), run_of("E2/mu2/V2/halt"), run_of("E1/mu1/V1/growth")
        self.assertEqual(fc.run_signature(a), fc.run_signature(b))
        self.assertTrue(fc.brute_run_isomorphic(a, b))
        self.assertNotEqual(fc.run_signature(a), fc.run_signature(c))
        self.assertFalse(fc.brute_run_isomorphic(a, c))
        self.assertEqual(len(fc.signature_digest(fc.run_signature(a))), 64)

    def test_the_search_sees_an_edge_label(self) -> None:
        """NEGATIVE: two runs alike but for one edge's label are told apart
        by the search, which never reads a signature."""
        x = synthetic([(0, 1, "switch", False, False), (1, 0, "switch", False, False)], {}, 2)
        y = synthetic([(0, 1, "switch", False, False), (1, 0, "growth", False, False)], {}, 2)
        self.assertFalse(fc.brute_run_isomorphic(x, y))
        self.assertTrue(fc.brute_run_isomorphic(x, x))
        z = synthetic([(0, 1, "switch", False, False)], {}, 2)
        self.assertFalse(fc.brute_run_isomorphic(x, z))
        w = synthetic([(1, 0, "switch", False, False), (0, 1, "switch", False, False)], {}, 2)
        self.assertTrue(fc.brute_run_isomorphic(x, w))
        v = synthetic([(0, 1, "switch", False, False), (0, 1, "switch", False, False)], {}, 2)
        self.assertFalse(fc.brute_run_isomorphic(x, v))


# ---------------------------------------------------------------------------
# The runner
# ---------------------------------------------------------------------------

SUBSET = ("E1/mu1/V1/halt", "E1/mu1/V1/switch", "E7/mu1/V1/switch", "E6/mu2/V1/switch", "E6/mu2/V2/switch")


class RunnerTests(unittest.TestCase):
    serial: tuple[dict[str, Any], dict[str, Any]]
    parallel: tuple[dict[str, Any], dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        engines = [engine_named(name) for name in SUBSET]
        cls.serial = rf.analyse(1, engines)
        cls.parallel = rf.analyse(2, engines)

    def test_the_worker_count_does_not_change_the_reports(self) -> None:
        self.assertEqual(self.serial, self.parallel)

    def test_continuation_one_replays(self) -> None:
        reports, _ = self.serial
        self.assertTrue(reports["continuation_one_replays"])
        self.assertEqual(len(reports["live"]), 64)

    def test_the_subset_reports(self) -> None:
        reports, full = self.serial
        self.assertEqual(reports["totals"]["runs"], 2 * len(SUBSET))
        self.assertEqual(reports["run_classes"]["v_twins_isomorphic"], 1)
        self.assertEqual(reports["carrying"]["streamless"], [])
        self.assertEqual(reports["runs"]["E6/mu2/V1/switch"]["L"]["closure"], "CYCLES")
        self.assertEqual(set(full["engines"]), set(SUBSET))
        self.assertGreater(reports["run_classes"]["brute_agreements"], 0)
        self.assertEqual(reports["run_classes"]["brute_disagreements"], [])
        self.assertEqual(reports["totals"]["refusal_shapes"], {"apart_transitive": 0, "apart_other": 0, "same": 0})

    def test_the_scorer_can_say_missed(self) -> None:
        reports, _ = self.serial
        scored = rf.score(reports)
        self.assertEqual(scored["R-5"]["verdict"], "MISSED")
        self.assertEqual(scored["R-8"]["verdict"], "MISSED")
        self.assertEqual({v["verdict"] for v in scored.values()} - {"HIT", "MISSED", "ELSEWHERE"}, set())

    def test_the_scorer_names_each_wrong_closure(self) -> None:
        """NEGATIVE: every closure the prediction rules out is named."""
        reports = copy.deepcopy(self.serial[0])
        runs = reports["runs"]
        runs["E6/mu2/V1/switch"]["L"]["closure"] = "NOT_CLOSED"
        runs["E1/mu1/V1/switch"]["L"]["closure"] = "CYCLES"
        runs["E4/mu1/V1/halt"] = copy.deepcopy(runs["E1/mu1/V1/halt"])
        wrong = rf.score(reports)["R-11"]["value"]["wrong"]
        self.assertIn("E6/mu2/V1/switch@L", wrong)
        self.assertIn("E1/mu1/V1/switch@L", wrong)
        self.assertIn("E4/mu1/V1/halt@L", wrong)
        runs["E1/mu1/V1/halt"]["L"]["nodes"] = 9
        misses = rf.score(reports)["R-8"]["value"]["shape_misses"]
        self.assertIn("E1/mu1/V1/halt@L: (9, 0, 'TERMINATES')", misses)

    def test_the_cross_checks_name_a_disagreement_and_count_what_they_skip(self) -> None:
        """NEGATIVE: an injected disagreement of the exhaustive search is
        named, and a key limit of zero counts every regime as above it."""
        engines = [engine_named("E1/mu1/V1/halt"), engine_named("E2/mu1/V1/halt")]
        with mock.patch.object(rf, "brute_run_isomorphic", lambda a, b: False), mock.patch.object(
            rf, "BRUTE_KEY_LIMIT", 0
        ):
            reports, _ = rf.analyse(1, engines)
        self.assertEqual(
            reports["run_classes"]["brute_disagreements"],
            ["E1/mu1/V1/halt~E2/mu1/V1/halt@L", "E1/mu1/V1/halt~E2/mu1/V1/halt@F"],
        )
        self.assertEqual(reports["key_crosscheck"]["above_limit"], 2)

    def test_an_engine_outcome_combines_both_readings(self) -> None:
        self.assertEqual(rf._engine_outcome([fc.HOLDS, fc.HOLDS]), fc.HOLDS)
        self.assertEqual(rf._engine_outcome([fc.HOLDS, fc.HOLDS_AT_BOUND]), fc.HOLDS_AT_BOUND)
        self.assertEqual(rf._engine_outcome([fc.UNDECIDED, fc.HOLDS]), fc.UNDECIDED)
        self.assertEqual(rf._engine_outcome([fc.UNDECIDED, fc.FAILS]), fc.FAILS)

    def test_an_unreadable_value_leaves_a_reading_undecided(self) -> None:
        real = fr.state_key

        def flaky(state: EState) -> Any:
            if state.regime.n_data() == 3:
                raise IsoBudgetError("probe budget")
            return real(state)

        with mock.patch.object(fr, "state_key", flaky):
            run = fr.build_run(engine_named("E8/mu1/V1/growth"), L)
        values = fr.node_values(run)
        candidates = rf._candidate_outcomes(run, values)
        self.assertEqual(candidates["demands"]["preserved"], fc.UNDECIDED)
        values[1]["classes"] = None
        self.assertEqual(rf._run_outcomes(run, values)["two_classes"].status, fc.UNDECIDED)

    def test_forbidden_keys_are_found(self) -> None:
        self.assertEqual(rf.forbidden_keys({"a": [{"Timestamp": 1}], "b": {"cwd": 2}}), ["a[0].Timestamp", "b.cwd"])

    def test_the_full_export_is_byte_stable(self) -> None:
        _, full = self.serial
        one, two = rf.render_full(full), rf.render_full(full)
        self.assertEqual(one, two)
        self.assertEqual(one[4:8], b"\0\0\0\0")
        self.assertEqual(json.loads(gzip.decompress(one)), json.loads(json.dumps(full)))

    def test_main_writes_then_checks_and_names_a_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            argv = ["--receipts", tmp, "--workers", "1", "--only", "E1/mu1/V1/halt"]
            self.assertEqual(rf.main(argv), 0)
            self.assertEqual(rf.main(argv + ["--check"]), 0)
            target = pathlib.Path(tmp) / rf.RECEIPT_NAME
            target.write_bytes(target.read_bytes().replace(b'"runs": 2', b'"runs": 3'))
            self.assertEqual(rf.main(argv + ["--check"]), 1)
            (pathlib.Path(tmp) / rf.FULL_NAME).unlink()
            self.assertEqual(rf.main(argv + ["--check"]), 1)

    def test_main_refuses_a_forbidden_key_and_an_oversized_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            argv = ["--receipts", tmp, "--workers", "1", "--only", "E1/mu1/V1/halt"]
            real = rf.build

            def tainted(workers: int, engines: Any) -> Any:
                payload, compressed = real(workers, engines)
                payload["host"] = "x"
                return payload, compressed

            with mock.patch.object(rf, "build", tainted):
                self.assertEqual(rf.main(argv), 1)
            with mock.patch.object(rf, "MEGABYTE", 10):
                self.assertEqual(rf.main(argv), 1)

    def test_the_frozen_digests_are_the_manifest_ones(self) -> None:
        manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
        frozen = {item["path"].split("/")[-1]: item["sha256"] for item in manifest["frozen_texts"]}
        self.assertEqual(rf.frozen_digest("PROMPT.md"), frozen["PROMPT.md"])
        self.assertEqual(rf.frozen_digest("PREDICTIONS.md"), frozen["PREDICTIONS.md"])


class CommittedReceiptTests(unittest.TestCase):
    """The committed receipts, read as bytes: their scores are the
    scorer's, the full export is the one the summary names, and the
    summary is small enough to stand alone."""

    payload: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads((RECEIPTS / rf.RECEIPT_NAME).read_text(encoding="utf-8"))

    def test_the_scores_are_recomputed_from_the_reports(self) -> None:
        rescored = json.loads(json.dumps(rf.score(self.payload["reports"])))
        self.assertEqual(rescored, self.payload["predictions_scored"])

    def test_the_full_export_is_the_one_named(self) -> None:
        raw = (RECEIPTS / rf.FULL_NAME).read_bytes()
        named = self.payload["full_export"]
        import hashlib

        self.assertEqual(hashlib.sha256(raw).hexdigest(), named["compressed_sha256"])
        self.assertEqual(hashlib.sha256(gzip.decompress(raw)).hexdigest(), named["content_sha256"])

    def test_the_summary_stands_alone(self) -> None:
        self.assertLess((RECEIPTS / rf.RECEIPT_NAME).stat().st_size, rf.MEGABYTE)
        self.assertEqual(rf.forbidden_keys(self.payload), [])
        self.assertEqual(self.payload["reports"]["totals"]["runs"], 288)

    def test_every_frontier_is_exported(self) -> None:
        full = json.loads(gzip.decompress((RECEIPTS / rf.FULL_NAME).read_bytes()))
        runs = self.payload["reports"]["runs"]
        for name, row in runs.items():
            for reading, summary in row.items():
                payload = full["payloads"][full["engines"][name][reading]]
                self.assertEqual(len(payload["frontier"]), summary["frontier"], f"{name}@{reading}")

    def test_every_failing_witness_path_starts_at_the_root(self) -> None:
        verdicts = self.payload["reports"]["run_verdicts"]
        for set_name, rows in verdicts.items():
            for reading_name, verdict in rows.items():
                witness: Optional[Any] = verdict.get("witness")
                if verdict["verdict"] == "NOT_FORCED" and isinstance(witness, list) and witness:
                    first = witness[0]
                    path = first if isinstance(first, list) else witness[2]
                    self.assertEqual(path[0], 0, f"{set_name}/{reading_name}")


class ShadowTests(unittest.TestCase):
    def test_the_tree_modules_are_not_shadowed_by_a_sibling(self) -> None:
        for module in (fr, fc, rf):
            self.assertEqual(pathlib.Path(module.__file__ or "").resolve().parent, HERE)
        self.assertIsInstance(SwitchMarker(), SwitchMarker)


if __name__ == "__main__":
    unittest.main()
