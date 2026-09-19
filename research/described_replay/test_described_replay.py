"""Deterministic and adversarial tests for all five stages.

AuthorityEffect: None.
"""

from __future__ import annotations

import ast
from collections import Counter
from dataclasses import fields, replace
import inspect
from pathlib import Path
import sys
import tempfile
from types import FrameType
import unittest
from unittest import mock

import class_replay
import cost_ledger
import description as description_module
import diagonal
import register
import run_described_replay
import stepper as stepper_module
from description import (
    AdmitDatum,
    AdmitForm,
    DecodeInvalid,
    DecodeValid,
    Description,
    EMPTY,
    Impose,
    Process,
    Regime,
    Supply,
    decode_description,
    decode_description_tagged,
    decoder_domain,
    description_is_admission_only,
    description_sha256,
    encode_description,
    enumerate_members,
    enumerate_description_regimes,
    event_from_json,
    event_json,
    is_class_member,
    process_key,
    prepare_description,
    prepared_decode_is_valid,
    regime_sha256,
    replay,
)
from receipt_io import (
    DuplicateNameError,
    deterministic_json_bytes,
    load_json_object,
    strict_json_loads,
    write_bytes_atomic,
)
from stepper import (
    Done,
    Invalid,
    PreparedState,
    Step,
    DescribedState,
    initial_state,
    iterate_stepper,
    step_described,
    stepper_total,
    terminal_result,
)
import verify_pins


HERE = Path(__file__).resolve().parent


class DescriptionStageTests(unittest.TestCase):
    members: tuple[Process, ...]

    @classmethod
    def setUpClass(cls) -> None:
        cls.members = enumerate_members()

    def test_exact_class_census(self) -> None:
        self.assertEqual(len(self.members), 178)
        self.assertEqual(
            Counter(len(member.events) for member in self.members),
            Counter({0: 1, 1: 5, 2: 26, 3: 146}),
        )
        self.assertEqual(len({process_key(member) for member in self.members}), 178)
        self.assertTrue(all(is_class_member(member) for member in self.members))

    def test_decode_encode_identity_and_injection(self) -> None:
        descriptions = [encode_description(member) for member in self.members]
        self.assertEqual(
            [decode_description(description) for description in descriptions],
            list(self.members),
        )
        self.assertEqual(len(set(descriptions)), 178)
        self.assertEqual(len({description_sha256(item) for item in descriptions}), 178)

    def test_every_encoding_is_admission_only(self) -> None:
        for member in self.members:
            description = encode_description(member)
            self.assertTrue(description_is_admission_only(description))
            self.assertTrue(
                all(isinstance(event, AdmitDatum) for event in description.admission_history)
            )

    def test_decoder_domain_rejects_each_malformed_surface(self) -> None:
        extra_component = Regime(("p0e0",), (1,), frozenset(), frozenset(), frozenset())
        wrong_position = Regime(("p1e0",), (), frozenset(), frozenset(), frozenset())
        too_long = Regime(
            ("p0e0", "p1e0", "p2e0", "p3e0"),
            (),
            frozenset(),
            frozenset(),
            frozenset(),
        )
        mismatched_history = Description((AdmitDatum("p0e1"),), Regime(("p0e0",), (), frozenset(), frozenset(), frozenset()))
        ill_formed = Regime(("p0e5",), (), frozenset(), frozenset(), frozenset())
        for value in (
            extra_component,
            wrong_position,
            too_long,
            mismatched_history,
            ill_formed,
        ):
            self.assertFalse(decoder_domain(value))
            self.assertIsInstance(decode_description_tagged(value), DecodeInvalid)
            self.assertIsNone(decode_description(value))

    def test_decoder_domain_iff_by_full_declared_word_enumeration(self) -> None:
        words = enumerate_description_regimes()
        encodings = {encode_description(member).regime for member in self.members}
        decoded = {word for word in words if decoder_domain(word)}
        self.assertEqual(len(words), 20_440)
        self.assertEqual(len(decoded), 178)
        self.assertEqual(decoded, encodings)

    def test_decoder_tag_retains_prefixes(self) -> None:
        member = next(item for item in self.members if len(item.events) == 3)
        result = decode_description_tagged(encode_description(member))
        self.assertIsInstance(result, DecodeValid)
        assert isinstance(result, DecodeValid)
        self.assertEqual(len(result.prefixes), 4)
        self.assertEqual(result.prefixes[-1], replay(member.events))

    def test_endpoint_does_not_determine_history(self) -> None:
        left = Process(EMPTY, ())
        right = Process(EMPTY, (Supply("a"),))
        self.assertTrue(is_class_member(left))
        self.assertTrue(is_class_member(right))
        self.assertNotEqual(left.events, right.events)
        self.assertEqual(replay(left.events), replay(right.events))
        self.assertNotEqual(
            description_sha256(encode_description(left)),
            description_sha256(encode_description(right)),
        )

    def test_event_json_roundtrip(self) -> None:
        events = {event for member in self.members for event in member.events}
        self.assertEqual(
            {event_from_json(event_json(event)) for event in events},
            events,
        )


