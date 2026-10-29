"""Unit 27 check: the abstraction barrier, computed on the Challenge 2 regime.

This model represents collapse classes by complete profiles and the
engine's isomorphism classes by canonical keys. The
script shows, by sample, what `Quot.barrier_R2L` states: a function that
reads only the class returns the same value on <a> and <ab>.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u27_barrier.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.iso import canonical, group_by_canonical, rename  # noqa: E402
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, Impose, replay  # noqa: E402
from derivation.observe import collapsed_pairs, profile  # noqa: E402


def main() -> int:
    failures: list[str] = []
    r2l = replay([AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(0, 1)])
    print(f"R2L collapsed pairs: {collapsed_pairs(r2l)}")
    if collapsed_pairs(r2l) != ((0, 1),):
        failures.append("R2L not collapsed")

    same_class = profile(r2l, 0) == profile(r2l, 1)
    print(f"profile(0) == profile(1): {same_class}")
    if not same_class:
        failures.append("profiles differ")

    # a function that reads only the class
    def through_class(d: int) -> int:
        return len(profile(r2l, d))

    # a function that reads the raw presentation, not the class
    def raw(d: int) -> str:
        return r2l.data[d]

    print(f"through the class: {through_class(0)} {through_class(1)}; "
          f"raw tokens: {raw(0)!r} {raw(1)!r}")
    if through_class(0) != through_class(1):
        failures.append("class function differs")
    if raw(0) == raw(1):
        failures.append("raw function should differ")

    # the engine's own quotient: isomorphic regimes share a key
    swapped = rename(r2l, (1, 0), ())
    same_key = canonical(r2l) == canonical(swapped)
    groups = group_by_canonical([(r2l, "r2l"), (swapped, "swapped")])
    print(f"canonical key equal after swapping the data: {same_key}; "
          f"groups: {list(groups.values())}")
    if not same_key or len(groups) != 1:
        failures.append("canonical")

    link = replay([AdmitForm(2), AdmitInst(0, (0, 1))], r2l)
    p0, p1 = profile(link, 0), profile(link, 1)
    print(f"binary link: profile sizes {len(p0)}, {len(p1)}; "
          f"equal full profiles={p0 == p1}; collapsed pairs={collapsed_pairs(link)}")
    if len(p0) != 1 or len(p1) != 1 or p0 == p1 or collapsed_pairs(link):
        failures.append("coarse summary is not the full profile")
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
