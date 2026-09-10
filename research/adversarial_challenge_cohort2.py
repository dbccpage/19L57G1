"""Empirical Adversarial Stress Suite for Genesis Cohort 2.

AuthorityEffect: None.
Configuration status: DECLARED_HOST_CONFIG.

Challenges:
1. Target A: Non-deterministic fork non-selection, ambiguous graph detection,
   extreme/malformed regimes, fuel exhaustion boundaries.
2. Target B: Quantitative rational frequency bounds L <= 3*zeros(L) <= L+2 across 100+
   random cycle lengths L in [1, 500], rational error budget in Q, and chain functionality
   asserting that non-functional prefix combinations like [0, 1, 0, 2] are unproduceable.
3. G010: Operational capability removal verification, adversarial smuggling attempts
   bypassing AST checks, empirical demonstration of straight-line length invariance, state collapse
   under register clobbering, and adapter non-recoverability.
"""

from __future__ import annotations

from fractions import Fraction
import random
import sys
from pathlib import Path

# Add dependencies to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.extend([
    str(REPO_ROOT / "code"),
    str(REPO_ROOT / "research" / "target_a_execution"),
    str(REPO_ROOT / "research" / "target_b_dynamics"),
    str(REPO_ROOT / "research" / "g010_primitive_removal"),
])

from runner import (
    Config,
    ExecutionError,
    Refusal,
    Terminal,
    check_word,
    lookup,
    run_det_of,
    step_det_of,
)
from control import (
    Controlled,
    State,
    build_program,
    ctrl_reader,
    enabled,
    enabled_at,
    fire,
    init,
    nops,
    run,
    run_det,
    step_det,
    successors,
)
from branch import (
    CFGBuilder,
    CFGState,
    FORM_CFG_BRANCH,
    FORM_CFG_INDIRECT,
    FORM_CFG_STEP,
    FORM_JUMP_TABLE,
    get_cfg_successors,
    init_cfg,
    resolve_jump_table_target,
    run_cfg,
    step_cfg,
)
from bounds import (
    TWIST_TAPE,
    is_chain,
    is_functional,
    pairs_of,
    precision_budget,
    rational_frequency,
    rational_frequency_error,
    run_cycle_program,
    verify_rational_error_bound,
    verify_zeros_bounds,
    zeros,
    zeros_closed_form,
)
from memory import (
    TWIST_TAPE as MEM_TWIST_TAPE,
    TWIST2_TAPE as MEM_TWIST2_TAPE,
    functional,
    windows,
)
from capability import (
    FULL_PROFILE,
    WITHOUT_ALLOC,
    WITHOUT_BRANCH,
    WITHOUT_MEMORY,
    Capability,
    CapabilityProfile,
    PublicView,
    Task,
)
from restriction import (
    STATIC_ADDRESS_BOUND,
    Add,
    AllocFresh,
    BaseInterpreter,
    Emit,
    Halt,
    Inc,
    Instruction,
    JumpIfNotZero,
    JumpIfZero,
    LinearInterpreter,
    LinearState,
    LoadMem,
    MemorylessInterpreter,
    MemorylessState,
    Nop,
    SetConst,
    StaticAddressInterpreter,
    StaticAddressState,
    StoreMem,
    SyntaxRefusal,
    UnrestrictedInterpreter,
    create_interpreter,
)
from obstruction import (
    AllocationObstruction,
    BranchingObstruction,
    LinearAdapter,
    MemoryObstruction,
    make_conditional_routing_task,
    make_dynamic_allocation_task,
    make_linear_arithmetic_task,
    make_persistent_retention_task,
    verify_adapter_cannot_bypass_branching,
)


# ===========================================================================
# 1. Target A Adversarial Challenges
# ===========================================================================

