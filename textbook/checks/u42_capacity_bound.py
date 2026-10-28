"""Unit 42 check: counting without choosing, and the coloured capacity bound.

Python (book): Genesis has no Python module for Pigeonhole or
CapacityBound. This script rebuilds `encode`, `colourBall` and a local
view from Genesis's definitions (over the ball of Unit 41) and checks:
the counting lemma and the pigeonhole on small instances; `encode` is
injective at fixed length and bounded by k^m; the threshold
k^(2d+1) + 2d + 2 forces a deep collision for every bounded colouring
of small chains; and, below the threshold, a colouring whose local view
separates every deep pair exists (k = 2, d = 0 as in Genesis; k = 2,
d = 1 by exhaustive search, which Genesis does not exhibit).
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u42_capacity_bound.py
"""
from __future__ import annotations

import itertools


def ball(i: int, d: int) -> list[int]:
    return [max(i - d, 0) + k for k in range(2 * d + 1)]


def encode(k: int, l: list[int]) -> int:
    """Lean's `encode k`: [] ↦ 0; x :: t ↦ x + k * encode k t."""
    return 0 if not l else l[0] + k * encode(k, l[1:])


def colour_ball(colour, i: int, d: int) -> list[int]:
    return [colour(x) for x in ball(i, d)]


def deep_points(n: int, d: int) -> list[int]:
    return [i for i in range(n + 1) if d < i and i + d < n]


def threshold(k: int, d: int) -> int:
    return k ** (2 * d + 1) + 2 * d + 2


def main() -> int:
    failures: list[str] = []

    # the counting lemma and the pigeonhole on instances
    nodup_below_3 = [list(p) for r in range(5) for p in itertools.permutations(range(3), r)]
    ok_count = all(len(l) <= 3 for l in nodup_below_3)
    f = [t % 3 for t in range(4)]
    coll = [(p, q) for p in range(4) for q in range(p + 1, 4) if f[p] == f[q]]
    print(f"duplicate-free lists below 3 have length <= 3: {ok_count} ({len(nodup_below_3)} lists); "
          f"4 indices into 3 values collide: {coll}")
    if not ok_count or not coll:
        failures.append("pigeonhole")

    # encode: bounded and injective at fixed length
    k, m = 2, 3
    lists = [list(t) for t in itertools.product(range(k), repeat=m)]
    codes = [encode(k, l) for l in lists]
    print(f"encode 2 over the {len(lists)} colour lists of length 3: {codes}; all below 2^3: "
          f"{all(c < k ** m for c in codes)}; injective: {len(set(codes)) == len(codes)}")
    if not all(c < k ** m for c in codes) or len(set(codes)) != len(codes):
        failures.append("encode")

    # the bound: every bounded colouring collides on a deep pair at the threshold
    print("k, d: threshold; deep points there; every colouring of 0..n collides on a deep pair")
    for k, d in ((1, 0), (1, 1), (2, 0), (2, 1), (3, 0)):
        n = threshold(k, d)
        pts = deep_points(n, d)
        all_collide = True
        for cols in itertools.product(range(k), repeat=n + 1):
            colour = cols.__getitem__
            views = [encode(k, colour_ball(colour, i, d)) for i in pts]
            if len(set(views)) == len(views):
                all_collide = False
                break
        print(f"  {k}, {d}: {n}; {pts} ({len(pts)} points, {k ** (2 * d + 1)} possible balls); {all_collide}")
        if not all_collide or len(pts) != k ** (2 * d + 1) + 1:
            failures.append(f"bound k={k} d={d}")

    # below the threshold a separating local view can exist
    print("k, d: n = threshold - 1; a colouring whose radius-d view separates every deep pair")
    for k, d in ((2, 0), (2, 1), (3, 0)):
        n = threshold(k, d) - 1
        pts = deep_points(n, d)
        found = None
        for cols in itertools.product(range(k), repeat=n + 1):
            colour = cols.__getitem__
            views = [encode(k, colour_ball(colour, i, d)) for i in pts]
            if len(set(views)) == len(views):
                found = list(cols)
                break
        print(f"  {k}, {d}: {n}; deep {pts}; colouring {found}")
        if found is None:
            failures.append(f"witness k={k} d={d}")

    # Genesis's own witness: parity at k = 2, d = 0, n = 3
    par = [i % 2 for i in range(4)]
    print(f"parity view at n = 3, d = 0: deep points {deep_points(3, 0)}, views "
          f"{[par[i] for i in deep_points(3, 0)]}, separated: {par[1] != par[2]}")
    if par[1] == par[2]:
        failures.append("parity")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
