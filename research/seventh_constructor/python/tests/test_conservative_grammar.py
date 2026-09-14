"""Tests for conservative event grammar, preconditions, and transition semantics.

AuthorityEffect: None.
"""

from __future__ import annotations

from pathlib import Path
import sys
import pytest

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(REPO_ROOT / "code") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code"))

from derivation.model import (
    EMPTY,
    AdmissionError,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    Regime,
)
from derivation.iso import canonical
from research.seventh_constructor.python.conservative_grammar import (
    SwapWitness,
    admitting_regime,
    cardinal_potential,
    check_swap_preconditions,
    step_swap,
    verify_cardinality_preservation,
    verify_isomorphism_preservation,
    verify_swap_involution,
)


@pytest.fixture
def asymmetric_regime_2() -> Regime:
    """Regime with 2 data tokens and asymmetric instance (0, 1)."""
    r = EMPTY
    r = r.__class__(r.data + ("a", "b"), (2,), frozenset(), frozenset(), frozenset())
    r = r.__class__(r.data, r.forms, frozenset({(0, (0, 1))}), r.rules, r.reqs)
    return r


@pytest.fixture
def complex_regime_3() -> Regime:
    """Regime with 3 tokens, 2 forms, instances, a rule, and a separation requirement."""
    r = EMPTY
    r = r.__class__(r.data + ("a", "b", "c"), (2, 1), frozenset(), frozenset(), frozenset())
    r = r.__class__(r.data, r.forms, frozenset({(0, (0, 1)), (1, (2,))}), frozenset({1}), frozenset({(0, 2)}))
    return r


def test_swap_preconditions_reject_small_regime() -> None:
    """Admitting condition requires at least 2 data tokens."""
    r_empty = EMPTY
    assert not admitting_regime(r_empty)
    with pytest.raises(AdmissionError, match="requires at least 2 data tokens"):
        check_swap_preconditions(r_empty, SwapWitness(0, 1))

    r_one = EMPTY.__class__(("a",), (), frozenset(), frozenset(), frozenset())
    assert not admitting_regime(r_one)
    with pytest.raises(AdmissionError, match="requires at least 2 data tokens"):
        check_swap_preconditions(r_one, SwapWitness(0, 1))


def test_swap_preconditions_reject_identical_indices(asymmetric_regime_2: Regime) -> None:
    """Swap requires distinct indices."""
    with pytest.raises(AdmissionError, match="must be distinct"):
        check_swap_preconditions(asymmetric_regime_2, SwapWitness(0, 0))


def test_swap_preconditions_reject_out_of_range(asymmetric_regime_2: Regime) -> None:
    """Swap indices must be strictly within [0, n_data)."""
    with pytest.raises(AdmissionError, match="out of range"):
        check_swap_preconditions(asymmetric_regime_2, SwapWitness(0, 2))
    with pytest.raises(AdmissionError, match="out of range"):
        check_swap_preconditions(asymmetric_regime_2, SwapWitness(-1, 1))


def test_cardinality_preservation(asymmetric_regime_2: Regime, complex_regime_3: Regime) -> None:
    """Theorem 1.1 / R1: Cardinal potential N(r) is preserved under swap."""
    swap_01 = SwapWitness(0, 1)
    assert verify_cardinality_preservation(asymmetric_regime_2, swap_01)
    assert verify_cardinality_preservation(complex_regime_3, swap_01)

    swap_12 = SwapWitness(1, 2)
    assert verify_cardinality_preservation(complex_regime_3, swap_12)


def test_swap_involution(asymmetric_regime_2: Regime, complex_regime_3: Regime) -> None:
    """Theorem 1.7: Swap is strictly involutive e_swap(e_swap(r)) == r."""
    swap_01 = SwapWitness(0, 1)
    assert verify_swap_involution(asymmetric_regime_2, swap_01)
    assert verify_swap_involution(complex_regime_3, swap_01)

    swap_02 = SwapWitness(0, 2)
    assert verify_swap_involution(complex_regime_3, swap_02)


def test_isomorphism_preservation(asymmetric_regime_2: Regime, complex_regime_3: Regime) -> None:
    """Theorem 2.9: Swapped regime has identical canonical key (isomorphic)."""
    swap_01 = SwapWitness(0, 1)
    assert verify_isomorphism_preservation(asymmetric_regime_2, swap_01)
    assert verify_isomorphism_preservation(complex_regime_3, swap_01)


def test_asymmetric_regime_state_distinctness(asymmetric_regime_2: Regime) -> None:
    """Theorem 2.3: In-place exchange yields a distinct presentation state when asymmetric."""
    r_after = step_swap(asymmetric_regime_2, SwapWitness(0, 1))
    assert r_after != asymmetric_regime_2
    assert (0, (1, 0)) in r_after.insts
    assert (0, (0, 1)) not in r_after.insts
    assert r_after.data == ("b", "a")
