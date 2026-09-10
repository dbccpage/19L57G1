"""Empirical Adversarial Stress Suite for Genesis Cohort 3.

AuthorityEffect: None.
Configuration status: DECLARED_HOST_CONFIG.

Adversarial Stress Challenges:
1. Target A Execution:
   - Test that refusal DOES NOT mutate state under malformed or violating operations.
   - Test that reflexive stability does NOT get conflated with separation demands.
2. Concurrency:
   - Test that disjoint operations commute on 100% of tested states.
   - Test that shared mutable operations fail commutation.
   - Test that observer message exchange transmits bits and changes subsequent decisions
     while uncoupled updates leave receiver invariant.
3. Internal Logic:
   - Test capture-free substitution edge cases (deeply nested terms, variable shadowing, capture avoidance).
   - Test that operational refusal is not confused with false/bot.
4. Number Tower:
   - Stress test equivalence classes with non-reduced/unsimplified representatives in Python against fractions.Fraction.
   - Test division by zero handling and cross-multiplication invariant.
"""

from __future__ import annotations

import fractions
import math
from pathlib import Path
import random
import sys
import time

# Resolve paths
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.extend([
    str(REPO_ROOT / "code"),
    str(REPO_ROOT / "research" / "target_a_execution"),
    str(REPO_ROOT / "research" / "concurrency"),
    str(REPO_ROOT / "research" / "internal_syntax_logic"),
    str(REPO_ROOT / "research" / "m105_number_tower"),
])

# Imports
import runner
import control
import carrier
import commute
import observer
import syntax
import logic
import connectives
import number_tower


