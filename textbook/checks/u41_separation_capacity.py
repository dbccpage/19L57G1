"""Unit 41 check: the radius-d structural outrun, computed.

Python (book): Genesis has no Python module for SeparationCapacity. This
script rebuilds `ball` and `profileD` from Genesis's `generator.profile1`
and `profile2` and checks, on chains up to length 15 and radii up to 4:
every deep pair shares a radius-d profile; the least length with a
colliding deep pair is 2d + 3; the radius-one profile and Genesis's
depth-2 profile agree on every interior pair; and the shifted ball at the
left end that the theorems' side conditions keep out of sight.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u41_separation_capacity.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.generator import profile1, profile2  # noqa: E402

MAX_N = 15
MAX_D = 4


def ball(i: int, d: int) -> list[int]:
    """Lean's `ball i d`: `(List.range (2d+1)).map (fun k => i - d + k)`,
    with truncated subtraction (`i - d` is 0 when `d > i`)."""
    return [max(i - d, 0) + k for k in range(2 * d + 1)]


def profile_d(n: int, i: int, d: int) -> list[tuple[bool, bool, bool]]:
    return [profile1(n, k) for k in ball(i, d)]


def deep(n: int, i: int, d: int) -> bool:
    return d < i and i + d < n


def main() -> int:
    failures: list[str] = []
    print(f"ball 2 1 = {ball(2, 1)}; ball 0 1 = {ball(0, 1)} (shifted: truncated subtraction starts the window at 0)")
    if ball(2, 1) != [1, 2, 3] or ball(0, 1) != [0, 1, 2]:
        failures.append("ball")

    all_const = all(
        profile_d(n, i, d) == [(True, True, True)] * (2 * d + 1)
        for d in range(MAX_D + 1) for n in range(1, MAX_N + 1)
        for i in range(n + 1) if deep(n, i, d)
    )
    print(f"every deep point's radius-d profile is the constant interior list "
          f"(n <= {MAX_N}, d <= {MAX_D}): {all_const}")
    if not all_const:
        failures.append("profileD_deep")

    print("radius d: least n with a colliding deep pair; 2d+3; deep points at that n")
    for d in range(MAX_D + 1):
        least = None
        for n in range(1, MAX_N + 1):
            deep_pts = [i for i in range(n + 1) if deep(n, i, d)]
            if any(profile_d(n, i, d) == profile_d(n, j, d)
                   for a, i in enumerate(deep_pts) for j in deep_pts[a + 1:]):
                least = n
                break
        pts = [i for i in range(least + 1) if deep(least, i, d)] if least else []
        print(f"  {d}: {least}; {2 * d + 3}; {pts}")
        if least != 2 * d + 3:
            failures.append(f"threshold d={d}")

    agree = all(
        (profile2(n, i) == profile2(n, j)) == (profile_d(n, i, 1) == profile_d(n, j, 1))
        for n in range(2, MAX_N + 1)
        for i in range(1, n) for j in range(1, n)
    )
    print(f"depth-2 equality == radius-one equality on every interior pair (n <= {MAX_N}): {agree}")
    if not agree:
        failures.append("correspondence")
    print(f"  n = 4: profileD 4 1 1 = {profile_d(4, 1, 1)}, profileD 4 3 1 = {profile_d(4, 3, 1)}; "
          f"deep points at radius 1: {[i for i in range(5) if deep(4, i, 1)]}")
    print(f"  n = 5: profileD 5 2 1 == profileD 5 3 1: {profile_d(5, 2, 1) == profile_d(5, 3, 1)}")
    if profile_d(4, 1, 1) == profile_d(4, 3, 1) or profile_d(5, 2, 1) != profile_d(5, 3, 1):
        failures.append("instances")

    # off the interior the correspondence fails: the shifted ball gives the
    # seed the same radius-one profile as element 1, while their depth-2
    # records differ
    same_d = profile_d(5, 0, 1) == profile_d(5, 1, 1)
    same_2 = profile2(5, 0) == profile2(5, 1)
    print(f"  off the interior (n = 5): profileD 0 == profileD 1: {same_d}; "
          f"profile2 0 == profile2 1: {same_2}; profile2 of the seed: {profile2(5, 0)}")
    if not same_d or same_2:
        failures.append("seed")

    same_at_one = profile_d(5, 2, 1) == profile_d(5, 3, 1)
    same_at_two = profile_d(5, 2, 2) == profile_d(5, 3, 2)
    print(f"fixed stage 5, pair (2,3): equal at radius 1 {same_at_one}; "
          f"equal at radius 2 {same_at_two}")
    if not same_at_one or same_at_two:
        failures.append("radius can help")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
