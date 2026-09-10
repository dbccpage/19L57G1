"""stress_adversarial_iso.py — Adversarial Stress Test Suite for CL-ISO-SOUND.

Adversarial exploration for ternary and higher-arity relations under
canonicalization and partition refinement (code/derivation/iso.py).

Test dimensions:
1. Empty and degenerate edge cases (0 data, all-equal triples, data-only).
2. Highly symmetric ternary structures (cyclic permutations, alternating relations).
3. Steiner Triple Systems / Fano plane blocks (3-uniform hypergraphs, Aut=168, Aut=21).
4. High automorphism counts (complete 3-uniform hypergraphs, S_4, S_5 actions).
5. Quaternary relations (arity 4) and multi-form cross-permutations.
6. Full pairwise cross-check matrix:
   canonical(A) == canonical(B) <===> canonical_bruteforce(A) == canonical_bruteforce(B).

AuthorityEffect: None.
"""

from __future__ import annotations

from itertools import combinations, permutations
import random
import sys
import time
from typing import Sequence

# Setup import paths
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "code"))
sys.path.insert(0, str(REPO_ROOT / "research" / "iso_sound"))

from derivation.iso import (  # noqa: E402
    IsoBudgetError,
    automorphisms,
    canonical,
    canonical_bruteforce,
    find_iso,
    isomorphic,
    rename,
    serialize,
)
from derivation.model import Regime  # noqa: E402


