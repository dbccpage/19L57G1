"""Tests of the rung-six cross-check and its runner.

Three kinds, kept apart:

* the receipt: it regenerates byte-identically, `--check` writes nothing
  and refuses drift, and it carries no temporal or environment key;
* the pieces of `succession.py`, each on a history short enough to read
  by hand, so a count checked over the rectangle is also checked where
  its value is known;
* NEGATIVE tests: each law and each census of the report is fed a forged
  sequence and must COUNT it, and each scored row is moved and must turn
  to a miss, so a report of zero violations is not a report of a check
  that cannot fire.
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

import succession as sc  # noqa: E402

# `succession` puts sibling trees on the path and each of them carries its
# own `run_*`, `verify_pins` and `test_*`; this tree goes back to the front
# first.  See the note in `succession.py`.
if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))
import run_succession as rs  # noqa: E402

from derivation.engine import GENESIS_F, GENESIS_L  # noqa: E402
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


def sequenced(base: Regime, *events: Event) -> sc.Sequenced:
    return sc.Sequenced(tuple(events), replay(tuple(events), base), sc.counts(base, events))


N = sc.ALPHABET.fresh_tokens


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
            drifted = RECEIPT.read_bytes().replace(
                b'"split_regimes": 33', b'"split_regimes": 34'
            )
            self.assertNotEqual(drifted, RECEIPT.read_bytes())
            target.write_bytes(drifted)
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
        """Dated 2026-09-25 in STATUS.md: six computational hits, no
        miss, ten rows scored elsewhere."""
        scored = payload()["predictions_scored"]
        verdicts = {pid: row["verdict"] for pid, row in scored.items()}
        self.assertEqual(
            sorted(pid for pid, v in verdicts.items() if v == "HIT"),
            ["M-10", "M-11", "M-12", "M-13", "M-8", "M-9"],
        )
        self.assertEqual(sorted(pid for pid, v in verdicts.items() if v == "MISSED"), [])
        self.assertEqual(sum(1 for v in verdicts.values() if v == "ELSEWHERE"), 10)
        self.assertEqual(len(verdicts), 16)

    def test_every_computational_row_can_miss(self) -> None:
        """NEGATIVE: each hit row turns to a miss when its value is moved,
        so a HIT is not a constant."""
        reports = payload()["reports"]
        movers: dict[str, Callable[[dict[str, Any]], None]] = {
            "M-8": lambda r: r.__setitem__("replay_mismatches", 1),
            "M-9": lambda r: r["bases"]["L"].__setitem__("changing_from_empty_violations", 1),
            "M-10": lambda r: r["bases"]["EMPTY"]["readings"]["ADMITTING"][
                "shortest_splitting_sequence"
            ].__setitem__("length", 2),
            "M-11": lambda r: r["bases"]["F"]["readings"]["ADMITTING"].__setitem__(
                "split_regimes", 276
            ),
            "M-12": lambda r: r["classes"].__setitem__(
                "shared_classes_with_agreeing_relative_counts", 1
            ),
            "M-13": lambda r: r["bases"]["F"]["genesis_counts"].__setitem__("EVERY", 6),
        }
        for pid, move in movers.items():
            moved = copy.deepcopy(reports)
            move(moved)
            self.assertEqual(rs.score(moved)[pid]["verdict"], "MISSED", pid)

    def test_a_split_changing_count_misses_m9(self) -> None:
        reports = copy.deepcopy(payload()["reports"])
        reports["bases"]["EMPTY"]["readings"]["CHANGING"]["split_regimes"] = 1
        self.assertEqual(rs.score(reports)["M-9"]["verdict"], "MISSED")

    def test_an_absent_splitting_sequence_misses_m10(self) -> None:
        for reading in ("EVERY", "ADMITTING"):
            reports = copy.deepcopy(payload()["reports"])
            reports["bases"]["L"]["readings"][reading]["shortest_splitting_sequence"] = None
            self.assertEqual(rs.score(reports)["M-10"]["verdict"], "MISSED", reading)

    def test_a_non_supply_every_witness_misses_m10(self) -> None:
        reports = copy.deepcopy(payload()["reports"])
        reports["bases"]["L"]["readings"]["EVERY"]["shortest_splitting_sequence"][
            "history"
        ] = ["Impose(0,1)"]
        self.assertEqual(rs.score(reports)["M-10"]["verdict"], "MISSED")

    def test_no_shared_class_misses_m12(self) -> None:
        reports = copy.deepcopy(payload()["reports"])
        reports["classes"]["classes_shared_by_bases"] = 0
        self.assertEqual(rs.score(reports)["M-12"]["verdict"], "MISSED")


class CountTests(unittest.TestCase):
    """The three counts on histories read by hand."""

    def test_the_element_count(self) -> None:
        self.assertEqual(sc.element_count(EMPTY), 0)
        r = regime(AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitForm(2), AdmitInst(0, (0, 1)),
                   AdmitRuleAll(0), Impose(0, 1))
        self.assertEqual(sc.element_count(r), 6)

    def test_a_supply_is_accepted_only_under_every(self) -> None:
        self.assertEqual(
            sc.counts(EMPTY, (Supply("<z>"),)), {"EVERY": 1, "ADMITTING": 0, "CHANGING": 0}
        )

    def test_a_repeated_admission_is_accepted_under_admitting_only(self) -> None:
        found = sc.counts(EMPTY, (AdmitForm(1), AdmitRuleAll(0), AdmitRuleAll(0)))
        self.assertEqual(found, {"EVERY": 3, "ADMITTING": 3, "CHANGING": 2})

    def test_the_sealed_genesis_histories(self) -> None:
        self.assertEqual(
            sc.counts(EMPTY, GENESIS_L), {"EVERY": 6, "ADMITTING": 2, "CHANGING": 2}
        )
        self.assertEqual(
            sc.counts(EMPTY, GENESIS_F), {"EVERY": 7, "ADMITTING": 3, "CHANGING": 3}
        )

    def test_a_refused_event_raises_as_the_sealed_replay_does(self) -> None:
        with self.assertRaises(AdmissionError):
            sc.counts(EMPTY, (Impose(0, 1),))


class SplittingTests(unittest.TestCase):
    """The shortest splitting sequence, on groups read by hand."""

    def test_an_unsplit_group_has_no_witness(self) -> None:
        one = sequenced(EMPTY, AdmitForm(1))
        split, pair = sc.splitting({one.regime: [one]}, "EVERY")
        self.assertEqual((split, pair), (0, None))
        self.assertIsNone(sc.witness(None, "EVERY"))

    def test_the_longer_member_is_the_splitting_one(self) -> None:
        short = sequenced(EMPTY)
        long = sequenced(EMPTY, Supply("<z>"))
        split, pair = sc.splitting({EMPTY: [long, short]}, "EVERY")
        self.assertEqual(split, 1)
        assert pair is not None
        self.assertEqual(pair, (short, long))
        found = sc.witness(pair, "EVERY")
        assert found is not None
        self.assertEqual(found["length"], 1)
        self.assertEqual(found["history"], ["Supply(<z>)"])
        self.assertEqual(found["splits_from"], [])

    def test_of_two_equal_lengths_the_lesser_in_order_splits(self) -> None:
        """Both members of an equal-length pair differ from a sequence of
        no greater length; the lesser by descriptor is the witness."""
        base = regime(AdmitDatum(N[0]), AdmitDatum(N[1]))
        repeat = sequenced(base, Impose(0, 1), Impose(0, 1))
        supplied = sequenced(base, Impose(0, 1), Supply("<z>"))
        split, pair = sc.splitting({repeat.regime: [supplied, repeat]}, "ADMITTING")
        self.assertEqual(split, 1)
        assert pair is not None
        self.assertEqual(pair[1], repeat)
        self.assertEqual(pair[0], supplied)

    def test_the_least_group_witness_wins(self) -> None:
        base = regime(AdmitDatum(N[0]), AdmitDatum(N[1]))
        a1 = sequenced(base, Impose(0, 1))
        a2 = sequenced(base, Impose(0, 1), Impose(0, 1))
        b1 = sequenced(base, AdmitForm(1), AdmitRuleAll(0))
        b2 = sequenced(base, AdmitForm(1), AdmitRuleAll(0), AdmitRuleAll(0))
        groups = {b1.regime: [b1, b2], a1.regime: [a1, a2]}
        split, pair = sc.splitting(groups, "ADMITTING")
        self.assertEqual(split, 2)
        assert pair is not None
        self.assertEqual(pair[1], a2)


class ForgedReportTests(unittest.TestCase):
    """NEGATIVE: every law of the base report and every census of the
    class report counts a forged sequence."""

    def test_a_forged_changing_count_violates_both_laws(self) -> None:
        good = sequenced(EMPTY, AdmitForm(1))
        forged = sc.Sequenced(good.history, good.regime, dict(good.counts, CHANGING=0))
        report = sc.base_report("EMPTY", EMPTY, [forged])
        self.assertEqual(report["changing_law_violations"], 1)
        self.assertEqual(report["changing_from_empty_violations"], 0)
        clean = sc.base_report("EMPTY", EMPTY, [good])
        self.assertEqual(clean["changing_law_violations"], 0)

    def test_a_forged_regime_violates_the_law_from_the_empty_regime(self) -> None:
        good = sequenced(EMPTY, AdmitForm(1))
        forged = sc.Sequenced(good.history, regime(AdmitForm(1), AdmitForm(1)), good.counts)
        report = sc.base_report("EMPTY", EMPTY, [forged])
        self.assertEqual(report["changing_from_empty_violations"], 1)
        self.assertEqual(report["changing_law_violations"], 1)

    def _population(self) -> Population:
        return Population((), (), Keys())

    def test_a_class_with_two_counts_within_a_base_is_counted(self) -> None:
        one = sequenced(EMPTY, AdmitForm(1))
        forged = sc.Sequenced((), one.regime, dict(one.counts, CHANGING=5))
        report = sc.class_report(self._population(), {"EMPTY": [one, forged]})
        self.assertEqual(report["classes_with_two_changing_counts_within_a_base"], {"EMPTY": 1})

    def test_agreeing_counts_at_two_bases_are_counted(self) -> None:
        """Two bases whose base-relative counts of one class agree: the
        census counts the class, and the count from the empty regime,
        which adds the bases' own element counts, then disagrees."""
        base_l = replay(GENESIS_L, EMPTY)
        at_empty = sequenced(EMPTY, AdmitDatum(N[0]), AdmitDatum(N[1]))
        at_l = sc.Sequenced((), base_l, dict(sc.counts(base_l, ()), CHANGING=2))
        report = sc.class_report(self._population(), {"EMPTY": [at_empty], "L": [at_l]})
        self.assertEqual(report["classes_shared_by_bases"], 1)
        self.assertEqual(report["shared_classes_by_bases"], {"EMPTY+L": 1})
        self.assertEqual(report["shared_classes_with_agreeing_relative_counts"], 1)
        self.assertEqual(report["shared_classes_with_two_counts_from_empty"], 1)

    def test_the_honest_shared_class_differs_relatively_and_agrees_from_empty(self) -> None:
        base_l = replay(GENESIS_L, EMPTY)
        at_empty = sequenced(EMPTY, AdmitDatum(N[0]), AdmitDatum(N[1]))
        at_l = sequenced(base_l)
        report = sc.class_report(self._population(), {"EMPTY": [at_empty], "L": [at_l]})
        self.assertEqual(report["classes_shared_by_bases"], 1)
        self.assertEqual(report["shared_classes_with_agreeing_relative_counts"], 0)
        self.assertEqual(report["shared_classes_with_two_counts_from_empty"], 0)


