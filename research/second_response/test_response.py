"""Tests of the rung-ten cross-check and its runner.

A hand copy of the shape of `research/second_profile/test_profile.py`,
with this rung's pieces.  Three kinds, kept apart:

* the receipt: it regenerates byte-identically, `--check` writes nothing
  and refuses drift, and it carries no temporal or environment key;
* the pieces of `response_rows.py`, each on a regime or a history short
  enough to read by hand, so a quantity checked over the rectangle is
  also checked where its value is known -- including a REFUSED demand,
  which the rectangle never reaches;
* NEGATIVE tests: each census of the report is fed a forged key
  procedure or a forged node and must COUNT what it was built to count,
  and each scored row is moved and must change its verdict, so a report
  of zero is not a report of a check that cannot fire.
"""

from __future__ import annotations

import copy
import json
import pathlib
import sys
import tempfile
import unittest
from typing import Any, Callable

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import response_rows as rr  # noqa: E402

# `response_rows` puts sibling trees on the path and each of them carries
# its own `run_*`, `verify_pins` and `test_*`; this tree goes back to the
# front first.  See the note in `response_rows.py`.
if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))
import run_response as rp  # noqa: E402

from derivation.candidates import NewDatum, NewForm, NewInst, NewRuleAll  # noqa: E402
from derivation.iso import CanonKey, canonical  # noqa: E402
from derivation.model import (  # noqa: E402
    EMPTY,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Regime,
    Supply,
    replay,
)
from iso_index import Keys, Population  # noqa: E402
from index import Rectangle  # noqa: E402
from nofirst import Node  # noqa: E402

RECEIPT = HERE / "receipts" / rp.RECEIPT_NAME
_PAYLOAD: dict[str, Any] | None = None


def payload() -> dict[str, Any]:
    """One build per test run; the rectangle is the expensive part."""
    global _PAYLOAD
    if _PAYLOAD is None:
        _PAYLOAD = rp.build()
    return _PAYLOAD


class CachedBuild:
    """Within a block, the runner's build returns the cached payload.  Used
    only by the tests of the runner's REFUSALS, which read the payload and
    never the computation; the tests of `--check` and of a fresh write
    call the real build."""

    def __enter__(self) -> None:
        self.saved = rp.build
        rp.build = payload

    def __exit__(self, *exc: object) -> None:
        rp.build = self.saved


def regime(*events: Event) -> Regime:
    return replay(tuple(events), EMPTY)


N = rr.ALPHABET.fresh_tokens

# Three data and one form of arity one: the regime of the Lean exhibit
# `one_inst_moves_two_pairs`, in the Python grammar.
THREE = (AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitDatum(N[2]), AdmitForm(1))

# Four data and a requirement on every pair of them: no response of at
# most two items separates all six pairs, so every demand is REFUSED.
REFUSING = (
    AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitDatum(N[2]), AdmitDatum(N[3]),
    Impose(0, 1), Impose(0, 2), Impose(0, 3), Impose(1, 2), Impose(1, 3), Impose(2, 3),
)


class LumpingKeys(Keys):
    """A FORGED key procedure that puts every regime in one class.  Used
    only to show that a census counts what a wrong partition would
    produce; the rectangle never sees it."""

    def key(self, regime: Regime) -> CanonKey:
        return self.brute(EMPTY)


def nodes(root: Regime, *histories: tuple[Event, ...]) -> list[tuple[tuple[Event, ...], Regime]]:
    """Every prefix of every history, the empty one included, with the
    regime it reaches from ``root``."""
    seen: dict[tuple[Event, ...], Regime] = {(): root}
    for history in histories:
        for k in range(1, len(history) + 1):
            seen[history[:k]] = replay(history[:k], root)
    return sorted(seen.items(), key=lambda item: len(item[0]))


