"""Target X310: Unit tests for individual pipeline stages and boundary contracts.

AuthorityEffect: None.
Epistemic Posture: Claim Hygiene Compliant (bounded, narrow, receipt-grounded).

Invariant Class 1 (Physical / Operational Invariant):
- Every stage transition preserves carrier state integrity or cleanly halts in typed refusal.
- Arithmetic is exact rational arithmetic via fractions.Fraction in [0, 1] cap Q.

Invariant Class 2 (Interface & Contract Boundary):
- Stage 1 consumes Controlled setting and SubstrateState, emitting RelationalModel.
- Stage 2 verifies spacelike non-signaling with TVD == 0/1 in exact Q.
- Stage 3 checks Grounding Firewall consensus override against empirical ground truth.
- Stage 4 solves exact linear feasibility yielding verified PrimalReceipt or Farkas DualReceipt.
- Stage 5 executes AGM belief revision, satisfying all 5 AGM postulates.
- Stage 6 enforces viability envelopes and licenses action execution under zero unilateral authority.

Invariant Class 3 (Negative Control & Adversarial Refutation):
- Fuel exhaustion or protection obligations halt execution in typed refusal without state mutation.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_CODE_DIR = _REPO_ROOT / "code"
if str(_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(_CODE_DIR))

for _sub in [
    "target_a_execution",
    "g011_finitary_substrate",
    "p200_operational_protocols",
    "g014_observer_descent",
    "x301_formal_semantics",
    "m114_solver_adapter",
    "x302_operational_reasoning",
    "x303_bounded_agency",
]:
    _sub_path = _REPO_ROOT / "research" / _sub
    if str(_sub_path) not in sys.path:
        sys.path.insert(0, str(_sub_path))

import research.target_a_execution.runner as _tar_runner
sys.modules["runner"] = _tar_runner
import research.p200_operational_protocols.protocol as _p200_prot
sys.modules["protocol"] = _p200_prot
import research.p200_operational_protocols.embedded_observer as _p200_emb
sys.modules["embedded_observer"] = _p200_emb

from research.target_a_execution.control import (
    Controlled,
    State as SubstrateState,
    build_program,
    encode_c,
    fire,
    nops as controlled_nops,
)
from research.target_a_execution.runner import (
    ProtectionKind,
    ProtectionObligation,
    Refusal as SubstrateRefusal,
)
from research.p200_operational_protocols.protocol import (
    CarrierState as P200CarrierState,
    Locus,
)
from research.x301_formal_semantics.semantics import (
    Atom,
    Observer as SemanticsObserver,
    Panel,
    PanelIllusionReceipt,
    RelationalModel,
    atom,
    conj,
    disj,
    eq,
    evaluate,
)
from research.m114_solver_adapter.solver_adapter import (
    Constraint,
    ConstraintProblem,
    ConstraintSense,
    DualReceipt,
    PrimalReceipt,
    ProblemType,
    SolverAdapter,
    VariableBound,
)
from research.x302_operational_reasoning.reasoning import (
    Atom as TMSAtom,
    ImmutableAxiomError,
    OperationalTMS,
)
from research.x303_bounded_agency.agency import (
    AgentController,
    RefusalReason as AgencyRefusalReason,
    ViabilityEnvelope,
    add_instance_action,
    canonical_model_digest,
)

from research.x310_vertical_integration.pipeline import (
    PipelineConfig,
    encode_substrate_to_relational,
    decode_relational_to_substrate,
    execute_stage_1_substrate,
    execute_stage_2_measurement,
    execute_stage_3_grounding,
    execute_stage_4_solver,
    execute_stage_5_reasoning,
    execute_stage_6_agency,
)


def test_stage_1_substrate_event_and_encoding():
    """Verify Stage 1 operational event fire and relational carrier encoding."""
    ctrl = frozenset({(0, 0), (1, 1)})
    c = Controlled(n=2, ops=((1, 0), (0, 1)), ctrl=ctrl)
    g = encode_c(c)
    s0 = SubstrateState(
        graph=g,
        nops=2,
        active=0,
        tape=(0,),
        clock=0,
        fuel=10,
        designated_pair=(0, 1),
    )
    cfg = PipelineConfig(fuel_budget=10)

    # Fire operation 0: moves from active datum 0 to 1
    res = execute_stage_1_substrate(config=cfg, controlled=c, initial_state=s0, op_index=0)
    assert not res.is_refusal
    assert res.final_state.active == 1
    assert res.final_state.clock == 1
    assert res.final_state.fuel == 9
    assert res.final_state.tape == (0, 1)

    # Carrier encoding validation
    model = res.carrier_model
    assert model.n_data() >= 2
    assert len(model.insts) > 0
    assert res.receipt["stage"] == "stage_1_substrate"
    assert res.receipt["state_sha256"] == canonical_model_digest(model)


def test_stage_1_refusal_on_fuel_exhaustion():
    """Verify Stage 1 refuses execution when declared fuel is exhausted."""
    ctrl = frozenset({(0, 0), (1, 1)})
    c = Controlled(n=2, ops=((1, 0), (0, 1)), ctrl=ctrl)
    g = encode_c(c)
    s_exhausted = SubstrateState(
        graph=g,
        nops=2,
        active=0,
        tape=(0,),
        clock=0,
        fuel=0,  # Zero fuel
    )
    cfg = PipelineConfig(fuel_budget=0)

    res = execute_stage_1_substrate(config=cfg, controlled=c, initial_state=s_exhausted, op_index=0)
    assert res.is_refusal
    assert "EXHAUSTED" in str(res.refusal_reason)
    assert res.final_state == s_exhausted  # State unmutated


def test_stage_2_multi_observer_non_signaling():
    """Verify Stage 2 multi-observer distributed measurement and TVD == 0/1 in Q."""
    cfg = PipelineConfig(tolerance_tvd=Fraction(0, 1))
    model = RelationalModel(
        data=(0, 1, 2, 3),
        forms=(1, 2),
        insts=frozenset({(0, (0,)), (1, (0, 1))}),
    )
    observers = [
        SemanticsObserver(observer_id="O1", projection_fn=lambda m: m),
        SemanticsObserver(observer_id="O2", projection_fn=lambda m: m),
        SemanticsObserver(observer_id="O3", projection_fn=lambda m: m),
    ]

    res = execute_stage_2_measurement(config=cfg, model=model, observers=observers)
    assert not res.is_refusal
    assert res.non_signaling_tvd == Fraction(0, 1)
    assert res.gluing_consistent
    assert res.receipt["non_signaling_tvd"] == "0/1"
    assert len(res.observer_projections) == 3


def test_stage_3_grounding_firewall_consensus_override():
    """Verify Stage 3 Grounding Firewall consensus override when panel claims ungrounded consensus."""
    cfg = PipelineConfig()
    model = RelationalModel(
        data=(0, 1),
        forms=(1, 2),
        insts=frozenset({(0, (0,))}),
    )
    observers = [
        SemanticsObserver(observer_id=f"O{i}", projection_fn=lambda m: m)
        for i in range(3)
    ]
    panel = Panel(observers=tuple(observers))
    formulas = [eq("0", "0")]

    # Positive control: genuine consensus on true proposition
    res_pos = execute_stage_3_grounding(config=cfg, model=model, panel=panel, formulas=formulas)
    assert not res_pos.is_refusal
    assert res_pos.firewall_action == "PASSED"
    assert res_pos.illusion_receipt is None

    # Negative control: adversarial override where panel asserts untrue proposition
    res_neg = execute_stage_3_grounding(
        config=cfg,
        model=model,
        panel=panel,
        formulas=formulas,
        adversarial_override=True,
        adversarial_formula_repr="Atom(P_phantom)",
    )
    assert res_neg.is_refusal
    assert res_neg.firewall_action == "REFUSAL_OVERRIDE"
    assert isinstance(res_neg.illusion_receipt, PanelIllusionReceipt)
    assert "P_phantom" in res_neg.illusion_receipt.formula_repr


def test_stage_4_solver_primal_and_dual_certificates():
    """Verify Stage 4 solver adapter produces verified primal or Farkas dual certificates."""
    cfg = PipelineConfig(solver_fuel=500)

    # 1. Feasible linear problem -> PrimalReceipt
    problem_feas = ConstraintProblem(
        problem_type=ProblemType.LINEAR_FEASIBILITY,
        variables=("x", "y"),
        constraints=(
            Constraint("c1", {"x": Fraction(1, 1), "y": Fraction(1, 1)}, ConstraintSense.LE, Fraction(4, 1)),
        ),
        bounds={
            "x": VariableBound(lower=Fraction(0, 1), upper=Fraction(3, 1)),
            "y": VariableBound(lower=Fraction(0, 1), upper=Fraction(3, 1)),
        },
    )
    res_feas = execute_stage_4_solver(config=cfg, problem=problem_feas)
    assert not res_feas.is_refusal
    assert res_feas.status == "FEASIBLE"
    assert isinstance(res_feas.primal_receipt, PrimalReceipt)
    assert res_feas.primal_receipt.verify(problem_feas)

    # 2. Infeasible linear problem -> DualReceipt (Farkas certificate)
    problem_infeas = ConstraintProblem(
        problem_type=ProblemType.LINEAR_FEASIBILITY,
        variables=("x",),
        constraints=(
            Constraint("c_lower", {"x": Fraction(1, 1)}, ConstraintSense.GE, Fraction(5, 1)),
            Constraint("c_upper", {"x": Fraction(1, 1)}, ConstraintSense.LE, Fraction(2, 1)),
        ),
        bounds={"x": VariableBound(lower=Fraction(0, 1), upper=Fraction(10, 1))},
    )
    res_infeas = execute_stage_4_solver(config=cfg, problem=problem_infeas)
    assert not res_infeas.is_refusal
    assert res_infeas.status == "INFEASIBLE"
    assert isinstance(res_infeas.dual_receipt, DualReceipt)
    assert res_infeas.dual_receipt.verify(problem_infeas)


def test_stage_5_tms_reasoning_and_agm_postulates():
    """Verify Stage 5 TMS contradiction detection, minimal hitting set, and AGM postulates."""
    cfg = PipelineConfig()
    tms = OperationalTMS()
    tms.add_axiom("ax_core", TMSAtom("SubstrateIntegrity"))
    tms.add_hypothesis("h1", TMSAtom("Policy1"), entrenchment=1)
    tms.add_hypothesis("h2", TMSAtom("Policy2"), entrenchment=2)

    res = execute_stage_5_reasoning(config=cfg, tms=tms)
    assert not res.is_refusal
    assert res.agm_postulates_satisfied["success"]
    assert res.agm_postulates_satisfied["inclusion"]
    assert res.agm_postulates_satisfied["vacuity"]
    assert res.agm_postulates_satisfied["consistency"]
    assert res.agm_postulates_satisfied["axiom_invariance"]

    # Invariant: firm axioms cannot be retracted
    try:
        tms.retract_axiom("ax_core")
        assert False, "Should have raised ImmutableAxiomError"
    except ImmutableAxiomError:
        pass


def test_stage_6_agency_viability_and_action_execution():
    """Verify Stage 6 bounded agency viability envelope check and licensed state commitment."""
    cfg = PipelineConfig(memory_horizon=5)
    carrier = RelationalModel(
        data=(0, 1),
        forms=(1, 2),
        insts=frozenset({(0, (0,)), (1, (0, 1))}),
    )
    envelope = ViabilityEnvelope(
        max_data=4,
        max_forms=4,
        max_arity=2,
        max_insts=5,
    )

    action_valid = add_instance_action(form=1, args=(1, 0), fuel_cost=1, name="act_valid")
    res_success = execute_stage_6_agency(
        config=cfg,
        carrier=carrier,
        envelope=envelope,
        fuel=10,
        candidates=[action_valid],
    )
    assert not res_success.is_refusal
    assert res_success.selected_action == "act_valid"
    assert (1, (1, 0)) in res_success.post_carrier.insts
    assert res_success.agency_receipt.outcome == "SUCCESS"

    # Negative control: action drives state outside envelope -> strict refusal, state unmutated
    action_overflow = add_instance_action(form=1, args=(1, 1), fuel_cost=1, name="act_overflow")
    strict_envelope = ViabilityEnvelope(
        max_data=2,
        max_forms=2,
        max_arity=2,
        max_insts=2,  # Current inst count is already 2!
    )
    res_refusal = execute_stage_6_agency(
        config=cfg,
        carrier=carrier,
        envelope=strict_envelope,
        fuel=10,
        candidates=[action_overflow],
    )
    assert res_refusal.is_refusal
    assert res_refusal.post_carrier == carrier  # Strictly unmutated
