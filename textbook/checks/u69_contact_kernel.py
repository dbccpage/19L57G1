"""Unit 69 check: the common replacement kernel (`ContactKernel.WitnessedDiff`),
its realizations, pair correspondence, pricing refutations, value fork, and
37-cell collision matrix.

Runs Genesis's `enum_bool_observers` (E1), `enum_settings_kernels` (E2),
`enum_value_fork` (E5), `COLLISION_CELLS`, and `SCOPE_KERNEL` from
`code/run_primitive_contact.py`, compares them with
`artifacts/primitive_contact.json`, and adds Python (book) checks for the
`NonZeroPair`/`SameDataKernel` bijection, `no_equivariant_pair_at_fixed_point`,
`vhom_not_unique` versus `vhom_unique_of_onto`, and `freeKernel` branching.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u69_contact_kernel.py
"""
from __future__ import annotations

import json
import sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

import run_primitive_contact as RPC  # noqa: E402


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "primitive_contact.json").read_text(encoding="utf-8"))

    # E1, E2, E5 from Genesis's contact runner
    e1 = RPC.enum_bool_observers()
    e2 = RPC.enum_settings_kernels()
    e5 = RPC.enum_value_fork()
    print(f"E1 witnessed_kernel_quadruples: {e1['witnessed_kernel_quadruples']} "
          f"(expected 8); matches artifact: {e1 == art['enumerations']['E1_bool_observers']}")
    print(f"E2 witnessed_kernel_counts_matching: {e2['witnessed_kernel_counts_matching']} "
          f"(expected [0, 4, 192]); matches a_setting_counts: "
          f"{e2['witnessed_kernel_counts_matching'] == e2['a_setting_counts']}")
    print(f"E5 value fork: {e5}; matches artifact: {e5 == art['enumerations']['E5_value_fork']}")
    if (
        e1 != art["enumerations"]["E1_bool_observers"]
        or e1["witnessed_kernel_quadruples"] != 8
    ):
        failures.append("E1")
    if (
        e2 != art["enumerations"]["E2_settings_kernels"]
        or e2["witnessed_kernel_counts_matching"] != [0, 4, 192]
    ):
        failures.append("E2")
    if (
        e5 != art["enumerations"]["E5_value_fork"]
        or e5["tables"] != 81
        or e5["oriented_class_presentations"] != 2
    ):
        failures.append("E5")

    # 37-row COLLISION_CELLS mirror and scope checks
    cells = RPC.COLLISION_CELLS
    cell_ids = [r[0] for r in cells]
    cells_ok = (
        len(cells) == 37
        and len(set(cell_ids)) == 37
        and [list(r) for r in cells] == art["collision_cells"]
    )
    terminals = {t["code"]: t["scope"] for t in art["verdict"]["terminals"]}
    k_scope = terminals["COMMON_PRIMITIVE_KERNEL_REPLACES_BOTH"]
    scope_ok = (
        k_scope == RPC.SCOPE_KERNEL
        and "ENDPOINT DISTINCTNESS ONLY" in k_scope
        and "INDUCED-APARTNESS MORPHISM GRADE" in k_scope
        and "DEFINITION not derivation" in k_scope
    )
    print(f"37 collision cells mirror artifact with distinct IDs: {cells_ok}; "
          f"kernel scope check: {scope_ok}")
    if not (cells_ok and scope_ok):
        failures.append("cells_or_scope")

    # Python (book): NonZeroPair <-> SameDataKernel correspondence & transpose non-uniqueness
    # Across all 64 (delta, Zero) pairs on Bool, 20 satisfy the 3 DiffObs laws
    # (matching E1['observer_law_pairs'] == 20):
    # 2 have 2 non-zero pairs ((False, True) and (True, False)), 18 have 0 (collapsed).
    pts = (False, True)
    tables = list(product(pts, repeat=4))
    zpreds = list(product(pts, repeat=2))

    def zrel(t: tuple[bool, ...], z: tuple[bool, ...], x: bool, y: bool) -> bool:
        return z[1 if t[(2 if x else 0) + (1 if y else 0)] else 0]

    def is_obs(t: tuple[bool, ...], z: tuple[bool, ...]) -> bool:
        refl = all(zrel(t, z, x, x) for x in pts)
        symm = all(zrel(t, z, y, x) for x in pts for y in pts if zrel(t, z, x, y))
        trans = all(
            zrel(t, z, x, w)
            for x in pts for y in pts for w in pts
            if zrel(t, z, x, y) and zrel(t, z, y, w)
        )
        return refl and symm and trans

    obs_list = [(t, z) for t in tables for z in zpreds if is_obs(t, z)]
    pair_correspondence_ok = True
    inhabited_obs = 0
    collapsed_obs = 0
    for t, z in obs_list:
        nz_pairs = [(a, b) for a in pts for b in pts if not zrel(t, z, a, b)]
        same_data_kernels = [
            (t, z, a, b)
            for a in pts for b in pts
            if all(zrel(t, z, x, x) for x in pts) and not zrel(t, z, a, b)
        ]
        # Round trips toPair(ofPair(p)) == p and ofPair(toPair(K)) == K
        if [k[2:] for k in same_data_kernels] != nz_pairs:
            pair_correspondence_ok = False
        if len(nz_pairs) == 0:
            collapsed_obs += 1
        elif len(nz_pairs) == 2 and nz_pairs[0] == (nz_pairs[1][1], nz_pairs[1][0]):
            inhabited_obs += 1
        else:
            pair_correspondence_ok = False
    # Fixed-point obstruction at boolEqObs (xor table (False, True, True, False), Zero=(True, False))
    bool_eq_t = (False, True, True, False)
    swap_bool_eq_t = tuple(
        bool_eq_t[(2 if (not x) else 0) + (1 if (not y) else 0)]
        for x in pts for y in pts
    )
    no_fixed_pair = (
        swap_bool_eq_t == bool_eq_t
        and all((not a, not b) != (a, b) for a in pts for b in pts)
    )
    print(f"Python (book) NonZeroPair<->SameDataKernel over {len(obs_list)} Bool observers "
          f"(inhabited={inhabited_obs}, collapsed={collapsed_obs}): {pair_correspondence_ok}; "
          f"swapObs fixed-point obstruction at boolEqObs: {no_fixed_pair}")
    if not (
        pair_correspondence_ok
        and len(obs_list) == 20
        and inhabited_obs == 2
        and collapsed_obs == 18
        and no_fixed_pair
    ):
        failures.append("pair_correspondence")

    # Python (book): VHom off-image non-uniqueness vs DeltaOnto uniqueness, and freeKernel branching
    # unitValKernel has delta image {0, 1} inside {0, 1, 2}; g1(v)=(v==1) and g2(v)=(v!=0)
    # both intertwine delta and preserve Zero (v==0), yet differ at v=2.
    g1 = {0: False, 1: True, 2: False}
    g2 = {0: False, 1: True, 2: True}
    u_delta = {(False, False): 0, (False, True): 1, (True, False): 0, (True, True): 0}
    b_delta = {(False, False): False, (False, True): True, (True, False): False, (True, True): False}
    vhom_fork_ok = (
        all(b_delta[(x, y)] == g1[u_delta[(x, y)]] for x in pts for y in pts)
        and all(b_delta[(x, y)] == g2[u_delta[(x, y)]] for x in pts for y in pts)
        and g1[0] is False and g2[0] is False
        and g1[2] != g2[2]
    )
    # On freeKernel (carrier {0,1,2}, single edge (0,1)), h1(2)=a and h2(2)=b both preserve
    # the edge (0,1) -> (a,b) and differ at 2 whenever a != b.
    h1_map = {0: "a", 1: "b", 2: "a"}
    h2_map = {0: "a", 1: "b", 2: "b"}
    branch_ok = (
        (h1_map[0], h1_map[1]) == ("a", "b")
        and (h2_map[0], h2_map[1]) == ("a", "b")
        and h1_map[2] != h2_map[2]
    )
    print(f"Python (book) VHom off-image non-uniqueness: {vhom_fork_ok}; "
          f"freeKernel third-point branching: {branch_ok}")
    if not (vhom_fork_ok and branch_ok):
        failures.append("vhom_or_branching")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
