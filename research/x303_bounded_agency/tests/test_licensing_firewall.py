"""Soviet invariant test suite for Alpha Engine Licensing, Grounding Firewall, and State Immutability.

Tested Invariants:
1. Invariant Class 1 (Zero Unilateral Authority): Carrier state cannot be mutated
   without an explicit metatheoretic License authorizing the action's canonical key.
2. Invariant Class 1 (Strict State Immutability on Refusal): Across every refusal path
   (fuel exhaustion, boundary violation, authorization denial, firewall override),
   the machine state is preserved strictly unmutated (state_after is state_before).
3. Invariant Class 1 (Grounding Firewall Consensus Override): When a multi-observer
   committee (N >= 3) unanimously certifies an action contradicted by ground carrier reality,
   the Grounding Firewall overrides the consensus, emits a PanelIllusionReceipt, and refuses.
4. Invariant Class 2 (Multi-Step Operational Lifecycle): Sequential agent transitions
   monotonically consume fuel, maintain FIFO memory records, and cleanly halt on budget exhaustion.
5. Invariant Class 3 (Cryptographic Determinism): Emitted AgencyReceipt audit structures
   produce deterministic, tamper-evident SHA-256 digests.

AuthorityEffect: None.
Epistemic Posture: Claim Hygiene Compliant (bounded, receipt-grounded).
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
CODE_DIR = REPO_ROOT / "code"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))
for _sub in ["x301_formal_semantics"]:
    _sub_path = REPO_ROOT / "research" / _sub
    if str(_sub_path) not in sys.path:
        sys.path.insert(0, str(_sub_path))

from research.x301_formal_semantics.semantics import (
    Atom,
    Identity,
    Observer,
    Panel,
    PanelIllusionReceipt,
    RelationalModel,
)
from research.x303_bounded_agency.agency import (
    ActionAuthorizer,
    AgencyReceipt,
    AgentController,
    CandidateAction,
    LicensedDriver,
    RefusalReason,
    StepResult,
    UnlicensedActionError,
    ViabilityEnvelope,
    add_instance_action,
    canonical_model_digest,
    remove_instance_action,
)


def _make_model() -> RelationalModel:
    return RelationalModel(
        data=("d0", "d1", "d2"),
        forms=(1, 2),
        insts=frozenset({(0, (0,))}),
        rules=frozenset(),
        reqs=frozenset(),
    )


# ---------------------------------------------------------------------------
# Invariant Class 1: Zero Unilateral Mutation Authority
# ---------------------------------------------------------------------------

def test_zero_unilateral_mutation_authority() -> None:
    """Invariant: Attempting to apply an action without an authorized license raises
    UnlicensedActionError and leaves carrier state unmutated.
    """
    model = _make_model()
    digest_before = canonical_model_digest(model)

    driver = LicensedDriver()
    authorizer = ActionAuthorizer()

    action = add_instance_action(form=0, args=(1,), fuel_cost=1)
    projected = action.apply(model)
    correct_key = action.get_canon_key(projected)

    # 1. License with an empty authorization list
    empty_license = authorizer.issue_license([])
    with pytest.raises(UnlicensedActionError) as exc_info:
        driver.apply_licensed(model, action, empty_license)
    assert "not authorized" in str(exc_info.value)
    assert canonical_model_digest(model) == digest_before

    # 2. License authorizing a completely different key
    bogus_key = (99, (1,), (), (), ())
    wrong_license = authorizer.issue_license([bogus_key])
    with pytest.raises(UnlicensedActionError):
        driver.apply_licensed(model, action, wrong_license)
    assert canonical_model_digest(model) == digest_before

    # 3. Valid license authorizing the exact canonical key succeeds
    valid_license = authorizer.issue_license([correct_key])
    new_model = driver.apply_licensed(model, action, valid_license)
    assert (0, (1,)) in new_model.insts
    assert (0, (1,)) not in model.insts


# ---------------------------------------------------------------------------
# Invariant Class 1: Grounding Firewall Consensus Override
# ---------------------------------------------------------------------------

def test_grounding_firewall_overrides_illusory_committee_consensus() -> None:
    """Invariant: When an N >= 3 observer panel unanimously certifies a formula
    that is false on ground carrier reality, the Grounding Firewall overrides
    consensus, emits a PanelIllusionReceipt, and refuses the step.
    """
    # Create carrier where form 0 has no instance (0, (2,))
    model = _make_model()
    target_formula = Atom(rel="form_0", args=("2",))  # Checks (0, (2,)) in insts

    # Construct a panel of N = 3 observers with a shared ungrounded illusion:
    # They project the model as having the instance (0, (2,))
    def illusory_projection(m: RelationalModel) -> RelationalModel:
        return RelationalModel(
            data=m.data,
            forms=m.forms,
            insts=m.insts | {(0, (2,))},  # Illusory instance injected into observer projection
            rules=m.rules,
            reqs=m.reqs,
        )

    obs1 = Observer(observer_id="obs_alpha", projection_fn=illusory_projection)
    obs2 = Observer(observer_id="obs_beta", projection_fn=illusory_projection)
    obs3 = Observer(observer_id="obs_gamma", projection_fn=illusory_projection)
    panel = Panel(observers=(obs1, obs2, obs3))

    # Observers unanimously perceive target_formula as TRUE
    assert panel.has_positive_consensus(model, target_formula)

    # Candidate action adds instance (0, (1,)) which does not satisfy target_formula on carrier
    action = add_instance_action(form=0, args=(1,), fuel_cost=1)

    env = ViabilityEnvelope(max_data=10, max_forms=5, max_arity=3, max_insts=10)
    controller = AgentController(
        state=model,
        envelope=env,
        total_fuel=10,
        goal_formula=target_formula,
    )

    # Execute step under the illusory panel
    result = controller.step([action], panel=panel)

    # Firewall must intervene: step is refused!
    assert result.is_refusal
    assert not result.is_success
    assert result.reason == RefusalReason.FIREWALL_CONSENSUS_OVERRIDE

    # Carrier state is strictly unmutated
    assert result.state is model
    assert controller.state is model

    # Audit receipt is a valid PanelIllusionReceipt
    assert isinstance(result.receipt, PanelIllusionReceipt)
    assert result.receipt.panel_size == 3
    assert result.receipt.panel_verdict is True
    assert result.receipt.ground_truth_verdict is False
    assert result.receipt.verify_checksum()


# ---------------------------------------------------------------------------
# Invariant Class 1: Universal State Immutability on Refusal
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "scenario",
    [
        "fuel_exhausted",
        "boundary_exceeded",
        "empty_candidates",
    ],
)
def test_refusal_state_immutability_matrix(scenario: str) -> None:
    """Invariant: In all refusal scenarios, result.state is state_before (exact reference identity)."""
    env = ViabilityEnvelope(max_data=3, max_forms=2, max_arity=2, max_insts=1)
    base_model = _make_model()

    if scenario == "fuel_exhausted":
        controller = AgentController(state=base_model, envelope=env, total_fuel=0)
        action = add_instance_action(form=0, args=(1,), fuel_cost=1)
        res = controller.step([action])
        assert res.is_refusal
        assert res.state is base_model

    elif scenario == "boundary_exceeded":
        controller = AgentController(state=base_model, envelope=env, total_fuel=10)
        # Adding an instance exceeds max_insts=1 (already has 1)
        violating_action = add_instance_action(form=0, args=(1,), fuel_cost=1)
        res = controller.step([violating_action])
        assert res.is_refusal
        assert res.state is base_model

    elif scenario == "empty_candidates":
        controller = AgentController(state=base_model, envelope=env, total_fuel=10)
        res = controller.step([])
        assert res.is_refusal
        assert res.state is base_model


# ---------------------------------------------------------------------------
# Invariant Class 2: Multi-Step Operational Lifecycle
# ---------------------------------------------------------------------------

def test_multi_step_agent_lifecycle() -> None:
    """Invariant: Sequential operational steps consume fuel monotonically,
    record transitions in bounded memory, and cleanly refuse when fuel reaches 0.
    """
    env = ViabilityEnvelope(
        max_data=10,
        max_forms=5,
        max_arity=3,
        max_insts=10,
    )
    initial_state = _make_model()
    total_fuel = 3

    controller = AgentController(
        state=initial_state,
        envelope=env,
        total_fuel=total_fuel,
        memory_horizon=5,
    )

    # Step 1: Add instance (0, (1,)) at cost 1
    act1 = add_instance_action(form=0, args=(1,), fuel_cost=1, name="step_1_add")
    res1 = controller.step([act1])
    assert res1.is_success
    assert controller.fuel == 2
    assert len(controller.memory) == 1
    assert (0, (1,)) in controller.state.insts

    # Step 2: Add instance (0, (2,)) at cost 2
    act2 = add_instance_action(form=0, args=(2,), fuel_cost=2, name="step_2_add")
    res2 = controller.step([act2])
    assert res2.is_success
    assert controller.fuel == 0
    assert len(controller.memory) == 2
    assert (0, (2,)) in controller.state.insts

    # Step 3: Attempt another action with 0 fuel remaining -> Clean refusal
    act3 = add_instance_action(form=1, args=(0, 1), fuel_cost=1, name="step_3_fail")
    state_before_refusal = controller.state
    res3 = controller.step([act3])

    assert res3.is_refusal
    assert res3.reason == RefusalReason.FUEL_EXHAUSTED
    assert res3.state is state_before_refusal
    # Memory was not incremented on refusal
    assert len(controller.memory) == 2


# ---------------------------------------------------------------------------
# Invariant Class 3: Deterministic Cryptographic Receipts
# ---------------------------------------------------------------------------

def test_deterministic_agency_receipt_digest() -> None:
    """Invariant: AgencyReceipt produces deterministic, tamper-evident SHA-256 digests."""
    r1 = AgencyReceipt.create(
        step_index=0,
        outcome="SUCCESS",
        pre_state_sha256="abc123pre",
        post_state_sha256="def456post",
        fuel_before=10,
        fuel_after=9,
        action_repr="add_inst(0, (1,))",
        timestamp="2026-09-12T00:00:00Z",
    )
    r2 = AgencyReceipt.create(
        step_index=0,
        outcome="SUCCESS",
        pre_state_sha256="abc123pre",
        post_state_sha256="def456post",
        fuel_before=10,
        fuel_after=9,
        action_repr="add_inst(0, (1,))",
        timestamp="2026-09-12T00:00:00Z",
    )

    # Identical inputs produce identical byte-pinned SHA-256 receipts
    assert r1.receipt_sha256 == r2.receipt_sha256
    assert len(r1.receipt_sha256) == 64
    assert r1.receipt_sha256 == r1.compute_sha256()

    # Tampering with any field alters the digest
    r_tampered = AgencyReceipt(
        schema=r1.schema,
        timestamp=r1.timestamp,
        step_index=r1.step_index,
        outcome=r1.outcome,
        refusal_reason=r1.refusal_reason,
        action_repr=r1.action_repr,
        pre_state_sha256=r1.pre_state_sha256,
        post_state_sha256="tampered_post_state",
        fuel_before=r1.fuel_before,
        fuel_after=r1.fuel_after,
        receipt_sha256=r1.receipt_sha256,
    )
    assert r_tampered.compute_sha256() != r1.receipt_sha256
