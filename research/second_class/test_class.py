"""Tests of the rung-eight cross-check and its runner.

A hand copy of the shape of `research/second_duration/test_duration.py`,
with this rung's pieces.  Three kinds, kept apart:

* the receipt: it regenerates byte-identically, `--check` writes nothing
  and refuses drift, and it carries no temporal or environment key;
* the pieces of `class_count.py`, each on a history short enough to read
  by hand, so a quantity checked over the rectangle is also checked where
  its value is known;
* NEGATIVE tests: each census of the report is fed a forged key procedure
  or a forged population and must COUNT what it was built to count, and
  each scored row is moved and must change its verdict, so a report of
  zero returns is not a report of a check that cannot fire.
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

import class_count as cc  # noqa: E402

# `class_count` puts sibling trees on the path and each of them carries
# its own `run_*`, `verify_pins` and `test_*`; this tree goes back to the
# front first.  See the note in `class_count.py`.
if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))
import run_class as rc  # noqa: E402

from derivation.iso import CanonKey  # noqa: E402
from derivation.model import (  # noqa: E402
    EMPTY,
    AdmissionError,
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
from index import Rectangle  # noqa: E402
from iso_index import Keys, Population  # noqa: E402
from nofirst import Node  # noqa: E402

RECEIPT = HERE / "receipts" / rc.RECEIPT_NAME
_PAYLOAD: dict[str, Any] | None = None


def payload() -> dict[str, Any]:
    """One build per test run; the rectangle is the expensive part."""
    global _PAYLOAD
    if _PAYLOAD is None:
        _PAYLOAD = rc.build()
    return _PAYLOAD


def regime(*events: Event) -> Regime:
    return replay(tuple(events), EMPTY)


N = cc.ALPHABET.fresh_tokens


class LumpingKeys(Keys):
    """A FORGED key procedure that puts every regime in one class.  Used
    only to show that a census counts what a wrong partition would
    produce; the rectangle never sees it."""

    def key(self, regime: Regime) -> CanonKey:
        return self.brute(EMPTY)


def rectangle(base: str, root: Regime, *histories: tuple[Event, ...]) -> Rectangle:
    nodes = tuple(Node(h, replay(h, root), 0) for h in ((),) + histories)
    return Rectangle(base, root, nodes, 0, 0)


class ReceiptTests(unittest.TestCase):
    def test_the_committed_receipt_is_a_fresh_run(self) -> None:
        committed = RECEIPT.read_bytes().replace(b"\r\n", b"\n")
        self.assertEqual(committed, rc.render(payload()))

    def test_the_receipt_is_stored_with_no_carriage_return(self) -> None:
        self.assertNotIn(b"\r", RECEIPT.read_bytes())

    def test_the_receipt_carries_no_forbidden_key(self) -> None:
        self.assertEqual(rc.forbidden_keys(payload()), [])

    def test_a_forbidden_key_is_named_at_any_depth(self) -> None:
        probe = {"a": [{"b": {"Timestamp": 1}}], "host": "x"}
        self.assertEqual(sorted(rc.forbidden_keys(probe)), ["a[0].b.Timestamp", "host"])

    def test_the_frozen_digests_are_the_manifest_ones(self) -> None:
        manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
        frozen = {item["path"].split("/")[-1]: item["sha256"] for item in manifest["frozen_texts"]}
        self.assertEqual(payload()["prompt_sha256"], frozen["PROMPT.md"])
        self.assertEqual(payload()["predictions_sha256"], frozen["PREDICTIONS.md"])

    def test_check_passes_and_writes_nothing(self) -> None:
        before = RECEIPT.read_bytes()
        self.assertEqual(rc.main(["--check"]), 0)
        self.assertEqual(RECEIPT.read_bytes(), before)

    def test_check_refuses_a_drifted_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / rc.RECEIPT_NAME
            drifted = RECEIPT.read_bytes().replace(
                b'"classes_at_more_than_one_base": 86', b'"classes_at_more_than_one_base": 87'
            )
            self.assertNotEqual(drifted, RECEIPT.read_bytes())
            target.write_bytes(drifted)
            self.assertEqual(rc.main(["--check", "--receipts", tmp]), 1)

    def test_check_refuses_a_missing_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(rc.main(["--check", "--receipts", tmp]), 1)

    def test_a_run_writes_the_same_bytes_elsewhere(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(rc.main(["--receipts", tmp]), 0)
            written = (pathlib.Path(tmp) / rc.RECEIPT_NAME).read_bytes()
            self.assertEqual(written, RECEIPT.read_bytes().replace(b"\r\n", b"\n"))

    def test_an_oversize_receipt_is_refused(self) -> None:
        saved = rc.MEGABYTE
        rc.MEGABYTE = 10
        try:
            with tempfile.TemporaryDirectory() as tmp:
                self.assertEqual(rc.main(["--receipts", tmp]), 1)
        finally:
            rc.MEGABYTE = saved

    def test_a_forbidden_key_in_the_payload_is_refused(self) -> None:
        saved = rc.build
        tainted = dict(payload(), timestamp="x")
        rc.build = lambda: tainted
        try:
            with tempfile.TemporaryDirectory() as tmp:
                self.assertEqual(rc.main(["--receipts", tmp]), 1)
        finally:
            rc.build = saved


class ScoringTests(unittest.TestCase):
    def test_the_scored_verdicts_are_the_dated_ones(self) -> None:
        """Dated 2026-09-25 in STATUS.md: four computational hits, one
        miss (P-13), eleven rows scored elsewhere."""
        scored = payload()["predictions_scored"]
        verdicts = {pid: row["verdict"] for pid, row in scored.items()}
        self.assertEqual(
            sorted(pid for pid, v in verdicts.items() if v == "HIT"),
            ["P-10", "P-11", "P-12", "P-9"],
        )
        self.assertEqual(sorted(pid for pid, v in verdicts.items() if v == "MISSED"), ["P-13"])
        self.assertEqual(sum(1 for v in verdicts.values() if v == "ELSEWHERE"), 11)
        self.assertEqual(len(verdicts), 16)

    def test_the_miss_is_the_across_bases_witness_alone(self) -> None:
        """P-13 misses on `counts_not_of_class` and on nothing else: the
        six hypothesis countermodels hold in the Python grammar."""
        value = payload()["predictions_scored"]["P-13"]["value"]
        self.assertEqual([name for name, holds in value.items() if not holds],
                         ["counts_not_of_class"])

    def test_every_hit_row_can_miss(self) -> None:
        """NEGATIVE: each hit row turns to a miss when its value is moved,
        so a HIT is not a constant."""
        reports = payload()["reports"]
        movers: dict[str, Callable[[dict[str, Any]], None]] = {
            "P-9": lambda r: r["classes"].__setitem__("key_brute_disagreements", 1),
            "P-10": lambda r: r["classes"]["within_base"]["L"].__setitem__(
                "classes_with_two_component_tuples", 1
            ),
            "P-11": lambda r: r["bases"]["F"].__setitem__("returns", 1),
            "P-12": lambda r: r["classes"].__setitem__(
                "classes_at_more_than_one_base_with_two_changing_counts", 0
            ),
        }
        for pid, move in movers.items():
            moved = copy.deepcopy(reports)
            move(moved)
            self.assertEqual(rc.score(moved)[pid]["verdict"], "MISSED", pid)

    def test_the_missed_row_can_hit(self) -> None:
        """NEGATIVE, the other way: P-13 is not a constant miss.  With the
        across-bases claim set true it turns to a hit."""
        reports = copy.deepcopy(payload()["reports"])
        reports["lean_witnesses"]["counts_not_of_class"]["claim_holds"] = True
        self.assertEqual(rc.score(reports)["P-13"]["verdict"], "HIT")

    def test_p10_misses_on_the_union_too(self) -> None:
        reports = copy.deepcopy(payload()["reports"])
        reports["classes"]["classes_over_all_bases_with_two_component_tuples"] = 1
        self.assertEqual(rc.score(reports)["P-10"]["verdict"], "MISSED")

    def test_p11_misses_on_a_missing_kind_and_on_a_growing_kind(self) -> None:
        for kinds in ({"Supply": 1, "Impose": 1, "AdmitInst": 1},
                      {"Supply": 1, "Impose": 1, "AdmitInst": 1, "AdmitRuleAll": 1,
                       "AdmitDatum": 1}):
            reports = copy.deepcopy(payload()["reports"])
            reports["bases"]["EMPTY"]["stutters_by_kind"] = kinds
            self.assertEqual(rc.score(reports)["P-11"]["verdict"], "MISSED", kinds)

    def test_p12_misses_outside_the_arithmetic_range(self) -> None:
        for value in (rc.MULTI_BASE_LOW - 1, rc.MULTI_BASE_HIGH + 1):
            reports = copy.deepcopy(payload()["reports"])
            reports["classes"]["classes_at_more_than_one_base"] = value
            self.assertEqual(rc.score(reports)["P-12"]["verdict"], "MISSED", value)

    def test_the_arithmetic_range_is_the_receipts(self) -> None:
        """P-12's bounds: the within-base class counts sum to ninety-one
        more than the union; a class at two bases counts once extra and a
        class at three twice, so the count lies between half of that,
        rounded up, and all of it."""
        excess = sum(rc.EXPECTED_CLASSES.values()) - rc.EXPECTED_ALL_CLASSES
        self.assertEqual(excess, 91)
        self.assertEqual((rc.MULTI_BASE_LOW, rc.MULTI_BASE_HIGH), ((excess + 1) // 2, excess))
        classes = payload()["reports"]["classes"]
        self.assertEqual(
            classes["classes_at_more_than_one_base"] + classes["classes_at_three_bases"], excess
        )


class CountTests(unittest.TestCase):
    """Each count on a history short enough to read by hand."""

    def test_the_five_components(self) -> None:
        r = regime(AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitForm(2), AdmitInst(0, (0, 1)),
                   AdmitRuleAll(0), Impose(0, 1))
        self.assertEqual(cc.components(r), (2, 1, 1, 1, 1))
        self.assertEqual(cc.components(EMPTY), (0, 0, 0, 0, 0))

    def test_supplies_and_repeats_change_nothing(self) -> None:
        history = (Supply("<z>"), AdmitDatum(N[0]), AdmitForm(1), AdmitInst(0, (0,)),
                   AdmitInst(0, (0,)), AdmitRuleAll(0), AdmitRuleAll(0))
        self.assertEqual(cc.counts(EMPTY, history), (4, 1, 3))

    def test_a_repeated_token_is_not_a_growth(self) -> None:
        self.assertEqual(cc.counts(EMPTY, (AdmitDatum(N[0]), AdmitDatum(N[0]))), (1, 1, 0))

    def test_the_prefixes_start_at_the_base(self) -> None:
        prefixes = cc.prefix_regimes(EMPTY, (AdmitDatum(N[0]), Supply("<z>")))
        self.assertEqual(len(prefixes), 3)
        self.assertEqual(prefixes[0], EMPTY)
        self.assertEqual(prefixes[1], prefixes[2])

    def test_a_refused_event_raises_as_the_sealed_replay_does(self) -> None:
        with self.assertRaises(AdmissionError):
            cc.counts(EMPTY, (Impose(0, 1),))


class RecurrenceTests(unittest.TestCase):
    def test_a_supply_is_a_stutter(self) -> None:
        found = cc.recurrences(EMPTY, (AdmitDatum(N[0]), Supply("<z>")), Keys())
        self.assertEqual(found, [cc.Recurrence(2, "Supply", True)])

    def test_growth_alone_never_recurs(self) -> None:
        history = (AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitForm(1), AdmitInst(0, (1,)))
        self.assertEqual(cc.recurrences(EMPTY, history, Keys()), [])
        self.assertFalse(cc.has_unchanging_event(EMPTY, history))

    def test_a_repeated_requirement_is_a_stutter(self) -> None:
        history = (AdmitDatum(N[0]), AdmitDatum(N[1]), Impose(0, 1), Impose(0, 1))
        self.assertEqual(cc.recurrences(EMPTY, history, Keys()),
                         [cc.Recurrence(4, "Impose", True)])
        self.assertTrue(cc.has_unchanging_event(EMPTY, history))

    def test_a_forged_partition_shows_returns_and_mismatches(self) -> None:
        """NEGATIVE: under a key procedure that lumps every regime, a
        growth reaches the class of the base without being the base; the
        report counts it as a return, and as a sequence that recurs
        without an unchanging event."""
        history = (AdmitDatum(N[0]),)
        found = cc.recurrences(EMPTY, history, LumpingKeys())
        self.assertEqual(found, [cc.Recurrence(1, "AdmitDatum", False)])
        report = cc.recurrence_report(EMPTY, [(), history], LumpingKeys())
        self.assertEqual(report["returns"], 1)
        self.assertEqual(report["recurs_iff_unchanging_mismatches"], 1)
        self.assertEqual(report["stutters_by_kind"], {})

    def test_the_report_counts_by_kind(self) -> None:
        histories = [(), (Supply("<z>"),), (AdmitForm(1), AdmitRuleAll(0), AdmitRuleAll(0))]
        report = cc.recurrence_report(EMPTY, histories, Keys())
        self.assertEqual(report["recurring_sequences"], 2)
        self.assertEqual(report["sequences_with_an_unchanging_event"], 2)
        self.assertEqual(report["stutters_by_kind"], {"AdmitRuleAll": 1, "Supply": 1})
        self.assertEqual(report["returns"], 0)


class ClassReportTests(unittest.TestCase):
    """NEGATIVE: the class censuses count a forged partition."""

    def _population(self, keys: Keys) -> Population:
        rects = (
            rectangle("EMPTY", EMPTY, (AdmitDatum(N[0]),), (AdmitForm(1),)),
            rectangle("L", regime(AdmitDatum(N[0])), (AdmitDatum(N[1]),)),
        )
        regimes = tuple(sorted({n.regime for r in rects for n in r.nodes},
                               key=lambda x: (x.n_data(), x.forms)))
        return Population(rects, regimes, keys)

    def test_the_true_partition_keeps_every_count(self) -> None:
        report = cc.class_report(self._population(Keys()))
        for row in report["within_base"].values():
            self.assertEqual(row["classes_with_two_component_tuples"], 0)
            self.assertEqual(row["classes_with_two_changing_counts"], 0)
        self.assertEqual(report["classes_over_all_bases_with_two_component_tuples"], 0)
        self.assertEqual(report["key_brute_disagreements"], 0)
        # One datum is reached from EMPTY in one event and is the base of L.
        self.assertEqual(report["classes_at_more_than_one_base"], 1)
        self.assertEqual(report["classes_at_more_than_one_base_with_two_changing_counts"], 1)

    def test_a_lumping_partition_is_counted_everywhere(self) -> None:
        report = cc.class_report(self._population(LumpingKeys()))
        empty = report["within_base"]["EMPTY"]
        self.assertEqual(empty["classes"], 1)
        self.assertEqual(empty["classes_with_two_component_tuples"], 1)
        self.assertEqual(empty["classes_with_two_changing_counts"], 1)
        self.assertEqual(empty["classes_with_two_growth_counts"], 1)
        self.assertEqual(empty["classes_with_two_rest_counts"], 1)
        self.assertEqual(report["classes_over_all_bases_with_two_component_tuples"], 1)
        self.assertGreater(report["key_brute_disagreements"], 0)
        self.assertEqual(report["classes_at_three_bases"], 0)


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
        self.assertEqual(reports["replay_mismatches"], 0)
        self.assertEqual(reports["distinct_regimes_over_all_bases"], 2316)

    def test_the_recurrence_counts_are_the_dated_ones(self) -> None:
        """Dated 2026-09-25 in STATUS.md."""
        bases = payload()["reports"]["bases"]
        self.assertEqual({b: bases[b]["recurring_sequences"] for b in bases},
                         {"EMPTY": 339, "L": 1597, "F": 4790})
        self.assertEqual({b: bases[b]["stutters"] for b in bases},
                         {"EMPTY": 454, "L": 1921, "F": 5583})
        self.assertEqual(bases["EMPTY"]["stutters_by_kind"],
                         {"AdmitInst": 4, "AdmitRuleAll": 38, "Impose": 1, "Supply": 411})
        for base, row in bases.items():
            self.assertEqual(row["returns"], 0, base)
            self.assertEqual(row["recurring_sequences"],
                             row["sequences_with_an_unchanging_event"], base)

    def test_the_class_counts_are_the_dated_ones(self) -> None:
        """Dated 2026-09-25 in STATUS.md."""
        classes = payload()["reports"]["classes"]
        self.assertEqual(classes["classes_at_more_than_one_base"], 86)
        self.assertEqual(classes["classes_at_three_bases"], 5)
        self.assertEqual(classes["classes_at_more_than_one_base_with_two_changing_counts"], 86)
        for base, row in classes["within_base"].items():
            for key in ("classes_with_two_changing_counts", "classes_with_two_growth_counts",
                        "classes_with_two_rest_counts"):
                self.assertEqual(row[key], 0, (base, key))


class WitnessTests(unittest.TestCase):
    def test_the_hypothesis_countermodels_hold_in_the_python_grammar(self) -> None:
        report = cc.lean_witnesses()
        for name in ("insts_need_nodup", "rules_need_nodup", "reqs_need_nodup"):
            self.assertTrue(report[name]["one_python_regime"], name)
        for name in ("insts_need_wf", "rules_need_wf", "reqs_need_wf"):
            self.assertTrue(report[name]["refused_by_the_sealed_step"], name)

    def test_the_across_bases_witness_misses_in_the_python_grammar(self) -> None:
        """The frozen P-13 wrote the Lean witness from the Lean reading
        regime `R2L`, which holds the requirement between its two data.
        The sealed Python reading regime L does not, so the two sides are
        not one class; the CHANGING counts are the claimed ones."""
        row = cc.lean_witnesses()["counts_not_of_class"]
        self.assertEqual(row["changing_counts"], [0, 3])
        self.assertFalse(row["one_class"])
        self.assertFalse(row["claim_holds"])
        self.assertEqual([type(e).__name__ for e in cc.across_bases_histories()[1]],
                         ["AdmitDatum", "AdmitDatum", "Impose"])

    def test_the_python_reading_witness(self) -> None:
        """Recorded after the miss, and not scored."""
        row = cc.python_reading_witness()
        self.assertEqual(row, {"reading_l_requirements": 0, "one_class": True,
                               "changing_counts": [0, 2]})

    def test_an_accepted_event_is_not_refused(self) -> None:
        self.assertFalse(cc._refused(EMPTY, Supply("<z>")))


if __name__ == "__main__":
    unittest.main()
