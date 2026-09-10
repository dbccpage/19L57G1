"""Tests for Requirement R1: W03 & Target A Operational Enforcement.

Verifies:
1. Typed operational policies: SEPARATED, COLLAPSED, REFLEXIVE.
2. Refusal semantics: PROTECTION_VIOLATION, MALFORMED_OBLIGATION, NO_EDGE, EXHAUSTED.
3. State non-mutation under refusal: state remains completely unmutated.
4. Designated pair validation and active preservation.
5. Counterexample to naive mapping: reflexive entries (boundary stability) do NOT
   falsely fail as naive separation demands.
6. Word machine (Config / step_word) enforcement.
7. Negative control matrices across operation families.
"""

from __future__ import annotations

import unittest

from control import (
    Controlled,
    State,
    build_program,
    fire,
    init,
    run,
    step_det,
    successors,
)
from runner import (
    Config,
    ExecutionError,
    ProtectionKind,
    ProtectionObligation,
    Refusal,
    Terminal,
    check_designated_pair,
    check_obligation,
    eval_word,
    lookup,
    next_of,
    run_word,
    step_word,
)


class TestProtectionPolicies(unittest.TestCase):
    """Unit tests for typed operational protection policies."""

    def setUp(self) -> None:
        # Carrier of size 4: {0, 1, 2, 3}
        # Op 0: permutation (0->1, 1->0, 2->2, 3->3)
        # Op 1: collapse (0->2, 1->2, 2->2, 3->3)
        # Op 2: boundary mover (0->0, 1->1, 2->3, 3->2)
        self.n = 4
        self.op_perm = (1, 0, 2, 3)
        self.op_coll = (2, 2, 2, 3)
        self.op_move = (0, 1, 3, 2)
        self.ctrl = frozenset({(0, 0), (0, 1), (0, 2)})
        self.controlled = Controlled(
            n=self.n,
            ops=(self.op_perm, self.op_coll, self.op_move),
            ctrl=self.ctrl,
        )

    def test_separated_pair_legal_transition(self) -> None:
        """Separated pair (0, 1) remains distinct under permutation op 0."""
        obl = ProtectionObligation(ProtectionKind.SEPARATED, 0, 1)
        # Enable only op 0 at active 0
        c = Controlled(n=self.n, ops=(self.op_perm,), ctrl=frozenset({(0, 0)}))
        s0 = init(c, x=0, fuel=5, protection_obligations=(obl,))

        s1 = step_det(s0)
        self.assertIsInstance(s1, State)
        assert isinstance(s1, State)
        self.assertEqual(s1.active, 1)
        self.assertEqual(s1.clock, 1)
        self.assertEqual(s1.fuel, 4)
        self.assertEqual(s1.tape, (0, 1))
        # Endpoints mapped: 0 -> 1, 1 -> 0, so new pair is (1, 0)
        self.assertEqual(len(s1.protection_obligations), 1)
        self.assertEqual(s1.protection_obligations[0], ProtectionObligation(ProtectionKind.SEPARATED, 1, 0))

    def test_separated_pair_violating_collapse_refusal(self) -> None:
        """Separated pair (0, 1) collapsed by op 1 (0->2, 1->2) triggers refusal."""
        obl = ProtectionObligation(ProtectionKind.SEPARATED, 0, 1)
        # Enable only op 0 which is op_coll in this controlled setting
        c = Controlled(n=self.n, ops=(self.op_coll,), ctrl=frozenset({(0, 0)}))
        s0 = init(c, x=0, fuel=5, protection_obligations=(obl,))

        # Firing directly returns Refusal.PROTECTION_VIOLATION
        res = fire(s0, 0)
        self.assertEqual(res, Refusal.PROTECTION_VIOLATION)

        # step_det returns Terminal.REFUSE (and alias Terminal.REFUSAL)
        term = step_det(s0)
        self.assertEqual(term, Terminal.REFUSE)
        self.assertEqual(term, Terminal.REFUSAL)

        # run halts with (Terminal.REFUSE, s0) leaving state unmutated
        t, s_end = run(s0)
        self.assertEqual(t, Terminal.REFUSE)
        self.assertEqual(s_end, s0)
        self.assertEqual(s_end.active, 0)
        self.assertEqual(s_end.tape, (0,))
        self.assertEqual(s_end.clock, 0)
        self.assertEqual(s_end.fuel, 5)

    def test_reflexive_boundary_stability_accepted(self) -> None:
        """Reflexive entry (2, 2) represents boundary stability: op 0 keeps 2 invariant (2->2)."""
        obl = ProtectionObligation(ProtectionKind.REFLEXIVE, 2, 2)
        c = Controlled(n=self.n, ops=(self.op_perm,), ctrl=frozenset({(0, 0)}))
        s0 = init(c, x=0, fuel=5, protection_obligations=(obl,))

        s1 = step_det(s0)
        self.assertIsInstance(s1, State)
        assert isinstance(s1, State)
        self.assertEqual(s1.active, 1)
        self.assertEqual(s1.clock, 1)
        self.assertEqual(s1.protection_obligations[0], ProtectionObligation(ProtectionKind.REFLEXIVE, 2, 2))

    def test_reflexive_boundary_mutation_refusal(self) -> None:
        """Reflexive entry (2, 2) violated by op_move which moves 2 to 3."""
        obl = ProtectionObligation(ProtectionKind.REFLEXIVE, 2, 2)
        c = Controlled(n=self.n, ops=(self.op_move,), ctrl=frozenset({(0, 0)}))
        s0 = init(c, x=0, fuel=5, protection_obligations=(obl,))

        res = fire(s0, 0)
        self.assertEqual(res, Refusal.PROTECTION_VIOLATION)

        term = step_det(s0)
        self.assertEqual(term, Terminal.REFUSE)

        t, s_end = run(s0)
        self.assertEqual(t, Terminal.REFUSE)
        self.assertEqual(s_end, s0)

    def test_reflexive_counterexample_to_naive_separation(self) -> None:
        """Counterexample to naive mapping: reflexive (x, x) does NOT fail initially.

        A naive engine treating all protection entries as separation demands (u != v)
        would immediately reject (2, 2) as violated on initialization or step 0.
        Our typed policy correctly classifies (2, 2) as REFLEXIVE (boundary stability),
        so it succeeds under authorized operations that leave datum 2 stable.
        """
        obl = ProtectionObligation(ProtectionKind.REFLEXIVE, 2, 2)
        c = Controlled(n=self.n, ops=(self.op_perm,), ctrl=frozenset({(0, 0)}))
        s0 = init(c, x=0, fuel=3, protection_obligations=(obl,))

        # Successfully steps, proving it is NOT rejected as a separation demand
        s1 = step_det(s0)
        self.assertIsInstance(s1, State)

    def test_collapsed_pair_explicit_refusal(self) -> None:
        """Collapsed entry (2, 2) under COLLAPSED policy explicitly refuses protection checks."""
        obl = ProtectionObligation(ProtectionKind.COLLAPSED, 2, 2)
        c = Controlled(n=self.n, ops=(self.op_perm,), ctrl=frozenset({(0, 0)}))
        s0 = init(c, x=0, fuel=3, protection_obligations=(obl,))

        res = fire(s0, 0)
        self.assertEqual(res, Refusal.PROTECTION_VIOLATION)

        term = step_det(s0)
        self.assertEqual(term, Terminal.REFUSE)

        t, s_end = run(s0)
        self.assertEqual(t, Terminal.REFUSE)
        self.assertEqual(s_end, s0)