class RectangleTests(unittest.TestCase):
    def test_the_rectangle_is_rung_three_s(self) -> None:
        bases = payload()["reports"]["bases"]
        self.assertEqual(
            {b: bases[b]["sequences"] for b in bases}, {"EMPTY": 577, "L": 3928, "F": 14293}
        )
        self.assertEqual(
            {b: bases[b]["distinct_regimes"] for b in bases}, {"EMPTY": 75, "L": 523, "F": 1718}
        )
        self.assertEqual(payload()["reports"]["replay_mismatches"], 0)

    def test_the_changing_reading_never_splits(self) -> None:
        for base, row in payload()["reports"]["bases"].items():
            self.assertEqual(row["readings"]["CHANGING"]["split_regimes"], 0, base)
            self.assertIsNone(row["readings"]["CHANGING"]["shortest_splitting_sequence"], base)

    def test_the_classes_are_rung_four_s(self) -> None:
        self.assertEqual(payload()["reports"]["classes"]["classes"], 402)


class WitnessTests(unittest.TestCase):
    def test_the_lean_witnesses_replay(self) -> None:
        """Each Lean countermodel, in the sealed Python grammar: both
        sides reach one regime and the counts differ as claimed."""
        report = sc.witness_report()
        self.assertEqual(sorted(report), ["admitting_splits", "base_matters", "every_splits"])
        for name, row in report.items():
            self.assertTrue(row["claim_holds"], name)
        self.assertEqual(report["every_splits"]["counts"], [0, 1])
        self.assertEqual(report["admitting_splits"]["counts"], [2, 3])
        self.assertEqual(report["base_matters"]["counts"], [3, 0])


if __name__ == "__main__":
    unittest.main()