class StepperStageTests(unittest.TestCase):
    def test_preparation_evidence_is_outside_described_state(self) -> None:
        self.assertEqual(
            tuple(field.name for field in fields(DescribedState)),
            ("description", "pointer", "regime"),
        )
        prepared = initial_state(
            encode_description(Process(EMPTY, (Supply("a"),)))
        )
        self.assertIsInstance(prepared, PreparedState)
        self.assertIsInstance(prepared.preparation, DecodeValid)

    def test_one_application_advances_one_event(self) -> None:
        member = Process(EMPTY, (Supply("a"),))
        state = initial_state(encode_description(member))
        result = step_described(state)
        self.assertIsInstance(result, Step)
        assert isinstance(result, Step)
        self.assertEqual(result.event, Supply("a"))
        self.assertEqual(result.state.pointer, 1)
        self.assertEqual(result.state.regime, EMPTY)

    def test_all_members_iterate_to_direct_replay(self) -> None:
        for member in enumerate_members():
            terminal = terminal_result(initial_state(encode_description(member)))
            self.assertIsInstance(terminal, Done)
            assert isinstance(terminal, Done)
            self.assertEqual(terminal.state.pointer, len(member.events))
            self.assertEqual(terminal.state.regime, replay(member.events))

    def test_exact_tag_partition_and_invalid_states(self) -> None:
        description = encode_description(Process(EMPTY, (Supply("a"),)))
        prepared_state = initial_state(description)
        states = (
            prepared_state,
            PreparedState(
                DescribedState(description, -1, EMPTY),
                prepared_state.preparation,
            ),
            PreparedState(
                DescribedState(description, 2, EMPTY),
                prepared_state.preparation,
            ),
            PreparedState(
                DescribedState(
                    description,
                    1,
                    Regime(
                        ("a",), (), frozenset(), frozenset(), frozenset()
                    ),
                ),
                prepared_state.preparation,
            ),
        )
        for state in states:
            result = step_described(state)
            self.assertIsInstance(result, (Step, Done, Invalid))
            self.assertTrue(stepper_total(state))
        self.assertIsInstance(step_described(states[1]), Invalid)
        self.assertIsInstance(step_described(states[2]), Invalid)
        self.assertIsInstance(step_described(states[3]), Invalid)

    def test_done_is_distinct_from_invalid(self) -> None:
        description = encode_description(Process(EMPTY, ()))
        self.assertIsInstance(step_described(initial_state(description)), Done)
        bad = Description((AdmitDatum("not-a-code"),), Regime(("not-a-code",), (), frozenset(), frozenset(), frozenset()))
        self.assertIsInstance(step_described(initial_state(bad)), Invalid)

    def test_stepper_body_does_not_call_whole_history_fold(self) -> None:
        source = inspect.getsource(step_described)
        tree = ast.parse(source)
        called = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        self.assertTrue(
            called.isdisjoint(
                {
                    "decode_description",
                    "decode_description_tagged",
                    "prepare_description",
                    "re" + "play",
                    "validate_description",
                    "_well_formed_prefixes",
                }
            )
        )
        self.assertEqual(sum(name == "apply_event" for name in called), 1)

    def test_preparation_occurs_once_before_transitions(self) -> None:
        description = encode_description(
            Process(EMPTY, (AdmitDatum("a"), Supply("b")))
        )
        with mock.patch.object(
            stepper_module,
            "prepare_description",
            wraps=prepare_description,
        ) as prepare:
            state = initial_state(description)
            self.assertEqual(prepare.call_count, 1)
        forbidden_codes = {
            description_module.decode_description.__code__,
            description_module.decode_description_tagged.__code__,
            description_module.prepare_description.__code__,
            description_module.replay.__code__,
            description_module.validate_description.__code__,
            description_module._well_formed_prefixes.__code__,
        }
        with (
            mock.patch.object(
                stepper_module,
                "prepare_description",
                side_effect=AssertionError("preparation repeated during step"),
            ),
            mock.patch.object(
                description_module,
                "decode_description_tagged",
                side_effect=AssertionError("decoder reached during step"),
            ),
            mock.patch.object(
                description_module,
                "_well_formed_prefixes",
                side_effect=AssertionError("prefix fold reached during step"),
            ),
        ):
            reached: list[str] = []

            def trace(frame: FrameType, event: str, argument: object) -> None:
                del argument
                if event == "call" and frame.f_code in forbidden_codes:
                    reached.append(frame.f_code.co_name)

            sys.setprofile(trace)
            try:
                first = step_described(state)
                self.assertIsInstance(first, Step)
                assert isinstance(first, Step)
                second = step_described(first.state)
                self.assertIsInstance(second, Step)
            finally:
                sys.setprofile(None)
            self.assertEqual(reached, [])

    def test_step_calls_transition_once_and_terminal_tags_call_it_zero_times(
        self,
    ) -> None:
        description = encode_description(Process(EMPTY, (AdmitDatum("a"),)))
        state = initial_state(description)
        with mock.patch.object(
            stepper_module,
            "apply_event",
            wraps=description_module.step,
        ) as transition:
            stepped = step_described(state)
            self.assertIsInstance(stepped, Step)
            self.assertEqual(transition.call_count, 1)
            assert isinstance(stepped, Step)
            done = step_described(stepped.state)
            self.assertIsInstance(done, Done)
            self.assertEqual(transition.call_count, 1)

        unprepared = DescribedState(description, 0, EMPTY)
        with mock.patch.object(
            stepper_module,
            "apply_event",
            wraps=description_module.step,
        ) as transition:
            self.assertIsInstance(step_described(unprepared), Invalid)
            self.assertEqual(transition.call_count, 0)

    def test_missing_mismatched_and_tampered_preparations_are_invalid(
        self,
    ) -> None:
        process = Process(EMPTY, (AdmitDatum("a"),))
        description = encode_description(process)
        prepared = prepare_description(description)
        self.assertIsInstance(prepared, DecodeValid)
        assert isinstance(prepared, DecodeValid)
        self.assertTrue(prepared_decode_is_valid(prepared))

        self.assertIsInstance(
            step_described(DescribedState(description, 0, EMPTY)),
            Invalid,
        )

        other_description = encode_description(Process(EMPTY, ()))
        other_prepared = prepare_description(other_description)
        self.assertIsInstance(other_prepared, DecodeValid)
        self.assertIsInstance(
            step_described(
                PreparedState(
                    DescribedState(description, 0, EMPTY), other_prepared
                )
            ),
            Invalid,
        )

        forged = replace(prepared, prefixes=(EMPTY, EMPTY))
        self.assertFalse(prepared_decode_is_valid(forged))
        self.assertIsInstance(
            step_described(
                PreparedState(DescribedState(description, 1, EMPTY), forged)
            ),
            Invalid,
        )

    def test_iterate_retains_one_result_per_application(self) -> None:
        member = next(item for item in enumerate_members() if len(item.events) == 3)
        results = iterate_stepper(initial_state(encode_description(member)))
        self.assertEqual(len(results), 4)
        self.assertTrue(all(isinstance(item, Step) for item in results[:-1]))
        self.assertIsInstance(results[-1], Done)


