"""Unit and property tests for signature transport and canonical isomorphism invariance.

Covers:
- All 3 Challenge-3 Reading L canonical isomorphism classes (U0, BL, BD).
- All 5 Challenge-3 Reading F canonical isomorphism classes (MarkF, DiagF, LinkF, OutF, InF).
- G012 translation commutation: M, sigma |= phi <=> tau_*(M), tau(sigma) |= tau(phi).
- Functorial properties of pushforward and formula renaming.
- Negative controls: dimension mismatches, un-transported asymmetric formulas.

AuthorityEffect: None.
Epistemic Posture: Claim Hygiene Compliant (bounded, exact rational receipts).
"""

from __future__ import annotations

from pathlib import Path
import sys
import pytest

PKG_DIR = Path(__file__).resolve().parent.parent
if str(PKG_DIR) not in sys.path:
    sys.path.insert(0, str(PKG_DIR))

from semantics import (
    FALSE,
    TRUE,
    Formula,
    Isomorphism,
    RelationalModel,
    atom,
    check_isomorphism,
    check_transport_invariance,
    conj,
    disj,
    eq,
    evaluate,
    exists,
    forall,
    get_challenge3_f_classes,
    get_challenge3_l_classes,
    imp,
    neg,
    pushforward,
    rename_assignment,
    rename_formula,
)


# ===========================================================================
# 1. Challenge-3 Reading L Invariance (3 Canonical Classes) (Class 1 & 4)
# ===========================================================================

def test_reading_l_canonical_classes_count_and_keys():
    """Class 4: Reading L admits exactly 3 canonical isomorphism classes under mu1 = 2."""
    l_classes = get_challenge3_l_classes()
    assert len(l_classes) == 3
    assert set(l_classes.keys()) == {"U0", "BL", "BD"}


def test_reading_l_pushforward_involution_and_exactness():
    """Class 1: Functorial pushforward exactness and involution under transposition."""
    l_classes = get_challenge3_l_classes()

    for cname, (m_a, m_b, tau) in l_classes.items():
        # Check that tau is transposition (1, 0)
        assert tau.pi == (1, 0)
        assert tau.phi == (0,)

        # 1. Direct pushforward relational structure matches m_b
        p_a = pushforward(tau, m_a)
        assert p_a.forms == m_b.forms
        assert p_a.insts == m_b.insts
        assert p_a.rules == m_b.rules
        assert p_a.reqs == m_b.reqs

        # 2. Inverse pushforward matches m_a
        tau_inv = tau.inverse()
        p_b = pushforward(tau_inv, m_b)
        assert p_b.insts == m_a.insts
        assert p_b.reqs == m_a.reqs
        assert p_b.forms == m_a.forms

        # 3. Involution: tau . tau = id on full model including data tokens
        p_involution = pushforward(tau, pushforward(tau, m_a))
        assert p_involution.data == m_a.data
        assert p_involution.insts == m_a.insts
        assert p_involution.reqs == m_a.reqs
        assert p_involution.forms == m_a.forms


def test_reading_l_semantic_truth_invariance_battery():
    """Class 1: Semantic satisfaction invariance across Reading L classes."""
    l_classes = get_challenge3_l_classes()

    test_formulas = [
        # Atomic formulas
        atom("0", "0"),
        atom("0", "1"),
        atom("req", "0", "1"),
        atom("rule", "0"),
        # Identities
        eq("0", "0"),
        eq("0", "1"),
        # Connectives
        conj(atom("0", "0"), atom("req", "0", "1")),
        disj(atom("0", "0"), atom("0", "1")),
        imp(atom("0", "0"), atom("req", "0", "1")),
        neg(atom("0", "1")),
        # Quantifiers
        exists("x", "data", atom("0", "x")),
        forall("x", "data", disj(atom("0", "x"), atom("req", "x", "0"))),
    ]

    for cname, (m_a, m_b, tau) in l_classes.items():
        for phi in test_formulas:
            v_a = evaluate(m_a, phi)
            tau_phi = rename_formula(tau, phi)
            v_b = evaluate(m_b, tau_phi)
            assert v_a == v_b, f"Reading L invariance failed for {cname} on {phi}"
            assert check_transport_invariance(m_a, tau, phi) is True


