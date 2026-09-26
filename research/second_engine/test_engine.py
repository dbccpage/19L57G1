"""The declared engine class, the probe, and the receipt.

Each result the receipt records is recomputed here from the declaration
or from the probe, and each refusal the tree relies on is shown to fire on
the exact defect it exists to catch: a label calling an engine one
declaration, an edge holding an event no capability emits, a node whose
history does not replay, a scorer that can only say HIT.  A check that
has never failed is quiet, not proved.
"""

from __future__ import annotations

import copy
import io
import json
import pathlib
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from typing import Any
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import engine_decl as ed  # noqa: E402
import engine_probe as ep  # noqa: E402
import run_engine as re_  # noqa: E402
from rules import APART, FREE, SAME, StakeRule  # noqa: E402
from derivation.candidates import NewDatum, NewForm, NewInst, NewRuleAll  # noqa: E402
from derivation.model import (  # noqa: E402
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    Regime,
    Supply,
)

READING = {reading.name: reading for reading in ep.readings()}
_PAYLOAD: dict[str, Any] | None = None


def payload() -> dict[str, Any]:
    """One build of the receipt payload, shared by the tests that read it."""
    global _PAYLOAD
    if _PAYLOAD is None:
        _PAYLOAD = re_.build()
    return _PAYLOAD


def probe_of(name: str, reading: str) -> ep.Probe:
    return ep.build_probe(ed.engine_named(name), READING[reading])


class DeclarationTests(unittest.TestCase):
    def test_the_class_and_its_literal_subclass(self) -> None:
        members = ed.engine_class()
        self.assertEqual(len(members), 144)
        self.assertEqual(len({m.name for m in members}), 144)
        self.assertEqual(len(ed.literal_class()), 108)
        self.assertTrue(all(m.literal for m in ed.literal_class()))

    def test_a_member_outside_the_declaration_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "not a rule"):
            ed.Engine("E10", "mu1", "V1", False, False)
        with self.assertRaisesRegex(ValueError, "not a measure"):
            ed.Engine("E1", "mu3", "V1", False, False)
        with self.assertRaisesRegex(ValueError, "not a validity"):
            ed.Engine("E1", "mu1", "V3", False, False)
        with self.assertRaises(KeyError):
            ed.engine_named("E1/mu1/V1/nothing")

    def test_the_capability_list_of_one_member(self) -> None:
        engine = ed.engine_named("E6/mu2/V2/growth+switch")
        self.assertEqual(
            engine.capabilities(),
            ("O3", "O4", "demand_read", "growth", "introduced_honoured",
             "least_response", "mu2", "no_regress", "replay", "switch"),
        )
        self.assertEqual(engine.count(), 10)
        self.assertEqual(engine.count(2), 11)
        with self.assertRaisesRegex(ValueError, "one or two"):
            engine.count(3)

    def test_the_count_minima_are_the_declared_sets(self) -> None:
        least = ed.count_minimal(ed.engine_class())
        self.assertEqual(len(least), 16)
        self.assertTrue(all(m.count() == 6 and m.continuation == "halt" for m in least))
        self.assertEqual(ed.count_minimal([]), ())
        literal2 = ed.count_minimal(ed.literal_class(), 2)
        self.assertTrue(all(m.continuation == "switch" for m in literal2))

    def test_inclusion_and_initial_members(self) -> None:
        a = ed.engine_named("E1/mu1/V1/halt")
        b = ed.engine_named("E1/mu1/V2/halt")
        c = ed.engine_named("E2/mu1/V1/halt")
        self.assertEqual(ed.inclusion_minimal([a, b]), (a,))
        self.assertEqual(ed.initial_members([a, b]), (a,))
        self.assertEqual(ed.initial_members([a, c]), ())
        self.assertEqual(set(ed.inclusion_minimal([a, b, c])), {a, c})

    def test_the_shared_capability_pairs(self) -> None:
        pairs = ed.shared_capability_pairs(ed.engine_class())
        self.assertEqual(len(pairs), 32)
        rules = {tuple(sorted((p[0].split("/")[0], p[1].split("/")[0]))) for p in pairs}
        self.assertEqual(rules, {("E2", "E7"), ("E3", "E4")})

    def test_a_label_calling_a_bundle_one_declaration_is_refused(self) -> None:
        """NEGATIVE: the refusal the seed asks for fires, naming the engine
        and every capability it declares."""
        engine = ed.engine_named("E4/mu1/V1/halt")
        with self.assertRaises(ed.BundleRefused) as caught:
            ed.check_declaration_label(engine, 1)
        message = str(caught.exception)
        self.assertIn("E4/mu1/V1/halt", message)
        for capability in engine.capabilities():
            self.assertIn(capability, message)
        ed.check_declaration_label(engine, engine.count())

    def test_every_member_refuses_the_label(self) -> None:
        refused = 0
        for engine in ed.engine_class():
            with self.assertRaises(ed.BundleRefused):
                ed.check_declaration_label(engine, 1)
            refused += 1
        self.assertEqual(refused, 144)

    def test_the_input_tally(self) -> None:
        self.assertEqual(ed.input_tally(ed.engine_named("E4/mu1/V1/halt")),
                         {"stake": True, "stream": False})
        self.assertEqual(ed.input_tally(ed.engine_named("E4/mu1/V1/growth")),
                         {"stake": True, "stream": True})


