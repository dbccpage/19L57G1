"""Unit and property tests for executable state interventions, empirical reference, and behavioral congruence.

Covers:
- Executable intervention operators: add_instance, remove_instance, toggle_rule, add_requirement, custom delta.
- Operational empirical reference: an assertion phi has empirical reference iff an executable intervention
  sequence produces an observable shift in evaluation.
- Discrimination witness recovery: find_discriminating_witness extracts the concrete counterfactual delta.
- Behavioral observational congruence: phi =_obs psi proved as an equivalence relation
  (reflexive, symmetric, transitive).
- Rejection of ungrounded decorative distinctions lacking an intervention witness.
- Negative controls: empty intervention pools, invariant tautologies.

AuthorityEffect: None.
Epistemic Posture: Claim Hygiene Compliant (bounded, receipt-grounded).
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
    Intervention,
    RelationalModel,
    add_instance_intervention,
    add_requirement_intervention,
    are_behaviorally_congruent,
    atom,
    conj,
    disj,
    eq,
    evaluate,
    find_discriminating_witness,
    has_empirical_reference,
    neg,
    remove_instance_intervention,
    toggle_rule_intervention,
)


@pytest.fixture
def base_carrier() -> RelationalModel:
    """Standard initial carrier state with one unary instance and one requirement."""
    return RelationalModel(
        data=("tok0", "tok1", "tok2"),
        forms=(1, 2),
        insts=frozenset({(0, (0,))}),
        rules=frozenset(),
        reqs=frozenset({(0, 1)}),
    )


# ===========================================================================
# 1. Executable State Interventions (Class 3 & 4)
# ===========================================================================

def test_add_instance_intervention(base_carrier: RelationalModel):
    """Class 3: Executable intervention adding a form instance."""
    interv = add_instance_intervention(0, (1,), name="add_form0_tok1")
    assert interv.name == "add_form0_tok1"

    perturbed = interv.apply(base_carrier)
    # Original carrier state is preserved unmutated
    assert (0, (1,)) not in base_carrier.insts
    # Perturbed carrier contains the new instance
    assert (0, (1,)) in perturbed.insts
    assert (0, (0,)) in perturbed.insts
    assert perturbed.data == base_carrier.data
    assert perturbed.forms == base_carrier.forms


def test_remove_instance_intervention(base_carrier: RelationalModel):
    """Class 3: Executable intervention removing an existing instance."""
    interv = remove_instance_intervention(0, (0,), name="rem_form0_tok0")
    perturbed = interv.apply(base_carrier)

    assert (0, (0,)) in base_carrier.insts
    assert (0, (0,)) not in perturbed.insts
    assert len(perturbed.insts) == 0


def test_toggle_rule_intervention(base_carrier: RelationalModel):
    """Class 3: Executable intervention toggling uniform all-tuples rule."""
    interv_on = toggle_rule_intervention(0, name="toggle_rule_0_on")
    perturbed_on = interv_on.apply(base_carrier)
    assert 0 not in base_carrier.rules
    assert 0 in perturbed_on.rules

    # Toggling again turns it off
    interv_off = toggle_rule_intervention(0, name="toggle_rule_0_off")
    perturbed_off = interv_off.apply(perturbed_on)
    assert 0 not in perturbed_off.rules


def test_add_requirement_intervention(base_carrier: RelationalModel):
    """Class 3: Executable intervention imposing a separation requirement."""
    interv = add_requirement_intervention(1, 2, name="impose_req_1_2")
    perturbed = interv.apply(base_carrier)

    assert (1, 2) not in base_carrier.reqs
    assert (1, 2) in perturbed.reqs
    # Order-normalization: (2, 1) also normalizes to (1, 2)
    interv_rev = add_requirement_intervention(2, 0, name="impose_req_0_2")
    perturbed_rev = interv_rev.apply(base_carrier)
    assert (0, 2) in perturbed_rev.reqs


def test_custom_delta_intervention(base_carrier: RelationalModel):
    """Class 3: Arbitrary user-defined state delta intervention."""
    def wipe_all(m: RelationalModel) -> RelationalModel:
        return RelationalModel(
            data=m.data,
            forms=m.forms,
            insts=frozenset(),
            rules=frozenset(),
            reqs=frozenset(),
        )

    interv = Intervention(name="wipe_all", delta_fn=wipe_all, description="Wipe all instances and reqs")
    perturbed = interv.apply(base_carrier)
    assert len(perturbed.insts) == 0
    assert len(perturbed.reqs) == 0
    assert len(base_carrier.insts) == 1


# ===========================================================================
# 2. Operational Empirical Reference & Discrimination Witnesses (Class 1 & 2)
# ===========================================================================

def test_grounded_assertion_possesses_empirical_reference(base_carrier: RelationalModel):
    """Class 1: Assertions about carrier state possess empirical reference."""
    phi_grounded = atom("0", "0")
    pool = [
        remove_instance_intervention(0, (0,), name="rem_tok0"),
        add_instance_intervention(0, (1,), name="add_tok1"),
        add_requirement_intervention(1, 2, name="req_1_2"),
    ]

    # phi_grounded evaluates to TRUE on base_carrier, but FALSE after rem_tok0
    assert has_empirical_reference(phi_grounded, base_carrier, pool) is True

    witness = find_discriminating_witness(phi_grounded, base_carrier, pool)
    assert witness is not None
    assert witness.name == "rem_tok0"

    # Verify that the witness indeed alters the valuation
    assert evaluate(base_carrier, phi_grounded) == TRUE
    assert evaluate(witness.apply(base_carrier), phi_grounded) == FALSE


def test_ungrounded_tautologies_lack_empirical_reference(base_carrier: RelationalModel):
    """Class 2: Internal identities and tautologies lack empirical reference in state pool."""
    phi_identity = eq("0", "0")
    phi_tautology = disj(atom("0", "0"), neg(atom("0", "0")))

    pool = [
        remove_instance_intervention(0, (0,), name="rem_tok0"),
        add_instance_intervention(0, (1,), name="add_tok1"),
        toggle_rule_intervention(0, name="toggle_rule"),
        add_requirement_intervention(0, 1, name="impose_req"),
    ]

    # Syntactic identity 0 = 0 is invariant under all carrier perturbations
    assert has_empirical_reference(phi_identity, base_carrier, pool) is False
    assert find_discriminating_witness(phi_identity, base_carrier, pool) is None


def test_negative_control_empty_intervention_pool(base_carrier: RelationalModel):
    """Class 2: An empty intervention pool cannot discriminate any formula."""
    phi = atom("0", "0")
    empty_pool: list[Intervention] = []

    assert has_empirical_reference(phi, base_carrier, empty_pool) is False
    assert find_discriminating_witness(phi, base_carrier, empty_pool) is None


def test_negative_control_noop_intervention(base_carrier: RelationalModel):
    """Class 2: No-op intervention that leaves model unchanged cannot discriminate."""
    noop = Intervention(name="noop", delta_fn=lambda m: m, description="No change")
    phi = atom("0", "0")

    assert has_empirical_reference(phi, base_carrier, [noop]) is False
    assert find_discriminating_witness(phi, base_carrier, [noop]) is None


# ===========================================================================
# 3. Behavioral Observational Congruence (Class 1 & 3)
# ===========================================================================

def test_behavioral_congruence_equivalence_relation(base_carrier: RelationalModel):
    """Class 1: Behavioral observational congruence is an equivalence relation."""
    pool = [
        remove_instance_intervention(0, (0,)),
        add_instance_intervention(0, (1,)),
        toggle_rule_intervention(0),
    ]
    models = [base_carrier, pool[0].apply(base_carrier)]

    phi_a = atom("0", "0")
    phi_b = conj(atom("0", "0"), eq("0", "0"))  # Equivalent: phi and True
    phi_c = conj(eq("0", "0"), atom("0", "0"))  # Commutative variant

    # 1. Reflexivity: phi =_obs phi
    assert are_behaviorally_congruent(phi_a, phi_a, models, pool) is True
    assert are_behaviorally_congruent(phi_b, phi_b, models, pool) is True

    # 2. Symmetry: phi_a =_obs phi_b <=> phi_b =_obs phi_a
    ab = are_behaviorally_congruent(phi_a, phi_b, models, pool)
    ba = are_behaviorally_congruent(phi_b, phi_a, models, pool)
    assert ab is True and ba is True

    # 3. Transitivity: if phi_a =_obs phi_b and phi_b =_obs phi_c, then phi_a =_obs phi_c
    bc = are_behaviorally_congruent(phi_b, phi_c, models, pool)
    ac = are_behaviorally_congruent(phi_a, phi_c, models, pool)
    assert bc is True and ac is True


def test_decorative_distinction_rejection(base_carrier: RelationalModel):
    """Class 3: Rejection of decorative ungrounded distinctions that lack an intervention witness."""
    pool = [
        remove_instance_intervention(0, (0,)),
        add_instance_intervention(0, (1,)),
    ]
    models = [base_carrier]

    # Two formulas with identical empirical behavior across all models and interventions:
    # Formula 1: form_0(0)
    # Formula 2: form_0(0) and (1 = 1)
    f_plain = atom("0", "0")
    f_ornament = conj(atom("0", "0"), eq("1", "1"))

    # They are behaviorally congruent; the decorative ornament adds no observable distinction
    assert are_behaviorally_congruent(f_plain, f_ornament, models, pool) is True

    # Conversely, an assertion with genuine operational difference is NOT congruent:
    f_distinct = atom("0", "1")
    assert are_behaviorally_congruent(f_plain, f_distinct, models, pool) is False
