"""Comprehensive test suite for Target X302: Operational Reasoning & Belief Revision.

Validates:
- Internal syntax: propositions, valuations, commitments, and justifications.
- Deductive inferences: Modus Ponens, Conjunction, Disjunction, Resolution, Contradictions.
- Endogenous TMS: dependency DAG tracking, support sets, cycle detection.
- Contradiction detection: direct (phi vs ~phi) and operational (x = v1 vs x = v2).
- Minimal retraction & AGM belief revision: minimum hitting set, entrenchment tie-breaking.
- Deactivation cascade propagation.
- AGM revision postulates: Success, Inclusion, Vacuity, Consistency, Axiom Invariance.
- Negative control matrix: invalid inputs, rule violations, tamper checks, edge cases.
"""

from __future__ import annotations

import pytest

try:
    from reasoning import (
        And,
        Atom,
        Bottom,
        CircularDependencyError,
        CommitmentClass,
        EqVal,
        FoundationalInconsistencyError,
        InactiveNodeError,
        ImmutableAxiomError,
        Implies,
        InvalidInferenceError,
        JustificationKind,
        Not,
        OperationalTMS,
        Or,
        RevisionReceipt,
        UnknownNodeError,
    )
except ImportError:
    from research.x302_operational_reasoning.reasoning import (  # type: ignore[no-redef]
        And,
        Atom,
        Bottom,
        CircularDependencyError,
        CommitmentClass,
        EqVal,
        FoundationalInconsistencyError,
        InactiveNodeError,
        ImmutableAxiomError,
        Implies,
        InvalidInferenceError,
        JustificationKind,
        Not,
        OperationalTMS,
        Or,
        RevisionReceipt,
        UnknownNodeError,
    )


# ============================================================================
# 1. Syntax, Commitments, and Formulas
# ============================================================================

def test_formula_syntax_and_equality() -> None:
    p = Atom("P")
    q = Atom("Q")
    not_p = Not(p)
    p_and_q = And(p, q)
    p_or_q = Or(p, q)
    p_imp_q = Implies(p, q)
    bot = Bottom()
    val1 = EqVal("state", "READY")
    val2 = EqVal("state", "RUNNING")

    assert str(p) == "P"
    assert str(not_p) == "~(P)"
    assert str(p_and_q) == "(P & Q)"
    assert str(p_or_q) == "(P | Q)"
    assert str(p_imp_q) == "(P -> Q)"
    assert str(bot) == "_|_"
    assert str(val1) == "(state = 'READY')"

    assert p == Atom("P")
    assert p != q
    assert not_p == Not(Atom("P"))
    assert val1 != val2
    assert hash(p) == hash(Atom("P"))
    assert hash(bot) == hash(Bottom())

    # Serialization to dict
    assert p.to_dict() == {"type": "atom", "name": "P"}
    assert not_p.to_dict() == {"type": "not", "inner": {"type": "atom", "name": "P"}}
    assert p_and_q.to_dict()["type"] == "and"
    assert p_or_q.to_dict()["type"] == "or"
    assert p_imp_q.to_dict()["type"] == "implies"
    assert val1.to_dict() == {"type": "eq_val", "variable": "state", "value": "READY"}
    assert bot.to_dict() == {"type": "bottom"}


def test_axiom_vs_hypothesis_commitments() -> None:
    tms = OperationalTMS()
    ax_id = tms.add_axiom("A1", Atom("P"))
    hyp_id = tms.add_hypothesis("H1", Atom("Q"), entrenchment=2)

    ax_node = tms.get_node(ax_id)
    hyp_node = tms.get_node(hyp_id)

    # Axiom: firm commitment, empty hypothesis support
    assert ax_node.commitment == CommitmentClass.AXIOM
    assert ax_node.support == frozenset()
    assert ax_node.is_active is True

    # Hypothesis: speculative commitment, singleton support
    assert hyp_node.commitment == CommitmentClass.HYPOTHESIS
    assert hyp_node.support == frozenset({"H1"})
    assert hyp_node.is_active is True

    # Check node and justification dict serialization
    assert ax_node.to_dict()["node_id"] == ax_id
    assert hyp_node.justification.to_dict()["kind"] == "HYPOTHESIS_PREMISE"
    assert tms.active_hypotheses == frozenset({"H1"})
    assert len(tms.nodes) == 2


