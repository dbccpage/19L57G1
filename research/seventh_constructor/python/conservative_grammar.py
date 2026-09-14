"""Conservative 7th constructor (e_swap) grammar, preconditions, and transition semantics.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Sequence, Union

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(REPO_ROOT / "code") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code"))

from derivation.model import (
    AdmissionError,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Regime,
    Supply,
    step as native_step,
)
from derivation.iso import canonical


@dataclass(frozen=True)
class SwapWitness:
    """The 7th constructor: in-place witness exchange e_swap(i, j).

    Transposes retained witness coordinates i and j on the carrier.
    Preserves cardinal potential N(r) = |D| + |F| + |I| + |R| + |Q|.
    """

    i: int
    j: int


ExtendedEvent = Union[Event, SwapWitness]


def cardinal_potential(r: Regime) -> int:
    """Cardinal potential N(r) = |D| + |F| + |I| + |R| + |Q|."""
    return len(r.data) + len(r.forms) + len(r.insts) + len(r.rules) + len(r.reqs)


def admitting_regime(r: Regime) -> bool:
    """Precondition: regime must contain at least 2 distinct retained data witnesses."""
    return r.n_data() >= 2


def check_swap_preconditions(r: Regime, e: SwapWitness) -> None:
    """Verify operational preconditions for e_swap without external tokens."""
    n = r.n_data()
    if n < 2:
        raise AdmissionError(f"admitting regime requires at least 2 data tokens, got {n}")
    if not (0 <= e.i < n and 0 <= e.j < n):
        raise AdmissionError(f"swap indices ({e.i}, {e.j}) out of range for n_data={n}")
    if e.i == e.j:
        raise AdmissionError(f"swap indices must be distinct, got {e.i} == {e.j}")


def step_swap(r: Regime, e: SwapWitness) -> Regime:
    """Apply the 7th constructor e_swap(i, j) to regime r."""
    check_swap_preconditions(r, e)
    i, j = e.i, e.j

    # Permute presentation tokens
    data_list = list(r.data)
    data_list[i], data_list[j] = data_list[j], data_list[i]
    new_data = tuple(data_list)

    # Transposition function on coordinates
    def tau(x: int) -> int:
        if x == i:
            return j
        if x == j:
            return i
        return x

    # Permute relational instances
    new_insts = frozenset(
        (form, tuple(tau(arg) for arg in args)) for (form, args) in r.insts
    )

    # Forms and rules are invariant under data permutation
    new_forms = r.forms
    new_rules = r.rules

    # Permute separation requirements
    new_reqs = frozenset(
        (min(tau(a), tau(b)), max(tau(a), tau(b))) for (a, b) in r.reqs
    )

    return Regime(new_data, new_forms, new_insts, new_rules, new_reqs)


def extended_step(r: Regime, e: ExtendedEvent) -> Regime:
    """Apply an event from the extended event grammar."""
    if isinstance(e, SwapWitness):
        return step_swap(r, e)
    return native_step(r, e)


def verify_cardinality_preservation(r: Regime, e: SwapWitness) -> bool:
    """Verify that e_swap strictly preserves cardinal potential N(step(r, e)) == N(r)."""
    n_before = cardinal_potential(r)
    r_after = step_swap(r, e)
    n_after = cardinal_potential(r_after)
    return n_before == n_after


def verify_swap_involution(r: Regime, e: SwapWitness) -> bool:
    """Verify that applying e_swap twice returns exactly to the initial regime."""
    r_swapped = step_swap(r, e)
    r_restored = step_swap(r_swapped, e)
    return r_restored == r


def verify_isomorphism_preservation(r: Regime, e: SwapWitness) -> bool:
    """Verify that e_swap maps r to an isomorphic regime under canonical quotient."""
    r_swapped = step_swap(r, e)
    return canonical(r) == canonical(r_swapped)