# ===========================================================================
# 2. Challenge-3 Reading F Invariance (5 Canonical Classes) (Class 1 & 4)
# ===========================================================================

def test_reading_f_canonical_classes_count_and_keys():
    """Class 4: Reading F admits exactly 5 canonical isomorphism classes under mu1 = 2."""
    f_classes = get_challenge3_f_classes()
    assert len(f_classes) == 5
    assert set(f_classes.keys()) == {"MarkF", "DiagF", "LinkF", "OutF", "InF"}


def test_reading_f_pushforward_involution_and_exactness():
    """Class 1: Functorial pushforward exactness and involution under transposition."""
    f_classes = get_challenge3_f_classes()

    for cname, (m_a, m_b, tau) in f_classes.items():
        # Check that tau is transposition (0, 2, 1) fixing genesis datum 0
        assert tau.pi == (0, 2, 1)
        assert tau.phi == (0,)

        # 1. Direct pushforward relational structure matches m_b
        p_a = pushforward(tau, m_a)
        assert p_a.forms == m_b.forms
        assert p_a.insts == m_b.insts
        assert p_a.rules == m_b.rules
        assert p_a.reqs == m_b.reqs

        # 2. Inverse pushforward matches m_a
        tau_inv = tau.inverse()
        p_b = pushforward(tau_inv, m_b)
        assert p_b.insts == m_a.insts
        assert p_b.reqs == m_a.reqs
        assert p_b.forms == m_a.forms

        # 3. Involution: tau . tau = id on full model including data tokens
        p_involution = pushforward(tau, pushforward(tau, m_a))
        assert p_involution.data == m_a.data
        assert p_involution.insts == m_a.insts
        assert p_involution.reqs == m_a.reqs
        assert p_involution.forms == m_a.forms


def test_reading_f_semantic_truth_invariance_battery():
    """Class 1: Semantic satisfaction invariance across Reading F classes."""
    f_classes = get_challenge3_f_classes()

    test_formulas = [
        # Mark and Diag patterns on target data
        atom("0", "1"),
        atom("0", "2"),
        atom("0", "1", "1"),
        atom("0", "2", "2"),
        # Directional link patterns with genesis datum 0
        atom("0", "1", "0"),
        atom("0", "2", "0"),
        atom("0", "0", "1"),
        atom("0", "0", "2"),
        # Target pair links
        atom("0", "1", "2"),
        atom("0", "2", "1"),
        # Requirements
        atom("req", "1", "2"),
        # Quantified assertions
        exists("x", "data", atom("0", "x")),
        exists("x", "data", exists("y", "data", atom("0", "x", "y"))),
        forall(
            "x",
            "data",
            imp(atom("req", "x", "1"), exists("y", "data", atom("0", "x", "y"))),
        ),
    ]

    for cname, (m_a, m_b, tau) in f_classes.items():
        for phi in test_formulas:
            v_a = evaluate(m_a, phi)
            tau_phi = rename_formula(tau, phi)
            v_b = evaluate(m_b, tau_phi)
            assert v_a == v_b, f"Reading F invariance failed for {cname} on {phi}"
            assert check_transport_invariance(m_a, tau, phi) is True


# ===========================================================================
# 3. Negative Controls & Boundary Conditions (Class 2 & 3)
# ===========================================================================