# ============================================================================
# 2. Deductive Inference Rules & Support Propagation
# ============================================================================

def test_modus_ponens_inference() -> None:
    tms = OperationalTMS()
    p = Atom("P")
    q = Atom("Q")
    n_p = tms.add_hypothesis("H1", p)
    n_imp = tms.add_hypothesis("H2", Implies(p, q))

    # Standard order (imp, arg)
    n_q = tms.apply_inference(
        formula=q,
        kind=JustificationKind.MODUS_PONENS,
        antecedents=(n_imp, n_p),
    )
    node_q = tms.get_node(n_q)
    assert node_q.formula == q
    assert node_q.support == frozenset({"H1", "H2"})
    assert node_q.antecedents == (n_imp, n_p)

    # Reversed order (arg, imp)
    n_q2 = tms.apply_inference(
        formula=q,
        kind=JustificationKind.MODUS_PONENS,
        antecedents=(n_p, n_imp),
    )
    assert tms.get_node(n_q2).formula == q


def test_conjunction_intro_and_elim() -> None:
    tms = OperationalTMS()
    p = Atom("P")
    q = Atom("Q")
    n_p = tms.add_axiom("A1", p)
    n_q = tms.add_hypothesis("H1", q)

    n_and = tms.apply_inference(
        formula=And(p, q),
        kind=JustificationKind.CONJUNCTION_INTRO,
        antecedents=(n_p, n_q),
    )
    assert tms.get_node(n_and).support == frozenset({"H1"})

    n_p_back = tms.apply_inference(
        formula=p,
        kind=JustificationKind.CONJUNCTION_ELIM_LEFT,
        antecedents=(n_and,),
    )
    assert tms.get_node(n_p_back).formula == p
    assert tms.get_node(n_p_back).support == frozenset({"H1"})

    n_q_back = tms.apply_inference(
        formula=q,
        kind=JustificationKind.CONJUNCTION_ELIM_RIGHT,
        antecedents=(n_and,),
    )
    assert tms.get_node(n_q_back).formula == q


def test_disjunction_intro_and_resolution() -> None:
    tms = OperationalTMS()
    p = Atom("P")
    q = Atom("Q")
    n_p = tms.add_hypothesis("H1", p)
    n_q = tms.add_hypothesis("H2", q)
    n_not_p = tms.add_hypothesis("H3", Not(p))
    n_not_q = tms.add_hypothesis("H4", Not(q))

    # Left disjunction intro
    n_or1 = tms.apply_inference(
        formula=Or(p, q),
        kind=JustificationKind.DISJUNCTION_INTRO_LEFT,
        antecedents=(n_p,),
    )
    assert tms.get_node(n_or1).support == frozenset({"H1"})

    # Right disjunction intro
    n_or2 = tms.apply_inference(
        formula=Or(p, q),
        kind=JustificationKind.DISJUNCTION_INTRO_RIGHT,
        antecedents=(n_q,),
    )
    assert tms.get_node(n_or2).support == frozenset({"H2"})

    # Resolution: (P | Q) with ~P -> Q
    n_res1 = tms.apply_inference(
        formula=q,
        kind=JustificationKind.RESOLUTION,
        antecedents=(n_or1, n_not_p),
    )
    assert tms.get_node(n_res1).formula == q

    # Resolution: (P | Q) with ~Q -> P (negating right disjunct)
    n_res2 = tms.apply_inference(
        formula=p,
        kind=JustificationKind.RESOLUTION,
        antecedents=(n_not_q, n_or1),
    )
    assert tms.get_node(n_res2).formula == p


# ============================================================================
# 3. Contradiction Detection (Direct & Operational)
# ============================================================================

def test_direct_contradiction_detection() -> None:
    tms = OperationalTMS()
    p = Atom("P")
    tms.add_hypothesis("H1", p)
    tms.add_hypothesis("H2", Not(p))

    conflicts = tms.detect_contradictions()
    assert len(conflicts) == 1
    assert conflicts[0] == frozenset({"H1", "H2"})


