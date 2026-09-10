"""Operational capability removal (BOUNDARY_REMOVAL_SEMANTICALLY_EXECUTED).

Provides distinct interpreters and syntax classes where designated capabilities
are physically absent from AST definitions and state representations, rather than
masked or filtered post-hoc.

AuthorityEffect: None.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Sequence

from capability import (
    Capability,
    CapabilityProfile,
    FULL_PROFILE,
    PublicView,
    WITHOUT_BRANCH,
    WITHOUT_MEMORY,
    WITHOUT_ALLOC,
)


class SyntaxRefusal(Exception):
    """Raised when an instruction belonging to a physically removed capability is submitted."""

    def __init__(self, capability: Capability, message: str) -> None:
        super().__init__(f"Refusal: {capability.value} primitive is physically absent: {message}")
        self.capability = capability


# ---------------------------------------------------------------------------
# Instructions
# ---------------------------------------------------------------------------


class Instruction(ABC):
    """Abstract base instruction."""

    @property
    @abstractmethod
    def required_capability(self) -> Capability | None:
        """The capability required for this instruction, or None if base primitive."""
        pass


# Base Instructions (available in all profiles)


@dataclass(frozen=True)
class Nop(Instruction):
    @property
    def required_capability(self) -> Capability | None:
        return None


@dataclass(frozen=True)
class SetConst(Instruction):
    dst: int
    val: int

    @property
    def required_capability(self) -> Capability | None:
        return None


@dataclass(frozen=True)
class Add(Instruction):
    dst: int
    src1: int
    src2: int

    @property
    def required_capability(self) -> Capability | None:
        return None


@dataclass(frozen=True)
class Inc(Instruction):
    reg: int

    @property
    def required_capability(self) -> Capability | None:
        return None


@dataclass(frozen=True)
class Emit(Instruction):
    src: int

    @property
    def required_capability(self) -> Capability | None:
        return None


@dataclass(frozen=True)
class Halt(Instruction):
    @property
    def required_capability(self) -> Capability | None:
        return None


# Branching Instructions (Capability.BRANCHING)


@dataclass(frozen=True)
class JumpIfZero(Instruction):
    cond_reg: int
    target_pc: int

    @property
    def required_capability(self) -> Capability | None:
        return Capability.BRANCHING


@dataclass(frozen=True)
class JumpIfNotZero(Instruction):
    cond_reg: int
    target_pc: int

    @property
    def required_capability(self) -> Capability | None:
        return Capability.BRANCHING


# Memory Retention Instructions (Capability.MEMORY_RETENTION)


@dataclass(frozen=True)
class StoreMem(Instruction):
    addr_reg: int
    val_reg: int

    @property
    def required_capability(self) -> Capability | None:
        return Capability.MEMORY_RETENTION


@dataclass(frozen=True)
class LoadMem(Instruction):
    dst_reg: int
    addr_reg: int

    @property
    def required_capability(self) -> Capability | None:
        return Capability.MEMORY_RETENTION


# Address Allocation Instructions (Capability.ADDRESS_ALLOCATION)


@dataclass(frozen=True)
class AllocFresh(Instruction):
    dst_reg: int

    @property
    def required_capability(self) -> Capability | None:
        return Capability.ADDRESS_ALLOCATION


# ---------------------------------------------------------------------------
# State Representations
# ---------------------------------------------------------------------------

STATIC_ADDRESS_BOUND = 4


@dataclass
class UnrestrictedState:
    """Full machine state carrying all capability substrates."""

    pc: int = 0
    regs: dict[int, int] = field(default_factory=dict)
    memory: dict[int, int] = field(default_factory=dict)
    allocated_addrs: set[int] = field(default_factory=set)
    output_tape: list[int] = field(default_factory=list)
    halted: bool = False
    steps: int = 0


@dataclass
class LinearState:
    """State for systems where branching is physically absent."""

    pc: int = 0
    regs: dict[int, int] = field(default_factory=dict)
    memory: dict[int, int] = field(default_factory=dict)
    allocated_addrs: set[int] = field(default_factory=set)
    output_tape: list[int] = field(default_factory=list)
    halted: bool = False
    steps: int = 0


@dataclass
class MemorylessState:
    """State where memory store is physically absent.

    Notice: No `memory` dictionary or auxiliary store attribute exists.
    """

    pc: int = 0
    regs: dict[int, int] = field(default_factory=dict)
    output_tape: list[int] = field(default_factory=list)
    halted: bool = False
    steps: int = 0


@dataclass
class StaticAddressState:
    """State where dynamic address allocation is physically absent.

    Notice: No `allocated_addrs` generator or dynamic heap exists;
    registers and memory locations are strictly bounded to [0, STATIC_ADDRESS_BOUND).
    """

    pc: int = 0
    regs: dict[int, int] = field(default_factory=dict)
    memory: dict[int, int] = field(default_factory=dict)
    output_tape: list[int] = field(default_factory=list)
    halted: bool = False
    steps: int = 0


# ---------------------------------------------------------------------------
# Interpreters
# ---------------------------------------------------------------------------


class BaseInterpreter(ABC):
    """Abstract interpreter defining the semantic execution contract."""

    @property
    @abstractmethod
    def profile(self) -> CapabilityProfile:
        pass

    @abstractmethod
    def validate_program(self, program: Sequence[Instruction]) -> None:
        """Statically verify that program AST contains only physically admitted instructions."""
        pass

    @abstractmethod
    def create_initial_state(self, inputs: Sequence[int]) -> Any:
        pass

    @abstractmethod
    def step(self, program: Sequence[Instruction], state: Any) -> None:
        pass

    def observe(self, state: Any, status: str, error: str | None = None) -> PublicView:
        """Shared public observation projection."""
        return PublicView(
            output_tape=tuple(state.output_tape),
            steps=state.steps,
            halted=state.halted,
            status=status,
            error=error,
        )

    def run(
        self, program: Sequence[Instruction], inputs: Sequence[int], fuel: int = 1000
    ) -> PublicView:
        """Execute program until halt, fuel exhaustion, or structural refusal."""
        try:
            self.validate_program(program)
        except SyntaxRefusal as exc:
            return PublicView(
                output_tape=(),
                steps=0,
                halted=False,
                status="SYNTAX_REFUSED",
                error=str(exc),
            )

        state = self.create_initial_state(inputs)

        while state.steps < fuel and not state.halted:
            if state.pc < 0 or state.pc >= len(program):
                state.halted = True
                break
            self.step(program, state)

        status = "HALTED" if state.halted else "FUEL_EXHAUSTED"
        return self.observe(state, status)


class UnrestrictedInterpreter(BaseInterpreter):
    """Full interpreter supporting all capabilities."""

    @property
    def profile(self) -> CapabilityProfile:
        return FULL_PROFILE

    def validate_program(self, program: Sequence[Instruction]) -> None:
        # All instructions are admitted
        pass

    def create_initial_state(self, inputs: Sequence[int]) -> UnrestrictedState:
        st = UnrestrictedState()
        for idx, val in enumerate(inputs):
            st.regs[idx] = val
        return st

    def step(self, program: Sequence[Instruction], state: UnrestrictedState) -> None:
        instr = program[state.pc]
        state.steps += 1

        if isinstance(instr, Nop):
            state.pc += 1
        elif isinstance(instr, SetConst):
            state.regs[instr.dst] = instr.val
            state.pc += 1
        elif isinstance(instr, Add):
            v1 = state.regs.get(instr.src1, 0)
            v2 = state.regs.get(instr.src2, 0)
            state.regs[instr.dst] = v1 + v2
            state.pc += 1
        elif isinstance(instr, Inc):
            state.regs[instr.reg] = state.regs.get(instr.reg, 0) + 1
            state.pc += 1
        elif isinstance(instr, Emit):
            state.output_tape.append(state.regs.get(instr.src, 0))
            state.pc += 1
        elif isinstance(instr, Halt):
            state.halted = True
        elif isinstance(instr, JumpIfZero):
            cond = state.regs.get(instr.cond_reg, 0)
            if cond == 0:
                state.pc = instr.target_pc
            else:
                state.pc += 1
        elif isinstance(instr, JumpIfNotZero):
            cond = state.regs.get(instr.cond_reg, 0)
            if cond != 0:
                state.pc = instr.target_pc
            else:
                state.pc += 1
        elif isinstance(instr, StoreMem):
            addr = state.regs.get(instr.addr_reg, 0)
            val = state.regs.get(instr.val_reg, 0)
            state.memory[addr] = val
            state.pc += 1
        elif isinstance(instr, LoadMem):
            addr = state.regs.get(instr.addr_reg, 0)
            state.regs[instr.dst_reg] = state.memory.get(addr, 0)
            state.pc += 1
        elif isinstance(instr, AllocFresh):
            # Deterministic fresh address generation
            fresh = max(state.allocated_addrs, default=0) + 1
            state.allocated_addrs.add(fresh)
            state.regs[instr.dst_reg] = fresh
            state.pc += 1
        else:
            raise RuntimeError(f"Unknown instruction: {instr}")


class LinearInterpreter(BaseInterpreter):
    """Interpreter where BRANCHING capability is physically removed.

    Semantics: Program counter strictly advances pc -> pc + 1 for all non-halting ops.
    No branching instructions exist in execution dispatch.
    """

    @property
    def profile(self) -> CapabilityProfile:
        return WITHOUT_BRANCH

    def validate_program(self, program: Sequence[Instruction]) -> None:
        for idx, instr in enumerate(program):
            if instr.required_capability == Capability.BRANCHING:
                raise SyntaxRefusal(
                    Capability.BRANCHING,
                    f"Instruction {type(instr).__name__} at index {idx} requires BRANCHING.",
                )

    def create_initial_state(self, inputs: Sequence[int]) -> LinearState:
        st = LinearState()
        for idx, val in enumerate(inputs):
            st.regs[idx] = val
        return st

    def step(self, program: Sequence[Instruction], state: LinearState) -> None:
        instr = program[state.pc]
        state.steps += 1

        # Notice: No JumpIfZero or JumpIfNotZero handlers exist.
        if isinstance(instr, Nop):
            state.pc += 1
        elif isinstance(instr, SetConst):
            state.regs[instr.dst] = instr.val
            state.pc += 1
        elif isinstance(instr, Add):
            v1 = state.regs.get(instr.src1, 0)
            v2 = state.regs.get(instr.src2, 0)
            state.regs[instr.dst] = v1 + v2
            state.pc += 1
        elif isinstance(instr, Inc):
            state.regs[instr.reg] = state.regs.get(instr.reg, 0) + 1
            state.pc += 1
        elif isinstance(instr, Emit):
            state.output_tape.append(state.regs.get(instr.src, 0))
            state.pc += 1
        elif isinstance(instr, Halt):
            state.halted = True
        elif isinstance(instr, StoreMem):
            addr = state.regs.get(instr.addr_reg, 0)
            val = state.regs.get(instr.val_reg, 0)
            state.memory[addr] = val
            state.pc += 1
        elif isinstance(instr, LoadMem):
            addr = state.regs.get(instr.addr_reg, 0)
            state.regs[instr.dst_reg] = state.memory.get(addr, 0)
            state.pc += 1
        elif isinstance(instr, AllocFresh):
            fresh = max(state.allocated_addrs, default=0) + 1
            state.allocated_addrs.add(fresh)
            state.regs[instr.dst_reg] = fresh
            state.pc += 1
        else:
            raise SyntaxRefusal(Capability.BRANCHING, f"Unauthorized instruction {instr}")


class MemorylessInterpreter(BaseInterpreter):
    """Interpreter where MEMORY_RETENTION capability is physically removed.

    Semantics: State carries NO auxiliary memory dictionary.
    No StoreMem or LoadMem dispatch exists.
    """

    @property
    def profile(self) -> CapabilityProfile:
        return WITHOUT_MEMORY

    def validate_program(self, program: Sequence[Instruction]) -> None:
        for idx, instr in enumerate(program):
            if instr.required_capability == Capability.MEMORY_RETENTION:
                raise SyntaxRefusal(
                    Capability.MEMORY_RETENTION,
                    f"Instruction {type(instr).__name__} at index {idx} requires MEMORY_RETENTION.",
                )

    def create_initial_state(self, inputs: Sequence[int]) -> MemorylessState:
        st = MemorylessState()
        for idx, val in enumerate(inputs):
            st.regs[idx] = val
        return st

    def step(self, program: Sequence[Instruction], state: MemorylessState) -> None:
        instr = program[state.pc]
        state.steps += 1

        # Notice: No StoreMem or LoadMem handlers exist.
        if isinstance(instr, Nop):
            state.pc += 1
        elif isinstance(instr, SetConst):
            state.regs[instr.dst] = instr.val
            state.pc += 1
        elif isinstance(instr, Add):
            v1 = state.regs.get(instr.src1, 0)
            v2 = state.regs.get(instr.src2, 0)
            state.regs[instr.dst] = v1 + v2
            state.pc += 1
        elif isinstance(instr, Inc):
            state.regs[instr.reg] = state.regs.get(instr.reg, 0) + 1
            state.pc += 1
        elif isinstance(instr, Emit):
            state.output_tape.append(state.regs.get(instr.src, 0))
            state.pc += 1
        elif isinstance(instr, Halt):
            state.halted = True
        elif isinstance(instr, JumpIfZero):
            cond = state.regs.get(instr.cond_reg, 0)
            state.pc = instr.target_pc if cond == 0 else state.pc + 1
        elif isinstance(instr, JumpIfNotZero):
            cond = state.regs.get(instr.cond_reg, 0)
            state.pc = instr.target_pc if cond != 0 else state.pc + 1
        else:
            raise SyntaxRefusal(Capability.MEMORY_RETENTION, f"Unauthorized instruction {instr}")


class StaticAddressInterpreter(BaseInterpreter):
    """Interpreter where ADDRESS_ALLOCATION capability is physically removed.

    Semantics: Register and memory address space is strictly bounded to [0, STATIC_ADDRESS_BOUND).
    No AllocFresh instruction or dynamic address generator exists.
    """

    @property
    def profile(self) -> CapabilityProfile:
        return WITHOUT_ALLOC

    def validate_program(self, program: Sequence[Instruction]) -> None:
        for idx, instr in enumerate(program):
            if instr.required_capability == Capability.ADDRESS_ALLOCATION:
                raise SyntaxRefusal(
                    Capability.ADDRESS_ALLOCATION,
                    f"Instruction {type(instr).__name__} at index {idx} requires ADDRESS_ALLOCATION.",
                )

    def create_initial_state(self, inputs: Sequence[int]) -> StaticAddressState:
        st = StaticAddressState()
        for idx, val in enumerate(inputs):
            if idx < STATIC_ADDRESS_BOUND:
                st.regs[idx] = val
        return st

    def step(self, program: Sequence[Instruction], state: StaticAddressState) -> None:
        instr = program[state.pc]
        state.steps += 1

        # Notice: No AllocFresh handler exists.
        if isinstance(instr, Nop):
            state.pc += 1
        elif isinstance(instr, SetConst):
            if 0 <= instr.dst < STATIC_ADDRESS_BOUND:
                state.regs[instr.dst] = instr.val
            state.pc += 1
        elif isinstance(instr, Add):
            v1 = state.regs.get(instr.src1, 0)
            v2 = state.regs.get(instr.src2, 0)
            if 0 <= instr.dst < STATIC_ADDRESS_BOUND:
                state.regs[instr.dst] = v1 + v2
            state.pc += 1
        elif isinstance(instr, Inc):
            if 0 <= instr.reg < STATIC_ADDRESS_BOUND:
                state.regs[instr.reg] = state.regs.get(instr.reg, 0) + 1
            state.pc += 1
        elif isinstance(instr, Emit):
            state.output_tape.append(state.regs.get(instr.src, 0))
            state.pc += 1
        elif isinstance(instr, Halt):
            state.halted = True
        elif isinstance(instr, JumpIfZero):
            cond = state.regs.get(instr.cond_reg, 0)
            state.pc = instr.target_pc if cond == 0 else state.pc + 1
        elif isinstance(instr, JumpIfNotZero):
            cond = state.regs.get(instr.cond_reg, 0)
            state.pc = instr.target_pc if cond != 0 else state.pc + 1
        elif isinstance(instr, StoreMem):
            addr = state.regs.get(instr.addr_reg, 0)
            val = state.regs.get(instr.val_reg, 0)
            # Static bounded memory
            if 0 <= addr < STATIC_ADDRESS_BOUND:
                state.memory[addr] = val
            state.pc += 1
        elif isinstance(instr, LoadMem):
            addr = state.regs.get(instr.addr_reg, 0)
            if 0 <= instr.dst_reg < STATIC_ADDRESS_BOUND:
                state.regs[instr.dst_reg] = state.memory.get(addr, 0)
            state.pc += 1
        else:
            raise SyntaxRefusal(Capability.ADDRESS_ALLOCATION, f"Unauthorized instruction {instr}")


def create_interpreter(profile: CapabilityProfile) -> BaseInterpreter:
    """Factory returning the appropriate interpreter for a declared capability profile."""
    if profile == FULL_PROFILE:
        return UnrestrictedInterpreter()
    elif not profile.has_branching and profile.has_memory and profile.has_alloc:
        return LinearInterpreter()
    elif profile.has_branching and not profile.has_memory and profile.has_alloc:
        return MemorylessInterpreter()
    elif profile.has_branching and profile.has_memory and not profile.has_alloc:
        return StaticAddressInterpreter()
    else:
        # Generic minimal interpreter for other restricted configurations
        return LinearInterpreter()
