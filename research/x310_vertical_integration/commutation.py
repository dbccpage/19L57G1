"""Commutation and determinism audits. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Optional, Sequence

from . import _bootstrap  # noqa: F401
from research.p200_operational_protocols.commutation import step_l1, sweep_commutation
from research.p200_operational_protocols.protocol import (
    CarrierState as P200CarrierState,
    Locus,
    create_non_disturbing_readout,
)
from research.target_a_execution.control import Controlled, encode_c
from research.target_a_execution.control import State as SubstrateState
from research.x301_formal_semantics.semantics import (
    RelationalModel,
    add_instance_intervention,
    add_requirement_intervention,
)
from research.x303_bounded_agency.agency import (
    AgentController,
    ViabilityEnvelope,
    add_instance_action,
    canonical_model_digest,
)
from .codec import decode_relational_to_substrate, encode_substrate_to_relational
from .types import PipelineConfig

def audit_readout_step_commutation(
    states: Optional[Sequence[P200CarrierState]] = None,
) -> bool:
    """Verify programmatic commutation of readout and localized transition: R o S = S o R.

    When measurement readout R2 and step S1 have disjoint footprints:
    R2(S1(s)) == S1(R2(s)).
    """
    sample_states = list(states) if states is not None else [
        P200CarrierState(l1=0, l2=0, m=0, r1=0, r2=0, dist=0),
        P200CarrierState(l1=1, l2=0, m=0, r1=0, r2=0, dist=0),
        P200CarrierState(l1=0, l2=1, m=0, r1=0, r2=0, dist=0),
        P200CarrierState(l1=1, l2=1, m=0, r1=0, r2=0, dist=0),
    ]

    # Non-disturbing readout at Locus 2 targeting Register R2
    readout_inst = create_non_disturbing_readout(Locus.L2, Locus.R2)
    readout_op = readout_inst.readout

    # Local step operation at Locus 1
    step_op = step_l1(lambda x: 1 - x if x in (0, 1) else x)

    res = sweep_commutation(sample_states, readout_op, step_op)
    return bool(res["all_commute"])


def audit_codec_roundtrip_commutation(
    sample_states: Optional[Sequence[SubstrateState]] = None,
) -> bool:
    """Check sample round trips with tape and protection supplied separately.

    This audit does not compare transitions or prove full codec inversion.
    """
    if sample_states is None:
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
        s1 = SubstrateState(
            graph=g,
            nops=2,
            active=1,
            tape=(0, 1),
            clock=1,
            fuel=9,
            designated_pair=(0, 1),
        )
        sample_states = [s0, s1]

    for s in sample_states:
        encoded = encode_substrate_to_relational(s)
        decoded = decode_relational_to_substrate(
            model=encoded,
            nops=s.nops,
            tape=s.tape,
            protection_obligations=s.protection_obligations,
        )
        if decoded != s:
            return False
    return True


@dataclass(frozen=True)
class DescentSquare:
    """One count-level descent square for a supplied relational carrier."""

    initial_counts: tuple[tuple[str, int], ...]
    updated_counts: tuple[tuple[str, int], ...]
    commutes_a: bool
    commutes_b: bool
    reconstructs: bool

    @property
    def commutes(self) -> bool:
        return self.commutes_a and self.commutes_b and self.reconstructs


def build_sheaf_descent_square(carrier: Optional[RelationalModel] = None) -> DescentSquare:
    """Project one actual carrier through up to two independent X301 additions.

    Only four component counts descend; this is not gluing of the full model.
    An addition is an identity step when its declared probe family has no
    missing instance or requirement.
    """
    import research.g014_observer_descent.observer_descent as g14

    model = carrier if carrier is not None else RelationalModel(
        data=("a", "b"), forms=(1, 2), insts=frozenset({(0, (0,))}),
        reqs=frozenset(),
    )

    def project_counts(m: RelationalModel) -> g14.CarrierState:
        return g14.CarrierState.from_mapping({
            "data_count": len(m.data), "form_count": len(m.forms),
            "inst_count": len(m.insts), "req_count": len(m.reqs),
        })

    g_state = project_counts(model)
    obs_a = g14.Observer(observer_id="OA", loci=("data_count", "inst_count"))
    obs_b = g14.Observer(observer_id="OB", loci=("form_count", "req_count"))
    coverage = g14.DescentCoverage(observers=(obs_a, obs_b))

    missing_inst: tuple[int, tuple[int, ...]] | None = None
    if model.data:
        for form, arity in enumerate(model.forms):
            if arity < 1:
                continue
            for datum in range(min(len(model.data), 2)):
                candidate = (form, (datum,) * arity)
                if candidate not in model.insts:
                    missing_inst = candidate
                    break
            if missing_inst is not None:
                break
    missing_req = next(
        ((i, j) for i in range(len(model.data))
         for j in range(i + 1, len(model.data)) if (i, j) not in model.reqs),
        None,
    )

    updated_model = model
    if missing_inst is not None:
        updated_model = add_instance_intervention(*missing_inst).apply(updated_model)
    if missing_req is not None:
        updated_model = add_requirement_intervention(*missing_req).apply(updated_model)
    s_prime = project_counts(updated_model)

    def u_a(s: g14.CarrierState) -> g14.CarrierState:
        d = s.to_dict()
        d["inst_count"] += int(missing_inst is not None)
        return g14.CarrierState.from_mapping(d)

    def u_b(s: g14.CarrierState) -> g14.CarrierState:
        d = s.to_dict()
        d["req_count"] += int(missing_req is not None)
        return g14.CarrierState.from_mapping(d)

    pi_a_updated = obs_a.project(s_prime)
    u_a_proj = u_a(obs_a.project(g_state))
    pi_b_updated = obs_b.project(s_prime)
    u_b_proj = u_b(obs_b.project(g_state))
    local_records = {"OA": u_a_proj, "OB": u_b_proj}
    glued_res = coverage.glue(local_records)
    return DescentSquare(
        initial_counts=g_state.data,
        updated_counts=s_prime.data,
        commutes_a=(pi_a_updated == u_a_proj),
        commutes_b=(pi_b_updated == u_b_proj),
        reconstructs=glued_res.is_ok() and (glued_res.unwrap() == s_prime),
    )


def audit_sheaf_descent_commutation(carrier: Optional[RelationalModel] = None) -> bool:
    """Check count-level descent on the supplied carrier, if any."""
    return build_sheaf_descent_square(carrier).commutes


def audit_refusal_state_preservation(
    carrier: Optional[RelationalModel] = None,
) -> bool:
    """Verify refusal state preservation commutation: S_refusal(M) = M.

    Whenever a refusal occurs, the carrier state is strictly unmutated.
    """
    model = carrier or RelationalModel(
        data=(0, 1),
        forms=(1, 2),
        insts=frozenset({(0, (0,)), (1, (0, 1))}),
        rules=frozenset(),
        reqs=frozenset({(0, 1)}),
    )

    env = ViabilityEnvelope(
        max_data=max(model.n_data(), 2),
        max_forms=max(model.n_forms(), 2),
        max_arity=max(max(model.forms, default=2), 2),
        max_insts=len(model.insts),
    )

    # Action that exceeds instance ceiling -> triggers refusal
    new_form = 0
    new_arg = 0
    for f in range(model.n_forms()):
        for x in range(model.n_data()):
            if (f, (x,)) not in model.insts:
                new_form = f
                new_arg = x
                break
    bad_action = add_instance_action(form=new_form, args=(new_arg,), fuel_cost=10, name="bad_overflow")
    controller = AgentController(
        state=model,
        envelope=env,
        total_fuel=5,
        memory_horizon=5,
    )

    pre_digest = canonical_model_digest(model)
    res = controller.step(candidates=[bad_action])

    if not res.is_refusal:
        return False

    post_digest = canonical_model_digest(res.state)
    return (pre_digest == post_digest) and (res.state == model)


@dataclass(frozen=True)
class CommutationResidual:
    """Exact rational priced residual for a categorical commutation square.

    Evaluates whether a diagram commutes; if non-commuting, assigns an exact rational
    disturbance / obstruction price in Q >= 0/1. For strictly commuting squares,
    residual_price_q is exactly 0/1.
    """

    diagram_id: str
    commutes: bool
    residual_price_q: Fraction
    metric_name: str
    description: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "diagram_id": self.diagram_id,
            "commutes": self.commutes,
            "residual_price_q": f"{self.residual_price_q.numerator}/{self.residual_price_q.denominator}",
            "metric_name": self.metric_name,
            "description": self.description,
        }


def audit_pipeline_run_determinism(
    config: Optional[PipelineConfig] = None,
) -> CommutationResidual:
    """Two runs of the same config produce the same terminal digest. Not a translation square."""
    from .pipeline import run_vertical_pipeline
    cfg = config or PipelineConfig(run_id="comp_comm_test", fuel_budget=10)
    res1 = run_vertical_pipeline(cfg, skip_composite_audit=True)
    res2 = run_vertical_pipeline(cfg, skip_composite_audit=True)
    same = (
        canonical_model_digest(res1.final_carrier) == canonical_model_digest(res2.final_carrier)
        and res1.is_success == res2.is_success
    )
    price = Fraction(0, 1) if same else Fraction(1, 1)
    return CommutationResidual(
        diagram_id="pipeline_run_determinism",
        commutes=same,
        residual_price_q=price,
        metric_name="terminal_carrier_digest_dist",
        description="Repeated pipeline runs under a fixed config yield the same terminal digest",
    )


def audit_commutation_residuals(
    p200_states: Optional[Sequence[P200CarrierState]] = None,
    substrate_states: Optional[Sequence[SubstrateState]] = None,
    relational_model: Optional[RelationalModel] = None,
    config: Optional[PipelineConfig] = None,
    skip_composite: bool = False,
) -> dict[str, CommutationResidual]:
    """Compute and emit exact rational priced residuals across vertical commutation squares."""
    r1_commutes = audit_readout_step_commutation(p200_states)
    r1 = CommutationResidual(
        diagram_id="readout_step_commutation",
        commutes=r1_commutes,
        residual_price_q=Fraction(0, 1) if r1_commutes else Fraction(1, 1),
        metric_name="readout_difference",
        description="Readout-to-step commutation on disjoint footprints (R o S = S o R)",
    )

    r2_commutes = audit_codec_roundtrip_commutation(substrate_states)
    r2 = CommutationResidual(
        diagram_id="codec_roundtrip_identity",
        commutes=r2_commutes,
        residual_price_q=Fraction(0, 1) if r2_commutes else Fraction(1, 1),
        metric_name="reconstruction_distance",
        description="Partial codec round-trip on graph/active/clock/fuel/nops; tape is declared metadata",
    )

    r3_commutes = audit_sheaf_descent_commutation(relational_model)
    r3 = CommutationResidual(
        diagram_id="sheaf_descent_commutation",
        commutes=r3_commutes,
        residual_price_q=Fraction(0, 1) if r3_commutes else Fraction(1, 1),
        metric_name="gluing_defect",
        description="Count-level descent for additions on the supplied carrier",
    )

    r4_commutes = audit_refusal_state_preservation(relational_model)
    r4 = CommutationResidual(
        diagram_id="refusal_state_preservation",
        commutes=r4_commutes,
        residual_price_q=Fraction(0, 1) if r4_commutes else Fraction(1, 1),
        metric_name="state_mutation_distance",
        description="Operational refusal state preservation (S_refusal(M) = M)",
    )

    out = {
        "readout_step_commutation": r1,
        "codec_roundtrip_identity": r2,
        "sheaf_descent_commutation": r3,
        "refusal_state_preservation": r4,
    }
    if not skip_composite:
        out["pipeline_run_determinism"] = audit_pipeline_run_determinism(config)
    return out


def run_commutation_audit(
    p200_states: Optional[Sequence[P200CarrierState]] = None,
    substrate_states: Optional[Sequence[SubstrateState]] = None,
    relational_model: Optional[RelationalModel] = None,
    config: Optional[PipelineConfig] = None,
    skip_composite: bool = False,
) -> dict[str, Any]:
    """Run programmatic audit across all 4 vertical commutation relations with priced residuals."""
    residuals = audit_commutation_residuals(
        p200_states=p200_states,
        substrate_states=substrate_states,
        relational_model=relational_model,
        config=config,
        skip_composite=skip_composite,
    )
    res: dict[str, Any] = {
        k: v.commutes for k, v in residuals.items()
    }
    res["residuals"] = {k: v.as_dict() for k, v in residuals.items()}
    return res
