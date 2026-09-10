"""Comparative execution engine running unrestricted vs restricted systems side-by-side.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Sequence

from capability import (
    Capability,
    CapabilityProfile,
    FULL_PROFILE,
    PublicView,
    Task,
    WITHOUT_BRANCH,
    WITHOUT_MEMORY,
    WITHOUT_ALLOC,
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
    UnrestrictedInterpreter,
    LinearInterpreter,
    MemorylessInterpreter,
    StaticAddressInterpreter,
    create_interpreter,
)
from obstruction import (
    make_linear_arithmetic_task,
    make_conditional_routing_task,
    make_persistent_retention_task,
    make_dynamic_allocation_task,
    ObstructionWitness,
)


@dataclass(frozen=True)
class ComparisonResult:
    """Structured record of side-by-side comparative execution."""

    task_name: str
    target_capability: str | None
    unrestricted_views: tuple[PublicView, ...]
    restricted_views: tuple[PublicView, ...]
    unrestricted_passed: bool
    restricted_passed: bool
    status: str  # "MATCHING_PASS", "OBSTRUCTED_AS_EXPECTED", "REGRESSION"
    obstruction_witness: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_name": self.task_name,
            "target_capability": self.target_capability,
            "unrestricted_passed": self.unrestricted_passed,
            "restricted_passed": self.restricted_passed,
            "status": self.status,
            "obstruction_witness": self.obstruction_witness,
            "unrestricted_views": [
                {
                    "output_tape": list(v.output_tape),
                    "steps": v.steps,
                    "halted": v.halted,
                    "status": v.status,
                }
                for v in self.unrestricted_views
            ],
            "restricted_views": [
                {
                    "output_tape": list(v.output_tape),
                    "steps": v.steps,
                    "halted": v.halted,
                    "status": v.status,
                }
                for v in self.restricted_views
            ],
        }


class ComparativeRunner:
    """Executes identical probe tasks across unrestricted and restricted interpreters."""

    def __init__(self) -> None:
        self.unrestricted_interp = UnrestrictedInterpreter()

    def run_comparison(
        self,
        task: Task,
        unrestricted_prog: Sequence[Instruction],
        restricted_prog: Sequence[Instruction],
        restricted_interp: BaseInterpreter,
    ) -> ComparisonResult:
        """Run a single task comparatively between unrestricted and restricted systems."""
        u_views = tuple(
            self.unrestricted_interp.run(unrestricted_prog, inp)
            for inp in task.test_inputs
        )
        r_views = tuple(
            restricted_interp.run(restricted_prog, inp) for inp in task.test_inputs
        )

        u_pass = task.validator(u_views)
        r_pass = task.validator(r_views)

        target_cap = (
            ", ".join(c.value for c in task.required_capabilities)
            if task.required_capabilities
            else None
        )

        witness: str | None = None
        if u_pass and r_pass:
            status = "MATCHING_PASS"
        elif u_pass and not r_pass:
            status = "OBSTRUCTED_AS_EXPECTED"
            witness = task.obstruction_witness(r_views)
        else:
            status = "REGRESSION"
            witness = f"Unexpected execution result: u_pass={u_pass}, r_pass={r_pass}"

        return ComparisonResult(
            task_name=task.name,
            target_capability=target_cap,
            unrestricted_views=u_views,
            restricted_views=r_views,
            unrestricted_passed=u_pass,
            restricted_passed=r_pass,
            status=status,
            obstruction_witness=witness,
        )

    def run_standard_battery(self) -> list[ComparisonResult]:
        """Run standard battery covering baseline and all three capability removals."""
        results: list[ComparisonResult] = []

        # 1. Baseline: Linear Arithmetic
        baseline_task = make_linear_arithmetic_task()
        baseline_prog = [
            Add(dst=2, src1=0, src2=1),
            Inc(reg=2),
            Emit(src=2),
            Halt(),
        ]
        results.append(
            self.run_comparison(
                task=baseline_task,
                unrestricted_prog=baseline_prog,
                restricted_prog=baseline_prog,
                restricted_interp=LinearInterpreter(),
            )
        )

        # 2. Branching Removal: Conditional Routing
        branch_task = make_conditional_routing_task()
        u_branch_prog = [
            JumpIfZero(cond_reg=0, target_pc=6),
            SetConst(dst=1, val=20),
            Emit(src=1),
            SetConst(dst=1, val=30),
            Emit(src=1),
            Halt(),
            SetConst(dst=1, val=10),
            Emit(src=1),
            Halt(),
        ]
        # Restricted linear program attempts to approximate but cannot branch
        r_linear_prog = [
            SetConst(dst=1, val=10),
            Emit(src=1),
            Halt(),
        ]
        results.append(
            self.run_comparison(
                task=branch_task,
                unrestricted_prog=u_branch_prog,
                restricted_prog=r_linear_prog,
                restricted_interp=LinearInterpreter(),
            )
        )

        # 3. Memory Removal: Persistent Retention
        mem_task = make_persistent_retention_task()
        u_mem_prog = [
            SetConst(dst=1, val=100),
            StoreMem(addr_reg=1, val_reg=0),
            SetConst(dst=0, val=0),
            SetConst(dst=1, val=0),
            SetConst(dst=1, val=100),
            LoadMem(dst_reg=0, addr_reg=1),
            Emit(src=0),
            Halt(),
        ]
        r_mem_prog = [
            SetConst(dst=0, val=0),
            SetConst(dst=1, val=0),
            Emit(src=0),
            Halt(),
        ]
        results.append(
            self.run_comparison(
                task=mem_task,
                unrestricted_prog=u_mem_prog,
                restricted_prog=r_mem_prog,
                restricted_interp=MemorylessInterpreter(),
            )
        )

        # 4. Allocation Removal: Dynamic Allocation
        alloc_task = make_dynamic_allocation_task()
        u_alloc_prog = [
            AllocFresh(dst_reg=0),
            Emit(src=0),
            AllocFresh(dst_reg=0),
            Emit(src=0),
            AllocFresh(dst_reg=0),
            Emit(src=0),
            AllocFresh(dst_reg=0),
            Emit(src=0),
            AllocFresh(dst_reg=0),
            Emit(src=0),
            Halt(),
        ]
        r_alloc_prog = [
            SetConst(dst=0, val=0),
            Emit(src=0),
            SetConst(dst=1, val=1),
            Emit(src=1),
            SetConst(dst=2, val=2),
            Emit(src=2),
            SetConst(dst=3, val=3),
            Emit(src=3),
            Emit(src=0),  # Collides by necessity
            Halt(),
        ]
        results.append(
            self.run_comparison(
                task=alloc_task,
                unrestricted_prog=u_alloc_prog,
                restricted_prog=r_alloc_prog,
                restricted_interp=StaticAddressInterpreter(),
            )
        )

        return results