class ClassReplayStageTests(unittest.TestCase):
    def test_model_layer_replays_every_description(self) -> None:
        for member in class_replay.class_members():
            result = class_replay.model_replay(encode_description(member))
            self.assertIsNotNone(result)
            assert result is not None
            self.assertTrue(result.certified)
            self.assertEqual(result.reproduced, replay(member.events))

    def test_complete_candidate_matrix_and_scoped_refusal(self) -> None:
        matrix = class_replay.complete_candidate_matrix()
        self.assertEqual(len(matrix), 178 * 178)
        self.assertEqual(
            len({(cell.candidate_index, cell.target_index) for cell in matrix}),
            len(matrix),
        )
        self.assertTrue(all(cell.candidate_execution_certified for cell in matrix))
        self.assertEqual(
            sum(cell.target_reproduction_certified for cell in matrix), 2724
        )
        self.assertEqual(class_replay.successful_candidate_indices(), ())
        self.assertEqual(
            class_replay.render_class_replay()["terminal"],
            "NO_SUCH_MEMBER_IN_CLASS",
        )

    def test_receipt_catalog_exports_every_member_and_description(self) -> None:
        payload = class_replay.render_class_replay()
        catalog = payload["member_description_catalog"]
        assert isinstance(catalog, list)
        self.assertEqual(len(catalog), 178)
        self.assertEqual(
            [entry["member_index"] for entry in catalog if isinstance(entry, dict)],
            list(range(178)),
        )
        self.assertTrue(
            all(
                isinstance(entry, dict)
                and "member_process" in entry
                and "description" in entry
                for entry in catalog
            )
        )

    def test_candidate_validates_but_does_not_read_description(self) -> None:
        class_replay.execute_class_process.cache_clear()
        class_replay._prepare_target_description.cache_clear()
        candidate = next(
            member
            for member in class_replay.class_members()
            if len(member.events) == 3
        )
        target = class_replay.class_members()[1]
        description = encode_description(target)
        with (
            mock.patch.object(
                class_replay,
                "prepare_description",
                wraps=description_module.prepare_description,
            ) as preparation,
            mock.patch.object(
                stepper_module,
                "apply_event",
                wraps=description_module.step,
            ) as transition,
        ):
            output = class_replay.feed_candidate(candidate, description)
            repeated = class_replay.feed_candidate(candidate, description)
            self.assertEqual(transition.call_count, len(candidate.events))
            self.assertEqual(preparation.call_count, 2)
        self.assertTrue(description.regime.data)
        self.assertEqual(repeated, output)
        self.assertEqual(output, replay(candidate.events, candidate.base))
        self.assertNotEqual(output.data, description.regime.data)
        class_replay.execute_class_process.cache_clear()
        class_replay._prepare_target_description.cache_clear()

    def test_candidate_feed_rejects_invalid_inputs(self) -> None:
        candidate = class_replay.class_members()[0]
        malformed = Description(
            (AdmitDatum("not-a-code"),),
            Regime(("not-a-code",), (), frozenset(), frozenset(), frozenset()),
        )
        with self.assertRaisesRegex(ValueError, "token does not match"):
            class_replay.feed_candidate(candidate, malformed)
        outside = Process(Regime(("a",), (), frozenset(), frozenset(), frozenset()), ())
        with self.assertRaisesRegex(ValueError, "outside the declared class"):
            class_replay.feed_candidate(outside, encode_description(candidate))