def test_operational_valuation_contradiction_detection() -> None:
    tms = OperationalTMS()
    val1 = EqVal("carrier_x", 10)
    val2 = EqVal("carrier_x", 20)

    tms.add_hypothesis("H1", val1)
    tms.add_hypothesis("H2", val2)

    conflicts = tms.detect_contradictions()
    assert len(conflicts) == 1
    assert conflicts[0] == frozenset({"H1", "H2"})


def test_direct_contradiction_explicit_derivation() -> None:
    tms = OperationalTMS()
    p = Atom("P")
    n1 = tms.add_hypothesis("H1", p)
    n2 = tms.add_hypothesis("H2", Not(p))

    n_bot = tms.apply_inference(
        formula=Bottom(),
        kind=JustificationKind.CONTRADICTION_DIRECT,
        antecedents=(n1, n2),
    )
    assert tms.get_node(n_bot).support == frozenset({"H1", "H2"})
    assert frozenset({"H1", "H2"}) in tms.active_conflicts

    # Reversed order
    n3 = tms.add_hypothesis("H3", Not(Atom("Z")))
    n4 = tms.add_hypothesis("H4", Atom("Z"))
    n_bot2 = tms.apply_inference(
        formula=Bottom(),
        kind=JustificationKind.CONTRADICTION_DIRECT,
        antecedents=(n3, n4),
    )
    assert tms.get_node(n_bot2).support == frozenset({"H3", "H4"})


def test_operational_contradiction_explicit_derivation() -> None:
    tms = OperationalTMS()
    n1 = tms.add_hypothesis("H1", EqVal("stage", "ALPHA"))
    n2 = tms.add_hypothesis("H2", EqVal("stage", "BETA"))

    n_bot = tms.apply_inference(
        formula=Bottom(),
        kind=JustificationKind.CONTRADICTION_VALUATION,
        antecedents=(n1, n2),
    )
    assert tms.get_node(n_bot).support == frozenset({"H1", "H2"})


# ============================================================================
# 4. Edge Cases & Safety Gates
# ============================================================================

def test_edge_case_1_foundational_inconsistency() -> None:
    """Derivation of bottom with empty support raises FoundationalInconsistencyError."""
    tms = OperationalTMS()
    p = Atom("P")
    tms.add_axiom("A1", p)
    with pytest.raises(FoundationalInconsistencyError):
        tms.add_axiom("A2", Not(p))


def test_edge_case_1_foundational_valuation_inconsistency() -> None:
    """Contradictory axioms on operational valuations raise FoundationalInconsistencyError."""
    tms = OperationalTMS()
    tms.add_axiom("A1", EqVal("capacity", 100))
    with pytest.raises(FoundationalInconsistencyError):
        tms.add_axiom("A2", EqVal("capacity", 200))


def test_edge_case_1_foundational_bottom_inference() -> None:
    """Directly deriving Bottom from axioms raises FoundationalInconsistencyError."""
    tms = OperationalTMS()
    n1 = tms.add_axiom("A1", Atom("P"))
    # Manually bypass add_axiom immediate check to test apply_inference gate
    just = tms.get_node(n1).justification
    tms._nodes["ax:A2"] = type(tms.get_node(n1))(
        node_id="ax:A2",
        formula=Not(Atom("P")),
        commitment=CommitmentClass.AXIOM,
        justification=just,
        antecedents=(),
        support=frozenset(),
        is_active=True,
    )
    with pytest.raises(FoundationalInconsistencyError):
        tms.apply_inference(
            formula=Bottom(),
            kind=JustificationKind.CONTRADICTION_DIRECT,
            antecedents=(n1, "ax:A2"),
        )


def test_edge_case_2_circular_dependency_detection() -> None:
    """Circular reasoning attempts are detected and raise CircularDependencyError."""
    tms = OperationalTMS()
    p = Atom("P")
    q = Atom("Q")
    n_p = tms.add_hypothesis("H1", p)
    n_q = tms.add_hypothesis("H2", q)

    n_and = tms.apply_inference(
        formula=And(p, q),
        kind=JustificationKind.CONJUNCTION_INTRO,
        antecedents=(n_p, n_q),
    )

    with pytest.raises(CircularDependencyError):
        tms._check_cycle(n_p, [n_and])


