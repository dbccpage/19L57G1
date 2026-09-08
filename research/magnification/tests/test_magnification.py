"""The exports against the engine's class; one named negative case per check;
the restart and magnification witnesses."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys
import tempfile
from typing import Mapping, Optional, Sequence, cast
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

import magnification as mg  # noqa: E402
from derivation.candidates import Bounds, NewForm, NewInst, min_responses, response_valid_naive  # noqa: E402
from derivation.engine import READING_F, READING_L, closure_challenge_orbits  # noqa: E402
from derivation.export import Json, read_json_gz, write_json_gz  # noqa: E402
from derivation.iso import canonical  # noqa: E402
from derivation.model import Regime, replay  # noqa: E402
from derivation.observe import collapsed_pairs  # noqa: E402

REPO = Path(__file__).resolve().parents[3]


def failures_of(record: Mapping[str, Json]) -> list[str]:
    return [str(f) for f in cast(Sequence[Json], record["failures"])]


def rewire_a_grandchild(ex: mg.Export) -> Optional[mg.Export]:
    """Point one grandchild edge of a two-step-checked node at a node of a
    class its grandchildren do not carry."""
    status = {int(str(n["id"])): str(n["status"]) for n in ex.nodes}
    keys = {nid: canonical(r) for nid, r in ex.regimes.items()}
    out: dict[int, list[tuple[int, int]]] = {}
    for k, e in enumerate(ex.edges):
        out.setdefault(int(str(e["parent"])), []).append((k, int(str(e["child"]))))
    for nid in sorted(out):
        children = [c for _, c in out[nid]]
        if status[nid] != "expanded" or any(status[c] != "expanded" for c in children):
            continue
        grand_keys = {keys[g] for c in children for _, g in out.get(c, [])}
        for c in children:
            for k, _ in out.get(c, []):
                for other in sorted(keys):
                    if keys[other] not in grand_keys:
                        edges = list(ex.edges)
                        edge = dict(edges[k])
                        edge["child"] = other
                        edges[k] = edge
                        return replace(ex, edges=tuple(edges))
    return None


class ClosedExports(unittest.TestCase):
    closed_l: mg.Export
    closed_f: mg.Export

    @classmethod
    def setUpClass(cls) -> None:
        cls.closed_l = mg.load(REPO, "closed_L")
        cls.closed_f = mg.load(REPO, "closed_F")

    def test_every_status_and_fan_agrees_with_the_relation(self) -> None:
        for ex, fans, rounds in ((self.closed_l, 1, 3), (self.closed_f, 4, 19)):
            record = mg.check_export(ex)
            self.assertEqual(failures_of(record), [])
            self.assertEqual(record["fans_checked"], fans)
            self.assertEqual(record["rounds_checked"], rounds)
            self.assertEqual(record["rounds_minimum_and_representative"], rounds)
            self.assertIsNone(record["first_cutoff_depth"])

    def test_orbit_demands_agree_with_brute_force(self) -> None:
        for ex in (self.closed_l, self.closed_f):
            record = mg.brute_orbit_check(ex)
            self.assertEqual(cast(Sequence[Json], record["disagreements"]), [])
            self.assertEqual(record["nodes_checked"], len(ex.regimes))

    def test_two_step_restart_agrees_with_the_dag(self) -> None:
        record = mg.restart_check(self.closed_f)
        self.assertEqual(failures_of(record), [])
        self.assertEqual(record["nodes_checked"], 1)

    def test_seed_responses_valid_and_context_cheaper(self) -> None:
        record = mg.magnification_check(self.closed_f)
        self.assertEqual(record["seed_responses_valid"], record["creation_rounds"])
        self.assertEqual(record["one_item_minima"], record["rounds_cheaper_than_the_seed"])
        self.assertGreater(int(str(record["rounds_cheaper_than_the_seed"])), 0)

    # --- negative cases, each applied to the check it tests ---

    def test_dropped_tie_edge_is_named(self) -> None:
        mutated = replace(self.closed_l, edges=self.closed_l.edges[:-1])
        failures = failures_of(mg.check_export(mutated))
        self.assertTrue(any("minimum classes have no edge" in f for f in failures), failures)

    def test_repeated_minimum_class_edge_is_named(self) -> None:
        mutated = replace(self.closed_l, edges=self.closed_l.edges + (self.closed_l.edges[-1],))
        failures = failures_of(mg.check_export(mutated))
        self.assertTrue(any("duplicate minimum class" in f for f in failures), failures)

    def test_redundant_response_with_the_same_endpoint_is_refused(self) -> None:
        edges: list[dict[str, Json]] = [dict(e) for e in self.closed_f.edges]
        index = next(k for k, e in enumerate(edges) if len(cast(Sequence[Json], e["response"])) == 1)
        response = list(cast(Sequence[Json], edges[index]["response"]))
        edges[index]["response"] = response + response
        failures = failures_of(mg.check_export(replace(self.closed_f, edges=tuple(edges))))
        self.assertTrue(any("response is not a minimum delta" in f for f in failures), failures)

    def test_unreported_inert_event_is_refused(self) -> None:
        edges: list[dict[str, Json]] = [dict(e) for e in self.closed_l.edges]
        edges[0]["events"] = list(cast(Sequence[Json], edges[0]["events"])) + [
            {"event": "supply", "token": "unreported"}]
        failures = failures_of(mg.check_export(replace(self.closed_l, edges=tuple(edges))))
        self.assertTrue(any("events differ from the declared response" in f for f in failures), failures)

    def test_supply_event_must_match_the_fresh_growth(self) -> None:
        ex = mg.load(REPO, "tree_L_mu2")
        edges: list[dict[str, Json]] = [dict(e) for e in ex.edges]
        index = next(k for k, e in enumerate(edges) if e["challenge"] == "supply")
        edges[index]["events"] = []
        failures = failures_of(mg.check_export(replace(ex, edges=tuple(edges))))
        self.assertTrue(any("supply events differ from fresh growth" in f for f in failures), failures)

    def test_non_minimum_response_is_named(self) -> None:
        edges: list[dict[str, Json]] = [dict(e) for e in self.closed_f.edges]
        index = next(k for k, e in enumerate(edges)
                     if e["challenge"] != "supply" and len(cast(Sequence[Json], e["response"])) == 1)
        parent = self.closed_f.regimes[int(str(edges[index]["parent"]))]
        target = mg.parse_target(str(edges[index]["challenge"]))
        edges[index]["response"] = [{"kind": "form", "arity": 1},
                                    {"kind": "inst", "form": len(parent.forms), "args": [target[1]]}]
        failures = failures_of(mg.check_export(replace(self.closed_f, edges=tuple(edges))))
        self.assertTrue(any("not a minimum class" in f for f in failures), failures)

    def test_wrong_status_is_named(self) -> None:
        nodes: list[dict[str, Json]] = [dict(n) for n in self.closed_f.nodes]
        index = next(k for k, n in enumerate(nodes) if n["status"] == "expanded" and n["id"] != 0)
        nodes[index]["status"] = "completed"
        failures = failures_of(mg.check_export(replace(self.closed_f, nodes=tuple(nodes))))
        self.assertTrue(any("status 'completed', the engine's order gives 'expanded'" in f
                            for f in failures), failures)

    def test_flipped_regime_hash_is_refused_at_load(self) -> None:
        payload = dict(cast(Mapping[str, Json], read_json_gz(REPO / "artifacts" / "full" / "closed_L.json.gz")))
        nodes: list[dict[str, Json]] = [dict(cast(Mapping[str, Json], n))
                                        for n in cast(Sequence[Json], payload["nodes"])]
        nodes[1]["regime_sha256"] = "0" * 64
        payload["nodes"] = cast(Json, nodes)
        with tempfile.TemporaryDirectory() as tmp:
            write_json_gz(Path(tmp) / "artifacts" / "full" / "closed_L.json.gz", cast(Json, payload))
            with self.assertRaisesRegex(mg.ClassError, "sealed certification failed"):
                mg.load(Path(tmp), "closed_L")

    def test_rewired_grandchild_breaks_the_two_step_check(self) -> None:
        mutated = rewire_a_grandchild(self.closed_f)
        self.assertIsNotNone(mutated)
        assert mutated is not None
        record = mg.restart_check(mutated)
        self.assertTrue(any("two-step classes differ" in f for f in failures_of(record)), record)


class OrbitPolicy(unittest.TestCase):
    def test_least_pair_is_not_the_orbit_policy(self) -> None:
        """The sealed regression regime: two collapsed pairs in two orbits;
        least-pair selection keeps one, the orbit policy keeps both."""
        r = Regime(("a", "b", "c", "d"), (1,), frozenset({(0, (2,)), (0, (3,))}), frozenset(), frozenset())
        self.assertEqual(collapsed_pairs(r), ((0, 1), (2, 3)))
        self.assertEqual(mg.brute_orbit_demands(r), ((0, 1), (2, 3)))
        self.assertEqual(closure_challenge_orbits(r), ((0, 1), (2, 3)))
        least_pair = tuple(sorted(collapsed_pairs(r))[:1])
        self.assertNotEqual(least_pair, mg.brute_orbit_demands(r))

    def test_reading_f_seed_target_is_not_an_orbit_representative(self) -> None:
        root_f = replay(READING_F.genesis)
        self.assertEqual(closure_challenge_orbits(root_f), ((0, 1),))
        self.assertEqual(mg.brute_orbit_demands(root_f), ((0, 1),))
        self.assertNotIn(READING_F.target, closure_challenge_orbits(root_f))
        root_l = replay(READING_L.genesis)
        self.assertEqual(closure_challenge_orbits(root_l), (READING_L.target,))


class Magnification(unittest.TestCase):
    def test_context_changes_the_minimum(self) -> None:
        """The Lean countermodel, executed: one unary form marking datum 0;
        at the collapsed pair (1, 2) the minimum costs one item, the seed's
        mark stays valid but is not among the minima."""
        ctx = Regime(("a", "b", "c"), (1,), frozenset({(0, (0,))}), frozenset(), frozenset())
        self.assertIn((1, 2), collapsed_pairs(ctx))
        mr = min_responses(ctx, (1, 2), "mu1", Bounds())
        assert mr is not None
        self.assertEqual(mr.cost[0], 1)
        self.assertIn((NewInst(0, (2,)),), mr.deltas)
        mark = (NewForm(1), NewInst(1, (1,)))
        self.assertTrue(response_valid_naive(ctx, (1, 2), mark))
        self.assertNotIn(mark, mr.deltas)
        seed = min_responses(replay(READING_L.genesis), (0, 1), "mu1", Bounds())
        assert seed is not None
        self.assertEqual(seed.cost[0], 2)

    def test_restart_from_a_node_reproduces_the_exported_classes(self) -> None:
        ex = mg.load(REPO, "tree_L_mu2")
        for nid in (1, 2, 3):
            record = mg.restart_from_node(ex, nid, 3)
            layers = cast(Sequence[Json], record["layers"])
            self.assertEqual(len(layers), 3)
            for layer in layers:
                self.assertTrue(cast(Mapping[str, Json], layer)["equal"], record)


if __name__ == "__main__":
    unittest.main()
