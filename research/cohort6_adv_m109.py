"""M109 adversarial checks for Cohort 6."""
from __future__ import annotations

from fractions import Fraction
import math
from pathlib import Path
import random
import subprocess
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET_DIRS = [
    REPO_ROOT / "research" / "p203_composite_systems",
    REPO_ROOT / "research" / "m108_internal_algebra",
    REPO_ROOT / "research" / "m109_obstruction_homology",
    REPO_ROOT / "research" / "x300_observer_information",
]
for p in reversed(TARGET_DIRS):
    p_str = str(p)
    if p_str in sys.path:
        sys.path.remove(p_str)
    sys.path.insert(0, p_str)

import composite_systems as p203
import algebra as m108
import homology as m109
import information as x300

def test_m109_adversarial_obstruction_homology() -> int:
    """Fuzz M109 chain complexes, boundary nilpotency, Stokes theorem, and Target 7 obstruction."""
    print(">>> Fuzzing Target M109: Higher Chain Complexes & Obstruction Homology...")
    checks = 0
    rng = random.Random(109109)

    # 1. Graded chain complexes: cycle complexes C_n sweeps
    for n in (3, 4, 5, 6, 8, 10):
        cn = m109.build_cycle_complex(n)
        assert cn.max_grade == 1
        assert cn.dimensions[0] == n
        assert cn.dimensions[1] == n

        # Nilpotency at all grades
        nil = cn.verify_nilpotency()
        assert nil == {}  # No intermediate 2-cells, boundary is trivially nilpotent
        checks += 1

        # Homology: 1 connected component, 1 1-cycle
        h = cn.compute_all_homology()
        assert h[0].betti_number == 1
        assert h[1].betti_number == 1
        assert cn.euler_characteristic() == 0
        checks += 3

        # Dual cochain complex & coboundary nilpotency
        dcn = cn.dual_cochain_complex()
        ch = dcn.compute_all_cohomology()
        assert ch[0].betti_number == 1
        assert ch[1].betti_number == 1
        checks += 2

    # 2. Torus complex T_{m,n} sweeps: \partial_1 \circ \partial_2 = 0 & Betti (1, 2, 1)
    for m, n in [(2, 2), (2, 3), (3, 3)]:
        torus = m109.build_torus_complex(m, n)
        nil = torus.verify_nilpotency()
        assert nil[1] is True  # \partial_1 \circ \partial_2 = 0
        checks += 1

        dtorus = torus.dual_cochain_complex()
        cobound_nil = dtorus.verify_coboundary_nilpotency()
        assert cobound_nil[0] is True  # \delta^1 \circ \delta^0 = 0
        checks += 1

        # Homology betti numbers: \beta_0 = 1, \beta_1 = 2, \beta_2 = 1
        h_torus = torus.compute_all_homology()
        assert h_torus[0].betti_number == 1
        assert h_torus[1].betti_number == 2
        assert h_torus[2].betti_number == 1
        assert torus.euler_characteristic() == 0
        checks += 4

        # Duality isomorphism over Q: dim H_k = dim H^k
        ch_torus = dtorus.compute_all_cohomology()
        for k in range(3):
            assert h_torus[k].betti_number == ch_torus[k].betti_number
        checks += 3

        # Discrete Stokes-Cartan theorem verification: <\delta \omega, c> = <\omega, \partial c>
        for _ in range(5):
            omega_1 = [Fraction(rng.randint(-10, 10), rng.randint(1, 5)) for _ in range(torus.dimensions[1])]
            c_2 = [Fraction(rng.randint(-10, 10), rng.randint(1, 5)) for _ in range(torus.dimensions[2])]
            assert dtorus.verify_stokes_theorem(1, omega_1, c_2) is True
            checks += 1

    # 3. Cubical cavity S^2 vs solid cube D^3
    s2 = m109.build_cubical_cavity_complex(include_3cell=False)
    assert s2.euler_characteristic() == 2  # \chi(S^2) = 2
    h_s2 = s2.compute_all_homology()
    assert h_s2[0].betti_number == 1
    assert h_s2[1].betti_number == 0
    assert h_s2[2].betti_number == 1  # 2-cavity cycle
    checks += 4

    cube = m109.build_cubical_cavity_complex(include_3cell=True)
    assert cube.euler_characteristic() == 1  # \chi(D^3) = 1
    h_cube = cube.compute_all_homology()
    assert h_cube[0].betti_number == 1
    assert h_cube[1].betti_number == 0
    assert h_cube[2].betti_number == 0  # 2-cavity cycle filled by 3-cell
    assert h_cube[3].betti_number == 0
    checks += 5

    # 4. Target 7 Relational Move Complex audit
    c7 = m109.build_target7_complex(pure_only=True)
    assert c7.dimensions[0] == 262
    assert c7.dimensions[1] == 638
    assert c7.dimensions[2] == 146
    checks += 3

    nil_c7 = c7.verify_nilpotency()
    assert nil_c7[1] is True  # \partial_1 \circ \partial_2 = 0
    checks += 1

    h0_c7 = c7.compute_homology(0)
    h1_c7 = c7.compute_homology(1)
    h2_c7 = c7.compute_homology(2)
    assert h0_c7.betti_number == 2
    assert h1_c7.betti_number == 232  # 378 cycles - 146 square boundaries = 232
    assert h2_c7.betti_number == 0
    checks += 3

    # Native candidate cost functions on Target 7 pure complex
    reports = m109.evaluate_target7_native_candidates(c7)
    assert len(reports) == 4
    for name in ("rule_span", "width_at_admission", "empty_admission", "mention_deficit"):
        assert name in reports
        # In 2-complex, these cost functions have non-zero coboundary on pure squares
        assert reports[name].is_cocycle is False
        checks += 2

    print(f"  M109 passed {checks} adversarial checks.")
    return checks


# ==============================================================================
# 4. Target X300: Observer-Relative Information, Channels & Loss Fuzzing
# ==============================================================================

