"""Comprehensive test suite for M100–M103 Internal Syntax, Operational Logic & Connectives.

AuthorityEffect: None.
"""

import pytest
import sys
from pathlib import Path

# Add package root to sys.path
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from syntax import (
    Var, Lam, App, Const,
    term_size, rename, subst, subst_single,
    id_renaming, id_subst, lift_renaming
)
from logic import (
    Atom, One, Tensor, Lolli, WithF, PlusF, Bang, Bot,
    formula_size, eval_formula, eval_context,
    Derivation, d_id, d_one_r, d_one_l, d_tensor_r, d_tensor_l, d_lolli_r, d_lolli_l, d_cut,
    reduce_tensor_cut, reduce_lolli_cut
)
from pricing import (
    RootAddress, ChildAddress, address_origin, address_depth,
    duplicate_bang, CostModel, priced_id, priced_exchange, priced_weakening, priced_contraction
)
from connectives import (
    MorId, MorComp, MorFst, MorSnd, MorPair,
    MorInl, MorInr, MorCopair, MorTensor, MorEval, MorCurry,
    simplify_morphism, RefusalReason, StepSuccess, StepRefusal, StepHalted,
    neg, step_with_state_preservation
)


# ===========================================================================
# M100: Internal Syntax & Substitution Tests
# ===========================================================================

def test_term_size_and_structure():
    t1 = Var(0)
    assert term_size(t1) == 1
    t2 = Lam(Var(0)) # identity function
    assert term_size(t2) == 2
    t3 = App(t2, Const(42))
    assert term_size(t3) == 4


def test_renaming_functoriality_identity():
    # rename id t == t
    t = Lam(App(Var(0), Var(1)))
    assert rename(id_renaming, t) == t


def test_renaming_functoriality_composition():
    rho1 = lambda n: n + 1
    rho2 = lambda n: n * 2
    rho_comp = lambda n: rho2(rho1(n))

    t = Lam(App(Var(0), Var(2)))
    # rename rho2 (rename rho1 t) == rename (rho2 ∘ rho1) t
    assert rename(rho2, rename(rho1, t)) == rename(rho_comp, t)


def test_substitution_identity():
    t = Lam(App(Var(0), Var(1)))
    assert subst(id_subst, t) == t


def test_single_substitution_beta():
    # (\. 0) arg -> arg
    identity_body = Var(0)
    arg = Const(99)
    assert subst_single(arg, identity_body) == arg

    # (\. 1) arg -> Var(0) (free variable shifted down)
    const_body = Var(1)
    assert subst_single(arg, const_body) == Var(0)


def test_capture_free_substitution():
    # Substituting a term with a free variable under a binder must shift the free variable
    # t = \. (Var 1 @ Var 0)
    # subst_single (Var 0) on body
    body = App(Var(1), Var(0))
    s = Var(5)
    # subst_single s t: under binder, s is shifted by 1, so Var 5 becomes Var 6
    lam_term = Lam(body)
    res = subst_single(s, lam_term)
    assert isinstance(res, Lam)
    # Inside the body: Var 1 was target of substitution -> becomes Var 6; Var 0 was bound -> remains Var 0
    assert res.body == App(Var(6), Var(0))


# ===========================================================================
# M101: Resource-Sensitive Consequence & Operational Logic Tests
# ===========================================================================

def test_formula_size_metrics():
    a = Atom(1)
    b = Atom(2)
    assert formula_size(a) == 1
    assert formula_size(One()) == 1
    assert formula_size(Bot()) == 1
    assert formula_size(Bang(a)) == 2
    assert formula_size(Tensor(a, b)) == 3
    assert formula_size(Lolli(a, b)) == 3


def test_identity_and_linear_derivations():
    a = Atom(10)
    b = Atom(20)

    # Identity: [A] |- A
    dA = d_id(a)
    assert dA.context == [a]
    assert dA.conclusion == a

    # One-R: [] |- 1
    dOne = d_one_r()
    assert dOne.context == []
    assert dOne.conclusion == One()

    # Tensor-R: [A, B] |- A ⊗ B
    dB = d_id(b)
    dAB = d_tensor_r(dA, dB)
    assert dAB.context == [a, b]
    assert dAB.conclusion == Tensor(a, b)


def test_principal_cut_reduction_tensor():
    a = Atom(1)
    b = Atom(2)
    c = Atom(3)

    dA = d_id(a)
    dB = d_id(b)
    # dC: [A, B, C] |- C
    dC = Derivation("hyp", [], [a, b, c], c)

    d_reduced = reduce_tensor_cut(dA, dB, dC)
    assert d_reduced.context == [a, b, c]
    assert d_reduced.conclusion == c


def test_principal_cut_reduction_lolli():
    a = Atom(1)
    b = Atom(2)
    c = Atom(3)

    # dAB: [A] |- B
    dAB = Derivation("hyp_ab", [], [a], b)
    # dA: [A] |- A
    dA = d_id(a)
    # dBC: [B] |- C
    dBC = Derivation("hyp_bc", [], [b], c)

    d_reduced = reduce_lolli_cut(dAB, dA, dBC)
    assert d_reduced.context == [a]
    assert d_reduced.conclusion == c


def test_phase_space_valuation_soundness():
    # Model valuation: atom i is satisfied at resource r iff r == i
    def val(atom_id: int, r: int) -> bool:
        return r == atom_id

    a1 = Atom(1)
    a2 = Atom(2)
    tens = Tensor(a1, a2)

    # Tensor is satisfied at resource 1 + 2 = 3
    assert eval_formula(val, tens, 3)
    # Tensor is NOT satisfied at resource 2 or 4
    assert not eval_formula(val, tens, 2)
    assert not eval_formula(val, tens, 4)

    # Context evaluation: [A(1), A(2)] is satisfied at 3
    assert eval_context(val, [a1, a2], 3)
    assert not eval_context(val, [a1, a2], 2)