class TestDesignatedPairEnforcement(unittest.TestCase):
    """Tests for designated pair active invariant preservation and refusal."""

    def setUp(self) -> None:
        self.n = 4
        self.op_swap = (1, 0, 2, 3)
        self.op_ident = (2, 2, 2, 3)

    def test_designated_pair_legal_transition(self) -> None:
        """Designated pair (0, 1) swapped to (1, 0) under legal operation."""
        c = Controlled(n=self.n, ops=(self.op_swap,), ctrl=frozenset({(0, 0)}))
        s0 = init(c, x=0, fuel=4, designated_pair=(0, 1))

        s1 = step_det(s0)
        self.assertIsInstance(s1, State)
        assert isinstance(s1, State)
        self.assertEqual(s1.designated_pair, (1, 0))

    def test_designated_pair_collapse_refusal(self) -> None:
        """Designated pair (0, 1) collapsed by op_ident (0->2, 1->2) triggers refusal."""
        c = Controlled(n=self.n, ops=(self.op_ident,), ctrl=frozenset({(0, 0)}))
        s0 = init(c, x=0, fuel=4, designated_pair=(0, 1))

        res = fire(s0, 0)
        self.assertEqual(res, Refusal.PROTECTION_VIOLATION)

        t, s_end = run(s0)
        self.assertEqual(t, Terminal.REFUSE)
        self.assertEqual(s_end, s0)

    def test_designated_pair_already_collapsed_refusal(self) -> None:
        """Designated pair with identical endpoints (1, 1) refuses stepping."""
        c = Controlled(n=self.n, ops=(self.op_swap,), ctrl=frozenset({(0, 0)}))
        s0 = init(c, x=0, fuel=4, designated_pair=(1, 1))

        res = fire(s0, 0)
        self.assertEqual(res, Refusal.PROTECTION_VIOLATION)

        term = step_det(s0)
        self.assertEqual(term, Terminal.REFUSE)
        self.assertEqual(run(s0)[1], s0)


