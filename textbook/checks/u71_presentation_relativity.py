"""Unit 71 check: presentation-relative identity, directional residuals,
comparison-forced refinement, internal symmetry breaks, and current residual
closure.

Checks Genesis's completion inventory bindings and axiom reports for
`PresentationRelativity` (32 theorems), `ClosureSymmetry` (7 theorems), and
`ResidualClosure` (7 theorems), and runs Python (book) finite checks:
  - exact equivalence of mutual factorization, fiber identity, and empty
    directional residuals across all 729 pairs of maps on D = [0, 1, 2];
  - forced split and strict class-count growth for every factorization failure
    on D = [0, 1, 2], plus vacuity on D = [];
  - panel extension fixture and the declared generator witness at n = 3, 4, 5
    under the supplied comparison id;
  - equivalence with InternalSymmetryBreak, transposition construction, and a
    double-swap witness on D = [0, 1, 2, 3] showing InternalSymmetryBreak is
    wider than single transpositions;
  - ResidualClosure's five-conjunct closure of the current obstruction r -> q
    together with a subsequent comparison q' that opens a new residual.

AuthorityEffect: None.
Run from the repository root:
    python textbook/checks/u71_presentation_relativity.py
"""
from __future__ import annotations

from itertools import product
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.completion import KIND_ROLE_OVERRIDES  # noqa: E402

Map = Callable[[int], int]


def fiber_constant(d_list: list[int], p: Map, q: Map) -> bool:
    return all(
        q(x) == q(y)
        for x in d_list
        for y in d_list
        if p(x) == p(y)
    )


def factors_on(d_list: list[int], p: Map, q: Map) -> bool:
    # By Compression.factors_iff_fiberConstant, existence of g : Nat -> Nat
    # with g(p(x)) = q(x) on D is equivalent to fiber_constant(D, p, q).
    return fiber_constant(d_list, p, q)


def fiber_identity_on(d_list: list[int], p: Map, q: Map) -> bool:
    return all(
        (p(x) == p(y)) == (q(x) == q(y))
        for x in d_list
        for y in d_list
    )


def presentation_identity_on(d_list: list[int], p: Map, q: Map) -> bool:
    return factors_on(d_list, p, q) and factors_on(d_list, q, p)


def directional_residuals(d_list: list[int], p: Map, q: Map) -> list[tuple[int, int]]:
    return [
        (x, y)
        for x in d_list
        for y in d_list
        if p(x) == p(y) and q(x) != q(y)
    ]


def residual_empty_on(d_list: list[int], p: Map, q: Map) -> bool:
    return not directional_residuals(d_list, p, q) and not directional_residuals(d_list, q, p)


def sig_list(q_family: list[Map], x: int) -> tuple[int, ...]:
    return tuple(q(x) for q in q_family)


def p_q(d_list: list[int], q_family: list[Map]) -> Map:
    def fn(x: int) -> int:
        sx = sig_list(q_family, x)
        for a in d_list:
            if sig_list(q_family, a) == sx:
                return a
        return 0
    return fn


def class_count(d_list: list[int], q_family: list[Map]) -> int:
    seen: list[tuple[int, ...]] = []
    for x in d_list:
        s = sig_list(q_family, x)
        if s not in seen:
            seen.append(s)
    return len(seen)


def joint_presentation(d_list: list[int], p: Map, q: Map) -> Map:
    return p_q(d_list, [p, q])


def transpose(a: int, b: int) -> Map:
    def fn(x: int) -> int:
        if x == a:
            return b
        if x == b:
            return a
        return x
    return fn


def is_internal_symmetry_break(
    d_list: list[int], p: Map, q: Map, sym: Map, point: int
) -> bool:
    involutive = all(sym(sym(x)) == x for x in range(max(d_list, default=0) + 3))
    domain_ok = all(sym(x) in d_list for x in d_list)
    p_inv = all(p(sym(x)) == p(x) for x in d_list)
    pt_ok = point in d_list and q(sym(point)) != q(point)
    return involutive and domain_ok and p_inv and pt_ok


def invariant_under_on(d_list: list[int], f: Map, sigma: Map) -> bool:
    return all(f(sigma(x)) == f(x) for x in d_list)


def depth_one_presentation(n: int) -> Map:
    # Mirrors PresentationRelativity.depthOnePresentation (reflState n):
    # At reflState n (n >= 3), endpoint 0 has (true, true, false) -> 6,
    # interior points 1..n-1 have (true, true, true) -> 7,
    # endpoint n has (true, false, true) -> 5.
    def fn(i: int) -> int:
        if i == 0:
            return 6
        if 1 <= i < n:
            return 7
        if i == n:
            return 5
        return 4
    return fn


