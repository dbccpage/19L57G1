"""Tests for the rung-two track-one cross-check.

Every positive check is paired with a negative one wherever a green test
would otherwise discharge nothing: a check that cannot fail is not a
check.  The negatives here are the ones the seed asks for -- smuggling, a
false minimum, and a bundled claim -- specialised to this rung:

* a stake that returns a value outside the three labels is refused, not
  silently accepted (smuggling a fourth label);
* the demand classifier and the independently written honour walk agree,
  AND a deliberately inconsistent stake makes them disagree, so the
  totality check is not a tautology;
* the free stake carries no demand, AND a labelling stake does carry one,
  so the emptiness result is not vacuous;
* the two enumerators agree, AND a truncated second enumerator disagrees,
  so the cross-check bites;
* the at-most-one measurement reports more than one when it is fed a
  regime that breaks the bound, so the reported bound is a measurement
  and not a constant.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import nofirst as nf  # noqa: E402
import run_nofirst as rn  # noqa: E402
import verify_pins as vp  # noqa: E402
from derivation.engine import READINGS  # noqa: E402
from derivation.model import (  # noqa: E402
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    Supply,
    replay,
    step,
)

# A small declared rectangle, used everywhere a test does not need the
# full one.  The full rectangle is exercised once, by the runner.
SMALL = nf.Alphabet(
    supply_token="<z>",
    fresh_tokens=("<n0>", "<n1>"),
    arities=(1, 2),
    max_data=3,
    max_forms=1,
    max_length=2,
)

L = READINGS[0]
F = READINGS[1]


class StakeTests(unittest.TestCase):
    def test_diagonal_is_free_whatever_the_rule_says(self) -> None:
        """The diagonal is free by construction, as the Lean structure's
        field requires, even when the rule would say otherwise."""
        s = nf.Stake("always_apart", lambda i, j: nf.APART)
        self.assertEqual(s.label(2, 2), nf.FREE)
        self.assertEqual(s.label(0, 1), nf.APART)

    def test_label_is_symmetric_by_normalisation(self) -> None:
        s = nf.Stake("chainish", lambda i, j: nf.APART if j - i == 1 else nf.FREE)
        self.assertEqual(s.label(1, 2), s.label(2, 1))
        self.assertEqual(s.label(0, 2), nf.FREE)

    def test_a_fourth_label_is_refused(self) -> None:
        """NEGATIVE: a stake smuggling a value outside the three labels
        raises rather than being carried silently into a demand set."""
        s = nf.Stake("smuggle", lambda i, j: "elsewhere")
        with self.assertRaises(ValueError):
            s.label(0, 1)

    def test_declared_stakes_are_the_seven_declared(self) -> None:
        names = [s.name for s in nf.declared_stakes()]
        self.assertEqual(names[0], "free")
        self.assertEqual(names[-1], "one_sided_total")
        self.assertEqual(len(names), 7)
        self.assertIn("total_apart", names)
        self.assertIn("chain", names)

    def test_one_sided_total_labels_nothing_same(self) -> None:
        """A one-sided commitment cannot ask for a collapse, so the stake
        it induces labels nothing same -- the Lean ``ofCommitment``."""
        s = nf.stake_of_one_sided_total()
        labels = {s.label(i, j) for i in range(4) for j in range(4)}
        self.assertNotIn(nf.SAME, labels)
        self.assertEqual(labels, {nf.APART, nf.FREE})


class ObservationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = replay(L.genesis)

    def test_honour_of_a_free_pair_is_unconditional(self) -> None:
        self.assertTrue(nf.honour(self.base, nf.FREE, 0, 1))

    def test_apart_is_dishonoured_at_a_collapsed_pair(self) -> None:
        """With no admitted form the pair is collapsed, so an apart label
        is not honoured and a same label is."""
        self.assertFalse(nf.honour(self.base, nf.APART, 0, 1))
        self.assertTrue(nf.honour(self.base, nf.SAME, 0, 1))

    def test_classifier_and_honour_walk_agree(self) -> None:
        apart = nf.all_apart_stake()
        for r in (self.base, replay(F.genesis)):
            ds = tuple(p for _, p in nf.demands(apart, r))
            self.assertEqual(ds, nf.dishonoured_labelled_pairs(apart, r))

    def test_negative_the_totality_check_can_disagree(self) -> None:
        """NEGATIVE: the agreement above is a check, not a tautology.  A
        stake whose rule is not a function of the pair alone makes the two
        walks disagree, and the receipt's totality counter would fire."""
        flips = {"n": 0}

        def unstable(i: int, j: int) -> str:
            flips["n"] += 1
            return nf.APART if flips["n"] % 2 else nf.SAME

        s = nf.Stake("unstable", unstable)
        r = self.base
        agree = tuple(p for _, p in nf.demands(s, r)) == (
            nf.dishonoured_labelled_pairs(s, r)
        )
        self.assertFalse(agree)

    def test_empty_profile_data_at_a_formless_regime(self) -> None:
        """With no form there is no context, so every datum's profile is
        empty."""
        self.assertEqual(nf.empty_profile_data(self.base), (0, 1))

    def test_free_stake_is_empty_and_a_labelling_stake_is_not(self) -> None:
        """Paired: emptiness under the free stake is not vacuous, because
        the same regime carries a demand under a labelling stake."""
        self.assertEqual(nf.demands(nf.FREE_STAKE, self.base), ())
        self.assertNotEqual(nf.demands(nf.all_apart_stake(), self.base), ())


