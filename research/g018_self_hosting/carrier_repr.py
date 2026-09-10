"""Object carrier representation for G018 Self-Hosting.

Represents an execution engine's own transition function, state graph,
and operational configurations inside the object carrier (states, transitions,
cursor, tape, fuel).

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


class CarrierEncodingError(ValueError):
    """Refusal for malformed or non-deterministic carrier representations."""


@dataclass(frozen=True)
class Transition:
    """A single deterministic state-graph transition edge."""

    curr_state: int
    read_sym: int
    next_state: int
    write_sym: int
    move_cursor: int  # -1 (left), 0 (stay), 1 (right)
    halt: bool

    def __post_init__(self) -> None:
        if self.curr_state < 0:
            raise CarrierEncodingError(f"curr_state must be non-negative: {self.curr_state}")
        if self.read_sym < 0:
            raise CarrierEncodingError(f"read_sym must be non-negative: {self.read_sym}")
        if self.next_state < 0:
            raise CarrierEncodingError(f"next_state must be non-negative: {self.next_state}")
        if self.write_sym < 0:
            raise CarrierEncodingError(f"write_sym must be non-negative: {self.write_sym}")
        if self.move_cursor not in (-1, 0, 1):
            raise CarrierEncodingError(f"move_cursor must be -1, 0, or 1: {self.move_cursor}")

    def serialize(self) -> tuple[int, ...]:
        """Serialize transition to a 6-tuple of integers."""
        return (
            self.curr_state,
            self.read_sym,
            self.next_state,
            self.write_sym,
            self.move_cursor + 1,  # map {-1, 0, 1} -> {0, 1, 2} for non-negative encoding
            1 if self.halt else 0,
        )

    @classmethod
    def deserialize(cls, items: Sequence[int]) -> Transition:
        """Deserialize from integer sequence."""
        if len(items) != 6:
            raise CarrierEncodingError(f"Transition requires 6 integers, got {len(items)}")
        curr_state, read_sym, next_state, write_sym, raw_move, raw_halt = items
        return cls(
            curr_state=curr_state,
            read_sym=read_sym,
            next_state=next_state,
            write_sym=write_sym,
            move_cursor=raw_move - 1,
            halt=(raw_halt != 0),
        )


@dataclass(frozen=True)
class MachineSpec:
    """Deterministic transition table and machine parameters."""

    transitions: tuple[Transition, ...]
    default_sym: int = 0

    def __post_init__(self) -> None:
        # Enforce determinism: at most one transition per (curr_state, read_sym)
        seen: set[tuple[int, int]] = set()
        for t in self.transitions:
            key = (t.curr_state, t.read_sym)
            if key in seen:
                raise CarrierEncodingError(f"Non-deterministic transition table: duplicate key {key}")
            seen.add(key)

    @property
    def num_states(self) -> int:
        """Total distinct state indices referenced."""
        if not self.transitions:
            return 0
        states: set[int] = set()
        for t in self.transitions:
            states.add(t.curr_state)
            states.add(t.next_state)
        return max(states) + 1 if states else 0

    def lookup(self, curr_state: int, read_sym: int) -> Transition | None:
        """Look up transition for current state and read symbol."""
        for t in self.transitions:
            if t.curr_state == curr_state and t.read_sym == read_sym:
                return t
        return None


@dataclass(frozen=True)
class MachineState:
    """Operational machine configuration inside the carrier."""

    state: int
    cursor: int
    tape: tuple[int, ...]
    fuel: int
    halted: bool

    def __post_init__(self) -> None:
        if self.state < 0:
            raise CarrierEncodingError(f"state must be non-negative: {self.state}")
        if self.cursor < 0:
            raise CarrierEncodingError(f"cursor must be non-negative: {self.cursor}")
        if self.fuel < 0:
            raise CarrierEncodingError(f"fuel must be non-negative: {self.fuel}")

    def read_symbol(self, default_sym: int = 0) -> int:
        """Read the symbol under the cursor."""
        if self.cursor < len(self.tape):
            return self.tape[self.cursor]
        return default_sym

    def write_symbol(self, sym: int, default_sym: int = 0) -> tuple[int, ...]:
        """Produce updated tape with symbol written at current cursor position."""
        if self.cursor < len(self.tape):
            tape_list = list(self.tape)
            tape_list[self.cursor] = sym
            return tuple(tape_list)
        # Extend tape up to cursor
        tape_list = list(self.tape)
        while len(tape_list) < self.cursor:
            tape_list.append(default_sym)
        tape_list.append(sym)
        return tuple(tape_list)


# Tag Constants for flat carrier serialization
TAG_SPEC_START = 1001
TAG_TRANS_ITEM = 1002
TAG_SPEC_END = 1003
TAG_STATE = 1004
TAG_CURSOR = 1005
TAG_TAPE_START = 1006
TAG_TAPE_END = 1007
TAG_FUEL = 1008
TAG_HALTED = 1009
TAG_EOF = 1010


def encode_carrier(spec: MachineSpec, state: MachineState) -> tuple[int, ...]:
    """Encode machine specification and operational state into a flat carrier tape."""
    words: list[int] = [TAG_SPEC_START, spec.default_sym, len(spec.transitions)]
    for t in spec.transitions:
        words.append(TAG_TRANS_ITEM)
        words.extend(t.serialize())
    words.append(TAG_SPEC_END)

    words.extend([TAG_STATE, state.state])
    words.extend([TAG_CURSOR, state.cursor])
    words.append(TAG_TAPE_START)
    words.append(len(state.tape))
    words.extend(state.tape)
    words.append(TAG_TAPE_END)
    words.extend([TAG_FUEL, state.fuel])
    words.extend([TAG_HALTED, 1 if state.halted else 0])
    words.append(TAG_EOF)
    return tuple(words)


def decode_carrier(data: Sequence[int]) -> tuple[MachineSpec, MachineState]:
    """Decode machine specification and state from flat carrier sequence."""
    idx = 0

    def consume(expected: int) -> None:
        nonlocal idx
        if idx >= len(data) or data[idx] != expected:
            val = data[idx] if idx < len(data) else "EOF"
            raise CarrierEncodingError(f"Expected tag {expected} at pos {idx}, got {val}")
        idx += 1

    def next_int() -> int:
        nonlocal idx
        if idx >= len(data):
            raise CarrierEncodingError("Unexpected EOF reading integer")
        val = data[idx]
        idx += 1
        return val

    consume(TAG_SPEC_START)
    default_sym = next_int()
    n_trans = next_int()
    transitions: list[Transition] = []
    for _ in range(n_trans):
        consume(TAG_TRANS_ITEM)
        items = [next_int() for _ in range(6)]
        transitions.append(Transition.deserialize(items))
    consume(TAG_SPEC_END)
    spec = MachineSpec(transitions=tuple(transitions), default_sym=default_sym)

    consume(TAG_STATE)
    st = next_int()

    consume(TAG_CURSOR)
    cur = next_int()

    consume(TAG_TAPE_START)
    tape_len = next_int()
    tape_items = tuple(next_int() for _ in range(tape_len))
    consume(TAG_TAPE_END)

    consume(TAG_FUEL)
    fuel = next_int()

    consume(TAG_HALTED)
    halted = (next_int() != 0)

    consume(TAG_EOF)
    state = MachineState(state=st, cursor=cur, tape=tape_items, fuel=fuel, halted=halted)
    return spec, state


def step_direct(spec: MachineSpec, state: MachineState) -> MachineState:
    """Direct execution step of the transition machine."""
    if state.halted or state.fuel == 0:
        return state

    read_sym = state.read_symbol(spec.default_sym)
    trans = spec.lookup(state.state, read_sym)

    if trans is None:
        # Undefined transition halts the machine, consuming 1 unit of fuel
        return MachineState(
            state=state.state,
            cursor=state.cursor,
            tape=state.tape,
            fuel=state.fuel - 1,
            halted=True,
        )

    new_tape = state.write_symbol(trans.write_sym, spec.default_sym)
    new_cursor = max(0, state.cursor + trans.move_cursor)
    return MachineState(
        state=trans.next_state,
        cursor=new_cursor,
        tape=new_tape,
        fuel=state.fuel - 1,
        halted=trans.halt,
    )


def run_direct(spec: MachineSpec, state: MachineState, max_steps: int | None = None) -> MachineState:
    """Iterate direct steps until halted, out of fuel, or step limit reached."""
    curr = state
    steps = 0
    while not curr.halted and curr.fuel > 0:
        if max_steps is not None and steps >= max_steps:
            break
        curr = step_direct(spec, curr)
        steps += 1
    return curr
