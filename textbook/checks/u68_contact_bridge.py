"""Unit 68 check: the observer zero-complement, the apartness round trip,
the representability countermodels, and the declared-column anchor (`DiffAnchor`).

Runs Genesis's `enum_bool_observers` (E1) and `enum_settings_kernels` (E2) from
`code/run_primitive_contact.py` and `insufficiency_countermodels` from
`code/derivation/apartness.py`, compares them with `artifacts/primitive_contact.json`,
and adds Python (book) checks for `bool_bs_repr` (carrier-2 Bs representability),
the four representability countermodels, and `colView`/`zeroP` with `DiffAnchor`'s
`DeltaConstant`.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u68_contact_bridge.py
"""
from __future__ import annotations

import json
import sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

import run_primitive_contact as RPC  # noqa: E402
from derivation.apartness import (  # noqa: E402
    all_relations,
    indist_is_equivalence,
    insufficiency_countermodels,
    is_irrefl,
    is_symm,
)


def col_view(cols: list[list[int]], i: int) -> tuple[bool, ...]:
    return tuple(i in c for c in cols)


def zero_p(cols: list[list[int]], i: int, j: int) -> bool:
    return all((i in c) == (j in c) for c in cols)


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "primitive_contact.json").read_text(encoding="utf-8"))

    # E1 and E2 from Genesis's contact runner
    e1 = RPC.enum_bool_observers()
    e2 = RPC.enum_settings_kernels()
    print(f"E1 Bool observers: {e1}; matches artifact: "
          f"{e1 == art['enumerations']['E1_bool_observers']}")
    print(f"E2 settings/kernels & Bell counts: {e2}; matches artifact: "
          f"{e2 == art['enumerations']['E2_settings_kernels']}")
    if e1 != art["enumerations"]["E1_bool_observers"] or e1["oriented_complement_observers"] != 0:
        failures.append("E1")
    if e2 != art["enumerations"]["E2_settings_kernels"] or e2["representable_relation_counts"] != [1, 2, 5]:
        failures.append("E2")

    # Apartness countermodels (carriers 1, 2, 3) and minimality of carrier 3 for Bs
    cms = insufficiency_countermodels()
    print(f"apartness insufficiency countermodels: {cms}")
    if not all(
        cms[k] for k in (
            "bare_breaks_refl",
            "irrefl_alone_breaks_symm",
            "symm_without_cotrans_breaks_trans",
            "two_point_countermodel_minimal",
            "three_point_countermodel_minimal",
        )
    ):
        failures.append("countermodels")

    # Python (book): bool_bs_repr — every witnessed irreflexive symmetric relation on
    # 2 points has an equivalence complement (1 relation: {(0, 1), (1, 0)})
    bs2 = [r for r in all_relations(2) if is_irrefl(2, r) and is_symm(2, r) and (0, 1) in r]
    bs2_repr = all(indist_is_equivalence(2, r) for r in bs2)
    # On 3 points, triSymRel = {(0, 1), (1, 0)} is witnessed, irreflexive, symmetric,
    # but its complement is NOT an equivalence (0 ~ 2 and 2 ~ 1 but not 0 ~ 1)
    tri_sym = frozenset({(0, 1), (1, 0)})
    tri_not_repr = (
        is_irrefl(3, tri_sym)
        and is_symm(3, tri_sym)
        and (0, 1) in tri_sym
        and not indist_is_equivalence(3, tri_sym)
    )
    print(f"Python (book) bool_bs_repr: {len(bs2)} witnessed Bs relation on n=2, "
          f"representable {bs2_repr}; triSymRel on n=3 breaks complement transitivity {tri_not_repr}")
    if len(bs2) != 1 or not bs2_repr or not tri_not_repr:
        failures.append("bool_bs_repr")

    # Scope verification: two non-interchangeable decidability admissions
    terminals = {t["code"]: t["scope"] for t in art["verdict"]["terminals"]}
    eq_scope = terminals["CONTACT_EQUIVALENT_UNDER_DECIDABLE_ZERO_PLUS_APARTNESS_ADMISSIONS"]
    inc_scope = terminals["CONTACT_INCOMPARABLE_WITH_COUNTERMODELS"]
    scope_ok = (
        "NOT interchangeable" in eq_scope
        and "ASSERTED APARTNESS relation" in eq_scope
        and "ZERO relation" in eq_scope
        and "bool_bs_repr" in inc_scope
    )
    print(f"scope records two non-interchangeable decidability admissions and bool_bs_repr: {scope_ok}")
    if not scope_ok:
        failures.append("scope")

    # Python (book): declared_zero_as_view and DiffAnchor (colObs_quotient_eq_iff_zeroP, colObs_deltaConstant)
    col_families = [[], [[0]], [[0, 1]], [[0], [1, 2]], [[0, 2], [1, 2]]]
    pts = [0, 1, 2, 3]
    anchor_ok = True
    for cols in col_families:
        # zeroP agrees with colView equality on all pairs
        for i, j in product(pts, repeat=2):
            if zero_p(cols, i, j) != (col_view(cols, i) == col_view(cols, j)):
                anchor_ok = False
        # DeltaConstant for colObs(cols): ZeroRel(x, x') and ZeroRel(y, y') -> delta(x, y) == delta(x', y')
        for x, xp, y, yp in product(pts, repeat=4):
            if zero_p(cols, x, xp) and zero_p(cols, y, yp):
                if (col_view(cols, x), col_view(cols, y)) != (col_view(cols, xp), col_view(cols, yp)):
                    anchor_ok = False
    empty_merges = zero_p([], 0, 1)
    single_separates = not zero_p([[0]], 0, 1)
    print(f"Python (book) declared_zero_as_view & DiffAnchor over {len(col_families)} column families: "
          f"{anchor_ok}; cols=[] merges (0,1) {empty_merges}; cols=[[0]] separates (0,1) {single_separates}")
    if not (anchor_ok and empty_merges and single_separates):
        failures.append("diff_anchor")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
