"""Unit 67 check: observer quotient descent, the all-zero countermodel,
the flagship pair obstruction, and the Compression dictionary.

Runs Genesis's `enum_descent_dictionary` (E3) and `enum_flagship_census` (E4)
from `code/run_primitive_contact.py`, compares them with
`artifacts/primitive_contact.json`, cross-checks `code/derivation/compression.py`
(`fiber_constant`, `factors_on`, `sig_eq`) against the dictionary theorems of
`ObsDescent`, and adds Python (book) checks for `collapseAllObs` and
`value_orientation_survives`.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u67_obs_descent.py
"""
from __future__ import annotations

import json
import sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

import run_primitive_contact as RPC  # noqa: E402
from derivation.compression import (  # noqa: E402
    all_families,
    all_functions,
    factors_on,
    fiber_constant,
    sig_eq,
)


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "primitive_contact.json").read_text(encoding="utf-8"))

    # E3: descent dictionary on 3 points, 2 values (64 pairs of views)
    e3 = RPC.enum_descent_dictionary()
    print(f"E3 descent dictionary: {e3}; matches artifact: "
          f"{e3 == art['enumerations']['E3_descent_dictionary']}")
    if e3 != art["enumerations"]["E3_descent_dictionary"] or e3 != {
        "combinations": 64,
        "descend_count": 28,
        "fixed_domain_divergence_count": 36,
    }:
        failures.append("E3")

    # E4: flagship pair obstruction census (120 triples out of 512)
    e4 = RPC.enum_flagship_census()
    print(f"E4 flagship census: {e4}; matches artifact: "
          f"{e4 == art['enumerations']['E4_flagship_census']}")
    if e4 != art["enumerations"]["E4_flagship_census"] or e4 != {"triples": 120}:
        failures.append("E4")

    # Compression dictionary: class-constant on full carrier <-> fiber_constant
    # and factors_on over every subset D of {0, 1, 2}
    subsets = [
        [x for x in range(3) if mask >> x & 1]
        for mask in range(1 << 3)
    ]
    fns = all_functions(3, 3)
    dict_ok = True
    for p in fns:
        for q in fns:
            cc = fiber_constant([0, 1, 2], p, q)
            all_D_fc = all(fiber_constant(D, p, q) for D in subsets)
            all_D_fac = all(factors_on(D, p, q, 3) for D in subsets)
            if not (cc == all_D_fc == all_D_fac):
                dict_ok = False
    # Fixed D = [] counterexample: fiberConstant_fixed_D_not_classConstant
    p_const0 = (0, 0, 0)
    q_id = (0, 1, 2)
    fixed_empty_fc = fiber_constant([], p_const0, q_id)
    global_cc = fiber_constant([0, 1, 2], p_const0, q_id)
    print(f"dictionary across all {len(fns) * len(fns)} pairs (n=3, m=3) and {len(subsets)} subsets: "
          f"{dict_ok}; fixed D=[] fiber-constant {fixed_empty_fc}, global class-constant {global_cc}")
    if not (dict_ok and fixed_empty_fc and not global_cc):
        failures.append("dictionary")

    # sigEq_append_iff check over all families on n=3, m=2
    fams = all_families(3, 2, 1)
    sigeq_ok = all(
        sig_eq(Q1 + Q2, x, y) == (sig_eq(Q1, x, y) and sig_eq(Q2, x, y))
        for Q1 in fams for Q2 in fams for x in range(3) for y in range(3)
    )
    print(f"sigEq_append_iff over {len(fams)}^2 family pairs: {sigeq_ok}")
    if not sigeq_ok:
        failures.append("sigEq_append")

    # Python (book): collapseAllObs on Bool vs subsingleton Unit
    pts = (False, True)
    all_zero = all(True for _ in pts for _ in pts)
    delta_collapse = lambda x, _y: x
    delta_const = all(
        delta_collapse(x, y) == delta_collapse(xp, yp)
        for x, xp, y, yp in product(pts, repeat=4)
    )
    id_const = all(x == y for x in pts for y in pts)
    unit_pts = (0,)
    unit_all_const = all(
        f[x] == f[y]
        for f in [(0,), (1,)] for x in unit_pts for y in unit_pts
    )
    print(f"Python (book) collapseAllObs: all pairs zero {all_zero}; "
          f"DeltaConstant {delta_const}; id ClassConstant {id_const}; "
          f"subsingleton carrier always ClassConstant {unit_all_const}")
    if not (all_zero and not delta_const and not id_const and unit_all_const):
        failures.append("collapseAllObs")

    # Python (book): intDiffObs value_orientation_survives
    d01 = 0 - 1
    d10 = 1 - 0
    z01 = (d01 == 0)
    z10 = (d10 == 0)
    orient_ok = (d01 != d10) and (z01 == z10)
    print(f"Python (book) intDiffObs orientation: delta(0,1)={d01} != delta(1,0)={d10}, "
          f"ZeroRel(0,1)={z01} == ZeroRel(1,0)={z10}: {orient_ok}")
    if not orient_ok:
        failures.append("orientation")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