class GeneratorTests(unittest.TestCase):
    def test_the_flip_exchanges_apart_and_same_and_keeps_free(self) -> None:
        genesis = ed.engine_replay(READING["F"].genesis).regime
        for rule in ed.RULE_NAMES:
            plain = ed.moded_rule(rule, ed.PLAIN)
            flipped = ed.moded_rule(rule, ed.FLIPPED)
            swap = {APART: SAME, SAME: APART, FREE: FREE}
            for pair in ((0, 1), (0, 2), (1, 2)):
                self.assertEqual(flipped.label(genesis, *pair), swap[plain.label(genesis, *pair)])
        self.assertIs(ed.moded_rule("E4", ed.FLIPPED), ed.moded_rule("E4", ed.FLIPPED))

    def test_an_unknown_mode_or_rule_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            ed.moded_rule("E1", "sideways")
        with self.assertRaises(KeyError):
            ed.moded_rule("E0", ed.PLAIN)

    def test_the_replay_rule_flips_on_every_marker(self) -> None:
        history = tuple(READING["L"].genesis)
        self.assertEqual(ed.engine_replay(history).mode, ed.PLAIN)
        once = ed.engine_replay(history + (ed.SwitchMarker(),))
        twice = ed.engine_replay(history + (ed.SwitchMarker(), ed.SwitchMarker()))
        self.assertEqual(once.mode, ed.FLIPPED)
        self.assertEqual(twice.mode, ed.PLAIN)
        self.assertEqual(once.regime, twice.regime)

    def test_growth_supplies_and_admits_one_fresh_token(self) -> None:
        regime = ed.engine_replay(READING["L"].genesis).regime
        supply, admit = ed.growth_events(regime)
        self.assertIsInstance(supply, Supply)
        self.assertIsInstance(admit, AdmitDatum)
        self.assertEqual(supply.token, admit.token)
        crowded = Regime(regime.data + ("engine_g2",), (), frozenset(), frozenset(), frozenset())
        self.assertEqual(ed.growth_events(crowded)[0].token, "engine_g3")
        taken = Regime(("engine_g2", "x"), (), frozenset(), frozenset(), frozenset())
        self.assertEqual(ed.growth_events(taken)[0].token, "engine_g2_1")