def test_target_a_fork_refusal_exhaustive() -> None:
    """Challenge 1.1: Verify the runner NEVER silently selects on non-deterministic forks.

    Tests k-way branch enablements (k in 2..20) and ambiguous CFG branches.
    """
    print("  [Target A] Testing fork refusal across k-way ambiguous enablements...")

    # Case A: Control-based enablement forks with k enabled operations
    for k_enabled in range(2, 21):
        # Create setting with k_enabled operations on carrier 2
        # Op 0: 0 -> 1, Op 1: 0 -> 0, Op 2: 0 -> 1, etc.
        ops = tuple(tuple((i + op_idx) % 2 for i in range(2)) for op_idx in range(k_enabled))
        ctrl = tuple((0, op_idx) for op_idx in range(k_enabled))
        C = Controlled(n=2, ops=ops, ctrl=ctrl)
        st = init(C, x=0, fuel=10)

        # Confirm all k operations are enabled
        en = enabled_at(st.graph, st.nops, st.active)
        assert len(en) == k_enabled, f"Expected {k_enabled} enabled ops, got {len(en)}"

        # Deterministic step MUST refuse selection and return Terminal.BRANCH
        result = step_det(st)
        assert result is Terminal.BRANCH, (
            f"Runner silently selected or failed on {k_enabled}-fork: got {result}"
        )

        # Full run MUST halt immediately with Terminal.BRANCH and state unchanged
        term, final_st = run(st)
        assert term is Terminal.BRANCH, f"Run returned {term} instead of Terminal.BRANCH"
        assert final_st.clock == 0, f"Clock advanced on fork: {final_st.clock}"
        assert final_st.fuel == 10, f"Fuel consumed on fork: {final_st.fuel}"
        assert final_st.tape == (0,), f"Tape modified on fork: {final_st.tape}"

    # Case B: Fork where all operations lead to the IDENTICAL target state
    # Op 0: 0 -> 1, Op 1: 0 -> 1. Even though targets coincide, it is a non-deterministic choice!
    ops_identical = ((1, 0), (1, 0))
    ctrl_identical = ((0, 0), (0, 1))
    C_id = Controlled(n=2, ops=ops_identical, ctrl=ctrl_identical)
    st_id = init(C_id, x=0, fuel=10)
    res_id = step_det(st_id)
    assert res_id is Terminal.BRANCH, (
        f"Runner falsely collapsed identical-target fork: got {res_id}"
    )

    # Case C: CFG non-deterministic forks
    # 1. Two conditional branches matching identical condition
    b1 = CFGBuilder()
    b1.add_branch(pc=0, cond_val=5, target_pc=10)
    b1.add_branch(pc=0, cond_val=5, target_pc=20)
    g1 = b1.to_graph()
    cfg_st1 = init_cfg(g1, start_pc=0, initial_data=5, fuel=10)
    res_cfg1 = step_cfg(cfg_st1)
    assert res_cfg1 is Terminal.BRANCH, (
        f"CFG runner failed to return BRANCH on ambiguous conditional: {res_cfg1}"
    )

    # 2. Unconditional step + matching conditional branch at same PC
    b2 = CFGBuilder()
    b2.add_step(src_pc=0, next_pc=10)
    b2.add_branch(pc=0, cond_val=5, target_pc=20)
    g2 = b2.to_graph()
    cfg_st2 = init_cfg(g2, start_pc=0, initial_data=5, fuel=10)
    res_cfg2 = step_cfg(cfg_st2)
    assert res_cfg2 is Terminal.BRANCH, (
        f"CFG runner failed to return BRANCH on step + branch ambiguity: {res_cfg2}"
    )

    # 3. Unconditional step + indirect jump table at same PC
    b3 = CFGBuilder()
    b3.add_step(src_pc=0, next_pc=10)
    b3.add_jump_table(table_id=1, targets=[30, 40])
    b3.add_indirect_jump(pc=0, table_id=1)
    g3 = b3.to_graph()
    cfg_st3 = init_cfg(g3, start_pc=0, initial_data=1, fuel=10)
    res_cfg3 = step_cfg(cfg_st3)
    assert res_cfg3 is Terminal.BRANCH, (
        f"CFG runner failed to return BRANCH on step + indirect jump: {res_cfg3}"
    )