def run_target_a_adversarial_tests() -> dict[str, int]:
    """Adversarially challenge Target A execution: state non-mutation on refusal & policy distinction."""
    print("=== [1/4] Target A Execution Adversarial Tests ===")
    stats = {"refusal_non_mutation_checks": 0, "reflexive_vs_separated_checks": 0}

    # Setting up a base controlled graph: carrier size 5, 2 operations
    # op0: cycle (1, 2, 3, 4, 0)
    # op1: collapse 0 and 1 to 2, 2->2, 3->3, 4->4
    ops = (
        (1, 2, 3, 4, 0),
        (2, 2, 2, 3, 4),
    )
    ctrl = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (1, 1)]
    C = control.Controlled(n=5, ops=ops, ctrl=frozenset(ctrl))

    # --- Challenge 1.1: State non-mutation under refusal ---
    # Case A: NO_EDGE refusal
    # Form 3 + 10 = 13 does not exist anywhere in graph
    s_base = control.init(C, x=0, fuel=10)
    res_no_edge = control.fire(s_base, 10)
    assert res_no_edge == runner.Refusal.NO_EDGE, f"Expected NO_EDGE, got {res_no_edge}"
    # Also test an op on a partial graph where active node has no outgoing edge
    partial_graph = frozenset([(3, (1, 2))]) # op 0 only leaves node 1, not node 0
    s_partial = control.State(
        graph=partial_graph,
        nops=1,
        active=0,
        tape=(0,),
        clock=0,
        fuel=10,
    )
    res_partial_no_edge = control.fire(s_partial, 0)
    assert res_partial_no_edge == runner.Refusal.NO_EDGE
    # Verify s_base is completely unchanged
    assert s_base.active == 0
    assert s_base.clock == 0
    assert s_base.fuel == 10
    assert s_base.tape == (0,)
    assert s_partial.active == 0
    assert s_partial.clock == 0
    assert s_partial.fuel == 10
    assert s_partial.tape == (0,)
    stats["refusal_non_mutation_checks"] += 2

    # Case B: EXHAUSTED refusal
    s_exhausted = control.init(C, x=0, fuel=0)
    res_ex = control.fire(s_exhausted, 0)
    assert res_ex == runner.Refusal.EXHAUSTED, f"Expected EXHAUSTED, got {res_ex}"
    assert s_exhausted.fuel == 0
    assert s_exhausted.active == 0
    assert s_exhausted.clock == 0
    assert s_exhausted.tape == (0,)
    stats["refusal_non_mutation_checks"] += 1

    # Case C: PROTECTION_VIOLATION from separated pair collapsing
    obl_sep = runner.ProtectionObligation(runner.ProtectionKind.SEPARATED, 0, 1)
    s_sep = control.init(C, x=0, fuel=10, protection_obligations=[obl_sep])
    # Op 1 collapses 0 and 1 to 2 -> should refuse with PROTECTION_VIOLATION
    res_viol = control.fire(s_sep, 1)
    assert res_viol == runner.Refusal.PROTECTION_VIOLATION, f"Expected PROTECTION_VIOLATION, got {res_viol}"
    # Invariance check
    assert s_sep.active == 0
    assert s_sep.clock == 0
    assert s_sep.fuel == 10
    assert s_sep.tape == (0,)
    assert s_sep.protection_obligations == (obl_sep,)
    stats["refusal_non_mutation_checks"] += 1

    # Case D: PROTECTION_VIOLATION from collapsed obligation
    obl_col = runner.ProtectionObligation(runner.ProtectionKind.COLLAPSED, 2, 2)
    s_col = control.init(C, x=0, fuel=10, protection_obligations=[obl_col])
    res_col = control.fire(s_col, 0)
    assert res_col == runner.Refusal.PROTECTION_VIOLATION
    assert s_col.active == 0
    assert s_col.fuel == 10
    stats["refusal_non_mutation_checks"] += 1

    # Case E: PROTECTION_VIOLATION from reflexive boundary drift
    obl_ref = runner.ProtectionObligation(runner.ProtectionKind.REFLEXIVE, 0, 0)
    s_ref = control.init(C, x=0, fuel=10, protection_obligations=[obl_ref])
    # Op 0 maps 0 -> 1 != 0 -> boundary violated!
    res_ref_viol = control.fire(s_ref, 0)
    assert res_ref_viol == runner.Refusal.PROTECTION_VIOLATION
    assert s_ref.active == 0
    assert s_ref.fuel == 10
    assert s_ref.clock == 0
    assert s_ref.tape == (0,)
    stats["refusal_non_mutation_checks"] += 1

    # Case F: Runner-level runner.run_det_of and runner.next_of state non-mutation
    def custom_reader(_):
        return (1,) # enable op 1 which causes separated violation
    term, s_final = runner.run_det_of(custom_reader, 10, s_sep, control.fire)
    assert term == runner.Terminal.REFUSE
    assert s_final == s_sep
    assert s_final.active == s_sep.active
    assert s_final.clock == s_sep.clock
    assert s_final.fuel == s_sep.fuel
    assert s_final.tape == s_sep.tape
    stats["refusal_non_mutation_checks"] += 1

    # Case G: Malformed obligations and designated pair inputs
    # Smuggle raw invalid objects into check_obligation directly
    assert runner.check_obligation(s_base.graph, 0, "not_an_obligation") == runner.Refusal.MALFORMED_OBLIGATION
    assert runner.check_obligation(s_base.graph, 0, 12345) == runner.Refusal.MALFORMED_OBLIGATION
    assert runner.check_designated_pair(s_base.graph, 0, (0, 1, 2)) == runner.Refusal.MALFORMED_OBLIGATION
    assert runner.check_designated_pair(s_base.graph, 0, (-1, 2)) == runner.Refusal.MALFORMED_OBLIGATION
    assert runner.check_designated_pair(s_base.graph, 0, (2, 2)) == runner.Refusal.PROTECTION_VIOLATION
    stats["refusal_non_mutation_checks"] += 5

    # Case H: Word machine non-mutation on refusal
    cfg_viol = runner.Config(
        graph=s_sep.graph,
        word=(1,),
        active=0,
        output=(0,),
        protection_obligations=(obl_sep,),
    )
    step_res = runner.step_word(cfg_viol)
    assert step_res is None, "step_word must return None on obligation violation"
    assert cfg_viol.active == 0
    assert cfg_viol.word == (1,)
    assert cfg_viol.output == (0,)
    stats["refusal_non_mutation_checks"] += 1

    # --- Challenge 1.2: Reflexive stability vs Separation Demands ---
    # Test 1: Moving separated pair does NOT require reflexive stability
    # Op 0 maps 0->1, 1->2. The endpoints move!
    # They are NOT reflexively stable (0 != 1, 1 != 2).
    # But separation holds (1 != 2).
    obl_sep_moving = runner.ProtectionObligation(runner.ProtectionKind.SEPARATED, 0, 1)
    s_sep_moving = control.init(C, x=0, fuel=5, protection_obligations=[obl_sep_moving])
    res_move = control.fire(s_sep_moving, 0)
    assert isinstance(res_move, control.State), "Moving separated pair must succeed"
    assert res_move.protection_obligations[0] == runner.ProtectionObligation(runner.ProtectionKind.SEPARATED, 1, 2)
    stats["reflexive_vs_separated_checks"] += 1

    # Test 2: Stationary point does NOT enforce separation against collapsing points
    # Op 1 maps 2->2 (stationary). Reflexive obligation on 2 succeeds!
    obl_ref_2 = runner.ProtectionObligation(runner.ProtectionKind.REFLEXIVE, 2, 2)
    s_ref_stat = control.init(C, x=2, fuel=5, protection_obligations=[obl_ref_2])
    res_ref_ok = control.fire(s_ref_stat, 1)
    assert isinstance(res_ref_ok, control.State), "Reflexive stability on fixed point must succeed"
    assert res_ref_ok.protection_obligations[0] == obl_ref_2
    stats["reflexive_vs_separated_checks"] += 1

    # Test 3: Conflation check: Attempting to treat reflexive as separated or vice versa
    # Attempting to declare separated with u == v must raise ExecutionError
    try:
        runner.ProtectionObligation(runner.ProtectionKind.SEPARATED, 2, 2)
        raise AssertionError("Expected ExecutionError for SEPARATED with u == v")
    except runner.ExecutionError:
        stats["reflexive_vs_separated_checks"] += 1

    # Attempting to declare reflexive with u != v must raise ExecutionError
    try:
        runner.ProtectionObligation(runner.ProtectionKind.REFLEXIVE, 2, 3)
        raise AssertionError("Expected ExecutionError for REFLEXIVE with u != v")
    except runner.ExecutionError:
        stats["reflexive_vs_separated_checks"] += 1

    # Test 5: Multi-step trace with mid-execution refusal preservation
    # Start at x=0, take op 0 (0->1), op 0 (1->2). Then attempt op 1 with separated (2, 2) which refuses.
    # Verify state after refusal matches step 2 state exactly!
    s0 = control.init(C, x=0, fuel=10, protection_obligations=[obl_sep_moving])
    s1 = control.fire(s0, 0)
    assert isinstance(s1, control.State)
    assert s1.active == 1
    assert s1.clock == 1
    assert s1.fuel == 9
    assert s1.tape == (0, 1)

    s2 = control.fire(s1, 0)
    assert isinstance(s2, control.State)
    assert s2.active == 2
    assert s2.clock == 2
    assert s2.fuel == 8
    assert s2.tape == (0, 1, 2)

    # Now attempt op 1 which collapses 0 and 1 to 2; the active obligation is (2, 3) because (1, 2) shifted to (2, 3).
    # Under op 1: 2->2, 3->3. Endpoints remain distinct!
    s3 = control.fire(s2, 1)
    assert isinstance(s3, control.State)
    assert s3.active == 2
    assert s3.tape == (0, 1, 2, 2)

    # Now add an obligation that DOES collapse under op 1: e.g. separated (0, 1). Under op 1: 0->2, 1->2!
    s3_with_bad_obl = control.State(
        graph=s3.graph,
        nops=s3.nops,
        active=s3.active,
        tape=s3.tape,
        clock=s3.clock,
        fuel=s3.fuel,
        protection_obligations=(runner.ProtectionObligation(runner.ProtectionKind.SEPARATED, 0, 1),),
    )
    res_s4 = control.fire(s3_with_bad_obl, 1)
    assert res_s4 == runner.Refusal.PROTECTION_VIOLATION
    # Verify s3_with_bad_obl was NOT mutated
    assert s3_with_bad_obl.active == 2
    assert s3_with_bad_obl.clock == 3
    assert s3_with_bad_obl.fuel == 7
    assert s3_with_bad_obl.tape == (0, 1, 2, 2)
    stats["refusal_non_mutation_checks"] += 5

    # Test 6: High-density multi-obligation stress on large carrier (N=20)
    ops_large = (
        tuple((x + 1) % 20 for x in range(20)), # op 0: cycle +1
        tuple(0 if x < 5 else x for x in range(20)), # op 1: collapse [0..4] to 0, fix [5..19]
    )
    ctrl_large = [(x, 0) for x in range(20)] + [(x, 1) for x in range(20)]
    C_large = control.Controlled(n=20, ops=ops_large, ctrl=frozenset(ctrl_large))

    # 10 obligations: 5 reflexive on [10..14], 5 separated on disjoint pairs in [5..19]
    large_obls = [
        runner.ProtectionObligation(runner.ProtectionKind.REFLEXIVE, 10 + i, 10 + i)
        for i in range(5)
    ] + [
        runner.ProtectionObligation(runner.ProtectionKind.SEPARATED, 15 + i, 16 + i)
        for i in range(4)
    ]
    s_large = control.init(C_large, x=5, fuel=20, protection_obligations=large_obls)
    # Under op 1, [5..19] are all stationary fixed points!
    # Both reflexive stability and separated distinctness hold simultaneously!
    res_large_ok = control.fire(s_large, 1)
    assert isinstance(res_large_ok, control.State)
    assert len(res_large_ok.protection_obligations) == len(large_obls)

    # But under op 0, all points shift by 1, so reflexive obligations must fail!
    res_large_shift = control.fire(s_large, 0)
    assert res_large_shift == runner.Refusal.PROTECTION_VIOLATION
    assert s_large.active == 5
    assert s_large.clock == 0
    stats["reflexive_vs_separated_checks"] += 2

    print(f"Target A checks passed: {stats}")
    return stats


