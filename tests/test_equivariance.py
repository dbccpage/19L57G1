"""Quotient-transition soundness: the challenge policy must be
isomorphism-equivariant.

Regression (caller correction, 2026-08-11): canonical parent quotient +
lexicographically least collapsed pair = non-equivariant transition."""

from __future__ import annotations

from itertools import permutations

from derivation.candidates import Bounds, delta_events, min_responses
from derivation.engine import closure_challenge_orbits, _quotient
from derivation.iso import CanonKey, automorphisms, canonical, rename
from derivation.model import (
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    Impose,
    Pair,
    Regime,
    replay,
)
from derivation.observe import collapsed_pairs

BOUNDS = Bounds(max_items=2, max_arity=2)


def _regression_regime() -> Regime:
    """Four data, one unary form, instances on data 2 and 3; collapsed
    pairs (0, 1) and (2, 3)."""
    return replay(
        [
            AdmitDatum("a"),
            AdmitDatum("b"),
            AdmitDatum("c"),
            AdmitDatum("d"),
            AdmitForm(1),
            AdmitInst(0, (2,)),
            AdmitInst(0, (3,)),
        ]
    )


def _children_for_challenge(r: Regime, target: Pair) -> frozenset[CanonKey]:
    """Canonical keys of the child regimes produced by all minimum valid
    responses to one separation challenge."""
    mr = min_responses(r, target, "mu1", BOUNDS)
    assert mr is not None
    return frozenset(
        canonical(
            replay(
                (Impose(target[0], target[1]),) + delta_events(r, rep),
                r,
            )
        )
        for rep, _ in _quotient(r, target, mr)
    )


def _expansion(r: Regime) -> frozenset[CanonKey]:
    """Canonical keys of all children across every challenge orbit."""
    out: set[CanonKey] = set()
    for target in closure_challenge_orbits(r):
        out |= _children_for_challenge(r, target)
    return frozenset(out)


def test_regression_canonical_equal_under_rename() -> None:
    r = _regression_regime()
    pi = (2, 3, 0, 1)
    rr = rename(r, pi, (0,))
    assert collapsed_pairs(r) == ((0, 1), (2, 3))
    assert collapsed_pairs(rr) == ((0, 1), (2, 3))
    assert canonical(r) == canonical(rr)


def test_least_pair_selection_is_not_equivariant() -> None:
    """Documents the repaired failure: under the old policy (challenge the
    lexicographically least collapsed pair of the stored representative),
    the isomorphic regimes r and rename(r, pi) issue index-pair (0, 1) in
    both labelings — but in r that is the unmarked pair and in the renamed
    regime the marked pair, so the produced children are non-isomorphic:
    the transition depended on the representative labeling."""
    r = _regression_regime()
    rr = rename(r, (2, 3, 0, 1), (0,))
    least_r = collapsed_pairs(r)[0]
    least_rr = collapsed_pairs(rr)[0]
    assert least_r == least_rr == (0, 1)
    assert _children_for_challenge(r, least_r) != _children_for_challenge(
        rr, least_rr
    )


def test_regression_orbits_are_distinct_and_both_retained() -> None:
    """The two collapsed pairs lie in distinct automorphism orbits (no
    automorphism exchanges the marked and unmarked pairs), so the policy
    retains both challenge branches."""
    r = _regression_regime()
    assert len(automorphisms(r)) == 4
    assert closure_challenge_orbits(r) == ((0, 1), (2, 3))


def test_orbit_policy_transition_congruence_exhaustive() -> None:
    """Transition congruence under isomorphism, exhaustively: for every
    data bijection of each sample regime, the renamed regime's expansion
    (all orbits, all minimum response classes) produces exactly the same
    set of child isomorphism classes."""
    samples = [
        _regression_regime(),
        # Challenge 3 situation, reading L
        replay([AdmitDatum("x"), AdmitDatum("y"), Impose(0, 1),
                AdmitForm(1), AdmitInst(0, (1,)), AdmitDatum("z")]),
        # four data, binary form, one link; (2, 3) still collapsed
        replay([AdmitDatum("w"), AdmitDatum("x"), AdmitDatum("y"),
                AdmitDatum("z"), Impose(0, 1), AdmitForm(2),
                AdmitInst(0, (0, 1))]),
    ]
    for r in samples:
        base_expansion = _expansion(r)
        assert base_expansion, "sample must have at least one orbit"
        for pi in permutations(range(r.n_data())):
            rr = rename(r, pi, tuple(range(len(r.forms))))
            assert canonical(rr) == canonical(r)
            assert _expansion(rr) == base_expansion, (r, pi)


def test_orbit_representatives_cover_all_collapsed_pairs() -> None:
    """Every collapsed pair belongs to exactly one challenge orbit."""
    from derivation.iso import pair_orbits

    r = _regression_regime()
    orbits = pair_orbits(r, collapsed_pairs(r))
    flat = [p for orbit in orbits for p in orbit]
    assert sorted(flat) == sorted(collapsed_pairs(r))
    assert len(flat) == len(set(flat))
