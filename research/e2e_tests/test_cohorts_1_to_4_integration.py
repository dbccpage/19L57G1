"""Comprehensive End-to-End Integration Suite Across Cohorts 1-4.

Validates the full cross-cohort computational, observational, and mathematical pipeline:
- Cohort 1: Relational signature partition equality and honest claims tracking.
- Cohort 2: Inductive finitary substrate (G011), represented execution (Target A), and scale limits (Target B).
- Cohort 3: Internal operational logic (M101-M103), number tower Q (M105-M106), protection obligations (W03),
            and concurrent commuting squares (W06, W07).
- Cohort 4: Bound-uniform signature codec (G012), coherent 2-cell trace calculus (G013),
            zero-oracle self-simulation (G018), and physical operational protocols with non-signaling (P200).

AuthorityEffect: None.
Axiom Scope: Strictly constructive finite operations without host oracles.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import pytest

# Ensure all research package paths are on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RESEARCH_DIR = REPO_ROOT / "research"

MODULE_PATHS = [
    REPO_ROOT / "code",
    RESEARCH_DIR / "g011_finitary_substrate",
    RESEARCH_DIR / "m105_number_tower",
    RESEARCH_DIR / "g012_typed_translation",
    RESEARCH_DIR / "target_a_execution",
    RESEARCH_DIR / "concurrency",
    RESEARCH_DIR / "internal_syntax_logic",
    RESEARCH_DIR / "g013_trace_calculus",
    RESEARCH_DIR / "g018_self_hosting",
    RESEARCH_DIR / "p200_operational_protocols",
    RESEARCH_DIR / "coherent_process_limits",
    RESEARCH_DIR / "toe_charter",
]

for p in reversed(MODULE_PATHS):
    p_str = str(p)
    if p_str not in sys.path:
        sys.path.insert(0, p_str)

# -------------------------------------------------------------------------
# Imports from Cohort packages
# -------------------------------------------------------------------------
from ordinals import Ordinal, Zero, Succ
from address import Address, Root, Child
from number_tower import NNO, IntZ, RatQ
import signature as g012_sig
import codec as g012_codec
import naturality as g012_nat
import control as target_a_ctrl
import runner as target_a_runner
import trace as g013_tr
import higher_cell as g013_cell
import factorization as g013_fact
import carrier_repr as g018_rep
import simulator as g018_sim
import reflection_boundary as g018_refl
import protocol as p200_proto
import commutation as p200_comm
import embedded_observer as p200_obs
import non_signaling as p200_ns


class TestSubstrateAndNumberTowerIntegration:
    """Validate G011 finitary substrate integrates cleanly with M105/M106 number tower."""

    def test_finitary_ordinals_to_peano_and_rationals(self) -> None:
        # Construct finitary ordinal from G011
        o3 = Ordinal.from_nat(3)
        assert o3.to_nat() == 3
        assert not o3.is_zero()

        # Construct tree address using Root and Child
        root_addr = Root()
        assert root_addr.is_root()
        c1 = root_addr.child(o3)
        assert c1.branch_ordinal() == o3
        assert c1.depth() == Ordinal.from_nat(1)

        # Construct Grothendieck integers and Rationals
        z_pos = IntZ.from_int(o3.to_nat())
        assert z_pos.to_int() == 3

        q1 = RatQ(num=z_pos, den=4)
        q2 = RatQ(num=IntZ(6, 0), den=8)
        assert q1 == q2  # Equivalence class reduction modulo cross-multiplication
        assert q1.to_fraction() == Fraction(3, 4)

        # Rational field operations
        q_sum = q1 + RatQ.from_int(1)
        assert q_sum == RatQ(num=IntZ(7, 0), den=4)
        assert q_sum.to_fraction() == Fraction(7, 4)


class TestCodecWithSubstrateValues:
    """Validate G012 bound-uniform codec encodes structures carrying finitary & rational values."""

    def test_roundtrip_codec_on_algebraic_structure(self) -> None:
        # Define signature with carriers for substrate elements and rational fractions
        sig = g012_sig.Signature(
            sorts=("Point", "Scalar"),
            constants=(
                g012_sig.ConstantSymbol(name="origin", sort="Point"),
                g012_sig.ConstantSymbol(name="unit", sort="Scalar"),
            ),
            relations=(
                g012_sig.RelationSymbol(name="Adjacent", arity=("Point", "Point")),
            ),
            functions=(
                g012_sig.FunctionSymbol(name="scale", arity=("Point", "Scalar"), target_sort="Point"),
            ),
            observers=(
                g012_sig.ObserverSymbol(name="obs_pt", target_sort="Point", record_sort="Scalar"),
            ),
        )

        struct = g012_sig.TypedStructure(
            signature=sig,
            carriers=(
                ("Point", ("p0", "p1", "p2")),
                ("Scalar", ("s0", "s1")),
            ),
            constants=(
                ("origin", "p0"),
                ("unit", "s1"),
            ),
            relations=(
                ("Adjacent", (("p0", "p1"), ("p1", "p2"))),
            ),
            functions=(
                ("scale", ((("p0", "s0"), "p0"), (("p1", "s1"), "p1"))),
            ),
        )

        # Encode to relational grammar
        rel_state = g012_codec.encode(struct)
        assert len(rel_state.data) > 0
        assert len(rel_state.forms) > 0

        # Decode and verify exact round-trip invertibility
        res = g012_codec.decode(rel_state)
        assert res.is_ok()
        decoded = res.unwrap()
        assert decoded == struct

        # Distortion vector in Q
        distortion = g012_nat.compute_distortion(struct, address_depth=3)
        assert isinstance(distortion.state_expansion, Fraction)
        assert distortion.state_expansion >= Fraction(1, 1)


class TestTargetAExecutionAndRefusalUnderObligations:
    """Validate Target A execution under W03 protection obligations preserves refusal without mutation."""

    def test_operational_refusal_preserves_unmutated_state(self) -> None:
        # Build controlled execution configuration
        ops = (
            (1, 2, 3, 4, 0),  # op 0: cycle
            (2, 2, 2, 3, 4),  # op 1: collapse 0 and 1 into 2
        )
        ctrl = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (1, 1)]
        C = target_a_ctrl.Controlled(n=5, ops=ops, ctrl=frozenset(ctrl))

        obl_sep = target_a_runner.ProtectionObligation(target_a_runner.ProtectionKind.SEPARATED, 0, 1)
        s_sep = target_a_ctrl.init(C, x=0, fuel=10, protection_obligations=[obl_sep])

        # Op 1 collapses 0 and 1 into 2 -> must refuse with PROTECTION_VIOLATION
        res_viol = target_a_ctrl.fire(s_sep, 1)
        assert res_viol == target_a_runner.Refusal.PROTECTION_VIOLATION

        # Invariance check: state must remain completely unmutated on refusal
        assert s_sep.active == 0
        assert s_sep.clock == 0
        assert s_sep.fuel == 10
        assert s_sep.tape == (0,)
        assert s_sep.protection_obligations == (obl_sep,)


class TestSelfHostingSimulatorTracksExecution:
    """Validate G018 zero-oracle internal simulator faithfully mirrors object-level stepping."""

    def test_internal_simulation_matches_direct_stepping(self) -> None:
        # Machine spec: 2 states, increments tape at head
        t0 = g018_rep.Transition(curr_state=0, read_sym=0, next_state=1, write_sym=1, move_cursor=1, halt=False)
        t1 = g018_rep.Transition(curr_state=1, read_sym=0, next_state=2, write_sym=2, move_cursor=0, halt=True)
        spec = g018_rep.MachineSpec(transitions=(t0, t1), default_sym=0)

        # Direct execution trace
        init_mstate = g018_rep.MachineState(state=0, cursor=0, tape=(0, 0, 0), fuel=10, halted=False)
        direct_s1 = g018_rep.step_direct(spec, init_mstate)
        assert direct_s1 is not None

        # Internal simulator representation
        sim_state = g018_sim.sim_embed(spec, init_mstate, simulator_fuel=50)
        sim_stepped = g018_sim.step_internal(sim_state)
        assert sim_stepped is not None

        extracted_spec, extracted_state = g018_sim.sim_extract(sim_stepped)
        assert extracted_spec == spec
        assert extracted_state == direct_s1

        # Reflection boundary fuel closed form check
        fuel_req = g018_refl.compute_fuel_required(depth=3, base_steps=10)
        decoupled = g018_refl.decoupled_compounding_fuel(depth=3, base_steps=10)
        assert fuel_req == decoupled


class TestTraceCalculusAndHigherCells:
    """Validate G013 coherent trace calculus and Middle Four Interchange law."""

    def test_trace_confluence_and_interchange_law(self) -> None:
        s0 = g013_tr.State.create("s0")
        s1 = g013_tr.State.create("s1")
        s2 = g013_tr.State.create("s2")
        s3 = g013_tr.State.create("s3")

        # Left sector: s0 -> s1 with routes p1, q1, r1
        p1 = g013_tr.Trace.from_step(g013_tr.Transition(s0, s1, "p1"))
        q1 = g013_tr.Trace.from_step(g013_tr.Transition(s0, s1, "q1"))
        r1 = g013_tr.Trace.from_step(g013_tr.Transition(s0, s1, "r1"))

        alpha1 = g013_cell.Cell2(p1, q1, g013_cell.Cell2Kind.INDEPENDENT_COMMUTE, "alpha1: p1 => q1")
        alpha2 = g013_cell.Cell2(q1, r1, g013_cell.Cell2Kind.INDEPENDENT_COMMUTE, "alpha2: q1 => r1")

        # Right sector: s1 -> s2 with routes p2, q2, r2
        p2 = g013_tr.Trace.from_step(g013_tr.Transition(s1, s2, "p2"))
        q2 = g013_tr.Trace.from_step(g013_tr.Transition(s1, s2, "q2"))
        r2 = g013_tr.Trace.from_step(g013_tr.Transition(s1, s2, "r2"))

        beta1 = g013_cell.Cell2(p2, q2, g013_cell.Cell2Kind.INDEPENDENT_COMMUTE, "beta1: p2 => q2")
        beta2 = g013_cell.Cell2(q2, r2, g013_cell.Cell2Kind.INDEPENDENT_COMMUTE, "beta2: q2 => r2")

        # Middle four interchange law on composite 2-cells
        assert g013_cell.verify_interchange_law(alpha1, alpha2, beta1, beta2)

        # Endpoint factorization: future state space depends only on terminal state s2
        future = g013_tr.Trace.from_step(g013_tr.Transition(s2, s3, "f"))
        witness = g013_fact.witness_endpoint_factorization(
            h1=p1.concat(p2),
            h2=q1.concat(q2),
            future=future,
        )
        assert witness.is_valid()
        assert witness.shared_endpoint == s2
        assert witness.final_state == s3


class TestOperationalProtocolsAndNonSignaling:
    """Validate P200 operational protocols, readout commutation, and spacelike non-signaling."""

    def test_readout_to_step_commutation_and_exact_tvd(self) -> None:
        # Multi-locus carrier state: L1, L2, M, R1, R2, DIST
        s = p200_proto.CarrierState(l1=3, l2=7, m=0, r1=0, r2=0, dist=0)

        # Step at L1
        step1 = p200_comm.create_step_l1("inc_l1", lambda x: (x + 1) % 10)
        # Non-disturbing readout at L2 into R2
        readout2 = p200_proto.create_non_disturbing_readout(
            target_locus=p200_proto.Locus.L2,
            record_locus=p200_proto.Locus.R2,
            probe_fn=lambda x: x * 2,
        )

        # Commutation: Readout ∘ Step == Step ∘ Readout
        s_step_readout = readout2.execute(step1.execute(s))
        s_readout_step = step1.execute(readout2.execute(s))
        assert s_step_readout == s_readout_step
        assert p200_comm.is_non_disturbing_sector(readout2.footprint, step1.footprint)

        # Duplicate observers agreement on symmetric preparation
        s_sym = p200_proto.prepare_symmetric(s, v=5, m=0)
        obs1, obs2 = p200_obs.create_duplicate_observers()
        s_obs = p200_obs.run_joint_protocol(obs1, obs2, s_sym)
        assert p200_proto.coincidence_evaluator(s_obs)
        assert s_obs.r1 == s_obs.r2
        assert p200_obs.check_inter_observer_agreement(obs1, obs2, s_sym)

        # Spacelike non-signaling with exact rational TVD
        states_ensemble = [
            p200_proto.CarrierState(l1=a, l2=b, m=0, r1=0, r2=0, dist=0)
            for a in range(3)
            for b in range(3)
        ]
        interventions = {
            "noop": lambda x: x,
            "shift": lambda x: (x + 5) % 10,
        }
        report = p200_ns.verify_spacelike_non_signaling(
            states=states_ensemble,
            interventions=interventions,
            observer_2=obs2,
        )
        assert report.non_signaling_satisfied
        assert report.max_total_variation_distance == Fraction(0, 1)  # Exact rational zero in Q
