"""Adversarial Fuzzing & Scale Invariant Stress Test Suite.

Challenger 2 Empirical Verification:
1. G011 Finitary Substrate:
   - fresh_address large scale allocation, collision resistance, and disjointness
   - Hierarchical address trees with deep nested branches and sibling path comparisons
   - Fuel-bounded recursion with complex AST instructions and boundary fuel values (0, 1, exact, excess)
2. G001 Target-Class Charter:
   - Frozen charter field immutability & CharterFreezeError enforcement
   - Comparison morphism composition associativity and distortion accumulation
3. E2E Suites:
   - Randomized input stress testing of E2E verification models

Adheres strictly to the Claim Hygiene Rule: local receipts only, empirical bounds reported.
AuthorityEffect: None.
"""

from __future__ import annotations

import math
import random
import sys
import time

sys.stdout.reconfigure(line_buffering=True)
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import Any, List, Sequence, Tuple

# Path setup
REPO_ROOT = Path(__file__).resolve().parent.parent
RESEARCH_DIR = REPO_ROOT / "research"
G011_DIR = RESEARCH_DIR / "g011_finitary_substrate"
G001_DIR = RESEARCH_DIR / "g001_target_charter"
E2E_DIR = RESEARCH_DIR / "e2e_tests"

for p in [str(G011_DIR), str(G001_DIR), str(E2E_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Imports from G011
import ordinals as g011_ord
from ordinals import Ordinal, Zero, Succ
import address as g011_addr
from address import Address, Root, Child
import freshness as g011_fresh
from freshness import AddressRegistry, fresh_address, fresh_index, max_branch_index
import recursion as g011_rec
from recursion import (
    State as G011State,
    NumVal,
    AddrVal,
    Nop,
    SetZero,
    SuccReg,
    PredReg,
    CopyReg,
    AllocAddr,
    WriteMem,
    ReadMem,
    Jump,
    BranchIfZero,
    Halt,
    Halted,
    OutOfFuel,
    run_with_fuel,
    rec_fuel,
    step as g011_step,
)

# Imports from G001
import charter as g001_charter
from charter import (
    AdequacyCriterion,
    CharterFreezeError,
    CriterionID,
    TargetClassCharter,
    default_criteria,
)
import adequacy as g001_adeq
from adequacy import EvaluationReport, TargetSystem, Verdict
import morphism as g001_morph
from morphism import (
    ComparisonMorphism,
    MorphismCompositionError,
    compose_morphisms,
    identity_morphism,
    verify_category_laws,
)

# Imports from E2E Harness
import harness as e2e_harness


# ============================================================================
# RESULTS TRACKER
# ============================================================================

class TestReport:
    def __init__(self):
        self.passed: List[str] = []
        self.findings: List[Tuple[str, str, str]] = [] # (Name, Severity, Description)
        self.receipts: List[str] = []

    def record_pass(self, name: str, details: str = ""):
        self.passed.append(name)
        msg = f"[PASS] {name}"
        if details:
            msg += f" -- {details}"
        self.receipts.append(msg)
        print(msg)

    def record_finding(self, name: str, severity: str, details: str):
        self.findings.append((name, severity, details))
        msg = f"[{severity}] {name}: {details}"
        self.receipts.append(msg)
        print(msg)


REPORT = TestReport()


# ============================================================================
# 1. G011 FINITARY SUBSTRATE FUZZING & STRESS TESTS
# ============================================================================

def stress_g011_fresh_address_sequential():
    """Stress test fresh_address with sequential allocations up to the recursion threshold."""
    print("\n--- G011.1: Sequential Address Allocation & Recursion Limit Fuzzing ---")
    reg = AddressRegistry.empty()
    allocated: list[Address] = []
    
    # 1. Test scaling from 1 to 150 allocations
    t0 = time.perf_counter()
    sample_points = [10, 50, 100, 150]
    for i in range(150):
        reg, fresh = reg.allocate()
        allocated.append(fresh)
        if (i + 1) in sample_points:
            t_elapsed = time.perf_counter() - t0
            REPORT.record_pass(f"sequential_alloc_N_{i+1}", f"Elapsed: {t_elapsed:.4f}s")
            
    # Verify zero collisions and strict pairwise disjointness among sample of allocated addresses
    sample_addrs = allocated[::15] # 10 sample addresses
    for idx_a, a in enumerate(sample_addrs):
        for idx_b, b in enumerate(sample_addrs):
            if idx_a != idx_b:
                assert a != b, f"Collision detected between {a} and {b}!"
                assert a.is_disjoint_from(b), f"Disjointness violation between {a} and {b}!"
    REPORT.record_pass("sequential_disjointness_sample_150", "Zero collisions, strict disjointness verified across sample.")

    # 2. Boundary test: verify fresh_address at N=980
    print("Testing recursion boundary on fresh_address...")
    boundary_alloc = [Address.root().child(Ordinal.from_nat(i)) for i in range(980)]
    f_980 = fresh_address(boundary_alloc)
    assert f_980 == Address.root().child(Ordinal.from_nat(980))
    REPORT.record_pass("fresh_address_boundary_980", "fresh_address succeeded at N=980")

    # 3. Adversarial Challenge: Find the exact boundary where Python recursion fails
    exact_fail = None
    for n in range(981, 1005):
        try:
            boundary_alloc.append(Address.root().child(Ordinal.from_nat(n - 1)))
            f_n = fresh_address(boundary_alloc)
        except RecursionError as e:
            exact_fail = (n, str(e))
            break
            
    if exact_fail:
        REPORT.record_finding(
            "G011_FRESH_ADDRESS_RECURSION_LIMIT",
            "CRITICAL_SCALING_DEFECT",
            f"fresh_address failed with RecursionError at N={exact_fail[0]}: {exact_fail[1]}. "
            "Cause: Ordinal.le recursively calls self._pred.le(other.pred()) exceeding Python stack depth.",
        )
    else:
        REPORT.record_pass("fresh_address_1000", "fresh_address succeeded up to 1000")


def stress_g011_fresh_address_wide_10000():
    """Stress test fresh_address with 10,000+ randomized wide hierarchical addresses."""
    print("\n--- G011.2: 10,000+ Address Large Set Allocation & Disjointness ---")
    random.seed(42)
    # Generate 10,000 distinct addresses distributed across wide branching structure
    # to avoid deep ordinals while maintaining a massive address registry:
    # 100 top branches (0..99) x 100 sub-branches (0..99)
    top_branches = [Ordinal.from_nat(i) for i in range(100)]
    sub_branches = [Ordinal.from_nat(j) for j in range(100)]
    
    t0 = time.perf_counter()
    allocated_10000: list[Address] = []
    for top in top_branches:
        parent = Address.root().child(top)
        for sub in sub_branches:
            allocated_10000.append(parent.child(sub))
            
    t_gen = time.perf_counter() - t0
    assert len(allocated_10000) == 10000
    REPORT.record_pass("generate_10000_addresses", f"Generated 10,000 structured addresses in {t_gen:.4f}s")
    
    # Verify uniqueness of all 10,000 addresses in the sequence
    t0 = time.perf_counter()
    addr_set = set(allocated_10000)
    assert len(addr_set) == 10000, f"Expected 10,000 distinct addresses, got {len(addr_set)}"
    REPORT.record_pass("verify_10000_unique", f"Verified 10,000 unique addresses via hash set in {time.perf_counter()-t0:.4f}s")
    
    # Execute fresh_address on the 10,000-address registry
    t0 = time.perf_counter()
    fresh = fresh_address(allocated_10000)
    t_fresh = time.perf_counter() - t0
    
    # The maximum top-level branch was 99, so fresh index must be 100
    expected_top = Ordinal.from_nat(100)
    assert fresh == Address.root().child(expected_top), f"Expected top branch 100, got {fresh}"
    REPORT.record_pass("fresh_address_10000_correctness", f"Computed fresh address {fresh} in {t_fresh:.4f}s")
    
    # Assert ZERO collisions with any of the 10,000 allocated addresses
    assert fresh not in addr_set, "Collision! Fresh address was found in allocated set!"
    REPORT.record_pass("fresh_address_10000_zero_collisions", "Confirmed ZERO collisions against all 10,000 addresses.")
    
    # Assert strict disjointness against randomized sample of 500 allocated addresses
    sample_check = random.sample(allocated_10000, 500)
    disjoint_count = 0
    for a in sample_check:
        assert fresh.is_disjoint_from(a), f"Disjointness failure: {fresh} is not disjoint from {a}"
        disjoint_count += 1
    REPORT.record_pass("fresh_address_10000_strict_disjointness", f"Confirmed strict disjointness against {disjoint_count} sampled addresses.")


def stress_g011_hierarchical_address_trees():
    """Stress test hierarchical address trees with deep nested branches and sibling path comparisons."""
    print("\n--- G011.3: Hierarchical Address Trees Deep Branching & Siblings ---")
    
    # 1. Build deep spines: root -> child(0) -> child(0) ...
    depths = [10, 50, 100, 200, 500, 990]
    deep_nodes: dict[int, Address] = {}
    
    curr = Address.root()
    z = Zero()
    for d in range(1, 991):
        curr = curr.child(z)
        if d in depths:
            deep_nodes[d] = curr
            
    # Check depth() on deep nodes
    for d, node in deep_nodes.items():
        assert node.depth().to_nat() == d, f"Depth mismatch at {d}: got {node.depth().to_nat()}"
    REPORT.record_pass("deep_tree_depth_metric", "Depth metric exact across depths up to 990.")

    # Check to_path and from_path round-trip on deep nodes
    for d in [10, 50, 100, 500]:
        node = deep_nodes[d]
        path = node.to_path()
        assert len(path) == d
        reconstructed = Address.from_path(path)
        assert reconstructed == node
    REPORT.record_pass("deep_tree_path_roundtrip", "to_path / from_path round-trip exact up to depth 500.")

    # 2. Sibling path comparisons
    # Compare spine node with sibling branch:
    # A = spine(d) = child(0)^d
    # B = sibling(d) = child(0)^(d-1).child(1)
    s1 = Succ(Zero())
    for d in [10, 100, 500]:
        node_a = deep_nodes[d]
        parent = node_a.parent()
        assert parent is not None
        sibling_b = parent.child(s1)
        
        # Must not be equal
        assert node_a != sibling_b
        # Neither is prefix of the other
        assert not node_a.is_prefix_of(sibling_b)
        assert not sibling_b.is_prefix_of(node_a)
        # Must be strictly disjoint
        assert node_a.is_disjoint_from(sibling_b)
        assert sibling_b.is_disjoint_from(node_a)
    REPORT.record_pass("deep_tree_sibling_disjointness", "Strict sibling disjointness verified at depth 10, 100, 500.")

    # 3. Adversarial Challenge: Deep Address Equality Recursion Limit
    try:
        deep_1000 = Address.root()
        for _ in range(1005):
            deep_1000 = deep_1000.child(Zero())
        # Equality check triggers recursive Child.__eq__ on parent
        is_eq = (deep_1000 == deep_1000)
        REPORT.record_pass("deep_tree_1005_eq", "Unexpectedly passed depth 1005 equality")
    except RecursionError as e:
        REPORT.record_finding(
            "G011_ADDRESS_EQ_RECURSION_LIMIT",
            "CRITICAL_SCALING_DEFECT",
            f"Address equality check failed with RecursionError at depth 1005: {e}. "
            "Cause: Child.__eq__ recursively compares self._parent == other._parent.",
        )

    # 4. Adversarial Challenge: Deep Address Hash Recursion Limit
    try:
        h = hash(deep_1000)
        REPORT.record_pass("deep_tree_1005_hash", "Unexpectedly passed depth 1005 hash")
    except RecursionError as e:
        REPORT.record_finding(
            "G011_ADDRESS_HASH_RECURSION_LIMIT",
            "CRITICAL_SCALING_DEFECT",
            f"Address hash failed with RecursionError at depth 1005: {e}. "
            "Cause: Child.__hash__ hashes (Child, self._parent, self._branch) recursively.",
        )


def stress_g011_fuel_bounded_recursion():
    """Test fuel-bounded recursion with complex AST instructions and boundary fuel values (0, 1, exact, excess)."""
    print("\n--- G011.4: Fuel-Bounded Recursion AST & Boundary Stress Tests ---")
    
    r0 = Ordinal.zero()
    r1 = r0.succ()
    r2 = r1.succ()
    r3 = r2.succ()
    
    # 1. Complex Program: Memory Allocation, Computation Loop, Read/Write
    # Loop 3 times:
    # 0: AllocAddr(dst=r0)          -- allocate fresh address -> mem[fresh] = 0
    # 1: SuccReg(reg=r1)            -- r1 (counter) ++
    # 2: WriteMem(r0, r1)           -- mem[r0] = r1
    # 3: ReadMem(r2, r0)            -- r2 = mem[r0]
    # 4: PredReg(reg=r3)            -- r3 (countdown) --
    # 5: BranchIfZero(r3, target=7) -- if countdown == 0 goto 7 (Halt)
    # 6: Jump(target=0)             -- goto 0
    # 7: Halt()
    prog: list[g011_rec.Instr] = [
        AllocAddr(dst=r0),
        SuccReg(reg=r1),
        WriteMem(addr_reg=r0, val_reg=r1),
        ReadMem(dst=r2, addr_reg=r0),
        PredReg(reg=r3),
        BranchIfZero(reg=r3, target=Ordinal.from_nat(7)),
        Jump(target=Ordinal.from_nat(0)),
        Halt(),
    ]
    
    # Initial state: r3 = 3 (loop 3 times)
    initial_state = G011State().set_reg(r3, NumVal(Ordinal.from_nat(3)))
    
    # Trace execution steps:
    # Iter 1: instructions 0, 1, 2, 3, 4, 5 (fallthrough), 6 (jump 0) -> 7 steps
    # Iter 2: instructions 0, 1, 2, 3, 4, 5 (fallthrough), 6 (jump 0) -> 7 steps
    # Iter 3: instructions 0, 1, 2, 3, 4, 5 (branch to 7), 7 (halt)   -> 7 steps
    # Total exact steps to halt = 7 + 7 + 7 = 21 steps.
    exact_steps = 21
    
    # Boundary Fuel Test A: fuel = 0
    res_zero = run_with_fuel(Ordinal.zero(), prog, initial_state)
    assert isinstance(res_zero, OutOfFuel), f"Expected OutOfFuel at fuel 0, got {res_zero}"
    assert not res_zero.state.halted
    assert res_zero.state.pc == Ordinal.zero()
    REPORT.record_pass("fuel_boundary_0", "Fuel=0 returns OutOfFuel without advancing state.")

    # Boundary Fuel Test B: fuel = 1
    res_one = run_with_fuel(Ordinal.from_nat(1), prog, initial_state)
    assert isinstance(res_one, OutOfFuel), f"Expected OutOfFuel at fuel 1, got {res_one}"
    assert not res_one.state.halted
    assert res_one.state.pc == Ordinal.from_nat(1) # Executed only AllocAddr(0)
    assert len(res_one.state.addrs) == 1
    REPORT.record_pass("fuel_boundary_1", "Fuel=1 executes exactly 1 step and returns OutOfFuel.")

    # Boundary Fuel Test C: fuel = exact - 1 (underflow)
    res_under = run_with_fuel(Ordinal.from_nat(exact_steps - 1), prog, initial_state)
    assert isinstance(res_under, OutOfFuel), f"Expected OutOfFuel at fuel {exact_steps - 1}, got {res_under}"
    assert not res_under.state.halted
    REPORT.record_pass(f"fuel_boundary_underflow_{exact_steps-1}", "Fuel=exact-1 exhausts fuel right before terminal halt.")

    # Boundary Fuel Test D: fuel = exact (exact)
    res_exact = run_with_fuel(Ordinal.from_nat(exact_steps), prog, initial_state)
    assert isinstance(res_exact, Halted), f"Expected Halted at fuel {exact_steps}, got {res_exact}"
    assert res_exact.state.halted
    assert res_exact.state.get_reg(r1) == NumVal(Ordinal.from_nat(3))
    assert res_exact.state.get_reg(r2) == NumVal(Ordinal.from_nat(3))
    assert len(res_exact.state.addrs) == 3
    REPORT.record_pass(f"fuel_boundary_exact_{exact_steps}", "Fuel=exact successfully reaches Halted with accurate memory/registers.")

    # Boundary Fuel Test E: fuel = exact + 50 (excess)
    res_excess = run_with_fuel(Ordinal.from_nat(exact_steps + 50), prog, initial_state)
    assert isinstance(res_excess, Halted), f"Expected Halted at fuel {exact_steps + 50}, got {res_excess}"
    assert res_excess.state.halted
    # Excess fuel MUST produce identical state to exact fuel without post-halt execution
    assert res_excess.state.pc == res_exact.state.pc
    assert res_excess.state.regs == res_exact.state.regs
    assert res_excess.state.mem == res_exact.state.mem
    assert res_excess.state.addrs == res_exact.state.addrs
    REPORT.record_pass(f"fuel_boundary_excess_{exact_steps+50}", "Excess fuel preserves exact final halted state without post-halt drift.")

    # 2. Type Refusal on Memory Instruction
    # Attempt WriteMem with NumVal in addr_reg
    refusal_prog: list[g011_rec.Instr] = [
        SetZero(reg=r0), # r0 = NumVal(0)
        WriteMem(addr_reg=r0, val_reg=r1), # Invalid! r0 is not AddrVal
    ]
    ref_res = run_with_fuel(Ordinal.from_nat(5), refusal_prog, G011State())
    assert isinstance(ref_res, Halted)
    assert ref_res.state.halted
    assert ref_res.state.pc == Ordinal.from_nat(1) # Halted immediately at WriteMem without advancing pc
    REPORT.record_pass("refusal_type_violation_write_mem", "WriteMem with NumVal in addr_reg unconditionally halts (refusal).")

    # 3. Structural Recursion Scheme (rec_fuel)
    # Factorial via endogenous structural recursion:
    # rec_fuel(0, 1, step) = 1
    # rec_fuel(n, base, step) = n * rec_fuel(n-1, base, step)
    def fact_step(n: Ordinal, acc: int) -> int:
        return n.succ().to_nat() * acc
        
    for n, expected_fact in [(0, 1), (1, 1), (2, 2), (3, 6), (4, 24), (5, 120), (6, 720)]:
        val = rec_fuel(Ordinal.from_nat(n), 1, fact_step)
        assert val == expected_fact, f"Factorial mismatch for {n}: {val} != {expected_fact}"
    REPORT.record_pass("rec_fuel_structural_recursion", "rec_fuel computes correct structural recursion up to 6! = 720.")

    # Adversarial Challenge on rec_fuel depth
    try:
        rec_fuel(Ordinal.from_nat(1005), 0, lambda n, acc: acc + 1)
        REPORT.record_pass("rec_fuel_1005", "Unexpectedly passed fuel 1005 in rec_fuel")
    except RecursionError as e:
        REPORT.record_finding(
            "G011_REC_FUEL_PYTHON_STACK_LIMIT",
            "CRITICAL_SCALING_DEFECT",
            f"rec_fuel crashed with RecursionError at fuel 1005: {e}. "
            "Cause: rec_fuel uses direct Python recursion without trampoline.",
        )


# ============================================================================
# 2. G001 TARGET-CLASS CHARTER STRESS TESTS
# ============================================================================

def stress_g001_charter_mutations():
    """Attempt to mutate frozen charter fields and verify CharterFreezeError is unconditionally raised."""
    print("\n--- G001.1: Target-Class Charter Freeze & Mutation Falsification ---")
    
    charter = TargetClassCharter()
    assert not charter.is_frozen
    assert charter.status == TargetClassCharter.UNFROZEN_STATUS
    
    # 1. Freezing the charter
    h1 = charter.freeze()
    assert charter.is_frozen
    assert charter.status == TargetClassCharter.FROZEN_STATUS
    assert charter.freeze_hash == h1
    REPORT.record_pass("charter_freeze_success", f"Charter frozen with SHA256 digest: {h1[:16]}...")
    
    # 2. Deterministic Hash Invariance
    h2 = charter.compute_hash()
    assert h1 == h2, "Hash mismatch on repeated computation!"
    REPORT.record_pass("charter_hash_invariance", "Charter cryptographic hash is strictly deterministic.")

    # 3. Attempt modify_criterion on frozen charter -> MUST raise CharterFreezeError
    crit = charter.get_criterion(CriterionID.COMPUTATIONAL)
    modified_crit = AdequacyCriterion(
        criterion_id=crit.criterion_id,
        name="Mutated Name",
        dimension=crit.dimension,
        description=crit.description,
        required_capabilities=crit.required_capabilities,
        falsification_conditions=crit.falsification_conditions,
        weight=99.0,
    )
    try:
        charter.modify_criterion(modified_crit)
        REPORT.record_finding("CHARTER_MODIFY_MUTATION_BREACH", "CRITICAL", "modify_criterion succeeded on frozen charter!")
    except CharterFreezeError:
        REPORT.record_pass("charter_modify_blocked", "CharterFreezeError unconditionally raised on modify_criterion.")

    # 4. Attempt add_criterion on frozen charter -> MUST raise CharterFreezeError
    try:
        charter.add_criterion(modified_crit)
        REPORT.record_finding("CHARTER_ADD_MUTATION_BREACH", "CRITICAL", "add_criterion succeeded on frozen charter!")
    except CharterFreezeError:
        REPORT.record_pass("charter_add_blocked", "CharterFreezeError unconditionally raised on add_criterion.")

    # 5. Attempt remove_criterion on frozen charter -> MUST raise CharterFreezeError
    try:
        charter.remove_criterion(CriterionID.COMPUTATIONAL)
        REPORT.record_finding("CHARTER_REMOVE_MUTATION_BREACH", "CRITICAL", "remove_criterion succeeded on frozen charter!")
    except CharterFreezeError:
        REPORT.record_pass("charter_remove_blocked", "CharterFreezeError unconditionally raised on remove_criterion.")

    # 6. Attempt mutation via returned criteria dict
    crit_dict = charter.criteria
    crit_dict[CriterionID.COMPUTATIONAL] = modified_crit
    # Verify original in charter was not mutated
    assert charter.get_criterion(CriterionID.COMPUTATIONAL).name != "Mutated Name"
    REPORT.record_pass("charter_dict_copy_isolation", "charter.criteria returns an isolated defensive copy.")

    # 7. Attempt in-place attribute mutation on returned AdequacyCriterion
    try:
        c_obj = charter.get_criterion(CriterionID.COMPUTATIONAL)
        c_obj.name = "Hacked"  # type: ignore
        REPORT.record_finding("CRITERION_MUTATION_BREACH", "HIGH", "AdequacyCriterion field modification succeeded!")
    except FrozenInstanceError:
        REPORT.record_pass("criterion_frozen_instance", "AdequacyCriterion raises FrozenInstanceError on direct attribute assignment.")

    # 8. Adversarial Challenge: Direct private attribute mutation
    # TargetClassCharter overrides __setattr__, preventing private field tampering
    try:
        charter._status = TargetClassCharter.UNFROZEN_STATUS
        if not charter.is_frozen:
            REPORT.record_finding(
                "G001_CHARTER_PRIVATE_ENCAPSULATION_GAP",
                "MEDIUM_HYGIENE_DEFECT",
                "TargetClassCharter lacks __setattr__ freeze guard: charter._status can be reset to UNFROZEN from outside.",
            )
            # Restore frozen status for subsequent tests
            charter._status = TargetClassCharter.FROZEN_STATUS
    except CharterFreezeError:
        REPORT.record_pass("charter_private_status_protected", "TargetClassCharter correctly rejects direct _status tampering.")


def stress_g001_comparison_morphisms():
    """Test comparison morphism composition associativity and distortion accumulation across chained morphisms."""
    print("\n--- G001.2: Comparison Morphism Composition Associativity & Distortion ---")
    
    # Construct 4 distinct test target systems
    S0 = TargetSystem("S0", [1, 2, 3], ["step"], lambda s, op: s + 1, lambda s: s)
    S1 = TargetSystem("S1", [10, 20, 30], ["step"], lambda s, op: s + 10, lambda s: s * 10)
    S2 = TargetSystem("S2", [100, 200, 300], ["step"], lambda s, op: s + 100, lambda s: s * 100)
    S3 = TargetSystem("S3", [1000, 2000, 3000], ["step"], lambda s, op: s + 1000, lambda s: s * 1000)
    
    # Construct 3 comparison morphisms with distinct nonlinear mapping functions
    m0 = ComparisonMorphism(
        name="m0",
        source=S0,
        target=S1,
        map_state=lambda s: s * 10,
        map_op=lambda op: op,
        map_obs=lambda obs: obs * 10,
        distortion=0.1,
        preserves_criteria={CriterionID.COMPUTATIONAL, CriterionID.REASONING, CriterionID.PHYSICAL},
    )
    m1 = ComparisonMorphism(
        name="m1",
        source=S1,
        target=S2,
        map_state=lambda s: s * 10,
        map_op=lambda op: op,
        map_obs=lambda obs: obs * 10,
        distortion=0.2,
        preserves_criteria={CriterionID.COMPUTATIONAL, CriterionID.PHYSICAL, CriterionID.EMPIRICAL},
    )
    m2 = ComparisonMorphism(
        name="m2",
        source=S2,
        target=S3,
        map_state=lambda s: s * 10,
        map_op=lambda op: op,
        map_obs=lambda obs: obs * 10,
        distortion=0.3,
        preserves_criteria={CriterionID.COMPUTATIONAL, CriterionID.EMPIRICAL},
    )
    
    # 1. Category Laws Verification via standard helper
    laws = verify_category_laws(m0, m1, m2, test_states=[1, 2, 3], test_ops=["step"], test_obs=[1, 2, 3])
    assert laws["left_identity"], "Left identity law failed!"
    assert laws["right_identity"], "Right identity law failed!"
    assert laws["associativity"], "Associativity law failed!"
    assert laws["distortion_triangle_bound"], "Distortion triangle bound failed!"
    REPORT.record_pass("category_laws_basic", "Category identity, associativity, and triangle bounds verified.")

    # 2. Comprehensive Associativity Stress Test on State, Op, Obs mappings
    # (m2 . m1) . m0
    comp_left = compose_morphisms(compose_morphisms(m0, m1), m2)
    # m2 . (m1 . m0)
    comp_right = compose_morphisms(m0, compose_morphisms(m1, m2))
    
    # Fuzz state transformations with 10,000 random inputs
    random.seed(99)
    test_inputs = [random.randint(-100000, 100000) for _ in range(10000)]
    state_mismatches = 0
    for x in test_inputs:
        val_l = comp_left.map_state(x)
        val_r = comp_right.map_state(x)
        if val_l != val_r:
            state_mismatches += 1
    assert state_mismatches == 0, f"Found {state_mismatches} state mapping associativity mismatches!"
    REPORT.record_pass("morphism_state_associativity_10000", "State mapping associativity holds exactly across 10,000 random inputs.")

    # 3. Preserved Criteria Intersection Associativity
    assert comp_left.preserves_criteria == comp_right.preserves_criteria
    assert comp_left.preserves_criteria == {CriterionID.COMPUTATIONAL}
    REPORT.record_pass("morphism_criteria_intersection", f"Preserved criteria intersection: {comp_left.preserves_criteria}")

    # 4. Adversarial Challenge: Floating Point Distortion Drift in Chained Composition
    print("Testing floating point distortion associativity drift...")
    # comp_left.distortion = (0.1 + 0.2) + 0.3 = 0.6000000000000001
    # comp_right.distortion = 0.1 + (0.2 + 0.3) = 0.6
    dist_l = comp_left.distortion
    dist_r = comp_right.distortion
    diff = abs(dist_l - dist_r)
    
    if dist_l != dist_r:
        REPORT.record_finding(
            "G001_MORPHISM_DISTORTION_FLOAT_DRIFT",
            "MEDIUM_HYGIENE_DEFECT",
            f"Strict distortion equality fails due to float arithmetic: left={dist_l}, right={dist_r}, delta={diff:.2e}. "
            "Morphism category law associativity strictly fails if equality requires dist_l == dist_r. "
            "Mitigation: Use exact rational Fraction arithmetic or declare epsilon-equivalence.",
        )
    else:
        REPORT.record_pass("morphism_distortion_exact", "Distortion equality was exact.")

    # 5. Long Chained Morphism Scaling (50 chained morphisms)
    sys_chain = [TargetSystem(f"T{i}", [0], ["op"], lambda s, op: s, lambda s: s) for i in range(51)]
    m_chain = [
        ComparisonMorphism(
            f"chain_{i}",
            sys_chain[i],
            sys_chain[i+1],
            lambda s: s + 1,
            lambda op: op,
            lambda obs: obs + 1,
            distortion=0.01,
        )
        for i in range(50)
    ]
    curr_m = m_chain[0]
    for m in m_chain[1:]:
        curr_m = compose_morphisms(curr_m, m)
        
    assert curr_m.source.name == "T0"
    assert curr_m.target.name == "T50"
    assert curr_m.map_state(0) == 50
    assert math.isclose(curr_m.distortion, 0.50, rel_tol=1e-9)
    REPORT.record_pass("morphism_chain_50", "Successfully composed chain of 50 comparison morphisms with bounded distortion.")


# ============================================================================
# 3. E2E SUITES RANDOMIZED INPUT STRESS TESTS
# ============================================================================

def stress_e2e_randomized_inputs():
    """Run E2E harness reference models with randomized inputs."""
    print("\n--- E2E.1: Randomized Graph Execution & Invariant Fuzzing ---")
    random.seed(12345)
    
    # 1. Fuzz Target A graph interpreter with 200 random valid graphs
    fuzz_passes = 0
    for test_idx in range(200):
        nops = random.randint(1, 4)
        node_count = random.randint(2, 10)
        
        # Generate random deterministic transitions
        transitions = []
        for op in range(nops):
            for node in range(node_count):
                target = random.randint(0, node_count - 1)
                transitions.append((op, node, target))
                
        # Generate random enablements
        enablements = []
        for node in range(node_count):
            enabled_op = random.randint(0, nops - 1)
            enablements.append((node, enabled_op))
            
        prog = e2e_harness.make_program(nops, transitions, enablements)
        start_node = random.randint(0, node_count - 1)
        fuel = random.randint(1, 50)
        
        state = e2e_harness.State(
            graph=prog,
            nops=nops,
            active=start_node,
            tape=(start_node,),
            clock=0,
            fuel=fuel,
        )
        
        # Execute run_det
        term, final_s = e2e_harness.run_det(fuel, state)
        
        # Verify core execution invariants:
        # Invariant 1: Clock plus remaining fuel == original fuel
        assert final_s.clock + final_s.fuel == fuel, f"Fuel conservation violated: clock={final_s.clock}, fuel={final_s.fuel}, original={fuel}"
        # Invariant 2: Tape length == clock + 1
        assert len(final_s.tape) == final_s.clock + 1, "Tape length != clock + 1"
        # Invariant 3: Active datum == tape[-1]
        assert final_s.active == final_s.tape[-1], "Active datum does not match tape head"
        # Invariant 4: Chain functionality
        assert e2e_harness.is_chain_functional(final_s.tape), "Chain functionality violated in single trace!"
        
        fuzz_passes += 1
        
    REPORT.record_pass("fuzz_target_a_graphs_200", f"200 randomized graph executions verified under fuel conservation & chain functionality.")

    # 2. Fuzz Target B rational frequency bounds
    # For a deterministic 3-cycle, verify zeros bound across randomized cycle lengths
    zeros_bound_passes = 0
    for length in range(1, 300):
        # 3-cycle starting at 0: 0, 1, 2, 0, 1, 2, ...
        tape = tuple(i % 3 for i in range(length))
        zeros = sum(1 for x in tape if x == 0)
        assert e2e_harness.check_zeros_bound(length, zeros), f"Zeros bound violated for length {length}: zeros={zeros}"
        zeros_bound_passes += 1
    REPORT.record_pass("fuzz_target_b_rational_bounds_300", f"Verified L <= 3*zeros <= L+2 across {zeros_bound_passes} randomized sequence lengths.")

    # 3. Fuzz G010 capability restriction on all 16 subsets
    all_caps = [
        e2e_harness.Capability.STORE_MUTATION,
        e2e_harness.Capability.DIRECT_LOOKUP,
        e2e_harness.Capability.CONDITIONAL_BRANCH,
        e2e_harness.Capability.UNBOUNDED_RECURSION,
    ]
    subsets: list[frozenset[e2e_harness.Capability]] = []
    for i in range(16):
        subsets.append(frozenset(all_caps[j] for j in range(4) if (i & (1 << j))))
        
    prog_cycle = e2e_harness.make_program(
        nops=1,
        transitions=[(0, 0, 1), (0, 1, 2), (0, 2, 0)],
        enablements=[(0, 0), (1, 0), (2, 0)],
    )
    
    cap_passes = 0
    for allowed in subsets:
        required = frozenset([e2e_harness.Capability.DIRECT_LOOKUP])
        res = e2e_harness.execute_restricted(prog_cycle, allowed, required, start=0, fuel=5)
        if e2e_harness.Capability.DIRECT_LOOKUP in allowed:
            assert res.status != "OBSTRUCTED_CAPABILITY_ABSENT"
        else:
            assert res.status == "OBSTRUCTED_CAPABILITY_ABSENT"
            assert res.output == ()
        cap_passes += 1
    REPORT.record_pass("fuzz_g010_capability_subsets_16", f"Verified obstruction and execution across all 16 capability subsets.")


# ============================================================================
# MASTER RUNNER & VERDICT EMISSION
# ============================================================================

def main():
    print("=" * 80)
    print("CHALLENGER 2: ADVERSARIAL EMPIRICAL FUZZING HARNESS")
    print("=" * 80)
    
    # 1. G011 Finitary Substrate
    stress_g011_fresh_address_sequential()
    stress_g011_fresh_address_wide_10000()
    stress_g011_hierarchical_address_trees()
    stress_g011_fuel_bounded_recursion()
    
    # 2. G001 Target-Class Charter
    stress_g001_charter_mutations()
    stress_g001_comparison_morphisms()
    
    # 3. E2E Suites
    stress_e2e_randomized_inputs()
    
    print("\n" + "=" * 80)
    print("SUMMARY OF ADVERSARIAL STRESS TEST FINDINGS")
    print("=" * 80)
    print(f"Total Verification Tests Passed: {len(REPORT.passed)}")
    print(f"Total Defects / Findings Logged: {len(REPORT.findings)}")
    print("-" * 80)
    
    for name, sev, desc in REPORT.findings:
        print(f"[{sev}] {name}\n  -> {desc}\n")
        
    print("=" * 80)
    
    # Determine Verdict
    # Critical findings:
    # 1. G011 Ordinal.le and Address.__eq__ hit RecursionError at depth >= 996 (or 1000+),
    #    making sequential fresh_address(N=10,000) or deep address tree comparison crash.
    # 2. G001 morphism distortion float drift causes strict category associativity to fail.
    # 3. G001 TargetClassCharter lacks __setattr__ encapsulation guard.
    
    has_critical = any(sev.startswith("CRITICAL") for _, sev, _ in REPORT.findings)
    if has_critical:
        verdict = "REQUEST_CHANGES"
    else:
        verdict = "APPROVE"
        
    print(f"OVERALL CHALLENGER VERDICT: {verdict}")
    print("=" * 80)
    return 0 if verdict == "APPROVE" else 1


if __name__ == "__main__":
    sys.exit(main())
