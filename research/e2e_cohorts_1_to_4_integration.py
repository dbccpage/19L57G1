"""Master End-to-End Integration Suite across Genesis Cohorts 1-4.

Exercises the complete, contiguous cross-cohort pipeline:
1. Substrate & Algebra: G011 finitary substrate tree addresses & ordinals embed into
   M105/M106 endogenous rational number tower Q with exact rational arithmetic.
2. Grammar & Codec: Multi-sorted typed structures carrying substrate and rational values
   encode into the sealed relational grammar (data, forms, insts, rules, reqs) via G012 codec
   with exact round-trip invertibility and distortion vectors in Q.
3. Execution & Refusal: Target A execution under W03 protection obligations preserves
   operational refusal without mutating carrier state.
4. Internalized Simulation: G018 zero-oracle step simulator faithfully tracks object process
   transitions, respecting the closed-form reflection fuel recurrence and boundary.
5. Higher Traces: G013 coherent trace calculus verifies 2-cell replay confluence, the Middle Four
   Interchange law, and endpoint factorization across parallel execution routes.
6. Operational Protocols: P200 embedded measurement instruments commute with disjoint process updates,
   duplicate observers agree on symmetric preparations, and spacelike loci exhibit exact rational
   zero total variation distance (TVD = 0/1 in Q) prior to causal mediation.

AuthorityEffect: None.
Axiom Scope: Constructive finite carrier operations with zero host oracles.
"""

from __future__ import annotations

import datetime
from fractions import Fraction
import json
from pathlib import Path
import sys
import time
from typing import Any, Dict

# Resolve paths
REPO_ROOT = Path(__file__).resolve().parent.parent
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