def test_non_triviality_bot_unprovable():
    # In any valuation, Bot() is never satisfied at any resource
    def val(atom_id: int, r: int) -> bool:
        return True

    for r in range(10):
        assert not eval_formula(val, Bot(), r)
    # Empty context is satisfied at r = 0, but Bot is False at r = 0
    assert eval_context(val, [], 0)
    assert not eval_formula(val, Bot(), 0)


# ===========================================================================
# M102: Resource Pricing & Structural Rules Tests
# ===========================================================================

def test_address_provenance_and_separation():
    root1 = RootAddress(101)
    root2 = RootAddress(102)

    child1_0 = ChildAddress(root1, 0)
    child1_1 = ChildAddress(root1, 1)
    child1_0_0 = ChildAddress(child1_0, 0)

    assert address_origin(root1) == 101
    assert address_origin(child1_0) == 101
    assert address_origin(child1_0_0) == 101
    assert address_depth(root1) == 0
    assert address_depth(child1_0) == 1
    assert address_depth(child1_0_0) == 2

    # Separation preservation: roots 101 and 102 are distinct, so their children remain distinct
    child2_0 = ChildAddress(root2, 0)
    assert address_origin(child1_0) != address_origin(child2_0)


def test_copy_safe_bang_duplication():
    root = RootAddress(7)
    a = Atom(1)
    c0, c1 = duplicate_bang(root, a)

    assert c0.addr != c1.addr
    assert address_origin(c0.addr) == 7
    assert address_origin(c1.addr) == 7
    assert c0.form == a
    assert c1.form == a


def test_priced_structural_derivations():
    cm = CostModel(cost_ex=1, cost_weak=1, cost_cont=2)
    a = Atom(1)
    b = Atom(2)

    # Linear identity cost is 0
    d0 = priced_id(a, cm)
    assert d0.structural_cost == 0

    # Weakening adds cost_weak (1)
    d1 = priced_weakening(d0, b, 1, cm)
    assert d1.structural_cost == 1
    assert d1.context == [a, b]

    # Exchange adds cost_ex (1)
    d2 = priced_exchange(d1, 0, cm)
    assert d2.structural_cost == 2
    assert d2.context == [b, a]

    # Contraction adds cost_cont (2)
    d3 = priced_weakening(d2, b, 0, cm) # [b, b, a] cost: 3
    d4 = priced_contraction(d3, 0, cm)  # [b, a] cost: 5
    assert d4.structural_cost == 5


# ===========================================================================
# M103: Connectives by Universal Property & Refusal Separation Tests
# ===========================================================================

def test_product_universal_property():
    a = Atom(1)
    b = Atom(2)
    c = Atom(3)

    f = MorId(a)
    g = MorId(b)
    # pair(f, g)
    pair_fg = MorPair(f, g)

    # First projection cancels pairing: fst ∘ pair(f, g) == f
    comp1 = MorComp(pair_fg, MorFst(a, b))
    assert simplify_morphism(comp1) == f

    # Second projection cancels pairing: snd ∘ pair(f, g) == g
    comp2 = MorComp(pair_fg, MorSnd(a, b))
    assert simplify_morphism(comp2) == g


def test_coproduct_universal_property():
    a = Atom(1)
    b = Atom(2)
    c = Atom(3)

    f = MorId(c)
    g = MorId(c)
    copair_fg = MorCopair(f, g)

    # First injection cancels copairing: inl ∘ copair(f, g) == f
    comp1 = MorComp(MorInl(a, b), copair_fg)
    assert simplify_morphism(comp1) == f

    # Second injection cancels copairing: inr ∘ copair(f, g) == g
    comp2 = MorComp(MorInr(a, b), copair_fg)
    assert simplify_morphism(comp2) == g


def test_internal_hom_universal_property():
    a = Atom(1)
    b = Atom(2)
    c = Atom(3)

    # Morphism f : C ⊗ A -> B
    f = MorId(b)
    # curry(f) : C -> (A ⊸ B)
    curry_f = MorCurry(f)
    # (curry(f) ⊗ id) ⨟ eval == f
    tensor_part = MorTensor(curry_f, MorId(a))
    eval_mor = MorEval(a, b)
    full_comp = MorComp(tensor_part, eval_mor)

    assert simplify_morphism(full_comp) == f


def test_refusal_state_preservation():
    # Transition function that refuses on negative input
    def step_counter(state: int) -> StepOutcome[int]:
        if state < 0:
            return StepRefusal(RefusalReason.PROTECTION_VIOLATION)
        elif state == 0:
            return StepHalted()
        else:
            return StepSuccess(state - 1)

    # On valid input: mutates state
    assert step_with_state_preservation(step_counter, 5) == 4
    assert step_with_state_preservation(step_counter, 1) == 0

    # On refusal: PRESERVES EXACT STATE UNMUTATED
    assert step_with_state_preservation(step_counter, -10) == -10
    assert step_with_state_preservation(step_counter, -1) == -1


def test_ontological_separation_refusal_vs_negation():
    # 1. Refusal is an operational outcome constructor, distinct from step and halt
    ref = StepRefusal(RefusalReason.DESIGNATED_PAIR_SEPARATION)
    step = StepSuccess(100)
    halt = StepHalted()

    assert ref != step
    assert ref != halt

    # 2. Negation is a linear logic formula: A ⊸ ⊥
    a = Atom(1)
    neg_a = neg(a)
    assert isinstance(neg_a, Lolli)
    assert neg_a.ante == a
    assert neg_a.succ == Bot()