def test_target_a_ambiguous_graph_refusal() -> None:
    """Challenge 1.2: Verify graph-edge level ambiguity is strictly detected and refused."""
    print("  [Target A] Testing ambiguous graph edge detection...")

    # Two distinct outgoing edges on same operation form leaving datum 0
    ambiguous_graph = frozenset([
        (3, (0, 1)),
        (3, (0, 2)),
    ])
    try:
        lookup(3, 0, ambiguous_graph)
        assert False, "Lookup silently selected between conflicting outgoing edges"
    except ExecutionError as exc:
        assert "ambiguous graph" in str(exc), f"Unexpected error message: {exc}"

    # Jump table with ambiguous targets for same (table_id, index)
    ambiguous_table = frozenset([
        (FORM_JUMP_TABLE, (1, 0, 10)),
        (FORM_JUMP_TABLE, (1, 0, 20)),
    ])
    try:
        resolve_jump_table_target(ambiguous_table, 1, 0)
        assert False, "Jump table lookup silently selected between conflicting entries"
    except ExecutionError as exc:
        assert "ambiguous" in str(exc), f"Unexpected jump table error: {exc}"


def test_target_a_extreme_and_fuel_boundaries() -> None:
    """Challenge 1.3: Test extreme regimes, fuel=0/1 boundaries, and malformed inputs."""
    print("  [Target A] Testing extreme regimes and fuel boundaries...")

    # Subtest 1: Fuel = 0 boundary in Control runner
    # Program with single deterministic operation 0 -> 1
    ops = ((1, 0),)
    ctrl = ((0, 0),)
    C = Controlled(n=2, ops=ops, ctrl=ctrl)

    st_f0 = init(C, x=0, fuel=0)
    step_res = step_det(st_f0)
    assert step_res is Terminal.EXHAUSTED, f"step_det at fuel 0 returned {step_res}"
    term, final_st = run(st_f0)
    assert term is Terminal.EXHAUSTED, f"run at fuel 0 returned {term}"
    assert final_st.clock == 0
    assert final_st.fuel == 0
    assert final_st.tape == (0,)

    # Subtest 2: Fuel = 1 boundary in Control runner (exact 1 step)
    # 2a. With cycle enablement (op enabled at both 0 and 1): step 1 fires, step 2 returns EXHAUSTED
    ops_cyc = ((1, 0),)
    ctrl_cyc = ((0, 0), (1, 0))
    C_cyc = Controlled(n=2, ops=ops_cyc, ctrl=ctrl_cyc)
    st_f1 = init(C_cyc, x=0, fuel=1)
    step_res1 = step_det(st_f1)
    assert isinstance(step_res1, State), f"step_det at fuel 1 failed to take step: {step_res1}"
    assert step_res1.active == 1
    assert step_res1.clock == 1
    assert step_res1.fuel == 0
    assert step_res1.tape == (0, 1)

    # From this new state (fuel 0 with op enabled), next step must be EXHAUSTED
    step_res2 = step_det(step_res1)
    assert step_res2 is Terminal.EXHAUSTED, f"Expected EXHAUSTED on fuel 0 with enabled op, got {step_res2}"

    # 2b. Priority ordering: if no op enabled, HALT takes precedence over EXHAUSTED
    st_no_op = init(C, x=0, fuel=1)  # C only has enablement at 0
    st_no_op1 = step_det(st_no_op)
    assert isinstance(st_no_op1, State)
    assert st_no_op1.active == 1 and st_no_op1.fuel == 0
    st_no_op2 = step_det(st_no_op1)
    assert st_no_op2 is Terminal.HALT, f"Expected HALT when no op enabled at fuel 0, got {st_no_op2}"

    # Subtest 3: Fuel = 0 boundary in CFG runner
    b = CFGBuilder().add_step(src_pc=0, next_pc=1)
    g = b.to_graph()
    cfg_f0 = init_cfg(g, start_pc=0, initial_data=0, fuel=0)
    cfg_res = step_cfg(cfg_f0)
    assert cfg_res is Terminal.EXHAUSTED, f"CFG at fuel 0 returned {cfg_res}"

    # Subtest 4: Invalid/malformed configurations
    try:
        init(C, x=0, fuel=-1)
        assert False, "Negative fuel accepted by init"
    except ExecutionError:
        pass

    try:
        init(C, x=99, fuel=10)
        assert False, "Out-of-carrier start datum accepted by init"
    except ExecutionError:
        pass

    try:
        check_word((-1, 0))
        assert False, "Negative word letter accepted by check_word"
    except ExecutionError:
        pass

    # Subtest 5: Disconnected graph / missing edge refusal
    # Operation is enabled at 0, but edge (3, (0, y)) is absent from graph
    orphan_graph = frozenset([
        (3 + 1 + 0, (0, 0)),  # Enablement edge for op 0
        # Notice: op edge (3, (0, y)) is completely missing!
    ])
    orphan_st = State(graph=orphan_graph, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    orphan_step = step_det(orphan_st)
    assert orphan_step is Terminal.REFUSE, (
        f"Missing edge returned {orphan_step} instead of Terminal.REFUSE"
    )


def test_target_a_memory_ladder_and_high_fuel() -> None:
    """Challenge 1.4: Test memory ladder monotonicity, ceiling breaks, and high-fuel execution."""
    print("  [Target A] Testing memory ladder monotonicity and high-fuel execution...")

    # 1. Canonical witnesses from memory.py
    assert not functional(1, MEM_TWIST_TAPE), "TWIST_TAPE (0, 1, 0, 0) should not be 1-functional"
    assert functional(2, MEM_TWIST_TAPE), "TWIST_TAPE (0, 1, 0, 0) should be 2-functional"

    assert not functional(1, MEM_TWIST2_TAPE), "TWIST2_TAPE should not be 1-functional"
    assert not functional(2, MEM_TWIST2_TAPE), "TWIST2_TAPE should not be 2-functional"
    assert functional(3, MEM_TWIST2_TAPE), "TWIST2_TAPE should be 3-functional"

    # 2. Ladder monotonicity: functional(k, tape) => functional(k+1, tape) for random tapes
    random.seed(998877)
    for _ in range(50):
        t_len = random.randint(5, 30)
        tape = tuple(random.randint(0, 3) for _ in range(t_len))
        for k in (1, 2, 3):
            if functional(k, tape):
                assert functional(k + 1, tape), (
                    f"Ladder monotonicity broken for tape {tape}: {k}-functional but not {k+1}-functional"
                )

    # 3. High fuel boundary: 10,000 steps on cycle program
    tape, z_count, freq, bound_ok = run_cycle_program(n_steps=10000)
    assert bound_ok, "Cycle program failed bound at 10,000 steps"
    assert len(tape) == 10001
    assert 10001 <= 3 * z_count <= 10003


# ===========================================================================
# 2. Target B Adversarial Challenges
# ===========================================================================

def test_target_b_rational_bounds_random_sample() -> None:
    """Challenge 2.1: Test L <= 3*zeros(L) <= L+2 across 100+ random cycle lengths L in [1, 500]."""
    print("  [Target B] Testing rational bounds across 150 random cycle lengths in [1, 500]...")

    random.seed(20260910)
    # Generate 150 distinct sample lengths including boundaries
    sample_lengths = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500])
    while len(sample_lengths) < 150:
        sample_lengths.add(random.randint(1, 500))

    sorted_samples = sorted(sample_lengths)
    for L in sorted_samples:
        z = zeros(L)
        z_cf = zeros_closed_form(L)
        assert z == z_cf, f"Closed form mismatch at L={L}: {z} != {z_cf}"

        # 1. Quantitative integer bounds: L <= 3*zeros(L) <= L + 2
        assert L <= 3 * z <= L + 2, (
            f"Bounds violated at L={L}: 3*zeros({L})={3*z}, expected in [{L}, {L+2}]"
        )
        assert verify_zeros_bounds(L)

        # 2. Exact rational frequency error bound in Q: |zeros(L)/L - 1/3| <= 2 / (3L)
        freq = rational_frequency(L)
        err = rational_frequency_error(L)
        budget = Fraction(2, 3 * L)
        assert err <= budget, (
            f"Rational error budget exceeded at L={L}: err={err} > budget={budget}"
        )
        assert verify_rational_error_bound(L)

        # 3. Execution on Target A runner for sample subsets (L in [1, 50])
        if L <= 50:
            tape, z_count, tape_freq, bound_ok = run_cycle_program(n_steps=L)
            assert bound_ok, f"Cycle program run failed bound at steps={L}"
            tape_len = len(tape)
            assert tape_len == L + 1
            assert tape_len <= 3 * z_count <= tape_len + 2

    # 4. Precision budget monotonicity test
    epsilons = [Fraction(1, 2), Fraction(1, 5), Fraction(1, 10), Fraction(1, 50), Fraction(1, 100), Fraction(1, 500)]
    prev_L = 0
    for eps in epsilons:
        L_req = precision_budget(eps)
        assert L_req >= prev_L, f"Precision budget not monotonic: {L_req} < {prev_L}"
        prev_L = L_req
        actual_err = rational_frequency_error(L_req)
        assert actual_err <= eps, (
            f"Precision budget insufficient: err={actual_err} > eps={eps} at L={L_req}"
        )