class AlphabetTests(unittest.TestCase):
    def test_arg_tuples_count(self) -> None:
        self.assertEqual(list(nf._arg_tuples(0, 3)), [()])
        self.assertEqual(len(list(nf._arg_tuples(1, 3))), 3)
        self.assertEqual(len(list(nf._arg_tuples(2, 3))), 9)

    def test_datum_admission_withheld_at_the_data_bound(self) -> None:
        r = replay(L.genesis)
        tiny = nf.Alphabet("<z>", ("<a>",), (1,), max_data=2, max_forms=1,
                           max_length=1)
        kinds = {nf.event_kind(e) for e in nf.alphabet_at(r, tiny, 0)}
        self.assertNotIn("AdmitDatum", kinds)

    def test_datum_admission_withheld_when_tokens_run_out(self) -> None:
        r = replay(L.genesis)
        tiny = nf.Alphabet("<z>", ("<a>",), (1,), max_data=9, max_forms=1,
                           max_length=1)
        kinds = {nf.event_kind(e) for e in nf.alphabet_at(r, tiny, 1)}
        self.assertNotIn("AdmitDatum", kinds)

    def test_form_admission_withheld_at_the_form_bound(self) -> None:
        r = step(replay(L.genesis), AdmitForm(2))
        tiny = nf.Alphabet("<z>", ("<a>",), (1, 2), max_data=5, max_forms=1,
                           max_length=1)
        kinds = {nf.event_kind(e) for e in nf.alphabet_at(r, tiny, 0)}
        self.assertNotIn("AdmitForm", kinds)

    def test_instances_and_rules_appear_once_a_form_is_admitted(self) -> None:
        r = step(replay(L.genesis), AdmitForm(2))
        kinds = {nf.event_kind(e) for e in nf.alphabet_at(r, SMALL, 0)}
        self.assertIn("AdmitInst", kinds)
        self.assertIn("AdmitRuleAll", kinds)

    def test_impositions_cover_every_held_pair(self) -> None:
        r = replay(F.genesis)
        imposes = [e for e in nf.alphabet_at(r, SMALL, 0) if isinstance(e, Impose)]
        self.assertEqual(len(imposes), 3)


class EnumeratorTests(unittest.TestCase):
    def test_root_is_the_reading_genesis(self) -> None:
        nodes, _, _ = nf.enumerate_rectangle(L.genesis, SMALL)
        self.assertEqual(nodes[0].history, ())
        self.assertEqual(nodes[0].regime, replay(L.genesis))

    def test_no_sequence_exceeds_the_declared_length(self) -> None:
        nodes, _, _ = nf.enumerate_rectangle(L.genesis, SMALL)
        self.assertTrue(all(len(n.history) <= SMALL.max_length for n in nodes))

    def test_bounds_and_refusals_are_counted_apart(self) -> None:
        nodes, bounds, refusals = nf.enumerate_rectangle(L.genesis, SMALL)
        self.assertGreater(len(nodes), 1)
        self.assertGreaterEqual(bounds, 0)
        self.assertGreaterEqual(refusals, 0)

    def test_the_two_enumerators_reach_the_same_regimes(self) -> None:
        for reading in (L, F):
            a, _, _ = nf.enumerate_rectangle(reading.genesis, SMALL)
            reach_a = frozenset(n.regime for n in a)
            reach_b, _ = nf.enumerate_by_levels(
                reading.genesis, SMALL, SMALL.max_length
            )
            self.assertEqual(reach_a, reach_b)

    def test_negative_a_truncated_second_enumerator_disagrees(self) -> None:
        """NEGATIVE: the cross-check bites.  Running the second enumerator
        one level short makes the two reaches differ, so agreement above is
        evidence and not an artefact of both walks being the same walk."""
        a, _, _ = nf.enumerate_rectangle(L.genesis, SMALL)
        reach_a = frozenset(n.regime for n in a)
        reach_b, _ = nf.enumerate_by_levels(
            L.genesis, SMALL, SMALL.max_length - 1
        )
        self.assertNotEqual(reach_a, reach_b)


