"""Fuel-Bounded Endogenous Structural Recursion.

Operational instruction interpreter and structural recursion scheme executing
entirely within the internal finitary substrate without host loop counters.

AuthorityEffect: None.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Sequence, TypeVar
from ordinals import Ordinal, Zero, Succ
from address import Address
from freshness import fresh_address

T = TypeVar("T")


# --- Values ---


class Val(ABC):
    """Endogenous machine value."""


@dataclass(frozen=True)
class NumVal(Val):
    """Ordinal numeric value."""

    val: Ordinal

    def __repr__(self) -> str:
        return f"NumVal({self.val!r})"


@dataclass(frozen=True)
class AddrVal(Val):
    """Tree address value."""

    addr: Address

    def __repr__(self) -> str:
        return f"AddrVal({self.addr!r})"


# --- Instructions ---


class Instr(ABC):
    """Endogenous machine instruction."""


@dataclass(frozen=True)
class Nop(Instr):
    """No operation."""


@dataclass(frozen=True)
class SetZero(Instr):
    """Set register to zero."""

    reg: Ordinal


@dataclass(frozen=True)
class SuccReg(Instr):
    """Increment ordinal register value."""

    reg: Ordinal


@dataclass(frozen=True)
class PredReg(Instr):
    """Decrement ordinal register value."""

    reg: Ordinal


@dataclass(frozen=True)
class CopyReg(Instr):
    """Copy value from src register to dst register."""

    dst: Ordinal
    src: Ordinal


@dataclass(frozen=True)
class AllocAddr(Instr):
    """Allocate a fresh tree address and store it into dst register."""

    dst: Ordinal


@dataclass(frozen=True)
class WriteMem(Instr):
    """Write value in val_reg to memory at tree address in addr_reg."""

    addr_reg: Ordinal
    val_reg: Ordinal


@dataclass(frozen=True)
class ReadMem(Instr):
    """Read value from memory at tree address in addr_reg into dst register."""

    dst: Ordinal
    addr_reg: Ordinal


@dataclass(frozen=True)
class Jump(Instr):
    """Unconditional jump to target ordinal."""

    target: Ordinal


@dataclass(frozen=True)
class BranchIfZero(Instr):
    """Branch to target ordinal if register holds NumVal(0)."""

    reg: Ordinal
    target: Ordinal


@dataclass(frozen=True)
class Halt(Instr):
    """Halt machine execution."""


# --- Machine State ---


@dataclass(frozen=True)
class State:
    """Pure finitary machine state."""

    pc: Ordinal = Zero()
    regs: tuple[tuple[Ordinal, Val], ...] = ()
    mem: tuple[tuple[Address, Val], ...] = ()
    addrs: tuple[Address, ...] = ()
    halted: bool = False

    def get_reg(self, r: Ordinal) -> Val:
        """Lookup register value, defaulting to NumVal(0)."""
        for k, v in self.regs:
            if k == r:
                return v
        return NumVal(Zero())

    def set_reg(self, r: Ordinal, v: Val) -> State:
        """Return state with updated register."""
        new_regs = ((r, v),) + self.regs
        return State(pc=self.pc, regs=new_regs, mem=self.mem, addrs=self.addrs, halted=self.halted)

    def get_mem(self, a: Address) -> Val:
        """Lookup memory value at address, defaulting to NumVal(0)."""
        for k, v in self.mem:
            if k == a:
                return v
        return NumVal(Zero())

    def set_mem(self, a: Address, v: Val) -> State:
        """Return state with updated memory."""
        new_mem = ((a, v),) + self.mem
        return State(pc=self.pc, regs=self.regs, mem=new_mem, addrs=self.addrs, halted=self.halted)


def fetch(pc: Ordinal, prog: Sequence[Instr]) -> Instr | None:
    """Fetch instruction by stepping purely inductively along the program list."""
    curr_pc = pc
    idx = 0
    while not curr_pc.is_zero() and idx < len(prog):
        curr_pc = curr_pc.pred()
        idx += 1
    if curr_pc.is_zero() and idx < len(prog):
        return prog[idx]
    return None


def step(prog: Sequence[Instr], s: State) -> State:
    """Single-step operational transition function."""
    if s.halted:
        return s

    instr = fetch(s.pc, prog)
    if instr is None:
        return State(pc=s.pc, regs=s.regs, mem=s.mem, addrs=s.addrs, halted=True)

    if isinstance(instr, Nop):
        return State(pc=s.pc.succ(), regs=s.regs, mem=s.mem, addrs=s.addrs, halted=False)

    if isinstance(instr, SetZero):
        return State(
            pc=s.pc.succ(),
            regs=((instr.reg, NumVal(Zero())),) + s.regs,
            mem=s.mem,
            addrs=s.addrs,
            halted=False,
        )

    if isinstance(instr, SuccReg):
        curr = s.get_reg(instr.reg)
        val: Val = NumVal(curr.val.succ()) if isinstance(curr, NumVal) else curr
        return State(
            pc=s.pc.succ(),
            regs=((instr.reg, val),) + s.regs,
            mem=s.mem,
            addrs=s.addrs,
            halted=False,
        )

    if isinstance(instr, PredReg):
        curr = s.get_reg(instr.reg)
        val = NumVal(curr.val.pred()) if isinstance(curr, NumVal) else curr
        return State(
            pc=s.pc.succ(),
            regs=((instr.reg, val),) + s.regs,
            mem=s.mem,
            addrs=s.addrs,
            halted=False,
        )

    if isinstance(instr, CopyReg):
        val = s.get_reg(instr.src)
        return State(
            pc=s.pc.succ(),
            regs=((instr.dst, val),) + s.regs,
            mem=s.mem,
            addrs=s.addrs,
            halted=False,
        )

    if isinstance(instr, AllocAddr):
        fresh = fresh_address(s.addrs)
        return State(
            pc=s.pc.succ(),
            regs=((instr.dst, AddrVal(fresh)),) + s.regs,
            mem=((fresh, NumVal(Zero())),) + s.mem,
            addrs=(fresh,) + s.addrs,
            halted=False,
        )

    if isinstance(instr, WriteMem):
        addr_val = s.get_reg(instr.addr_reg)
        if isinstance(addr_val, AddrVal):
            val = s.get_reg(instr.val_reg)
            return State(
                pc=s.pc.succ(),
                regs=s.regs,
                mem=((addr_val.addr, val),) + s.mem,
                addrs=s.addrs,
                halted=False,
            )
        # Type refusal / halt on invalid address
        return State(pc=s.pc, regs=s.regs, mem=s.mem, addrs=s.addrs, halted=True)

    if isinstance(instr, ReadMem):
        addr_val = s.get_reg(instr.addr_reg)
        if isinstance(addr_val, AddrVal):
            val = s.get_mem(addr_val.addr)
            return State(
                pc=s.pc.succ(),
                regs=((instr.dst, val),) + s.regs,
                mem=s.mem,
                addrs=s.addrs,
                halted=False,
            )
        return State(pc=s.pc, regs=s.regs, mem=s.mem, addrs=s.addrs, halted=True)

    if isinstance(instr, Jump):
        return State(pc=instr.target, regs=s.regs, mem=s.mem, addrs=s.addrs, halted=False)

    if isinstance(instr, BranchIfZero):
        curr = s.get_reg(instr.reg)
        if isinstance(curr, NumVal) and curr.val.is_zero():
            return State(pc=instr.target, regs=s.regs, mem=s.mem, addrs=s.addrs, halted=False)
        return State(pc=s.pc.succ(), regs=s.regs, mem=s.mem, addrs=s.addrs, halted=False)

    if isinstance(instr, Halt):
        return State(pc=s.pc, regs=s.regs, mem=s.mem, addrs=s.addrs, halted=True)

    return State(pc=s.pc, regs=s.regs, mem=s.mem, addrs=s.addrs, halted=True)


# --- Execution Results & Fuel-Bounded Evaluator ---


class ExecResult(ABC):
    """Result of fuel-bounded execution."""

    @property
    @abstractmethod
    def state(self) -> State:
        """The terminal or suspended state."""


@dataclass(frozen=True)
class Halted(ExecResult):
    """Machine execution successfully reached a halted state."""

    _state: State

    @property
    def state(self) -> State:
        return self._state

    def __repr__(self) -> str:
        return f"Halted(state={self._state!r})"


@dataclass(frozen=True)
class OutOfFuel(ExecResult):
    """Machine execution exhausted allocated fuel."""

    _state: State

    @property
    def state(self) -> State:
        return self._state

    def __repr__(self) -> str:
        return f"OutOfFuel(state={self._state!r})"


def run_with_fuel(fuel: Ordinal, prog: Sequence[Instr], s: State) -> ExecResult:
    """Execute program under pure structural fuel-bounded recursion."""
    if not isinstance(fuel, Ordinal):
        raise TypeError(f"fuel must be an Ordinal, got {type(fuel)}")

    curr_fuel = fuel
    curr_state = s

    while not curr_fuel.is_zero():
        if curr_state.halted:
            return Halted(curr_state)
        curr_state = step(prog, curr_state)
        curr_fuel = curr_fuel.pred()

    if curr_state.halted:
        return Halted(curr_state)
    return OutOfFuel(curr_state)


def rec_fuel(fuel: Ordinal, base: T, step_fn: Callable[[Ordinal, T], T]) -> T:
    """General endogenous structural recursion scheme on Ordinals evaluated iteratively."""
    if not isinstance(fuel, Ordinal):
        raise TypeError(f"fuel must be an Ordinal, got {type(fuel)}")
    ords: list[Ordinal] = []
    curr = fuel
    while not curr.is_zero():
        curr = curr.pred()
        ords.append(curr)
    acc = base
    for o in reversed(ords):
        acc = step_fn(o, acc)
    return acc