def test_edge_case_3_overlapping_conflict_sets_minimal_hitting_set() -> None:
    """Multiple overlapping conflict sets: S1={H1,H2}, S2={H2,H3}, S3={H1,H3}.

    Min cardinality hitting set is size 2: e.g. {H1, H2} or {H1, H3} or {H2, H3}.
    With entrenchment H1=1, H2=2, H3=3:
    Weight of {H1, H2} = 1 + 2 = 3.
    Weight of {H1, H3} = 1 + 3 = 4.
    Weight of {H2, H3} = 2 + 3 = 5.
    Optimal minimal hitting set MUST be {H1, H2}!
    """
    tms = OperationalTMS()
    tms.add_hypothesis("H1", Atom("P1"), entrenchment=1)
    tms.add_hypothesis("H2", Atom("P2"), entrenchment=2)
    tms.add_hypothesis("H3", Atom("P3"), entrenchment=3)

    tms._active_conflicts.add(frozenset({"H1", "H2"}))
    tms._active_conflicts.add(frozenset({"H2", "H3"}))
    tms._active_conflicts.add(frozenset({"H1", "H3"}))

    retractions = tms.compute_minimal_retractions()
    assert len(retractions) == 1
    assert retractions[0] == frozenset({"H1", "H2"})


def test_edge_case_4_vacuous_revision() -> None:
    """Consistent state revision is vacuous: R = empty, 0 deactivated."""
    tms = OperationalTMS()
    tms.add_axiom("A1", Atom("P"))
    tms.add_hypothesis("H1", Atom("Q"))

    receipt = tms.revise()
    assert receipt.conflict_sets == ()
    assert receipt.retracted_hypotheses == frozenset()
    assert receipt.deactivated_nodes == ()
    assert "ax:A1" in receipt.surviving_beliefs
    assert "hyp:H1" in receipt.surviving_beliefs
    assert len(tms.history) == 1


def test_edge_case_5_immutable_axiom_error() -> None:
    """Attempting to retract a firm axiom raises ImmutableAxiomError."""
    tms = OperationalTMS()
    tms.add_axiom("A1", Atom("P"))
    with pytest.raises(ImmutableAxiomError):
        tms.retract_axiom("A1")


def test_edge_case_6_cascade_deactivation_down_dag() -> None:
    """Downstream derivations depending on retracted hypothesis are transitively deactivated."""
    tms = OperationalTMS()
    p = Atom("P")
    q = Atom("Q")
    r = Atom("R")

    n_p = tms.add_hypothesis("H1", p)
    n_q = tms.add_hypothesis("H2", q)
    n_not_q = tms.add_hypothesis("H3", Not(q))

    n_pq = tms.apply_inference(
        formula=And(p, q),
        kind=JustificationKind.CONJUNCTION_INTRO,
        antecedents=(n_p, n_q),
    )

    tms.add_axiom("A1", r)
    n_pqr = tms.apply_inference(
        formula=And(And(p, q), r),
        kind=JustificationKind.CONJUNCTION_INTRO,
        antecedents=(n_pq, "ax:A1"),
    )

    tms.detect_contradictions()
    assert frozenset({"H2", "H3"}) in tms.active_conflicts

    receipt = tms.revise(selected_retraction=frozenset({"H2"}))

    assert "hyp:H2" in receipt.deactivated_nodes
    assert n_pq in receipt.deactivated_nodes
    assert n_pqr in receipt.deactivated_nodes
    assert tms.get_node("hyp:H1").is_active is True
    assert tms.get_node("ax:A1").is_active is True
    assert tms.get_node("hyp:H3").is_active is True


# ============================================================================
# 5. AGM Belief Revision Postulate Verification
# ============================================================================

def test_agm_postulates_compliance() -> None:
    tms = OperationalTMS()
    tms.add_axiom("A1", Atom("StructureInvariance"))
    tms.add_hypothesis("H1", Atom("StateA"), entrenchment=1)
    tms.add_hypothesis("H2", Not(Atom("StateA")), entrenchment=2)

    receipt = tms.revise()
    verification = tms.verify_agm_postulates(receipt)

    assert verification["success"] is True
    assert verification["inclusion"] is True
    assert verification["consistency"] is True
    assert verification["axiom_invariance"] is True
    assert verification["vacuity"] is True