class TestStateNonMutationMatrix(unittest.TestCase):
    """Negative control matrix verifying state remains completely unmutated across all refusal modes."""

    def test_non_mutation_on_all_refusals(self) -> None:
        """Sweep all refusal variants: EXHAUSTED, NO_EDGE, PROTECTION_VIOLATION, MALFORMED_OBLIGATION."""
        n = 4
        op_legal = (1, 0, 2, 3)
        c = Controlled(n=n, ops=(op_legal,), ctrl=frozenset({(0, 0)}))

        # Case 1: EXHAUSTED (fuel = 0)
        s_exhausted = init(c, x=0, fuel=0)
        res_ex = fire(s_exhausted, 0)
        self.assertEqual(res_ex, Refusal.EXHAUSTED)
        term_ex, s_after_ex = run(s_exhausted)
        self.assertEqual(term_ex, Terminal.EXHAUSTED)
        self.assertEqual(s_after_ex, s_exhausted)

        # Case 2: NO_EDGE (op 5 has no edges)
        s_noedge = init(c, x=0, fuel=5)
        res_ne = fire(s_noedge, 5)
        self.assertEqual(res_ne, Refusal.NO_EDGE)
        nxt_ne = next_of(lambda _: (5,), s_noedge, fire)
        self.assertEqual(nxt_ne, s_noedge)

        # Case 3: PROTECTION_VIOLATION via separated pair collapse
        op_coll = (2, 2, 2, 2)
        c_coll = Controlled(n=n, ops=(op_coll,), ctrl=frozenset({(0, 0)}))
        obl_sep = ProtectionObligation(ProtectionKind.SEPARATED, 0, 1)
        s_viol = init(c_coll, x=0, fuel=5, protection_obligations=(obl_sep,))
        res_pv = fire(s_viol, 0)
        self.assertEqual(res_pv, Refusal.PROTECTION_VIOLATION)
        term_pv, s_after_pv = run(s_viol)
        self.assertEqual(term_pv, Terminal.REFUSE)
        self.assertEqual(s_after_pv, s_viol)
        # Deep field equality check
        self.assertEqual(s_after_pv.active, s_viol.active)
        self.assertEqual(s_after_pv.tape, s_viol.tape)
        self.assertEqual(s_after_pv.clock, s_viol.clock)
        self.assertEqual(s_after_pv.fuel, s_viol.fuel)
        self.assertEqual(s_after_pv.graph, s_viol.graph)
        self.assertEqual(s_after_pv.protection_obligations, s_viol.protection_obligations)
        self.assertEqual(s_after_pv.designated_pair, s_viol.designated_pair)

        # Case 4: MALFORMED_OBLIGATION
        s_mal = State(
            graph=s_viol.graph,
            nops=s_viol.nops,
            active=0,
            tape=(0,),
            clock=0,
            fuel=5,
            protection_obligations=(123,),  # type: ignore # malformed integer instead of ProtectionObligation
        )
        res_mal = fire(s_mal, 0)
        self.assertEqual(res_mal, Refusal.MALFORMED_OBLIGATION)
        nxt_mal = next_of(lambda _: (0,), s_mal, fire)
        self.assertEqual(nxt_mal, s_mal)


