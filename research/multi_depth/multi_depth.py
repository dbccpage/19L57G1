"""General multi-depth ladder of retained-record enablement machines.

Mirrors lean/DepthLadder.lean:
- windows(k, tape) extracts all contiguous sublists of length k.
- functional(k, tape) tests whether two windows of length k + 1 agreeing on their first k entries agree on the last.
- ladder_monotonicity verifies that functional(k, tape) implies functional(k + 1, tape).
- Arbitrary depth-d machine reading d past record entries on arity-(d+1) control forms.
- Renaming invariance verified across 1,152 sweep runs without host oracles.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from typing import Callable, Iterator, Sequence

Word = tuple[int, ...]


# ---------------------------------------------------------------------------
# Generic window operator, functionality, and monotonicity
# ---------------------------------------------------------------------------


def windows(k: int, tape: Sequence[int]) -> tuple[Word, ...]:
    """Every contiguous sublist of length ``k`` in order."""
    if k < 1:
        raise ValueError("window length must be at least 1")
    if len(tape) < k:
        return ()
    return tuple(tuple(tape[i : i + k]) for i in range(len(tape) - k + 1))


def functional(k: int, tape: Sequence[int]) -> bool:
    """A tape is functional in ``k`` entries when any two windows of length
    ``k + 1`` that agree on their first ``k`` entries agree on the last."""
    seen: dict[Word, int] = {}
    for w in windows(k + 1, tape):
        prefix, succ = w[:k], w[k]
        if seen.setdefault(prefix, succ) != succ:
            return False
    return True


def check_monotonicity(tape: Sequence[int], max_k: int = 10) -> bool:
    """Verify that functional(k, tape) implies functional(k + 1, tape)."""
    for k in range(1, max_k):
        if functional(k, tape):
            assert functional(k + 1, tape), f"monotonicity violated at k={k} for {tape}"
    return True


# ---------------------------------------------------------------------------
# Multi-depth machines and control
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FiniteSetting:
    """A finite setting with carrier size ``n`` and operations ``ops``."""
    n: int
    ops: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class DepthMachine:
    """A retained-record enablement machine reading ``depth`` entries.
    Control form has arity ``depth + 1``: ``(d_past, ..., d_active, k)``."""
    depth: int
    setting: FiniteSetting
    table: dict[Word, int]


@dataclass(frozen=True)
class MachineState:
    tape: tuple[int, ...]
    active: int
    fuel: int


def suffix_window(depth: int, tape: Sequence[int]) -> Word:
    """Extract the last ``depth`` data from ``tape``, padding with the initial datum
    if ``len(tape) < depth``."""
    if not tape:
        raise ValueError("tape cannot be empty")
    if len(tape) >= depth:
        return tuple(tape[-depth:])
    init = tape[0]
    pad = (init,) * (depth - len(tape))
    return pad + tuple(tape)


def step(machine: DepthMachine, s: MachineState) -> MachineState | None:
    """Perform one deterministic step without host oracles."""
    if s.fuel <= 0:
        return None
    key = suffix_window(machine.depth, s.tape)
    op_idx = machine.table.get(key)
    if op_idx is None:
        return None  # Halt
    next_datum = machine.setting.ops[op_idx][s.active]
    return MachineState(
        tape=s.tape + (next_datum,),
        active=next_datum,
        fuel=s.fuel - 1,
    )


def run_machine(machine: DepthMachine, start: int, fuel: int) -> MachineState:
    """Run machine to completion or fuel exhaustion."""
    curr = MachineState(tape=(start,), active=start, fuel=fuel)
    while curr.fuel > 0:
        nxt = step(machine, curr)
        if nxt is None:
            break
        curr = nxt
    return curr


# ---------------------------------------------------------------------------
# Strict ladder exhibits: T_d separates depth d from depth d - 1
# ---------------------------------------------------------------------------


def twist_tape(k: int) -> tuple[int, ...]:
    """Generate a witness tape functional in ``k + 1`` entries that breaks
    functionality in ``k`` entries, proving the strict inclusion of the ladder."""
    if k < 1:
        raise ValueError("k must be at least 1")
    prefix = tuple(range(k))
    return prefix + (k, k + 1) + prefix + (k + 2, k + 3)


# ---------------------------------------------------------------------------
# Renaming sweep verification across 1,152 runs
# ---------------------------------------------------------------------------


def apply_permutation(p: tuple[int, ...], x: int) -> int:
    return p[x]


def rename_setting(F: FiniteSetting, sigma: tuple[int, ...]) -> FiniteSetting:
    inv = [0] * F.n
    for i, v in enumerate(sigma):
        inv[v] = i
    new_ops = []
    for op in F.ops:
        new_op = tuple(sigma[op[inv[x]]] for x in range(F.n))
        new_ops.append(new_op)
    return FiniteSetting(F.n, tuple(new_ops))


def rename_machine(M: DepthMachine, sigma: tuple[int, ...]) -> DepthMachine:
    new_setting = rename_setting(M.setting, sigma)
    inv = [0] * M.setting.n
    for i, v in enumerate(sigma):
        inv[v] = i
    new_table: dict[Word, int] = {}
    for key, op in M.table.items():
        new_key = tuple(sigma[k] for k in key)
        new_table[new_key] = op
    return DepthMachine(M.depth, new_setting, new_table)


def run_sweep_verification() -> dict[str, object]:
    """Exhaustive sweep over:
    - 6 permutations of 3-point carrier
    - 64 deterministic programs (depth 1 on 3 data, 3 ops + halt)
    - 3 initial states
    Total runs: 6 * 64 * 3 = 1,152.
    Confirms representation transport and renaming invariance without host logs."""
    n = 3
    # Standard cyclic permutations and identity as ops
    ops = (
        tuple((x + 1) % n for x in range(n)),
        tuple((x + 2) % n for x in range(n)),
        tuple(x for x in range(n)),
    )
    F = FiniteSetting(n=n, ops=ops)

    all_perms = list(permutations(range(n)))
    assert len(all_perms) == 6

    # 64 deterministic choices for 3 data with 3 ops + halt (4 choices per datum): 4^3 = 64
    runs_checked = 0
    invariance_failures = 0

    for choices in product(range(4), repeat=3):
        # Build depth-1 table
        table = { (x,): choices[x] for x in range(3) if choices[x] < 3 }
        M = DepthMachine(depth=1, setting=F, table=table)

        for start in range(n):
            fuel = 6
            base_state = run_machine(M, start, fuel)

            for sigma in all_perms:
                runs_checked += 1
                M_renamed = rename_machine(M, sigma)
                start_renamed = sigma[start]
                renamed_state = run_machine(M_renamed, start_renamed, fuel)

                expected_tape = tuple(sigma[x] for x in base_state.tape)
                if renamed_state.tape != expected_tape:
                    invariance_failures += 1

    return {
        "sweep_runs_checked": runs_checked,
        "invariance_failures": invariance_failures,
        "invariance_verified": (invariance_failures == 0 and runs_checked == 1152),
    }