class ResponderTests(unittest.TestCase):
    def test_the_genesis_ties(self) -> None:
        for reading, ties in (("L", (6, 2)), ("F", (10, 2))):
            state = ed.engine_replay(READING[reading].genesis)
            rule = ed.moded_rule("E4", ed.PLAIN)
            for target in ed.state_demands("E4", state):
                found = ed.least_responses(state.regime, rule, target, "V1")
                assert found is not None
                self.assertEqual((len(found["mu1"].deltas), len(found["mu2"].deltas)), ties)
                self.assertEqual(found["mu1"].item_count, 2)

    def test_an_unknown_member_is_refused(self) -> None:
        state = ed.engine_replay(READING["L"].genesis)
        with self.assertRaises(ValueError):
            ed.least_responses(state.regime, ed.moded_rule("E4", ed.PLAIN), ("apart", (0, 1)), "V9")

    def test_a_demand_no_delta_can_answer_is_refused(self) -> None:
        """Three collapsed data with the pair (0, 1) labelled apart and the
        two other pairs labelled same: separating 0 from 1 breaks one of
        the pairs honoured before, so member one refuses every delta."""

        def labeler(regime: Regime, i: int, j: int) -> Any:
            return APART if (i, j) == (0, 1) else SAME

        rule = StakeRule("probe_rule", ("O1",), labeler, "menu")
        state = ed.engine_replay(READING["F"].genesis)
        self.assertIsNone(ed.least_responses(state.regime, rule, ("apart", (0, 1)), "V1", memo=False))

    def test_member_two_refuses_an_introduced_datum_left_unhonoured(self) -> None:
        """The clause member two adds: a delta introducing a datum whose
        pair with a held datum is labelled and not honoured afterwards."""
        state = ed.engine_replay(READING["L"].genesis)
        rule = ed.moded_rule("E4", ed.PLAIN)
        delta = (NewDatum(), NewForm(1))
        self.assertFalse(ed.introduced_clause(state.regime, rule, delta))
        self.assertTrue(ed.introduced_clause(state.regime, rule, (NewForm(1),)))

    def test_the_responder_agrees_with_rung_two(self) -> None:
        state = ed.engine_replay(READING["F"].genesis)
        for rule in ("E4",):
            for target in ed.state_demands(rule, state):
                self.assertEqual(
                    ep.responder_crosscheck(state.regime, rule, ed.PLAIN, target),
                    {"mu1": True, "mu2": True},
                )

    def test_the_crosscheck_reads_a_refusal_on_both_sides(self) -> None:
        state = ed.engine_replay(READING["L"].genesis)
        with mock.patch.object(ep, "least_responses", return_value=None), mock.patch.object(
            ep, "rung_two_minimum_responses", return_value=None
        ):
            self.assertEqual(
                ep.responder_crosscheck(state.regime, "E4", ed.PLAIN, ("apart", (0, 1))),
                {"mu1": True, "mu2": True},
            )
        with mock.patch.object(ep, "least_responses", return_value=None):
            self.assertEqual(
                ep.responder_crosscheck(state.regime, "E4", ed.PLAIN, ("apart", (0, 1))),
                {"mu1": False, "mu2": False},
            )


