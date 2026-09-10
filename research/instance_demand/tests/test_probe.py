from __future__ import annotations

from dataclasses import replace
import unittest
from unittest.mock import patch

from derivation.model import AdmitDatum, AdmitForm, AdmitInst, AdmissionError, Supply, replay
from derivation.observe import derivable
import probe


class StageOne(unittest.TestCase):
    def test_exhaustive_one_form_population(self) -> None:
        result = probe.sweep()
        self.assertEqual(result["states"], 1062)
        self.assertEqual(result["successful_transitions"], 17762)
        self.assertEqual(result["fresh_derivable_instances"], 2337)

    def test_original_i1_fails_nonvacuity_both_readings(self) -> None:
        for reading in ("L", "F"):
            result = probe.sample(reading, False)
            self.assertTrue(result["instance_stored"])
            self.assertTrue(result["already_separable"])
            self.assertIsNotNone(result["separating_context"])
            self.assertEqual(result["requirements"], [])
            self.assertFalse(result["contains_impose"])

    def test_uniform_control_is_collapsed_but_still_admitted(self) -> None:
        for reading in ("L", "F"):
            result = probe.sample(reading, True)
            self.assertFalse(result["already_separable"])
            self.assertIsNone(result["separating_context"])
            self.assertTrue(result["instance_event_present"])

    def test_writer_injection_names_event_and_recovers(self) -> None:
        before = replay((AdmitDatum("a"), AdmitForm(1)))
        supplied = Supply("not-admitted")
        injected = replace(before, insts=frozenset({(0, (0,))}))
        with self.assertRaisesRegex(ValueError, "INSTANCE_WRITER: Supply"):
            probe.check_step(before, supplied, injected)
        probe.check_step(before, supplied, before)

    def test_history_is_not_a_proof_of_external_choice(self) -> None:
        # The same recorded event can be returned by a program or entered by an
        # operator. This test asserts occurrence only; authorship is absent.
        history = (AdmitDatum("a"), AdmitForm(1), AdmitInst(0, (0,)))
        self.assertEqual(probe.instance_events(history), replay(history).insts)
        self.assertEqual(probe.instance_events(history + (history[-1],)), replay(history).insts)

    def test_invalid_admission_is_outside_successful_histories(self) -> None:
        with self.assertRaises(AdmissionError):
            replay((AdmitInst(0, (0,)),))

    def test_unknown_reading_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "READING"):
            probe.sample("unknown", False)

    def test_report_preserves_open_scope(self) -> None:
        result = probe.report()
        self.assertEqual(result["outcome"], "OPEN")
        self.assertEqual(result["stage"], 1)
        samples = result["samples"]
        assert isinstance(samples, list)
        self.assertEqual(len(samples), 4)

    def test_replay_mismatch_injection(self) -> None:
        history = (AdmitDatum("a"), AdmitForm(2))
        before = replay(history)
        with patch.object(probe, "configurations", return_value=iter([(history, before)])):
            with patch.object(probe, "replay", return_value=replace(before, forms=())):
                with self.assertRaisesRegex(ValueError, "REPLAY_MISMATCH"):
                    probe.sweep()
        self.assertEqual(replay(history), before)

    def test_origin_mismatch_injection(self) -> None:
        history = (AdmitDatum("a"), AdmitForm(2), AdmitInst(0, (0, 0)))
        before = replay(history)
        with patch.object(probe, "configurations", return_value=iter([(history, before)])):
            with patch.object(probe, "instance_events", return_value=frozenset()):
                with self.assertRaisesRegex(ValueError, "INSTANCE_ORIGIN"):
                    probe.sweep()
        self.assertEqual(probe.instance_events(history), before.insts)

    def test_uniformity_mismatch_injection(self) -> None:
        history = (AdmitDatum("a"), AdmitForm(2))
        before = replay(history)
        with patch.object(probe, "configurations", return_value=iter([(history, before)])):
            with patch.object(probe, "derivable", side_effect=[True, False]):
                with self.assertRaisesRegex(ValueError, "UNIFORM_CONCLUSION"):
                    probe.sweep()
        self.assertFalse(derivable(before, (0, (0, 0))))
