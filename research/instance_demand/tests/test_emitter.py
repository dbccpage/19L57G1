from __future__ import annotations

from dataclasses import replace
import unittest
from unittest.mock import patch

from derivation.model import AdmitForm, AdmitInst, Impose, Regime, Supply, replay
import emitter as e


def seed() -> Regime:
    return replay(e.history(4, ((0, 2),), ((2, 1),), True, True))


class EmitterTests(unittest.TestCase):
    def test_full_report(self) -> None:
        report = e.report()
        self.assertEqual(report["stage"], 3)
        self.assertEqual(report["outcome"], "OPEN")
        self.assertEqual(len(tuple(e.configurations())), 5140)
        self.assertIn("REFUTED", str(report["native_inference"]))

    def test_ambiguous_graph_retains_every_output_and_refuses_unique_lookup(self) -> None:
        r = replay(e.history(4, ((0, 2), (0, 3)), ((2, 1), (3, 2)), True, True))
        self.assertEqual(e.raw_outputs(r.insts), ((5, (0, 1)), (5, (0, 2))))
        self.assertFalse(e.functional(r.insts, 3))
        self.assertIsNone(e.lookup_unique(r.insts, 3, 0))
        self.assertIsNone(e.eval_word(r.insts, (0, 1), 0))
        after, events = e.emit(r)
        e.audit(r, after, events)
        self.assertEqual(e.eval_word(r.insts, (), 0), 0)

    def test_distinct_paths_can_have_same_output(self) -> None:
        r = replay(e.history(4, ((0, 2), (0, 3)), ((2, 1), (3, 1)), True, True))
        after, events = e.emit(r)
        self.assertEqual(len(events), 2)
        self.assertEqual(len(after.insts - r.insts), 1)
        e.audit(r, after, events)
        self.assertEqual(e.emit(after), (after, ()))

    def test_missing_instruction_or_edge_disables_output(self) -> None:
        r = seed()
        for item in r.insts:
            smaller = replace(r, insts=r.insts - {item})
            self.assertEqual(e.raw_outputs(smaller.insts), ())

    def test_emission_does_not_use_requirements(self) -> None:
        r = seed()
        changed = replay((Impose(0, 1),), base=r)
        self.assertEqual(e.raw_outputs(changed.insts), e.raw_outputs(r.insts))
        after, events = e.emit(changed)
        self.assertEqual(after.reqs, changed.reqs)
        e.audit(changed, after, events)

    def test_output_shape_is_checked_before_admission(self) -> None:
        r = replay((AdmitInst(0, (0, 1, 3)),), base=seed())
        self.assertIn((6, (0, 1)), e.raw_outputs(r.insts))
        self.assertNotIn((6, (0, 1)), e.pending(r))
        unary = replay((AdmitForm(1),), base=r)
        self.assertNotIn((6, (0, 1)), e.pending(unary))
        self.assertFalse(e.well_formed(r, (5, (0, 9))))
        self.assertFalse(e.well_formed(r, (-1, (0, 1))))

    def test_program_controls_output_form(self) -> None:
        r = replay((AdmitForm(2), AdmitInst(0, (0, 1, 3))), base=seed())
        self.assertEqual(set(e.pending(r)), {(5, (0, 1)), (6, (0, 1))})
        after, events = e.emit(r)
        e.audit(r, after, events)

    def test_bad_raw_output_is_rejected(self) -> None:
        r = seed()
        after, events = e.emit(r)
        with patch.object(e, "raw_outputs", return_value=()):
            with self.assertRaisesRegex(ValueError, "PATH_POPULATION"):
                e.audit(r, after, events)

    def test_wrong_endpoint_or_trace_is_rejected(self) -> None:
        r = seed()
        after, events = e.emit(r)
        with self.assertRaisesRegex(ValueError, "EMISSION_ENDPOINT"):
            e.audit(r, r, events)
        for bad in ((), (Supply("x"),), (AdmitInst(5, (0, 2)),)):
            with self.assertRaisesRegex(ValueError, "EMISSION_TRACE"):
                e.audit(r, after, bad)
        with patch.object(e, "replay", return_value=r):
            with self.assertRaisesRegex(ValueError, "EMISSION_REPLAY"):
                e.audit(r, after, events)
        e.audit(r, after, events)

    def test_wrong_execution_output_is_rejected(self) -> None:
        r = seed()
        after, events = e.emit(r)
        with patch.object(e, "eval_word", return_value=3):
            with self.assertRaisesRegex(ValueError, "EXECUTION_BRIDGE"):
                e.audit(r, after, events)

    def test_wrong_whole_history_and_no_program_output_are_rejected(self) -> None:
        history = e.history(4, ((0, 2),), ((2, 1),), True, True)
        r = replay(history)
        after, events = e.emit(r)
        with patch.object(e, "configurations", return_value=iter((history,))), \
             patch.object(e, "emit", return_value=(after, events)), \
             patch.object(e, "audit", return_value=0), patch.object(e, "replay", side_effect=(r, r)):
            with self.assertRaisesRegex(ValueError, "WHOLE_HISTORY"):
                e.sweep()
        no_program = e.history(4, ((0, 2),), ((2, 1),), False, True)
        r = replay(no_program)
        after = replay(events, base=r)
        with patch.object(e, "configurations", return_value=iter((no_program,))), \
             patch.object(e, "emit", return_value=(after, events)), patch.object(e, "audit", return_value=0):
            with self.assertRaisesRegex(ValueError, "MISSING_INSTRUCTION"):
                e.sweep()

    def test_samples_distinguish_derivability_and_unmet_demand(self) -> None:
        for reading in ("L", "F"):
            unruled = e.sample(reading, False)
            covered = e.sample(reading, True)
            self.assertFalse(unruled["payload_previously_derivable"])
            self.assertTrue(unruled["pair_already_separated_by_emission"])
            self.assertTrue(covered["payload_previously_derivable"])
            self.assertFalse(covered["pair_already_separated_by_emission"])
            self.assertTrue(covered["whole_response_replay"])
            self.assertEqual(covered["outputs_without_instruction"], ())
            self.assertTrue(covered["same_profiles_without_instruction"])
        with self.assertRaisesRegex(ValueError, "READING"):
            e.sample("unknown", True)

    def test_bad_sample_witnesses_are_rejected(self) -> None:
        with patch.object(e, "separable", return_value=True):
            with self.assertRaisesRegex(ValueError, "SAMPLE_BOUNDARY"):
                e.sample("L", True)
        with patch.object(e, "separable", return_value=False):
            with self.assertRaisesRegex(ValueError, "SAMPLE_RESPONSE"):
                e.sample("L", True)
