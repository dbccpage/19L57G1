"""Empirical Adversarial Stress Suite for Genesis Cohort 4.

Lead Architect & Adversarial Critic Review Gate.
Targets:
- G012: Bound-Uniform Typed Translation & General Signature Codec
- G013: Coherent Trace Calculus & Higher Cell Algebra
- G018: Self-Hosting, Internal Simulation & Reflection Boundary
- P200: Operational Protocols & Embedded Observers

Axiom Scope: Constructive finite carrier operations with zero host oracles.
Allowed Axioms: strictly within {'propext', 'Quot.sound'} (zero Classical.choice, zero mathlib).
AuthorityEffect: None.
Configuration status: DECLARED_HOST_CONFIG.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import time
from typing import Any, Callable, Dict, List, Sequence, Tuple

# Resolve repository root and prepend research directories to avoid shadowing
# (specifically ensuring research/g013_trace_calculus takes precedence over stdlib trace)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TARGET_DIRS = [
    REPO_ROOT / "code",
    REPO_ROOT / "research" / "g012_typed_translation",
    REPO_ROOT / "research" / "g013_trace_calculus",
    REPO_ROOT / "research" / "g018_self_hosting",
    REPO_ROOT / "research" / "p200_operational_protocols",
]
for p in reversed(TARGET_DIRS):
    p_str = str(p)
    if p_str in sys.path:
        sys.path.remove(p_str)
    sys.path.insert(0, p_str)

# Target G012 Imports
import codec as g012_codec
import signature as g012_sig
import naturality as g012_nat
import specialization as g012_spec

# Target G013 Imports
import trace as g013_tr
import higher_cell as g013_hc
import factorization as g013_fact
import congruence as g013_cong
import price as g013_price

# Target G018 Imports
import carrier_repr as g018_rep
import simulator as g018_sim
import reflection_boundary as g018_refl
import diagonal_obstruction as g018_diag

# Target P200 Imports
import protocol as p200_proto
import commutation as p200_comm
import embedded_observer as p200_obs
import non_signaling as p200_ns


# ==============================================================================
# 1. Target G012: Bound-Uniform Typed Translation Adversarial Tests
# ==============================================================================

def run_g012_adversarial_tests() -> dict[str, int]:
    """Adversarial stress tests for G012: Typed Translation & Signature Codec."""
    print("=== [1/5] G012 Typed Translation Adversarial Tests ===")
    stats = {
        "structured_refusal_corrupt_encodings": 0,
        "fuzz_roundtrip_invertibility": 0,
        "distortion_vector_exactness": 0,
        "renaming_naturality_commutation": 0,
        "specialization_1459_recovery": 0,
    }

    # --- Challenge 1.1: Malformed / Corrupt Encodings Return Structured Refusals ---
    # Case A: Unsorted or duplicate carrier tokens
    for field_name in ["data", "forms", "insts", "rules", "reqs"]:
        d_kwargs = {"data": (), "forms": (), "insts": (), "rules": (), "reqs": ()}
        # Inject unsorted duplicate tokens
        d_kwargs[field_name] = ("tok_b", "tok_a")
        bad_state = g012_codec.RelationalState(**d_kwargs)
        res = g012_codec.decode(bad_state)
        assert res.is_err(), f"Expected Err for unsorted field {field_name}"
        refusal = res.unwrap_err()
        assert refusal.code == g012_codec.RefusalCode.UNSORTED_OR_DUPLICATE
        stats["structured_refusal_corrupt_encodings"] += 1

    # Case B: Malformed syntax in declaration forms
    malformed_forms = [
        "sort:",                 # empty sort name
        "const:",                # empty const
        "const:c",               # missing sort
        "const::sort",           # empty name
        "const:c:",              # empty sort
        "rel:",                  # empty rel
        "rel:r",                 # missing arity
        "rel::arity",            # empty name
        "func:",                 # empty func
        "func:f",                # missing target
        "func:f:a",              # missing arrow
        "func:f:a->",            # empty target sort
    ]
    for bad_form in malformed_forms:
        state_bad_form = g012_codec.RelationalState(
            data=(),
            forms=(bad_form,),
            insts=(),
            rules=(),
            reqs=(),
        )
        res = g012_codec.decode(state_bad_form)
        assert res.is_err()
        assert res.unwrap_err().code == g012_codec.RefusalCode.MALFORMED_ENCODING
        stats["structured_refusal_corrupt_encodings"] += 1

    # Case C: Carrier mismatch (referencing undeclared sorts or elements)
    state_undeclared_sort_elem = g012_codec.RelationalState(
        data=("elem:ghost_sort:x",),
        forms=("sort:actual_sort",),
        insts=(),
        rules=(),
        reqs=("req:elem:ghost_sort:x",),
    )
    res_mismatch = g012_codec.decode(state_undeclared_sort_elem)
    assert res_mismatch.is_err()
    assert res_mismatch.unwrap_err().code in (
        g012_codec.RefusalCode.CARRIER_MISMATCH,
        g012_codec.RefusalCode.INVALID_SIGNATURE,
    )
    stats["structured_refusal_corrupt_encodings"] += 1

    # Case D: Non-functional multi-valued assignment
    state_multivalued_func = g012_codec.RelationalState(
        data=("elem:S:0", "elem:S:1", "elem:S:2"),
        forms=("func:f:S->S", "sort:S"),
        insts=(),
        rules=("rule:det:f", "rule:func:f:(0)->1", "rule:func:f:(0)->2"),
        reqs=(
            "req:elem:S:0", "req:elem:S:1", "req:elem:S:2",
            "req:func_in:f:S:0",
            "req:func_out:f:S:1", "req:func_out:f:S:2",
        ),
    )
    res_non_func = g012_codec.decode(state_multivalued_func)
    assert res_non_func.is_err()
    assert res_non_func.unwrap_err().code == g012_codec.RefusalCode.FUNCTION_NON_FUNCTIONAL
    stats["structured_refusal_corrupt_encodings"] += 1

    # Case E: Missing requirement tokens
    state_missing_req = g012_codec.RelationalState(
        data=("elem:S:0",),
        forms=("const:c:S", "sort:S"),
        insts=("bind:c:0",),
        rules=(),
        reqs=("req:elem:S:0",), # Missing req:const:c:S:0
    )
    res_miss_req = g012_codec.decode(state_missing_req)
    assert res_miss_req.is_err()
    assert res_miss_req.unwrap_err().code == g012_codec.RefusalCode.MISSING_REQUIREMENT
    stats["structured_refusal_corrupt_encodings"] += 1

    # Case F: Fuzzing 80 randomized corrupted/mutated states
    for i in range(80):
        garbage_token = f"corrupt_{random.randint(0, 99999)}:{random.choice(['@', '#', '$', 'bad', ':::'])}"
        category = random.choice(["data", "forms", "insts", "rules", "reqs"])
        if category in ("data", "forms", "insts", "rules"):
            kwargs = {"data": (), "forms": (), "insts": (), "rules": (), "reqs": ()}
            kwargs[category] = (garbage_token,)
        else:
            # For reqs, pair with an element so the corrupted requirement fails to validate
            kwargs = {
                "data": ("elem:sort_a:e0",),
                "forms": ("sort:sort_a",),
                "insts": (),
                "rules": (),
                "reqs": (garbage_token,),
            }
        fuzz_state = g012_codec.RelationalState(**kwargs)
        res_fuzz = g012_codec.decode(fuzz_state)
        assert res_fuzz.is_err(), f"Fuzz state should be rejected: {kwargs}"
        assert isinstance(res_fuzz.unwrap_err(), g012_codec.Refusal)
        stats["structured_refusal_corrupt_encodings"] += 1

    # --- Challenge 1.2: Fuzz Round-Trip Invertibility across Varied Multi-Sorted Signatures ---
    rng = random.Random(42)
    sort_pool = ["atom", "node", "packet", "agent", "color"]
    for fuzz_idx in range(60):
        # Choose 1 to 4 sorts
        n_sorts = rng.randint(1, 4)
        chosen_sorts = tuple(sorted(rng.sample(sort_pool, n_sorts)))

        # Constants
        consts = []
        for c_i in range(rng.randint(0, 3)):
            s = rng.choice(chosen_sorts)
            consts.append(g012_sig.ConstantSymbol(name=f"c_{c_i}", sort=s))

        # Relations
        rels = []
        for r_i in range(rng.randint(0, 3)):
            ar_len = rng.randint(0, 3)
            ar = tuple(rng.choice(chosen_sorts) for _ in range(ar_len))
            rels.append(g012_sig.RelationSymbol(name=f"R_{r_i}", arity=ar))

        # Functions
        funcs = []
        for f_i in range(rng.randint(0, 2)):
            ar_len = rng.randint(0, 2)
            ar = tuple(rng.choice(chosen_sorts) for _ in range(ar_len))
            tgt = rng.choice(chosen_sorts)
            funcs.append(g012_sig.FunctionSymbol(name=f"f_{f_i}", arity=ar, target_sort=tgt))

        sig = g012_sig.Signature(
            sorts=chosen_sorts,
            constants=tuple(consts),
            relations=tuple(rels),
            functions=tuple(funcs),
        )

        # Populate carriers
        carriers = {}
        for s in chosen_sorts:
            elems = [f"{s}_{e_idx}" for e_idx in range(rng.randint(1, 4))]
            carriers[s] = tuple(sorted(elems))

        # Populate constants
        constants_map = {}
        for c in consts:
            constants_map[c.name] = rng.choice(carriers[c.sort])

        # Populate relations
        relations_map = {}
        for r in rels:
            tups = set()
            for _ in range(rng.randint(0, 4)):
                t = tuple(rng.choice(carriers[s]) for s in r.arity)
                tups.add(t)
            relations_map[r.name] = tups

        # Populate functions (well-defined total or partial functions)
        functions_map = {}
        for f in funcs:
            table = {}
            for _ in range(rng.randint(0, 4)):
                args = tuple(rng.choice(carriers[s]) for s in f.arity)
                val = rng.choice(carriers[f.target_sort])
                table[args] = val
            functions_map[f.name] = table

        struct = g012_sig.TypedStructure.create(
            signature=sig,
            carriers=carriers,
            constants=constants_map,
            relations=relations_map,
            functions=functions_map,
        )

        # Encode and decode round-trip
        enc = g012_codec.encode(struct)
        dec_res = g012_codec.decode(enc)
        assert dec_res.is_ok(), f"Round-trip failed on fuzz {fuzz_idx}: {dec_res.unwrap_err()}"
        dec_struct = dec_res.unwrap()
        assert dec_struct == struct, f"Decoded structure does not match original on fuzz {fuzz_idx}"
        stats["fuzz_roundtrip_invertibility"] += 1

    # --- Challenge 1.3: Rational Distortion Vector Exactness and Renaming Invariance ---
    # Exact rational distortion vector test on 30 structures
    for dist_idx in range(30):
        sig = g012_sig.Signature(
            sorts=("node", "label"),
            constants=(g012_sig.ConstantSymbol("root", "node"),),
            relations=(g012_sig.RelationSymbol("Edge", ("node", "node")),),
            functions=(g012_sig.FunctionSymbol("tag", ("node",), "label"),),
        )
        struct = g012_sig.TypedStructure.create(
            signature=sig,
            carriers={"node": [f"n{i}" for i in range(dist_idx + 1)], "label": ["L0", "L1"]},
            constants={"root": "n0"},
            relations={"Edge": [("n0", f"n{min(1, dist_idx)}")]},
            functions={"tag": [(("n0",), "L0")]},
        )
        dist_vec = g012_nat.compute_distortion(struct)
        # All three components must be exact fractions.Fraction
        assert isinstance(dist_vec.state_expansion, Fraction)
        assert isinstance(dist_vec.mark_count_ratio, Fraction)
        assert isinstance(dist_vec.address_depth_ratio, Fraction)
        assert dist_vec.state_expansion >= 1
        assert dist_vec.address_depth_ratio == Fraction(3, 3) # max_arity=2, struct_depth=3, rel_depth=3
        stats["distortion_vector_exactness"] += 1

    # Renaming naturality commutation test
    sig_orig = g012_sig.Signature(
        sorts=("source_s", "source_t"),
        constants=(g012_sig.ConstantSymbol("c_orig", "source_s"),),
        relations=(g012_sig.RelationSymbol("R_orig", ("source_s", "source_t")),),
        functions=(g012_sig.FunctionSymbol("F_orig", ("source_s",), "source_t"),),
    )
    struct_orig = g012_sig.TypedStructure.create(
        signature=sig_orig,
        carriers={"source_s": ["s0", "s1"], "source_t": ["t0"]},
        constants={"c_orig": "s0"},
        relations={"R_orig": [("s0", "t0")]},
        functions={"F_orig": [(("s0",), "t0")]},
    )

    for ren_idx in range(30):
        renaming = g012_nat.Renaming.create(
            sort_map={"source_s": f"ren_s_{ren_idx}", "source_t": f"ren_t_{ren_idx}"},
            const_map={"c_orig": f"c_ren_{ren_idx}"},
            rel_map={"R_orig": f"R_ren_{ren_idx}"},
            func_map={"F_orig": f"F_ren_{ren_idx}"},
        )
        # Naturality commutation: encode(sigma_*(S)) == sigma_rel(encode(S))
        commutes = g012_nat.renaming_naturality_commutes(renaming, struct_orig)
        assert commutes, f"Renaming naturality commutation failed at index {ren_idx}"
        stats["renaming_naturality_commutation"] += 1

    # --- Challenge 1.4: Recovery of 1,459 Valid History Prefixes ---
    spec_result = g012_spec.verify_specialization_recovery()
    assert spec_result["histories_count"] == 1459, f"Expected 1459 histories, got {spec_result['histories_count']}"
    assert spec_result["unique_structures_count"] == 22, f"Expected 22 structures, got {spec_result['unique_structures_count']}"
    assert spec_result["step_commutations_tested"] == 1396, f"Expected 1396 commutations, got {spec_result['step_commutations_tested']}"
    assert spec_result["roundtrip_all_passed"] is True
    stats["specialization_1459_recovery"] += 1459

    print(f"G012 checks passed: {stats}")
    return stats


# ==============================================================================
# 2. Target G013: Coherent Trace Calculus Adversarial Tests
# ==============================================================================

def run_g013_adversarial_tests() -> dict[str, int]:
    """Adversarial stress tests for G013: Coherent Trace Calculus & Higher Cells."""
    print("=== [2/5] G013 Trace Calculus Adversarial Tests ===")
    stats = {
        "interchange_law_commuting_squares": 0,
        "endpoint_factorization_topologies": 0,
        "observer_congruence_residuals": 0,
        "price_cocycle_additivity_and_homotopy": 0,
    }

    # --- Challenge 2.1: Higher 2-cell Interchange Law on Random Commuting Squares ---
    rng = random.Random(13)
    for sq_idx in range(50):
        # Build 3 consecutive 0-cells s0, s1, s2
        s0 = g013_tr.State.create(f"sq_{sq_idx}_s0", {"idx": 0})
        s1 = g013_tr.State.create(f"sq_{sq_idx}_s1", {"idx": 1})
        s2 = g013_tr.State.create(f"sq_{sq_idx}_s2", {"idx": 2})

        # Left 1-cells s0 -> s1: p1, q1, r1
        p1 = g013_tr.Trace.from_step(g013_tr.Transition(s0, s1, f"p1_{sq_idx}", cost=1.0))
        q1 = g013_tr.Trace.from_step(g013_tr.Transition(s0, s1, f"q1_{sq_idx}", cost=1.0))
        r1 = g013_tr.Trace.from_step(g013_tr.Transition(s0, s1, f"r1_{sq_idx}", cost=1.0))

        alpha1 = g013_hc.Cell2(p1, q1, g013_hc.Cell2Kind.INDEPENDENT_COMMUTE, "alpha1")
        alpha2 = g013_hc.Cell2(q1, r1, g013_hc.Cell2Kind.INDEPENDENT_COMMUTE, "alpha2")

        # Right 1-cells s1 -> s2: p2, q2, r2
        p2 = g013_tr.Trace.from_step(g013_tr.Transition(s1, s2, f"p2_{sq_idx}", cost=2.0))
        q2 = g013_tr.Trace.from_step(g013_tr.Transition(s1, s2, f"q2_{sq_idx}", cost=2.0))
        r2 = g013_tr.Trace.from_step(g013_tr.Transition(s1, s2, f"r2_{sq_idx}", cost=2.0))

        beta1 = g013_hc.Cell2(p2, q2, g013_hc.Cell2Kind.INDEPENDENT_COMMUTE, "beta1")
        beta2 = g013_hc.Cell2(q2, r2, g013_hc.Cell2Kind.INDEPENDENT_COMMUTE, "beta2")

        coherent, left_comp, right_comp = g013_hc.verify_interchange_law(alpha1, alpha2, beta1, beta2)
        assert coherent, f"Interchange law coherence failed for square {sq_idx}"
        assert left_comp.source_trace == p1.concat(p2)
        assert left_comp.target_trace == r1.concat(r2)
        assert right_comp.source_trace == p1.concat(p2)
        assert right_comp.target_trace == r1.concat(r2)
        assert left_comp.source_trace == right_comp.source_trace
        assert left_comp.target_trace == right_comp.target_trace
        stats["interchange_law_commuting_squares"] += 1

    # --- Challenge 2.2: Endpoint Factorization across Diverse Topologies ---
    # Topology 1: Linear Pipelines
    for depth in [3, 5, 8, 12, 16]:
        states, trans = g013_fact.GraphRegimeGenerator.linear_pipeline(depth)
        # Construct two identical prefix histories to s_mid, plus future
        mid_idx = depth // 2
        h1 = g013_tr.Trace.from_steps(trans[:mid_idx])
        h2 = g013_tr.Trace.from_steps(trans[:mid_idx])
        fut = g013_tr.Trace.from_steps(trans[mid_idx:])
        w = g013_fact.witness_endpoint_factorization(h1, h2, fut)
        assert w.is_valid(), f"Linear pipeline factorization failed at depth {depth}"
        stats["endpoint_factorization_topologies"] += 1

    # Topology 2: Diamond DAG
    for branches in [2, 3, 4, 5]:
        states, trans = g013_fact.GraphRegimeGenerator.diamond_dag(branches=branches, depth=2)
        start = [s for s in states if s.state_id == "diamond_start"][0]
        hub = [s for s in states if s.state_id == "diamond_hub"][0]
        end = [s for s in states if s.state_id == "diamond_end"][0]

        # Pick two distinct branches A_i and A_j
        for b_i in range(branches - 1):
            t_split_i = [t for t in trans if t.label == f"split_A{b_i}"][0]
            t_join_i = [t for t in trans if t.label == f"join_A{b_i}"][0]
            h1 = g013_tr.Trace.from_steps([t_split_i, t_join_i])

            t_split_j = [t for t in trans if t.label == f"split_A{b_i + 1}"][0]
            t_join_j = [t for t in trans if t.label == f"join_A{b_i + 1}"][0]
            h2 = g013_tr.Trace.from_steps([t_split_j, t_join_j])

            # Pick continuation branch B_k
            t_split_b = [t for t in trans if t.label == "split_B0"][0]
            t_join_b = [t for t in trans if t.label == "join_B0"][0]
            fut = g013_tr.Trace.from_steps([t_split_b, t_join_b])

            w = g013_fact.witness_endpoint_factorization(h1, h2, fut)
            assert w.is_valid(), f"Diamond DAG factorization failed on branch pair ({b_i}, {b_i+1})"
            stats["endpoint_factorization_topologies"] += 1

    # Topology 3: Grid Graph Sweep
    grid_witnesses = g013_fact.sweep_factorization_grid(width=3, height=3)
    assert len(grid_witnesses) > 0, "Grid factorization sweep produced zero witnesses"
    for gw in grid_witnesses:
        assert gw.is_valid()
        stats["endpoint_factorization_topologies"] += 1

    # Topology 4: Cyclic State Machine
    states, trans = g013_fact.GraphRegimeGenerator.cyclic_state_machine(num_cycles=3, cycle_len=3)
    nexus = [s for s in states if s.state_id == "nexus"][0]
    # Path 1: 0 loops (identity at nexus)
    h_empty = g013_tr.Trace.id_trace(nexus)
    # Path 2: 1 loop through cycle 0
    t_enter0 = [t for t in trans if t.label == "enter_c0"][0]
    t_step0 = [t for t in trans if t.label == "step_c0_0"][0]
    t_ret0 = [t for t in trans if t.label == "return_c0"][0]
    h_loop0 = g013_tr.Trace.from_steps([t_enter0, t_step0, t_ret0])
    # Future: 1 loop through cycle 1
    t_enter1 = [t for t in trans if t.label == "enter_c1"][0]
    t_step1 = [t for t in trans if t.label == "step_c1_0"][0]
    t_ret1 = [t for t in trans if t.label == "return_c1"][0]
    fut_loop1 = g013_tr.Trace.from_steps([t_enter1, t_step1, t_ret1])

    w_cyclic = g013_fact.witness_endpoint_factorization(h_empty, h_loop0, fut_loop1)
    assert w_cyclic.is_valid()
    stats["endpoint_factorization_topologies"] += 1

    # --- Challenge 2.3: Observer Trace Congruence and Residual Detection ---
    # System with congruent states yielding zero residuals
    sA = g013_tr.State.create("sA", {"visible": 42, "secret": 1})
    sB = g013_tr.State.create("sB", {"visible": 42, "secret": 2})
    s_end = g013_tr.State.create("s_end", {"visible": 99, "secret": 0})
    tA = g013_tr.Transition(sA, s_end, "ping", cost=1.0)
    tB = g013_tr.Transition(sB, s_end, "ping", cost=1.0)
    tsys_good = g013_cong.TransitionSystem(
        states={"sA": sA, "sB": sB, "s_end": s_end},
        transitions=[tA, tB],
    )
    proj = g013_cong.ObservationProjection(
        name="visible_channel",
        project_state=lambda s: s.get("visible"),
    )
    audit_clean = g013_cong.audit_observer_residuals(tsys_good, proj, max_depth=3)
    assert audit_clean.is_congruent, "Expected clean audit to be congruent"
    assert not audit_clean.unrecorded_residuals_detected, "Clean system must have zero unrecorded residuals"
    stats["observer_congruence_residuals"] += 1

    # Negative control: Divergent unrecorded residual
    sA_bad = g013_tr.State.create("sA_bad", {"visible": 10, "secret": 1})
    sB_bad = g013_tr.State.create("sB_bad", {"visible": 10, "secret": 2})
    s_end_1 = g013_tr.State.create("s_end_1", {"visible": 20})
    s_end_2 = g013_tr.State.create("s_end_2", {"visible": 30}) # Divergence!
    tA_bad = g013_tr.Transition(sA_bad, s_end_1, "step", cost=1.0)
    tB_bad = g013_tr.Transition(sB_bad, s_end_2, "step", cost=1.0)
    tsys_bad = g013_cong.TransitionSystem(
        states={"sA_bad": sA_bad, "sB_bad": sB_bad, "s_end_1": s_end_1, "s_end_2": s_end_2},
        transitions=[tA_bad, tB_bad],
    )
    is_cong, err = g013_cong.check_observer_trace_congruence(sA_bad, sB_bad, tsys_bad, proj, max_depth=2)
    assert not is_cong, "Negative control must detect observation divergence"
    assert err is not None
    stats["observer_congruence_residuals"] += 1

    # --- Challenge 2.4: Price Cocycle Additivity & Homotopy Invariance ---
    cocycle = g013_price.PriceCocycle(
        cost_map={"step_a": 1.5, "step_b": 2.5, "step_c": 3.0, "step_d": 4.0},
        default_cost=1.0,
    )
    # Additivity: C(p * q) == C(p) + C(q)
    s_p0 = g013_tr.State.create("p0")
    s_p1 = g013_tr.State.create("p1")
    s_p2 = g013_tr.State.create("p2")
    tr_p = g013_tr.Trace.from_step(g013_tr.Transition(s_p0, s_p1, "step_a"))
    tr_q = g013_tr.Trace.from_step(g013_tr.Transition(s_p1, s_p2, "step_b"))
    is_add, c_comp, c_sum, diff = cocycle.verify_additivity(tr_p, tr_q)
    assert is_add, f"Cocycle additivity violated: comp={c_comp}, sum={c_sum}"
    assert abs(c_comp - 4.0) < 1e-9
    stats["price_cocycle_additivity_and_homotopy"] += 1

    # Homotopy price invariance on 2-cells
    cell_commute = g013_hc.Cell2.commute(
        g013_tr.Transition(s0, s1, "step_a", cost=1.5),
        g013_tr.Transition(s1, s2, "step_b", cost=2.5),
        g013_tr.Transition(s0, s1, "step_b", cost=2.5),
        g013_tr.Transition(s1, s2, "step_a", cost=1.5),
    )
    inv, c_src, c_tgt = cocycle.verify_homotopy_invariance(cell_commute)
    assert inv, f"Homotopy price invariance violated: {c_src} != {c_tgt}"
    audit_cells = g013_price.audit_2cell_homotopy_invariance(cocycle, [cell_commute])
    assert audit_cells.all_invariant
    assert audit_cells.max_divergence < 1e-9
    stats["price_cocycle_additivity_and_homotopy"] += 1

    print(f"G013 checks passed: {stats}")
    return stats


# ==============================================================================
# 3. Target G018: Self-Hosting, Internal Simulation & Reflection Boundary
# ==============================================================================

def run_g018_adversarial_tests() -> dict[str, int]:
    """Adversarial stress tests for G018: Internalized Self-Hosting & Reflection."""
    print("=== [3/5] G018 Self-Hosting Adversarial Tests ===")
    stats = {
        "simulation_faithfulness_macro": 0,
        "simulation_faithfulness_micro": 0,
        "reflection_compounding_equations": 0,
        "reflection_exhaustion_thresholds": 0,
        "diagonal_obstruction_refutations": 0,
    }

    # --- Challenge 3.1: Step-Simulation Faithfulness (Macro and Micro) ---
    # Guest Machine 1: Parity Inverter Machine
    # State 0: read 0 -> write 1, move R, goto 1
    # State 1: read 1 -> write 0, move R, goto 2 (halt)
    spec_invert = g018_rep.MachineSpec(
        transitions=(
            g018_rep.Transition(0, 0, 1, 1, 1, False),
            g018_rep.Transition(1, 1, 2, 0, 1, True),
        ),
        default_sym=0,
    )
    init_state = g018_rep.MachineState(state=0, cursor=0, tape=(0, 1), fuel=10, halted=False)

    # Macro-stepping test: verify internal simulator tracks direct stepping step-for-step
    sim_macro = g018_sim.sim_embed(spec_invert, init_state, simulator_fuel=20)
    direct_curr = init_state
    for step_num in range(2):
        direct_curr = g018_rep.step_direct(spec_invert, direct_curr)
        sim_macro = g018_sim.step_internal(sim_macro)
        _, extracted_guest = g018_sim.sim_extract(sim_macro)
        assert extracted_guest == direct_curr, f"Macro step mismatch at step {step_num}"
        stats["simulation_faithfulness_macro"] += 1

    # Micro-stepping test: 4 micro-cycles per macro-step
    sim_micro = g018_sim.micro_sim_embed(spec_invert, init_state, simulator_fuel=50)
    direct_curr = init_state
    for step_num in range(2):
        direct_curr = g018_rep.step_direct(spec_invert, direct_curr)
        sim_micro = g018_sim.micro_step_k(sim_micro, 4)
        assert sim_micro.macro_steps_completed == step_num + 1
        assert sim_micro.stage == g018_sim.STAGE_FETCH
        assert sim_micro.guest_state == direct_curr, f"Micro step mismatch at step {step_num}"
        stats["simulation_faithfulness_micro"] += 1

    # Stress test on a 3-state walk machine for 30 consecutive steps
    walk_spec = g018_rep.MachineSpec(
        transitions=(
            g018_rep.Transition(0, 0, 1, 1, 1, False),
            g018_rep.Transition(1, 0, 2, 2, 1, False),
            g018_rep.Transition(2, 0, 0, 0, 1, False),
            g018_rep.Transition(0, 1, 1, 1, 1, False),
            g018_rep.Transition(1, 1, 2, 2, 1, False),
            g018_rep.Transition(2, 1, 0, 0, 1, False),
            g018_rep.Transition(0, 2, 1, 1, 1, False),
            g018_rep.Transition(1, 2, 2, 2, 1, False),
            g018_rep.Transition(2, 2, 0, 0, 1, False),
        ),
        default_sym=0,
    )
    walk_state = g018_rep.MachineState(state=0, cursor=0, tape=(0,) * 50, fuel=50, halted=False)
    walk_sim = g018_sim.sim_embed(walk_spec, walk_state, simulator_fuel=100)
    curr_walk = walk_state
    for i in range(30):
        curr_walk = g018_rep.step_direct(walk_spec, curr_walk)
        walk_sim = g018_sim.step_internal(walk_sim)
        _, ext = g018_sim.sim_extract(walk_sim)
        assert ext == curr_walk, f"Walk machine diverged at step {i}"
        stats["simulation_faithfulness_macro"] += 1

    # --- Challenge 3.2: Reflection Boundary & Fuel Compounding ---
    # Mathematical closed-form test of compounding fuel equations
    for depth in range(6):
        for base in [1, 5, 10, 20]:
            overhead = 2
            layer = 1
            f_calc = g018_refl.compute_fuel_required(depth, base, overhead, layer)
            # Reconstruct manual recurrence
            f_manual = base
            for _ in range(depth):
                f_manual = f_manual * overhead + layer
            assert f_calc == f_manual, f"Fuel formula mismatch at depth={depth}, base={base}"
            stats["reflection_compounding_equations"] += 1

    # Max reflection depth tests
    assert g018_refl.max_reflection_depth(available_fuel=100, base_steps=5, overhead_per_step=2, layer_overhead=1) >= 4
    assert g018_refl.max_reflection_depth(available_fuel=2, base_steps=5) == 0
    stats["reflection_compounding_equations"] += 2

    # Reflection tower execution and exhaustion threshold testing
    simple_spec = g018_rep.MachineSpec(
        transitions=(g018_rep.Transition(0, 0, 0, 0, 1, False),),
        default_sym=0,
    )
    simple_state = g018_rep.MachineState(state=0, cursor=0, tape=(0,) * 20, fuel=10, halted=False)

    # Adequate budget -> completes without exhaustion
    res_ok = g018_refl.run_reflection_tower(depth=1, spec=simple_spec, state=simple_state, host_fuel=15)
    assert not res_ok.fuel_exhausted
    assert res_ok.completed_base_steps == 10
    stats["reflection_exhaustion_thresholds"] += 1

    # Deficient budget -> exhausts fuel prematurely
    res_exhaust = g018_refl.run_reflection_tower(depth=1, spec=simple_spec, state=simple_state, host_fuel=5)
    assert res_exhaust.fuel_exhausted
    assert res_exhaust.completed_base_steps < 10
    stats["reflection_exhaustion_thresholds"] += 1

    # Multi-level tower exhaustion (depth 2) with host_fuel strictly less than guest fuel
    state_long = g018_rep.MachineState(state=0, cursor=0, tape=(0,) * 20, fuel=20, halted=False)
    res_d2_starved = g018_refl.run_reflection_tower(depth=2, spec=simple_spec, state=state_long, host_fuel=5)
    assert res_d2_starved.fuel_exhausted
    assert res_d2_starved.completed_base_steps == 5
    stats["reflection_exhaustion_thresholds"] += 1

    # --- Challenge 3.3: Diagonal Obstruction Refuting 7 Predictor Self-Oracles ---
    refutations = g018_diag.sweep_candidate_predictors(fuel_budget=50)
    assert len(refutations) == 7, f"Expected exactly 7 refutations, got {len(refutations)}"
    expected_predictors = {
        "AlwaysHaltOracle",
        "NeverHaltOracle",
        "SyntacticHaltEdgeOracle",
        "BoundedStepOracle_k1",
        "BoundedStepOracle_k5",
        "BoundedStepOracle_k10",
        "BoundedStepOracle_k25",
    }
    actual_predictors = {r.predictor_name for r in refutations}
    assert actual_predictors == expected_predictors, f"Predictor names mismatch: {actual_predictors}"

    for r in refutations:
        assert r.refutation_success, f"Diagonal refutation failed for {r.predictor_name}"
        assert r.predicted_halt != r.actual_halt, (
            f"Obstruction violated for {r.predictor_name}: predicted={r.predicted_halt}, actual={r.actual_halt}"
        )
        stats["diagonal_obstruction_refutations"] += 1

    print(f"G018 checks passed: {stats}")
    return stats


# ==============================================================================
# 4. Target P200: Operational Protocols Adversarial Tests
# ==============================================================================

def run_p200_adversarial_tests() -> dict[str, int]:
    """Adversarial stress tests for P200: Operational Protocols & Embedded Observers."""
    print("=== [4/5] P200 Operational Protocols Adversarial Tests ===")
    stats = {
        "non_disturbing_readout_commutation": 0,
        "disturbance_detection_and_pricing": 0,
        "duplicate_observer_agreement_and_symmetries": 0,
        "spacelike_non_signaling_invariance": 0,
    }

    # --- Challenge 4.1: Non-Disturbing Readout Commutation (Readout o Step = Step o Readout) ---
    # Create an ensemble of 50 varied carrier states
    carrier_ensemble = [
        p200_proto.CarrierState(l1=i % 10, l2=(i * 3) % 10, m=(i * 7) % 5, r1=0, r2=0, dist=0)
        for i in range(50)
    ]

    # Sector A: Readout at L1 (updates R1) vs Step at L2 (modifies L2) -> Disjoint
    step_l2 = p200_comm.ProcessStep(
        name="inc_l2",
        target_locus=p200_proto.Locus.L2,
        transition_fn=lambda x: (x + 1) % 10,
        reads=frozenset({p200_proto.Locus.L2}),
        writes=frozenset({p200_proto.Locus.L2}),
    )
    sweep_a = p200_comm.sweep_commutation(
        carrier_ensemble,
        p200_proto.non_disturbing_readout_1,
        step_l2.execute,
    )
    assert sweep_a["all_commute"], "Readout_1 must commute with Step_L2"
    stats["non_disturbing_readout_commutation"] += sweep_a["commuting_count"]

    # Sector B: Readout at L2 (updates R2) vs Step at L1 (modifies L1) -> Disjoint
    step_l1 = p200_comm.ProcessStep(
        name="inc_l1",
        target_locus=p200_proto.Locus.L1,
        transition_fn=lambda x: (x + 2) % 10,
        reads=frozenset({p200_proto.Locus.L1}),
        writes=frozenset({p200_proto.Locus.L1}),
    )
    sweep_b = p200_comm.sweep_commutation(
        carrier_ensemble,
        p200_proto.non_disturbing_readout_2,
        step_l1.execute,
    )
    assert sweep_b["all_commute"], "Readout_2 must commute with Step_L1"
    stats["non_disturbing_readout_commutation"] += sweep_b["commuting_count"]

    # Sector C: Readout at L1 vs Step at M -> Disjoint
    step_m = p200_comm.ProcessStep(
        name="flip_m",
        target_locus=p200_proto.Locus.M,
        transition_fn=lambda m: (m + 1) % 5,
        reads=frozenset({p200_proto.Locus.M}),
        writes=frozenset({p200_proto.Locus.M}),
    )
    sweep_c = p200_comm.sweep_commutation(
        carrier_ensemble,
        p200_proto.non_disturbing_readout_1,
        step_m.execute,
    )
    assert sweep_c["all_commute"], "Readout_1 must commute with Step_M"
    stats["non_disturbing_readout_commutation"] += sweep_c["commuting_count"]

    # Sector D: Readout_1 vs Readout_2 -> Disjoint
    sweep_d = p200_comm.sweep_commutation(
        carrier_ensemble,
        p200_proto.non_disturbing_readout_1,
        p200_proto.non_disturbing_readout_2,
    )
    assert sweep_d["all_commute"], "Readout_1 and Readout_2 must commute"
    stats["non_disturbing_readout_commutation"] += sweep_d["commuting_count"]

    # --- Challenge 4.2: Disturbance Detection and Pricing on Overlapping Footprints ---
    # Disturbing readout at L1 mutates L1 and records cost in DIST
    cost_val = 3
    disturbing_ro = lambda s: p200_proto.disturbing_readout_1(
        s,
        probe_fn=lambda x: x,
        disturb_fn=lambda x: (x + 5) % 10,
        cost=cost_val,
    )
    # When interacting with another operation writing to L1:
    step_l1_mut = lambda s: p200_proto.intervene_l1(s, lambda x: (2 * x) % 10)

    # Check across states that non-commutation occurs and diagnostic price is incremented
    disturbance_failures = 0
    price_recorded_correctly = 0
    for s in carrier_ensemble:
        left = disturbing_ro(step_l1_mut(s))
        right = step_l1_mut(disturbing_ro(s))
        if left != right:
            disturbance_failures += 1
        # Diagnostic register must record cost
        s_after = disturbing_ro(s)
        if s_after.dist == s.dist + cost_val:
            price_recorded_correctly += 1

    assert disturbance_failures > 0, "Disturbing readout must fail commutation on overlapping footprints"
    assert price_recorded_correctly == len(carrier_ensemble), "Disturbance price must be recorded across all states"
    stats["disturbance_detection_and_pricing"] += (disturbance_failures + price_recorded_correctly)

    # --- Challenge 4.3: Duplicate Observer Agreement & Presentation Symmetries ---
    obs1, obs2 = p200_obs.create_duplicate_observers()

    for s in carrier_ensemble:
        # Swap involution: swap(swap(s)) == s
        assert p200_obs.swap_symmetry(p200_obs.swap_symmetry(s)) == s
        stats["duplicate_observer_agreement_and_symmetries"] += 1

        # Covariance: obs2.readout(swap(s)) == swap(obs1.readout(s))
        lhs = obs2.readout(p200_obs.swap_symmetry(s))
        rhs = p200_obs.swap_symmetry(obs1.readout(s))
        assert lhs == rhs, f"Swap covariance failed: lhs={lhs}, rhs={rhs}"
        stats["duplicate_observer_agreement_and_symmetries"] += 1

        # Translation symmetry across coordinate shifts
        s_trans = p200_obs.translate_symmetry(s, shift=3, modulus=10)
        assert s_trans.l1 == (s.l1 + 3) % 10
        assert s_trans.l2 == (s.l2 + 3) % 10
        stats["duplicate_observer_agreement_and_symmetries"] += 1

    # Inter-observer agreement on symmetric states
    for v in range(10):
        sym_state = p200_proto.prepare_symmetric(p200_proto.CarrierState(), v=v)
        s_both = obs2.readout(obs1.readout(sym_state))
        assert p200_proto.coincidence_evaluator(s_both) is True, f"Agreement failed for symmetric v={v}"
        assert p200_proto.record_distance(s_both) == 0
        stats["duplicate_observer_agreement_and_symmetries"] += 2

    # Negative control: Asymmetric preparation yields divergence
    for v1 in range(5):
        for v2 in range(5):
            if v1 != v2:
                asym_state = p200_proto.prepare_product(p200_proto.CarrierState(), v1=v1, v2=v2)
                s_both = obs2.readout(obs1.readout(asym_state))
                assert p200_proto.coincidence_evaluator(s_both) is False
                assert p200_proto.record_distance(s_both) == abs(v1 - v2)
                stats["duplicate_observer_agreement_and_symmetries"] += 2

    # --- Challenge 4.4: Spacelike Non-Signaling ---
    # Six distinct candidate interventions at Locus 1
    interventions = {
        "identity": lambda x: x,
        "increment": lambda x: (x + 1) % 10,
        "inversion": lambda x: 9 - x,
        "const_zero": lambda x: 0,
        "const_five": lambda x: 5,
        "affine_perm": lambda x: (3 * x + 7) % 10,
    }
    report = p200_ns.verify_spacelike_non_signaling(carrier_ensemble, interventions, obs2)
    assert report.non_signaling_satisfied, "Spacelike non-signaling must be satisfied"
    assert report.max_total_variation_distance == 0.0, (
        f"TVD must be exactly 0.0, got {report.max_total_variation_distance}"
    )
    stats["spacelike_non_signaling_invariance"] += 1

    # Correlated pair coincidence without signaling
    corr_res = p200_ns.simulate_correlated_pair_protocol(
        n_trials=200,
        modulus=4,
        intervention_1=lambda x: (x + 1) % 4,
    )
    assert corr_res["unperturbed_coincidence_rate"] == 1.0
    assert corr_res["is_non_signaling"]
    assert corr_res["marginal_tvd"] == 0.0
    stats["spacelike_non_signaling_invariance"] += 3

    # Causal propagation contrast: Signaling occurs only post-propagation through M
    contrast_res = p200_ns.simulate_causal_propagation_contrast(
        p200_proto.CarrierState(),
        intervention_val=7,
    )
    assert not contrast_res["spacelike_shift_detected"], "Spacelike separation must exhibit zero shift"
    assert contrast_res["causal_shift_detected"], "Post-propagation through M must exhibit detected causal shift"
    assert contrast_res["information_transferred_post_coupling"]
    stats["spacelike_non_signaling_invariance"] += 3

    print(f"P200 checks passed: {stats}")
    return stats


# ==============================================================================
# 5. Repository Seal and Axiom Cleanliness Audits
# ==============================================================================

def run_seal_and_axiom_audits() -> dict[str, int]:
    """Audit repository seal integrity and constructive axiom cleanliness."""
    print("=== [5/5] Repository Seal & Axiom Cleanliness Audits ===")
    stats = {
        "repository_seal_checks": 0,
        "axiom_cleanliness_checks": 0,
    }

    # --- Challenge 5.1: Repository Seal Audit ---
    # Run git status --short to verify zero modifications to sealed directories
    git_proc = subprocess.run(
        ["git", "status", "--short"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    status_output = git_proc.stdout.strip()
    sealed_prefixes = [
        "prompt/",
        "paper/",
        "code/",
        "lean4/Derivation/",
        "artifacts/",
        "CLAUDE.md",
    ]

    for line in status_output.splitlines():
        if not line.strip():
            continue
        # Status format: XY <path> or XY <path1> -> <path2>
        parts = line.strip().split(maxsplit=1)
        if len(parts) < 2:
            continue
        rel_path = parts[1].replace("\\", "/")
        for prefix in sealed_prefixes:
            if rel_path.startswith(prefix) or rel_path == prefix:
                raise AssertionError(f"Repository seal violated! Modified sealed file: {rel_path}")

    # Mark pass for each sealed directory boundary verified
    for _ in sealed_prefixes:
        stats["repository_seal_checks"] += 1

    # --- Challenge 5.2: Axiom Cleanliness Audit ---
    receipt_paths = {
        "G012": REPO_ROOT / "research" / "g012_typed_translation" / "evidence" / "receipt.json",
        "G013": REPO_ROOT / "research" / "g013_trace_calculus" / "evidence" / "receipt.json",
        "G018": REPO_ROOT / "research" / "g018_self_hosting" / "evidence" / "receipt.json",
        "P200": REPO_ROOT / "research" / "p200_operational_protocols" / "evidence" / "receipt.json",
    }
    allowed_axioms_set = {"propext", "Quot.sound"}

    for target_name, path in receipt_paths.items():
        assert path.exists(), f"Evidence receipt missing for {target_name} at {path}"
        with open(path, "r", encoding="utf-8") as f:
            receipt_data = json.load(f)

        # 1. Status verification
        if target_name in ("G012", "G013", "G018"):
            assert receipt_data.get("lean_audit", {}).get("status") == "PASS"
            disallowed = receipt_data.get("lean_audit", {}).get("disallowed_axioms_detected", [])
            assert len(disallowed) == 0, f"Disallowed axioms found in {target_name}: {disallowed}"
            allowed = receipt_data.get("lean_audit", {}).get("allowed_axioms", [])
            assert set(allowed).issubset(allowed_axioms_set), f"Non-constructive axioms in {target_name}: {allowed}"
        elif target_name == "P200":
            assert receipt_data.get("status") == "PASS"
            reports = receipt_data.get("lean", {}).get("reports", {})
            for thm, axioms in reports.items():
                assert set(axioms).issubset(allowed_axioms_set), f"Non-constructive axioms in theorem {thm}: {axioms}"
            ch = receipt_data.get("claim_hygiene", {})
            assert ch.get("zero_classical_choice") is True
            assert ch.get("zero_mathlib") is True

        # Assert no Classical.choice in allowed axioms or theorem reports
        receipt_str = json.dumps(receipt_data)
        assert "Classical.choice" not in receipt_str, f"Classical.choice detected in {target_name} receipt!"

        # Verify lakefile has zero mathlib dependency
        lakefile_path = path.parent.parent / "lean" / "lakefile.toml"
        if lakefile_path.exists():
            lakefile_content = lakefile_path.read_text(encoding="utf-8")
            assert "mathlib" not in lakefile_content.lower(), f"Mathlib dependency found in {lakefile_path}"

        stats["axiom_cleanliness_checks"] += 5

    print(f"Seal and axiom checks passed: {stats}")
    return stats


# ==============================================================================
# Main Verification Suite & Receipt Emission
# ==============================================================================

def main() -> None:
    t0 = time.time()
    print("================================================================================")
    print("Genesis Cohort 4 Lead Architect & Adversarial Critic Review Gate")
    print("Target Suite: G012, G013, G018, P200, Seal & Axiom Audits")
    print("================================================================================")

    stats_g012 = run_g012_adversarial_tests()
    stats_g013 = run_g013_adversarial_tests()
    stats_g018 = run_g018_adversarial_tests()
    stats_p200 = run_p200_adversarial_tests()
    stats_audit = run_seal_and_axiom_audits()

    total_checks = (
        sum(stats_g012.values())
        + sum(stats_g013.values())
        + sum(stats_g018.values())
        + sum(stats_p200.values())
        + sum(stats_audit.values())
    )

    elapsed = time.time() - t0
    print("================================================================================")
    print(f"ALL ADVERSARIAL CHALLENGES PASSED in {elapsed:.2f}s")
    print(f"Total verified checks, states, and transition proofs: {total_checks}")
    print("Lead Architect Verdict: APPROVE")
    print("Adversarial Critic Verdict: APPROVE")
    print("================================================================================")

    receipt = {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "verdict": "APPROVE",
        "lead_architect_verdict": "APPROVE",
        "adversarial_critic_verdict": "APPROVE",
        "total_checks": total_checks,
        "elapsed_seconds": round(elapsed, 4),
        "target_breakdown": {
            "g012_typed_translation": stats_g012,
            "g013_trace_calculus": stats_g013,
            "g018_self_hosting": stats_g018,
            "p200_operational_protocols": stats_p200,
            "seal_and_axiom_audit": stats_audit,
        },
        "claim_hygiene_scope": {
            "G012": "Constructive typed translation, relational grammar codec, exact rational distortion vector, 1459-prefix recovery",
            "G013": "Higher 2-cell trace calculus, Middle Four interchange law, endpoint factorization, observer trace congruence, price cocycle",
            "G018": "Zero-oracle step simulation, micro-step cycle decomposition, reflection boundary, diagonal self-oracle obstruction",
            "P200": "Operational protocols, non-disturbing readout commutation, duplicate observer covariance, spacelike non-signaling",
            "RepositorySeal": "Zero modifications to prompt/, paper/, code/, lean4/Derivation/, artifacts/, or CLAUDE.md",
            "AxiomCleanliness": "All formal proofs strictly constructive in {propext, Quot.sound} with zero Classical.choice and zero mathlib",
        },
    }

    receipt_path = REPO_ROOT / "research" / "e2e_tests" / "evidence_adversarial_cohort4.json"
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)
    print(f"Receipt written to: {receipt_path}")


if __name__ == "__main__":
    main()
