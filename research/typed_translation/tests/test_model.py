from __future__ import annotations

import unittest

from typed_translation.model import (
    EVENT_ORDER,
    BoundaryRefusal,
    BoundaryState,
    Mark,
    RawEvent,
    RawKind,
    SourceEvent,
    SourceRefusal,
    SourceReplay,
    SourceState,
    Transaction,
    flatten_transactions,
    measure,
    replay_boundary,
    replay_source,
    source_accepts,
    source_kind,
    source_label,
    source_raw_trace,
    source_step,
)


class SourceModelTests(unittest.TestCase):
    def test_event_order_is_the_frozen_eight(self) -> None:
        self.assertEqual(len(EVENT_ORDER), 8)
        self.assertEqual(EVENT_ORDER, tuple(SourceEvent))

    def test_supply_is_state_inert_but_enables_admission(self) -> None:
        before = SourceReplay()
        after = source_step(before, SourceEvent.SUPPLY_D0)
        self.assertEqual(after.state, before.state)
        self.assertEqual(after.supplied, frozenset({0}))
        self.assertTrue(source_accepts(after, SourceEvent.ADMIT_D0))

    def test_duplicate_supply_is_refused(self) -> None:
        replay = source_step(SourceReplay(), SourceEvent.SUPPLY_D0)
        self.assertFalse(source_accepts(replay, SourceEvent.SUPPLY_D0))
        with self.assertRaisesRegex(SourceRefusal, "supply_d0"):
            source_step(replay, SourceEvent.SUPPLY_D0)

    def test_datum_requires_prior_supply(self) -> None:
        self.assertFalse(source_accepts(SourceReplay(), SourceEvent.ADMIT_D0))
        with self.assertRaises(SourceRefusal):
            source_step(SourceReplay(), SourceEvent.ADMIT_D1)

    def test_each_datum_is_admitted_once(self) -> None:
        replay = replay_source(
            (SourceEvent.SUPPLY_D0, SourceEvent.ADMIT_D0)
        )
        self.assertEqual(replay.state.data, frozenset({0}))
        self.assertFalse(source_accepts(replay, SourceEvent.ADMIT_D0))

    def test_form_and_rule_guards(self) -> None:
        self.assertTrue(source_accepts(SourceReplay(), SourceEvent.ADMIT_FORM))
        self.assertFalse(source_accepts(SourceReplay(), SourceEvent.ADMIT_RULE))
        replay = replay_source((SourceEvent.ADMIT_FORM, SourceEvent.ADMIT_RULE))
        self.assertTrue(replay.state.form)
        self.assertTrue(replay.state.rule)
        self.assertFalse(source_accepts(replay, SourceEvent.ADMIT_RULE))

    def test_instance_requires_form_and_its_datum(self) -> None:
        supplied = replay_source((SourceEvent.SUPPLY_D0, SourceEvent.ADMIT_D0))
        self.assertFalse(source_accepts(supplied, SourceEvent.ADMIT_INST0))
        ready = source_step(supplied, SourceEvent.ADMIT_FORM)
        self.assertTrue(source_accepts(ready, SourceEvent.ADMIT_INST0))
        done = source_step(ready, SourceEvent.ADMIT_INST0)
        self.assertEqual(done.state.instances, frozenset({0}))
        self.assertFalse(source_accepts(done, SourceEvent.ADMIT_INST0))

    def test_full_replay_retains_all_fields_separately(self) -> None:
        replay = replay_source(EVENT_ORDER)
        self.assertEqual(replay.state.data, frozenset({0, 1}))
        self.assertTrue(replay.state.form)
        self.assertEqual(replay.state.instances, frozenset({0, 1}))
        self.assertTrue(replay.state.rule)
        self.assertEqual(replay.supplied, frozenset({0, 1}))

    def test_profile_is_rule_or_instance(self) -> None:
        instance = SourceState(data=frozenset({0, 1}), form=True, instances=frozenset({0}))
        rule = SourceState(data=frozenset({0, 1}), form=True, rule=True)
        self.assertEqual([instance.profile(i) for i in (0, 1)], [True, False])
        self.assertEqual([rule.profile(i) for i in (0, 1)], [True, True])
        self.assertTrue(instance.task())
        self.assertFalse(rule.task())

    def test_task_has_no_subject_before_both_data(self) -> None:
        self.assertIsNone(SourceState().task())

    def test_profile_refuses_an_unknown_datum(self) -> None:
        with self.assertRaisesRegex(ValueError, "zero or one"):
            SourceState().profile(2)

    def test_source_state_record_keeps_fields_and_projection(self) -> None:
        state = SourceState(data=frozenset({0, 1}), form=True, instances=frozenset({1}))
        record = state.as_record()
        self.assertEqual(record["instances"], [1])
        self.assertEqual(record["profile"], [False, True])
        self.assertTrue(record["task"])

    def test_source_kinds_and_labels_are_total(self) -> None:
        self.assertEqual(
            [source_kind(event) for event in EVENT_ORDER].count(RawKind.PRESENTATION),
            2,
        )
        self.assertEqual(source_label(SourceEvent.ADMIT_FORM), "form")
        self.assertEqual(source_label(SourceEvent.ADMIT_RULE), "rule")

    def test_source_trace_uses_the_common_protocol(self) -> None:
        trace = source_raw_trace(EVENT_ORDER)
        self.assertEqual(measure(trace, "mu1"), 6)
        self.assertEqual(measure(trace, "mu2"), 8)