class FirstDemandTests(unittest.TestCase):
    def test_no_demand_under_the_free_stake_anywhere(self) -> None:
        fd = nf.first_demand(L.genesis, (Supply("<z>"), AdmitDatum("<q>")),
                             nf.FREE_STAKE)
        self.assertIsNone(fd.index)
        self.assertIsNone(fd.kind)
        self.assertIsNone(fd.dishonoured_index)

    def test_a_demand_at_genesis_is_recorded_at_index_zero(self) -> None:
        fd = nf.first_demand(L.genesis, (), nf.all_apart_stake())
        self.assertEqual(fd.index, 0)
        self.assertEqual(fd.kind, "genesis")
        self.assertEqual(fd.dishonoured_index, 0)

    def test_first_demand_and_first_dishonour_coincide(self) -> None:
        """The two indices are computed by separate tests inside the same
        walk; they agreeing is the content of the frozen prediction."""
        chain = (AdmitForm(2), AdmitRuleAll(0), Impose(0, 1))
        for stake in nf.declared_stakes():
            fd = nf.first_demand(F.genesis, chain, stake)
            self.assertEqual(fd.index, fd.dishonoured_index)

    def test_non_inert_admission_can_trigger_the_first_demand(self) -> None:
        """A declaration supplies the label, not the first-occurrence
        event.  This witness is why the general temporal claim stays OPEN:
        an instance admission is recorded as the first-demand trigger."""
        s = nf.stake_of_commitment(nf.commitment_named("total_same"))
        history = (AdmitForm(1), AdmitInst(0, (0,)))
        fd = nf.first_demand(F.genesis, history, s)
        self.assertEqual(fd.index, 2)
        self.assertEqual(fd.kind, "AdmitInst")

    def test_two_datum_admissions_witness_a_later_first_demand(self) -> None:
        """A second independent witness uses a different non-inert kind.

        The all-apart declaration is present before the run, but its first
        demand appears only when the second datum is admitted.
        """
        history = (AdmitDatum("<a>"), AdmitDatum("<b>"))
        fd = nf.first_demand((), history, nf.all_apart_stake())
        self.assertEqual(fd.index, 2)
        self.assertEqual(fd.kind, "AdmitDatum")

    def test_ledger_does_not_turn_label_source_into_event_source(self) -> None:
        ledger = (HERE / "CLAIM_LEDGER.md").read_text(encoding="utf-8")
        self.assertIn(
            "sentence concluding that the first\ndemand of any run has one source",
            ledger,
        )
        self.assertIn(
            "A general first-demand index over an arbitrary run is NOT proved",
            ledger,
        )


class InertiaTests(unittest.TestCase):
    def test_supply_and_imposition_are_inert_in_the_small_rectangle(self) -> None:
        nodes, _, _ = nf.enumerate_rectangle(F.genesis, SMALL)
        inert, exercised = nf.inert_event_kinds(
            replay(F.genesis), nodes, nf.declared_stakes()
        )
        self.assertIn("Supply", inert)
        self.assertIn("Impose", inert)
        self.assertTrue(set(inert) <= set(exercised))

    def test_admitting_a_form_is_inert(self) -> None:
        """The finding that missed prediction N-16 and became the Lean
        theorem ``admitForm_preserves_demands``: a form carries no
        instance and no rule, so it moves no profile."""
        for reading in (L, F):
            r = replay(reading.genesis)
            after = step(r, AdmitForm(2))
            for s in nf.declared_stakes():
                self.assertEqual(nf.demands(s, r), nf.demands(s, after))

    def test_admitting_an_instance_is_not_inert(self) -> None:
        """NEGATIVE: inertia is a property of some kinds, not of all.  An
        instance admission changes a demand set, so the inert set is not
        everything."""
        r = step(step(replay(F.genesis), AdmitForm(1)), AdmitInst(0, (0,)))
        s = nf.all_apart_stake()
        before = step(replay(F.genesis), AdmitForm(1))
        self.assertNotEqual(nf.demands(s, before), nf.demands(s, r))

    def test_kind_occurrences_counts_every_event(self) -> None:
        nodes, _, _ = nf.enumerate_rectangle(L.genesis, SMALL)
        counts = nf.kind_occurrences(nodes)
        self.assertEqual(sum(counts.values()), sum(len(n.history) for n in nodes))


