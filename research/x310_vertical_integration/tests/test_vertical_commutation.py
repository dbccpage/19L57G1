"""Target X310: Programmatic verification of the four vertical commutation diagrams.

AuthorityEffect: None.
Epistemic Posture: Claim Hygiene Compliant (bounded, narrow, receipt-grounded).

Diagram 1: Readout-to-step commutation (R o S = S o R on non-disturbing sectors).
Diagram 2: Signature codec inversion and step transport (T^-1 o T = id).
Diagram 3: Multi-observer sheaf descent commutation (pi_i o U = u_i o pi_i).
Diagram 4: Refusal state preservation commutation (S_refusal(M) = M).
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
)
from research.p200_operational_protocols.protocol import (
    CarrierState as P200CarrierState,
    Locus,
    create_non_disturbing_readout,
)
from research.p200_operational_protocols.commutation import (
    check_commutation,
    step_l1,
    sweep_commutation,
)
import research.g014_observer_descent.observer_descent as g14
from research.x301_formal_semantics.semantics import (
    RelationalModel,
    atom,
    eq,
)
from research.x303_bounded_agency.agency import (
    AgentController,
    ViabilityEnvelope,
    add_instance_action,
    canonical_model_digest,
)

from research.x310_vertical_integration.pipeline import (
    CommutationResidual,
    audit_codec_roundtrip_commutation,
    audit_commutation_residuals,
    audit_pipeline_run_determinism,
    audit_readout_step_commutation,
    audit_refusal_state_preservation,
    audit_sheaf_descent_commutation,
    decode_relational_to_substrate,
    encode_substrate_to_relational,
    run_commutation_audit,
)
from research.x310_vertical_integration.commutation import build_sheaf_descent_square


def test_diagram_1_readout_step_commutation():
    """Verify Diagram 1: Readout R2 and step S1 commute on disjoint footprints."""
    # Positive control: non-disturbing readout at L2 and step at L1
    states = [
        P200CarrierState(l1=0, l2=0, m=0, r1=0, r2=0, dist=0),
        P200CarrierState(l1=1, l2=0, m=0, r1=0, r2=0, dist=0),
        P200CarrierState(l1=0, l2=1, m=0, r1=0, r2=0, dist=0),
        P200CarrierState(l1=1, l2=1, m=0, r1=0, r2=0, dist=0),
    ]
    assert audit_readout_step_commutation(states)

    # Negative control: disturbing step on the same locus as readout breaks commutation
    readout_inst = create_non_disturbing_readout(Locus.L2, Locus.R2)
    disturbing_step = lambda s: P200CarrierState(
        l1=s.l1, l2=1 - s.l2, m=s.m, r1=s.r1, r2=s.r2, dist=s.dist
    )
    res_disturbed = sweep_commutation(states, readout_inst.readout, disturbing_step)
    # When step mutates L2 before vs after readout, readouts differ
    assert not res_disturbed["all_commute"]


def test_diagram_2_codec_inversion_and_step_transport():
    """Verify Diagram 2: Signature codec roundtrip identity and operational transport."""
    # Build parameterized Controlled settings
    ctrl = frozenset({(0, 0), (1, 1), (2, 0)})
    ops = ((1, 2, 0), (0, 1, 2))
    c = Controlled(n=3, ops=ops, ctrl=ctrl)
    g = encode_c(c)

    # Test round-trip across states in a sequence
    s0 = SubstrateState(
        graph=g,
        nops=2,
        active=0,
        tape=(0,),
        clock=0,
        fuel=15,
        designated_pair=(0, 2),
    )

    encoded = encode_substrate_to_relational(s0)
    decoded = decode_relational_to_substrate(
        model=encoded,
        nops=s0.nops,
        clock=s0.clock,
        fuel=s0.fuel,
        tape=s0.tape,
        protection_obligations=s0.protection_obligations,
    )
    assert decoded == s0

    # Test step transport: firing op 0 in substrate maps to transition in relational model
    s1 = fire(s0, 0)
    assert not isinstance(s1, tuple)
    assert s1.active == 1
    assert s1.clock == 1
    assert s1.fuel == 14

    encoded_s1 = encode_substrate_to_relational(s1)
    decoded_s1 = decode_relational_to_substrate(
        model=encoded_s1,
        nops=s1.nops,
        clock=s1.clock,
        fuel=s1.fuel,
        tape=s1.tape,
        protection_obligations=s1.protection_obligations,
    )
    assert decoded_s1 == s1
    assert canonical_model_digest(encoded_s1) != canonical_model_digest(encoded)


def test_descent_preserves_empty_and_saturated_carriers():
    for carrier in (
        RelationalModel(data=(), forms=(), insts=frozenset(), reqs=frozenset()),
        RelationalModel(
            data=("a", "b"), forms=(1,),
            insts=frozenset({(0, (0,)), (0, (1,))}),
            reqs=frozenset({(0, 1)}),
        ),
    ):
        square = build_sheaf_descent_square(carrier)
        assert square.initial_counts == square.updated_counts
        assert dict(square.initial_counts)["data_count"] == len(carrier.data)
        assert square.commutes


def test_diagram_3_sheaf_descent_commutation():
    """Verify Diagram 3: Multi-observer sheaf descent commutes with concurrent step."""
    assert audit_sheaf_descent_commutation()

    supplied = RelationalModel(
        data=("a", "b", "c"), forms=(1,), insts=frozenset(), reqs=frozenset(),
    )
    square = build_sheaf_descent_square(supplied)
    assert dict(square.initial_counts) == {
        "data_count": 3, "form_count": 1, "inst_count": 0, "req_count": 0,
    }
    assert dict(square.updated_counts) == {
        "data_count": 3, "form_count": 1, "inst_count": 1, "req_count": 1,
    }
    assert square.commutes

    # Negative control: overlapping conflicting local updates cause gluing obstruction
    initial_mapping = {"l1": 1, "l2": 2, "overlap": 5}
    g_state = g14.CarrierState.from_mapping(initial_mapping)
    obs_a = g14.Observer(observer_id="OA", loci=("l1", "overlap"))
    obs_b = g14.Observer(observer_id="OB", loci=("l2", "overlap"))
    coverage = g14.DescentCoverage(observers=(obs_a, obs_b))

    # Observers record conflicting values on the shared overlap locus
    conflicting_records = {
        "OA": g14.CarrierState.from_mapping({"l1": 1, "overlap": 100}),
        "OB": g14.CarrierState.from_mapping({"l2": 2, "overlap": 200}),
    }
    glued_res = coverage.glue(conflicting_records)
    assert glued_res.is_err()
    obstruction = glued_res.unwrap_err()
    assert obstruction.overlap_locus == "overlap"


def test_diagram_4_refusal_state_preservation():
    """Verify Diagram 4: Operational refusal preserves carrier state strictly unmutated."""
    carrier = RelationalModel(
        data=(0, 1, 2),
        forms=(1, 2, 2),
        insts=frozenset({(0, (0,)), (1, (0, 1)), (2, (1, 2))}),
        reqs=frozenset({(0, 1)}),
    )
    # Audit verifies that refusal leaves carrier byte-identical and structurally identical
    assert audit_refusal_state_preservation(carrier)


def test_comprehensive_commutation_audit():
    """Verify run_commutation_audit returns True for all relations and records priced residuals."""
    audit = run_commutation_audit()
    assert audit["readout_step_commutation"]
    assert audit["codec_roundtrip_identity"]
    assert audit["sheaf_descent_commutation"]
    assert audit["refusal_state_preservation"]
    assert audit["pipeline_run_determinism"]
    assert "residuals" in audit
    for key, res_dict in audit["residuals"].items():
        assert res_dict["commutes"] is True
        assert res_dict["residual_price_q"] == "0/1"


def test_priced_commutation_residuals():
    """Verify that all commuting squares emit exact rational price 0/1,
    while disturbed/obstructed squares emit strictly positive disturbance prices > 0/1.
    """
    residuals = audit_commutation_residuals()
    for d_id, res in residuals.items():
        assert isinstance(res, CommutationResidual)
        assert res.commutes
        assert res.residual_price_q == Fraction(0, 1)

    # Disturbed square test: disturbing intervention on same locus
    states = [
        P200CarrierState(l1=0, l2=0, m=0, r1=0, r2=0, dist=0),
        P200CarrierState(l1=1, l2=0, m=0, r1=0, r2=0, dist=0),
    ]
    readout_inst = create_non_disturbing_readout(Locus.L2, Locus.R2)
    disturbing_step = lambda s: P200CarrierState(
        l1=s.l1, l2=1 - s.l2, m=s.m, r1=s.r1, r2=s.r2, dist=s.dist
    )
    dist_res = sweep_commutation(states, readout_inst.readout, disturbing_step)
    commutes = bool(dist_res["all_commute"])
    price = Fraction(0, 1) if commutes else Fraction(1, 1)
    disturbed_residual = CommutationResidual(
        diagram_id="disturbed_readout_intervention",
        commutes=commutes,
        residual_price_q=price,
        metric_name="readout_divergence",
        description="Disturbed noncommuting square with strictly positive disturbance price",
    )
    assert not disturbed_residual.commutes
    assert disturbed_residual.residual_price_q == Fraction(1, 1)
    assert disturbed_residual.residual_price_q > Fraction(0, 1)


def test_pipeline_run_determinism():
    """Two runs of the same config share a terminal digest."""
    comp_res = audit_pipeline_run_determinism()
    assert comp_res.commutes
    assert comp_res.residual_price_q == Fraction(0, 1)
    assert comp_res.diagram_id == "pipeline_run_determinism"
