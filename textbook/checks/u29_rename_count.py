"""Unit 29 check: the collapsed-pair count survives every renaming of the data.

Genesis's `iso.rename` applies a bijection of the data (and of the forms;
here the identity). For every permutation of the data of two sample
regimes the collapsed pairs are carried to the collapsed pairs and their
number is unchanged. The countermodel of `CountTransport.lean` is shown
on the Python side: `cmRegime` separates its two data, and a datum is
never separable from itself.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u29_rename_count.py
"""
from __future__ import annotations

import sys
from itertools import permutations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.iso import rename  # noqa: E402
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, Regime, replay  # noqa: E402
from derivation.observe import collapsed_pairs, separable  # noqa: E402


def transported(r: Regime, pi: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted((min(pi[i], pi[j]), max(pi[i], pi[j]))
                        for (i, j) in collapsed_pairs(r)))


def main() -> int:
    failures: list[str] = []
    cm = replay([AdmitDatum("a"), AdmitDatum("b"), AdmitForm(1), AdmitInst(0, (0,))])
    print(f"cmRegime: separable(0, 1) {separable(cm, 0, 1)}, collapsed pairs "
          f"{collapsed_pairs(cm)}, separable(0, 0) {separable(cm, 0, 0)}")
    if not separable(cm, 0, 1) or separable(cm, 0, 0):
        failures.append("cmRegime")

    reg = replay([AdmitDatum("a"), AdmitDatum("b"), AdmitDatum("c"),
                  AdmitDatum("d"), AdmitForm(1), AdmitInst(0, (2,)),
                  AdmitInst(0, (3,))])
    link = replay([AdmitDatum("w"), AdmitDatum("x"), AdmitDatum("y"),
                   AdmitForm(2), AdmitInst(0, (0, 1))])
    for name, r in (("regRegime", reg), ("link3", link)):
        base = collapsed_pairs(r)
        n = r.n_data()
        ok = True
        for pi in permutations(range(n)):
            rr = rename(r, pi, tuple(range(len(r.forms))))
            ok &= collapsed_pairs(rr) == transported(r, pi)
            ok &= len(collapsed_pairs(rr)) == len(base)
        print(f"{name}: collapsed {base}; over all {len(list(permutations(range(n))))} "
              f"renamings the pairs are carried and the count is {len(base)}: {ok}")
        if not ok:
            failures.append(name)
        swap = tuple(reversed(range(n)))
        print(f"  example, renaming {swap}: {collapsed_pairs(rename(r, swap, tuple(range(len(r.forms)))))}")

    mark0 = replay([AdmitDatum("a"), AdmitDatum("b"), AdmitDatum("c"),
                    AdmitForm(1), AdmitInst(0, (0,))])
    renamed = rename(mark0, (1, 0, 2), (0,))
    before, after = collapsed_pairs(mark0), collapsed_pairs(renamed)
    print(f"fixed versus mapped pair: before={before}, after={after}; "
          f"old (1,2) collapsed={(1, 2) in before}; mapped (0,2) collapsed={(0, 2) in after}; "
          f"fixed (1,2) collapsed={(1, 2) in after}")
    if before != ((1, 2),) or after != ((0, 2),):
        failures.append("fixed pair list is not transported")
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
