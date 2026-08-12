"""Tests for the implemented isomorphism relation and canonical forms."""

from __future__ import annotations

from itertools import permutations

import pytest

from derivation.iso import (
    IsoBudgetError,
    canonical,
    canonical_bruteforce,
    group_by_canonical,
    isomorphic,
    rename,
)
from derivation.model import (
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    Regime,
    replay,
)


def _mk(*events: object) -> Regime:
    return replay(list(events))  # type: ignore[arg-type]


U_A = _mk(
    AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(0, 1),
    AdmitForm(1), AdmitInst(0, (0,)),
)
U_B = _mk(
    AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(0, 1),
    AdmitForm(1), AdmitInst(0, (1,)),
)
B_LINK = _mk(
    AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(0, 1),
    AdmitForm(2), AdmitInst(0, (0, 1)),
)
B_LINK_R = _mk(
    AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(0, 1),
    AdmitForm(2), AdmitInst(0, (1, 0)),
)
B_DIAG = _mk(
    AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(0, 1),
    AdmitForm(2), AdmitInst(0, (0, 0)),
)
# Reading F shapes: three data, link to / from the never-required datum 0.
F_OUT = _mk(
    AdmitDatum("<>"), AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(1, 2),
    AdmitForm(2), AdmitInst(0, (1, 0)),
)
F_IN = _mk(
    AdmitDatum("<>"), AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(1, 2),
    AdmitForm(2), AdmitInst(0, (0, 1)),
)


def test_mark_variants_are_isomorphic() -> None:
    assert isomorphic(U_A, U_B)


def test_link_variants_are_isomorphic() -> None:
    assert isomorphic(B_LINK, B_LINK_R)


def test_arity_distinguishes_classes() -> None:
    assert not isomorphic(U_A, B_LINK)
    assert not isomorphic(U_A, B_DIAG)


def test_diag_is_not_link() -> None:
    assert not isomorphic(B_DIAG, B_LINK)


def test_direction_relative_to_requirement_matters() -> None:
    """A link out of the required pair is not isomorphic to a link into it:
    the bijection must preserve the requirement set, so it cannot swap the
    never-required datum with a required one."""
    assert not isomorphic(F_OUT, F_IN)


def test_tokens_are_forgotten() -> None:
    a = _mk(AdmitDatum("first"), AdmitForm(1), AdmitInst(0, (0,)))
    b = _mk(AdmitDatum("second"), AdmitForm(1), AdmitInst(0, (0,)))
    assert canonical(a) == canonical(b)


def test_canonical_invariant_under_rename() -> None:
    regimes = [U_A, B_LINK, B_DIAG, F_OUT, F_IN]
    for r in regimes:
        n, nf = r.n_data(), len(r.forms)
        for pi in permutations(range(n)):
            for phi in permutations(range(nf)):
                assert canonical(rename(r, pi, phi)) == canonical(r)


def test_agreement_with_bruteforce_on_pairs() -> None:
    """Equality of refined canonical keys agrees with equality of
    brute-force keys on every pair from a mixed collection."""
    collection = [U_A, U_B, B_LINK, B_LINK_R, B_DIAG, F_OUT, F_IN]
    for a in collection:
        for b in collection:
            assert (canonical(a) == canonical(b)) == (
                canonical_bruteforce(a) == canonical_bruteforce(b)
            )


def test_rule_sets_participate_in_canonical() -> None:
    plain = _mk(AdmitDatum("x"), AdmitForm(1))
    ruled = _mk(AdmitDatum("x"), AdmitForm(1), AdmitRuleAll(0))
    assert canonical(plain) != canonical(ruled)


def test_perm_budget_error() -> None:
    """Nine structureless data admit 9! candidate bijections, exceeding the
    default budget; the declared bound raises instead of silently
    truncating -- for canonicalization and for automorphism search."""
    from derivation.iso import automorphisms

    r = replay([AdmitDatum(f"d{i}") for i in range(9)])
    with pytest.raises(IsoBudgetError):
        canonical(r)
    with pytest.raises(IsoBudgetError):
        automorphisms(r)
    # An explicit larger budget succeeds.
    assert canonical(r, perm_budget=400_000)[0] == 9


def test_group_by_canonical_groups_and_preserves_order() -> None:
    groups = group_by_canonical(
        [(U_A, "a"), (U_B, "b"), (B_LINK, "c")]
    )
    assert sorted(len(v) for v in groups.values()) == [1, 2]
    for members in groups.values():
        if len(members) == 2:
            assert members == ["a", "b"]