def main() -> int:
    failures: list[str] = []

    # 1. Check completion.py bindings and artifacts/lean_axioms.txt coverage
    ax_text = (ROOT / "artifacts" / "lean_axioms.txt").read_text(encoding="utf-8")
    mod_counts = {
        "PresentationRelativity.": 32,
        "ClosureSymmetry.": 7,
        "ResidualClosure.": 7,
    }
    for prefix, expected_count in mod_counts.items():
        bound = [k for k in KIND_ROLE_OVERRIDES if k.startswith(prefix)]
        in_ax = [
            line for line in ax_text.splitlines()
            if f"'{prefix}" in line
        ]
        print(f"{prefix[:-1]}: bound in completion.py = {len(bound)}, "
              f"in lean_axioms.txt = {len(in_ax)}")
        if len(bound) != expected_count or len(in_ax) != expected_count:
            failures.append(f"inventory_{prefix[:-1]}")

    # 2. Exhaustive check on D = [0, 1, 2] (27 maps, 729 pairs)
    d3 = [0, 1, 2]
    all_maps: list[Map] = [
        (lambda tbl=tbl: lambda x: tbl[x] if 0 <= x < len(tbl) else 0)()
        for tbl in product(d3, repeat=3)
    ]
    equiv_ok = True
    split_ok = True
    sym_ok = True
    closure_ok = True
    failed_pairs = 0

    for p in all_maps:
        for q in all_maps:
            pid = presentation_identity_on(d3, p, q)
            fid = fiber_identity_on(d3, p, q)
            remp = residual_empty_on(d3, p, q)
            if not (pid == fid == remp):
                equiv_ok = False

            res = directional_residuals(d3, p, q)
            fac = factors_on(d3, p, q)
            if fac != (len(res) == 0):
                sym_ok = False

            if not fac:
                failed_pairs += 1
                x0, y0 = res[0]
                # Every common refinement r must split (x0, y0) and grow classCount
                for r in all_maps:
                    if factors_on(d3, r, p) and factors_on(d3, r, q):
                        if r(x0) == r(y0) or not (
                            class_count(d3, [p]) < class_count(d3, [r])
                        ):
                            split_ok = False
                # Joint presentation must factor both and grow classCount
                jp = joint_presentation(d3, p, q)
                if not (
                    factors_on(d3, jp, p)
                    and factors_on(d3, jp, q)
                    and class_count(d3, [p]) < class_count(d3, [jp])
                ):
                    split_ok = False
                # Transposition from residual is a valid InternalSymmetryBreak
                sym = transpose(x0, y0)
                if not is_internal_symmetry_break(d3, p, q, sym, x0):
                    sym_ok = False
                # ResidualClosure on jp: loses sym invariance, splits pair,
                # grows count, and has empty residual r -> q
                if not (
                    not invariant_under_on(d3, jp, sym)
                    and jp(sym(x0)) != jp(x0)
                    and class_count(d3, [p]) < class_count(d3, [jp])
                    and len(directional_residuals(d3, jp, q)) == 0
                ):
                    closure_ok = False

    print(f"D = [0, 1, 2]: {len(all_maps)} maps, {len(all_maps)**2} pairs, "
          f"{failed_pairs} factorization failures; "
          f"equivalences={equiv_ok}, forced_split={split_ok}, "
          f"symmetry_break={sym_ok}, residual_closure={closure_ok}")
    if not (equiv_ok and split_ok and sym_ok and closure_ok):
        failures.append("d3_exhaustive")

    # 3. Vacuity on D = [] and double-swap non-transposition witness on D = [0, 1, 2, 3]
    vacuous_empty = all(factors_on([], p, q) for p in all_maps[:5] for q in all_maps[:5])
    d4 = [0, 1, 2, 3]
    p_coarse: Map = lambda x: 0
    q_fine: Map = lambda x: x
    double_swap: Map = lambda x: {0: 1, 1: 0, 2: 3, 3: 2}.get(x, x)
    moved_points = [x for x in d4 if double_swap(x) != x]
    double_swap_valid = is_internal_symmetry_break(d4, p_coarse, q_fine, double_swap, 0)
    print(f"Python (book): FactorsOn [] vacuous={vacuous_empty}; "
          f"double-swap on D=[0,1,2,3] moves {len(moved_points)} points "
          f"(not a single transposition) and is InternalSymmetryBreak={double_swap_valid}")
    if not (vacuous_empty and len(moved_points) == 4 and double_swap_valid):
        failures.append("vacuity_and_double_swap")

    # 4. Generator instance at n = 3, 4, 5 (with supplied id)
    gen_ok = True
    for n in (3, 4, 5):
        dom = list(range(n + 1))
        dp = depth_one_presentation(n)
        id_map: Map = lambda x: x
        res_n = directional_residuals(dom, dp, id_map)
        jp_n = joint_presentation(dom, dp, id_map)
        if not (
            (1, 2) in res_n
            and not factors_on(dom, dp, id_map)
            and class_count(dom, [dp]) == 3
            and class_count(dom, [jp_n]) == n + 1
        ):
            gen_ok = False
    print(f"generator depth-one profile vs supplied id on n=3,4,5: {gen_ok}")
    if not gen_ok:
        failures.append("generator_instance")

    # 5. Closing current obstruction r -> q does not close future comparison r -> q'
    p0: Map = lambda x: 0
    q_half: Map = lambda x: x // 2
    r_curr: Map = q_half
    q_next: Map = lambda x: x
    curr_closed = len(directional_residuals(d3, r_curr, q_half)) == 0
    next_open = directional_residuals(d3, r_curr, q_next) == [(0, 1), (1, 0)]
    print(f"Python (book): r -> q closed ({curr_closed}) while r -> q' has "
          f"residuals {directional_residuals(d3, r_curr, q_next)} ({next_open})")
    if not (curr_closed and next_open):
        failures.append("current_vs_future")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