class ProbeTests(unittest.TestCase):
    def test_the_four_root_terminals(self) -> None:
        self.assertEqual(probe_of("E4/mu1/V1/halt", "L").root_terminal, "responded")
        self.assertEqual(probe_of("E1/mu1/V1/halt", "L").root_terminal, "fixpoint")
        self.assertEqual(probe_of("E1/mu1/V1/switch", "L").root_terminal, "continued")
        with mock.patch.object(ep, "least_responses", return_value=None):
            refused = ep.build_probe(ed.engine_named("E4/mu1/V1/halt"), READING["L"])
        self.assertEqual(refused.root_terminal, "refused")
        self.assertEqual(refused.edges, [])

    def test_a_switch_child_is_answered_and_a_quiet_one_names_its_continuations(self) -> None:
        live = probe_of("E1/mu2/V1/growth+switch", "L")
        vias = sorted(node.via for node in live.nodes[1:])
        self.assertEqual(vias, ["growth", "switch"])
        switch_child = next(node for node in live.nodes if node.via == "switch")
        assert switch_child.answers is not None
        self.assertTrue(all(record.answered for record in switch_child.answers))
        growth_child = next(node for node in live.nodes if node.via == "growth")
        self.assertEqual(growth_child.enabled, ("growth", "switch"))
        quiet = probe_of("E7/mu1/V1/switch", "F")
        self.assertEqual(quiet.nodes[1].enabled, ("switch",))

    def test_growth_stops_at_the_data_bound(self) -> None:
        grown = probe_of("E2/mu1/V1/growth", "F")
        self.assertEqual(grown.nodes[1].state.regime.n_data(), 4)
        self.assertEqual(grown.nodes[1].enabled, ())

    def test_every_node_replays_and_every_edge_is_attributed(self) -> None:
        for engine in ed.engine_class():
            for reading in READING.values():
                probe = ep.build_probe(engine, reading)
                self.assertEqual(ep.replay_mismatches(probe), [])
                self.assertEqual(ep.attribution_violations(probe), [])

    def test_a_node_that_does_not_replay_is_named(self) -> None:
        """NEGATIVE: the replay check bites."""
        probe = probe_of("E4/mu1/V1/halt", "L")
        probe.nodes[1].state = ed.EState(probe.nodes[1].state.regime, ed.FLIPPED)
        self.assertEqual(ep.replay_mismatches(probe), ["E4/mu1/V1/halt@L: node 1"])

    def test_an_edge_carrying_a_requirement_is_named(self) -> None:
        """NEGATIVE: an edge holding an event no capability emits -- a
        requirement -- is refused by name."""
        probe = probe_of("E4/mu1/V1/halt", "L")
        probe.edges[0].events = probe.edges[0].events + (Impose(0, 1),)
        violations = ep.attribution_violations(probe)
        self.assertEqual(len(violations), 1)
        self.assertIn("Impose", violations[0])
        self.assertIn("edge 0", violations[0])

    def test_every_other_misattribution_is_named(self) -> None:
        cases: list[tuple[str, str, Any]] = []
        probe = probe_of("E4/mu1/V1/halt", "L")
        probe.edges[0].delta = (NewForm(1), NewRuleAll(0))
        cases.append(("not a recorded minimum", "", probe))
        probe = probe_of("E4/mu1/V1/halt", "L")
        probe.edges[0].pair = (0, 5)
        cases.append(("answers no demand", "", probe))
        probe = probe_of("E4/mu1/V1/halt", "L")
        probe.edges[0].events = probe.edges[0].events[:1]
        cases.append(("other than its delta's admissions", "", probe))
        probe = probe_of("E4/mu1/V1/halt", "L")
        probe.edges[0].kind = "teleport"
        cases.append(("unknown kind", "", probe))
        probe = probe_of("E2/mu1/V1/growth", "L")
        probe.edges[0].events = (Supply("a"), AdmitDatum("b"))
        cases.append(("one fresh token", "", probe))
        probe = probe_of("E2/mu1/V1/growth", "L")
        probe.engine = ed.engine_named("E2/mu1/V1/halt")
        cases.append(("growth is not enabled", "", probe))
        probe = probe_of("E2/mu1/V1/switch", "L")
        probe.edges[0].events = (AdmitForm(1),)
        cases.append(("one switch marker", "", probe))
        probe = probe_of("E2/mu1/V1/switch", "L")
        probe.engine = ed.engine_named("E2/mu1/V1/halt")
        cases.append(("switch is not enabled", "", probe))
        for fragment, _, tampered in cases:
            violations = ep.attribution_violations(tampered)
            self.assertEqual(len(violations), 1, fragment)
            self.assertIn(fragment, violations[0])

    def test_labels_and_the_exhaustive_search_agree_and_both_say_no(self) -> None:
        a = probe_of("E4/mu1/V1/halt", "F")
        b = probe_of("E4/mu1/V1/growth", "F")
        c = probe_of("E4/mu2/V1/halt", "F")
        d = probe_of("E1/mu1/V1/halt", "F")
        self.assertEqual(ep.probe_signature(a), ep.probe_signature(b))
        self.assertTrue(ep.brute_isomorphic(a, b))
        self.assertNotEqual(ep.probe_signature(a), ep.probe_signature(c))
        self.assertFalse(ep.brute_isomorphic(a, c))
        self.assertFalse(ep.brute_isomorphic(a, d))
        self.assertEqual(len(ep.signature_digest(ep.probe_signature(a))), 64)

    def test_the_search_tells_a_relabelled_edge_apart(self) -> None:
        """NEGATIVE: two probes with one level-one state each and equal
        state labels, differing only in the label of the edge into it."""
        a = probe_of("E1/mu1/V1/switch", "L")
        b = probe_of("E1/mu1/V1/switch", "L")
        b.edges[0].kind = "growth"
        self.assertFalse(ep.brute_isomorphic(a, b))
        self.assertNotEqual(ep.probe_signature(a), ep.probe_signature(b))
        c = probe_of("E1/mu1/V1/switch", "L")
        c.edges.append(copy.copy(c.edges[0]))
        self.assertFalse(ep.brute_isomorphic(a, c))

    def test_the_key_partition_against_the_brute_force_minimum(self) -> None:
        regimes = [node.state.regime for node in probe_of("E4/mu1/V1/halt", "F").nodes]
        check = ep.key_brute_disagreements(regimes)
        self.assertEqual(check["disagreements"], 0)
        self.assertEqual(check["regimes"], len(regimes))
        self.assertLess(check["classes"], len(regimes))


