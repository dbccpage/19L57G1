"""Tests of the rung-seven cross-check and its runner.

A hand copy of the shape of `research/second_succession/test_succession.py`,
with this rung's pieces.  Three kinds, kept apart:

* the receipt: it regenerates byte-identically, `--check` writes nothing
  and refuses drift, and it carries no temporal or environment key;
* the pieces of `duration.py`, each on a history short enough to read by
  hand, so a quantity checked over the rectangle is also checked where
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

import duration as du  # noqa: E402

# `duration` puts sibling trees on the path and each of them carries its
# own `run_*`, `verify_pins` and `test_*`; this tree goes back to the front
# first.  See the note in `duration.py`.
if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))
import run_duration as rd  # noqa: E402

from derivation.engine import GENESIS_L  # noqa: E402
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

RECEIPT = HERE / "receipts" / rd.RECEIPT_NAME
_PAYLOAD: dict[str, Any] | None = None


def payload() -> dict[str, Any]:
    """One build per test run; the rectangle is the expensive part."""
    global _PAYLOAD
    if _PAYLOAD is None:
        _PAYLOAD = rd.build()
    return _PAYLOAD


def regime(*events: Event) -> Regime:
    return replay(tuple(events), EMPTY)


def sequenced(base: Regime, *events: Event) -> du.Sequenced:
    return du.Sequenced(tuple(events), replay(tuple(events), base), du.vector(base, events))


N = du.ALPHABET.fresh_tokens


class ReceiptTests(unittest.TestCase):
    def test_the_committed_receipt_is_a_fresh_run(self) -> None:
        committed = RECEIPT.read_bytes().replace(b"\r\n", b"\n")
        self.assertEqual(committed, rd.render(payload()))

    def test_the_receipt_is_stored_with_no_carriage_return(self) -> None:
        self.assertNotIn(b"\r", RECEIPT.read_bytes())

    def test_the_receipt_carries_no_forbidden_key(self) -> None:
        self.assertEqual(rd.forbidden_keys(payload()), [])

    def test_a_forbidden_key_is_named_at_any_depth(self) -> None:
        probe = {"a": [{"b": {"Timestamp": 1}}], "host": "x"}
        self.assertEqual(sorted(rd.forbidden_keys(probe)), ["a[0].b.Timestamp", "host"])

    def test_the_frozen_digests_are_the_manifest_ones(self) -> None:
        manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
        frozen = {item["path"].split("/")[-1]: item["sha256"] for item in manifest["frozen_texts"]}
        self.assertEqual(payload()["prompt_sha256"], frozen["PROMPT.md"])
        self.assertEqual(payload()["predictions_sha256"], frozen["PREDICTIONS.md"])

    def test_check_passes_and_writes_nothing(self) -> None:
        before = RECEIPT.read_bytes()
        self.assertEqual(rd.main(["--check"]), 0)
        self.assertEqual(RECEIPT.read_bytes(), before)

    def test_check_refuses_a_drifted_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / rd.RECEIPT_NAME
            drifted = RECEIPT.read_bytes().replace(
                b'"vector_split_regimes": 47', b'"vector_split_regimes": 48'
            )
            self.assertNotEqual(drifted, RECEIPT.read_bytes())
            target.write_bytes(drifted)
            self.assertEqual(rd.main(["--check", "--receipts", tmp]), 1)

    def test_check_refuses_a_missing_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(rd.main(["--check", "--receipts", tmp]), 1)

    def test_a_run_writes_the_same_bytes_elsewhere(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(rd.main(["--receipts", tmp]), 0)
            written = (pathlib.Path(tmp) / rd.RECEIPT_NAME).read_bytes()
            self.assertEqual(written, RECEIPT.read_bytes().replace(b"\r\n", b"\n"))

    def test_an_oversize_receipt_is_refused(self) -> None:
        saved = rd.MEGABYTE
        rd.MEGABYTE = 10
        try:
            with tempfile.TemporaryDirectory() as tmp:
                self.assertEqual(rd.main(["--receipts", tmp]), 1)
        finally:
            rd.MEGABYTE = saved

    def test_a_forbidden_key_in_the_payload_is_refused(self) -> None:
        saved = rd.build
        tainted = dict(payload(), timestamp="x")
        rd.build = lambda: tainted
        try:
            with tempfile.TemporaryDirectory() as tmp:
                self.assertEqual(rd.main(["--receipts", tmp]), 1)
        finally:
            rd.build = saved


class ScoringTests(unittest.TestCase):
    def test_the_scored_verdicts_are_the_dated_ones(self) -> None:
        """Dated 2026-09-25 in STATUS.md: seven computational hits, no
        miss, ten rows scored elsewhere."""
        scored = payload()["predictions_scored"]
        verdicts = {pid: row["verdict"] for pid, row in scored.items()}
        self.assertEqual(
            sorted(pid for pid, v in verdicts.items() if v == "HIT"),
            ["N-10", "N-11", "N-12", "N-13", "N-14", "N-8", "N-9"],
        )
        self.assertEqual(sorted(pid for pid, v in verdicts.items() if v == "MISSED"), [])
        self.assertEqual(sum(1 for v in verdicts.values() if v == "ELSEWHERE"), 10)
        self.assertEqual(len(verdicts), 17)

    def test_every_computational_row_can_miss(self) -> None:
        """NEGATIVE: each hit row turns to a miss when its value is moved,
        so a HIT is not a constant."""
        reports = payload()["reports"]
        movers: dict[str, Callable[[dict[str, Any]], None]] = {
            "N-8": lambda r: r.__setitem__("replay_mismatches", 1),
            "N-9": lambda r: r["bases"]["L"].__setitem__("sum_violations", 1),
            "N-10": lambda r: r["bases"]["F"].__setitem__(
                "regimes_with_unreached_or_extra_tuples", 1
            ),
            "N-11": lambda r: r["bases"]["EMPTY"]["shortest_gap_splitting_sequence"].__setitem__(
                "length", 4
            ),
            "N-12": lambda r: r["bases"]["L"].__setitem__("tail_only_regimes", 0),
            "N-13": lambda r: r["classes"]["classes_with_two_sums"].__setitem__("F", 1),
            "N-14": lambda r: r["lean_witnesses"]["gap_splits"].__setitem__(
                "claim_holds", False
            ),
        }
        for pid, move in movers.items():
            moved = copy.deepcopy(reports)
            move(moved)
            self.assertEqual(rd.score(moved)[pid]["verdict"], "MISSED", pid)

    def test_more_gap_split_than_vector_split_misses_n11(self) -> None:
        reports = copy.deepcopy(payload()["reports"])
        reports["bases"]["F"]["gap_split_regimes"] = reports["bases"]["F"]["vector_split_regimes"] + 1
        self.assertEqual(rd.score(reports)["N-11"]["verdict"], "MISSED")

    def test_an_absent_splitting_sequence_misses_n11(self) -> None:
        for key in ("shortest_vector_splitting_sequence", "shortest_gap_splitting_sequence"):
            reports = copy.deepcopy(payload()["reports"])
            reports["bases"]["L"][key] = None
            self.assertEqual(rd.score(reports)["N-11"]["verdict"], "MISSED", key)

    def test_no_class_with_two_envelopes_misses_n13(self) -> None:
        reports = copy.deepcopy(payload()["reports"])
        reports["classes"]["classes_with_two_envelopes"]["EMPTY"] = 0
        self.assertEqual(rd.score(reports)["N-13"]["verdict"], "MISSED")


class VectorTests(unittest.TestCase):
    """The duration vector on histories read by hand."""

    def test_the_empty_history_has_one_empty_segment(self) -> None:
        self.assertEqual(du.vector(EMPTY, ()), (0,))

    def test_a_supply_and_a_repeat_are_not_rounds(self) -> None:
        history = (AdmitForm(1), Supply("<z>"), AdmitRuleAll(0), AdmitRuleAll(0))
        self.assertEqual(du.vector(EMPTY, history), (2,))

    def test_a_repeated_datum_token_is_not_a_growth(self) -> None:
        history = (AdmitDatum(N[0]), AdmitDatum(N[0]), AdmitForm(1))
        self.assertEqual(du.vector(EMPTY, history), (0, 1))

    def test_segments_follow_the_growths(self) -> None:
        history = (
            AdmitForm(1), AdmitDatum(N[0]), AdmitInst(0, (0,)), AdmitRuleAll(0),
            AdmitDatum(N[1]), Impose(0, 1),
        )
        self.assertEqual(du.vector(EMPTY, history), (1, 2, 1))
        self.assertEqual(du.gaps(du.vector(EMPTY, history)), (2,))

    def test_the_sealed_genesis_history(self) -> None:
        """Two growths and no rest round: three empty segments."""
        self.assertEqual(du.vector(EMPTY, GENESIS_L), (0, 0, 0))

    def test_a_refused_event_raises_as_the_sealed_replay_does(self) -> None:
        with self.assertRaises(AdmissionError):
            du.vector(EMPTY, (Impose(0, 1),))


class EnvelopeTests(unittest.TestCase):
    """Levels and the envelope on regimes read by hand."""

    def test_levels_of_each_kind(self) -> None:
        reached = regime(
            AdmitForm(2), AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitInst(0, (0, 1)),
            AdmitRuleAll(0), Impose(0, 1),
        )
        self.assertEqual(du.levels(EMPTY, reached), (0, 0, 2, 2))

    def test_a_base_datum_has_level_zero(self) -> None:
        base = regime(AdmitDatum(N[0]), AdmitDatum(N[1]))
        reached = replay((AdmitDatum(N[2]), Impose(0, 1), Impose(1, 2)), base)
        self.assertEqual(du.levels(base, reached), (0, 1))

    def test_the_base_elements_are_not_new(self) -> None:
        base = regime(AdmitForm(1), AdmitDatum(N[0]), AdmitInst(0, (0,)))
        reached = replay((AdmitRuleAll(0),), base)
        self.assertEqual(du.levels(base, reached), (0,))

    def test_a_lone_form_can_sit_anywhere(self) -> None:
        reached = regime(AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitForm(1))
        self.assertEqual(
            sorted(du.envelope(EMPTY, reached)), [(0, 0, 1), (0, 1, 0), (1, 0, 0)]
        )

    def test_a_requirement_on_the_newest_datum_is_pinned_to_the_tail(self) -> None:
        reached = regime(AdmitDatum(N[0]), AdmitDatum(N[1]), Impose(0, 1))
        self.assertEqual(sorted(du.envelope(EMPTY, reached)), [(0, 0, 1)])

    def test_an_instance_limits_the_suffix(self) -> None:
        reached = regime(AdmitDatum(N[0]), AdmitForm(1), AdmitInst(0, (0,)))
        self.assertEqual(sorted(du.envelope(EMPTY, reached)), [(0, 2), (1, 1)])

    def test_no_growth_leaves_one_segment(self) -> None:
        reached = regime(AdmitForm(1), AdmitRuleAll(0))
        self.assertEqual(sorted(du.envelope(EMPTY, reached)), [(2,)])


class SplittingTests(unittest.TestCase):
    """The shortest splitting sequence, on groups read by hand."""

    def test_an_unsplit_group_has_no_witness(self) -> None:
        one = sequenced(EMPTY, AdmitForm(1))
        split, pair = du.splitting({one.regime: [one]}, lambda s: s.vector)
        self.assertEqual((split, pair), (0, None))
        self.assertIsNone(du.witness(None, lambda s: s.vector))

    def test_the_lead_and_the_tail_split(self) -> None:
        early = sequenced(EMPTY, AdmitForm(1), AdmitDatum(N[0]))
        late = sequenced(EMPTY, AdmitDatum(N[0]), AdmitForm(1))
        split, pair = du.splitting({early.regime: [early, late]}, lambda s: s.vector)
        self.assertEqual(split, 1)
        assert pair is not None
        found = du.witness(pair, lambda s: s.vector)
        assert found is not None
        self.assertEqual(found["length"], 2)
        self.assertEqual(found["history"], ["AdmitDatum(<n0>)", "AdmitForm(1)"])
        self.assertEqual(found["value"], [0, 1])
        self.assertEqual(found["splits_from_value"], [1, 0])

    def test_a_shorter_sequence_with_a_supply_does_not_split(self) -> None:
        plain = sequenced(EMPTY, AdmitForm(1))
        supplied = sequenced(EMPTY, AdmitForm(1), Supply("<z>"))
        split, pair = du.splitting({plain.regime: [supplied, plain]}, lambda s: s.vector)
        self.assertEqual((split, pair), (0, None))

    def test_the_least_group_witness_wins(self) -> None:
        a1 = sequenced(EMPTY, AdmitForm(1), AdmitDatum(N[0]))
        a2 = sequenced(EMPTY, AdmitDatum(N[0]), AdmitForm(1))
        b1 = sequenced(EMPTY, AdmitDatum(N[0]), AdmitForm(1), AdmitDatum(N[1]))
        b2 = sequenced(EMPTY, AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitForm(1))
        groups = {b1.regime: [b1, b2], a1.regime: [a1, a2]}
        split, pair = du.splitting(groups, lambda s: s.vector)
        self.assertEqual(split, 2)
        assert pair is not None
        self.assertEqual(len(pair[1].history), 2)
        gap_split, gap_pair = du.splitting(groups, lambda s: du.gaps(s.vector))
        self.assertEqual(gap_split, 1)
        assert gap_pair is not None
        self.assertEqual(len(gap_pair[1].history), 3)


class ForgedReportTests(unittest.TestCase):
    """NEGATIVE: every law of the base report and every census of the
    class report counts a forged sequence."""

    def test_a_forged_vector_violates_the_shape_laws_and_the_envelope(self) -> None:
        good = sequenced(EMPTY, AdmitDatum(N[0]), AdmitForm(1))
        clean = du.base_report(EMPTY, [good])
        for key in ("length_violations", "sum_violations", "vectors_outside_envelope"):
            self.assertEqual(clean[key], 0, key)
        self.assertEqual(clean["regimes_with_unreached_or_extra_tuples"], 1)
        long = du.Sequenced(good.history, good.regime, (0, 1, 0))
        heavy = du.Sequenced(good.history, good.regime, (0, 2))
        report = du.base_report(EMPTY, [long, heavy])
        self.assertEqual(report["length_violations"], 1)
        self.assertEqual(report["sum_violations"], 1)
        self.assertEqual(report["vectors_outside_envelope"], 2)

    def test_a_vector_below_the_bound_is_outside_the_envelope(self) -> None:
        good = sequenced(EMPTY, AdmitDatum(N[0]), AdmitDatum(N[1]), Impose(0, 1))
        early = du.Sequenced(good.history, good.regime, (0, 1, 0))
        report = du.base_report(EMPTY, [early])
        self.assertEqual(report["length_violations"], 0)
        self.assertEqual(report["sum_violations"], 0)
        self.assertEqual(report["vectors_outside_envelope"], 1)
        self.assertEqual(report["one_tuple_iff_one_vector_violations"], 0)

    def test_the_full_envelope_reached_is_counted_as_such(self) -> None:
        early = sequenced(EMPTY, AdmitForm(1), AdmitDatum(N[0]))
        late = sequenced(EMPTY, AdmitDatum(N[0]), AdmitForm(1))
        report = du.base_report(EMPTY, [early, late])
        self.assertEqual(report["regimes_with_unreached_or_extra_tuples"], 0)
        self.assertEqual(report["vector_split_regimes"], 1)
        self.assertEqual(report["gap_split_regimes"], 0)

    def test_a_one_vector_regime_with_a_wide_envelope_is_counted(self) -> None:
        late = sequenced(EMPTY, AdmitDatum(N[0]), AdmitForm(1))
        report = du.base_report(EMPTY, [late])
        self.assertEqual(report["one_tuple_iff_one_vector_violations"], 1)
        self.assertEqual(report["regimes_reached_with_one_vector"], 1)
        self.assertEqual(report["regimes_with_one_tuple_envelope"], 0)

    def test_the_tail_only_census(self) -> None:
        pinned = sequenced(EMPTY, AdmitDatum(N[0]), AdmitDatum(N[1]), Impose(0, 1))
        bare = sequenced(EMPTY, AdmitDatum(N[0]))
        lone = sequenced(EMPTY, AdmitForm(1))
        report = du.base_report(EMPTY, [pinned, bare, lone])
        self.assertEqual(report["regimes_with_one_tuple_envelope"], 3)
        self.assertEqual(report["tail_only_regimes"], 1)

    def _population(self) -> Population:
        return Population((), (), Keys())

    def test_a_class_with_two_vectors_and_two_sums_is_counted(self) -> None:
        one = sequenced(EMPTY, AdmitDatum(N[0]), AdmitForm(1))
        other = du.Sequenced(one.history, one.regime, (1, 0))
        forged = du.Sequenced(one.history, one.regime, (1, 1))
        report = du.class_report(self._population(), {"EMPTY": EMPTY}, {"EMPTY": [one, other]})
        self.assertEqual(report["classes_with_two_vectors"], {"EMPTY": 1})
        self.assertEqual(report["classes_with_two_sums"], {"EMPTY": 0})
        report = du.class_report(self._population(), {"EMPTY": EMPTY}, {"EMPTY": [one, forged]})
        self.assertEqual(report["classes_with_two_sums"], {"EMPTY": 1})

    def test_isomorphic_regimes_with_two_envelopes_are_counted(self) -> None:
        """An instance on the first datum and one on the second: one class
        by the implemented isomorphism, two envelopes by level."""
        on_first = sequenced(EMPTY, AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitForm(1),
                             AdmitInst(0, (0,)))
        on_second = sequenced(EMPTY, AdmitDatum(N[0]), AdmitDatum(N[1]), AdmitForm(1),
                              AdmitInst(0, (1,)))
        population = self._population()
        self.assertEqual(
            population.keys.key(on_first.regime), population.keys.key(on_second.regime)
        )
        report = du.class_report(population, {"EMPTY": EMPTY}, {"EMPTY": [on_first, on_second]})
        self.assertEqual(report["classes"], {"EMPTY": 1})
        self.assertEqual(report["classes_with_two_envelopes"], {"EMPTY": 1})


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

    def test_the_envelope_is_reached_exactly(self) -> None:
        for base, row in payload()["reports"]["bases"].items():
            self.assertEqual(row["vectors_outside_envelope"], 0, base)
            self.assertEqual(row["regimes_with_unreached_or_extra_tuples"], 0, base)
            self.assertEqual(
                row["regimes_with_one_tuple_envelope"], row["regimes_reached_with_one_vector"], base
            )

    def test_the_split_counts_are_the_dated_ones(self) -> None:
        """Dated 2026-09-25 in STATUS.md."""
        bases = payload()["reports"]["bases"]
        self.assertEqual(
            {b: bases[b]["vector_split_regimes"] for b in bases}, {"EMPTY": 47, "L": 260, "F": 597}
        )
        self.assertEqual(
            {b: bases[b]["gap_split_regimes"] for b in bases}, {"EMPTY": 19, "L": 63, "F": 103}
        )
        self.assertEqual(
            {b: bases[b]["tail_only_regimes"] for b in bases}, {"EMPTY": 3, "L": 13, "F": 17}
        )


class WitnessTests(unittest.TestCase):
    def test_the_lean_witnesses_replay(self) -> None:
        """Each Lean countermodel, in the sealed Python grammar: both
        sides reach one regime and the segments differ as claimed; the
        pinned regime's envelope is one tuple, with its rest round in the
        tail."""
        report = du.witness_report()
        self.assertEqual(sorted(report), ["gap_splits", "lead_splits", "pinned_by_requirement"])
        for name, row in report.items():
            self.assertTrue(row["claim_holds"], name)
        self.assertEqual(report["lead_splits"]["segments"], [1, 0])
        self.assertEqual(report["gap_splits"]["segments"], [1, 0])
        self.assertEqual(report["pinned_by_requirement"]["vector"], [0, 0, 1])

    def test_the_witnesses_are_the_lean_histories(self) -> None:
        witnesses = du.lean_witnesses()
        left, right, position = witnesses["gap_splits"]
        self.assertEqual(position, 1)
        self.assertEqual([type(e).__name__ for e in left], ["AdmitDatum", "AdmitForm", "AdmitDatum"])
        self.assertEqual([type(e).__name__ for e in right], ["AdmitDatum", "AdmitDatum", "AdmitForm"])
        self.assertEqual(du.pinned_history()[-1], Impose(0, 1))


if __name__ == "__main__":
    unittest.main()
