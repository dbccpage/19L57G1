"""Tests for contexts, profiles, and observational equivalence."""

from __future__ import annotations

from derivation.model import (
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    replay,
    step,
)
from derivation.observe import (
    collapsed_pairs,
    contexts,
    derivable,
    plug,
    profile,
    profiles,
    satisfies,
    separable,
    slot_tuples,
    witness,
)


def _r2() -> object:
    return replay([AdmitDatum("<a>"), AdmitDatum("<ab>")])


def test_no_forms_means_no_contexts() -> None:
    r = _r2()
    assert contexts(r) == ()  # type: ignore[arg-type]
    assert profiles(r) == (frozenset(), frozenset())  # type: ignore[arg-type]


def test_slot_tuples_and_context_count() -> None:
    # arity 2 over 2 data: 3^2 slot tuples, 2^2 without holes.
    assert len(list(slot_tuples(2, 2))) == 9
    r = replay([AdmitDatum("x"), AdmitDatum("y"), AdmitForm(2)])
    assert len(contexts(r)) == 9 - 4


def test_plug_fills_every_hole_with_the_same_datum() -> None:
    assert plug((0, (None, 1, None)), 5) == (0, (5, 1, 5))


def test_derivable_via_instance_and_via_rule() -> None:
    base = replay([AdmitDatum("x"), AdmitForm(1)])
    assert not derivable(base, (0, (0,)))
    with_inst = step(base, AdmitInst(0, (0,)))
    assert derivable(with_inst, (0, (0,)))
    with_rule = step(base, AdmitRuleAll(0))
    assert derivable(with_rule, (0, (0,)))


def test_unary_mark_separates_and_witness() -> None:
    r = replay(
        [
            AdmitDatum("<a>"),
            AdmitDatum("<ab>"),
            AdmitForm(1),
            AdmitInst(0, (1,)),
        ]
    )
    assert separable(r, 0, 1)
    assert witness(r, 0, 1) == (0, (None,))
    assert profile(r, 1) == frozenset({(0, (None,))})
    assert profile(r, 0) == frozenset()


def test_collapsed_pairs_and_witness_none() -> None:
    r = _r2()
    assert collapsed_pairs(r) == ((0, 1),)  # type: ignore[arg-type]
    assert witness(r, 0, 1) is None  # type: ignore[arg-type]


def test_rule_floods_uniformly_no_separation() -> None:
    r = replay(
        [
            AdmitDatum("<a>"),
            AdmitDatum("<ab>"),
            AdmitForm(1),
            AdmitRuleAll(0),
        ]
    )
    assert not separable(r, 0, 1)
    assert profile(r, 0) == profile(r, 1) != frozenset()


def test_satisfies_both_ways() -> None:
    r = replay(
        [
            AdmitDatum("<a>"),
            AdmitDatum("<ab>"),
            Impose(0, 1),
        ]
    )
    assert not satisfies(r)
    ok = replay(
        [AdmitForm(1), AdmitInst(0, (1,))],
        r,
    )
    assert satisfies(ok)