class BoundaryModelTests(unittest.TestCase):
    def test_presentation_replays_without_marks(self) -> None:
        transaction = Transaction(
            RawKind.PRESENTATION, (RawEvent(RawKind.PRESENTATION, "x"),)
        )
        replay = replay_boundary((transaction,))
        self.assertEqual(replay.state, BoundaryState())
        self.assertEqual(replay.presented, frozenset({"x"}))

    def test_administrative_presentation_and_admission_replay(self) -> None:
        mark = Mark("x", (0, 0, 0))
        transaction = Transaction(
            RawKind.ADMISSION,
            (
                RawEvent(RawKind.PRESENTATION, "x"),
                RawEvent(RawKind.ADMISSION, "x", mark),
            ),
        )
        replay = replay_boundary((transaction,))
        self.assertEqual(replay.state.marks, frozenset({mark}))

    def test_unpresented_label_is_refused(self) -> None:
        mark = Mark("x", (0, 0, 0))
        transaction = Transaction(
            RawKind.ADMISSION, (RawEvent(RawKind.ADMISSION, "x", mark),)
        )
        with self.assertRaisesRegex(BoundaryRefusal, "UNPRESENTED_LABEL"):
            replay_boundary((transaction,))

    def test_empty_transaction_is_refused(self) -> None:
        with self.assertRaisesRegex(BoundaryRefusal, "EMPTY_TRANSACTION"):
            replay_boundary((Transaction(RawKind.ADMISSION, ()),))

    def test_presentation_kind_cannot_hide_an_admission(self) -> None:
        mark = Mark("x", (0, 0, 0))
        transaction = Transaction(
            RawKind.PRESENTATION, (RawEvent(RawKind.ADMISSION, "x", mark),)
        )
        with self.assertRaisesRegex(BoundaryRefusal, "PRESENTATION_KIND_MISMATCH"):
            replay_boundary((transaction,))

    def test_admission_transaction_needs_an_admission(self) -> None:
        transaction = Transaction(
            RawKind.ADMISSION, (RawEvent(RawKind.PRESENTATION, "x"),)
        )
        with self.assertRaisesRegex(BoundaryRefusal, "ADMISSION_WITHOUT"):
            replay_boundary((transaction,))

    def test_presentation_cannot_carry_a_mark(self) -> None:
        mark = Mark("x", (0, 0, 0))
        transaction = Transaction(
            RawKind.PRESENTATION, (RawEvent(RawKind.PRESENTATION, "x", mark),)
        )
        with self.assertRaisesRegex(BoundaryRefusal, "PRESENTATION_CARRIES_MARK"):
            replay_boundary((transaction,))

    def test_raw_admission_needs_a_mark(self) -> None:
        transaction = Transaction(
            RawKind.ADMISSION,
            (
                RawEvent(RawKind.PRESENTATION, "x"),
                RawEvent(RawKind.ADMISSION, "x"),
            ),
        )
        with self.assertRaisesRegex(BoundaryRefusal, "ADMISSION_KIND_MISMATCH"):
            replay_boundary((transaction,))

    def test_mark_label_must_match_event_label(self) -> None:
        transaction = Transaction(
            RawKind.ADMISSION,
            (
                RawEvent(RawKind.PRESENTATION, "x"),
                RawEvent(RawKind.ADMISSION, "x", Mark("y", (0, 0, 0))),
            ),
        )
        with self.assertRaisesRegex(BoundaryRefusal, "LABEL_MARK_MISMATCH"):
            replay_boundary((transaction,))

    def test_duplicate_mark_is_refused(self) -> None:
        mark = Mark("x", (0, 0, 0))
        first = Transaction(
            RawKind.ADMISSION,
            (
                RawEvent(RawKind.PRESENTATION, "x"),
                RawEvent(RawKind.ADMISSION, "x", mark),
            ),
        )
        second = Transaction(RawKind.ADMISSION, (RawEvent(RawKind.ADMISSION, "x", mark),))
        with self.assertRaisesRegex(BoundaryRefusal, "DUPLICATE_MARK"):
            replay_boundary((first, second))

    def test_flatten_and_records_are_deterministic(self) -> None:
        raw = RawEvent(RawKind.PRESENTATION, "x")
        transaction = Transaction(RawKind.PRESENTATION, (raw,))
        self.assertEqual(flatten_transactions((transaction,)), (raw,))
        self.assertEqual(transaction.as_record()["kind"], "PRESENTATION")
        self.assertEqual(BoundaryState().as_record(), {"marks": []})

    def test_raw_admission_record_includes_the_mark(self) -> None:
        mark = Mark("x", (0, 0, 0))
        record = RawEvent(RawKind.ADMISSION, "x", mark).as_record()
        self.assertEqual(record["mark"], mark.as_record())

    def test_unknown_measure_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown measure"):
            measure((), "mu3")


if __name__ == "__main__":
    unittest.main()