def test_target_b_chain_functionality_and_unproduceability() -> None:
    """Challenge 2.2: Assert that non-functional prefix combinations like [0, 1, 0, 2] are strictly unproduceable."""
    print("  [Target B] Testing chain functionality and non-functional prefix unproduceability...")

    # 1. Direct validation of known non-functional tapes
    assert not is_functional(pairs_of(TWIST_TAPE)), "TWIST_TAPE (0, 1, 0, 2) falsely evaluated as functional"
    assert not is_functional(pairs_of((5, 1, 5, 2)))
    assert not is_functional(pairs_of((0, 0, 1, 0, 0, 2)))  # Non-functional at depth 1
    assert not is_functional(pairs_of((1, 2, 3, 4, 1, 99)))

    # 2. Adversarial program generation: verify that NO deterministic machine can EVER emit a non-functional tape
    random.seed(424242)
    carrier_size = 5
    n_programs = 100

    for prog_idx in range(n_programs):
        # Generate random deterministic transition mapping: carrier -> carrier
        mapping = tuple(random.randint(0, carrier_size - 1) for _ in range(carrier_size))
        ops = (mapping,)
        ctrl = tuple((x, 0) for x in range(carrier_size))
        C = Controlled(n=carrier_size, ops=ops, ctrl=ctrl)

        start_x = random.randint(0, carrier_size - 1)
        st = init(C, x=start_x, fuel=30)
        term, final_st = run(st)

        # Every realized deterministic tape MUST be functional
        pairs = pairs_of(final_st.tape)
        assert is_functional(pairs), (
            f"Deterministic runner produced NON-FUNCTIONAL tape: {final_st.tape}"
        )

        # Verify that TWIST_TAPE prefix [0, 1, 0, 2] is NEVER produced
        tape_tuple = final_st.tape
        for i in range(len(tape_tuple) - 3):
            sub = tape_tuple[i:i+4]
            assert sub != TWIST_TAPE, (
                f"Deterministic runner produced TWIST_TAPE subsequence at index {i}: {sub}"
            )