class DiagonalStageTests(unittest.TestCase):
    def test_self_description_witness_is_exactly_empty(self) -> None:
        self.assertEqual(diagonal.self_description_witness_indices(), (0,))
        witness = class_replay.class_members()[0]
        self.assertEqual(witness.events, ())

    def test_outside_reporter_is_correct_within_bound(self) -> None:
        members = class_replay.class_members()
        self.assertTrue(
            all(
                diagonal.outside_report(member)
                == diagonal.target_reaches_terminal(member)
                for member in members
            )
        )
        self.assertLessEqual(max(map(diagonal.outside_report_cost, members)), 6)

    def test_candidate_cost_uses_candidate_steps_and_target_admissions(self) -> None:
        members = class_replay.class_members()
        one = next(member for member in members if len(member.events) == 1)
        three = next(member for member in members if len(member.events) == 3)
        self.assertEqual(diagonal.candidate_run_cost(one, three), 4)
        self.assertEqual(diagonal.outside_report_cost(three), 6)
        matrix = diagonal.complete_reporter_matrix()
        self.assertTrue(
            all(
                cell.cost
                == len(members[cell.candidate_index].events)
                + len(members[cell.target_index].events)
                for cell in matrix
            )
        )

    def test_terminal_partition_is_nonconstant(self) -> None:
        values = Counter(
            diagonal.target_reaches_terminal(member)
            for member in class_replay.class_members()
        )
        self.assertEqual(values, Counter({True: 128, False: 50}))

    def test_no_fixed_reporter_and_every_diagonal_disagrees(self) -> None:
        self.assertEqual(diagonal.successful_reporter_indices(), ())
        self.assertEqual(len(diagonal.complete_reporter_matrix()), 178 * 178)
        self.assertTrue(
            all(
                diagonal.diagonal_disagrees(candidate)
                for candidate in class_replay.class_members()
            )
        )
        payload = diagonal.render_diagonal_stage()
        reporter = payload["reporter_search"]
        assert isinstance(reporter, dict)
        self.assertEqual(reporter["terminal"], "DECIDER_REFUSED_WITHIN_COST")
        self.assertEqual(payload["unbounded"], "OPEN_UNBOUNDED")