def test_revision_receipt_hashing_and_tamper_detection() -> None:
    tms = OperationalTMS()
    tms.add_hypothesis("H1", Atom("X"))
    tms.add_hypothesis("H2", Not(Atom("X")))

    receipt = tms.revise()
    assert len(receipt.justification_hash) == 64
    assert receipt.to_dict()["justification_hash"] == receipt.justification_hash

    recomputed_hash = tms._hash_receipt(
        receipt.conflict_sets,
        receipt.retracted_hypotheses,
        receipt.deactivated_nodes,
        receipt.surviving_beliefs,
    )
    assert receipt.justification_hash == recomputed_hash


# ============================================================================
# 6. Negative Controls Matrix & Branch Coverage
# ============================================================================

def test_negative_control_duplicate_ids() -> None:
    tms = OperationalTMS()
    tms.add_axiom("A1", Atom("P"))
    with pytest.raises(ValueError):
        tms.add_axiom("A1", Atom("Q"))

    tms.add_hypothesis("H1", Atom("P"))
    with pytest.raises(ValueError):
        tms.add_hypothesis("H1", Atom("Q"))


def test_negative_control_invalid_entrenchment() -> None:
    tms = OperationalTMS()
    with pytest.raises(ValueError):
        tms.add_hypothesis("H1", Atom("P"), entrenchment=0)


def test_negative_control_unknown_and_inactive_antecedents() -> None:
    tms = OperationalTMS()
    with pytest.raises(UnknownNodeError):
        tms.apply_inference(
            formula=Atom("P"),
            kind=JustificationKind.CONJUNCTION_INTRO,
            antecedents=("node:999",),
        )

    n_p = tms.add_hypothesis("H1", Atom("P"))
    tms.add_hypothesis("H2", Not(Atom("P")))
    tms.revise(selected_retraction=frozenset({"H1"}))

    with pytest.raises(InactiveNodeError):
        tms.apply_inference(
            formula=And(Atom("P"), Atom("P")),
            kind=JustificationKind.CONJUNCTION_INTRO,
            antecedents=(n_p, n_p),
        )


def test_negative_control_rule_violations() -> None:
    tms = OperationalTMS()
    p = Atom("P")
    q = Atom("Q")
    r = Atom("R")
    n_p = tms.add_axiom("A1", p)
    n_q = tms.add_axiom("A2", q)

    # Empty antecedents
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=p, kind=JustificationKind.MODUS_PONENS, antecedents=())

    # MP wrong number of antecedents
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=p, kind=JustificationKind.MODUS_PONENS, antecedents=(n_p,))

    # MP with non-implication
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=r, kind=JustificationKind.MODUS_PONENS, antecedents=(n_p, n_q))

    # Conjunction intro wrong count
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=And(p, q), kind=JustificationKind.CONJUNCTION_INTRO, antecedents=(n_p,))

    # Conjunction intro mismatched formula
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=p, kind=JustificationKind.CONJUNCTION_INTRO, antecedents=(n_p, n_q))

    # Conjunction elim left wrong count or non-And
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=p, kind=JustificationKind.CONJUNCTION_ELIM_LEFT, antecedents=(n_p, n_q))
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=p, kind=JustificationKind.CONJUNCTION_ELIM_LEFT, antecedents=(n_p,))

    # Conjunction elim right wrong count or non-And
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=q, kind=JustificationKind.CONJUNCTION_ELIM_RIGHT, antecedents=(n_p, n_q))
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=q, kind=JustificationKind.CONJUNCTION_ELIM_RIGHT, antecedents=(n_p,))

    # Disjunction intro left invalid
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=p, kind=JustificationKind.DISJUNCTION_INTRO_LEFT, antecedents=(n_p,))
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=Or(q, p), kind=JustificationKind.DISJUNCTION_INTRO_LEFT, antecedents=(n_p,))

    # Disjunction intro right invalid
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=p, kind=JustificationKind.DISJUNCTION_INTRO_RIGHT, antecedents=(n_p,))
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=Or(p, q), kind=JustificationKind.DISJUNCTION_INTRO_RIGHT, antecedents=(n_p,))

    # Resolution invalid
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=p, kind=JustificationKind.RESOLUTION, antecedents=(n_p,))
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=r, kind=JustificationKind.RESOLUTION, antecedents=(n_p, n_q))

    # Direct contradiction invalid
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=Bottom(), kind=JustificationKind.CONTRADICTION_DIRECT, antecedents=(n_p,))
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(formula=Bottom(), kind=JustificationKind.CONTRADICTION_DIRECT, antecedents=(n_p, n_q))

    # Valuation contradiction with identical values or wrong types
    n_val1 = tms.add_hypothesis("H1", EqVal("x", 5))
    n_val2 = tms.add_hypothesis("H2", EqVal("x", 5))
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(
            formula=Bottom(),
            kind=JustificationKind.CONTRADICTION_VALUATION,
            antecedents=(n_val1, n_val2),
        )
    with pytest.raises(InvalidInferenceError):
        tms.apply_inference(
            formula=Bottom(),
            kind=JustificationKind.CONTRADICTION_VALUATION,
            antecedents=(n_p, n_val1),
        )