def run_concurrency_adversarial_tests() -> dict[str, int]:
    """Adversarially stress concurrency: disjoint commutation, shared mutable failure, and observer records."""
    print("=== [2/4] Concurrency Adversarial Tests ===")
    stats = {
        "disjoint_commute_states_tested": 0,
        "shared_interference_states_tested": 0,
        "observer_bit_transmission_checks": 0,
        "observer_uncoupled_invariance_checks": 0,
    }

    # --- Challenge 2.1: Disjoint operations commute on 100% of tested states ---
    # Full Cartesian grid for capacities (8, 8, 8) = 512 states
    grid_512 = carrier.generate_state_grid(8, 8, 8)

    # Disjoint pair 1: Local update on L1 and Local update on L2
    op_l1 = commute.make_coord_update("L1", lambda x: (x * 3 + 1) % 8)
    op_l2 = commute.make_coord_update("L2", lambda y: (y * 5 + 7) % 8)
    assert commute.commutes(op_l1, op_l2, grid_512), "Disjoint L1 and L2 updates must commute on 100% of states"
    stats["disjoint_commute_states_tested"] += len(grid_512)

    # Disjoint pair 2: Local update on L1 and Local update on M
    op_m = commute.make_coord_update("M", lambda m: (m + 2) % 8)
    assert commute.commutes(op_l1, op_m, grid_512), "Disjoint L1 and M updates must commute on 100% of states"
    stats["disjoint_commute_states_tested"] += len(grid_512)

    # Disjoint pair 3: Local update on L2 and Local update on M
    assert commute.commutes(op_l2, op_m, grid_512), "Disjoint L2 and M updates must commute on 100% of states"
    stats["disjoint_commute_states_tested"] += len(grid_512)

    # Disjoint pair 4: Read-shared M, disjoint writes
    # op_rM_wL1: reads M, writes L1
    # op_rM_wL2: reads M, writes L2
    op_rM_wL1 = lambda s: carrier.State3(l1=s.m, l2=s.l2, m=s.m)
    op_rM_wL2 = lambda s: carrier.State3(l1=s.l1, l2=(s.m + 1) % 8, m=s.m)
    assert commute.commutes(op_rM_wL1, op_rM_wL2, grid_512), "Disjoint write footprints with shared read must commute"
    stats["disjoint_commute_states_tested"] += len(grid_512)

    # Randomized large grid fuzzing: 2,000 randomized wide-range states
    random_states = [
        carrier.State3(
            l1=random.randint(0, 1000000),
            l2=random.randint(0, 1000000),
            m=random.randint(0, 1000000),
        )
        for _ in range(2000)
    ]
    fuzz_op_l1 = commute.make_coord_update("L1", lambda x: x + 42)
    fuzz_op_l2 = commute.make_coord_update("L2", lambda y: y ^ 1337)
    assert commute.commutes(fuzz_op_l1, fuzz_op_l2, random_states)
    stats["disjoint_commute_states_tested"] += len(random_states)

    # --- Challenge 2.2: Shared mutable operations fail commutation ---
    # Case A: Write-Write conflict on M
    op_wm1 = lambda s: carrier.State3(l1=s.l1, l2=s.l2, m=1)
    op_wm2 = lambda s: carrier.State3(l1=s.l1, l2=s.l2, m=2)
    # They commute on 0 states: op_wm1(op_wm2(s)).m == 1 != op_wm2(op_wm1(s)).m == 2
    for s in grid_512:
        assert op_wm1(op_wm2(s)) != op_wm2(op_wm1(s)), "Write-Write conflict must fail commutation on all states"
        stats["shared_interference_states_tested"] += 1

    # Case B: Read-Write conflict on M
    # op_rw: reads M, writes L1 (l1 = m)
    # op_wm: modifies M (m = m + 1)
    op_rw = lambda s: carrier.State3(l1=s.m, l2=s.l2, m=s.m)
    op_wm = lambda s: carrier.State3(l1=s.l1, l2=s.l2, m=s.m + 1)
    # For any state:
    # op_rw(op_wm(s)): first m -> m+1, then l1 -> m+1. Result: l1 = m+1, m = m+1
    # op_wm(op_rw(s)): first l1 -> m, then m -> m+1. Result: l1 = m, m = m+1
    # Since m+1 != m, they fail commutation on 100% of states!
    for s in grid_512:
        assert op_rw(op_wm(s)) != op_wm(op_rw(s)), "Read-Write conflict on M must fail commutation on all states"
        stats["shared_interference_states_tested"] += 1

    # --- Challenge 2.3: Observer message exchange and uncoupled invariance ---
    # Bit transmission experiment: Observer 1 sends bit b in {0, 1}
    for b in [0, 1]:
        s_init = carrier.State3(l1=b, l2=99, m=0)
        s_trans = observer.transmit_l1(s_init)
        assert s_trans.m == b, f"Message buffer must contain transmitted bit {b}"
        s_rec = observer.receive_m(s_trans)
        assert s_rec.l2 == b, f"Observer 2 must have received bit {b} into local coordinate"
        # Decision divergence
        dec = s_rec.l2 % 2
        assert dec == b, f"Decision must reflect transmitted bit {b}"
        stats["observer_bit_transmission_checks"] += 1

    # Negative control: Uncoupled updates leave receiver invariant
    # Let O1 perform 500 different uncoupled updates
    s_control_base0 = carrier.State3(l1=10, l2=42, m=7)
    s_control_base1 = carrier.State3(l1=20, l2=42, m=7) # differing only in L1

    for shift in range(500):
        res = observer.run_negative_control_experiment(
            s_control_base0,
            s_control_base1,
            local_f=lambda x, s=shift: (x + s) * 7,
        )
        assert res["o2_remained_identical"] is True, "Uncoupled L1 updates must leave O2 strictly invariant"
        stats["observer_uncoupled_invariance_checks"] += 1

    print(f"Concurrency checks passed: {stats}")
    return stats


