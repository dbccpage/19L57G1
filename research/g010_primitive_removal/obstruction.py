"""Constructive obstruction proofs and operational demonstrations for G010.

Demonstrates that tasks requiring a removed primitive are strictly unsolvable across
the shared PublicView interface, and cannot be recovered via capability-preserving adapters.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

from capability import (
    Capability,
    PublicView,
    Task,
)
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
    BaseInterpreter,
    LinearInterpreter,
    MemorylessInterpreter,
    StaticAddressInterpreter,
    STATIC_ADDRESS_BOUND,
)


# ---------------------------------------------------------------------------
# Constructive Obstruction Witnesses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ObstructionWitness:
    """Mathematical and operational certificate that a task is obstructed."""

    task_name: str
    missing_capability: Capability
    obstruction_type: str
    formal_proof_summary: str
    empirical_observation: str


class BranchingObstruction:
    """Constructive obstruction for systems lacking Capability.BRANCHING."""

    @staticmethod
    def verify_length_invariance(
        interpreter: LinearInterpreter,
        program: Sequence[Instruction],
        inputs1: Sequence[int],
        inputs2: Sequence[int],
    ) -> tuple[bool, str]:
        """Shows in this model that a straight-line program emits an invariant tape length.

        In the absence of branching, every non-halting step increments pc by 1.
        The sequence of instructions traversed is identical regardless of input values.
        """
        view1 = interpreter.run(program, inputs1)
        view2 = interpreter.run(program, inputs2)

        len1 = len(view1.output_tape)
        len2 = len(view2.output_tape)

        if len1 == len2:
            return (
                True,
                f"Straight-line trace length is invariant: len(out({inputs1})) = {len1} == len(out({inputs2})) = {len2}",
            )
        return (False, f"Unexpected length variation: {len1} != {len2}")


class MemoryObstruction:
    """Constructive obstruction for systems lacking Capability.MEMORY_RETENTION."""

    @staticmethod
    def verify_state_collapse(
        interpreter: MemorylessInterpreter,
        program: Sequence[Instruction],
        inputs1: Sequence[int],
        inputs2: Sequence[int],
    ) -> tuple[bool, str]:
        """Shows in this model that overwriting registers in a memoryless system erases prior state.

        When memory retention is absent, the state has zero auxiliary storage.
        Once all registers are overwritten, initial inputs are completely erased.
        """
        view1 = interpreter.run(program, inputs1)
        view2 = interpreter.run(program, inputs2)

        if view1.output_tape == view2.output_tape and inputs1 != inputs2:
            return (
                True,
                f"State collapse certified: inputs {inputs1} and {inputs2} yield identical outputs {view1.output_tape}",
            )
        return (False, "State collapse not demonstrated")


class AllocationObstruction:
    """Constructive obstruction for systems lacking Capability.ADDRESS_ALLOCATION."""

    @staticmethod
    def verify_pigeonhole_collision(
        interpreter: StaticAddressInterpreter,
        program: Sequence[Instruction],
        inputs: Sequence[int],
        required_entities: int,
    ) -> tuple[bool, str]:
        """Shows in this model that allocating > STATIC_ADDRESS_BOUND entities causes collision.

        By finite slot collision (pigeonhole), mapping required_entities > bound
        into static addresses forces at least one duplicate.
        """
        view = interpreter.run(program, inputs)
        unique_addrs = set(view.output_tape)

        if len(unique_addrs) <= STATIC_ADDRESS_BOUND < required_entities:
            return (
                True,
                f"Pigeonhole collision certified: requested {required_entities} distinct addresses, "
                f"but static system produced at most {len(unique_addrs)} unique values (bound={STATIC_ADDRESS_BOUND})",
            )
        return (False, "Pigeonhole collision not certified")


# ---------------------------------------------------------------------------
# Pre-Registered Adequacy Probe Tasks
# ---------------------------------------------------------------------------


def make_conditional_routing_task() -> Task:
    """Task requiring Capability.BRANCHING.

    On input 0: emit tape [10] (length 1).
    On input 1: emit tape [20, 30] (length 2).
    """

    def validator(views: tuple[PublicView, ...]) -> bool:
        if len(views) != 2:
            return False
        v0, v1 = views[0], views[1]
        return v0.output_tape == (10,) and v1.output_tape == (20, 30)

    def witness(views: tuple[PublicView, ...]) -> str:
        if len(views) < 2:
            return "Insufficient views"
        l0, l1 = len(views[0].output_tape), len(views[1].output_tape)
        return (
            f"BRANCHING_OBSTRUCTION: Input 0 yielded tape length {l0}, input 1 yielded tape length {l1}. "
            f"A straight-line linear program has a fixed execution path with invariant tape length."
        )

    return Task(
        name="CONDITIONAL_ROUTING_TASK",
        description="Emit length 1 on input 0 and length 2 on input 1",
        required_capabilities=frozenset({Capability.BRANCHING}),
        test_inputs=((0,), (1,)),
        validator=validator,
        obstruction_witness=witness,
    )


def make_persistent_retention_task() -> Task:
    """Task requiring Capability.MEMORY_RETENTION.

    Store input x, run a register-clobber sequence zeroing all registers,
    and then emit x.
    """

    def validator(views: tuple[PublicView, ...]) -> bool:
        if len(views) != 2:
            return False
        v1, v2 = views[0], views[1]
        return v1.output_tape == (42,) and v2.output_tape == (99,)

    def witness(views: tuple[PublicView, ...]) -> str:
        if len(views) < 2:
            return "Insufficient views"
        t1, t2 = views[0].output_tape, views[1].output_tape
        return (
            f"MEMORY_OBSTRUCTION: Overwriting registers in a memoryless system erased distinction: "
            f"tape(42)={t1} == tape(99)={t2}. Information capacity bound was exceeded."
        )

    return Task(
        name="PERSISTENT_RETENTION_TASK",
        description="Preserve input value across a destructive register-clobber sequence",
        required_capabilities=frozenset({Capability.MEMORY_RETENTION}),
        test_inputs=((42,), (99,)),
        validator=validator,
        obstruction_witness=witness,
    )


def make_dynamic_allocation_task() -> Task:
    """Task requiring Capability.ADDRESS_ALLOCATION.

    Allocate 5 distinct active entities and emit their addresses.
    """

    def validator(views: tuple[PublicView, ...]) -> bool:
        if not views:
            return False
        v = views[0]
        return len(v.output_tape) == 5 and len(set(v.output_tape)) == 5

    def witness(views: tuple[PublicView, ...]) -> str:
        if not views:
            return "No views"
        tape = views[0].output_tape
        return (
            f"ALLOCATION_OBSTRUCTION: Output tape {tape} contains only {len(set(tape))} unique addresses. "
            f"By finite slot collision, 5 entities cannot be uniquely allocated in {STATIC_ADDRESS_BOUND} static slots."
        )

    return Task(
        name="DYNAMIC_ALLOCATION_TASK",
        description="Allocate 5 pairwise distinct dynamic addresses",
        required_capabilities=frozenset({Capability.ADDRESS_ALLOCATION}),
        test_inputs=((),),
        validator=validator,
        obstruction_witness=witness,
    )


# Capability-Neutral Baseline Task
def make_linear_arithmetic_task() -> Task:
    """Baseline task requiring NO specialized capabilities.

    Computes (x + y) + 1 and emits the result.
    """

    def validator(views: tuple[PublicView, ...]) -> bool:
        if len(views) != 2:
            return False
        return views[0].output_tape == (6,) and views[1].output_tape == (11,)

    def witness(views: tuple[PublicView, ...]) -> str:
        return "BASELINE_PASS: Capability-neutral task succeeded."

    return Task(
        name="LINEAR_ARITHMETIC_TASK",
        description="Compute (x + y) + 1 linearly",
        required_capabilities=frozenset(),
        test_inputs=((2, 3), (4, 6)),
        validator=validator,
        obstruction_witness=witness,
    )


# ---------------------------------------------------------------------------
# Hidden Adapter Non-Recoverability
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LinearAdapter:
    """A capability-preserving public-view adapter.

    Cannot implement branching or conditional branching.
    """

    input_transform: Callable[[Sequence[int]], tuple[int, ...]]
    output_transform: Callable[[PublicView], PublicView]

    def wrap_run(
        self,
        interpreter: BaseInterpreter,
        program: Sequence[Instruction],
        inputs: Sequence[int],
    ) -> PublicView:
        adapted_inputs = self.input_transform(inputs)
        view = interpreter.run(program, adapted_inputs)
        return self.output_transform(view)


def verify_adapter_cannot_bypass_branching(
    adapter: LinearAdapter,
    interpreter: LinearInterpreter,
    program: Sequence[Instruction],
    task: Task,
) -> bool:
    """Verifies that a linear adapter cannot bypass the branching obstruction.

    If the linear program produces identical tape lengths, a length-preserving
    adapter cannot generate differing tape lengths required by the task.
    """
    view0 = adapter.wrap_run(interpreter, program, task.test_inputs[0])
    view1 = adapter.wrap_run(interpreter, program, task.test_inputs[1])
    return not task.validator((view0, view1))