class TestConfigWordMachineEnforcement(unittest.TestCase):
    """Tests for Config and step_word enforcing protection obligations."""

    def test_word_machine_separated_success_and_collapse(self) -> None:
        """Word machine enforces obligations along the sequence of operations."""
        # Graph with 2 ops:
        # op 0 (form 3): permutes (0->1, 1->0, 2->2, 3->3)
        # op 1 (form 4): collapses (0->2, 1->2, 2->2, 3->3)
        n = 4
        ops = ((1, 0, 2, 3), (2, 2, 2, 3))
        graph = build_program(n, ops, ())
        obl = ProtectionObligation(ProtectionKind.SEPARATED, 0, 1)

        # Word [0]: legal step
        c0 = Config(
            graph=graph,
            word=(0,),
            active=0,
            output=(0,),
            protection_obligations=(obl,),
            designated_pair=(0, 1),
        )
        c1 = step_word(c0)
        self.assertIsNotNone(c1)
        assert c1 is not None
        self.assertEqual(c1.active, 1)
        self.assertEqual(c1.output, (0, 1))
        self.assertEqual(c1.designated_pair, (1, 0))
        self.assertEqual(c1.protection_obligations, (ProtectionObligation(ProtectionKind.SEPARATED, 1, 0),))

        # Word [1]: collapsing op, must return None
        c_fail = Config(
            graph=graph,
            word=(1,),
            active=0,
            output=(0,),
            protection_obligations=(obl,),
            designated_pair=(0, 1),
        )
        self.assertIsNone(step_word(c_fail))

    def test_word_machine_run_word(self) -> None:
        """run_word halts early and returns None when an obligation is violated."""
        n = 4
        ops = ((1, 0, 2, 3), (2, 2, 2, 3))
        graph = build_program(n, ops, ())
        obl = ProtectionObligation(ProtectionKind.SEPARATED, 0, 1)

        # Word [0, 1] starts legal, then collapses on step 2
        c_seq = Config(
            graph=graph,
            word=(0, 1),
            active=0,
            output=(0,),
            protection_obligations=(obl,),
        )
        self.assertIsNone(run_word(c_seq))