class CrosscheckInjectionTests(unittest.TestCase):
    """NEGATIVE: every cross-check of the receipt reports a disagreement
    when one is injected, so the zeros the receipt records are
    measurements and not the only value the code can produce."""

    def test_an_isomorphism_disagreement_is_reported(self) -> None:
        with mock.patch.object(re_, "brute_isomorphic", return_value=True):
            reports = re_.analyse()
        self.assertTrue(reports["crosscheck"]["iso_disagreements"])
        self.assertEqual(reports["crosscheck"]["iso_comparisons_not_isomorphic"], 0)

    def test_a_responder_disagreement_with_rung_two_is_reported(self) -> None:
        with mock.patch.object(re_, "responder_crosscheck", return_value={"mu1": False, "mu2": True}):
            reports = re_.analyse()
        self.assertEqual(len(reports["crosscheck"]["rung_two_disagreements"]), 4)

    def test_a_representative_and_a_member_disagreement_are_reported(self) -> None:
        real = ed.least_responses

        def skewed(regime: Regime, rule: StakeRule, target: Any, validity: str) -> Any:
            if rule.name == "E9~" and target[1] == (0, 2):
                return None
            if rule.name == "E2~" and validity == "V2" and target[1] == (1, 2):
                found = real(regime, rule, target, validity)
                assert found is not None
                return {"mu1": found["mu2"], "mu2": found["mu2"]}
            return real(regime, rule, target, validity)

        with mock.patch.object(re_, "least_responses", side_effect=skewed):
            reports = re_.analyse()
        cross = reports["crosscheck"]
        self.assertTrue(any("E9/flipped" in item for item in cross["representative_disagreements"]))
        self.assertTrue(any("E2/flipped" in item for item in cross["member_one_two_disagreements"]))
        self.assertGreater(cross["refused_situations"], 0)

    def test_the_item_shapes(self) -> None:
        delta = (NewDatum(), NewForm(1), NewRuleAll(0), NewInst(0, (0,)))
        self.assertEqual(re_._item_shape(delta), "datum+form+inst+rule")

    def test_the_demand_census_names_an_odd_state_at_l(self) -> None:
        probe = probe_of("E4/mu1/V1/halt", "L")
        clean = re_.demand_census([probe])
        self.assertEqual(clean["e4_children_at_L_reading_other_than_one_same"], 0)
        self.assertEqual(clean["same_demands_after_an_e4_response"]["L"], [1])
        probe.nodes[1].demands = probe.nodes[1].demands + (("apart", (0, 1)),)
        self.assertEqual(re_.demand_census([probe])["e4_children_at_L_reading_other_than_one_same"], 1)
        grown = probe_of("E2/mu1/V1/growth", "L")
        grown.nodes[1].demands = (("same", (0, 2)),)
        self.assertEqual(re_.demand_census([grown])["demands_at_growth_states"], 1)

    def test_member_two_drops_a_delta_member_one_keeps(self) -> None:
        """Two collapsed data and one unary form, E-four labelling the pair
        apart.  At two items member one keeps the delta admitting a fresh
        datum and an instance on the first datum; member two drops it,
        because the fresh datum and the second one are left in one orbit
        and collapsed, labelled apart and not honoured."""
        regime = Regime(("a", "b"), (1,), frozenset(), frozenset(), frozenset())
        rule = ed.moded_rule("E4", ed.PLAIN)
        target: ed.Target = ("apart", (0, 1))
        wide = ed._valid_at(regime, rule, target, "V1", 2, False)
        strict = ed._valid_at(regime, rule, target, "V2", 2, False)
        dropped = sorted(set(wide) - set(strict), key=repr)
        self.assertTrue(set(strict) < set(wide))
        self.assertIn((NewDatum(), NewInst(0, (0,))), dropped)
        self.assertTrue(all(any(isinstance(i, NewDatum) for i in d) for d in dropped))

    def test_the_no_op_filter_drops_a_rule_already_standing(self) -> None:
        ruled = Regime(("a", "b"), (1,), frozenset(), frozenset({0}), frozenset())
        ones = ed._valid_at(ruled, ed.moded_rule("E1", ed.FLIPPED), ("same", (0, 1)), "V1", 1, False)
        self.assertFalse(any(isinstance(i, NewRuleAll) for d in ones for i in d))

    def test_the_search_backtracks_and_remembers(self) -> None:
        """Three level-one states labelled x, x, y on the left and x, x, z
        on the right: the search places both x states, fails on y, swaps
        the x states, reaches the remembered failure and says no; with z
        made y it says yes."""
        a = probe_of("E1/mu1/V1/switch", "L")
        b = probe_of("E1/mu1/V1/switch", "L")
        for probe in (a, b):
            base = probe.nodes[1]
            probe.nodes[1:] = [
                ep.PNode(k + 1, 1, base.history, base.state, base.demands, base.via)
                for k in range(3)
            ]
            probe.edges = []
        labels = {id(a): {1: "x", 2: "x", 3: "y"}, id(b): {1: "x", 2: "x", 3: "z"}}
        owner = {id(node): id(probe) for probe in (a, b) for node in probe.nodes}

        def fake(node: ep.PNode) -> Any:
            if node.level == 0:
                return ("root",)
            return (labels[owner[id(node)]][node.node_id],)

        with mock.patch.object(ep, "node_label", side_effect=fake):
            self.assertFalse(ep.brute_isomorphic(a, b))
            labels[id(b)][3] = "y"
            self.assertTrue(ep.brute_isomorphic(a, b))