def test_selected_retraction_errors() -> None:
    tms = OperationalTMS()
    tms.add_hypothesis("H1", Atom("P"))
    tms.add_hypothesis("H2", Not(Atom("P")))

    # Retraction fails to hit conflict
    with pytest.raises(ValueError, match="fails to hit conflict"):
        tms.revise(selected_retraction=frozenset({"H99"}))

    # Retraction attempts to include an axiom
    tms.add_axiom("A1", Atom("Invariant"))
    with pytest.raises(ImmutableAxiomError, match="Cannot include axiom"):
        tms.revise(selected_retraction=frozenset({"A1", "H1"}))


def test_empty_conflict_set_in_hitting_set_raises() -> None:
    tms = OperationalTMS()
    tms._active_conflicts.add(frozenset())
    with pytest.raises(FoundationalInconsistencyError):
        tms.compute_minimal_retractions()


def test_get_node_unknown() -> None:
    tms = OperationalTMS()
    with pytest.raises(UnknownNodeError):
        tms.get_node("invalid_node_id")


def test_multi_step_cycle_detection() -> None:
    tms = OperationalTMS()
    p = Atom("P")
    n1 = tms.add_hypothesis("H1", p)
    # n2 depends on n1
    n2 = tms.apply_inference(
        formula=Or(p, Atom("Q")),
        kind=JustificationKind.DISJUNCTION_INTRO_LEFT,
        antecedents=(n1,),
    )
    # n3 depends on n2
    n3 = tms.apply_inference(
        formula=Or(Or(p, Atom("Q")), Atom("R")),
        kind=JustificationKind.DISJUNCTION_INTRO_LEFT,
        antecedents=(n2,),
    )
    # cycle checking n1 against [n3]
    with pytest.raises(CircularDependencyError):
        tms._check_cycle(n1, [n3])


def test_conjunction_elim_mismatched_formula() -> None:
    tms = OperationalTMS()
    p = Atom("P")
    q = Atom("Q")
    r = Atom("R")
    n_and = tms.add_axiom("A1", And(p, q))

    with pytest.raises(InvalidInferenceError, match="Conjunction Elim Left failure"):
        tms.apply_inference(formula=r, kind=JustificationKind.CONJUNCTION_ELIM_LEFT, antecedents=(n_and,))

    with pytest.raises(InvalidInferenceError, match="Conjunction Elim Right failure"):
        tms.apply_inference(formula=r, kind=JustificationKind.CONJUNCTION_ELIM_RIGHT, antecedents=(n_and,))


def test_resolution_mismatched_formula() -> None:
    tms = OperationalTMS()
    p = Atom("P")
    q = Atom("Q")
    r = Atom("R")
    n_or = tms.add_axiom("A1", Or(p, q))
    n_not_p = tms.add_axiom("A2", Not(p))

    with pytest.raises(InvalidInferenceError, match="Resolution failure"):
        tms.apply_inference(formula=r, kind=JustificationKind.RESOLUTION, antecedents=(n_or, n_not_p))


def test_contradiction_valuation_mismatched_vars() -> None:
    tms = OperationalTMS()
    n1 = tms.add_hypothesis("H1", EqVal("var_x", 1))
    n2 = tms.add_hypothesis("H2", EqVal("var_y", 2))

    with pytest.raises(InvalidInferenceError, match="Contradiction Valuation failure"):
        tms.apply_inference(
            formula=Bottom(),
            kind=JustificationKind.CONTRADICTION_VALUATION,
            antecedents=(n1, n2),
        )