class AtMostOneTests(unittest.TestCase):
    def test_a_demand_free_all_apart_regime_has_at_most_one_empty_profile(
        self,
    ) -> None:
        nodes, _, _ = nf.enumerate_rectangle(F.genesis, SMALL)
        apart = nf.all_apart_stake()
        for node in nodes:
            if nf.demands(apart, node.regime):
                continue
            self.assertLessEqual(len(nf.empty_profile_data(node.regime)), 1)

    def test_negative_the_empty_profile_count_is_measured_not_asserted(
        self,
    ) -> None:
        """NEGATIVE: the bound above is a measurement.  A regime that is
        NOT demand-free under the all-apart stake does carry two empty
        profiles, so the counter can report more than one."""
        r = replay(F.genesis)
        self.assertNotEqual(nf.demands(nf.all_apart_stake(), r), ())
        self.assertGreater(len(nf.empty_profile_data(r)), 1)

    def test_growth_from_a_demand_free_regime_adds_at_most_one(self) -> None:
        nodes, _, _ = nf.enumerate_rectangle(F.genesis, SMALL)
        apart = nf.all_apart_stake()
        for node in nodes:
            if nf.demands(apart, node.regime):
                continue
            if node.regime.n_data() >= SMALL.max_data:
                continue
            grown = nf.grow_once(node.regime, "<grow>")
            fresh = grown.n_data() - 1
            new = [p for _, p in nf.demands(apart, grown) if fresh in p]
            self.assertLessEqual(len(new), 1)


class RunnerTests(unittest.TestCase):
    def test_measure_reading_reports_the_declared_shape(self) -> None:
        payload = rn.measure_reading(
            "L", L.genesis, nf.declared_stakes(), SMALL, 1
        )
        self.assertEqual(payload["reading"], "L")
        self.assertEqual(payload["genesis_data"], 2)
        self.assertEqual(payload["demands"]["free_stake_nodes_with_a_demand"], 0)
        self.assertEqual(payload["demands"]["demands_at_an_unlabelled_pair"], 0)
        self.assertEqual(payload["demands"]["totality_mismatches"], 0)
        self.assertTrue(payload["crosscheck"]["reach_agrees"])

    def test_scoring_is_mechanical_and_records_a_miss(self) -> None:
        """A fabricated reading with a free-stake demand must score N-13 a
        MISS: the scorer reads the values and does not assume them."""
        good = rn.measure_reading("L", L.genesis, nf.declared_stakes(), SMALL, 1)
        bad = json.loads(json.dumps(good))
        bad["demands"]["free_stake_nodes_with_a_demand"] = 1
        self.assertEqual(rn.score([good])["N-13"]["verdict"], "HIT")
        self.assertEqual(rn.score([bad])["N-13"]["verdict"], "MISSED")

    def test_extrapolation_is_pending_and_not_scored_here(self) -> None:
        good = rn.measure_reading("L", L.genesis, nf.declared_stakes(), SMALL, 1)
        self.assertEqual(rn.score([good])["N-X"]["verdict"], "PENDING")

    def test_receipt_regenerates_byte_identically(self) -> None:
        payload = rn.build(SMALL, 1)
        with tempfile.TemporaryDirectory() as tmp:
            a = rn.write(payload, pathlib.Path(tmp) / "a")
            b = rn.write(rn.build(SMALL, 1), pathlib.Path(tmp) / "b")
            self.assertEqual(a.read_bytes(), b.read_bytes())
            self.assertNotIn(b"\r", a.read_bytes())

    def test_receipt_carries_no_input_count_claim(self) -> None:
        """FW-COUNT: this rung claims no change to the declared-input
        count in either direction."""
        payload = rn.build(SMALL, 1)
        self.assertEqual(payload["input_count_claim"], "none")
        self.assertEqual(payload["authority_effect"], "None")

    def test_receipt_pins_the_frozen_texts(self) -> None:
        """The runner hashing the frozen texts from disk is the second
        half of the pin; the first half is verify_pins.py reading blobs."""
        payload = rn.build(SMALL, 1)
        manifest = json.loads(
            (HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        )
        frozen = {f["path"]: f["sha256"] for f in manifest["frozen_texts"]}
        self.assertEqual(
            payload["prompt_sha256"],
            frozen["research/second_nofirst/PROMPT.md"],
        )
        self.assertEqual(
            payload["predictions_sha256"],
            frozen["research/second_nofirst/PREDICTIONS.md"],
        )

    def test_committed_receipt_matches_a_fresh_run(self) -> None:
        """The committed receipt is the full rectangle, regenerated here
        and compared byte for byte."""
        committed = (HERE / "receipts" / "nofirst.json").read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            fresh = rn.write(rn.build(), pathlib.Path(tmp))
            self.assertEqual(committed, fresh.read_bytes())

    def test_main_writes_a_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, str(HERE / "run_nofirst.py"), "--receipts", tmp],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue((pathlib.Path(tmp) / "nofirst.json").exists())