class JsonTests(unittest.TestCase):
    def test_every_item_and_event_kind_is_written(self) -> None:
        delta = (NewDatum(), NewForm(2), NewRuleAll(0), NewInst(0, (1, 0)))
        self.assertEqual(
            ep.delta_json(delta),
            [{"item": "datum"}, {"item": "form", "arity": 2}, {"item": "rule", "form": 0},
             {"item": "inst", "form": 0, "args": [1, 0]}],
        )
        self.assertEqual(ep.event_json(ed.SwitchMarker()), {"event": "switch"})
        self.assertEqual(ep.event_json(AdmitInst(0, (1,))), {"event": "AdmitInst", "form": 0, "args": [1]})
        self.assertEqual(ep.event_json(AdmitRuleAll(0)), {"event": "AdmitRuleAll", "form": 0})
        self.assertEqual(ep.event_json(Impose(0, 1)), {"event": "Impose", "i": 0, "j": 1})

    def test_a_probe_payload_names_no_engine(self) -> None:
        text = json.dumps(ep.probe_payload(probe_of("E4/mu1/V1/halt", "L")))
        self.assertNotIn("E4/", text)


class ReceiptTests(unittest.TestCase):
    def test_every_computed_prediction_is_a_hit(self) -> None:
        scored = payload()["predictions_scored"]
        computed = {pid: row["verdict"] for pid, row in scored.items() if row["verdict"] != "ELSEWHERE"}
        self.assertEqual(sorted(computed), sorted(
            ["C-8", "C-9", "C-10", "C-11", "C-12", "C-13", "C-14", "C-15", "C-16", "C-17",
             "C-18", "C-19", "C-22"]))
        self.assertEqual(set(computed.values()), {"HIT"})
        self.assertEqual(len(scored), 23)

    def test_the_scorer_can_say_missed(self) -> None:
        """NEGATIVE: a scorer that can only say HIT proves nothing.  Each
        computed row is scored against a report altered at the value it
        reads, and each comes back MISSED."""
        reports = payload()["reports"]
        alterations: dict[str, Any] = {
            "C-8": lambda r: r["class"].__setitem__("members", 143),
            "C-9": lambda r: r["class"].__setitem__("shared_capability_pairs", 31),
            "C-10": lambda r: r["class"].__setitem__("members_of_count_one", 1),
            "C-11": lambda r: r["probe"].__setitem__("demands_at_growth_states", 1),
            "C-12": lambda r: r["probe"].__setitem__("refusals", 1),
            "C-13": lambda r: r["probe"].__setitem__("e4_children_at_L_reading_other_than_one_same", 1),
            "C-14": lambda r: r["live"].pop(),
            "C-15": lambda r: r["minima"]["class/live/1"]["members"].pop(),
            "C-16": lambda r: r["minima"]["class/all/1"].__setitem__("probe_classes", 1),
            "C-17": lambda r: r["minima"]["class/all/1"]["initial_in_minima"].append("x"),
            "C-18": lambda r: r["probe"]["attribution_violations"].append("x"),
            "C-19": lambda r: r["crosscheck"]["iso_disagreements"].append("x"),
            "C-22": lambda r: r["streamless_live"].pop(),
        }
        for pid, alter in alterations.items():
            altered = copy.deepcopy(reports)
            alter(altered)
            self.assertEqual(re_.score(altered)[pid]["verdict"], "MISSED", pid)

    def test_the_committed_receipt_regenerates_byte_identically(self) -> None:
        committed = (HERE / "receipts" / re_.RECEIPT_NAME).read_bytes().replace(b"\r\n", b"\n")
        self.assertEqual(re_.render(payload()), committed)
        self.assertLess(len(committed), re_.MEGABYTE)

    def test_the_probe_puts_the_members_in_ten_classes(self) -> None:
        probe = payload()["reports"]["probe"]
        self.assertEqual(probe["member_classes_by_signature"], 10)
        self.assertEqual(probe["member_classes_by_content"], 10)
        self.assertEqual(probe["distinct_probe_payloads"], 20)

    def test_the_receipt_carries_no_forbidden_key(self) -> None:
        self.assertEqual(re_.forbidden_keys(payload()), [])
        self.assertEqual(re_.forbidden_keys({"a": [{"Timestamp": 1}]}), ["a[0].Timestamp"])

    def test_the_receipt_records_its_frozen_texts(self) -> None:
        self.assertEqual(payload()["prompt_sha256"], re_.frozen_digest("PROMPT.md"))
        self.assertEqual(payload()["input_count_claim"], "none")

    def _main(self, argv: list[str]) -> tuple[int, str]:
        out = io.StringIO()
        with redirect_stdout(out):
            code = re_.main(argv)
        return code, out.getvalue()

    def test_the_entry_point_writes_checks_and_refuses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, text = self._main(["--receipts", tmp, "--check"])
            self.assertEqual(code, 1)
            self.assertIn("is missing", text)
            code, text = self._main(["--receipts", tmp])
            self.assertEqual(code, 0)
            self.assertIn("wrote", text)
            code, text = self._main(["--receipts", tmp, "--check"])
            self.assertEqual(code, 0)
            self.assertIn("matches a fresh run", text)
            target = pathlib.Path(tmp) / re_.RECEIPT_NAME
            target.write_bytes(target.read_bytes() + b" ")
            code, text = self._main(["--receipts", tmp, "--check"])
            self.assertEqual(code, 1)
            self.assertIn("differs from a fresh run", text)

    def test_the_entry_point_refuses_a_forbidden_key_and_an_oversized_receipt(self) -> None:
        with mock.patch.object(re_, "build", return_value={"timestamp": 0, "predictions_scored": {}}):
            code, text = self._main(["--check"])
        self.assertEqual(code, 1)
        self.assertIn("forbidden keys", text)
        big = {"blob": "x" * (re_.MEGABYTE + 1), "predictions_scored": {}}
        with mock.patch.object(re_, "build", return_value=big):
            code, text = self._main(["--check"])
        self.assertEqual(code, 1)
        self.assertIn("must be split", text)


if __name__ == "__main__":
    unittest.main()