# ===========================================================================
# 3. G010 Adversarial Challenges
# ===========================================================================

def test_g010_capability_smuggling_refusal() -> None:
    """Challenge 3.1: Attempt to bypass capability removal by crafting programs that sneak removed primitives."""
    print("  [G010] Testing capability smuggling refusal and physical absence...")

    lin_interp = LinearInterpreter()
    mem_interp = MemorylessInterpreter()
    stat_interp = StaticAddressInterpreter()

    # Attempt A: Directly submitting branching instructions to LinearInterpreter
    branch_progs = [
        [JumpIfZero(cond_reg=0, target_pc=5)],
        [JumpIfNotZero(cond_reg=0, target_pc=5)],
    ]
    for prog in branch_progs:
        view = lin_interp.run(prog, inputs=(0,))
        assert view.status == "SYNTAX_REFUSED", (
            f"LinearInterpreter accepted branching instruction: status={view.status}"
        )
        assert "requires BRANCHING" in (view.error or "")

    # Attempt B: Sneaking custom instruction with required_capability = None past AST validator
    class SneakyBranch(Instruction):
        @property
        def required_capability(self) -> Capability | None:
            return None  # Disguised as base primitive!

    sneaky_prog = [SneakyBranch()]
    # validate_program may not reject SneakyBranch because required_capability is None,
    # BUT step() must physically refuse it because it has no dispatch case!
    try:
        lin_interp.run(sneaky_prog, inputs=(0,))
        assert False, "LinearInterpreter silently executed unauthorized custom instruction"
    except SyntaxRefusal as exc:
        assert exc.capability == Capability.BRANCHING, f"Wrong refusal capability: {exc}"

    # Attempt C: Submitting memory instructions to MemorylessInterpreter
    mem_progs = [
        [StoreMem(addr_reg=0, val_reg=1)],
        [LoadMem(dst_reg=0, addr_reg=1)],
    ]
    for prog in mem_progs:
        view = mem_interp.run(prog, inputs=(0, 1))
        assert view.status == "SYNTAX_REFUSED"
        assert "requires MEMORY_RETENTION" in (view.error or "")

    # Attempt D: Submitting dynamic allocation to StaticAddressInterpreter
    alloc_prog = [AllocFresh(dst_reg=0)]
    view = stat_interp.run(alloc_prog, inputs=())
    assert view.status == "SYNTAX_REFUSED"
    assert "requires ADDRESS_ALLOCATION" in (view.error or "")