class PinTests(unittest.TestCase):
    def test_pins_verify(self) -> None:
        lines = vp.verify()
        self.assertTrue(any(line.startswith("snapshot commit:") for line in lines))
        self.assertTrue(any(line.startswith("span:") for line in lines))
        self.assertTrue(any(line.startswith("frozen:") for line in lines))

    def test_every_declared_span_is_verified(self) -> None:
        manifest = json.loads(
            (HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        )
        lines = vp.verify()
        self.assertEqual(
            sum(1 for line in lines if line.startswith("span:")),
            len(manifest["spans"]),
        )

    def test_unsafe_paths_are_refused(self) -> None:
        """NEGATIVE: a manifest path escaping the repository is refused
        before any blob is read."""
        for bad in ("../outside", "/etc/passwd", "", 7):
            with self.assertRaises(ValueError):
                vp._safe(bad)

    def test_a_span_past_the_end_of_a_file_is_named(self) -> None:
        """NEGATIVE: a span running past the file fails by name rather
        than silently hashing a short segment."""
        from pathlib import PurePosixPath

        with self.assertRaises(ValueError) as caught:
            vp._span_sha256(
                "HEAD", PurePosixPath("research/second_nofirst/PROMPT.md"),
                1, 100000,
            )
        self.assertIn("runs past the end", str(caught.exception))

    def test_span_hashing_is_line_ending_insensitive(self) -> None:
        from pathlib import PurePosixPath

        p = PurePosixPath("research/second/PLAN.md")
        self.assertEqual(
            vp._span_sha256("HEAD", p, 26, 32),
            "fcb11a68c5a283d0a4c59110e270d60e97166baef8769b6778a2a8626b82196a",
        )

    def test_a_missing_git_object_is_reported(self) -> None:
        from pathlib import PurePosixPath

        with self.assertRaises(ValueError):
            vp._blob_sha256("HEAD", PurePosixPath("research/second_nofirst/absent"))

    def test_ancestor_reports_an_unusable_revision_as_undecided(self) -> None:
        """NEGATIVE: a git exit other than zero or one is reported as
        undecided, never silently as "not an ancestor" -- the distinction
        the rung-zero verifier records."""
        self.assertTrue(vp._ancestor("0" * 40).startswith("undecided"))
        head = vp._git("rev-parse", "HEAD")
        self.assertEqual(vp._ancestor(head), "ancestor")

    def test_the_local_verifier_is_not_shadowed_by_a_sibling(self) -> None:
        """NEGATIVE: the sibling two-sided tree also carries a
        `verify_pins`; this asserts the module under test is this rung's,
        by a member only this one has."""
        self.assertTrue(vp.__file__.replace("\\", "/").endswith(
            "research/second_nofirst/verify_pins.py"))
        self.assertTrue(hasattr(vp, "_span_sha256"))

    def test_int_field_is_typed(self) -> None:
        with self.assertRaises(ValueError):
            vp._int({"first_line": "3"}, "first_line")


if __name__ == "__main__":
    unittest.main()
