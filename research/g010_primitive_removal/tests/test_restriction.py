"""Unit tests for operational capability removal and distinct interpreters."""

import pytest

from capability import Capability
from restriction import (
    Instruction,
    Nop,
    SetConst,
    Add,
    Inc,
    Emit,
    Halt,
    JumpIfZero,
    JumpIfNotZero,
    StoreMem,
    LoadMem,
    AllocFresh,
    SyntaxRefusal,
    UnrestrictedInterpreter,
    LinearInterpreter,
    MemorylessInterpreter,
    StaticAddressInterpreter,
    MemorylessState,
    StaticAddressState,
    STATIC_ADDRESS_BOUND,
)


def test_base_instructions_admitted_in_all_interpreters() -> None:
    prog = [
        SetConst(dst=0, val=5),
        Inc(reg=0),
        Emit(src=0),
        Halt(),
    ]
    interps = [
        UnrestrictedInterpreter(),
        LinearInterpreter(),
        MemorylessInterpreter(),
        StaticAddressInterpreter(),
    ]
    for interp in interps:
        view = interp.run(prog, ())
        assert view.status == "HALTED"
        assert view.output_tape == (6,)


def test_linear_interpreter_refuses_branching_instructions() -> None:
    interp = LinearInterpreter()
    prog_jump = [JumpIfZero(cond_reg=0, target_pc=2), Halt()]

    with pytest.raises(SyntaxRefusal) as excinfo:
        interp.validate_program(prog_jump)
    assert excinfo.value.capability == Capability.BRANCHING

    # Run should return SYNTAX_REFUSED view
    view = interp.run(prog_jump, ())
    assert view.status == "SYNTAX_REFUSED"
    assert "BRANCHING" in (view.error or "")


def test_linear_interpreter_strictly_increments_pc() -> None:
    interp = LinearInterpreter()
    prog = [
        SetConst(dst=0, val=1),
        SetConst(dst=1, val=2),
        Add(dst=2, src1=0, src2=1),
        Emit(src=2),
        Halt(),
    ]
    st = interp.create_initial_state(())
    for expected_pc in range(4):
        assert st.pc == expected_pc
        interp.step(prog, st)
    assert st.pc == 4
    assert not st.halted
    interp.step(prog, st)
    assert st.halted


def test_memoryless_interpreter_refuses_memory_instructions() -> None:
    interp = MemorylessInterpreter()
    prog_store = [StoreMem(addr_reg=0, val_reg=1), Halt()]
    prog_load = [LoadMem(dst_reg=0, addr_reg=1), Halt()]

    for p in [prog_store, prog_load]:
        with pytest.raises(SyntaxRefusal) as excinfo:
            interp.validate_program(p)
        assert excinfo.value.capability == Capability.MEMORY_RETENTION

        view = interp.run(p, ())
        assert view.status == "SYNTAX_REFUSED"


def test_memoryless_state_has_no_memory_attribute() -> None:
    st = MemorylessState()
    assert not hasattr(st, "memory")


def test_static_address_interpreter_refuses_alloc_instructions() -> None:
    interp = StaticAddressInterpreter()
    prog_alloc = [AllocFresh(dst_reg=0), Halt()]

    with pytest.raises(SyntaxRefusal) as excinfo:
        interp.validate_program(prog_alloc)
    assert excinfo.value.capability == Capability.ADDRESS_ALLOCATION

    view = interp.run(prog_alloc, ())
    assert view.status == "SYNTAX_REFUSED"


def test_static_address_state_has_no_alloc_attribute() -> None:
    st = StaticAddressState()
    assert not hasattr(st, "allocated_addrs")


def test_static_address_bound_enforced() -> None:
    interp = StaticAddressInterpreter()
    # Attempting to write outside STATIC_ADDRESS_BOUND is ignored
    prog = [
        SetConst(dst=STATIC_ADDRESS_BOUND + 1, val=999),
        SetConst(dst=0, val=42),
        Emit(src=0),
        Halt(),
    ]
    view = interp.run(prog, ())
    assert view.status == "HALTED"
    assert view.output_tape == (42,)
