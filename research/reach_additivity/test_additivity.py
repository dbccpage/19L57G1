"""Unit tests for the composition and cost claims.

Every test below pins a sentence that appears in `STATUS.md` or
`CLAIM_LEDGER.md`.  AuthorityEffect: None.
"""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (str(HERE), str(REPO / "code")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from derivation.model import Regime  # noqa: E402
from derivation.candidates import (  # noqa: E402
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    delta_events,
    iter_full_deltas,
)

import additivity as add  # noqa: E402
import survey  # noqa: E402


def a_base_with_a_standing_instance() -> tuple[str, Regime]:
    for name, base in survey.rectangle():
        if base.insts:
            return name, base
    raise AssertionError("the rectangle carries no standing instance")


class Composition(unittest.TestCase):
    def test_compose_is_concatenation(self) -> None:
        d = (NewDatum(),)
        e = (NewForm(1),)
        self.assertEqual(add.compose(d, e), (NewDatum(), NewForm(1)))

    def test_composition_is_not_total(self) -> None:
        """A response can be well formed after another and ill formed on its
        own.  This is what makes composition more than bookkeeping, and the
        survey counts how often it happens."""

        _, base = survey.rectangle()[0]
        d = (NewForm(1),)
        middle = add.act(base, d)
        assert middle is not None
        e = (NewInst(len(base.forms), (0,)),)
        self.assertIsNotNone(add.act(middle, e))
        self.assertIsNone(add.act(base, e))
        self.assertIsNotNone(add.act(base, add.compose(d, e)))

    def test_event_tuples_are_identical_not_merely_equivalent(self) -> None:
        """The composite's event tuple IS the concatenation of the parts'
        event tuples.  That is why the two sides also agree on
        ill-formedness rather than merely on results."""

        _, base = survey.rectangle()[0]
        d = (NewDatum(),)
        middle = add.act(base, d)
        assert middle is not None
        e = (NewDatum(),)
        self.assertEqual(
            delta_events(base, add.compose(d, e)),
            delta_events(base, d) + delta_events(middle, e),
        )


class SequentialAction(unittest.TestCase):
    def test_every_triple_in_the_rectangle_agrees(self) -> None:
        report = survey.sequential_survey()
        self.assertEqual(report["triples"], report["states_agree"])
        self.assertEqual(report["triples"], report["event_tuples_agree"])
        self.assertEqual(report["composite_defined_but_not_stepwise"], 0)
        self.assertEqual(report["stepwise_defined_but_not_composite"], 0)

    def test_some_second_responses_are_ill_formed_at_the_original_base(self) -> None:
        """If none were, the agreement above would be a statement about
        independent responses and would prove much less."""

        report = survey.sequential_survey()
        stray = report["second_response_ill_formed_at_the_original_base"]
        assert isinstance(stray, int)
        self.assertGreater(stray, 0)


class Additivity(unittest.TestCase):
    def test_every_functional_is_additive_over_the_rectangle(self) -> None:
        report = survey.additivity_survey()
        by = report["by_functional"]
        assert isinstance(by, dict)
        for name, row in by.items():
            self.assertEqual(row["not_additive"], 0, name)
            self.assertGreater(row["checked"], 0, name)

    def test_the_item_count_is_additive_too(self) -> None:
        """Additivity does not separate the base-relative cost from the
        base-free one, which is the rung's correction to its own premise."""

        report = survey.additivity_survey()
        count = report["item_count"]
        assert isinstance(count, dict)
        self.assertEqual(count["not_additive"], 0)
        self.assertGreater(count["checked"], 0)

    def test_no_step_cost_is_negative_in_the_rectangle(self) -> None:
        report = survey.additivity_survey()
        least = report["least_step_cost_seen"]
        assert isinstance(least, dict)
        for name, value in least.items():
            self.assertGreaterEqual(value, 0, name)


class SelfLoops(unittest.TestCase):
    def test_an_instance_repeat_is_a_self_loop(self) -> None:
        _, base = a_base_with_a_standing_instance()
        form, args = sorted(base.insts)[0]
        self.assertEqual(add.act(base, (NewInst(form, args),)), base)

    def test_a_form_repeat_is_never_a_self_loop(self) -> None:
        """Form admission appends unconditionally: two forms of equal arity
        are two forms.  Pinned because the whole self-loop classification
        turns on it."""

        for _, base in survey.rectangle():
            if not base.forms:
                continue
            after = add.act(base, (NewForm(base.forms[0]),))
            self.assertIsNotNone(after)
            self.assertNotEqual(after, base)

    def test_a_datum_item_is_never_a_self_loop(self) -> None:
        """The recorded miss, pinned so it cannot quietly become true.

        Datum admission absorbs a repeat at the EVENT level, but the item
        level never presents one: the item-to-event translation numbers a
        fresh datum from the base's own datum count, so the token is new
        every time.  Absorption downstream does not make a self-loop
        upstream."""

        for _, base in survey.rectangle():
            after = add.act(base, (NewDatum(),))
            self.assertIsNotNone(after)
            self.assertNotEqual(after, base)

    def test_a_rule_repeat_is_a_self_loop_but_is_never_enumerated(self) -> None:
        """Absorbing and offered are different questions.  The sealed
        one-item enumerator subtracts the standing rules, so a rule
        self-loop exists and the estate never proposes one."""

        found = False
        for _, base in survey.rectangle():
            if not base.rules:
                continue
            found = True
            form = sorted(base.rules)[0]
            self.assertEqual(add.act(base, (NewRuleAll(form),)), base)
            enumerated = [d for d in iter_full_deltas(base, 1, survey.BOUNDS)]
            self.assertNotIn((NewRuleAll(form),), enumerated)
        self.assertTrue(found, "the rectangle carries no standing rule")

    def test_depth_one_answers_the_question_vacuously(self) -> None:
        """Why the declared depth is two.  A shallower rectangle would have
        reported no closed walk, and `FW-VACUOUS` refuses that as a
        finding."""

        shallow = survey.rectangle(depth=1)
        self.assertTrue(all(not base.insts and not base.rules for _, base in shallow))


class Circulation(unittest.TestCase):
    def test_the_witness_has_equal_endpoints(self) -> None:
        witness = survey.circulation_witness()
        self.assertTrue(witness["endpoints_equal"])

    def test_every_difference_cost_agrees_and_the_item_count_does_not(self) -> None:
        witness = survey.circulation_witness()
        self.assertTrue(witness["every_difference_cost_agrees"])
        self.assertTrue(witness["item_count_differs"])

    def test_the_step_by_step_total_equals_the_endpoint_difference(self) -> None:
        """Telescoping, computed rather than assumed: `path_total_diff`
        sums step by step and never looks at the endpoints."""

        for name, base in survey.rectangle()[:6]:
            path = []
            here = base
            for _ in range(2):
                moves = list(iter_full_deltas(here, 1, survey.BOUNDS))
                if not moves:
                    break
                path.append(moves[0])
                nxt = add.act(here, moves[0])
                assert nxt is not None
                here = nxt
            for label, functional in add.FUNCTIONALS.items():
                stepwise = add.path_total_diff(functional, base, path)
                end = add.path_end(base, path)
                assert end is not None
                self.assertEqual(
                    stepwise, functional(end) - functional(base), f"{name} {label}"
                )


class ReceiptReplay(unittest.TestCase):
    def test_the_committed_receipt_replays_byte_for_byte(self) -> None:
        import run_additivity

        committed = (HERE / "receipts" / "reach_additivity.json").read_text("utf-8")
        fresh = json.dumps(
            run_additivity.build(), indent=2, sort_keys=True, ensure_ascii=True
        ) + "\n"
        self.assertEqual(committed, fresh)


if __name__ == "__main__":
    unittest.main()