def test_g010_straight_line_length_invariance_fuzzing() -> None:
    """Challenge 3.2: Adversarially fuzz 200 random linear programs to verify tape length is 100% input-invariant."""
    print("  [G010] Fuzzing 200 random linear programs to test tape length invariance...")

    random.seed(987654)
    interp = LinearInterpreter()
    n_programs = 200

    linear_op_choices = [
        lambda: Nop(),
        lambda: SetConst(dst=random.randint(0, 3), val=random.randint(0, 50)),
        lambda: Add(dst=random.randint(0, 3), src1=random.randint(0, 3), src2=random.randint(0, 3)),
        lambda: Inc(reg=random.randint(0, 3)),
        lambda: Emit(src=random.randint(0, 3)),
        lambda: Halt(),
    ]

    for p_idx in range(n_programs):
        prog_len = random.randint(3, 20)
        prog: list[Instruction] = [random.choice(linear_op_choices)() for _ in range(prog_len)]

        # Run on diverse inputs
        v0 = interp.run(prog, inputs=(0,))
        v1 = interp.run(prog, inputs=(1,))
        v99 = interp.run(prog, inputs=(99,))
        v_neg = interp.run(prog, inputs=(-5,))

        len0 = len(v0.output_tape)
        len1 = len(v1.output_tape)
        len99 = len(v99.output_tape)
        len_neg = len(v_neg.output_tape)

        # In a straight-line program, tape length MUST be strictly invariant across ALL inputs
        assert len0 == len1 == len99 == len_neg, (
            f"Linear program {p_idx} violated length invariance: {len0}, {len1}, {len99}, {len_neg}"
        )

    # Verify that CONDITIONAL_ROUTING_TASK is obstructed for LinearInterpreter
    task = make_conditional_routing_task()
    # Any linear program emits same length on (0,) and (1,), but task requires 1 and 2
    dummy_linear_prog = [SetConst(dst=0, val=10), Emit(src=0), Halt()]
    v_task0 = interp.run(dummy_linear_prog, inputs=task.test_inputs[0])
    v_task1 = interp.run(dummy_linear_prog, inputs=task.test_inputs[1])
    assert not task.validator((v_task0, v_task1)), (
        "Linear program falsely passed conditional routing task!"
    )