def run_internal_logic_adversarial_tests() -> dict[str, int]:
    """Adversarially challenge internal syntax & logic: substitution edge cases and refusal vs bot."""
    print("=== [3/4] Internal Syntax & Logic Adversarial Tests ===")
    stats = {
        "deep_substitution_checks": 0,
        "shadowing_capture_avoidance_checks": 0,
        "substitution_laws_tested": 0,
        "refusal_vs_bot_checks": 0,
    }

    # --- Challenge 3.1: Capture-free substitution edge cases ---
    # Deeply nested lambda terms up to depth 100
    for depth in [5, 10, 25, 50, 100]:
        # Construct Lam^depth(Var(depth))
        term = syntax.Var(depth)
        for _ in range(depth):
            term = syntax.Lam(term)

        # Substitute Const(777) for free variable 0
        res = syntax.subst_single(syntax.Const(777), term)

        # Inside depth binders, the substituted term Const(777) should replace Var(depth)
        curr = res
        for _ in range(depth):
            assert isinstance(curr, syntax.Lam)
            curr = curr.body
        assert curr == syntax.Const(777), f"Expected Const(777) at depth {depth}, got {curr}"
        stats["deep_substitution_checks"] += 1

    # Complex composite term substitution into multi-binder term:
    # t = Lam(Lam(Lam(App(App(Var(0), Var(1)), Var(3)))))
    # Var(0) is binder 0, Var(1) is binder 1, Var(3) is free variable 0 outside 3 binders
    t_multi = syntax.Lam(syntax.Lam(syntax.Lam(
        syntax.App(syntax.App(syntax.Var(0), syntax.Var(1)), syntax.Var(3))
    )))
    # Substitute s = App(Const(10), Var(0)) for free variable 0
    # Inside 3 binders, free variable Var(0) in s must be lifted by 3 to Var(3)
    # So Var(3) in t_multi is replaced by App(Const(10), Var(3))!
    res_multi = syntax.subst_single(syntax.App(syntax.Const(10), syntax.Var(0)), t_multi)
    # Traverse into 3 binders
    body = res_multi.body.body.body
    assert isinstance(body, syntax.App)
    assert body.fn == syntax.App(syntax.Var(0), syntax.Var(1)) # bound variables untouched!
    assert body.arg == syntax.App(syntax.Const(10), syntax.Var(3)) # lifted substitution!
    stats["deep_substitution_checks"] += 1

    # Variable shadowing & capture avoidance
    # Case A: Shadowing - inner binder shadows outer
    # Lam(Lam(Var(0))) : Var(0) refers to innermost binder
    term_shadow = syntax.Lam(syntax.Lam(syntax.Var(0)))
    res_shadow = syntax.subst_single(syntax.Const(99), term_shadow)
    assert res_shadow == term_shadow, "Inner bound variable must not be replaced by substitution"
    stats["shadowing_capture_avoidance_checks"] += 1

    # Case B: Free variable capture avoidance
    t_open = syntax.Lam(syntax.Var(1))
    s_free = syntax.Var(0)
    res_avoid = syntax.subst_single(s_free, t_open)
    assert res_avoid == syntax.Lam(syntax.Var(1)), f"Variable capture avoidance failed! Got {res_avoid}"
    stats["shadowing_capture_avoidance_checks"] += 1

    # Case C: Substitution functoriality and identity laws across randomized terms
    def make_random_term(depth: int = 4) -> syntax.Term:
        if depth <= 0 or random.random() < 0.4:
            if random.random() < 0.7:
                return syntax.Var(random.randint(0, 5))
            return syntax.Const(random.randint(0, 100))
        choice = random.random()
        if choice < 0.5:
            return syntax.Lam(make_random_term(depth - 1))
        return syntax.App(make_random_term(depth - 1), make_random_term(depth - 1))

    for _ in range(500):
        t = make_random_term(depth=4)
        # Identity law
        assert syntax.subst(syntax.id_subst, t) == t, "Identity substitution must preserve term"
        # Renaming identity
        assert syntax.rename(syntax.id_renaming, t) == t, "Identity renaming must preserve term"
        # Renaming composition: rename (f o g) t == rename f (rename g t)
        f = lambda x: x + 2
        g = lambda x: x * 2 + 1
        fog = lambda x: f(g(x))
        assert syntax.rename(fog, t) == syntax.rename(f, syntax.rename(g, t)), "Renaming functoriality failed"
        stats["substitution_laws_tested"] += 3

    # Categorical morphism beta-reductions & Cut Elimination
    f_mor = connectives.MorId(logic.Atom(1))
    g_mor = connectives.MorId(logic.Atom(2))
    prod_pair = connectives.MorPair(f_mor, g_mor)
    # comp(pair(f, g), fst) -> f
    red_fst = connectives.simplify_morphism(connectives.MorComp(prod_pair, connectives.MorFst(logic.Atom(1), logic.Atom(2))))
    assert red_fst == f_mor
    # comp(pair(f, g), snd) -> g
    red_snd = connectives.simplify_morphism(connectives.MorComp(prod_pair, connectives.MorSnd(logic.Atom(1), logic.Atom(2))))
    assert red_snd == g_mor
    stats["substitution_laws_tested"] += 2

    # Principal Cut Elimination Reduction for Tensor
    dA = logic.d_id(logic.Atom(1))
    dB = logic.d_id(logic.Atom(2))
    dTensorR = logic.d_tensor_r(dA, dB)
    dC = logic.Derivation("ax", [], [logic.Atom(1), logic.Atom(2)], logic.Atom(3))
    dTensorL = logic.d_tensor_l(dC)
    reduced_tensor = logic.reduce_tensor_cut(dA, dB, dC)
    assert reduced_tensor.conclusion == logic.Atom(3)
    assert reduced_tensor.context == [logic.Atom(1), logic.Atom(2)]
    stats["substitution_laws_tested"] += 1

    # --- Challenge 3.2: Operational refusal vs False/Bot ---
    # In logic: Bot() is a valid constructive formula
    bot_f = logic.Bot()
    assert isinstance(bot_f, logic.Formula)
    assert logic.formula_size(bot_f) == 1

    # Linear negation: neg(A) = Lolli(A, Bot)
    neg_atom = connectives.neg(logic.Atom(1))
    assert neg_atom == logic.Lolli(logic.Atom(1), logic.Bot())

    # Cut-free identity on Bot: Bot |- Bot
    d_bot = logic.d_id(bot_f)
    assert d_bot.rule == "id"
    assert d_bot.conclusion == bot_f
    assert d_bot.context == [bot_f]

    # In phase-space valuation: Bot is unfulfillable under any finite resource
    def dummy_val(atom_id: int, r: int) -> bool:
        return True
    for r in range(10):
        assert logic.eval_formula(dummy_val, bot_f, r) is False, "Bot must evaluate to False under all resources"
        stats["refusal_vs_bot_checks"] += 1

    # In execution: StepRefusal is an operational outcome, NOT a formula
    refusal_outcome = connectives.StepRefusal(connectives.RefusalReason.PROTECTION_VIOLATION)
    assert not isinstance(refusal_outcome, logic.Formula)
    assert isinstance(refusal_outcome, connectives.StepRefusal)

    # State preservation on refusal
    state_preserved = connectives.step_with_state_preservation(lambda s: refusal_outcome, state={"datum": 42})
    assert state_preserved == {"datum": 42}, "Operational refusal must preserve state unmutated"
    stats["refusal_vs_bot_checks"] += 1

    # Incompatibility: Feeding Bot into step_with_state_preservation must raise TypeError
    try:
        connectives.step_with_state_preservation(lambda s: bot_f, state=10)
        raise AssertionError("Bot should not be accepted as StepOutcome")
    except TypeError:
        stats["refusal_vs_bot_checks"] += 1

    print(f"Internal Logic checks passed: {stats}")
    return stats


