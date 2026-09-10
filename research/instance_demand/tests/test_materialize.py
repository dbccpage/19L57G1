from __future__ import annotations

from dataclasses import replace
import unittest
from unittest.mock import patch

from derivation.model import (
    AdmissionError, AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll,
    Event, Impose, Regime, Supply, replay,
)
import materialize as m


def base() -> Regime:
    return replay((AdmitDatum("a"), AdmitDatum("b"), AdmitForm(2), AdmitRuleAll(0)))


class MaterializationTests(unittest.TestCase):
    def test_exhaustive_binary_rectangle(self) -> None:
        self.assertEqual(m.sweep(), {"states": 1062, "new_admissions": 2337,
                                    "verified_fixed_points": 1062, "data_bound": 3,
                                    "binary_forms": 1, "requirements_per_state": 0})

    def test_mixed_arities_existing_requirements_and_unruled_instances(self) -> None:
        r = replay((AdmitForm(1), AdmitForm(3), AdmitRuleAll(2),
                    AdmitInst(1, (0,)), Impose(0, 1)), base=base())
        after, events = m.materialize(r)
        self.assertEqual(len(events), 12)
        self.assertEqual(after.reqs, r.reqs)
        self.assertIn((1, (0,)), after.insts)
        self.assertNotIn((1, (1,)), after.insts)
        m.audit(r, after, events)
        self.assertEqual(m.materialize(after), (after, ()))
        self.assertEqual(m.read_pairs(after), ((0, 1),))

    def test_reader_retains_all_alternatives(self) -> None:
        r = replay((AdmitDatum("c"),), base=base())
        after, _ = m.materialize(r)
        self.assertEqual(m.read_pairs(after), ((0, 1), (0, 2), (1, 2)))
        self.assertEqual(m.read_pairs(r), ())
        self.assertEqual(m.read_pairs(replace(after, reqs=frozenset({(0, 1)}))), m.read_pairs(after))
        self.assertEqual(m.read_pairs(replace(r, insts=frozenset({(0, (0,)), (1, (0, 1))}))), ())

    def test_invalid_direct_states_are_rejected(self) -> None:
        r = base()
        invalid = [replace(r, forms=(0,)), replace(r, rules=frozenset({1})),
                   replace(r, insts=frozenset({(-1, (0, 1))})),
                   replace(r, insts=frozenset({(0, (0,))})),
                   replace(r, insts=frozenset({(0, (0, 2))})),
                   replace(r, reqs=frozenset({(1, 0)}))]
        for bad in invalid:
            with self.assertRaises(AdmissionError):
                m.materialize(bad)

    def test_audit_rejects_missing_extra_or_changed_payload(self) -> None:
        r = base()
        after, events = m.materialize(r)
        for bad, error in ((replace(after, insts=after.insts - {(0, (0, 1))}), "CLOSURE"),
                           (replace(after, insts=after.insts | {(1, (0,))}), "CLOSURE"),
                           (replace(after, reqs=frozenset({(0, 1)})), "FIELDS")):
            with self.assertRaisesRegex(ValueError, error):
                m.audit(r, bad, events)
        m.audit(r, after, events)

    def test_audit_rejects_duplicate_wrong_or_noninstance_events(self) -> None:
        r = base()
        after, events = m.materialize(r)
        for bad in (events + events[:1], (Supply("x"),) + events[1:],
                    events[:1] + events[:1] + events[2:]):
            with self.assertRaisesRegex(ValueError, "ADMISSION_TRACE"):
                m.audit(r, after, bad)

    def test_audit_detects_replay_and_observation_corruption(self) -> None:
        r = base()
        after, events = m.materialize(r)
        with patch.object(m, "replay", return_value=r):
            with self.assertRaisesRegex(ValueError, "REPLAY_MISMATCH"):
                m.audit(r, after, events)
        with patch.object(m, "profiles", side_effect=[(), (frozenset(),)]):
            with self.assertRaisesRegex(ValueError, "OBSERVATIONS_CHANGED"):
                m.audit(r, after, events)

    def test_fixed_point_failure_is_detected(self) -> None:
        r = base()
        after, events = m.materialize(r)
        with patch.object(m, "configurations", return_value=iter((((), r),))), \
             patch.object(m, "materialize", side_effect=[(after, events), (r, ())]), \
             patch.object(m, "audit"):
            with self.assertRaisesRegex(ValueError, "NOT_A_FIXED_POINT"):
                m.sweep()

    def test_samples_and_report(self) -> None:
        report = m.report()
        self.assertEqual(report["stage"], 2)
        self.assertEqual(report["outcome"], "OPEN")
        self.assertEqual(m.sample("L")["fresh_instances"], 4)
        self.assertEqual(m.sample("F")["fresh_instances"], 9)
        self.assertEqual(m.sample("F")["read_pairs_after_answer"], ((0, 1), (0, 2), (1, 2)))
        with self.assertRaisesRegex(ValueError, "READING"):
            m.sample("unknown")

    def test_sample_rejects_unmet_or_answer_witness_corruption(self) -> None:
        with patch.object(m, "read_pairs", return_value=()):
            with self.assertRaisesRegex(ValueError, "UNMET_PAIR_WITNESS"):
                m.sample("L")
        with patch.object(m, "separable", side_effect=[True]):
            with self.assertRaisesRegex(ValueError, "UNMET_PAIR_WITNESS"):
                m.sample("L")
        with patch.object(m, "separable", side_effect=[False, False]):
            with self.assertRaisesRegex(ValueError, "ANSWER_WITNESS"):
                m.sample("L")

    def test_native_rule_alone_still_stores_nothing(self) -> None:
        self.assertEqual(base().insts, frozenset())
        after, events = m.materialize(base())
        self.assertEqual(len(after.insts), 4)
        self.assertTrue(all(isinstance(e, AdmitInst) for e in events))
        history: tuple[Event, ...] = events
        self.assertFalse(any(isinstance(e, Impose) for e in history))