def test_g010_memoryless_state_collapse_adversarial() -> None:
    """Challenge 3.3: Verify that destructive clobbering in MemorylessInterpreter permanently erases inputs."""
    print("  [G010] Testing state collapse and memory obstruction under destructive clobbering...")

    interp = MemorylessInterpreter()
    # Program zeroes registers 0 through 3, then emits register 0
    clobber_prog = [
        SetConst(dst=0, val=0),
        SetConst(dst=1, val=0),
        SetConst(dst=2, val=0),
        SetConst(dst=3, val=0),
        Emit(src=0),
        Halt(),
    ]

    # Test 50 distinct pairs of inputs
    random.seed(112233)
    for _ in range(50):
        x = random.randint(1, 1000000)
        y = random.randint(1, 1000000)
        if x == y:
            y += 1

        v_x = interp.run(clobber_prog, inputs=(x,))
        v_y = interp.run(clobber_prog, inputs=(y,))

        # Distinct inputs MUST collapse to identical output
        assert v_x.output_tape == v_y.output_tape == (0,), (
            f"State collapse failed for {x} vs {y}: {v_x.output_tape} vs {v_y.output_tape}"
        )


def test_g010_adapter_non_recoverability_stress() -> None:
    """Challenge 3.4: Stress-test that linear/length-preserving adapters cannot bypass branching obstruction."""
    print("  [G010] Stress-testing adapter non-recoverability...")

    task = make_conditional_routing_task()
    interp = LinearInterpreter()
    prog = [SetConst(dst=0, val=10), Emit(src=0), Halt()]

    # Adversarial candidate adapters attempting to modify output
    adversarial_adapters = [
        # Adapter 1: Identity
        LinearAdapter(input_transform=lambda inps: inps, output_transform=lambda view: view),
        # Adapter 2: Value scaling (transforms values but preserves length)
        LinearAdapter(
            input_transform=lambda inps: inps,
            output_transform=lambda view: PublicView(
                output_tape=tuple(v * 2 for v in view.output_tape),
                steps=view.steps,
                halted=view.halted,
                status=view.status,
            ),
        ),
        # Adapter 3: Input perturbation
        LinearAdapter(
            input_transform=lambda inps: tuple(x + 100 for x in inps),
            output_transform=lambda view: view,
        ),
    ]

    for idx, adapter in enumerate(adversarial_adapters):
        failed = verify_adapter_cannot_bypass_branching(adapter, interp, prog, task)
        assert failed, f"Adapter {idx} bypassed branching obstruction!"


# ===========================================================================
# Master Execution Harness
# ===========================================================================

def run_all_adversarial_challenges() -> None:
    print("=====================================================================")
    print("  RUNNING ADVERSARIAL BEHAVIORAL & PHYSICAL DYNAMICS CHALLENGE SUITE")
    print("  Scope: Genesis Cohort 2 (Targets A & B, G010)")
    print("=====================================================================")

    print("\n--- Target A Challenges ---")
    test_target_a_fork_refusal_exhaustive()
    test_target_a_ambiguous_graph_refusal()
    test_target_a_extreme_and_fuel_boundaries()
    test_target_a_memory_ladder_and_high_fuel()
    print("  PASS: Target A fork refusal, ambiguity detection, memory ladder, and fuel boundaries verified.")

    print("\n--- Target B Challenges ---")
    test_target_b_rational_bounds_random_sample()
    test_target_b_chain_functionality_and_unproduceability()
    print("  PASS: Target B rational bounds (150 random L) and chain functionality verified.")

    print("\n--- G010 Challenges ---")
    test_g010_capability_smuggling_refusal()
    test_g010_straight_line_length_invariance_fuzzing()
    test_g010_memoryless_state_collapse_adversarial()
    test_g010_adapter_non_recoverability_stress()
    print("  PASS: G010 capability removal, obstruction proofs, and adapter non-recoverability verified.")

    print("\n=====================================================================")
    print("  ALL EMPIRICAL ADVERSARIAL CHALLENGES PASSED (100% SUCCESS RATE)")
    print("=====================================================================")


if __name__ == "__main__":
    run_all_adversarial_challenges()