class ReceiptTests(unittest.TestCase):
    def test_the_committed_receipt_is_a_fresh_run(self) -> None:
        committed = RECEIPT.read_bytes().replace(b"\r\n", b"\n")
        self.assertEqual(committed, rp.render(payload()))

    def test_the_receipt_is_stored_with_no_carriage_return(self) -> None:
        self.assertNotIn(b"\r", RECEIPT.read_bytes())

    def test_the_receipt_carries_no_forbidden_key(self) -> None:
        self.assertEqual(rp.forbidden_keys(payload()), [])

    def test_a_forbidden_key_is_named_at_any_depth(self) -> None:
        probe = {"a": [{"b": {"Timestamp": 1}}], "host": "x"}
        self.assertEqual(sorted(rp.forbidden_keys(probe)), ["a[0].b.Timestamp", "host"])

    def test_the_frozen_digests_are_the_manifest_ones(self) -> None:
        manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
        frozen = {item["path"].split("/")[-1]: item["sha256"] for item in manifest["frozen_texts"]}
        self.assertEqual(payload()["prompt_sha256"], frozen["PROMPT.md"])
        self.assertEqual(payload()["predictions_sha256"], frozen["PREDICTIONS.md"])

    def test_check_passes_and_writes_nothing(self) -> None:
        before = RECEIPT.read_bytes()
        self.assertEqual(rp.main(["--check"]), 0)
        self.assertEqual(RECEIPT.read_bytes(), before)

    def test_check_refuses_a_drifted_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / rp.RECEIPT_NAME
            drifted = RECEIPT.read_bytes().replace(b'"situations": 68', b'"situations": 69')
            self.assertNotEqual(drifted, RECEIPT.read_bytes())
            target.write_bytes(drifted)
            with CachedBuild():
                self.assertEqual(rp.main(["--check", "--receipts", tmp]), 1)

    def test_check_refuses_a_missing_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, CachedBuild():
            self.assertEqual(rp.main(["--check", "--receipts", tmp]), 1)

    def test_a_run_writes_the_same_bytes_elsewhere(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(rp.main(["--receipts", tmp]), 0)
            written = (pathlib.Path(tmp) / rp.RECEIPT_NAME).read_bytes()
            self.assertEqual(written, RECEIPT.read_bytes().replace(b"\r\n", b"\n"))

    def test_an_oversize_receipt_is_refused(self) -> None:
        saved = rp.MEGABYTE
        rp.MEGABYTE = 10
        try:
            with tempfile.TemporaryDirectory() as tmp, CachedBuild():
                self.assertEqual(rp.main(["--receipts", tmp]), 1)
        finally:
            rp.MEGABYTE = saved

    def test_a_forbidden_key_in_the_payload_is_refused(self) -> None:
        saved = rp.build
        tainted = dict(payload(), timestamp="x")
        rp.build = lambda: tainted
        try:
            with tempfile.TemporaryDirectory() as tmp:
                self.assertEqual(rp.main(["--receipts", tmp]), 1)
        finally:
            rp.build = saved


class ScoringTests(unittest.TestCase):
    def test_the_scored_verdicts_are_the_dated_ones(self) -> None:
        """Dated 2026-09-25 in STATUS.md: eleven computational hits, one
        miss (R-11), twelve rows scored elsewhere."""
        scored = payload()["predictions_scored"]
        verdicts = {pid: row["verdict"] for pid, row in scored.items()}
        self.assertEqual(
            sorted(pid for pid, v in verdicts.items() if v == "HIT"),
            sorted(["R-9", "R-10", "R-12", "R-13", "R-14", "R-15", "R-16", "R-17",
                    "R-18", "R-19", "R-20"]),
        )
        self.assertEqual(sorted(pid for pid, v in verdicts.items() if v == "MISSED"), ["R-11"])
        self.assertEqual(sum(1 for v in verdicts.values() if v == "ELSEWHERE"), 12)
        self.assertEqual(len(verdicts), 24)

    def test_the_miss_is_recorded_with_its_value(self) -> None:
        """R-11 predicted a refusal at L and at F; none is refused at any
        base, under either measure, and the two measures agree."""
        value = payload()["predictions_scored"]["R-11"]["value"]
        self.assertEqual(value["refused"], {m: {"EMPTY": 0, "L": 0, "F": 0} for m in rr.MEASURES})
        self.assertEqual(value["refusal_disagreements"], {"EMPTY": 0, "L": 0, "F": 0})

    def test_the_missed_row_could_have_hit(self) -> None:
        """NEGATIVE, in the other direction: R-11 is not a constant miss."""
        reports = copy.deepcopy(payload()["reports"])
        for base in ("L", "F"):
            for m in rr.MEASURES:
                reports["bases"][base]["measures"][m]["refused"] = 1
        self.assertEqual(rp.score(reports)["R-11"]["verdict"], "HIT")

    def test_every_hit_row_can_miss(self) -> None:
        """NEGATIVE: each hit row turns to a miss when its value is moved,
        so a HIT is not a constant."""
        reports = payload()["reports"]

        def measure(base: str, m: str, key: str, value: object) -> Callable[[dict[str, Any]], None]:
            return lambda r: r["bases"][base]["measures"][m].__setitem__(key, value)

        def flatten_mu2(r: dict[str, Any]) -> None:
            for b in ("EMPTY", "L", "F"):
                r["bases"][b]["measures"]["mu2"]["largest_finite_distance"] = 1

        movers: dict[str, list[Callable[[dict[str, Any]], None]]] = {
            "R-9": [lambda r: r["classes"].__setitem__("key_brute_disagreements", 1),
                    lambda r: r["bases"]["L"].__setitem__("sequences", 1)],
            "R-10": [lambda r: r["bases"]["EMPTY"].__setitem__("regimes_outside_domain", 0),
                     lambda r: r["bases"]["F"].__setitem__("inside_domain_with_rules", 1)],
            "R-12": [measure("L", "mu1", "responses_with_rule_item", 1),
                     measure("F", "mu2", "responses_moving_an_unmentioned_pair", 1)],
            "R-13": [measure("EMPTY", "mu1", "responses_moving_a_pair_together", 1),
                     measure("L", "mu2", "responses_moving_a_pair_together", 0),
                     measure("F", "mu1", "responses_not_moving_their_demand_apart", 1)],
            "R-14": [measure("L", "mu1", "reach_class_violations", 1),
                     measure("EMPTY", "mu2", "responses_with_empty_reach", 0)],
            "R-15": [measure("L", "mu1", "least_length_with_an_edge", 2), flatten_mu2],
            "R-16": [measure("EMPTY", "mu2", "least_length_with_two_tie_classes", 2),
                     measure("F", "mu1", "demands_with_tie_count_one", 0),
                     lambda r: r["bases"]["L"]["refinement"].__setitem__("mu2_not_among_mu1", 1)],
            "R-17": [lambda r: r["classes"]["within_base"]["F"].__setitem__(
                "classes_with_two_values_of_signature_mu2", 1)],
            "R-18": [lambda r: r["exhaustion_changes_over_all_bases"].__setitem__("Impose", [0, 1]),
                     lambda r: r["bases"]["L"]["exhaustion"].__setitem__("holds_two_mismatches", 1)],
            "R-19": [lambda r: r["bases"]["EMPTY"]["exhaustion"].__setitem__(
                "least_length_holding_two_with_an_exhausted_form", 4)],
            "R-20": [lambda r: r["crosscheck_empty_base"].__setitem__("response_disagreements", 1),
                     measure("F", "mu1", "reference_validity_failures", 1)],
        }
        for pid, moves in movers.items():
            for move in moves:
                moved = copy.deepcopy(reports)
                move(moved)
                self.assertEqual(rp.score(moved)[pid]["verdict"], "MISSED", pid)


class ExhaustionTests(unittest.TestCase):
    """Exhaustion on regimes short enough to read by hand."""

    def test_a_form_with_no_instance_is_exhausted(self) -> None:
        r = regime(*THREE)
        self.assertFalse(rr.distinguishes(r, 0))
        self.assertEqual(rr.exhausted_count(r), 1)
        self.assertFalse(rr.holds_two(r))

    def test_an_instance_on_one_datum_distinguishes(self) -> None:
        r = regime(*THREE, AdmitInst(0, (0,)))
        self.assertTrue(rr.distinguishes(r, 0))
        self.assertEqual(rr.exhausted_count(r), 0)
        self.assertTrue(rr.holds_two(r))

    def test_a_rule_exhausts_its_form(self) -> None:
        r = regime(*THREE, AdmitInst(0, (0,)), AdmitRuleAll(0))
        self.assertEqual(rr.exhausted_count(r), 1)

    def test_a_datum_can_end_exhaustion(self) -> None:
        """The Lean exhibit `exhaustion_ended_by_datum`."""
        one = regime(AdmitDatum(N[0]), AdmitForm(1), AdmitInst(0, (0,)))
        self.assertEqual(rr.exhausted_count(one), 1)
        self.assertEqual(rr.exhausted_count(replay((AdmitDatum(N[1]),), one)), 0)

    def test_a_small_exhaustion_report_by_hand(self) -> None:
        root = regime(*THREE)
        rows = nodes(root, (AdmitInst(0, (0,)), AdmitInst(0, (1,)), AdmitInst(0, (2,))),
                     (AdmitRuleAll(0),), (Supply("<z>"),), (AdmitForm(2),))
        counts = {r: rr.exhausted_count(r) for _, r in rows}
        report = rr.exhaustion_report(rows, counts)
        self.assertEqual(report["changes_by_kind"], {
            "AdmitForm": [1], "AdmitInst": [-1, 0, 1], "AdmitRuleAll": [0], "Supply": [0],
        })
        self.assertEqual(report["least_length_with_an_exhausted_form"], 0)
        self.assertEqual(report["least_length_holding_two_with_an_exhausted_form"], None)
        self.assertEqual(report["holds_two_mismatches"], 0)
        self.assertEqual(report["ruled_forms_distinguishing"], 0)

    def test_a_forged_count_is_a_mismatch(self) -> None:
        """NEGATIVE: an exhausted count that contradicts holding two is
        counted."""
        r = regime(*THREE, AdmitInst(0, (0,)))
        report = rr.exhaustion_report([((), r)], {r: 1})
        self.assertEqual(report["holds_two_mismatches"], 1)


class ResponderTests(unittest.TestCase):
    """The sealed responder, read on regimes short enough to read by hand."""

    def test_the_domain_is_the_rule_free_regimes(self) -> None:
        self.assertTrue(rr.in_domain(regime(*THREE)))
        self.assertFalse(rr.in_domain(regime(*THREE, AdmitRuleAll(0))))
        responder = rr.Responder()
        ruled = regime(*THREE, AdmitRuleAll(0))
        self.assertEqual(rr.signature(ruled, "mu1", responder), (False,))
        self.assertFalse(responder.domain(ruled))

    def test_the_lean_exhibits_in_the_python_grammar(self) -> None:
        """Recorded, not scored: one instance moves two pairs apart; on the
        other regime it moves one apart and one together."""
        report = rr.lean_witnesses()
        self.assertEqual(report["one_inst_moves_two_pairs"], [[[0, 1], True], [[0, 2], True]])
        self.assertEqual(report["response_collapses_a_pair"], [[[0, 1], True], [[0, 2], False]])

    def test_a_demand_among_three_collapsed_data(self) -> None:
        """Demand (0, 1) among three collapsed data and one form of arity
        one: the two responses are the instance at either demanded datum;
        each moves the demand and the pair with the third datum, so the
        third datum is in the reach; the two are one tie class."""
        responder = rr.Responder()
        r = regime(*THREE)
        ans = responder.answer(r, (0, 1), "mu1")
        self.assertEqual(ans.cost, (1, -1))
        self.assertEqual({resp.delta for resp in ans.responses},
                         {(NewInst(0, (0,)),), (NewInst(0, (1,)),)})
        for resp in ans.responses:
            self.assertEqual(resp.reach, frozenset({2}))
            self.assertEqual(len(resp.moved), 2)
        self.assertEqual(ans.tie_classes(), 1)
        self.assertIs(responder.answer(r, (0, 1), "mu1"), ans)

    def test_the_two_measures_part_at_two_items(self) -> None:
        """Two collapsed data and no form: every response is a new form and
        one instance on it.  Under mu1 the arity-two forms tie with the
        arity-one form; mu2 keeps only arity one."""
        responder = rr.Responder()
        r = regime(AdmitDatum(N[0]), AdmitDatum(N[1]))
        one = responder.answer(r, (0, 1), "mu1")
        two = responder.answer(r, (0, 1), "mu2")
        self.assertEqual(one.cost, (2, -1))
        self.assertEqual(two.cost, (2, 1))
        self.assertEqual({resp.delta for resp in two.responses},
                         {(NewForm(1), NewInst(0, (0,))), (NewForm(1), NewInst(0, (1,)))})
        self.assertLess({resp.delta for resp in two.responses},
                        {resp.delta for resp in one.responses})
        self.assertEqual(one.tie_classes(), 3)
        self.assertEqual(two.tie_classes(), 1)

    def test_a_refused_demand(self) -> None:
        """Four data and a requirement on every pair: no response of at most
        two items separates all six, so every demand is refused, by the
        sealed responder and by the unpruned reference alike."""
        responder = rr.Responder()
        r = regime(*REFUSING)
        for m in rr.MEASURES:
            ans = responder.answer(r, (0, 1), m)
            self.assertIsNone(ans.cost)
            self.assertEqual(ans.responses, ())
            self.assertIsNone(rr.unpruned(r, (0, 1), m))
        report = rr.measure_report([((), r)], "mu1", responder)
        self.assertEqual(report["refused"], 6)
        self.assertEqual(report["demands"], 6)
        signature = rr.signature(r, "mu2", responder)
        self.assertEqual(signature[0], True)
        self.assertEqual(signature[1], tuple([((-1, -1), 0, 0, ())] * 6))
        cross = rr.crosscheck([r], responder)
        self.assertEqual(cross["refusal_disagreements"], 0)
        self.assertEqual(cross["situations"], 12)

    def test_the_unpruned_minimum_agrees_by_hand(self) -> None:
        r = regime(*THREE)
        self.assertEqual(rr.unpruned(r, (0, 1), "mu1"),
                         frozenset({(NewInst(0, (0,)),), (NewInst(0, (1,)),)}))
        two = regime(AdmitDatum(N[0]), AdmitDatum(N[1]))
        self.assertEqual(rr.unpruned(two, (0, 1), "mu2"),
                         frozenset({(NewForm(1), NewInst(0, (0,))),
                                    (NewForm(1), NewInst(0, (1,)))}))
        cross = rr.crosscheck([r, two, regime(*THREE, AdmitRuleAll(0))], rr.Responder())
        self.assertEqual(cross, {"situations": 8, "response_disagreements": 0,
                                 "refusal_disagreements": 0, "tie_partition_disagreements": 0})

    def test_mentioned_and_moved_read_the_delta(self) -> None:
        self.assertEqual(rr.mentioned((NewDatum(), NewInst(0, (1, 3)))), frozenset({1, 3}))
        before = regime(*THREE, AdmitInst(0, (2,)))
        after = replay((AdmitInst(0, (0,)),), before)
        self.assertEqual(rr.moved_pairs(before, after), (((0, 1), True), ((0, 2), False)))
        self.assertEqual(rr.moved_pairs(before, before), ())


class AdjacencyTests(unittest.TestCase):
    def _answer(self, *moved: tuple[tuple[int, int], bool]) -> rr.Answer:
        resp = rr.Response((), tuple(moved), frozenset(), canonical(EMPTY), EMPTY)
        return rr.Answer((0, 1), (1, -1), (resp,))

    def test_an_empty_graph(self) -> None:
        self.assertEqual(rr.adjacency(3, []), (0, (1, 1, 1), 0))
        self.assertEqual(rr.adjacency(0, []), (0, (), 0))

    def test_a_path_of_two_edges_has_distance_two(self) -> None:
        """Pairs (0,1)-(0,2) moved by one response and (0,2)-(1,2) by
        another: two edges, one piece of three, distance two between
        (0,1) and (1,2), which no response moves together."""
        answers = [self._answer(((0, 1), True), ((0, 2), True)),
                   self._answer(((0, 2), True), ((1, 2), False))]
        self.assertEqual(rr.adjacency(3, answers), (2, (3,), 2))

    def test_a_triangle_has_distance_one(self) -> None:
        answers = [self._answer(((0, 1), True), ((0, 2), True), ((1, 2), True))]
        self.assertEqual(rr.adjacency(3, answers), (3, (3,), 1))


class ForgedResponder(rr.Responder):
    """A FORGED responder, used only to show that each census of
    `measure_report`, `refinement_violations` and `crosscheck` COUNTS the
    defect it exists to catch.  Under `mu1` it refuses every demand; under
    `mu2` it returns two forged responses: a lone rule item that moves an
    unmentioned pair together and claims a reach it cannot have, and one
    of empty reach, each with its own tie key over one regime."""

    def answer(self, regime: Regime, target: tuple[int, int], measure: str) -> rr.Answer:
        if measure == "mu1":
            return rr.Answer(target, None, ())
        imposed = replay((Impose(*target),), regime)
        loud = rr.Response((NewRuleAll(0),), (((1, 2), False),), frozenset({2}),
                           canonical(EMPTY), imposed)
        quiet = rr.Response((NewInst(0, (0,)),), (), frozenset(), canonical(imposed), imposed)
        return rr.Answer(target, (1, 0), (loud, quiet))


class ForgedCensusTests(unittest.TestCase):
    """NEGATIVE: every violation the rectangle reports as zero is counted
    when it is there."""

    def setUp(self) -> None:
        self.r = regime(*THREE)
        self.rows = [((), self.r)]

    def test_every_response_census_counts_a_forged_response(self) -> None:
        report = rr.measure_report(self.rows, "mu2", ForgedResponder())
        for key in ("reference_validity_failures", "responses_with_rule_item",
                    "responses_mentioning_no_demanded_datum",
                    "responses_moving_an_unmentioned_pair",
                    "responses_not_moving_their_demand_apart",
                    "responses_moving_a_pair_together", "reach_two_pair_mismatches",
                    "reach_class_violations"):
            self.assertGreater(report[key], 0, key)
        self.assertEqual(report["responses"], 6)

    def test_the_refinement_census_counts_a_forged_split(self) -> None:
        self.assertEqual(rr.refinement_violations(self.rows, ForgedResponder()),
                         {"refusal_disagreements": 3, "mu2_not_among_mu1": 3})

    def test_the_crosscheck_counts_a_forged_answer(self) -> None:
        cross = rr.crosscheck([self.r], ForgedResponder())
        self.assertEqual(cross["refusal_disagreements"], 3)
        self.assertEqual(cross["response_disagreements"], 3)
        self.assertEqual(cross["tie_partition_disagreements"], 3)

    def test_a_distinguishing_ruled_form_would_be_counted(self) -> None:
        ruled = regime(*THREE, AdmitRuleAll(0))
        saved = rr.distinguishes
        rr.distinguishes = lambda regime, form: True
        try:
            report = rr.exhaustion_report([((), ruled)], {ruled: 1})
        finally:
            rr.distinguishes = saved
        self.assertEqual(report["ruled_forms_distinguishing"], 1)


class ReportTests(unittest.TestCase):
    def test_a_small_measure_report_by_hand(self) -> None:
        """From three collapsed data and a form: the base has three
        demands, each answered at one item by two responses of reach one;
        after an instance at datum two, one demand is left, (0, 1), whose
        responses move (0, 2) together or apart."""
        root = regime(*THREE)
        rows = nodes(root, (AdmitInst(0, (2,)),), (AdmitRuleAll(0),))
        responder = rr.Responder()
        report = rr.measure_report(rows, "mu1", responder)
        self.assertEqual(report["regimes_in_domain"], 2)
        self.assertEqual(report["demands"], 4)
        self.assertEqual(report["refused"], 0)
        self.assertEqual(report["answered_by_cost"], {"1": 4})
        self.assertEqual(report["responses_with_rule_item"], 0)
        self.assertEqual(report["responses_moving_an_unmentioned_pair"], 0)
        self.assertEqual(report["responses_moving_a_pair_together"], 2)
        self.assertEqual(report["least_length_with_an_edge"], 0)
        self.assertEqual(report["reach_class_violations"], 0)
        self.assertEqual(report["reach_two_pair_mismatches"], 0)
        self.assertEqual(report["reference_validity_failures"], 0)
        self.assertEqual(rr.refinement_violations(rows, responder),
                         {"refusal_disagreements": 0, "mu2_not_among_mu1": 0})

    def test_a_regime_with_one_datum_has_no_demand(self) -> None:
        responder = rr.Responder()
        rows = nodes(EMPTY, (AdmitDatum(N[0]),))
        report = rr.measure_report(rows, "mu2", responder)
        self.assertEqual(report["demands"], 0)
        self.assertIsNone(report["least_length_with_an_edge"])
        self.assertIsNone(report["least_length_with_two_tie_classes"])


class ClassReportTests(unittest.TestCase):
    """NEGATIVE: the class censuses count a forged partition."""

    def _population(self, keys: Keys) -> Population:
        empty_nodes = nodes(EMPTY, THREE + (AdmitInst(0, (0,)),))
        rects = (
            Rectangle("EMPTY", EMPTY, tuple(Node(h, r, 0) for h, r in empty_nodes), 0, 0),
        )
        regimes = tuple(sorted({r for _, r in empty_nodes},
                               key=lambda x: (x.n_data(), x.forms, len(x.insts))))
        return Population(rects, regimes, keys)

    def test_the_true_partition_lumps_nothing(self) -> None:
        population = self._population(Keys())
        counts = {r: rr.exhausted_count(r) for r in population.regimes}
        report = rr.class_report(population, counts, rr.Responder())
        for row in list(report["within_base"].values()) + [report["over_all_bases"]]:
            for key, value in row.items():
                if key.startswith("classes_with_two_values_of_"):
                    self.assertEqual(value, 0, key)
        self.assertEqual(report["key_brute_disagreements"], 0)
        self.assertEqual(report["distinct_regimes_over_all_bases"], 6)

    def test_a_lumping_partition_is_counted_everywhere(self) -> None:
        population = self._population(LumpingKeys())
        counts = {r: rr.exhausted_count(r) for r in population.regimes}
        report = rr.class_report(population, counts, rr.Responder())
        for row in list(report["within_base"].values()) + [report["over_all_bases"]]:
            self.assertEqual(row["classes"], 1)
            self.assertEqual(row["classes_with_two_values_of_exhausted_count"], 1)
            self.assertEqual(row["classes_with_two_values_of_signature_mu1"], 1)
            self.assertEqual(row["classes_with_two_values_of_signature_mu2"], 1)
        self.assertGreater(report["key_brute_disagreements"], 0)


class RectangleTests(unittest.TestCase):
    def test_the_rectangle_is_rung_three_s(self) -> None:
        reports = payload()["reports"]
        bases = reports["bases"]
        self.assertEqual(
            {b: bases[b]["sequences"] for b in bases}, {"EMPTY": 577, "L": 3928, "F": 14293}
        )
        self.assertEqual(
            {b: bases[b]["distinct_regimes"] for b in bases}, {"EMPTY": 75, "L": 523, "F": 1718}
        )
        self.assertEqual({b: bases[b]["replay_mismatches"] for b in bases},
                         {"EMPTY": 0, "L": 0, "F": 0})
        self.assertEqual(reports["classes"]["distinct_regimes_over_all_bases"], 2316)

    def test_the_domain_counts_are_the_dated_ones(self) -> None:
        """Dated 2026-09-25 in STATUS.md."""
        bases = payload()["reports"]["bases"]
        self.assertEqual({b: bases[b]["regimes_in_domain"] for b in bases},
                         {"EMPTY": 47, "L": 402, "F": 1441})
        self.assertEqual({b: bases[b]["regimes_outside_domain"] for b in bases},
                         {"EMPTY": 28, "L": 121, "F": 277})

    def test_the_response_counts_are_the_dated_ones(self) -> None:
        """Dated 2026-09-25 in STATUS.md."""
        bases = payload()["reports"]["bases"]
        table = {
            (b, m): (row["demands"], row["responses"], row["largest_tie_class_count"],
                     row["largest_reach"], row["largest_finite_distance"],
                     row["responses_moving_a_pair_together"])
            for b in bases for m, row in bases[b]["measures"].items()
        }
        self.assertEqual(table, {
            ("EMPTY", "mu1"): (34, 270, 5, 2, 1, 0),
            ("EMPTY", "mu2"): (34, 100, 4, 2, 2, 0),
            ("L", "mu1"): (597, 5136, 8, 3, 2, 114),
            ("L", "mu2"): (597, 3276, 8, 3, 2, 114),
            ("F", "mu1"): (2479, 21876, 16, 3, 2, 1152),
            ("F", "mu2"): (2479, 17986, 16, 3, 2, 1152),
        })

    def test_no_distance_above_two_within_the_bound(self) -> None:
        """Recorded beside R-15, which asked for at least two: no adjacency
        graph of the rectangle has a finite distance above two."""
        bases = payload()["reports"]["bases"]
        for b in bases:
            for m in rr.MEASURES:
                self.assertLessEqual(bases[b]["measures"][m]["largest_finite_distance"], 2)


if __name__ == "__main__":
    unittest.main()
