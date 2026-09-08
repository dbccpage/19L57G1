"""The census over the real exports, and one negative test per invariant.

Each negative test mutates one reconstructed node or one exported edge in
memory and asserts that the check fails naming exactly that node or edge.
Nothing under artifacts/ is written.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Mapping, Sequence, cast
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parents[1] / "code"))

import census  # noqa: E402
from derivation.candidates import Bounds  # noqa: E402
from derivation.export import Json, read_json_gz, verify_full_export  # noqa: E402
from derivation.model import Event, Regime  # noqa: E402
from derivation.observe import collapsed_pairs  # noqa: E402


def _load(name: str) -> Mapping[str, object]:
    return cast(Mapping[str, object], read_json_gz(census.ROOT / "artifacts" / "full" / f"{name}.json.gz"))


class CensusOverTheExports(unittest.TestCase):
    payload: census.JsonDict

    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = census.census()

    def test_every_node_satisfies_every_invariant(self) -> None:
        exports = cast(Mapping[str, Mapping[str, object]], self.payload["exports"])
        self.assertEqual(set(exports), set(census.EXPORTS))
        for name, record in exports.items():
            verdicts = cast(Mapping[str, Mapping[str, int]], record["invariants"])
            for key in census.INVARIANTS:
                self.assertEqual(verdicts[key]["fails_on"], 0, f"{name}: {key}")
                self.assertEqual(verdicts[key]["holds_on"], record["nodes"], f"{name}: {key}")

    def test_every_round_is_a_recorded_minimum(self) -> None:
        totals = cast(Mapping[str, int], self.payload["totals"])
        self.assertEqual(totals["rounds"], totals["minimum_agreements"])
        self.assertEqual(totals["rounds"] + totals["supply"], totals["edges"])

    def test_every_node_is_its_own_class(self) -> None:
        exports = cast(Mapping[str, Mapping[str, object]], self.payload["exports"])
        for name, record in exports.items():
            per_depth = cast(Mapping[str, Mapping[str, int]], record["classes_per_depth"])
            for depth, row in per_depth.items():
                self.assertEqual(row["nodes"], row["classes"], f"{name} depth {depth}")

    def test_committed_record_is_current(self) -> None:
        self.assertEqual(census.OUTPUT.read_bytes(), census.render(self.payload))

    def test_unreachable_states_are_not_exported(self) -> None:
        for row in cast(Sequence[Mapping[str, object]], self.payload["countermodels"]):
            self.assertFalse(row["isomorphic_to_an_exported_node"], str(row["name"]))
            self.assertTrue(row["well_formed"])
            nearest = cast(Mapping[str, object], row["nearest_exported_node"])
            self.assertEqual(nearest["distance"], 1)

    def test_closure_fixpoints_are_not_the_all_pairs_demanded_subset(self) -> None:
        exports = cast(Mapping[str, Mapping[str, object]], self.payload["exports"])
        expected = {"closed_L": 3, "closed_F": 16, "tree_L_mu1": 968,
                    "tree_L_mu2": 414, "tree_F_mu1": 912, "tree_F_mu2": 631}
        for name, count in expected.items():
            self.assertEqual(exports[name]["fixpoints"], count, name)
        totals = cast(Mapping[str, int], self.payload["totals"])
        self.assertEqual(totals["fixpoints"], 2944)
        self.assertEqual(totals["all_pairs_demanded"], 28)


class NegativeTestsNameTheDefect(unittest.TestCase):
    """Every mutation is in memory; the exports on disk are never touched."""

    name: str
    export: Mapping[str, object]
    histories: dict[int, tuple[Event, ...]]
    regimes: dict[int, Regime]
    bounds: Bounds

    @classmethod
    def setUpClass(cls) -> None:
        cls.name = "closed_L"
        cls.export = _load(cls.name)
        cls.histories, cls.regimes = census.reconstruct(cls.name, cls.export)
        cls.bounds = Bounds()

    def _mutated(self, nid: int, regime: Regime) -> dict[int, Regime]:
        regimes = dict(self.regimes)
        regimes[nid] = regime
        return regimes

    def test_a_rule_on_one_node_is_named(self) -> None:
        # Promoting the marking form to a uniform rule also collapses the pair
        # the mark separated, so the answered invariant is named as well.
        r = self.regimes[1]
        regimes = self._mutated(1, Regime(r.data, r.forms, r.insts, frozenset({0}), r.reqs))
        failures = census.node_failures(self.name, regimes)
        self.assertEqual(failures, ["closed_L node 1: invariant rule_free fails",
                                    "closed_L node 1: invariant answered fails"])

    def test_an_ill_formed_instance_on_one_node_is_named(self) -> None:
        r = self.regimes[1]
        bad = r.insts | {(0, (0, 0))}  # arity one form given two arguments
        regimes = self._mutated(1, Regime(r.data, r.forms, bad, r.rules, r.reqs))
        failures = census.node_failures(self.name, regimes)
        self.assertEqual(failures, ["closed_L node 1: invariant well_formed fails"])

    def test_an_unanswered_requirement_on_one_node_is_named(self) -> None:
        r = self.regimes[0]
        regimes = self._mutated(0, Regime(r.data, r.forms, r.insts, r.rules, frozenset({(0, 1)})))
        failures = census.node_failures(self.name, regimes)
        self.assertEqual(failures, ["closed_L node 0: invariant answered fails"])

    def test_a_form_without_an_instance_on_one_node_is_named(self) -> None:
        r = self.regimes[1]
        regimes = self._mutated(1, Regime(r.data, r.forms + (2,), r.insts, r.rules, r.reqs))
        failures = census.node_failures(self.name, regimes)
        self.assertEqual(failures, ["closed_L node 1: invariant forms_used fails"])

    def test_a_non_minimum_response_on_one_edge_is_named(self) -> None:
        edges = [dict(e) for e in cast(Sequence[Mapping[str, object]], self.export["edges"])]
        edges[0]["response"] = list(cast(Sequence[object], edges[0]["response"])) + [
            {"kind": "inst", "form": 0, "args": [1]}
        ]
        payload = dict(self.export)
        payload["edges"] = edges
        failures, _ = census.edge_failures(self.name, payload, self.regimes, "mu1", self.bounds)
        self.assertEqual(failures, ["closed_L edge 0->1: response outside the declared bounds"])

    def test_a_standing_target_on_one_edge_is_named(self) -> None:
        r = self.regimes[0]
        regimes = self._mutated(0, Regime(r.data, r.forms, r.insts, r.rules, frozenset({(0, 1)})))
        failures, _ = census.edge_failures(self.name, self.export, regimes, "mu1", self.bounds)
        self.assertIn("closed_L edge 0->1: target (0, 1) already stands on the parent", failures)

    def test_a_tampered_creation_hash_is_named(self) -> None:
        nodes = [dict(n) for n in cast(Sequence[Mapping[str, object]], self.export["nodes"])]
        nodes[2]["regime_sha256"] = "0" * 64
        payload = dict(self.export)
        payload["nodes"] = nodes
        with self.assertRaises(census.CensusError) as caught:
            census.reconstruct(self.name, payload)
        self.assertIn("closed_L node 2", str(caught.exception))

    def test_a_duplicate_class_is_named(self) -> None:
        regimes = self._mutated(2, self.regimes[1])
        nodes = cast(Sequence[Mapping[str, object]], self.export["nodes"])
        failures, _, _ = census.class_census(self.name, nodes, regimes)
        self.assertEqual(failures, ["closed_L node 2: isomorphic to node 1"])

    def test_actual_events_are_bound_to_the_checked_minimum(self) -> None:
        edges = [dict(e) for e in cast(Sequence[Mapping[str, object]], self.export["edges"])]
        events = list(cast(Sequence[object], edges[0]["events"]))
        # An absorbed repeat preserves every endpoint and the sealed replay
        # certificate, but it is not the advertised two-item response block.
        events.append({"event": "admit_inst", "form": 0, "args": [0]})
        edges[0]["events"] = events
        payload = dict(self.export)
        payload["edges"] = edges
        self.assertTrue(verify_full_export(cast(Mapping[str, Json], payload)))
        failures, _ = census.edge_failures(self.name, payload, self.regimes, "mu1", self.bounds)
        self.assertEqual(failures, ["closed_L edge 0->1: recorded events differ from the imposed target and response"])
        recovered, _ = census.edge_failures(self.name, self.export, self.regimes, "mu1", self.bounds)
        self.assertEqual(recovered, [])

    def test_supply_must_be_fresh_in_the_actual_parent(self) -> None:
        state = Regime(("g1",), (), frozenset(), frozenset(), frozenset())
        payload: dict[str, object] = {"edges": [{"parent": 0, "child": 0, "kind": "merge",
            "challenge": "supply", "response": [], "events": [
                {"event": "supply", "token": "g1"}, {"event": "admit_datum", "token": "g1"}]}]}
        failures, _ = census.edge_failures("probe", payload, {0: state}, "mu1", self.bounds)
        self.assertEqual(failures, ["probe edge 0->0: supply edge does not admit exactly one fresh datum"])
        fresh_parent = Regime(("a",), (), frozenset(), frozenset(), frozenset())
        recovered, _ = census.edge_failures("probe", payload, {0: fresh_parent}, "mu1", self.bounds)
        self.assertEqual(recovered, [])

    def test_a_response_can_separate_pairs_that_were_never_demanded(self) -> None:
        _, regimes = census.reconstruct("closed_F", _load("closed_F"))
        state = regimes[3]
        self.assertEqual(collapsed_pairs(state), ())
        self.assertTrue(census.fixpoint(state))
        self.assertFalse(census.all_pairs_demanded(state))


class TheUnreachableStates(unittest.TestCase):
    def test_form_without_instance_fails_only_the_invariants_it_should(self) -> None:
        state = census.unreachable_states()["form_without_instance"]
        self.assertTrue(census.well_formed(state))
        self.assertTrue(census.rule_free(state))
        self.assertFalse(census.forms_used(state))

    def test_ruled_mark_carries_a_rule(self) -> None:
        state = census.unreachable_states()["ruled_mark"]
        self.assertTrue(census.well_formed(state))
        self.assertFalse(census.rule_free(state))
        self.assertTrue(census.forms_used(state))


if __name__ == "__main__":
    unittest.main()