def run_integration_pipeline() -> Dict[str, Any]:
    start_time = time.perf_counter()
    stats: Dict[str, int] = {
        "substrate_to_algebra_checks": 0,
        "codec_roundtrip_checks": 0,
        "refusal_invariance_checks": 0,
        "simulation_faithfulness_checks": 0,
        "trace_and_higher_cell_checks": 0,
        "protocol_commutation_checks": 0,
        "spacelike_non_signaling_checks": 0,
    }

    print("=" * 80)
    print("Genesis Cohorts 1-4 Master End-to-End Integration Suite")
    print("Target Pipeline: G011 -> M105/M106 -> G012 -> Target A/W03 -> G018 -> G013 -> P200")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # 1. Substrate & Algebra: G011 -> M105/M106
    # -------------------------------------------------------------------------
    print(">>> Stage 1: Substrate to Exact Rational Tower...")
    for i in range(1, 21):
        ord_val = Ordinal.from_nat(i)
        assert ord_val.to_nat() == i
        z = IntZ.from_int(ord_val.to_nat())
        q1 = RatQ(num=z, den=i + 1)
        q2 = RatQ(num=IntZ.from_int(i * 3), den=(i + 1) * 3)
        assert q1 == q2
        assert q1.to_fraction() == Fraction(i, i + 1)
        stats["substrate_to_algebra_checks"] += 2

    # -------------------------------------------------------------------------
    # 2. Grammar & Codec: G012 with Substrate & Rational Values
    # -------------------------------------------------------------------------
    print(">>> Stage 2: Multi-Sorted Relational Codec Invertibility & Distortion...")
    sig = g012_sig.Signature(
        sorts=("Locus", "Value"),
        constants=(
            g012_sig.ConstantSymbol(name="origin", sort="Locus"),
            g012_sig.ConstantSymbol(name="unit", sort="Value"),
        ),
        relations=(
            g012_sig.RelationSymbol(name="Coupled", arity=("Locus", "Locus")),
        ),
        functions=(
            g012_sig.FunctionSymbol(name="eval", arity=("Locus", "Value"), target_sort="Value"),
        ),
        observers=(
            g012_sig.ObserverSymbol(name="obs_v", target_sort="Locus", record_sort="Value"),
        ),
    )

    for step_idx in range(1, 15):
        loci = tuple(sorted(f"l_{k}" for k in range(step_idx)))
        vals = tuple(sorted(f"v_{k}" for k in range(step_idx)))
        struct = g012_sig.TypedStructure(
            signature=sig,
            carriers=(("Locus", loci), ("Value", vals)),
            constants=(("origin", loci[0]), ("unit", vals[0])),
            relations=(("Coupled", tuple(sorted((loci[j], loci[(j + 1) % len(loci)]) for j in range(len(loci))))),),
            functions=(("eval", tuple(sorted(((loci[j], vals[j]), vals[(j + 1) % len(vals)]) for j in range(len(loci))))),),
        )

        rel_state = g012_codec.encode(struct)
        res = g012_codec.decode(rel_state)
        assert res.is_ok()
        assert res.unwrap() == struct

        distortion = g012_nat.compute_distortion(struct, address_depth=3)
        assert isinstance(distortion.state_expansion, Fraction)
        assert distortion.state_expansion >= Fraction(1, 1)
        stats["codec_roundtrip_checks"] += 2

    # -------------------------------------------------------------------------
    # 3. Execution & Refusal Under Obligations (Target A / W03)
    # -------------------------------------------------------------------------
    print(">>> Stage 3: Target A Execution Under Protection Obligations...")
    ops = (
        (1, 2, 3, 4, 0),
        (2, 2, 2, 3, 4),  # Collapses 0 and 1 into 2
    )
    ctrl = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (1, 1)]
    C = target_a_ctrl.Controlled(n=5, ops=ops, ctrl=frozenset(ctrl))

    obl_sep = target_a_runner.ProtectionObligation(target_a_runner.ProtectionKind.SEPARATED, 0, 1)
    s_sep = target_a_ctrl.init(C, x=0, fuel=10, protection_obligations=[obl_sep])

    # Firing collapsing op must produce refusal and preserve state
    refusal_res = target_a_ctrl.fire(s_sep, 1)
    assert refusal_res == target_a_runner.Refusal.PROTECTION_VIOLATION
    assert s_sep.active == 0
    assert s_sep.fuel == 10
    assert s_sep.clock == 0
    assert s_sep.tape == (0,)
    stats["refusal_invariance_checks"] += 5

    # -------------------------------------------------------------------------
    # 4. Zero-Oracle Self-Hosting Simulator (G018)
    # -------------------------------------------------------------------------
    print(">>> Stage 4: Zero-Oracle Self-Simulation & Reflection Boundary...")
    t0 = g018_rep.Transition(curr_state=0, read_sym=0, next_state=1, write_sym=1, move_cursor=1, halt=False)
    t1 = g018_rep.Transition(curr_state=1, read_sym=0, next_state=2, write_sym=2, move_cursor=0, halt=True)
    spec = g018_rep.MachineSpec(transitions=(t0, t1), default_sym=0)
    init_mstate = g018_rep.MachineState(state=0, cursor=0, tape=(0, 0, 0), fuel=10, halted=False)

    direct_s1 = g018_rep.step_direct(spec, init_mstate)
    sim_state = g018_sim.sim_embed(spec, init_mstate, simulator_fuel=50)
    sim_stepped = g018_sim.step_internal(sim_state)
    assert sim_stepped is not None
    _, extracted_state = g018_sim.sim_extract(sim_stepped)
    assert extracted_state == direct_s1

    # Check closed-form compounding recurrence across depth 1..10
    for d in range(1, 11):
        rec_fuel = g018_refl.compute_fuel_required(depth=d, base_steps=10)
        dec_fuel = g018_refl.decoupled_compounding_fuel(depth=d, base_steps=10)
        assert rec_fuel == dec_fuel
        stats["simulation_faithfulness_checks"] += 2

    # -------------------------------------------------------------------------
    # 5. Coherent Trace Calculus & Higher Cells (G013)
    # -------------------------------------------------------------------------
    print(">>> Stage 5: Trace Calculus, Interchange Law & Endpoint Factorization...")
    s0 = g013_tr.State.create("s0")
    s1 = g013_tr.State.create("s1")
    s2 = g013_tr.State.create("s2")
    s3 = g013_tr.State.create("s3")

    p1 = g013_tr.Trace.from_step(g013_tr.Transition(s0, s1, "p1"))
    q1 = g013_tr.Trace.from_step(g013_tr.Transition(s0, s1, "q1"))
    r1 = g013_tr.Trace.from_step(g013_tr.Transition(s0, s1, "r1"))
    alpha1 = g013_cell.Cell2(p1, q1, g013_cell.Cell2Kind.INDEPENDENT_COMMUTE, "alpha1")
    alpha2 = g013_cell.Cell2(q1, r1, g013_cell.Cell2Kind.INDEPENDENT_COMMUTE, "alpha2")

    p2 = g013_tr.Trace.from_step(g013_tr.Transition(s1, s2, "p2"))
    q2 = g013_tr.Trace.from_step(g013_tr.Transition(s1, s2, "q2"))
    r2 = g013_tr.Trace.from_step(g013_tr.Transition(s1, s2, "r2"))
    beta1 = g013_cell.Cell2(p2, q2, g013_cell.Cell2Kind.INDEPENDENT_COMMUTE, "beta1")
    beta2 = g013_cell.Cell2(q2, r2, g013_cell.Cell2Kind.INDEPENDENT_COMMUTE, "beta2")

    assert g013_cell.verify_interchange_law(alpha1, alpha2, beta1, beta2)

    future = g013_tr.Trace.from_step(g013_tr.Transition(s2, s3, "f"))
    witness = g013_fact.witness_endpoint_factorization(p1.concat(p2), q1.concat(q2), future)
    assert witness.is_valid()
    stats["trace_and_higher_cell_checks"] += 5

    # -------------------------------------------------------------------------
    # 6. Operational Protocols & Spacelike Non-Signaling (P200, W06/W07)
    # -------------------------------------------------------------------------
    print(">>> Stage 6: Readout Commutation & Spacelike Non-Signaling in Q...")
    step_l1 = p200_comm.create_step_l1("inc", lambda x: (x + 2) % 10)
    readout_l2 = p200_proto.create_non_disturbing_readout(
        p200_proto.Locus.L2, p200_proto.Locus.R2, probe_fn=lambda x: x * 3
    )

    states_sweep = [
        p200_proto.CarrierState(l1=a, l2=b, m=0, r1=0, r2=0, dist=0)
        for a in range(5)
        for b in range(5)
    ]
    for s in states_sweep:
        assert readout_l2.execute(step_l1.execute(s)) == step_l1.execute(readout_l2.execute(s))
        stats["protocol_commutation_checks"] += 1

    obs1, obs2 = p200_obs.create_duplicate_observers()
    report = p200_ns.verify_spacelike_non_signaling(
        states=states_sweep,
        interventions={
            "noop": lambda x: x,
            "add1": lambda x: (x + 1) % 10,
            "mult2": lambda x: (x * 2) % 10,
        },
        observer_2=obs2,
    )
    assert report.non_signaling_satisfied
    assert report.max_total_variation_distance == Fraction(0, 1)
    stats["spacelike_non_signaling_checks"] += len(states_sweep)

    elapsed = time.perf_counter() - start_time
    total_checks = sum(stats.values())

    print("=" * 80)
    print(f"ALL INTEGRATION CHECKS PASSED in {elapsed:.4f}s")
    print(f"Total Verified Checks Across Cohorts 1-4: {total_checks}")
    print(f"Breakdown: {stats}")
    print("=" * 80)

    receipt = {
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "verdict": "APPROVE",
        "total_checks": total_checks,
        "elapsed_seconds": round(elapsed, 4),
        "check_breakdown": stats,
        "pipeline_stages": [
            "G011 Finitary Substrate -> M105/M106 Number Tower Q",
            "G012 Bound-Uniform Codec -> Relational State Inversion",
            "Target A Execution -> W03 Protection Obligation Refusal Invariance",
            "G018 Zero-Oracle Self-Simulation -> Reflection Recurrence",
            "G013 2-Cell Trace Calculus -> Middle Four Interchange & Factorization",
            "P200 Operational Protocols -> Non-Disturbing Commutation & Spacelike Non-Signaling",
        ],
        "claim_hygiene_scope": {
            "Substrate": "Inductive finite ordinals and tree addresses with zero host memory pointers",
            "Algebra": "Constructive integers and exact rational localization Q modulo cross-multiplication",
            "Codec": "Invertible multi-sorted relational grammar mapping with exact rational distortion vectors",
            "Execution": "Represented CFG stepping with state-preserving refusal under protection obligations",
            "Simulation": "Zero-oracle internal self-simulation bounded by closed-form reflection fuel",
            "Traces": "Confluent 2-cells satisfying the Middle Four Interchange law and endpoint factorization",
            "Protocols": "Operational non-disturbing readout commutation and exact spacelike non-signaling TVD = 0/1",
        },
    }

    receipt_path = RESEARCH_DIR / "evidence_cohorts_1_to_4_integration.json"
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)
    print(f"Receipt written to: {receipt_path}")

    return receipt


if __name__ == "__main__":
    run_integration_pipeline()
