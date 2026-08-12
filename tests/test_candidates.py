"""Tests for candidate deltas: enumeration completeness, fast-vs-naive
validity agreement, cost measures, and the negative (smuggling /
false-minimality) results discovered during the derivation."""

from __future__ import annotations

import pytest

from derivation.candidates import (
    Bounds,
    Delta,
    MinResponses,
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    NodeView,
    apply_delta,
    canonical_delta,
    delta_events,
    item_key,
    iter_cost1_items,
    iter_cost2_deltas,
    iter_full_deltas,
    min_responses,
    mu1,
    mu2,
    profile_additions,
    response_valid_fast,
    response_valid_naive,
)
from derivation.model import (
    AdmissionError,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    Pair,
    Regime,
    replay,
)

BOUNDS = Bounds(max_items=2, max_arity=2)


def _r2() -> Regime:
    """Reading L regime at the Challenge 3 situation (before Impose)."""
    return replay([AdmitDatum("<a>"), AdmitDatum("<ab>")])


def _marked() -> Regime:
    """Two data, one unary form, datum 1 marked, requirement imposed."""
    return replay(
        [
            AdmitDatum("<a>"),
            AdmitDatum("<ab>"),
            Impose(0, 1),
            AdmitForm(1),
            AdmitInst(0, (1,)),
        ]
    )


def _rich() -> Regime:
    """Three data, unary + binary forms, some instances, one requirement.

    Small but structurally mixed regime used for exhaustive cross-checks."""
    return replay(
        [
            AdmitDatum("x"),
            AdmitDatum("y"),
            AdmitDatum("z"),
            Impose(0, 1),
            AdmitForm(1),
            AdmitForm(2),
            AdmitInst(0, (1,)),
            AdmitInst(1, (0, 2)),
        ]
    )


def test_item_key_orders_kinds_canonically() -> None:
    delta = canonical_delta(
        (NewInst(0, (0,)), NewForm(1), NewDatum(), NewRuleAll(0))
    )
    kinds = [type(it).__name__ for it in delta]
    assert kinds == ["NewDatum", "NewForm", "NewRuleAll", "NewInst"]
    assert item_key(NewForm(1)) < item_key(NewForm(2))


def test_measures() -> None:
    d: Delta = canonical_delta((NewForm(2), NewInst(0, (0, 1))))
    assert mu1(d) == 2
    assert mu2(d) == (2, 2)
    assert mu2((NewDatum(), NewInst(0, (0, 2)))) == (2, 0)


def test_delta_events_fresh_tokens_are_positional() -> None:
    base = _r2()
    events = delta_events(base, (NewDatum(), NewDatum()))
    assert [e.token for e in events] == ["w2", "w3"]  # type: ignore[union-attr]
    r = apply_delta(base, (NewDatum(), NewDatum()))
    assert r.data == ("<a>", "<ab>", "w2", "w3")


def test_apply_delta_rejects_ill_formed() -> None:
    with pytest.raises(AdmissionError):
        apply_delta(_r2(), (NewInst(0, (0,)),))  # no form admitted
    with pytest.raises(AdmissionError):
        apply_delta(_r2(), (NewRuleAll(0),))
    with pytest.raises(AdmissionError):
        apply_delta(_marked(), (NewInst(0, (5,)),))


def test_nodeview_requires_rule_free_base() -> None:
    base = replay([AdmitDatum("x"), AdmitForm(1), AdmitRuleAll(0)])
    with pytest.raises(ValueError):
        NodeView.of(base)


def test_profile_additions_multi_position_instance() -> None:
    """A diagonal instance contributes every nonempty hole subset."""
    base = replay([AdmitDatum("x"), AdmitDatum("y"), AdmitForm(2)])
    view = NodeView.of(base)
    adds, n_total = profile_additions(view, (NewInst(0, (0, 0)),))
    assert n_total == 2
    assert adds[0] == {
        (0, (None, 0)),
        (0, (0, None)),
        (0, (None, None)),
    }
    assert 1 not in adds


def test_profile_additions_rule_floods_every_datum() -> None:
    base = replay([AdmitDatum("x"), AdmitDatum("y"), AdmitForm(1)])
    view = NodeView.of(base)
    adds, _ = profile_additions(view, (NewRuleAll(0),))
    assert adds[0] == adds[1] == {(0, (None,))}


def test_fast_equals_naive_on_full_space() -> None:
    """Cross-validation: the fast incremental validity check agrees with
    the naive replay-based check on every well-formed delta of cost <= 2,
    on both a bare and a structurally rich base regime."""
    for base, target in ((_r2(), (0, 1)), (_rich(), (1, 2))):
        view = NodeView.of(base)
        for cost in (0, 1, 2):
            for delta in iter_full_deltas(base, cost, BOUNDS):
                fast = response_valid_fast(view, target, delta)
                naive = response_valid_naive(base, target, delta)
                assert fast == naive, (base, target, delta)