def test_verify_agm_postulates_with_inconsistency() -> None:
    tms = OperationalTMS()
    p = Atom("P")
    tms.add_hypothesis("H1", p)
    tms.add_hypothesis("H2", Not(p))

    fake_receipt = RevisionReceipt(
        conflict_sets=(),
        retracted_hypotheses=frozenset(),
        deactivated_nodes=(),
        surviving_beliefs=("hyp:H1", "hyp:H2"),
        justification_hash="fake",
    )
    postulates = tms.verify_agm_postulates(fake_receipt)
    assert postulates["consistency"] is False

    # Valuation inconsistency in surviving beliefs
    tms2 = OperationalTMS()
    tms2.add_hypothesis("H1", EqVal("x", 1))
    tms2.add_hypothesis("H2", EqVal("x", 2))
    fake_receipt2 = RevisionReceipt(
        conflict_sets=(),
        retracted_hypotheses=frozenset(),
        deactivated_nodes=(),
        surviving_beliefs=("hyp:H1", "hyp:H2"),
        justification_hash="fake2",
    )
    postulates2 = tms2.verify_agm_postulates(fake_receipt2)
    assert postulates2["consistency"] is False


def test_resolution_with_non_negation_raises() -> None:
    tms = OperationalTMS()
    n_or = tms.add_axiom("A1", Or(Atom("P"), Atom("Q")))
    n_r = tms.add_axiom("A2", Atom("R"))
    with pytest.raises(InvalidInferenceError, match="Resolution failure"):
        tms.apply_inference(
            formula=Atom("Q"),
            kind=JustificationKind.RESOLUTION,
            antecedents=(n_or, n_r),
        )


def test_contradiction_valuation_wrong_count_or_same_values() -> None:
    tms = OperationalTMS()
    n1 = tms.add_hypothesis("H1", EqVal("x", 1))
    with pytest.raises(InvalidInferenceError, match="Contradiction Valuation requires 2 antecedents"):
        tms.apply_inference(
            formula=Bottom(),
            kind=JustificationKind.CONTRADICTION_VALUATION,
            antecedents=(n1,),
        )

    n2 = tms.add_hypothesis("H2", EqVal("x", 1))
    with pytest.raises(InvalidInferenceError, match="Contradiction Valuation failure"):
        tms.apply_inference(
            formula=Bottom(),
            kind=JustificationKind.CONTRADICTION_VALUATION,
            antecedents=(n1, n2),
        )


def test_detect_contradictions_with_empty_support() -> None:
    # Direct contradiction with empty support in detect_contradictions
    tms = OperationalTMS()
    n1 = tms.add_axiom("A1", Atom("P"))
    # inject node without triggering add_axiom check
    just = tms.get_node(n1).justification
    tms._nodes["ax:A2"] = type(tms.get_node(n1))(
        node_id="ax:A2",
        formula=Not(Atom("P")),
        commitment=CommitmentClass.AXIOM,
        justification=just,
        antecedents=(),
        support=frozenset(),
        is_active=True,
    )
    with pytest.raises(FoundationalInconsistencyError, match="Direct contradiction"):
        tms.detect_contradictions()

    # Valuation contradiction with empty support in detect_contradictions
    tms2 = OperationalTMS()
    n_v1 = tms2.add_axiom("A1", EqVal("v", 10))
    tms2._nodes["ax:A2"] = type(tms2.get_node(n_v1))(
        node_id="ax:A2",
        formula=EqVal("v", 20),
        commitment=CommitmentClass.AXIOM,
        justification=just,
        antecedents=(),
        support=frozenset(),
        is_active=True,
    )
    with pytest.raises(FoundationalInconsistencyError, match="Conflicting operational valuations"):
        tms2.detect_contradictions()

    # Bottom node with empty support in detect_contradictions
    tms3 = OperationalTMS()
    n_b = tms3.add_axiom("A1", Atom("X"))
    tms3._nodes["ax:Bot"] = type(tms3.get_node(n_b))(
        node_id="ax:Bot",
        formula=Bottom(),
        commitment=CommitmentClass.AXIOM,
        justification=just,
        antecedents=(),
        support=frozenset(),
        is_active=True,
    )
    with pytest.raises(FoundationalInconsistencyError, match="Absurdity node exists with empty support"):
        tms3.detect_contradictions()
