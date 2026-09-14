"""Tests for movegraph topology, 1-cycle generation, and quotient collapse.

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
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    Regime,
)
from research.seventh_constructor.python.conservative_grammar import (
    ExtendedEvent,
    SwapWitness,
    cardinal_potential,
    extended_step,
    step_swap,
)
from research.seventh_constructor.python.movegraph import Movegraph


@pytest.fixture
def asymmetric_r0() -> Regime:
    """Base asymmetric regime r0 matching Lean r0."""
    return Regime(("a", "b"), (2,), frozenset({(0, (0, 1))}), frozenset(), frozenset())


def test_native_movegraph_is_dag(asymmetric_r0: Regime) -> None:
    """Theorem 2.1: Native movegraph without swap is strictly acyclic DAG (Z_1 = 0)."""
    native_events: list[ExtendedEvent] = [
        AdmitDatum("c"),
        AdmitForm(1),
        AdmitInst(0, (1, 0)),
    ]
    mg = Movegraph(asymmetric_r0, native_events, max_depth=3)
    assert mg.is_acyclic_dag()
    assert mg.cycle_space_dimension() == 0
    assert len(mg.find_simple_cycles()) == 0


def test_extended_movegraph_generates_2_cycle(asymmetric_r0: Regime) -> None:
    """Theorems 2.2-2.4: Extended movegraph with swap generates explicit 2-cycle r0 <-> r1."""
    swap_01: list[ExtendedEvent] = [SwapWitness(0, 1)]
    mg = Movegraph(asymmetric_r0, swap_01, max_depth=3)

    assert not mg.is_acyclic_dag()
    cycles = mg.find_simple_cycles(max_cycle_len=2)
    assert len(cycles) >= 1

    cycle = cycles[0]
    assert len(cycle) == 2
    r_a = mg.regimes[cycle[0]]
    r_b = mg.regimes[cycle[1]]
    assert r_a != r_b
    assert cardinal_potential(r_a) == cardinal_potential(r_b)


def test_extended_movegraph_dim_z1_nontrivial(asymmetric_r0: Regime) -> None:
    """Theorem 2.8: 1-cycle space dimension is strictly non-zero (Z_1 != 0)."""
    swap_01: list[ExtendedEvent] = [SwapWitness(0, 1)]
    mg = Movegraph(asymmetric_r0, swap_01, max_depth=2)

    dim_z1 = mg.cycle_space_dimension()
    assert dim_z1 >= 1


def test_extended_movegraph_3_cycle() -> None:
    """Verify multi-step cycle generation on 3 tokens with transpositions (0, 1) and (1, 2)."""
    r_initial = Regime(("a", "b", "c"), (2,), frozenset({(0, (0, 1))}), frozenset(), frozenset())
    events: list[ExtendedEvent] = [SwapWitness(0, 1), SwapWitness(1, 2)]
    mg = Movegraph(r_initial, events, max_depth=4)

    cycles = mg.find_simple_cycles(max_cycle_len=6)
    assert len(cycles) >= 1


def test_quotient_projection_cycle_collapse(asymmetric_r0: Regime) -> None:
    """Theorems 2.10-2.11: Swap cycle collapses to a point in quotient, demonstrating non-descent."""
    swap_01: list[ExtendedEvent] = [SwapWitness(0, 1)]
    mg = Movegraph(asymmetric_r0, swap_01, max_depth=2)

    cycles = mg.find_simple_cycles(max_cycle_len=2)
    assert len(cycles) >= 1

    report = mg.evaluate_quotient_projection(cycles[0])
    assert report["collapses_to_point"] is True
    assert report["unique_quotient_states"] == 1
    assert report["descended_coboundary_vanishes"] is True
    assert report["presentation_non_descent_defect"] == 1