class CostLedgerStageTests(unittest.TestCase):
    def test_base_pair_is_initially_unseparated(self) -> None:
        base = cost_ledger.separation_base()
        self.assertEqual(base.reqs, frozenset({(0, 1)}))
        self.assertFalse(cost_ledger.satisfies(base))

    def test_pruned_and_full_valid_sets_agree(self) -> None:
        payload = cost_ledger.render_cost_ledger()
        self.assertTrue(payload["pruned_full_valid_agree"])
        self.assertEqual(
            payload["pruned_two_item_valid"], payload["full_two_item_valid"]
        )

    def test_both_measures_retain_both_raw_ties(self) -> None:
        one = cost_ledger.find_responses("mu1")
        two = cost_ledger.find_responses("mu2")
        self.assertEqual(one.measure_value, 2)
        self.assertEqual(two.measure_value, (2, 1))
        self.assertEqual(len(one.winners), 2)
        self.assertEqual(len(two.winners), 2)
        self.assertEqual(one.finding_cost, 12)
        self.assertEqual(two.finding_cost, 12)
        self.assertTrue(all(cost_ledger.checking_cost(item) == 4 for item in one.winners))

    def test_response_check_executes_one_transition_per_charged_event(
        self,
    ) -> None:
        base = cost_ledger.separation_base()
        delta = cost_ledger.find_responses("mu1").winners[0]
        events = cost_ledger.delta_events(base, delta)
        with mock.patch.object(
            cost_ledger,
            "apply_event",
            wraps=description_module.step,
        ) as transition:
            run = cost_ledger.execute_delta(base, delta)
        self.assertEqual(transition.call_count, len(events))
        self.assertEqual(run.stepper_application_count, len(events))
        self.assertEqual(run.description_admission_count, len(events))
        self.assertEqual(run.endpoint, replay(events, base))
        artificial = cost_ledger.ResponseEventRun(base, 3, 5)
        with mock.patch.object(
            cost_ledger, "execute_delta", return_value=artificial
        ) as execution:
            self.assertEqual(cost_ledger.checking_cost(delta), 8)
            execution.assert_called_once_with(
                cost_ledger.separation_base(), delta
            )
        source = inspect.getsource(cost_ledger.execute_response_events)
        tree = ast.parse(source)
        called = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        self.assertNotIn("re" + "play", called)
        self.assertEqual(sum(name == "apply_event" for name in called), 1)

        payload = cost_ledger.render_cost_ledger()
        self.assertEqual(
            payload["execution_surface"],
            "response_event_stepper_not_dr_decoder",
        )
        rows = payload["rows"]
        assert isinstance(rows, list)
        for row in rows:
            assert isinstance(row, dict)
            supplied = row["supplied_responses"]
            assert isinstance(supplied, list)
            for response in supplied:
                assert isinstance(response, dict)
                self.assertEqual(response["description_admission_count"], 2)
                self.assertEqual(response["stepper_application_count"], 2)

    def test_secondary_quotient_retains_one_two_member_class(self) -> None:
        for measure in ("mu1", "mu2"):
            groups = cost_ledger.grouped_winners(cost_ledger.find_responses(measure))
            self.assertEqual(len(groups), 1)
            self.assertEqual(len(groups[0]), 2)

    def test_canonical_key_retains_carrier_cardinality(self) -> None:
        two = cost_ledger.separation_base()
        three = cost_ledger.apply_delta(two, (cost_ledger.NewDatum(),))
        self.assertNotEqual(
            cost_ledger.canonical_regime_key(two),
            cost_ledger.canonical_regime_key(three),
        )

    def test_four_named_pruning_exclusions_have_negative_witnesses(self) -> None:
        base = cost_ledger.separation_base()
        rule = (cost_ledger.NewForm(1), cost_ledger.NewRuleAll(0))
        datum = (cost_ledger.NewDatum(), cost_ledger.NewDatum())
        form = (cost_ledger.NewForm(1), cost_ledger.NewForm(1))
        self.assertTrue(cost_ledger.has_removable_rule(rule))
        self.assertTrue(cost_ledger.has_irrelevant_new_datum(base, datum))
        self.assertTrue(cost_ledger.has_irrelevant_new_form(base, form))
        self.assertFalse(cost_ledger.response_valid(base, rule))
        self.assertFalse(cost_ledger.response_valid(base, datum))
        self.assertFalse(cost_ledger.response_valid(base, form))

        mention_base = replay(
            (
                AdmitDatum("a"),
                AdmitDatum("b"),
                AdmitDatum("c"),
                AdmitForm(1),
                AdmitForm(1),
                Impose(0, 1),
            )
        )
        misses = (
            cost_ledger.NewInst(0, (2,)),
            cost_ledger.NewInst(1, (2,)),
        )
        self.assertTrue(cost_ledger.instances_miss_target(misses))
        self.assertFalse(cost_ledger.response_valid(mention_base, misses))

    def test_unknown_measure_and_out_of_bound_cost_fail(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown measure"):
            cost_ledger.find_responses("missing")
        with self.assertRaisesRegex(ValueError, "outside the declared bound"):
            cost_ledger.candidates_at_cost(cost_ledger.separation_base(), 3)


class RegisterAndReceiptTests(unittest.TestCase):
    def test_register_walks_exactly_five_stages(self) -> None:
        description_payload = class_replay.render_description_stage()
        self.assertNotIn("evidence_class", description_payload)
        self.assertEqual(
            description_payload["observation_evidence_class"],
            "FINITE_COMPUTATION",
        )
        payload = register.render_register()
        stages = payload["stages"]
        assert isinstance(stages, list)
        self.assertEqual(
            [stage["stage"] for stage in stages if isinstance(stage, dict)],
            ["Description", "Stepper", "ClassReplay", "Diagonal", "CostLedger"],
        )
        self.assertEqual(payload["terminal"], "REGISTER_WRITTEN")
        self.assertEqual(payload["unbounded"], "OPEN_UNBOUNDED")
        self.assertFalse(payload["frontier_started"])
        for stage in stages:
            assert isinstance(stage, dict)
            self.assertNotIn("evidence_class", stage)
            observation = stage["python_observation"]
            assert isinstance(observation, dict)
            self.assertEqual(
                observation["evidence_class"], "FINITE_COMPUTATION"
            )
            claims = stage["terminal_claims"]
            assert isinstance(claims, list)
            for claim in claims:
                assert isinstance(claim, dict)
                if claim["evidence_class"] == "PROVED_THEOREM":
                    self.assertTrue(claim["lean_evidence"])

    def test_tau_has_exact_protected_surfaces(self) -> None:
        tau = register.render_tau()
        self.assertFalse(tau["final_state"])
        self.assertTrue(tau["stage_register_complete"])
        self.assertFalse(tau["publication_complete"])
        self.assertEqual(tau["sealed_paths_touched"], [])
        self.assertEqual(tau["shared_files_touched"], [])
        self.assertEqual(
            tau["opens_unchanged"],
            ["OB1_UNCHANGED", "S66_UNCHANGED", "S9_LAST_UNCHANGED"],
        )
        manifest = verify_pins.load_manifest()
        self.assertEqual(
            tau["outside_bet_hash"],
            manifest["outside_bet_commitment_sha256"],
        )

    def test_renderer_is_byte_stable(self) -> None:
        first = run_described_replay.render_outputs()
        second = run_described_replay.render_outputs()
        self.assertEqual(first, second)

    def test_strict_json_rejects_duplicate_names_and_nonstandard_numbers(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate JSON object name"):
            strict_json_loads(b'{"a":1,"a":2}')
        with self.assertRaisesRegex(ValueError, "non-standard"):
            strict_json_loads(b'{"a":NaN}')

    def test_atomic_writer_roundtrip_and_existing_directory_refusal(self) -> None:
        with tempfile.TemporaryDirectory(dir=HERE) as raw:
            root = Path(raw)
            target = root / "receipt.json"
            payload = deterministic_json_bytes({"authority_effect": None})
            write_bytes_atomic(target, payload)
            self.assertEqual(target.read_bytes(), payload)
            self.assertEqual(load_json_object(target), {"authority_effect": None})
            directory_target = root / "not-a-file"
            directory_target.mkdir()
            with self.assertRaisesRegex(ValueError, "regular file"):
                write_bytes_atomic(directory_target, payload)

    def test_scope_injection_names_only_outside_paths(self) -> None:
        self.assertEqual(
            verify_pins.scope_failures(
                (
                    "research/described_replay/receipts/x.json",
                    "artifacts/claims.json",
                    "research/other/status.md",
                )
            ),
            ("artifacts/claims.json", "research/other/status.md"),
        )

    def test_register_receipts_name_stored_files(self) -> None:
        stages = register.render_register()["stages"]
        assert isinstance(stages, list)
        receipts: list[str] = []
        for stage in stages:
            assert isinstance(stage, dict)
            observation = stage["python_observation"]
            assert isinstance(observation, dict)
            receipt = observation["receipt"]
            assert isinstance(receipt, str)
            receipts.append(receipt)
        self.assertEqual(
            [
                "receipts/python/description.json",
                "receipts/python/stepper.json",
                "receipts/python/class_replay.json.gz",
                "receipts/python/diagonal.json.gz",
                "receipts/python/cost_ledger.json",
            ],
            receipts,
        )
        stored = {
            f"receipts/python/{name}" for name in run_described_replay.STORED_NAMES
        }
        for receipt in receipts:
            self.assertIn(receipt, stored)
            self.assertTrue((HERE / receipt).is_file(), receipt)

    def test_committed_receipts_match_the_rendering(self) -> None:
        self.assertEqual(
            [],
            run_described_replay.snapshot_failures(
                run_described_replay.render_outputs(),
                run_described_replay.receipt_snapshot(),
            ),
        )


if __name__ == "__main__":
    unittest.main()