def test_negative_control_unrenamed_asymmetric_formula_fails():
    """Class 2: Evaluating un-renamed asymmetric formula on transported model fails."""
    # U0 class has instance (0, (0,)) on datum 0.
    # Transported model has instance (0, (1,)) on datum 1.
    l_classes = get_challenge3_l_classes()
    m_a, m_b, tau = l_classes["U0"]

    phi_asymmetric = atom("0", "0")
    # In m_a, form_0 holds on 0:
    assert evaluate(m_a, phi_asymmetric) == TRUE
    # In m_b, form_0 holds on 1, NOT 0:
    assert evaluate(m_b, phi_asymmetric) == FALSE

    # Only when renamed under tau does it match:
    renamed_phi = rename_formula(tau, phi_asymmetric)
    assert repr(renamed_phi) == "0(1)"
    assert evaluate(m_b, renamed_phi) == TRUE


def test_negative_control_dimension_mismatch():
    """Class 2: Mismatched permutation dimensions raise ValueError."""
    m = RelationalModel(
        data=("d0", "d1"),
        forms=(1,),
    )
    # Permutation pi has length 3, but model has 2 data tokens:
    bad_tau_data = Isomorphism(pi=(0, 1, 2), phi=(0,))
    with pytest.raises(ValueError):
        pushforward(bad_tau_data, m)

    # Permutation phi has length 2, but model has 1 form:
    bad_tau_form = Isomorphism(pi=(1, 0), phi=(0, 1))
    with pytest.raises(ValueError):
        pushforward(bad_tau_form, m)


def test_variable_assignment_transport():
    """Class 3: Signature transport of variable environments."""
    tau = Isomorphism(pi=(1, 0), phi=(0,))
    env = {"x": 0, "y": 1, "unrelated_str": "hello"}
    transported_env = rename_assignment(tau, env)

    assert transported_env["x"] == 1
    assert transported_env["y"] == 0
    assert transported_env["unrelated_str"] == "hello"


def test_custom_relation_transport():
    """Class 3: Transport of models with custom named relations."""
    tau = Isomorphism(
        pi=(1, 0),
        phi=(0,),
        rel_map={"R_left": "R_right"},
        const_map={"c0": "c1"},
    )
    m = RelationalModel(
        data=("d0", "d1"),
        forms=(1,),
        custom_relations={"R_left": frozenset({(0, 1)})},
    )
    push_m = pushforward(tau, m)
    assert "R_right" in push_m.custom_relations
    assert push_m.custom_relations["R_right"] == frozenset({(1, 0)})


# ===========================================================================
# 4. Remediation Regression Tests (Defect Fixes for rename_formula & pushforward)
# ===========================================================================

def test_rule_atom_invariance_under_data_transposition():
    """Remediation: rule atom preserves truth invariance when model has non-empty rules under data transposition.

    In Atom('rule', ('0',)), '0' is a form index, NOT a data token.
    Under tau = Isomorphism(pi=(1, 0), phi=(0,)), rename_formula must use tau.phi
    to keep '0' mapped to '0', preserving naturality commutation.
    """
    m = RelationalModel(
        data=("d0", "d1"),
        forms=(1,),
        rules=frozenset({0}),
        reqs=frozenset({(0, 1)}),
    )
    tau = Isomorphism(pi=(1, 0), phi=(0,))
    phi = atom("rule", "0")

    # Before fix, rename_formula mistakenly mapped form index 0 via pi to 1
    ren_phi = rename_formula(tau, phi)
    assert repr(ren_phi) == "rule(0)"

    p_m = pushforward(tau, m)
    assert 0 in p_m.rules
    assert evaluate(m, phi) == TRUE
    assert evaluate(p_m, ren_phi) == TRUE
    assert check_transport_invariance(m, tau, phi) is True


