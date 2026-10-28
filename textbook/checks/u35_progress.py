"""Unit 35 check: the fresh-mark response is always available.

Runs Lean's `mark_progress` recipe (one fresh unary form, one instance on
the second target datum) through Genesis's Python on regimes whose
imposed demands are all met, for every ordered pair of distinct data, and
shows the two hypotheses doing work: an unmet imposed demand blocks the
response, and a datum has no separation from itself. Then checks the
engine assertion that no node is ever without a response.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u35_progress.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import Bounds, NewForm, NewInst, apply_delta, response_valid_naive  # noqa: E402
from derivation.engine import READING_F, READING_L, build_tree  # noqa: E402
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, Impose, replay  # noqa: E402
from derivation.observe import collapsed_pairs, separable, satisfies  # noqa: E402


def mark(r, j):
    """Lean's `[.newForm 1, .newInst r.forms.length [j]]`."""
    return (NewForm(1), NewInst(len(r.forms), (j,)))


def main() -> int:
    failures: list[str] = []
    bases = {
        "bare3": replay([AdmitDatum("x"), AdmitDatum("y"), AdmitDatum("z")]),
        "U0": replay([AdmitDatum("a"), AdmitDatum("b"), Impose(0, 1), AdmitForm(1), AdmitInst(0, (0,))]),
        "mixed": replay([AdmitDatum("x"), AdmitDatum("y"), AdmitDatum("z"), Impose(0, 1),
                         AdmitForm(1), AdmitForm(2), AdmitInst(0, (1,)), AdmitInst(1, (0, 2))]),
    }
    for name, r in bases.items():
        n = r.n_data()
        if not satisfies(r):
            failures.append(f"{name} hypothesis")
        pairs = [(i, j) for i in range(n) for j in range(n) if i < j]
        ok = all(response_valid_naive(r, (i, j), mark(r, j)) and response_valid_naive(r, (i, j), mark(r, i))
                 for i, j in pairs)
        s = apply_delta(r, mark(r, 1))
        print(f"{name}: {n} data, forms {list(r.forms)}, imposed demands met: {satisfies(r)}; "
              f"fresh mark on either datum valid for all {len(pairs)} pairs: {ok}; "
              f"after the mark on datum 1: forms {list(s.forms)}, {len(s.insts)} instances, "
              f"collapsed pairs {collapsed_pairs(s)}")
        if not ok:
            failures.append(f"{name} mark")
    # hypothesis 1: an imposed demand that is not yet met
    unmet = replay([AdmitDatum("x"), AdmitDatum("y"), AdmitDatum("z"), Impose(0, 1)])
    d = mark(unmet, 2)
    s = apply_delta(unmet, d)
    v = response_valid_naive(unmet, (1, 2), d)
    print(f"unmet (0, 1) imposed: the mark on datum 2 separates (1, 2): {separable(s, 1, 2)}, "
          f"(0, 1): {separable(s, 0, 1)}; valid response to (1, 2): {v}")
    if v or not separable(s, 1, 2) or separable(s, 0, 1):
        failures.append("unmet")
    # hypothesis 2: i = j
    r = bases["bare3"]
    s = apply_delta(r, mark(r, 1))
    print(f"a datum against itself: separable(1, 1) = {separable(s, 1, 1)}")
    if separable(s, 1, 1):
        failures.append("self")
    # the engine never lacks a response
    for reading, nm in ((READING_L, "L"), (READING_F, "F")):
        t = build_tree(reading, "mu1", Bounds(2, 2), max_rounds=15, pre_expansion_node_guard=200)
        st = t.stats()["by_status"]
        print(f"reading {nm} tree: statuses {st}; terminal_no_response present: {'terminal_no_response' in st}")
        if "terminal_no_response" in st:
            failures.append(f"{nm} no_response")
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
