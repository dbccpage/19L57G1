"""Commuting dynamics square and fuel-independence across observation scales.

AuthorityEffect: None.
Mirrors Lean 4 constructive formalization in Commute.lean.

Key concepts:
- Commuting Dynamics Square:
    bond_n(step_{n+1}(x)) = step_n(bond_n(x))
- Realization 1: Observation trace square:
    Let Tr_{n}(s) = (obs(0, s), ..., obs(n, s)).
    bond_trace(Tr_{n+1}(s)) = Tr_n(s).
    step_trace(Tr_n(s)) = Tr_n(next_state(s)).
    Then bond_trace(step_trace(Tr_{n+1}(s))) == step_trace(bond_trace(Tr_{n+1}(s))).
- Realization 2: Pointwise transition square on thread stages:
    For any transition law F : Fin c -> Fin c,
    step_stage(w) = (F(w_0), ..., F(w_{n-1})).
    bond(step_stage(w)) == step_stage(bond(w)).
    Induces continuous endomorphism step_thread on the thread space.
- Fuel independence and boundary failure:
    Commuting holds when fuel >= n + 1. If fuel is exhausted, the transition stalls.
- Non-local shift failure:
    Shift on arbitrary words cannot be computed from prefixes without external future data.
"""

from __future__ import annotations

from typing import Callable, Sequence

from limits import Word, bond, compatible, of_seq, to_seq
from observe import State, next_state, obs, obs_trace


def step_stage(func: Callable[[int], int], w: Word) -> Word:
    """Dynamic step on a finite stage: apply transition law F pointwise."""
    return tuple(func(x) for x in w)


def verify_stage_commuting_square(func: Callable[[int], int], w: Word) -> bool:
    """Verify bond_n(step_{n+1}(w)) == step_n(bond_n(w))."""
    if len(w) == 0:
        return True
    left = bond(step_stage(func, w))
    right = step_stage(func, bond(w))
    return left == right


def step_thread(func: Callable[[int], int], family: Sequence[Word]) -> tuple[Word, ...]:
    """Lift transition map F to an endomorphism on the thread space."""
    return tuple(step_stage(func, stage) for stage in family)


def verify_thread_step_compatibility(func: Callable[[int], int], family: Sequence[Word]) -> bool:
    """Verify that applying step_thread to a compatible thread yields a compatible thread."""
    if not compatible(family):
        return False
    stepped = step_thread(func, family)
    return compatible(stepped)


def verify_thread_sequence_commute(
    func: Callable[[int], int], family: Sequence[Word], max_idx: int
) -> bool:
    """Verify to_seq(step_thread(t), i) == F(to_seq(t, i))."""
    stepped = step_thread(func, family)
    for i in range(min(max_idx, len(family) - 1)):
        if to_seq(stepped, i) != func(to_seq(family, i)):
            return False
    return True


def bond_trace(tr: tuple[Word, ...]) -> tuple[Word, ...]:
    """Bonding map on observation traces: forget the last observation."""
    return tr[:-1]


def step_trace(n: int, s: State) -> tuple[Word, ...]:
    """Trace of n observations after advancing the state by one step."""
    s_next = next_state(s)
    return obs_trace(n, s_next)


def verify_trace_commuting_square(s: State, n: int) -> bool:
    """Verify that the observation trace square commutes:
    bond_trace(step_trace(n + 1, s)) == step_trace(n, s)
    """
    left = bond_trace(step_trace(n + 1, s))
    right = step_trace(n, s)
    return left == right


def verify_iter_next_commute(s: State, n: int) -> bool:
    """Verify that iterating n + 1 times from s equals iterating n times from next_state(s):
    obs(n + 1, s) == obs(n, next_state(s)).
    """
    return obs(n + 1, s) == obs(n, next_state(s))


def fuel_exhaustion_commute_obstruction(s: State, n: int) -> tuple[bool, Word, Word]:
    """Exhibit fuel boundary effect: if fuel is insufficient (e.g. fuel = n),
    stepping after scale n halts on exhausted terminal while higher fuel would proceed.
    """
    s_starved = s.with_fuel(n)
    s_ample = s.with_fuel(n + 1)

    obs_starved_succ = obs(n + 1, s_starved)
    obs_ample_succ = obs(n + 1, s_ample)
    commutes_under_starvation = obs_starved_succ == obs_ample_succ
    return commutes_under_starvation, obs_starved_succ, obs_ample_succ