def test_inst_atom_invariance_under_form_permutation():
    """Remediation: inst atom renames arg 0 via tau.phi and args 1..k via tau.pi.

    In Atom('inst', ('0', '1')), '0' is the form index and '1' is the data token argument.
    Under form swap tau.phi=(1, 0) and identity data tau.pi=(0, 1),
    rename_formula must map arg 0 to '1' and arg 1 to '1'.
    """
    m = RelationalModel(
        data=("d0", "d1"),
        forms=(1, 1),
        insts=frozenset({(0, (1,))}),
    )
    tau = Isomorphism(pi=(0, 1), phi=(1, 0))  # swap forms 0 and 1, fix data
    phi = atom("inst", "0", "1")

    ren_phi = rename_formula(tau, phi)
    assert repr(ren_phi) == "inst(1, 1)"

    p_m = pushforward(tau, m)
    assert (1, (1,)) in p_m.insts
    assert evaluate(m, phi) == TRUE
    assert evaluate(p_m, ren_phi) == TRUE
    assert check_transport_invariance(m, tau, phi) is True


def test_pushforward_rejection_non_bijective_and_out_of_bounds():
    """Remediation: pushforward validates bijectivity and bounds of pi and phi, raising ValueError."""
    m = RelationalModel(data=("d0", "d1"), forms=(1,), reqs=frozenset({(0, 1)}))

    # 1. Non-injective pi (duplicate indices)
    with pytest.raises(ValueError, match=r"pi must be a valid permutation"):
        pushforward(Isomorphism(pi=(0, 0), phi=(0,)), m)

    # 2. Negative index in pi
    with pytest.raises(ValueError, match=r"pi must be a valid permutation"):
        pushforward(Isomorphism(pi=(-1, 0), phi=(0,)), m)

    # 3. Out-of-bounds index in pi
    with pytest.raises(ValueError, match=r"pi must be a valid permutation"):
        pushforward(Isomorphism(pi=(0, 5), phi=(0,)), m)

    # 4. Dimension mismatch in pi length
    with pytest.raises(ValueError, match=r"pi must be a valid permutation"):
        pushforward(Isomorphism(pi=(0, 1, 2), phi=(0,)), m)

    # 5. Non-injective phi (form permutation)
    m_forms2 = RelationalModel(data=("d0", "d1"), forms=(1, 2))
    with pytest.raises(ValueError, match=r"phi must be a valid permutation"):
        pushforward(Isomorphism(pi=(0, 1), phi=(0, 0)), m_forms2)

    # 6. Out-of-bounds index in phi
    with pytest.raises(ValueError, match=r"phi must be a valid permutation"):
        pushforward(Isomorphism(pi=(0, 1), phi=(0, 2)), m_forms2)


def test_check_isomorphism_protocol():
    """Remediation: check_isomorphism verifies relational equivalence under isomorphism."""
    l_classes = get_challenge3_l_classes()
    f_classes = get_challenge3_f_classes()

    # Reading L classes: canonical isomorphisms hold bidirectionally
    for cname, (m_a, m_b, tau) in l_classes.items():
        assert check_isomorphism(tau, m_a, m_b) is True
        assert check_isomorphism(tau.inverse(), m_b, m_a) is True

    # Reading F classes: canonical isomorphisms hold
    for cname, (m_a, m_b, tau) in f_classes.items():
        assert check_isomorphism(tau, m_a, m_b) is True
        assert check_isomorphism(tau.inverse(), m_b, m_a) is True

    # Negative control: Cross-class pseudo-isomorphism between non-isomorphic classes (U0 vs BL)
    m_u0, _, tau_l = l_classes["U0"]
    m_bl, _, _ = l_classes["BL"]
    assert check_isomorphism(tau_l, m_u0, m_bl) is False

    # Negative control: Non-bijective permutation returns False
    bad_tau = Isomorphism(pi=(0, 0), phi=(0,))
    assert check_isomorphism(bad_tau, m_u0, m_u0) is False

    # Negative control: Dimension mismatch returns False
    bad_dim_tau = Isomorphism(pi=(0, 1, 2), phi=(0,))
    assert check_isomorphism(bad_dim_tau, m_u0, m_u0) is False

    # Negative control: Asymmetric state self-comparison under transposition fails
    assert check_isomorphism(tau_l, m_u0, m_u0) is False
