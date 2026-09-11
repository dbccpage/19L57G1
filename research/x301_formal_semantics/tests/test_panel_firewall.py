"""Unit, integration, and adversarial tests for Multi-Observer Panel Consensus and the Grounding Firewall.

Formalizes and tests: "Panel agreement is not truth."
Covers:
- Panel of N >= 3 independent observers with partial / coarse projections.
- Unanimous panel consensus on ungrounded or phantom assertions.
- Grounding Firewall refutation via executable carrier intervention.
- Firewall override of committee consensus:
  - Typed refusal: StepResult.refusal with retained state.
  - Strict preservation of carrier state unmutated (rejecting proposed illegal mutation).
  - Emission of immutable PanelIllusionReceipt with SHA-256 digest.
- Receipt integrity: tamper detection via SHA-256 checksum verification.
- Positive control: valid consensus with verified ground truth passes.
- Disagreement control: non-consensus panel yields standard refusal without illusion receipt.
- Panel size constraint: N < 3 rejected with ValueError.

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
    GroundingFirewall,
    Observer,
    Panel,
    PanelIllusionReceipt,
    RelationalModel,
    StepRefusalData,
    StepResult,
    add_instance_intervention,
    add_requirement_intervention,
    atom,
    evaluate,
    evaluate_with_grounding_firewall,
    remove_instance_intervention,
)


# ===========================================================================
# 1. Panel Construction & Sizing Invariants (Class 2 & 3)
# ===========================================================================

def test_panel_requires_at_least_three_observers():
    """Class 2: Panel protocol enforces N >= 3 observers; N < 3 raises ValueError."""
    obs1 = Observer("obs1", lambda m: m)
    obs2 = Observer("obs2", lambda m: m)

    # Empty observers
    with pytest.raises(ValueError, match="N >= 3"):
        Panel([])

    # N = 1
    with pytest.raises(ValueError, match="N >= 3"):
        Panel([obs1])

    # N = 2
    with pytest.raises(ValueError, match="N >= 3"):
        Panel([obs1, obs2])

    # N = 3 is accepted
    obs3 = Observer("obs3", lambda m: m)
    panel3 = Panel([obs1, obs2, obs3])
    assert len(panel3.observers) == 3


# ===========================================================================
# 2. Unanimous Panel False Consensus Refuted by Ground Carrier (Class 1 & 3)
# ===========================================================================

@pytest.fixture
def ground_carrier() -> RelationalModel:
    """Actual ground carrier state where form 0 holds only on datum 0."""
    return RelationalModel(
        data=("datum0", "datum1", "datum2"),
        forms=(1, 2),
        insts=frozenset({(0, (0,))}),
        rules=frozenset(),
        reqs=frozenset({(0, 1)}),
    )


def test_grounding_firewall_refutes_unanimous_panel_illusion_n3(ground_carrier: RelationalModel):
    """Class 1: N = 3 panel unanimously agrees on false claim; Grounding Firewall overrides and refuses."""
    # Target assertion phi: form 0 holds on datum 1
    phi = atom("0", "1")

    # Verify ground carrier truth: phi is FALSE on actual carrier!
    assert evaluate(ground_carrier, phi) == FALSE

    # Construct N = 3 observers with coarse / phantom projections
    def proj_rule(m: RelationalModel) -> RelationalModel:
        # Observer A projects form 0 with all-tuples rule
        return RelationalModel(
            data=m.data, forms=m.forms, insts=m.insts, rules=m.rules | {0}, reqs=m.reqs
        )

    def proj_phantom_inst(m: RelationalModel) -> RelationalModel:
        # Observer B projects with phantom instance on datum 1
        return RelationalModel(
            data=m.data, forms=m.forms, insts=m.insts | {(0, (1,))}, rules=m.rules, reqs=m.reqs
        )

    def proj_collapsed_view(m: RelationalModel) -> RelationalModel:
        # Observer C projects with phantom instance on datum 1
        return RelationalModel(
            data=m.data, forms=m.forms, insts=m.insts | {(0, (1,))}, rules=m.rules, reqs=m.reqs
        )

    obs_a = Observer("obs_a_rule", proj_rule, "Projects form 0 as all-tuples rule")
    obs_b = Observer("obs_b_phantom", proj_phantom_inst, "Projects phantom instance (0, 1)")
    obs_c = Observer("obs_c_collapsed", proj_collapsed_view, "Projects collapsed view")

    panel = Panel([obs_a, obs_b, obs_c])
    assert len(panel.observers) == 3

    # All 3 observers unanimously vote TRUE for phi
    is_agree, consensus_val = panel.unanimous_consensus(ground_carrier, phi)
    assert is_agree is True
    assert consensus_val == TRUE
    assert panel.has_positive_consensus(ground_carrier, phi) is True

    # Counterfactual intervention pool on ground carrier
    candidate_interventions = [
        remove_instance_intervention(0, (0,), name="remove_datum0"),
        add_requirement_intervention(1, 2, name="req_1_2"),
    ]

    # Proposed illegal state mutation based on false consensus
    illegal_mutated_state = RelationalModel(
        data=ground_carrier.data,
        forms=ground_carrier.forms,
        insts=ground_carrier.insts | {(1, (1, 2))},
        rules=ground_carrier.rules,
        reqs=ground_carrier.reqs,
    )

    # Execute Grounding Firewall
    step_result = evaluate_with_grounding_firewall(
        model=ground_carrier,
        formula=phi,
        panel=panel,
        candidate_interventions=candidate_interventions,
        proposed_mutation=illegal_mutated_state,
    )

    # Invariants under Grounding Firewall:
    # 1. Step is a typed refusal
    assert step_result.is_success is False
    assert step_result.is_refusal is True

    # 2. State is strictly preserved unmutated (not mutated to illegal_mutated_state)
    assert step_result.state == ground_carrier
    assert step_result.state != illegal_mutated_state

    # 3. Refusal descriptor access
    assert isinstance(step_result.refusal, StepRefusalData)
    assert step_result.refusal.retained_state == ground_carrier
    assert "override" in step_result.refusal.reason.lower()

    # 4. PanelIllusionReceipt is emitted and valid
    receipt = step_result.receipt
    assert receipt is not None
    assert isinstance(receipt, PanelIllusionReceipt)
    assert receipt.schema == "panel-illusion-v1"
    assert receipt.panel_size == 3
    assert receipt.observer_ids == ("obs_a_rule", "obs_b_phantom", "obs_c_collapsed")
    assert receipt.panel_verdict is True
    assert receipt.ground_truth_verdict is False
    assert receipt.firewall_action == "STEP_REFUSAL_STATE_PRESERVED"
    assert receipt.refuting_intervention != ""
    assert receipt.verify_checksum() is True


def test_grounding_firewall_scale_n5_observers(ground_carrier: RelationalModel):
    """Class 1: Panel of N = 5 observers unanimously agreeing on false assertion."""
    phi = atom("0", "2")
    assert evaluate(ground_carrier, phi) == FALSE

    # 5 observers with coarse projections that certify phi
    def make_coarse_obs(idx: int) -> Observer:
        return Observer(
            f"obs_{idx}",
            lambda m: RelationalModel(
                data=m.data, forms=m.forms, insts=m.insts | {(0, (2,))}, rules=m.rules, reqs=m.reqs
            ),
        )

    observers = [make_coarse_obs(i) for i in range(5)]
    panel = Panel(observers)
    assert len(panel.observers) == 5

    assert panel.has_positive_consensus(ground_carrier, phi) is True

    candidate_interventions = [
        remove_instance_intervention(0, (0,), name="rem_inst_0"),
    ]

    step_result = evaluate_with_grounding_firewall(
        model=ground_carrier,
        formula=phi,
        panel=panel,
        candidate_interventions=candidate_interventions,
    )

    assert step_result.is_refusal is True
    assert step_result.state == ground_carrier
    assert step_result.receipt is not None
    assert step_result.receipt.panel_size == 5
    assert step_result.receipt.verify_checksum() is True


# ===========================================================================
# 3. Receipt Integrity & Adversarial Tampering Checks (Class 2)
# ===========================================================================

def test_panel_illusion_receipt_tamper_detection():
    """Class 2: Tampering with receipt payload invalidates SHA-256 checksum."""
    receipt = PanelIllusionReceipt.create(
        formula_repr="0(1)",
        panel_size=3,
        observer_ids=["o1", "o2", "o3"],
        refuting_intervention="rem_inst",
        observable_readout_before="0",
        observable_readout_after="0",
        panel_verdict=True,
        ground_truth_verdict=False,
    )

    # Initial receipt is authentic
    assert receipt.verify_checksum() is True

    # Tampered receipt: altered panel_verdict
    tampered_verdict = PanelIllusionReceipt(
        schema=receipt.schema,
        timestamp=receipt.timestamp,
        formula_repr=receipt.formula_repr,
        panel_size=receipt.panel_size,
        observer_ids=receipt.observer_ids,
        panel_verdict=False,  # TAMPERED
        refuting_intervention=receipt.refuting_intervention,
        observable_readout_before=receipt.observable_readout_before,
        observable_readout_after=receipt.observable_readout_after,
        ground_truth_verdict=receipt.ground_truth_verdict,
        firewall_action=receipt.firewall_action,
        receipt_sha256=receipt.receipt_sha256,
    )
    assert tampered_verdict.verify_checksum() is False

    # Tampered receipt: altered ground_truth_verdict
    tampered_gt = PanelIllusionReceipt(
        schema=receipt.schema,
        timestamp=receipt.timestamp,
        formula_repr=receipt.formula_repr,
        panel_size=receipt.panel_size,
        observer_ids=receipt.observer_ids,
        panel_verdict=receipt.panel_verdict,
        refuting_intervention=receipt.refuting_intervention,
        observable_readout_before=receipt.observable_readout_before,
        observable_readout_after=receipt.observable_readout_after,
        ground_truth_verdict=True,  # TAMPERED
        firewall_action=receipt.firewall_action,
        receipt_sha256=receipt.receipt_sha256,
    )
    assert tampered_gt.verify_checksum() is False


# ===========================================================================
# 4. Positive and Non-Consensus Controls (Class 3)
# ===========================================================================

def test_positive_control_panel_and_ground_agree(ground_carrier: RelationalModel):
    """Class 3: When panel and ground carrier both certify TRUE, mutation is accepted."""
    # True claim on carrier: form 0 holds on datum 0
    phi_true = atom("0", "0")
    assert evaluate(ground_carrier, phi_true) == TRUE

    # 3 transparent observers
    obs1 = Observer("obs1", lambda m: m)
    obs2 = Observer("obs2", lambda m: m)
    obs3 = Observer("obs3", lambda m: m)
    panel = Panel([obs1, obs2, obs3])

    mutated_state = RelationalModel(
        data=ground_carrier.data,
        forms=ground_carrier.forms,
        insts=ground_carrier.insts | {(0, (1,))},
        rules=ground_carrier.rules,
        reqs=ground_carrier.reqs,
    )

    step_result = evaluate_with_grounding_firewall(
        model=ground_carrier,
        formula=phi_true,
        panel=panel,
        candidate_interventions=[],
        proposed_mutation=mutated_state,
    )

    assert step_result.is_success is True
    assert step_result.is_refusal is False
    assert step_result.state == mutated_state
    assert step_result.receipt is None


def test_dissenting_panel_yields_standard_refusal_without_illusion(ground_carrier: RelationalModel):
    """Class 3: When panel does not reach consensus, refusal occurs without illusion receipt."""
    phi = atom("0", "0")

    # Observer 1 is transparent (sees True), Observer 2 hides instances (sees False)
    obs1 = Observer("obs1", lambda m: m)
    obs2 = Observer("obs2", lambda m: RelationalModel(data=m.data, forms=m.forms))
    obs3 = Observer("obs3", lambda m: m)
    panel = Panel([obs1, obs2, obs3])

    is_agree, _ = panel.unanimous_consensus(ground_carrier, phi)
    assert is_agree is False

    step_result = evaluate_with_grounding_firewall(
        model=ground_carrier,
        formula=phi,
        panel=panel,
        candidate_interventions=[],
    )

    assert step_result.is_success is False
    assert step_result.is_refusal is True
    assert step_result.state == ground_carrier
    assert step_result.receipt is None
    assert "did not certify" in (step_result.reason or "")
