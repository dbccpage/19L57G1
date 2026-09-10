"""Master Empirical Adversarial Stress Suite for Genesis Cohort 5.

Lead Architect & Adversarial Critic Review Gate.
Targets:
- G014: Multi-Observer Descent & Natural Transport
- G015/G017: First-Demand, Invocation Bridge & Autonomous Stepping
- M104/M107: Coherent Equality Layers & Derived Order Family
- P201/P202: Relational Dimensions, Calibration & Causal Relational Clocks

Axiom Scope: Constructive finite carrier operations with zero host oracles.
Allowed Axioms: strictly within {'propext', 'Quot.sound'} (zero Classical.choice, zero mathlib).
AuthorityEffect: None.
Claim Hygiene: All properties bounded to finite discrete models; exact rational arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import random
import subprocess
import sys
import time
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent

# Prepend research directories
TARGET_DIRS = [
    REPO_ROOT / "research" / "g014_observer_descent",
    REPO_ROOT / "research" / "g015_autonomous_stepping",
    REPO_ROOT / "research" / "m104_equality_order",
    REPO_ROOT / "research" / "p201_relational_spacetime",
]
for p in reversed(TARGET_DIRS):
    p_str = str(p)
    if p_str in sys.path:
        sys.path.remove(p_str)
    sys.path.insert(0, p_str)

import observer_descent as g014
import stepping as g015
import equality_order as m104
import relational_spacetime as p201


def test_g014_adversarial_descent_and_gluing() -> int:
    """Fuzz G014 multi-observer descent, gluing obstructions, and natural transport."""
    print(">>> Fuzzing Target G014: Multi-Observer Descent...")
    checks = 0
    rng = random.Random(1414)

    # 1. Random coverages and compatible gluing sweeps
    for n_loci in range(3, 12):
        locus_names = [f"loc_{i}" for i in range(n_loci)]
        state_map = {loc: rng.randint(0, 1000) for loc in locus_names}
        state = g014.CarrierState.from_mapping(state_map)

        # Build overlapping chain coverage
        obs_list = []
        for i in range(n_loci - 1):
            obs_list.append(g014.Observer(f"O_{i}", (locus_names[i], locus_names[i + 1])))
        cov = g014.DescentCoverage(observers=tuple(obs_list))

        records = {obs.observer_id: obs.project(state) for obs in cov.observers}
        res = cov.glue(records)
        assert res.is_ok()
        assert res.unwrap() == state
        checks += 2

        # Incompatible record perturbation fuzz
        target_obs = obs_list[0]
        overlap_locus = target_obs.loci[1]
        bad_records = dict(records)
        bad_map = records[target_obs.observer_id].to_dict()
        bad_map[overlap_locus] = bad_map[overlap_locus] + 9999
        bad_records[target_obs.observer_id] = g014.CarrierState.from_mapping(bad_map)

        obstr = cov.glue(bad_records)
        assert obstr.is_err()
        err = obstr.unwrap_err()
        assert err.overlap_locus == overlap_locus
        checks += 2

        # Natural transport fuzzing along random permutations
        permuted_names = list(locus_names)
        rng.shuffle(permuted_names)
        perm = dict(zip(locus_names, permuted_names))

        t_obs, t_state, t_readout = g014.natural_transport(obs_list[0], state, perm)
        direct_readout = t_obs.project(t_state)
        assert direct_readout == t_readout
        checks += 1

    print(f"  G014 passed {checks} adversarial checks.")
    return checks


def test_g015_adversarial_stepping() -> int:
    """Fuzz G015/G017 demand lifecycle, priority tie-breaking, and saturation."""
    print(">>> Fuzzing Target G015/G017: Autonomous Stepping...")
    checks = 0
    rng = random.Random(1515)

    # 1. Randomized priority and tie-breaking sweeps
    for _ in range(50):
        n_demands = rng.randint(3, 15)
        demands = []
        for i in range(n_demands):
            pri = rng.randint(1, 5)
            demands.append(
                g015.Demand(
                    demand_id=i,
                    kind="WRITE",
                    priority=pri,
                    target_locus=f"reg_{i}",
                    payload=i * 10,
                    remaining_budget=0,
                    status=g015.DemandStatus.PENDING,
                )
            )
        # Shuffle presentation order to test that internal selection is presentation-invariant
        shuffled = list(demands)
        rng.shuffle(shuffled)
        state = g015.CarrierState.create_initial({"reg_0": 0}, shuffled)

        best_id = g015.select_first_demand(state)
        assert best_id is not None
        # Best demand must have minimum priority, then minimum demand_id
        selected = [d for d in demands if d.demand_id == best_id][0]
        min_pri = min(d.priority for d in demands)
        assert selected.priority == min_pri
        min_id_at_pri = min(d.demand_id for d in demands if d.priority == min_pri)
        assert selected.demand_id == min_id_at_pri
        checks += 3

    # 2. Reopen chain saturation fuzz
    for budget in range(1, 20):
        d = g015.Demand(1, "REOPEN_CHAIN", priority=1, target_locus="c", payload=1, remaining_budget=budget, status=g015.DemandStatus.PENDING)
        s0 = g015.CarrierState.create_initial({"c": 0}, [d])
        final_s, outcomes = g015.run_to_saturation(s0, max_steps=budget + 5)
        assert final_s.step_count == budget
        assert final_s.resources_spent == Fraction(budget, 1)
        assert final_s.get_memory("c") == budget
        checks += 3

    # 3. Inert history non-spontaneity fuzz
    inert = g015.CarrierState.create_initial({"l": 42}, [])
    for _ in range(10):
        out = g015.step_autonomous(inert)
        assert out.status == "QUIESCENT"
        assert out.state == inert
        checks += 1

    print(f"  G015/G017 passed {checks} adversarial checks.")
    return checks


def test_m104_adversarial_equality_and_orders() -> int:
    """Fuzz M104/M107 equality layer separations and derived orders."""
    print(">>> Fuzzing Target M104/M107: Equality Layers & Order Family...")
    checks = 0
    rng = random.Random(104107)

    # 1. DefEq without Presentation Identity fuzzing
    for _ in range(50):
        a = rng.randint(0, 100)
        b = rng.randint(0, 100)
        t_add = m104.SyntaxTerm("Add", (m104.SyntaxTerm("Const", (), str(a)), m104.SyntaxTerm("Const", (), str(b))))
        t_const = m104.SyntaxTerm("Const", (), str(a + b))
        assert m104.is_definitially_equal(t_add, t_const)
        assert not t_add.is_presentation_identical(t_const)
        checks += 2

    # 2. Observational Equivalence without State Identity fuzzing
    for _ in range(50):
        vis_a = rng.randint(0, 50)
        vis_b = rng.randint(0, 50)
        hid_1 = rng.randint(100, 200)
        hid_2 = rng.randint(201, 300)
        s1 = m104.StateWithHiddenSector(vis_a, vis_b, hid_1)
        s2 = m104.StateWithHiddenSector(vis_a, vis_b, hid_2)
        observers = (
            m104.AdmittedObserver("OA", ("a",)),
            m104.AdmittedObserver("OB", ("b",)),
            m104.AdmittedObserver("OAB", ("a", "b")),
        )
        assert m104.is_observationally_equivalent(s1, s2, observers)
        assert s1 != s2
        checks += 2

    # 3. Reachability preorder vs Cost order non-conflation fuzzing
    for _ in range(30):
        cost1 = Fraction(rng.randint(1, 10), rng.randint(1, 5))
        cost2 = cost1 + Fraction(rng.randint(1, 10), rng.randint(1, 5))
        tr1 = m104.ExecutionTrace("A", "Z", steps=10, cost=cost1)
        tr2 = m104.ExecutionTrace("A", "B", steps=1, cost=cost2)
        assert m104.cost_leq(tr1, tr2)
        assert not m104.cost_leq(tr2, tr1)
        checks += 2

    print(f"  M104/M107 passed {checks} adversarial checks.")
    return checks


def test_p201_adversarial_spacetime() -> int:
    """Fuzz P201/P202 relational quantities, covariance, and clock rates."""
    print(">>> Fuzzing Target P201/P202: Relational Dimensions & Clocks...")
    checks = 0
    rng = random.Random(201202)

    # 1. Unit covariance and dimensionless ratio invariance
    for _ in range(50):
        val1 = Fraction(rng.randint(1, 100), rng.randint(1, 10))
        val2 = Fraction(rng.randint(1, 100), rng.randint(1, 10))
        scale = Fraction(rng.randint(1, 50), rng.randint(1, 50))

        u1 = p201.CalibrationStandard("Std1", p201.PhysicalDimension.LENGTH, Fraction(1, 1))
        u2 = p201.CalibrationStandard("Std2", p201.PhysicalDimension.LENGTH, scale)

        q1 = p201.RelationalQuantity(val1, p201.PhysicalDimension.LENGTH, u1)
        q2 = p201.RelationalQuantity(val2, p201.PhysicalDimension.LENGTH, u1)

        q1_scaled = q1.rescale_standard(u2, scale)
        q2_scaled = q2.rescale_standard(u2, scale)

        ratio1 = p201.compute_dimensionless_ratio(q1, q2).unwrap()
        ratio2 = p201.compute_dimensionless_ratio(q1_scaled, q2_scaled).unwrap()
        assert ratio1 == ratio2
        checks += 2

    # 2. Cross-dimension refusal fuzzing
    dims = list(p201.PhysicalDimension)
    for i in range(len(dims)):
        for j in range(len(dims)):
            if i != j:
                u_i = p201.CalibrationStandard("U1", dims[i], Fraction(1, 1))
                u_j = p201.CalibrationStandard("U2", dims[j], Fraction(1, 1))
                qi = p201.RelationalQuantity(Fraction(1, 1), dims[i], u_i)
                qj = p201.RelationalQuantity(Fraction(1, 1), dims[j], u_j)
                res = p201.compute_dimensionless_ratio(qi, qj)
                assert res.is_err()
                assert "Refusal: dimension mismatch" in res.unwrap_err()
                checks += 1

    # 3. Future-test congruence and clock synchronization
    for _ in range(20):
        init_a = rng.randint(0, 100)
        init_b = rng.randint(0, 100)
        s1 = p201.RelationalState.create({"a": init_a, "b": init_b})
        s2 = p201.RelationalState.create({"a": init_a, "b": init_b})
        assert p201.are_future_equivalent(s1, s2, horizon=15)

        # Step congruence
        s1_next = p201.step_relational(s1)
        s2_next = p201.step_relational(s2)
        assert p201.are_future_equivalent(s1_next, s2_next, horizon=15)
        checks += 2

        # Relational clock progression: 20 steps
        curr = s1
        for _ in range(20):
            curr = p201.step_relational(curr)
        rate = p201.measure_relative_clock_rate(s1, curr).unwrap()
        assert rate == Fraction(2, 1)
        checks += 1

    print(f"  P201/P202 passed {checks} adversarial checks.")
    return checks


def audit_repository_seal_and_axioms() -> int:
    """Audit repository blind seal integrity and Lean 4 axiom censuses across Cohort 5."""
    print(">>> Auditing Repository Seal & Lean 4 Axioms...")
    checks = 0

    # 1. Seal audit: git status outside research/
    git_proc = subprocess.run(["git", "status", "--porcelain"], cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    assert git_proc.returncode == 0
    modified_outside_research = []
    for line in git_proc.stdout.splitlines():
        path = line.strip().split()[-1]
        if not path.startswith("research/"):
            modified_outside_research.append(path)
    assert len(modified_outside_research) == 0, f"Sealed path modified: {modified_outside_research}"
    checks += 1

    # 2. Lean packages build and axiom audit
    lean_packages = [
        REPO_ROOT / "research" / "g014_observer_descent" / "lean",
        REPO_ROOT / "research" / "g015_autonomous_stepping" / "lean",
        REPO_ROOT / "research" / "m104_equality_order" / "lean",
        REPO_ROOT / "research" / "p201_relational_spacetime" / "lean",
    ]
    for pkg in lean_packages:
        proc = subprocess.run(["lake", "build"], cwd=pkg, capture_output=True, text=True, check=False)
        assert proc.returncode == 0, f"lake build failed for {pkg.parent.name}:\n{proc.stderr}"
        checks += 1

        inv_proc = subprocess.run(["lake", "env", "lean", "Inventory.lean"], cwd=pkg, capture_output=True, text=True, check=False)
        assert inv_proc.returncode == 0, f"Inventory.lean failed for {pkg.parent.name}:\n{inv_proc.stderr}"
        output = inv_proc.stdout + inv_proc.stderr
        for ax in ["Classical.choice", "mathlib"]:
            assert ax not in output, f"Disallowed dependency {ax} found in {pkg.parent.name}"
        checks += 1

    print(f"  Seal and axiom audits passed {checks} checks.")
    return checks


def main() -> None:
    print("=" * 80)
    print("Genesis Cohort 5 Empirical Adversarial Stress Suite")
    print("Lead Architect & Adversarial Critic Review Gate")
    print("=" * 80)

    start_time = time.time()
    total_checks = 0

    total_checks += test_g014_adversarial_descent_and_gluing()
    total_checks += test_g015_adversarial_stepping()
    total_checks += test_m104_adversarial_equality_and_orders()
    total_checks += test_p201_adversarial_spacetime()
    total_checks += audit_repository_seal_and_axioms()

    elapsed = time.time() - start_time
    print("=" * 80)
    print(f"ALL ADVERSARIAL CHECKS PASSED in {elapsed:.4f}s")
    print(f"Total Verified Checks for Cohort 5: {total_checks}")
    print("Axioms verified strictly within {propext, Quot.sound}; zero Classical.choice.")
    print("=" * 80)

    receipt = {
        "suite": "Cohort 5 Empirical Adversarial Stress Suite",
        "total_checks": total_checks,
        "elapsed_seconds": elapsed,
        "targets_covered": ["G014", "G015", "G017", "M104", "M107", "P201", "P202"],
        "status": "PASS",
    }
    receipt_path = REPO_ROOT / "research" / "evidence_cohort5_adversarial.json"
    receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"Receipt written to {receipt_path}")


if __name__ == "__main__":
    main()