def run_adversarial_suite() -> dict[str, object]:
    results: dict[str, object] = {}
    failures: list[str] = []
    tests_run = 0

    print("=" * 70)
    print("STARTING ADVERSARIAL STRESS SUITE FOR CL-ISO-SOUND")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # SUITE 1: Empty and Degenerate Boundary Cases
    # -------------------------------------------------------------------------
    print("\n[Suite 1] Empty and Degenerate Boundary Cases...")
    r_empty = Regime((), (), frozenset(), frozenset(), frozenset())
    assert canonical(r_empty) == canonical_bruteforce(r_empty)
    tests_run += 1

    # Data-only regimes with ternary form
    for n in (1, 2, 3, 4, 5):
        r_data_only = Regime(
            tuple(f"d{i}" for i in range(n)),
            (3,),
            frozenset(),
            frozenset(),
            frozenset(),
        )
        tests_run += 1
        can = canonical(r_data_only)
        brute = canonical_bruteforce(r_data_only)
        if can != brute:
            failures.append(f"Suite 1: Data-only n={n} can != brute")
        # Rename and check invariance
        for _ in range(5):
            pi = tuple(random.sample(range(n), n))
            r_perm = rename(r_data_only, pi, (0,))
            if canonical(r_perm) != can:
                failures.append(f"Suite 1: Data-only n={n} permuted can != can")
            if canonical_bruteforce(r_perm) != brute:
                failures.append(f"Suite 1: Data-only n={n} permuted brute != brute")
            tests_run += 2

    # Degenerate all-equal triples: (x, x, x)
    r_diag = Regime(
        ("a", "b", "c"),
        (3,),
        frozenset([(0, (0, 0, 0)), (0, (1, 1, 1))]),
        frozenset(),
        frozenset(),
    )
    can_diag = canonical(r_diag)
    brute_diag = canonical_bruteforce(r_diag)
    tests_run += 1
    for pi in permutations(range(3)):
        rp = rename(r_diag, pi, (0,))
        if canonical(rp) != can_diag:
            failures.append(f"Suite 1: Diag perm {pi} can != can_diag")
        if canonical_bruteforce(rp) != brute_diag:
            failures.append(f"Suite 1: Diag perm {pi} brute != brute_diag")
        tests_run += 2

    # Mixed degenerate triples: (x, x, y), (x, y, x), (y, x, x)
    r_mixed_deg = Regime(
        ("a", "b"),
        (3,),
        frozenset([(0, (0, 0, 1)), (0, (0, 1, 0)), (0, (1, 0, 0))]),
        frozenset(),
        frozenset(),
    )
    can_md = canonical(r_mixed_deg)
    brute_md = canonical_bruteforce(r_mixed_deg)
    tests_run += 1
    for pi in permutations(range(2)):
        rp = rename(r_mixed_deg, pi, (0,))
        if canonical(rp) != can_md:
            failures.append(f"Suite 1: Mixed deg perm {pi} can != can_md")
        if canonical_bruteforce(rp) != brute_md:
            failures.append(f"Suite 1: Mixed deg perm {pi} brute != brute_md")
        tests_run += 2

    print(f"  Passed Suite 1 ({tests_run} assertions, {len(failures)} failures).")

    # -------------------------------------------------------------------------
    # SUITE 2: Cyclic Ternary Permutations & Alternating Relations
    # -------------------------------------------------------------------------
    print("\n[Suite 2] Cyclic Ternary Permutations & Alternating Relations...")
    s2_start = tests_run
    # r_even: cyclic shifts of (0, 1, 2)
    r_even = Regime(
        ("0", "1", "2"),
        (3,),
        frozenset([(0, (0, 1, 2)), (0, (1, 2, 0)), (0, (2, 0, 1))]),
        frozenset(),
        frozenset(),
    )
    # r_odd: cyclic shifts of (0, 2, 1)
    r_odd = Regime(
        ("0", "1", "2"),
        (3,),
        frozenset([(0, (0, 2, 1)), (0, (2, 1, 0)), (0, (1, 0, 2))]),
        frozenset(),
        frozenset(),
    )
    # They are isomorphic via swap (1, 2)
    can_even = canonical(r_even)
    can_odd = canonical(r_odd)
    brute_even = canonical_bruteforce(r_even)
    brute_odd = canonical_bruteforce(r_odd)

    if can_even != can_odd:
        failures.append("Suite 2: r_even and r_odd must have equal canonical key")
    if brute_even != brute_odd:
        failures.append("Suite 2: r_even and r_odd must have equal brute key")
    tests_run += 2

    # All automorphisms of r_even: since all 3 cyclic shifts are in r_even,
    # cyclic shifts are automorphisms. Any odd permutation (e.g. (0 1)) maps r_even to r_odd,
    # which is NOT equal to r_even as a set of tuples!
    # So Aut(r_even) as directed tuples has order exactly 3 (A_3 = C_3)!
    autos_even = automorphisms(r_even)
    if len(autos_even) != 3:
        failures.append(f"Suite 2: Aut(r_even) expected 3, got {len(autos_even)}")
    tests_run += 1

    # Now add requirements breaking symmetry
    # r_even_req: reqs = {(0, 1)}
    r_even_req = Regime(
        ("0", "1", "2"),
        (3,),
        frozenset([(0, (0, 1, 2)), (0, (1, 2, 0)), (0, (2, 0, 1))]),
        frozenset(),
        frozenset([(0, 1)]),
    )
    # Under swap (0, 1), req {(0, 1)} is preserved, but r_even goes to r_odd!
    # So r_even_req is isomorphic to r_odd_req!
    r_odd_req = Regime(
        ("0", "1", "2"),
        (3,),
        frozenset([(0, (0, 2, 1)), (0, (2, 1, 0)), (0, (1, 0, 2))]),
        frozenset(),
        frozenset([(0, 1)]),
    )
    if canonical(r_even_req) != canonical(r_odd_req):
        failures.append("Suite 2: r_even_req and r_odd_req must be isomorphic")
    if canonical_bruteforce(r_even_req) != canonical_bruteforce(r_odd_req):
        failures.append("Suite 2: r_even_req and r_odd_req brute must match")
    tests_run += 2

    # Now compare against a non-isomorphic ternary relation:
    # r_linear: (0, 1, 2) and (1, 2, 0), but missing (2, 0, 1)
    r_linear = Regime(
        ("0", "1", "2"),
        (3,),
        frozenset([(0, (0, 1, 2)), (0, (1, 2, 0))]),
        frozenset(),
        frozenset(),
    )
    if canonical(r_even) == canonical(r_linear):
        failures.append("Suite 2: r_even and r_linear falsely merged!")
    if canonical_bruteforce(r_even) == canonical_bruteforce(r_linear):
        failures.append("Suite 2: r_even and r_linear brute falsely merged!")
    tests_run += 2

    # 5-element cyclic tournament
    c5_triples = frozenset((0, ((i) % 5, (i + 1) % 5, (i + 2) % 5)) for i in range(5))
    r_c5 = Regime(tuple(f"d{i}" for i in range(5)), (3,), c5_triples, frozenset(), frozenset())
    can_c5 = canonical(r_c5)
    brute_c5 = canonical_bruteforce(r_c5)
    for _ in range(10):
        pi = tuple(random.sample(range(5), 5))
        rp = rename(r_c5, pi, (0,))
        if canonical(rp) != can_c5:
            failures.append("Suite 2: C5 tournament rename can mismatch")
        if canonical_bruteforce(rp) != brute_c5:
            failures.append("Suite 2: C5 tournament rename brute mismatch")
        tests_run += 2

    print(f"  Passed Suite 2 ({tests_run - s2_start} assertions, {len(failures)} failures).")

    # -------------------------------------------------------------------------
    # SUITE 3: Steiner Triple Systems and Fano Plane Blocks (3-uniform hypergraphs)
    # -------------------------------------------------------------------------
    print("\n[Suite 3] Steiner Triple Systems / Fano Plane Blocks...")
    s3_start = tests_run
    # The 7 lines of the Fano plane PG(2, 2):
    fano_blocks = [
        (0, 1, 3),
        (1, 2, 4),
        (2, 3, 5),
        (3, 4, 6),
        (4, 5, 0),
        (5, 6, 1),
        (6, 0, 2),
    ]
    # Fully undirected 3-uniform hypergraph: all 6 permutations per block
    fano_full_insts = frozenset(
        (0, perm) for b in fano_blocks for perm in permutations(b)
    )
    r_fano_full = Regime(
        tuple(f"p{i}" for i in range(7)),
        (3,),
        fano_full_insts,
        frozenset(),
        frozenset(),
    )
    # This is a 1-orbit, highly symmetric hypergraph.
    # Automorphism group of Fano plane is PGL(3, 2) which has order 168!
    t0 = time.time()
    can_fano = canonical(r_fano_full)
    dt_can = time.time() - t0
    print(f"    Fano full canonical computed in {dt_can:.3f}s")

    t0 = time.time()
    brute_fano = canonical_bruteforce(r_fano_full)
    dt_brute = time.time() - t0
    print(f"    Fano full bruteforce computed in {dt_brute:.3f}s")

    # Automorphism check:
    autos_fano = automorphisms(r_fano_full)
    print(f"    Fano full automorphisms count: {len(autos_fano)} (expected 168)")
    if len(autos_fano) != 168:
        failures.append(f"Suite 3: Fano full Aut expected 168, got {len(autos_fano)}")
    tests_run += 1

    # Permuted Fano planes
    rng = random.Random(1337)
    for trial in range(8):
        pi = tuple(rng.sample(range(7), 7))
        r_fano_perm = rename(r_fano_full, pi, (0,))
        if canonical(r_fano_perm) != can_fano:
            failures.append(f"Suite 3: Fano perm {trial} can != can_fano")
        if canonical_bruteforce(r_fano_perm) != brute_fano:
            failures.append(f"Suite 3: Fano perm {trial} brute != brute_fano")
        # find_iso must succeed
        iso_witness = find_iso(r_fano_full, r_fano_perm)
        if iso_witness is None:
            failures.append(f"Suite 3: find_iso failed on isomorphic Fano perm {trial}")
        tests_run += 3

    # Perturbed Fano plane: replace block (0, 1, 3) with (0, 1, 4)
    # This destroys the Steiner triple system property (pair (0, 1) appears twice, (0, 3) missing).
    perturbed_blocks = [
        (0, 1, 4),
        (1, 2, 4),
        (2, 3, 5),
        (3, 4, 6),
        (4, 5, 0),
        (5, 6, 1),
        (6, 0, 2),
    ]
    perturbed_insts = frozenset(
        (0, perm) for b in perturbed_blocks for perm in permutations(b)
    )
    r_fano_perturbed = Regime(
        tuple(f"p{i}" for i in range(7)),
        (3,),
        perturbed_insts,
        frozenset(),
        frozenset(),
    )
    can_pert = canonical(r_fano_perturbed)
    brute_pert = canonical_bruteforce(r_fano_perturbed)

    if can_pert == can_fano:
        failures.append("Suite 3: Perturbed Fano falsely has same canonical key as Fano!")
    if brute_pert == brute_fano:
        failures.append("Suite 3: Perturbed Fano falsely has same brute key as Fano!")
    # Check partition agreement
    if (can_pert == can_fano) != (brute_pert == brute_fano):
        failures.append("Suite 3: Discrepancy between can and brute on perturbed Fano!")
    tests_run += 3

    # Oriented Fano plane: only the 3 cyclic permutations per block (21 triples)
    # Blocks are oriented: (i, i+1, i+3)
    oriented_insts = frozenset(
        (0, (b[k % 3], b[(k + 1) % 3], b[(k + 2) % 3]))
        for b in fano_blocks
        for k in range(3)
    )
    r_fano_oriented = Regime(
        tuple(f"p{i}" for i in range(7)),
        (3,),
        oriented_insts,
        frozenset(),
        frozenset(),
    )
    autos_oriented = automorphisms(r_fano_oriented)
    # Oriented Fano plane has order 21 automorphism group (Frobenius group F_21 = C_7 : C_3)
    print(f"    Fano oriented automorphisms count: {len(autos_oriented)} (expected 21)")
    if len(autos_oriented) != 21:
        failures.append(f"Suite 3: Oriented Fano Aut expected 21, got {len(autos_oriented)}")
    tests_run += 1

    can_or = canonical(r_fano_oriented)
    brute_or = canonical_bruteforce(r_fano_oriented)
    for _ in range(5):
        pi = tuple(rng.sample(range(7), 7))
        rp = rename(r_fano_oriented, pi, (0,))
        if canonical(rp) != can_or:
            failures.append("Suite 3: Oriented Fano rename can mismatch")
        if canonical_bruteforce(rp) != brute_or:
            failures.append("Suite 3: Oriented Fano rename brute mismatch")
        tests_run += 2

    print(f"  Passed Suite 3 ({tests_run - s3_start} assertions, {len(failures)} failures).")

    # -------------------------------------------------------------------------
    # SUITE 4: High Automorphism Counts & Arity >= 4
    # -------------------------------------------------------------------------
    print("\n[Suite 4] High Automorphism Counts & Arity >= 4...")
    s4_start = tests_run
    # Complete 3-uniform hypergraph on n=4: C(4, 3) = 4 triples
    insts_k4 = frozenset(
        (0, perm) for c in combinations(range(4), 3) for perm in permutations(c)
    )
    r_k4 = Regime(tuple(f"d{i}" for i in range(4)), (3,), insts_k4, frozenset(), frozenset())
    can_k4 = canonical(r_k4)
    brute_k4 = canonical_bruteforce(r_k4)
    autos_k4 = automorphisms(r_k4)
    if len(autos_k4) != 24:
        failures.append(f"Suite 4: K_4^3 Aut expected 24, got {len(autos_k4)}")
    tests_run += 1
    for pi in permutations(range(4)):
        rp = rename(r_k4, pi, (0,))
        if canonical(rp) != can_k4:
            failures.append("Suite 4: K_4^3 rename can mismatch")
        if canonical_bruteforce(rp) != brute_k4:
            failures.append("Suite 4: K_4^3 rename brute mismatch")
        tests_run += 2

    # Complete 3-uniform hypergraph on n=5: C(5, 3) = 10 triples
    insts_k5 = frozenset(
        (0, perm) for c in combinations(range(5), 3) for perm in permutations(c)
    )
    r_k5 = Regime(tuple(f"d{i}" for i in range(5)), (3,), insts_k5, frozenset(), frozenset())
    can_k5 = canonical(r_k5)
    brute_k5 = canonical_bruteforce(r_k5)
    autos_k5 = automorphisms(r_k5)
    if len(autos_k5) != 120:
        failures.append(f"Suite 4: K_5^3 Aut expected 120, got {len(autos_k5)}")
    tests_run += 1
    for _ in range(10):
        pi = tuple(rng.sample(range(5), 5))
        rp = rename(r_k5, pi, (0,))
        if canonical(rp) != can_k5:
            failures.append("Suite 4: K_5^3 rename can mismatch")
        if canonical_bruteforce(rp) != brute_k5:
            failures.append("Suite 4: K_5^3 rename brute mismatch")
        tests_run += 2

    # Quaternary relation (arity 4) on n=5:
    # Hyper-edges of size 4: C(5, 4) = 5 edges
    insts_q5 = frozenset(
        (0, perm) for c in combinations(range(5), 4) for perm in permutations(c)
    )
    r_q5 = Regime(tuple(f"d{i}" for i in range(5)), (4,), insts_q5, frozenset(), frozenset())
    can_q5 = canonical(r_q5)
    brute_q5 = canonical_bruteforce(r_q5)
    autos_q5 = automorphisms(r_q5)
    if len(autos_q5) != 120:
        failures.append(f"Suite 4: Q_5^4 Aut expected 120, got {len(autos_q5)}")
    tests_run += 1
    for _ in range(10):
        pi = tuple(rng.sample(range(5), 5))
        rp = rename(r_q5, pi, (0,))
        if canonical(rp) != can_q5:
            failures.append("Suite 4: Q_5^4 rename can mismatch")
        if canonical_bruteforce(rp) != brute_q5:
            failures.append("Suite 4: Q_5^4 rename brute mismatch")
        tests_run += 2

    # Multi-form ternary + quaternary regime:
    # form 0: arity 3, form 1: arity 4
    insts_multi = frozenset([
        (0, (0, 1, 2)),
        (0, (1, 2, 3)),
        (1, (0, 1, 2, 3)),
    ])
    r_multi = Regime(
        ("d0", "d1", "d2", "d3"),
        (3, 4),
        insts_multi,
        frozenset([0]),
        frozenset([(0, 1)]),
    )
    can_multi = canonical(r_multi)
    brute_multi = canonical_bruteforce(r_multi)
    for pi in permutations(range(4)):
        rp = rename(r_multi, pi, (0, 1))
        if canonical(rp) != can_multi:
            failures.append("Suite 4: Multi-form rename can mismatch")
        if canonical_bruteforce(rp) != brute_multi:
            failures.append("Suite 4: Multi-form rename brute mismatch")
        tests_run += 2

    print(f"  Passed Suite 4 ({tests_run - s4_start} assertions, {len(failures)} failures).")

    # -------------------------------------------------------------------------
    # SUITE 5: Cross-Regime Partition Agreement Matrix (All-Pairs Falsification Hunt)
    # -------------------------------------------------------------------------
    print("\n[Suite 5] Full Pairwise Partition Equivalence Matrix...")
    s5_start = tests_run
    # Build a collection of diverse adversarial regimes
    adversarial_regimes: list[tuple[str, Regime]] = [
        ("empty", r_empty),
        ("data_only_1", Regime(("a",), (3,), frozenset(), frozenset(), frozenset())),
        ("data_only_2", Regime(("a", "b"), (3,), frozenset(), frozenset(), frozenset())),
        ("data_only_3", Regime(("a", "b", "c"), (3,), frozenset(), frozenset(), frozenset())),
        ("diag", r_diag),
        ("mixed_deg", r_mixed_deg),
        ("even", r_even),
        ("odd", r_odd),  # isomorphic to even!
        ("even_req", r_even_req),
        ("odd_req", r_odd_req),  # isomorphic to even_req!
        ("linear", r_linear),
        ("c5", r_c5),
        ("fano_full", r_fano_full),
        ("fano_pert", r_fano_perturbed),
        ("fano_or", r_fano_oriented),
        ("k4", r_k4),
        ("k5", r_k5),
        ("q5", r_q5),
        ("multi", r_multi),
    ]

    # Add 2 random renamings for each regime
    expanded_regimes: list[tuple[str, Regime]] = []
    for tag, r in adversarial_regimes:
        expanded_regimes.append((tag, r))
        n = r.n_data()
        nf = len(r.forms)
        for rep in range(2):
            pi = tuple(rng.sample(range(n), n)) if n > 0 else ()
            # For phi, keep forms arity preserved
            phi = tuple(range(nf))
            rp = rename(r, pi, phi)
            expanded_regimes.append((f"{tag}_rename{rep}", rp))

    print(f"    Evaluating all pairs among {len(expanded_regimes)} regimes ({len(expanded_regimes)**2} pairs)...")
    keys_can = [canonical(r) for _, r in expanded_regimes]
    keys_brute = [canonical_bruteforce(r) for _, r in expanded_regimes]

    falsifier_pairs = []
    for i in range(len(expanded_regimes)):
        for j in range(i, len(expanded_regimes)):
            can_eq = (keys_can[i] == keys_can[j])
            brute_eq = (keys_brute[i] == keys_brute[j])
            tests_run += 1
            if can_eq != brute_eq:
                falsifier_pairs.append({
                    "i": expanded_regimes[i][0],
                    "j": expanded_regimes[j][0],
                    "can_eq": can_eq,
                    "brute_eq": brute_eq,
                })

    if falsifier_pairs:
        failures.append(f"Suite 5: Found {len(falsifier_pairs)} partition discrepancies!")
        for fp in falsifier_pairs[:5]:
            print(f"      DISCREPANCY: {fp}")
    else:
        print(f"    Zero discrepancies across all {len(expanded_regimes)**2} pair comparisons!")

    print(f"  Passed Suite 5 ({tests_run - s5_start} assertions, {len(failures)} failures).")

    # -------------------------------------------------------------------------
    # SUMMARY AND VERDICT
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print(f"TOTAL ADVERSARIAL ASSERTIONS: {tests_run:,}")
    print(f"TOTAL FAILURES:               {len(failures)}")
    print(f"FINAL ADVERSARIAL VERDICT:    {'APPROVE' if len(failures) == 0 else 'REJECT'}")
    print("=" * 70)

    return {
        "tests_run": tests_run,
        "failures": failures,
        "verdict": "APPROVE" if len(failures) == 0 else "REJECT",
    }


if __name__ == "__main__":
    result = run_adversarial_suite()
    if result["verdict"] != "APPROVE":
        sys.exit(1)
    sys.exit(0)