def test_pruned_cost2_contains_every_valid_full_delta() -> None:
    """Completeness certificate for the pruned enumeration: every valid
    cost-2 delta in the full space that contains no rule item and no
    irrelevant (unreferenced) datum/form appears in the pruned space; and
    every valid rule-bearing or irrelevant-item delta has a valid sub-delta
    (so it is never a *minimum*)."""
    for base, target in ((_r2(), (0, 1)), (_marked(), (0, 1)), (_rich(), (1, 2))):
        view = NodeView.of(base)
        pruned = set(iter_cost2_deltas(base, BOUNDS, target))
        for delta in iter_full_deltas(base, 2, BOUNDS):
            if not response_valid_fast(view, target, delta):
                continue
            if delta in pruned:
                continue
            # Excluded but valid: must have a valid strict sub-delta.
            subs = [
                (delta[0],),
                (delta[1],),
            ]
            ok = False
            for sub in subs:
                try:
                    apply_delta(base, sub)
                except AdmissionError:
                    continue
                if response_valid_naive(base, target, sub):
                    ok = True
                    break
            assert ok, f"excluded valid delta with no valid sub-delta: {delta}"


def test_c3_cost1_all_fail_and_min_is_two() -> None:
    """No zero- or one-item delta separates <a> from <ab> at Challenge 3."""
    base = _r2()
    view = NodeView.of(base)
    target: Pair = (0, 1)
    assert not response_valid_fast(view, target, ())
    for it in iter_cost1_items(base, BOUNDS):
        assert not response_valid_fast(view, target, (it,))
    mr = min_responses(base, target, "mu1", BOUNDS)
    assert mr is not None and mr.cost[0] == 2
    assert len(mr.deltas) == 6  # 2 unary marks + 4 binary variants


def test_c3_mu2_minimum_is_unary_mark() -> None:
    mr = min_responses(_r2(), (0, 1), "mu2", BOUNDS)
    assert mr is not None
    assert mr.cost == (2, 1)
    assert mr.deltas == (
        canonical_delta((NewForm(1), NewInst(0, (0,)))),
        canonical_delta((NewForm(1), NewInst(0, (1,)))),
    )


def test_new_datum_alone_never_separates() -> None:
    """Negative: admitting a fresh datum does not affect any profile of
    previously admitted data (datum-irrelevance)."""
    for base, target in ((_r2(), (0, 1)), (_marked(), (0, 1))):
        view = NodeView.of(base)
        adds, _ = profile_additions(view, (NewDatum(),))
        assert adds == {}
        assert response_valid_fast(view, target, (NewDatum(),)) == (
            response_valid_fast(view, target, ())
        )


def test_rule_never_appears_in_minimum_responses() -> None:
    """Negative (rule-removal lemma): on a base where some responses are
    valid, no minimum response contains a uniform rule; moreover for every
    valid rule-bearing delta in the full space, dropping the rule item
    preserves validity."""
    base = _rich()
    view = NodeView.of(base)
    target: Pair = (1, 2)
    mr = min_responses(base, target, "mu1", BOUNDS)
    assert mr is not None
    for delta in mr.deltas:
        assert not any(isinstance(it, NewRuleAll) for it in delta)
    for delta in iter_full_deltas(base, 2, BOUNDS):
        if not any(isinstance(it, NewRuleAll) for it in delta):
            continue
        if not response_valid_fast(view, target, delta):
            continue
        rest = tuple(it for it in delta if not isinstance(it, NewRuleAll))
        try:
            apply_delta(base, rest)
        except AdmissionError:  # pragma: no cover - rest is always wf here
            continue
        assert response_valid_naive(base, target, rest)


def test_smuggling_a_bundle_is_not_one_item() -> None:
    """Negative: a 'single step' that silently bundles a form and an
    instance has measured cost 2, not 1."""
    bundle = canonical_delta((NewForm(1), NewInst(0, (1,))))
    assert mu1(bundle) == 2


def test_min_responses_rejects_unknown_measure() -> None:
    with pytest.raises(ValueError):
        min_responses(_r2(), (0, 1), "mu3", BOUNDS)


def test_iter_full_deltas_rejects_unsupported_cost() -> None:
    with pytest.raises(ValueError):
        list(iter_full_deltas(_r2(), 3, BOUNDS))


def test_min_responses_none_when_no_bounded_response() -> None:
    """A regime engineered so that no delta of <= 2 items can satisfy all
    requirements: impossible to build with the progress lemma in force,
    so exercise the None path with max_items=0."""
    mr = min_responses(_r2(), (0, 1), "mu1", Bounds(max_items=0, max_arity=2))
    assert mr is None


def test_min_responses_cost1_path() -> None:
    """After the unary mark, separating a fresh collapsed datum needs only
    one instance (cost 1)."""
    base = replay(
        [
            AdmitDatum("g2"),
        ],
        _marked(),
    )
    mr = min_responses(base, (0, 2), "mu1", BOUNDS)
    assert mr is not None
    assert mr.cost[0] == 1
    assert canonical_delta((NewInst(0, (2,)),)) in mr.deltas


def test_minresponses_structure() -> None:
    mr = min_responses(_r2(), (0, 1), "mu1", BOUNDS)
    assert isinstance(mr, MinResponses)
    assert mr.measure == "mu1"
    assert mr.complete_within == BOUNDS
