"""Standard-library verification for the finite replay/lift/descent fixture."""

from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest

from finite_tower import (
    CONDITIONAL_ADMISSIONS,
    CandidateKind,
    Disposition,
    active_measure,
    aggregate_effect,
    build_tower,
    candidate_grammar,
    closure,
    degree_profile,
    descent_rejects,
    down,
    genesis,
    model_report,
    no_swap_stable_single_pair_choice,
    render_report,
    replay,
    replay_invariant,
    retained_ties,
    structural_descent,
    symmetric_single_pair_failure,
    up,
    write_report,
)


class FiniteTowerTests(unittest.TestCase):
    def test_completed_stages_cover_zero_through_fifteen(self) -> None:
        stages = build_tower(15)
        self.assertEqual(tuple(stage.index for stage in stages), tuple(range(16)))
        self.assertEqual(stages[0].admissions, CONDITIONAL_ADMISSIONS)
        self.assertIn("initial-carrier:labels-0-1", CONDITIONAL_ADMISSIONS)
        self.assertIn("seed-edge:0-1", CONDITIONAL_ADMISSIONS)
        self.assertTrue(all(active_measure(stage) == 0 for stage in stages))
        self.assertTrue(all(replay_invariant(stage).holds for stage in stages))

    def test_up_down_identity_preservation_and_closure_progress(self) -> None:
        source = genesis()
        record = up(source)
        provisional = record.target
        completed = closure(provisional)

        self.assertEqual(down(record), source)
        with self.assertRaises(ValueError):
            down(replace(record, fresh=99))
        self.assertEqual(provisional.index, source.index + 1)
        self.assertTrue(set(source.edges).issubset(provisional.edges))
        self.assertTrue(replay_invariant(provisional).holds)
        self.assertEqual(active_measure(provisional), 1)
        self.assertEqual(active_measure(completed), 0)
        self.assertTrue(replay_invariant(completed).holds)

    def test_structural_descent_agrees_with_certified_descent_and_can_fail(self) -> None:
        for stage in build_tower(15):
            record = up(stage)
            self.assertEqual(structural_descent(record.target), down(record))
            # Genesis has no history and every completed stage ends in a closure.
            with self.assertRaises(ValueError):
                structural_descent(stage)
        record = up(genesis())
        moved_anchor = replace(record.target, anchor=1)
        self.assertNotEqual(structural_descent(moved_anchor), record.source)

    def test_descent_rejects_reports_uncertified_records_without_raising(self) -> None:
        record = up(genesis())
        self.assertFalse(descent_rejects(record))
        self.assertTrue(descent_rejects(replace(record, target=closure(record.target))))
        self.assertTrue(descent_rejects(replace(record, fresh=99)))

    def test_replay_reconstructs_each_history_and_rejects_tampering(self) -> None:
        for stage in build_tower(15):
            self.assertEqual(replay(stage.history), stage)

        final = build_tower(2)[-1]
        tampered = replace(final.history[-1], parent_key="not-the-parent")
        with self.assertRaises(ValueError):
            replay(final.history[:-1] + (tampered,))

    def test_candidate_grammar_retains_every_tied_minimum(self) -> None:
        provisional = up(genesis()).target
        candidates = candidate_grammar(provisional)
        self.assertEqual(
            {candidate.kind for candidate in candidates}, set(CandidateKind)
        )
        self.assertEqual(
            {candidate.disposition for candidate in candidates},
            {
                Disposition.OPEN,
                Disposition.UNIQUE,
                Disposition.CONDITIONAL,
                Disposition.TIED,
            },
        )
        self.assertEqual(
            next(candidate for candidate in candidates
                 if candidate.code == "observer_extension").disposition,
            Disposition.OPEN,
        )
        ties = retained_ties(candidates)
        self.assertEqual(
            tuple(candidate.code for candidate in ties),
            ("aggregate_all_carrier", "aggregate_active_orbit"),
        )
        all_carrier = aggregate_effect(provisional, "aggregate_all_carrier")
        active_orbit = aggregate_effect(provisional, "aggregate_active_orbit")
        carrier = provisional.carrier + (len(provisional.carrier),)
        self.assertNotEqual(
            degree_profile(carrier, all_carrier),
            degree_profile(carrier, active_orbit),
        )

    def test_symmetric_fixture_rejects_one_pair_transport(self) -> None:
        witness = symmetric_single_pair_failure()
        self.assertTrue(witness.is_transport_failure)
        self.assertTrue(no_swap_stable_single_pair_choice())
        self.assertNotEqual(
            witness.transported_selection, witness.selection_after_transport
        )

    def test_report_is_byte_stable_and_scope_labelled(self) -> None:
        first = render_report(15)
        second = render_report(15)
        self.assertEqual(first, second)
        payload = json.loads(first)
        self.assertEqual(payload["schema"], "finite-replay-lift-descent-v1")
        self.assertEqual(len(payload["stages"]), 16)
        self.assertEqual(
            set(payload["laws_checked"]),
            {
                "descent_rejects_an_uncertified_lift_record",
                "each_emitted_round_closure_decreases_active_measure",
                "old_distinctions_are_preserved",
                "replay_invariant_holds",
                "replay_reconstructs_every_completed_stage",
                "structural_descent_inverts_each_certified_lift",
            },
        )
        self.assertTrue(all(payload["laws_checked"].values()))
        self.assertFalse(payload["retained_ties"]["same_effect"])
        self.assertEqual(payload["scope"]["status"], "conditional-finite-fixture")

    def test_writer_has_identical_bytes_at_two_destinations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "first.json"
            second = root / "nested" / "second.json"
            write_report(first)
            write_report(second)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_report_function_agrees_with_the_writer_shape(self) -> None:
        payload = model_report(15)
        self.assertEqual(payload["stages"][-1]["n"], 15)
        self.assertEqual(
            payload["negative_fixture"]["candidate"]["disposition"], "refuted"
        )


if __name__ == "__main__":
    unittest.main()
