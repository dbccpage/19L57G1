from __future__ import annotations

import unittest

from typed_translation.enumerate import Candidate, enumerate_histories, unique_states
from typed_translation.model import (
    BoundaryRefusal,
    BoundaryState,
    Mark,
    RawEvent,
    RawKind,
    SourceEvent,
    SourceState,
    Transaction,
    replay_boundary,
    replay_source,
)
from typed_translation.translation import (
    LABEL_SPECS,
    REFUSAL_CODES,
    _fixed_labels,
    _ratio,
    address_for,
    boundary_task,
    decode_history,
    decode_state,
    distortion_report,
    encode_state,
    evaluate_candidate,
    labels_for_state,
    nearby_shell,
    provenance_witness,
    shell_report,
    statement_capabilities,
    translate_history,
    typed_states,
)


VALID_DIRECT = Candidate(
    "state_sensitive", True, True, True, False, True, "direct"
)
VALID_COMPLEMENTED = Candidate(
    "state_sensitive", True, True, True, False, True, "complemented"
)


class CodecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.histories = enumerate_histories()
        cls.states = unique_states(cls.histories)
        cls.domain = typed_states(cls.states)
        cls.shell = nearby_shell(cls.domain)

    def test_address_families_complement_only_outer_side(self) -> None:
        direct = address_for("inst_0", "direct")
        complemented = address_for("inst_0", "complemented")
        self.assertEqual(direct[1:], complemented[1:])
        self.assertEqual(direct[0], 1 - complemented[0])

    def test_unknown_address_family_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "address family"):
            address_for("d0", "other")

    def test_canonical_labels_include_compensation_exactly(self) -> None:
        state = SourceState(
            data=frozenset({0, 1}),
            form=True,
            instances=frozenset({0}),
            rule=True,
        )
        labels = labels_for_state(state)
        self.assertIn("comp_0", labels)
        self.assertNotIn("comp_1", labels)

    def test_all_source_states_round_trip_both_families(self) -> None:
        for state in self.states:
            for family in ("direct", "complemented"):
                decoded = decode_state(encode_state(state, family))
                self.assertEqual(decoded.state, state)
                self.assertTrue(decoded.accepted)

    def test_typed_domain_is_structural_and_deduplicated(self) -> None:
        self.assertEqual(len(self.domain), 43)
        self.assertEqual(len(set(self.domain)), 43)
        for state in self.domain:
            decoded = decode_state(state)
            self.assertIsNotNone(decoded.state)
            assert decoded.state is not None and decoded.family is not None
            self.assertEqual(encode_state(decoded.state, decoded.family), state)

    def test_unknown_label_refusal(self) -> None:
        result = decode_state(BoundaryState(frozenset({Mark("unknown", (0, 0, 0))})))
        self.assertEqual(result.refusal, "UNKNOWN_LABEL")

    def test_duplicate_label_refusal(self) -> None:
        state = BoundaryState(
            frozenset({Mark("d0", (0, 0, 0)), Mark("d0", (1, 0, 0))})
        )
        self.assertEqual(decode_state(state).refusal, "DUPLICATE_LABEL")

    def test_role_shape_refuses_bad_width_and_tag(self) -> None:
        bad_width = BoundaryState(frozenset({Mark("d0", (0, 0))}))
        bad_tag = BoundaryState(frozenset({Mark("d0", (0, 1, 1))}))
        self.assertEqual(decode_state(bad_width).refusal, "ROLE_STRUCTURE")
        self.assertEqual(decode_state(bad_tag).refusal, "ROLE_STRUCTURE")

    def test_role_shape_refuses_nonbinary_address(self) -> None:
        state = BoundaryState(frozenset({Mark("d0", (2, 0, 0))}))
        self.assertEqual(decode_state(state).refusal, "ROLE_STRUCTURE")

    def test_role_shape_refuses_incomplete_pairs_and_antecedents(self) -> None:
        incomplete = BoundaryState(frozenset({Mark("form_0", address_for("form_0", "direct"))}))
        instance = BoundaryState(frozenset({Mark("inst_0", address_for("inst_0", "direct"))}))
        self.assertEqual(decode_state(incomplete).refusal, "ROLE_STRUCTURE")
        self.assertEqual(decode_state(instance).refusal, "ROLE_STRUCTURE")

    def test_role_shape_refuses_spurious_compensation(self) -> None:
        state = BoundaryState(frozenset({Mark("comp_0", address_for("comp_0", "direct"))}))
        self.assertEqual(decode_state(state).refusal, "ROLE_STRUCTURE")

    def test_mixed_address_family_is_refused(self) -> None:
        state = encode_state(SourceState(data=frozenset({0, 1})), "direct")
        d0 = next(mark for mark in state.marks if mark.label == "d0")
        mixed = BoundaryState(
            frozenset((set(state.marks) - {d0}) | {Mark("d0", (1, 0, 0))})
        )
        self.assertEqual(decode_state(mixed).refusal, "ADDRESS_FAMILY")

    def test_nearby_shell_is_nonempty_and_fully_named(self) -> None:
        report = shell_report(self.shell)
        self.assertEqual(report["population"], 1326)
        self.assertEqual(report["silent_truncations"], [])
        counts = report["code_counts"]
        assert isinstance(counts, dict)
        self.assertEqual(set(counts), set(REFUSAL_CODES))
        self.assertTrue(all(counts[code] > 0 for code in REFUSAL_CODES))

    def test_shell_examples_reproduce_their_codes(self) -> None:
        report = shell_report(self.shell)
        examples = report["examples"]
        self.assertEqual(set(examples), set(REFUSAL_CODES))

    def test_fixed_blocks_cover_every_admission_kind(self) -> None:
        self.assertEqual(_fixed_labels(SourceEvent.ADMIT_D0), frozenset({"d0"}))
        self.assertEqual(_fixed_labels(SourceEvent.ADMIT_D1), frozenset({"d1"}))
        self.assertEqual(len(_fixed_labels(SourceEvent.ADMIT_FORM)), 2)
        self.assertEqual(_fixed_labels(SourceEvent.ADMIT_INST0), frozenset({"inst_0"}))
        self.assertEqual(_fixed_labels(SourceEvent.ADMIT_INST1), frozenset({"inst_1"}))
        self.assertEqual(len(_fixed_labels(SourceEvent.ADMIT_RULE)), 2)

    def test_presentation_has_no_fixed_admission_block(self) -> None:
        with self.assertRaisesRegex(ValueError, "presentation event"):
            _fixed_labels(SourceEvent.SUPPLY_D0)

    def test_label_census_is_fixed_and_typed(self) -> None:
        self.assertEqual(len(LABEL_SPECS), 10)
        self.assertEqual({role for role, _ in LABEL_SPECS.values()}, {"datum", "form", "instance", "rule"})


class TranslationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.histories = enumerate_histories()
        cls.states = unique_states(cls.histories)
        cls.domain = typed_states(cls.states)
        cls.shell = nearby_shell(cls.domain)

    def test_full_state_sensitive_translation_replays(self) -> None:
        history = tuple(SourceEvent)
        translated = translate_history(VALID_DIRECT, history)
        self.assertEqual(
            replay_boundary(translated).state,
            encode_state(replay_source(history).state, "direct"),
        )
        self.assertEqual(decode_history(translated), history)

    def test_rule_then_instance_adds_compensation_state_sensitively(self) -> None:
        history = (
            SourceEvent.SUPPLY_D0,
            SourceEvent.ADMIT_D0,
            SourceEvent.ADMIT_FORM,
            SourceEvent.ADMIT_RULE,
            SourceEvent.ADMIT_INST0,
        )
        labels = [
            raw.label
            for raw in translate_history(VALID_DIRECT, history)[-1].raw
            if raw.kind is RawKind.ADMISSION
        ]
        self.assertEqual(labels, ["comp_0", "inst_0"])

    def test_rule_after_instance_adds_rule_and_compensation(self) -> None:
        history = (
            SourceEvent.SUPPLY_D0,
            SourceEvent.ADMIT_D0,
            SourceEvent.ADMIT_FORM,
            SourceEvent.ADMIT_INST0,
            SourceEvent.ADMIT_RULE,
        )
        labels = {
            raw.label
            for raw in translate_history(VALID_DIRECT, history)[-1].raw
            if raw.kind is RawKind.ADMISSION
        }
        self.assertEqual(labels, {"rule_0", "rule_1", "comp_0"})

    def test_memoryless_translation_has_a_replay_counterexample(self) -> None:
        candidate = Candidate("memoryless", True, True, True, False, True, "direct")
        verdict = evaluate_candidate(candidate, self.histories, self.domain, self.shell)
        self.assertFalse(verdict.valid)
        self.assertFalse(verdict.clauses["histories"])

    def test_unknown_event_context_fails_closed(self) -> None:
        candidate = Candidate("unknown", True, True, True, False, True, "direct")
        history = (SourceEvent.ADMIT_FORM,)
        with self.assertRaisesRegex(ValueError, "event context"):
            translate_history(candidate, history)

    def test_no_synthetic_supply_has_event_counterexample(self) -> None:
        candidate = Candidate("state_sensitive", False, True, True, False, True, "direct")
        verdict = evaluate_candidate(candidate, self.histories, self.domain, self.shell)
        self.assertFalse(verdict.clauses["accepted_events"])

    def test_direct_candidate_is_valid(self) -> None:
        verdict = evaluate_candidate(VALID_DIRECT, self.histories, self.domain, self.shell)
        self.assertTrue(verdict.valid)
        self.assertTrue(all(verdict.clauses.values()))

    def test_complemented_candidate_is_valid(self) -> None:
        verdict = evaluate_candidate(VALID_COMPLEMENTED, self.histories, self.domain, self.shell)
        self.assertTrue(verdict.valid)

    def test_tag_exchange_fails_carrier_typing(self) -> None:
        candidate = Candidate("state_sensitive", True, True, True, False, False, "direct")
        verdict = evaluate_candidate(candidate, self.histories[:1], self.domain[:1], self.shell)
        self.assertFalse(verdict.clauses["carrier"])
        self.assertIn("tag exchange", str(verdict.counterexamples["carrier"]))

    def test_empty_shell_fails_the_shell_clause(self) -> None:
        verdict = evaluate_candidate(VALID_DIRECT, (), (), ())
        self.assertFalse(verdict.clauses["refusal_shell"])
        self.assertIn("refusal_shell", verdict.counterexamples)

    def test_shell_report_names_a_silent_typed_input(self) -> None:
        state = encode_state(SourceState(), "direct")
        report = shell_report((state,))
        self.assertEqual(len(report["silent_truncations"]), 1)

    def test_task_needs_outer_exchange_mark_permutations_and_forgotten_labels(self) -> None:
        state = encode_state(SourceState(data=frozenset({0, 1})), "direct")
        self.assertFalse(boundary_task(VALID_DIRECT, state))
        no_outer = Candidate("state_sensitive", True, False, True, False, True, "direct")
        no_perms = Candidate("state_sensitive", True, True, False, False, True, "direct")
        labels = Candidate("state_sensitive", True, True, True, True, True, "direct")
        self.assertTrue(boundary_task(no_outer, state))
        self.assertTrue(boundary_task(no_perms, state))
        self.assertTrue(boundary_task(labels, state))

    def test_task_has_no_subject_without_two_data(self) -> None:
        self.assertIsNone(boundary_task(VALID_DIRECT, BoundaryState()))

    def test_unnamed_tags_do_not_create_a_false_positive_at_empty_profile(self) -> None:
        candidate = Candidate("state_sensitive", True, True, True, False, False, "direct")
        state = encode_state(SourceState(data=frozenset({0, 1})), "direct")
        self.assertFalse(boundary_task(candidate, state))

    def test_decode_history_refuses_unknown_presentation(self) -> None:
        transactions = (Transaction(RawKind.PRESENTATION, (RawEvent(RawKind.PRESENTATION, "x"),)),)
        with self.assertRaisesRegex(BoundaryRefusal, "UNDECODABLE_PRESENTATION"):
            decode_history(transactions)

    def test_decode_history_refuses_unknown_admission_block(self) -> None:
        transactions = (
            Transaction(
                RawKind.ADMISSION,
                (RawEvent(RawKind.ADMISSION, "x", Mark("x", (0, 0, 0))),),
            ),
        )
        with self.assertRaisesRegex(BoundaryRefusal, "UNDECODABLE_ADMISSION"):
            decode_history(transactions)

    def test_statement_price_is_separate_and_exact(self) -> None:
        self.assertEqual(
            statement_capabilities(VALID_DIRECT),
            ("state_inspection", "administrative_presentation"),
        )
        baseline = Candidate("memoryless", False, True, True, False, True, "direct")
        self.assertEqual(statement_capabilities(baseline), ())

    def test_distortion_maxima_match_frozen_prediction(self) -> None:
        report = distortion_report(VALID_DIRECT, self.histories)
        extrema = report["extrema"]
        assert isinstance(extrema, dict)
        self.assertEqual(extrema["mu1"]["forward_max"], 4)
        self.assertEqual(extrema["mu2"]["forward_max"], 12)
        self.assertFalse(report["exact_both_measures"])

    def test_distortion_table_is_complete_and_bidirectional(self) -> None:
        report = distortion_report(VALID_DIRECT, self.histories)
        table = report["table"]
        assert isinstance(table, list)
        self.assertEqual(len(table), len(self.histories))
        for row in table:
            self.assertEqual(row["mu1"]["forward_additive"], -row["mu1"]["backward_additive"])

    def test_reduced_ratio_and_zero_base(self) -> None:
        self.assertEqual(_ratio(4, 2), "2/1")
        self.assertEqual(_ratio(0, 0), "ZERO_BASE")

    def test_provenance_witness_keeps_both_source_fields(self) -> None:
        witness = provenance_witness(self.states, "direct")
        self.assertEqual(witness["equal_profile"], [True, True])
        left = witness["left"]
        right = witness["right"]
        self.assertNotEqual(left["instances"], right["instances"])
        self.assertNotEqual(left["rule"], right["rule"])
        self.assertNotEqual(witness["left_labels"], witness["right_labels"])


if __name__ == "__main__":
    unittest.main()