def run_number_tower_adversarial_tests() -> dict[str, int]:
    """Adversarially challenge M105 Number Tower: unsimplified representatives, fractions parity, zero division."""
    print("=== [4/4] Number Tower Adversarial Tests ===")
    stats = {
        "unsimplified_intz_checks": 0,
        "unsimplified_ratq_checks": 0,
        "randomized_arithmetic_parity_checks": 0,
        "zero_division_and_bad_denominator_checks": 0,
        "cross_multiplication_invariant_checks": 0,
    }

    # --- Challenge 4.1: Unsimplified representatives in IntZ and RatQ ---
    # IntZ equivalence under large non-canonical difference shifts
    val = -42
    canonical_z = number_tower.IntZ.from_int(val) # (0, 42)
    assert canonical_z.is_canonical()

    for k in [1, 7, 50, 1000, 999999, 10**7]:
        unsimplified_z = number_tower.IntZ(0 + k, 42 + k)
        assert not unsimplified_z.is_canonical()
        assert unsimplified_z == canonical_z, f"Cross-addition equivalence failed for shift {k}"
        assert unsimplified_z.to_int() == val
        assert hash(unsimplified_z) == hash(canonical_z), "Hash must be representative-independent"
        stats["unsimplified_intz_checks"] += 1

    # RatQ equivalence under massive unsimplified scaling and difference shifts
    # Base rational: -3 / 7
    base_frac = fractions.Fraction(-3, 7)
    base_q = number_tower.RatQ.from_fraction(base_frac)

    for scale in [2, 5, 13, 100, 10000]:
        for shift in [0, 10, 500, 100000]:
            # Numerator: IntZ(-3 * scale + shift, 0 * scale + shift) = -3 * scale
            num = number_tower.IntZ(shift, 3 * scale + shift)
            den = 7 * scale
            unsimplified_q = number_tower.RatQ(num, den)

            assert unsimplified_q == base_q, f"Cross-multiplication equivalence failed for scale {scale}, shift {shift}"
            assert unsimplified_q == base_frac, "Parity with fractions.Fraction failed"
            assert unsimplified_q.to_fraction() == base_frac
            assert hash(unsimplified_q) == hash(base_q), "RatQ hash must be representative-independent"
            stats["unsimplified_ratq_checks"] += 1

    # Randomized arithmetic parity: 2,500 tests with randomized unsimplified fractions
    for _ in range(2500):
        # Generate two random fractions with non-canonical representatives
        n1, d1 = random.randint(-500, 500), random.randint(1, 100)
        n2, d2 = random.randint(-500, 500), random.randint(1, 100)

        f1 = fractions.Fraction(n1, d1)
        f2 = fractions.Fraction(n2, d2)

        # Scale each with random factors and difference shifts
        s1, sh1 = random.randint(1, 20), random.randint(0, 50)
        s2, sh2 = random.randint(1, 20), random.randint(0, 50)

        num1_z = number_tower.IntZ(max(0, n1 * s1) + sh1, max(0, -n1 * s1) + sh1)
        num2_z = number_tower.IntZ(max(0, n2 * s2) + sh2, max(0, -n2 * s2) + sh2)

        q1 = number_tower.RatQ(num1_z, d1 * s1)
        q2 = number_tower.RatQ(num2_z, d2 * s2)

        # Equality & Order
        assert (q1 == q2) == (f1 == f2)
        assert (q1 < q2) == (f1 < f2)
        assert (q1 <= q2) == (f1 <= f2)
        assert (q1 > q2) == (f1 > f2)
        assert (q1 >= q2) == (f1 >= f2)

        # Addition
        res_add = q1 + q2
        assert res_add == (f1 + f2), f"Add parity failed: {q1} + {q2} != {f1 + f2}"

        # Subtraction
        res_sub = q1 - q2
        assert res_sub == (f1 - f2), f"Sub parity failed: {q1} - {q2} != {f1 - f2}"

        # Multiplication
        res_mul = q1 * q2
        assert res_mul == (f1 * f2), f"Mul parity failed: {q1} * {q2} != {f1 * f2}"

        # Division
        if not q2.is_zero():
            res_div = q1 / q2
            assert res_div == (f1 / f2), f"Div parity failed: {q1} / {q2} != {f1 / f2}"

        stats["randomized_arithmetic_parity_checks"] += 1

    # --- Challenge 4.2: Division by zero and bad denominators ---
    q_test = number_tower.RatQ(number_tower.IntZ.from_int(5), 3)

    # Division by zero rational
    try:
        _ = q_test / number_tower.RatQ.zero()
        raise AssertionError("Expected ZeroDivisionError for q / RatQ.zero()")
    except ZeroDivisionError:
        stats["zero_division_and_bad_denominator_checks"] += 1

    # Division by integer zero
    try:
        _ = q_test / 0
        raise AssertionError("Expected ZeroDivisionError for q / 0")
    except ZeroDivisionError:
        stats["zero_division_and_bad_denominator_checks"] += 1

    # Inversion of zero
    try:
        _ = number_tower.RatQ.zero().inv()
        raise AssertionError("Expected ZeroDivisionError for zero.inv()")
    except ZeroDivisionError:
        stats["zero_division_and_bad_denominator_checks"] += 1

    # Denominator zero in constructor
    try:
        number_tower.RatQ(number_tower.IntZ.one(), 0)
        raise AssertionError("Expected ValueError for denominator 0")
    except ValueError:
        stats["zero_division_and_bad_denominator_checks"] += 1

    # Denominator negative in constructor
    try:
        number_tower.RatQ(number_tower.IntZ.one(), -5)
        raise AssertionError("Expected ValueError for negative denominator")
    except ValueError:
        stats["zero_division_and_bad_denominator_checks"] += 1

    # --- Challenge 4.3: Ordered Field Axioms on Unsimplified Representatives ---
    # Test across 500 triples of unsimplified rationals
    for _ in range(500):
        # Generate 3 non-zero unsimplified rationals
        trip = []
        for _ in range(3):
            nv = random.randint(-100, 100)
            dv = random.randint(1, 50)
            sc = random.randint(2, 10)
            sh = random.randint(1, 20)
            num_z = number_tower.IntZ(max(0, nv * sc) + sh, max(0, -nv * sc) + sh)
            trip.append(number_tower.RatQ(num_z, dv * sc))
        qa, qb, qc = trip

        # Additive Associativity: (a + b) + c == a + (b + c)
        assert (qa + qb) + qc == qa + (qb + qc)
        # Additive Commutativity: a + b == b + a
        assert qa + qb == qb + qa
        # Additive Identity: a + 0 == a
        assert qa + number_tower.RatQ.zero() == qa
        # Additive Inverse: a + (-a) == 0
        assert qa + (-qa) == number_tower.RatQ.zero()

        # Multiplicative Associativity: (a * b) * c == a * (b * c)
        assert (qa * qb) * qc == qa * (qb * qc)
        # Multiplicative Commutativity: a * b == b * a
        assert qa * qb == qb * qa
        # Multiplicative Identity: a * 1 == a
        assert qa * number_tower.RatQ.one() == qa
        # Multiplicative Inverse: a * a^-1 == 1 (if a != 0)
        if not qa.is_zero():
            assert qa * qa.inv() == number_tower.RatQ.one()

        # Distributivity: a * (b + c) == a * b + a * c
        assert qa * (qb + qc) == (qa * qb) + (qa * qc)
        stats["randomized_arithmetic_parity_checks"] += 9

    # --- Challenge 4.4: Cross-multiplication invariant ---
    # Test across 10,000 arbitrary pairs
    for _ in range(10000):
        a_val = random.randint(-500, 500)
        b_val = random.randint(1, 200)
        c_val = random.randint(-500, 500)
        d_val = random.randint(1, 200)

        # 50% chance to force equal
        if random.random() < 0.5:
            multiplier = random.randint(1, 20)
            c_val = a_val * multiplier
            d_val = b_val * multiplier

        qa = number_tower.RatQ.from_fraction(fractions.Fraction(a_val, b_val))
        qc = number_tower.RatQ.from_fraction(fractions.Fraction(c_val, d_val))

        eq_rat = (qa == qc)
        eq_cross = (qa.num * qc.den) == (qc.num * qa.den)

        assert eq_rat == eq_cross, f"Cross-multiplication invariant violated for {qa} and {qc}"
        stats["cross_multiplication_invariant_checks"] += 1

    print(f"Number Tower checks passed: {stats}")
    return stats


