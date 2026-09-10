"""Unit tests for constructive obstruction proofs and non-recoverability."""

from obstruction import (
    BranchingObstruction,
    MemoryObstruction,
    AllocationObstruction,
    LinearAdapter,
    verify_adapter_cannot_bypass_branching,
    make_conditional_routing_task,
    make_persistent_retention_task,
    make_dynamic_allocation_task,
)
from restriction import (
    LinearInterpreter,
    MemorylessInterpreter,
    StaticAddressInterpreter,
    SetConst,
    Emit,
    Halt,
    Add,
    Inc,
    JumpIfZero,
    JumpIfNotZero,
    STATIC_ADDRESS_BOUND,
)


def test_branching_obstruction_length_invariance() -> None:
    interp = LinearInterpreter()
    # Any straight-line program emits invariant tape length
    prog = [
        SetConst(dst=1, val=10),
        Emit(src=1),
        Halt(),
    ]
    ok, msg = BranchingObstruction.verify_length_invariance(interp, prog, (0,), (1,))
    assert ok
    assert "invariant" in msg


def test_linear_adapter_cannot_bypass_branching_task() -> None:
    task = make_conditional_routing_task()
    interp = LinearInterpreter()
    prog = [
        SetConst(dst=1, val=10),
        Emit(src=1),
        Halt(),
    ]
    # An adapter that is linear / length-preserving
    adapter = LinearAdapter(
        input_transform=lambda inps: inps,
        output_transform=lambda view: view,
    )
    failed = verify_adapter_cannot_bypass_branching(adapter, interp, prog, task)
    assert failed


def test_memory_obstruction_state_collapse() -> None:
    interp = MemorylessInterpreter()
    # Program clobbers all registers to 0
    prog = [
        SetConst(dst=0, val=0),
        SetConst(dst=1, val=0),
        SetConst(dst=2, val=0),
        SetConst(dst=3, val=0),
        Emit(src=0),
        Halt(),
    ]
    ok, msg = MemoryObstruction.verify_state_collapse(interp, prog, (42,), (99,))
    assert ok
    assert "State collapse certified" in msg


def test_allocation_obstruction_pigeonhole() -> None:
    interp = StaticAddressInterpreter()
    # Program attempts to emit 5 distinct addresses
    prog = [
        SetConst(dst=0, val=0),
        Emit(src=0),
        SetConst(dst=1, val=1),
        Emit(src=1),
        SetConst(dst=2, val=2),
        Emit(src=2),
        SetConst(dst=3, val=3),
        Emit(src=3),
        Emit(src=0),  # Collides
        Halt(),
    ]
    ok, msg = AllocationObstruction.verify_pigeonhole_collision(
        interp, prog, (), required_entities=5
    )
    assert ok
    assert "Pigeonhole collision certified" in msg
