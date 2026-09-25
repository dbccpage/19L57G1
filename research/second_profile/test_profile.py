"""Tests of the rung-nine cross-check and its runner.

A hand copy of the shape of `research/second_class/test_class.py`, with
this rung's pieces.  Three kinds, kept apart:

* the receipt: it regenerates byte-identically, `--check` writes nothing
  and refuses drift, and it carries no temporal or environment key;
* the pieces of `profile_rows.py`, each on a regime or a history short
  enough to read by hand, so a quantity checked over the rectangle is
  also checked where its value is known;
* NEGATIVE tests: each census of the report is fed a forged key
  procedure and must COUNT what it was built to count, and each scored
  row is moved and must change its verdict, so a report of zero lumped
  classes is not a report of a check that cannot fire.
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

import profile_rows as pr  # noqa: E402

# `profile_rows` puts sibling trees on the path and each of them carries
# its own `run_*`, `verify_pins` and `test_*`; this tree goes back to the
# front first.  See the note in `profile_rows.py`.
if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))
import run_profile as rp  # noqa: E402

from derivation.iso import CanonKey  # noqa: E402
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


def regime(*events: Event) -> Regime:
    return replay(tuple(events), EMPTY)


N = pr.ALPHABET.fresh_tokens


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


# The regime of the Lean witness `twoness_at_four`, in the Python grammar.
FOUR = (AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitForm(1), AdmitInst(0, (0,)))


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
            drifted = RECEIPT.read_bytes().replace(
                b'"sequences_holding_two": 22', b'"sequences_holding_two": 23'
            )
            self.assertNotEqual(drifted, RECEIPT.read_bytes())
            target.write_bytes(drifted)
            self.assertEqual(rp.main(["--check", "--receipts", tmp]), 1)

    def test_check_refuses_a_missing_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
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
            with tempfile.TemporaryDirectory() as tmp:
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
        """Dated 2026-09-25 in STATUS.md: seven computational hits, no
        miss, eleven rows scored elsewhere."""
        scored = payload()["predictions_scored"]
        verdicts = {pid: row["verdict"] for pid, row in scored.items()}
        self.assertEqual(
            sorted(pid for pid, v in verdicts.items() if v == "HIT"),
            ["Q-10", "Q-11", "Q-12", "Q-13", "Q-14", "Q-8", "Q-9"],
        )
        self.assertEqual(sorted(pid for pid, v in verdicts.items() if v == "MISSED"), [])
        self.assertEqual(sum(1 for v in verdicts.values() if v == "ELSEWHERE"), 11)
        self.assertEqual(len(verdicts), 18)

    def test_every_hit_row_can_miss(self) -> None:
        """NEGATIVE: each hit row turns to a miss when its value is moved,
        so a HIT is not a constant."""
        reports = payload()["reports"]
        movers: dict[str, Callable[[dict[str, Any]], None]] = {
            "Q-8": lambda r: r["classes"].__setitem__("key_brute_disagreements", 1),
            "Q-9": lambda r: r["bases"]["EMPTY"].__setitem__("sequences_holding_two", 23),
            "Q-10": lambda r: r["bases"]["L"].__setitem__("two_count_mismatches", 1),
            "Q-11": lambda r: r["bases"]["F"].__setitem__("largest_class_count", 5),
            "Q-12": lambda r: r["classes"]["over_all_bases"].__setitem__(
                "classes_with_two_class_counts", 1
            ),
            "Q-13": lambda r: r["bases"]["EMPTY"].__setitem__(
                "ending_transitions_by_kind", {"AdmitInst": 1}
            ),
            "Q-14": lambda r: r["changes_by_kind_over_all_bases"].__setitem__("Impose", [0, 1]),
        }
        for pid, move in movers.items():
            moved = copy.deepcopy(reports)
            move(moved)
            self.assertEqual(rp.score(moved)[pid]["verdict"], "MISSED", pid)

    def test_q9_misses_on_a_least_length(self) -> None:
        reports = copy.deepcopy(payload()["reports"])
        reports["bases"]["L"]["least_length_holding_two"] = 3
        self.assertEqual(rp.score(reports)["Q-9"]["verdict"], "MISSED")

    def test_q11_misses_on_a_violated_bound(self) -> None:
        for key in ("count_above_data", "count_above_named_plus_one"):
            reports = copy.deepcopy(payload()["reports"])
            reports["bases"]["EMPTY"][key] = 1
            self.assertEqual(rp.score(reports)["Q-11"]["verdict"], "MISSED", key)

    def test_q12_misses_within_a_base_and_on_holding_two(self) -> None:
        reports = copy.deepcopy(payload()["reports"])
        reports["classes"]["within_base"]["F"]["classes_with_two_values_of_holding_two"] = 1
        self.assertEqual(rp.score(reports)["Q-12"]["verdict"], "MISSED")

    def test_q13_misses_on_a_keeping_kind_or_a_missing_kind(self) -> None:
        for kinds in ({"AdmitInst": 1}, {"AdmitInst": 1, "AdmitRuleAll": 1, "AdmitForm": 1}):
            reports = copy.deepcopy(payload()["reports"])
            reports["bases"]["F"]["ending_transitions_by_kind"] = kinds
            self.assertEqual(rp.score(reports)["Q-13"]["verdict"], "MISSED", kinds)

    def test_q14_misses_on_each_clause(self) -> None:
        cases: list[tuple[str, list[int]]] = [
            ("AdmitDatum", [0, 1, 2]),
            ("AdmitRuleAll", [-1, 0]),
            ("AdmitInst", [-1, 0, 1]),
            ("AdmitInst", [-3, -1, 0, 1, 2]),
        ]
        for kind, values in cases:
            reports = copy.deepcopy(payload()["reports"])
            reports["changes_by_kind_over_all_bases"][kind] = values
            self.assertEqual(rp.score(reports)["Q-14"]["verdict"], "MISSED", (kind, values))
        reports = copy.deepcopy(payload()["reports"])
        del reports["changes_by_kind_over_all_bases"]["Supply"]
        self.assertEqual(rp.score(reports)["Q-14"]["verdict"], "MISSED")


class RegimeTests(unittest.TestCase):
    """Each reading on a regime short enough to read by hand."""

    def test_the_empty_regime(self) -> None:
        self.assertFalse(pr.holds_two(EMPTY))
        self.assertEqual(pr.class_count(EMPTY), 0)
        self.assertEqual(pr.named(EMPTY), 0)

    def test_data_without_an_instance_are_one_class(self) -> None:
        r = regime(AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitForm(1), AdmitRuleAll(0))
        self.assertFalse(pr.holds_two(r))
        self.assertEqual(pr.class_count(r), 1)

    def test_the_four_event_witness(self) -> None:
        r = regime(*FOUR)
        self.assertTrue(pr.holds_two(r))
        self.assertEqual(pr.class_count(r), 2)
        self.assertEqual(pr.named(r), 1)

    def test_an_instance_of_arity_two_names_two_data(self) -> None:
        r = regime(AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitDatum(N[2]), AdmitForm(2),
                   AdmitInst(0, (0, 1)))
        self.assertEqual(pr.class_count(r), 3)
        self.assertEqual(pr.named(r), 2)

    def test_the_readings_are_memoized_and_agree(self) -> None:
        seen = pr.Readings()
        r = regime(*FOUR)
        self.assertTrue(seen.two(r))
        self.assertTrue(seen.two(r))
        self.assertEqual(seen.count(r), 2)
        self.assertEqual(seen.count(r), 2)

    def test_the_lean_witnesses_in_the_python_grammar(self) -> None:
        """Recorded, not scored: the four-event witness holds two, and one
        instance or one rule after it ends holding two."""
        report = pr.lean_witnesses()
        self.assertEqual(report["twoness_at_four"], {"holds_two": True, "class_count": 2})
        for name in ("twoness_lost_by_inst", "twoness_lost_by_rule"):
            self.assertEqual(report[name], {"holds_two": False, "class_count": 1}, name)


class BaseReportTests(unittest.TestCase):
    def test_a_small_rectangle_by_hand(self) -> None:
        """From the regime of the four-event witness: one more instance
        ends holding two and lowers the count by one; a supply changes
        nothing; a datum raises nothing it separates and joins the class
        of the unnamed datum."""
        root = regime(*FOUR)
        report = pr.base_report(
            root,
            nodes(root, (AdmitInst(0, (1,)),), (Supply("<z>"),), (AdmitDatum(N[2]),)),
            Keys(),
            pr.Readings(),
        )
        self.assertEqual(report["least_length_holding_two"], 0)
        self.assertEqual(report["ending_transitions_by_kind"], {"AdmitInst": 1})
        self.assertEqual(report["changes_by_kind"],
                         {"AdmitDatum": [0], "AdmitInst": [-1], "Supply": [0]})
        self.assertEqual(report["replay_mismatches"], 0)
        self.assertEqual(report["two_count_mismatches"], 0)
        self.assertEqual(report["largest_class_count"], 2)

    def test_no_sequence_holds_two_from_the_empty_regime_in_one_event(self) -> None:
        report = pr.base_report(
            EMPTY, nodes(EMPTY, (AdmitDatum(N[0]),), (AdmitForm(1),)), Keys(), pr.Readings()
        )
        self.assertIsNone(report["least_length_holding_two"])
        self.assertEqual(report["sequences_holding_two"], 0)
        self.assertEqual(report["ending_transitions_by_kind"], {})

    def test_a_forged_regime_is_counted_as_a_replay_mismatch(self) -> None:
        """NEGATIVE: a node whose recorded regime is not its replay is
        counted."""
        forged = [((), EMPTY), ((AdmitDatum(N[0]),), EMPTY)]
        report = pr.base_report(EMPTY, forged, Keys(), pr.Readings())
        self.assertEqual(report["replay_mismatches"], 1)

    def test_a_rule_can_end_holding_two(self) -> None:
        root = regime(*FOUR)
        report = pr.base_report(root, nodes(root, (AdmitRuleAll(0),), (Impose(0, 1),)),
                                Keys(), pr.Readings())
        self.assertEqual(report["ending_transitions_by_kind"], {"AdmitRuleAll": 1})
        self.assertEqual(report["changes_by_kind"], {"AdmitRuleAll": [-1], "Impose": [0]})


class ClassReportTests(unittest.TestCase):
    """NEGATIVE: the class censuses count a forged partition."""

    def _population(self, keys: Keys) -> Population:
        empty_nodes = nodes(EMPTY, FOUR)
        rects = (
            Rectangle("EMPTY", EMPTY, tuple(Node(h, r, 0) for h, r in empty_nodes), 0, 0),
        )
        regimes = tuple(sorted({r for _, r in empty_nodes},
                               key=lambda x: (x.n_data(), x.forms, len(x.insts))))
        return Population(rects, regimes, keys)

    def test_the_true_partition_lumps_nothing(self) -> None:
        report = pr.class_report(self._population(Keys()), pr.Readings())
        for row in list(report["within_base"].values()) + [report["over_all_bases"]]:
            self.assertEqual(row["classes_with_two_values_of_holding_two"], 0)
            self.assertEqual(row["classes_with_two_class_counts"], 0)
        self.assertEqual(report["key_brute_disagreements"], 0)
        self.assertEqual(report["distinct_regimes_over_all_bases"], 5)

    def test_a_lumping_partition_is_counted_everywhere(self) -> None:
        report = pr.class_report(self._population(LumpingKeys()), pr.Readings())
        for row in list(report["within_base"].values()) + [report["over_all_bases"]]:
            self.assertEqual(row["classes"], 1)
            self.assertEqual(row["classes_with_two_values_of_holding_two"], 1)
            self.assertEqual(row["classes_with_two_class_counts"], 1)
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

    def test_the_holding_two_counts_are_the_dated_ones(self) -> None:
        """Dated 2026-09-25 in STATUS.md."""
        bases = payload()["reports"]["bases"]
        self.assertEqual({b: bases[b]["sequences_holding_two"] for b in bases},
                         {"EMPTY": 22, "L": 2036, "F": 8676})
        self.assertEqual({b: bases[b]["regimes_holding_two"] for b in bases},
                         {"EMPTY": 6, "L": 315, "F": 1240})
        self.assertEqual({b: bases[b]["classes_holding_two"] for b in bases},
                         {"EMPTY": 3, "L": 82, "F": 156})
        self.assertEqual({b: bases[b]["ending_transitions_by_kind"] for b in bases},
                         {"EMPTY": {}, "L": {"AdmitInst": 28, "AdmitRuleAll": 126},
                          "F": {"AdmitInst": 6, "AdmitRuleAll": 370}})

    def test_the_class_count_histograms_are_the_dated_ones(self) -> None:
        """Dated 2026-09-25 in STATUS.md."""
        bases = payload()["reports"]["bases"]
        self.assertEqual({b: bases[b]["class_count_histogram"] for b in bases}, {
            "EMPTY": {"0": 21, "1": 48, "2": 6},
            "L": {"1": 208, "2": 225, "3": 90},
            "F": {"1": 478, "2": 356, "3": 824, "4": 60},
        })

    def test_no_instance_admission_lowered_the_count_by_two(self) -> None:
        """Recorded beside Q-14, which allowed it: within the rectangle no
        instance admission lowers the class count by two."""
        changes = payload()["reports"]["changes_by_kind_over_all_bases"]
        self.assertEqual(changes["AdmitInst"], [-1, 0, 1, 2])


if __name__ == "__main__":
    unittest.main()
