"""Tests of the rung-five cross-check and its runner.

Three kinds, kept apart:

* the receipt: it regenerates byte-identically, `--check` writes nothing
  and refuses drift, and it carries no temporal or environment key;
* the pieces of `symmetry.py`, each on a regime small enough to read by
  hand, so a law checked over the rectangle is also checked where its
  value is known;
* NEGATIVE tests: each law of the edge report is fed a forged edge and
  must COUNT a violation, so a report of zero violations is not a report
  of a check that cannot fire.
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

import symmetry as sy  # noqa: E402

# `symmetry` puts sibling trees on the path and each of them carries its
# own `run_*`, `verify_pins` and `test_*`; this tree goes back to the front
# first.  See the note in `symmetry.py`.
if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))
import run_symmetry as rs  # noqa: E402

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
    step,
)
from nofirst import Alphabet, Node  # noqa: E402
from index import Rectangle  # noqa: E402
from iso_index import Keys, Population  # noqa: E402

RECEIPT = HERE / "receipts" / rs.RECEIPT_NAME
_PAYLOAD: dict[str, Any] | None = None


def payload() -> dict[str, Any]:
    """One build per test run; the rectangle is the expensive part."""
    global _PAYLOAD
    if _PAYLOAD is None:
        _PAYLOAD = rs.build()
    return _PAYLOAD


def regime(*events: Event) -> Regime:
    return replay(tuple(events), EMPTY)


N = sy.ALPHABET.fresh_tokens


class ReceiptTests(unittest.TestCase):
    def test_the_committed_receipt_is_a_fresh_run(self) -> None:
        committed = RECEIPT.read_bytes().replace(b"\r\n", b"\n")
        self.assertEqual(committed, rs.render(payload()))

    def test_the_receipt_is_stored_with_no_carriage_return(self) -> None:
        self.assertNotIn(b"\r", RECEIPT.read_bytes())

    def test_the_receipt_carries_no_forbidden_key(self) -> None:
        self.assertEqual(rs.forbidden_keys(payload()), [])

    def test_a_forbidden_key_is_named_at_any_depth(self) -> None:
        probe = {"a": [{"b": {"Timestamp": 1}}], "host": "x"}
        self.assertEqual(sorted(rs.forbidden_keys(probe)), ["a[0].b.Timestamp", "host"])

    def test_the_frozen_digests_are_the_manifest_ones(self) -> None:
        manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
        frozen = {item["path"].split("/")[-1]: item["sha256"] for item in manifest["frozen_texts"]}
        self.assertEqual(payload()["prompt_sha256"], frozen["PROMPT.md"])
        self.assertEqual(payload()["predictions_sha256"], frozen["PREDICTIONS.md"])

    def test_check_passes_and_writes_nothing(self) -> None:
        before = RECEIPT.read_bytes()
        self.assertEqual(rs.main(["--check"]), 0)
        self.assertEqual(RECEIPT.read_bytes(), before)

    def test_check_refuses_a_drifted_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / rs.RECEIPT_NAME
            target.write_bytes(RECEIPT.read_bytes().replace(b'"largest": 240', b'"largest": 241'))
            self.assertEqual(rs.main(["--check", "--receipts", tmp]), 1)

    def test_check_refuses_a_missing_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(rs.main(["--check", "--receipts", tmp]), 1)

    def test_a_run_writes_the_same_bytes_elsewhere(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(rs.main(["--receipts", tmp]), 0)
            written = (pathlib.Path(tmp) / rs.RECEIPT_NAME).read_bytes()
            self.assertEqual(written, RECEIPT.read_bytes().replace(b"\r\n", b"\n"))

    def test_an_oversize_receipt_is_refused(self) -> None:
        saved = rs.MEGABYTE
        rs.MEGABYTE = 10
        try:
            with tempfile.TemporaryDirectory() as tmp:
                self.assertEqual(rs.main(["--receipts", tmp]), 1)
        finally:
            rs.MEGABYTE = saved

    def test_a_forbidden_key_in_the_payload_is_refused(self) -> None:
        saved = rs.build
        tainted = dict(payload(), timestamp="x")
        rs.build = lambda: tainted
        try:
            with tempfile.TemporaryDirectory() as tmp:
                self.assertEqual(rs.main(["--receipts", tmp]), 1)
        finally:
            rs.build = saved


class ScoringTests(unittest.TestCase):
    def test_the_scored_verdicts_are_the_dated_ones(self) -> None:
        """Dated 2026-09-25 in STATUS.md: eight computational hits and one
        miss, K-14, recorded next to its value."""
        scored = payload()["predictions_scored"]
        verdicts = {pid: row["verdict"] for pid, row in scored.items()}
        self.assertEqual(
            sorted(pid for pid, v in verdicts.items() if v == "HIT"),
            ["K-10", "K-11", "K-12", "K-13", "K-15", "K-16", "K-17"],
        )
        self.assertEqual(sorted(pid for pid, v in verdicts.items() if v == "MISSED"), ["K-14"])
        self.assertEqual(sum(1 for v in verdicts.values() if v == "ELSEWHERE"), 12)
        self.assertEqual(
            scored["K-14"]["value"]["largest_fall"], {"kinds": ["AdmitInst"], "ratio": "24"}
        )
        self.assertEqual(
            scored["K-14"]["value"]["largest_rise"], {"kinds": ["AdmitDatum"], "ratio": "5"}
        )

    def test_every_computational_row_can_miss(self) -> None:
        """NEGATIVE: each hit row turns to a miss when its value is moved,
        so a HIT is not a constant."""
        reports = payload()["reports"]
        movers: dict[str, Callable[[dict[str, Any]], None]] = {
            "K-10": lambda r: r.__setitem__("replay_mismatches", 1),
            "K-11": lambda r: r["edges"]["by_kind"]["AdmitDatum"]["changing"].__setitem__("down", 1),
            "K-12": lambda r: r["edges"]["datum_law"].__setitem__("violations", 1),
            "K-13": lambda r: r["edges"]["meet_law"].__setitem__("ratio_violations", 1),
            "K-15": lambda r: r["sequences"]["classes_by_base"]["EMPTY"].__setitem__("FALLING", 1),
            "K-16": lambda r: r["sequences"].__setitem__("class_revisits_after_a_changing_event", 1),
            "K-17": lambda r: r["automorphisms"].__setitem__("largest", 24),
        }
        for pid, move in movers.items():
            moved = copy.deepcopy(reports)
            move(moved)
            self.assertEqual(rs.score(moved)[pid]["verdict"], "MISSED", pid)
        fixed = copy.deepcopy(reports)
        fixed["edges"]["largest_fall"] = {"ratio": "20", "kinds": ["AdmitInst"]}
        self.assertEqual(rs.score(fixed)["K-14"]["verdict"], "HIT")

    def test_no_mixed_sequence_scores_as_a_miss(self) -> None:
        reports = copy.deepcopy(payload()["reports"])
        reports["sequences"]["shortest_mixed"] = None
        self.assertEqual(rs.score(reports)["K-15"]["verdict"], "MISSED")


class RectangleTests(unittest.TestCase):
    def test_the_rectangle_is_rung_three_s(self) -> None:
        bases = payload()["reports"]["bases"]
        self.assertEqual(
            {b: bases[b]["sequences"] for b in bases}, {"EMPTY": 577, "L": 3928, "F": 14293}
        )
        self.assertEqual(payload()["reports"]["edges"]["edges"], 18795)

    def test_every_edge_is_counted_once_by_kind(self) -> None:
        by_kind = payload()["reports"]["edges"]["by_kind"]
        total = sum(
            by_kind[k][s][d] for k in by_kind for s in by_kind[k] for d in by_kind[k][s]
        )
        self.assertEqual(total, 18795)

    def test_the_three_adding_kinds_move_both_ways(self) -> None:
        by_kind = payload()["reports"]["edges"]["by_kind"]
        for kind in sy.ADDING_KINDS:
            self.assertGreater(by_kind[kind]["changing"]["up"], 0, kind)
            self.assertGreater(by_kind[kind]["changing"]["down"], 0, kind)
        for kind in ("AdmitDatum", "AdmitForm"):
            self.assertEqual(by_kind[kind]["changing"]["down"], 0, kind)

    def test_the_lean_witnesses_replay(self) -> None:
        witnesses = payload()["reports"]["lean_witnesses"]
        self.assertEqual(len(witnesses), 6)
        for name, row in witnesses.items():
            self.assertTrue(row["claim_holds"], name)
            shape = row["regime_before"]
            self.assertLessEqual(shape["data"], 3, name)
            self.assertLessEqual(shape["forms"], 2, name)


class PieceTests(unittest.TestCase):
    def test_untouched_data_and_forms(self) -> None:
        r = regime(AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitDatum(N[2]),
                   AdmitForm(1), AdmitForm(1), AdmitForm(2),
                   AdmitInst(0, (0,)), Supply("<z>"))
        self.assertEqual(sy.untouched_data(r), 2)
        self.assertEqual(sy.untouched_forms(r, 1), 1)
        self.assertEqual(sy.untouched_forms(r, 2), 1)
        r2 = step(step(r, Impose(1, 2)), AdmitRuleAll(1))
        self.assertEqual(sy.untouched_data(r2), 0)
        self.assertEqual(sy.untouched_forms(r2, 1), 0)

    def test_added_element_by_kind(self) -> None:
        r = regime(AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitForm(2))
        inst = AdmitInst(0, (1, 0))
        self.assertEqual(sy.added_element(r, inst, step(r, inst)), ("inst", (0, (1, 0))))
        self.assertEqual(sy.added_element(r, AdmitRuleAll(0), step(r, AdmitRuleAll(0))), ("rule", 0))
        self.assertEqual(sy.added_element(r, Impose(0, 1), step(r, Impose(0, 1))), ("req", (0, 1)))
        self.assertIsNone(sy.added_element(r, Supply("<z>"), r))
        grown = step(r, AdmitDatum(N[2]))
        self.assertIsNone(sy.added_element(r, AdmitDatum(N[2]), grown))
        again = step(r, inst)
        self.assertIsNone(sy.added_element(again, inst, step(again, inst)))

    def test_images_by_kind(self) -> None:
        pair = ((2, 0, 1), (1, 0))
        self.assertEqual(sy.image(pair, ("inst", (0, (0, 1)))), (1, (2, 0)))
        self.assertEqual(sy.image(pair, ("rule", 1)), 0)
        self.assertEqual(sy.image(pair, ("req", (0, 1))), (0, 2))

    def test_direction_and_sequence_classes(self) -> None:
        self.assertEqual(sy.direction(1, 2), "up")
        self.assertEqual(sy.direction(2, 1), "down")
        self.assertEqual(sy.direction(2, 2), "equal")
        self.assertEqual(sy.sequence_class([1]), "CONSTANT")
        self.assertEqual(sy.sequence_class([1, 2, 2]), "RISING")
        self.assertEqual(sy.sequence_class([6, 2, 2]), "FALLING")
        self.assertEqual(sy.sequence_class([2, 6, 2]), "MIXED")

    def test_element_count(self) -> None:
        r = regime(AdmitDatum(N[0]), AdmitForm(1), AdmitInst(0, (0,)), AdmitRuleAll(0))
        self.assertEqual(sy.element_count(r), 4)

    def test_sealed_and_brute_sets_agree_where_the_value_is_known(self) -> None:
        """Five untouched data and two untouched unary forms: every
        bijection pair, five factorial times two."""
        r = regime(*(AdmitDatum(t) for t in N), AdmitForm(1), AdmitForm(1))
        auts = sy.Automorphisms()
        self.assertEqual(auts.size(r), 240)
        self.assertEqual(auts.of(r), sy.brute_automorphisms(r))
        self.assertIs(auts.of(r), auts.of(r))


class NegativeLawTests(unittest.TestCase):
    """Each law is fed an edge that breaks it and must count a violation."""

    def setUp(self) -> None:
        self.auts = sy.Automorphisms()
        self.two = regime(AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitForm(1))

    def test_a_forged_datum_edge_violates_the_datum_law(self) -> None:
        after = step(step(self.two, AdmitDatum(N[2])), AdmitInst(0, (2,)))
        edge = sy.Edge("EMPTY", (AdmitDatum(N[2]),), self.two, after)
        report = sy.edge_report([edge], self.auts)
        self.assertEqual(report["datum_law"], {"checked": 1, "violations": 1})
        self.assertEqual(report["element_count_violations"], 1)

    def test_a_forged_form_edge_violates_the_form_law(self) -> None:
        after = step(step(self.two, AdmitForm(1)), AdmitInst(1, (0,)))
        edge = sy.Edge("EMPTY", (AdmitForm(1),), self.two, after)
        report = sy.edge_report([edge], self.auts)
        self.assertEqual(report["form_law"], {"checked": 1, "violations": 1})

    def test_a_forged_adding_edge_violates_the_meet_law(self) -> None:
        """The regime after is reached by a DIFFERENT event, so the common
        set is not the fixer set of the element claimed, and the counts of
        images do not balance the sizes."""
        after = step(self.two, AdmitDatum(N[2]))
        edge = sy.Edge("EMPTY", (AdmitInst(0, (0,)),), self.two, after)
        report = sy.edge_report([edge], self.auts)
        self.assertEqual(report["meet_law"]["set_violations"], 1)
        self.assertEqual(report["meet_law"]["ratio_violations"], 1)

    def test_a_real_adding_edge_keeps_the_meet_law(self) -> None:
        after = step(self.two, AdmitInst(0, (0,)))
        edge = sy.Edge("EMPTY", (AdmitInst(0, (0,)),), self.two, after)
        report = sy.edge_report([edge], self.auts)
        self.assertEqual(report["meet_law"], {"checked": 1, "set_violations": 0, "ratio_violations": 0})
        self.assertEqual(report["largest_fall"], {"ratio": "2", "kinds": ["AdmitInst"]})


class SmallRectangleTests(unittest.TestCase):
    def test_a_one_event_rectangle_has_no_mixed_sequence(self) -> None:
        """A declared alphabet of one event per sequence: no sequence can
        both rise and fall, so the shortest MIXED witness is absent, and
        the report says so rather than inventing one."""
        tiny = Alphabet(
            supply_token="<z>", fresh_tokens=(N[0],), arities=(1,),
            max_data=5, max_forms=1, max_length=1,
        )
        reports = sy.all_reports(tiny)
        self.assertIsNone(reports["sequences"]["shortest_mixed"])
        self.assertEqual(reports["replay_mismatches"], 0)
        self.assertEqual(reports["sequences"]["class_revisits_after_a_changing_event"], 0)


class ForgedPopulationTests(unittest.TestCase):
    """NEGATIVE: the cross-checks that report zero over the rectangle are
    fed a population or a procedure built to break them, and must count."""

    def forged(self) -> Population:
        """A root, one changing event, then a node whose recorded regime is
        a renaming of its parent's: a return to the parent's class by a
        changing edge, and a node that does not replay from its history."""
        root = regime(AdmitDatum("<a>"), AdmitDatum("<b>"))
        first = step(root, AdmitForm(1))
        back = regime(AdmitDatum("<c>"), AdmitDatum("<d>"), AdmitForm(1))
        nodes = (
            Node((), root, 0),
            Node((AdmitForm(1),), first, 0),
            Node((AdmitForm(1), AdmitInst(0, (0,))), back, 0),
        )
        rect = Rectangle("EMPTY", root, nodes, 0, 0)
        return Population((rect,), (root, first, back), Keys())

    def test_a_forged_return_to_a_class_is_counted(self) -> None:
        report = sy.sequence_report(self.forged(), sy.Automorphisms())
        self.assertEqual(report["class_revisits_after_a_changing_event"], 1)

    def test_a_forged_replay_mismatch_is_counted(self) -> None:
        forged = self.forged()
        saved = sy.build_population
        sy.build_population = lambda alphabet=sy.ALPHABET: forged
        try:
            reports = sy.all_reports()
        finally:
            sy.build_population = saved
        self.assertEqual(reports["replay_mismatches"], 1)

    def test_a_tampered_automorphism_procedure_is_caught_both_ways(self) -> None:
        class Tampered(sy.Automorphisms):
            def of(self, regime: Regime) -> frozenset[sy.Pair]:
                return frozenset(list(super().of(regime))[:1])

        population = self.forged()
        report = sy.automorphism_crosscheck(population, Tampered())
        self.assertEqual(report["set_disagreements"], 3)
        self.assertEqual(report["count_disagreements"], 3)


if __name__ == "__main__":
    unittest.main()
