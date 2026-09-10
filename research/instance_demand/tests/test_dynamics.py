from __future__ import annotations

from dataclasses import replace
import unittest
from unittest.mock import patch

from derivation.model import AdmissionError, AdmitForm, AdmitInst, Impose, Regime, replay
import dynamics as d
import emitter as e


def chain() -> Regime:
    return replay(d.history(4, ((0, 1), (1, 2), (2, 3)), True, True))


class DynamicsTests(unittest.TestCase):
    def test_complete_census_and_claim_assessment(self) -> None:
        report = d.report()
        self.assertEqual(report["stage"], 4)
        self.assertEqual(report["outcome"], "OPEN")
        self.assertEqual(len(tuple(d.configurations())), 2124)
        self.assertIn("OPEN", str(report["E1"]))
        self.assertIn("NOT_SATISFIED", str(report["E2_literal"]))

    def test_chain_needs_two_rounds_and_retains_duplicate_path_events(self) -> None:
        r = chain()
        result = d.run(r)
        d.audit(r, result)
        self.assertEqual(d.budget(r), 61)
        self.assertEqual([len(batch) for batch in result.batches], [2, 2])
        self.assertEqual([len(b.insts - a.insts) for a, b in zip(result.states, result.states[1:])], [2, 1])
        self.assertEqual(d.run(result.states[-1]), d.Run((result.states[-1],), ()))
        self.assertEqual(d.reference_closure(r), result.states[-1].insts)
        self.assertIn((3, (0, 3)), result.states[-1].insts)
        self.assertTrue(e.functional(r.insts, 3))
        self.assertFalse(e.functional(result.states[1].insts, 3))

    def test_covered_chain_stays_unmet_until_existing_response(self) -> None:
        covered = d.chain_sample(True)
        self.assertFalse(covered["payload_initially_stored"])
        self.assertTrue(covered["payload_initially_derivable"])
        self.assertFalse(covered["pair_initially_separable"])
        self.assertFalse(covered["pair_terminal_separable"])
        self.assertTrue(covered["whole_response_replay"])
        self.assertTrue(covered["answered_payload_retained"])
        unruled = d.chain_sample(False)
        self.assertFalse(unruled["payload_initially_derivable"])
        self.assertTrue(unruled["pair_initially_separable"])
        self.assertTrue(unruled["whole_replay"])

    def test_multiple_instructions_with_reused_output_forms(self) -> None:
        r = replay(d.history(4, ((0, 1), (2, 3)), False, True) + (
            AdmitForm(2), AdmitInst(4, (1, 2)), AdmitInst(0, (0, 1, 0)), AdmitInst(0, (0, 0, 1))))
        result = d.run(r)
        d.audit(r, result)
        self.assertIn((3, (0, 2)), result.states[-1].insts)
        self.assertIn((4, (0, 3)), result.states[-1].insts)
        self.assertEqual(e.instructions(r.insts), e.instructions(result.states[-1].insts))

    def test_no_program_empty_carrier_and_invalid_output_shape(self) -> None:
        for n in (0, 1):
            r = replay(d.history(n, (), False, False))
            result = d.run(r)
            d.audit(r, result)
            self.assertEqual(result.batches, ())
        r = replay(d.history(4, ((0, 1), (1, 2)), False, False) + (
            AdmitInst(0, (0, 0, 1)),))
        self.assertEqual(d.run(r).batches, ())
        unary = replay((AdmitForm(1),), base=r)
        d.audit(unary, d.run(unary))
        self.assertEqual(d.run(unary).batches, ())

    def test_existing_requirements_preserved_through_all_rounds(self) -> None:
        r = replay((Impose(0, 3),), base=chain())
        result = d.run(r)
        d.audit(r, result)
        for state in result.states:
            self.assertEqual(state.reqs, r.reqs)
        self.assertFalse(any(isinstance(event, Impose) for batch in result.batches for event in batch))

    def test_malformed_initial_state_refused(self) -> None:
        r = replace(chain(), insts=frozenset({(3, (0, 9))}))
        with self.assertRaisesRegex(AdmissionError, "INSTANCE_SHAPE"):
            d.run(r)
        with self.assertRaisesRegex(AdmissionError, "INSTANCE_SHAPE"):
            d.audit(r, d.Run((r,), ()))

    def test_population_and_empty_batch_controls(self) -> None:
        r = chain()
        for result in (d.Run((), ()), d.Run((replace(r, reqs=frozenset({(0, 3)})),), ()),
                       d.Run((r, r), ())):
            with self.assertRaisesRegex(ValueError, "ROUND_POPULATION"):
                d.audit(r, result)
        with self.assertRaisesRegex(ValueError, "EMPTY_RECORDED_BATCH"):
            d.audit(r, d.Run((r, r), ((),)))

    def test_wrong_endpoint_and_premature_stop_refused(self) -> None:
        r = chain()
        result = d.run(r)
        with self.assertRaisesRegex(ValueError, "EMISSION_ENDPOINT"):
            d.audit(r, d.Run((r, r), (result.batches[0],)))
        with self.assertRaisesRegex(ValueError, "TERMINAL_NOT_CLOSED"):
            d.audit(r, d.Run((r,), ()))

    def test_independent_instruction_and_decrease_controls(self) -> None:
        r = chain()
        fake = (AdmitInst(3, (0, 2)),)
        changed = replace(r, insts=r.insts | {(0, (0, 0, 1))})
        with patch.object(e, "audit"):
            with self.assertRaisesRegex(ValueError, "INSTRUCTIONS_CHANGED"):
                d.audit(r, d.Run((r, changed), (fake,)))
            with self.assertRaisesRegex(ValueError, "NO_STRICT_DECREASE"):
                d.audit(r, d.Run((r, r), (fake,)))

    def test_bound_controls_and_changed_empty_round_refused(self) -> None:
        r = chain()
        result = d.run(r)
        with patch.object(d, "budget", return_value=0):
            with self.assertRaisesRegex(ValueError, "ROUND_BOUND_EXCEEDED"):
                d.run(r)
            with self.assertRaisesRegex(ValueError, "ROUND_BOUND$"):
                d.audit(r, result)
        with patch.object(e, "emit", return_value=(replace(r, insts=frozenset()), ())):
            with self.assertRaisesRegex(ValueError, "EMPTY_ROUND_CHANGED"):
                d.run(r)

    def test_least_extension_and_replay_controls(self) -> None:
        r = chain()
        result = d.run(r)
        with patch.object(d, "reference_closure", return_value=r.insts):
            with self.assertRaisesRegex(ValueError, "TERMINAL_NOT_LEAST"):
                d.audit(r, result)
        with patch.object(d, "replay", return_value=r):
            with self.assertRaisesRegex(ValueError, "DYNAMICS_REPLAY"):
                d.audit(r, result)
        d.audit(r, result)

    def test_whole_history_and_response_controls(self) -> None:
        seed = d.history(4, ((0, 1), (1, 2), (2, 3)), True, True)
        r = replay(seed)
        terminal = d.run(r).states[-1]
        with patch.object(d, "configurations", return_value=iter((seed,))), \
             patch.object(d, "replay", side_effect=(r, terminal, r)):
            with self.assertRaisesRegex(ValueError, "DYNAMICS_WHOLE_HISTORY"):
                d.sweep()
        with patch.object(d, "separable", return_value=False):
            with self.assertRaisesRegex(ValueError, "CHAIN_RESPONSE"):
                d.chain_sample(True)
