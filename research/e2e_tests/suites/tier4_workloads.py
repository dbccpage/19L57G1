"""Tier 4: Real-World Workload Scenarios E2E Test Suite.

Executes realistic multi-step workloads across Genesis Cohort 2 substrates:
1. Complete autonomous program loop with memory recording and terminal resolution
2. Cyclic process limiting frequency convergence across geometric scales
3. Full 9-criteria charter evaluation of an admitted substrate candidate
4. Endogenous address allocation, program synthesis, and capability-restricted execution

Adheres strictly to the Claim Hygiene Rule and constructive finite boundaries.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

E2E_ROOT = Path(__file__).resolve().parent.parent
if str(E2E_ROOT) not in sys.path:
    sys.path.insert(0, str(E2E_ROOT))

from harness import (
    AdequacyDimension,
    Capability,
    ComparisonMorphism,
    FreshnessGenerator,
    MemoryState,
    Ordinal,
    State,
    TargetSystem,
    Terminal,
    TreeAddress,
    check_zeros_bound,
    evaluate_system,
    execute_restricted,
    make_program,
    obs_scale,
    rational_frequency,
    run_det,
    step_det,
    step_with_memory,
)


def test_w01_complete_autonomous_program_loop() -> None:
    """Complete autonomous program loop with memory recording and terminal resolution."""
    # Program: 0 -> 1 -> 2 -> 3 -> 4 (halt)
    transitions = [(0, i, i + 1) for i in range(4)]
    enablements = [(i, 0) for i in range(4)]  # Datum 4 has no enablement -> halt
    prog = make_program(nops=1, transitions=transitions, enablements=enablements)

    s0 = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=10)
    ms = MemoryState(base_state=s0, records=())

    steps = 0
    while True:
        nxt = step_with_memory(ms)
        if isinstance(nxt, Terminal):
            assert nxt is Terminal.HALT
            break
        ms = nxt
        steps += 1

    assert steps == 4
    assert ms.base_state.active == 4
    assert ms.base_state.tape == (0, 1, 2, 3, 4)
    assert ms.base_state.clock == 4
    assert ms.base_state.fuel == 6

    # Verify memory growth
    depth1_records = [r for r in ms.records if r.depth == 1]
    depth2_records = [r for r in ms.records if r.depth == 2]
    assert len(depth1_records) == 4
    assert len(depth2_records) == 3  # (0,1,2), (1,2,3), (2,3,4)
    assert depth2_records[-1].payload == (2, 3, 4)


def test_w02_cyclic_process_limiting_frequency_convergence() -> None:
    """Cyclic process limiting frequency convergence across geometric observation scales."""
    # 3-cycle: 0 -> 1 -> 2 -> 0
    prog = make_program(
        nops=1,
        transitions=[(0, 0, 1), (0, 1, 2), (0, 2, 0)],
        enablements=[(0, 0), (1, 0), (2, 0)],
    )
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=200)

    scales = [3, 6, 12, 24, 48, 96]
    previous_error = float("inf")

    for L in scales:
        # Observe tape of length L+1 (start datum + L transitions)
        tape = obs_scale(L, s)
        transitions_observed = tape[1:]  # Exactly L steps
        assert len(transitions_observed) == L

        zeros_count, total = rational_frequency(transitions_observed, target=0)
        assert total == L

        # 1. Verify exact integer zeros bound: L <= 3 * zeros <= L + 2
        assert check_zeros_bound(L, zeros_count)

        # 2. Verify rational precision bound: |zeros/L - 1/3| <= 2 / (3L)
        freq = zeros_count / L
        error = abs(freq - 1/3)
        max_error = 2 / (3 * L)
        assert error <= max_error + 1e-9

        # 3. Verify monotonic precision tightening as scale increases
        assert max_error < previous_error
        previous_error = max_error


def test_w03_full_nine_criteria_charter_evaluation() -> None:
    """Full 9-criteria charter evaluation of an admitted substrate candidate."""
    # Candidate substrate providing formal constructive evidence objects
    substrate = TargetSystem(
        name="AdmittedConstructiveSubstrate",
        dimension_scores={
            AdequacyDimension.COMPUTATIONAL_UNIVERSALITY: True,
            AdequacyDimension.REASONING_ADEQUACY: True,
            AdequacyDimension.REPRESENTATIONAL_COMPLETENESS: True,
            AdequacyDimension.MATHEMATICAL_FOUNDATIONS: True,
            AdequacyDimension.PHYSICAL_ADEQUACY: True,
            AdequacyDimension.EMPIRICAL_ADEQUACY: True,
            AdequacyDimension.CALCULUS_UNIQUENESS: True,
            AdequacyDimension.PHYSICAL_MODEL_UNIQUENESS: True,
            AdequacyDimension.COMPARISON_MORPHISMS: True,
        },
        metadata={
            "charter_status": "TOE_TARGET_CLASS_FROZEN",
            "lean4_axioms": "{propext, Quot.sound}",
            "classical_choice": False,
            "mathlib": False,
        },
    )

    # Evaluate against frozen charter
    is_admitted, met_count = evaluate_system(substrate)
    assert is_admitted is True
    assert met_count == 9

    # Reference target system
    reference = TargetSystem(
        name="ReferenceStandardModel",
        dimension_scores={dim: True for dim in AdequacyDimension},
    )

    # Establish comparison morphism
    morphism = ComparisonMorphism(
        source=substrate,
        target=reference,
        mapping_name="SubstrateSimulationEmbedding",
        preserves_adequacy=True,
    )
    assert morphism.preserves_adequacy is True
    assert morphism.source.name == "AdmittedConstructiveSubstrate"
    assert morphism.target.name == "ReferenceStandardModel"


def test_w04_endogenous_synthesis_and_execution_pipeline() -> None:
    """Endogenous address allocation, program synthesis, and capability-restricted execution."""
    gen = FreshnessGenerator()
    root = TreeAddress.root()

    # Endogenously allocate 3 disjoint node addresses
    addr0 = gen.fresh_address(root)
    addr1 = gen.fresh_address(root)
    addr2 = gen.fresh_address(root)
    assert addr0.path != addr1.path and addr1.path != addr2.path

    # Extract internal integer IDs from addresses
    n0, n1, n2 = addr0.path[0], addr1.path[0], addr2.path[0]

    # Synthesize linear transition graph
    transitions = [(0, n0, n1), (0, n1, n2)]
    enablements = [(n0, 0), (n1, 0)]
    prog = make_program(nops=1, transitions=transitions, enablements=enablements)

    # Execute under full capabilities
    caps = frozenset([Capability.DIRECT_LOOKUP])
    res_success = execute_restricted(prog, allowed_caps=caps, required_caps=caps, start=n0, fuel=5, nops=1)
    assert res_success.status == "halt"
    assert res_success.output == (n0, n1, n2)

    # Execute under removed capability
    res_obstructed = execute_restricted(prog, allowed_caps=frozenset(), required_caps=caps, start=n0, fuel=5, nops=1)
    assert res_obstructed.status == "OBSTRUCTED_CAPABILITY_ABSENT"
    assert res_obstructed.output == ()