class TestNegativeControlSweepMatrix(unittest.TestCase):
    """Exhaustive parametric matrix sweep across policies and operational behaviors."""

    def test_exhaustive_policy_sweep(self) -> None:
        """Matrix testing of 3 policies x 3 operation behaviors."""
        n = 4
        # Operations:
        # 1. Identity: preserves separation and boundary stability
        op_id = (0, 1, 2, 3)
        # 2. Transposition (0, 1): preserves separation, violates boundary of 0/1, preserves boundary of 2
        op_swap = (1, 0, 2, 3)
        # 3. Complete collapse to 0: violates separation (all collapse), preserves boundary of 0, violates boundary of 2
        op_all0 = (0, 0, 0, 0)

        graph = build_program(n, (op_id, op_swap, op_all0), ())

        # Check SEPARATED (0, 1)
        obl_sep = ProtectionObligation(ProtectionKind.SEPARATED, 0, 1)
        self.assertEqual(check_obligation(graph, 0, obl_sep), ProtectionObligation(ProtectionKind.SEPARATED, 0, 1))
        self.assertEqual(check_obligation(graph, 1, obl_sep), ProtectionObligation(ProtectionKind.SEPARATED, 1, 0))
        self.assertEqual(check_obligation(graph, 2, obl_sep), Refusal.PROTECTION_VIOLATION)

        # Check COLLAPSED (0, 0)
        obl_col = ProtectionObligation(ProtectionKind.COLLAPSED, 0, 0)
        self.assertEqual(check_obligation(graph, 0, obl_col), Refusal.PROTECTION_VIOLATION)
        self.assertEqual(check_obligation(graph, 1, obl_col), Refusal.PROTECTION_VIOLATION)
        self.assertEqual(check_obligation(graph, 2, obl_col), Refusal.PROTECTION_VIOLATION)

        # Check REFLEXIVE (2, 2)
        obl_ref2 = ProtectionObligation(ProtectionKind.REFLEXIVE, 2, 2)
        self.assertEqual(check_obligation(graph, 0, obl_ref2), ProtectionObligation(ProtectionKind.REFLEXIVE, 2, 2))
        self.assertEqual(check_obligation(graph, 1, obl_ref2), ProtectionObligation(ProtectionKind.REFLEXIVE, 2, 2))
        self.assertEqual(check_obligation(graph, 2, obl_ref2), Refusal.PROTECTION_VIOLATION)  # 2 maps to 0

class TestMalformedAndMissingEdges(unittest.TestCase):
    """Tests for malformed obligations and edge exhaustion failures."""

    def test_malformed_obligation_validation_in_constructor(self) -> None:
        """ProtectionObligation constructor rejects negative data, reflexive u!=v, separated u==v."""
        with self.assertRaises(ExecutionError):
            ProtectionObligation(ProtectionKind.SEPARATED, -1, 2)
        with self.assertRaises(ExecutionError):
            ProtectionObligation(ProtectionKind.SEPARATED, 2, 2)
        with self.assertRaises(ExecutionError):
            ProtectionObligation(ProtectionKind.REFLEXIVE, 1, 2)
        with self.assertRaises(ExecutionError):
            ProtectionObligation(ProtectionKind.REFLEXIVE, -1, -1)

    def test_init_bounds_validation(self) -> None:
        """init rejects obligations or designated pairs exceeding carrier bounds."""
        c = Controlled(n=3, ops=((0, 1, 2),), ctrl=frozenset({(0, 0)}))
        # Designated pair out of bounds
        with self.assertRaises(ExecutionError):
            init(c, x=0, fuel=3, designated_pair=(0, 5))
        # Obligation out of bounds
        with self.assertRaises(ExecutionError):
            init(c, x=0, fuel=3, protection_obligations=(ProtectionObligation(ProtectionKind.SEPARATED, 0, 5),))

    def test_missing_edge_on_obligation_endpoint(self) -> None:
        """If graph has no edge leaving an obligation endpoint, returns Refusal.NO_EDGE."""
        # Carrier of 3, but op 0 graph only defined for datum 0 and 1
        edges = frozenset({(3, (0, 1)), (3, (1, 2))})
        obl = ProtectionObligation(ProtectionKind.SEPARATED, 1, 2)  # datum 2 has no edge
        res = check_obligation(edges, 0, obl)
        self.assertEqual(res, Refusal.NO_EDGE)

        # Also for designated pair
        dp_res = check_designated_pair(edges, 0, (1, 2))
        self.assertEqual(dp_res, Refusal.NO_EDGE)

        # Also for reflexive entry
        obl_ref = ProtectionObligation(ProtectionKind.REFLEXIVE, 2, 2)
        ref_res = check_obligation(edges, 0, obl_ref)
        self.assertEqual(ref_res, Refusal.NO_EDGE)


if __name__ == "__main__":
    unittest.main()

