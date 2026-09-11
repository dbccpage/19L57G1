"""Unit and property tests for compositional semantic satisfaction and Heyting valuation domain.

AuthorityEffect: None.
Epistemic Posture: Claim Hygiene Compliant (bounded receipts, exact rational valuations).
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import pytest

PKG_DIR = Path(__file__).resolve().parent.parent
if str(PKG_DIR) not in sys.path:
    sys.path.insert(0, str(PKG_DIR))

from semantics import (
    FALSE,
    HALF,
    TRUE,
    Atom,
    BoundedExists,
    BoundedForall,
    Conj,
    Disj,
    Formula,
    Identity,
    Imp,
    Neg,
    RationalValuation,
    RelationalModel,
    atom,
    conj,
    disj,
    eq,
    evaluate,
    exists,
    forall,
    imp,
    join,
    meet,
    neg,
    pseudo_complement,
    implies,
)


# ===========================================================================
# 1. Heyting Truth Structure (Poset) Invariants & Boundary Tests (Class 1 & 2)
# ===========================================================================

def test_rational_valuation_construction_and_bounds():
    """Negative-control matrix: Out-of-bounds valuations must be rejected."""
    # Positive cases
    v0 = RationalValuation(0)
    v1 = RationalValuation(1)
    v_half = RationalValuation(Fraction(1, 2))
    v_third = RationalValuation("1/3")
    assert v0.val == Fraction(0, 1)
    assert v1.val == Fraction(1, 1)
    assert v_half.val == Fraction(1, 2)
    assert v_third.val == Fraction(1, 3)

    # Negative controls (out-of-bounds)
    with pytest.raises(ValueError):
        RationalValuation(-1)
    with pytest.raises(ValueError):
        RationalValuation(Fraction(-1, 10))
    with pytest.raises(ValueError):
        RationalValuation(Fraction(11, 10))
    with pytest.raises(ValueError):
        RationalValuation("2/1")
    with pytest.raises(ValueError):
        RationalValuation(1.5)


def test_poset_order_and_boolean_coercion():
    """Class 3: Order relations and Boolean coercion."""
    v0 = RationalValuation(0)
    v1 = RationalValuation(Fraction(1, 3))
    v2 = RationalValuation(Fraction(2, 3))
    v3 = RationalValuation(1)

    assert v0 < v1 < v2 < v3
    assert v0 <= v1 <= v2 <= v3
    assert v3 > v2 > v1 > v0
    assert v3 >= v2 >= v1 >= v0
    assert v1 == RationalValuation(Fraction(2, 6))
    assert v1 != v2

    # Boolean coercion: only 1 is True
    assert not bool(v0)
    assert not bool(v1)
    assert not bool(v2)
    assert bool(v3)
    assert v3.is_true and not v3.is_false
    assert v0.is_false and not v0.is_true
    assert not v1.is_true and not v1.is_false


def test_heyting_algebra_laws_property():
    """Class 1: Algebraic laws over rational valuation domain."""
    sample_values = [
        Fraction(0, 1),
        Fraction(1, 6),
        Fraction(1, 3),
        Fraction(1, 2),
        Fraction(2, 3),
        Fraction(5, 6),
        Fraction(1, 1),
    ]
    vals = [RationalValuation(f) for f in sample_values]

    for a in vals:
        # Idempotence
        assert meet(a, a) == a
        assert join(a, a) == a

        # Identity elements
        assert meet(a, TRUE) == a
        assert meet(a, FALSE) == FALSE
        assert join(a, TRUE) == TRUE
        assert join(a, FALSE) == a

        # Negation / Pseudo-complement: a meet ~a == 0
        neg_a = pseudo_complement(a)
        assert meet(a, neg_a) == FALSE

        # Implication self: a -> a == 1
        assert implies(a, a) == TRUE

        # Double negation expansion: a <= ~~a
        neg_neg_a = pseudo_complement(neg_a)
        assert a <= neg_neg_a

        for b in vals:
            # Commutativity
            assert meet(a, b) == meet(b, a)
            assert join(a, b) == join(b, a)

            # Absorption
            assert meet(a, join(a, b)) == a
            assert join(a, meet(a, b)) == a

            # Heyting adjunction: meet(c, a) <= b iff c <= implies(a, b)
            for c in vals:
                left_cond = meet(c, a) <= b
                right_cond = c <= implies(a, b)
                assert left_cond == right_cond, f"Adjunction failed for a={a}, b={b}, c={c}"


def test_constructive_failure_of_law_of_excluded_middle():
    """Class 3: Constructive failure of LEM in intermediate valuation domain."""
    # In an intuitionistic valuation domain, a \lor \neg a is not generally 1.
    val_half = RationalValuation(Fraction(1, 2))
    neg_half = pseudo_complement(val_half)
    assert neg_half == FALSE  # since 1/2 is not 0, 1/2 -> 0 is 0
    lem_val = join(val_half, neg_half)
    assert lem_val == val_half
    assert lem_val != TRUE  # LEM does not hold constructively for intermediate values


# ===========================================================================
# 2. Compositional Satisfaction: Relational Model Setup (Class 3 & 4)
# ===========================================================================

@pytest.fixture
def sample_model() -> RelationalModel:
    """Standard 5-partition relational carrier model."""
    return RelationalModel(
        data=("tok0", "tok1", "tok2"),
        forms=(1, 2),  # form 0 is unary, form 1 is binary
        insts=frozenset({
            (0, (0,)),        # form_0 holds on datum 0
            (1, (0, 1)),      # form_1 holds on (0, 1)
        }),
        rules=frozenset(),    # no forms under uniform rule
        reqs=frozenset({(0, 1), (1, 2)}),  # separation requirement pairs
        custom_relations={
            "custom_tag": frozenset({("tok0",), ("tok2",)}),
            "custom_pair": frozenset({(0, 2)}),
        },
        custom_domains={
            "tag_sort": ("tok0", "tok1", "tok2"),
            "sub_sort": (0, 1),
        },
    )


def test_atomic_evaluation_instances(sample_model: RelationalModel):
    """Class 3: Form instances positive and negative evaluations."""
    # Form 0 (unary)
    assert evaluate(sample_model, atom("0", "0")) == TRUE
    assert evaluate(sample_model, atom("form_0", "0")) == TRUE
    assert evaluate(sample_model, atom("inst", "0", "0")) == TRUE

    # Negative controls on form 0
    assert evaluate(sample_model, atom("0", "1")) == FALSE
    assert evaluate(sample_model, atom("0", "2")) == FALSE

    # Form 1 (binary)
    assert evaluate(sample_model, atom("1", "0", "1")) == TRUE
    assert evaluate(sample_model, atom("form_1", "0", "1")) == TRUE
    assert evaluate(sample_model, atom("inst", "1", "0", "1")) == TRUE

    # Negative controls on form 1 (asymmetric link)
    assert evaluate(sample_model, atom("1", "1", "0")) == FALSE
    assert evaluate(sample_model, atom("1", "0", "2")) == FALSE


def test_atomic_evaluation_rules_and_requirements(sample_model: RelationalModel):
    """Class 3: Uniform all-tuples rules and separation requirements."""
    # Requirements
    assert evaluate(sample_model, atom("req", "0", "1")) == TRUE
    assert evaluate(sample_model, atom("req", "1", "0")) == TRUE  # symmetric pair check
    assert evaluate(sample_model, atom("req", "1", "2")) == TRUE
    assert evaluate(sample_model, atom("req", "0", "2")) == FALSE  # not in reqs

    # Rules
    assert evaluate(sample_model, atom("rule", "0")) == FALSE

    # Model with rule active on form 0
    model_with_rule = RelationalModel(
        data=sample_model.data,
        forms=sample_model.forms,
        insts=sample_model.insts,
        rules=frozenset({0}),
        reqs=sample_model.reqs,
    )
    assert evaluate(model_with_rule, atom("rule", "0")) == TRUE
    # When rule is active, all tuples for form 0 are derivable
    assert evaluate(model_with_rule, atom("0", "0")) == TRUE
    assert evaluate(model_with_rule, atom("0", "1")) == TRUE
    assert evaluate(model_with_rule, atom("0", "2")) == TRUE


def test_atomic_evaluation_negative_controls(sample_model: RelationalModel):
    """Class 2: Unknown relations, arity mismatches, and malformed inputs."""
    # Unknown relation returns bottom (refusal)
    assert evaluate(sample_model, atom("nonexistent_predicate", "0")) == FALSE
    assert evaluate(sample_model, atom("random_relation", "0", "1")) == FALSE

    # Arity mismatch on recognized forms
    # Form 0 has arity 1; passing 2 arguments returns FALSE
    assert evaluate(sample_model, atom("0", "0", "1")) == FALSE
    # Form 1 has arity 2; passing 1 argument returns FALSE
    assert evaluate(sample_model, atom("1", "0")) == FALSE

    # Out-of-bounds form index
    assert evaluate(sample_model, atom("99", "0")) == FALSE
    assert evaluate(sample_model, atom("form_99", "0")) == FALSE


def test_custom_relations_and_domains(sample_model: RelationalModel):
    """Class 3: Custom named relations and custom domain quantification."""
    assert evaluate(sample_model, atom("custom_tag", "tok0")) == TRUE
    assert evaluate(sample_model, atom("custom_tag", "tok1")) == FALSE
    assert evaluate(sample_model, atom("custom_pair", "0", "2")) == TRUE
    assert evaluate(sample_model, atom("custom_pair", "2", "0")) == FALSE


# ===========================================================================
# 3. Compositional Connectives & Variable Assignments (Class 1 & 3)
# ===========================================================================

def test_identity_evaluation(sample_model: RelationalModel):
    """Class 3: Internal syntactic identity statement left == right."""
    assert evaluate(sample_model, eq("0", "0")) == TRUE
    assert evaluate(sample_model, eq("0", "1")) == FALSE
    assert evaluate(sample_model, eq("tok0", "tok0")) == TRUE
    assert evaluate(sample_model, eq("tok0", "tok1")) == FALSE

    # Variables in assignment
    env = {"x": 0, "y": 0, "z": 1}
    assert evaluate(sample_model, eq("x", "y"), env) == TRUE
    assert evaluate(sample_model, eq("x", "z"), env) == FALSE


def test_conjunction_compositionality(sample_model: RelationalModel):
    """Class 1: Compositional conjunction phi_1 and phi_2 equals meet(val(phi_1), val(phi_2))."""
    f_t = atom("0", "0")  # TRUE
    f_f = atom("0", "1")  # FALSE

    assert evaluate(sample_model, conj(f_t, f_t)) == TRUE
    assert evaluate(sample_model, conj(f_t, f_f)) == FALSE
    assert evaluate(sample_model, conj(f_f, f_t)) == FALSE
    assert evaluate(sample_model, conj(f_f, f_f)) == FALSE


def test_disjunction_compositionality(sample_model: RelationalModel):
    """Class 1: Compositional disjunction phi_1 or phi_2 equals join(val(phi_1), val(phi_2))."""
    f_t = atom("0", "0")  # TRUE
    f_f = atom("0", "1")  # FALSE

    assert evaluate(sample_model, disj(f_t, f_t)) == TRUE
    assert evaluate(sample_model, disj(f_t, f_f)) == TRUE
    assert evaluate(sample_model, disj(f_f, f_t)) == TRUE
    assert evaluate(sample_model, disj(f_f, f_f)) == FALSE


def test_implication_and_modus_ponens(sample_model: RelationalModel):
    """Class 1: Compositional Heyting implication satisfies modus ponens."""
    f_t = atom("0", "0")  # TRUE
    f_f = atom("0", "1")  # FALSE

    assert evaluate(sample_model, imp(f_t, f_t)) == TRUE
    assert evaluate(sample_model, imp(f_f, f_t)) == TRUE
    assert evaluate(sample_model, imp(f_f, f_f)) == TRUE
    assert evaluate(sample_model, imp(f_t, f_f)) == FALSE

    # Modus ponens: if phi is TRUE and (phi -> psi) is TRUE, then psi is TRUE
    phi = atom("0", "0")
    psi = atom("1", "0", "1")
    f_implication = imp(phi, psi)
    v_phi = evaluate(sample_model, phi)
    v_imp = evaluate(sample_model, f_implication)
    v_psi = evaluate(sample_model, psi)

    assert v_phi == TRUE
    assert v_imp == TRUE
    assert v_psi == TRUE
    assert meet(v_phi, v_imp) <= v_psi


def test_operational_negation_refusal(sample_model: RelationalModel):
    """Class 3: Negation as operational refusal: neg(phi) = (phi -> 0)."""
    f_t = atom("0", "0")  # TRUE
    f_f = atom("0", "1")  # FALSE

    assert evaluate(sample_model, neg(f_t)) == FALSE
    assert evaluate(sample_model, neg(f_f)) == TRUE

    # Refusal of contradiction: phi and not(phi) evaluates to FALSE
    contradiction = conj(f_t, neg(f_t))
    assert evaluate(sample_model, contradiction) == FALSE


# ===========================================================================
# 4. Bounded Quantifiers over Finite Carrier Sorts (Class 1 & 3)
# ===========================================================================

def test_bounded_universal_quantifier(sample_model: RelationalModel):
    """Class 1: Universal quantification as meet over finite carrier sort."""
    # forall x in data. (x = 0 or req(x, 1) or req(0, x))
    # Domain: {0, 1, 2}
    # x = 0: (0 = 0) is TRUE -> TRUE
    # x = 1: req(1, 1) FALSE, req(0, 1) TRUE -> TRUE
    # x = 2: req(2, 1) is req(1, 2) TRUE -> TRUE
    f_all_true = forall(
        "x",
        "data",
        disj(eq("x", "0"), disj(atom("req", "x", "1"), atom("req", "0", "x"))),
    )
    assert evaluate(sample_model, f_all_true) == TRUE

    # forall x in data. form_0(x) -> FALSE since form_0 holds only on 0
    f_all_false = forall("x", "data", atom("0", "x"))
    assert evaluate(sample_model, f_all_false) == FALSE

    # Empty domain universal quantifier evaluates to TRUE (vacuous truth)
    f_empty = forall("x", "nonexistent_sort", atom("0", "x"))
    assert evaluate(sample_model, f_empty) == TRUE


def test_bounded_existential_quantifier(sample_model: RelationalModel):
    """Class 1: Existential quantification as join over finite carrier sort."""
    # exists x in data. form_0(x) -> TRUE (witnessed by 0)
    f_ex_true = exists("x", "data", atom("0", "x"))
    assert evaluate(sample_model, f_ex_true) == TRUE

    # exists x in data. (form_0(x) and x = 2) -> FALSE
    f_ex_false = exists("x", "data", conj(atom("0", "x"), eq("x", "2")))
    assert evaluate(sample_model, f_ex_false) == FALSE

    # Empty domain existential quantifier evaluates to FALSE
    f_empty = exists("x", "nonexistent_sort", atom("0", "x"))
    assert evaluate(sample_model, f_empty) == FALSE


def test_nested_quantifiers_and_interaction(sample_model: RelationalModel):
    """Class 3: Nested universal and existential quantifiers."""
    # forall x in sub_sort. exists y in data. (x = y)
    # sub_sort is {0, 1}, data is {0, 1, 2}
    nested_formula = forall("x", "sub_sort", exists("y", "data", eq("x", "y")))
    assert evaluate(sample_model, nested_formula) == TRUE

    # exists x in sub_sort. forall y in data. (x = y) -> FALSE
    impossible_equal = exists("x", "sub_sort", forall("y", "data", eq("x", "y")))
    assert evaluate(sample_model, impossible_equal) == FALSE