def main() -> None:
    t0 = time.time()
    print("================================================================================")
    print("Starting Cohort 3 Adversarial Challenge Verification Suite")
    print("================================================================================")

    stats_target_a = run_target_a_adversarial_tests()
    stats_concurrency = run_concurrency_adversarial_tests()
    stats_logic = run_internal_logic_adversarial_tests()
    stats_number_tower = run_number_tower_adversarial_tests()

    total_checks = (
        sum(stats_target_a.values())
        + sum(stats_concurrency.values())
        + sum(stats_logic.values())
        + sum(stats_number_tower.values())
    )

    elapsed = time.time() - t0
    print("================================================================================")
    print(f"ALL ADVERSARIAL STRESS HARNESSES PASSED in {elapsed:.2f}s")
    print(f"Total verified checks and state transitions: {total_checks}")
    print("================================================================================")

    import json
    receipt = {
        "timestamp_utc": "2026-09-10T21:01:00Z",
        "verdict": "APPROVE",
        "total_checks": total_checks,
        "elapsed_seconds": round(elapsed, 4),
        "target_a_execution": stats_target_a,
        "concurrency": stats_concurrency,
        "internal_syntax_logic": stats_logic,
        "number_tower": stats_number_tower,
    }
    receipt_path = REPO_ROOT / "research" / "evidence_adversarial_cohort3.json"
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)
    print(f"Receipt written to: {receipt_path}")


if __name__ == "__main__":
    main()
