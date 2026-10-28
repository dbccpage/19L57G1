"""Unit 30 check: the mention lemma and the two irrelevance corollaries.

On a three-datum regime with one unary form: an instance mentioning only
datum 2 leaves (0, 1) collapsed (R3); a fresh form with no instance
leaves every pair as it was (R2); an instance mentioning datum 0
separates (0, 1), the boundary. Then the pruning the lemma licenses:
on a four-datum base, every cost-2 delta the pruned enumeration drops
that is instance-only mentions neither target datum and is not a valid
response.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u30_mention.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import (  # noqa: E402
    Bounds,
    NewInst,
    iter_cost2_deltas,
    iter_full_deltas,
    response_valid_naive,
)
from derivation.model import AdmissionError, AdmitDatum, AdmitForm, AdmitInst, replay  # noqa: E402
from derivation.observe import collapsed_pairs, contexts, plug  # noqa: E402


def main() -> int:
    failures: list[str] = []
    base = replay([AdmitDatum("a"), AdmitDatum("b"), AdmitDatum("c"), AdmitForm(1)])
    r3 = replay([AdmitInst(0, (2,))], base)
    r2 = replay([AdmitForm(2)], base)
    edge = replay([AdmitInst(0, (0,))], base)
    print(f"base {collapsed_pairs(base)}; mark on 2 (R3) {collapsed_pairs(r3)}; "
          f"fresh binary form (R2) {collapsed_pairs(r2)}; mark on 0 {collapsed_pairs(edge)}")
    if collapsed_pairs(base) != ((0, 1), (0, 2), (1, 2)):
        failures.append("base")
    if (0, 1) not in collapsed_pairs(r3) or collapsed_pairs(r3) != ((0, 1),):
        failures.append("R3")
    if collapsed_pairs(r2) != collapsed_pairs(base):
        failures.append("R2")
    if (0, 1) in collapsed_pairs(edge):
        failures.append("boundary")

    every_plug = all(d in plug(c, d)[1] for c in contexts(r2) for d in range(3))
    print(f"every plug mentions its datum ({len(contexts(r2))} contexts of the "
          f"regime with both forms): {every_plug}")
    if not every_plug:
        failures.append("plug")

    four = replay([AdmitDatum("a"), AdmitDatum("b"), AdmitDatum("c"),
                   AdmitDatum("d"), AdmitForm(1)])
    target = (0, 1)
    bounds = Bounds(max_items=2, max_arity=2)
    full = list(iter_full_deltas(four, 2, bounds))
    pruned = set(iter_cost2_deltas(four, bounds, target))
    dropped = [d for d in full if d not in pruned]

    def valid(d: tuple[object, ...]) -> bool:
        try:
            return response_valid_naive(four, target, d)  # type: ignore[arg-type]
        except AdmissionError:
            return False

    # the mention lemma's own case: two distinct instances, neither mentioning 0 or 1
    unmentioning = [d for d in dropped
                    if all(isinstance(it, NewInst) for it in d) and d[0] != d[1]
                    and all(0 not in it.args and 1 not in it.args for it in d)]  # type: ignore[union-attr]
    unmentioning_valid = [d for d in unmentioning if valid(d)]
    # every other dropped delta that is valid has a valid one-item part
    valid_dropped = [d for d in dropped if valid(d)]
    covered = [d for d in valid_dropped if any(valid((it,)) for it in d)]
    print(f"four data, target (0, 1): {len(full)} two-item deltas, {len(pruned)} kept, "
          f"{len(dropped)} dropped")
    print(f"  dropped by the mention lemma (two distinct instances, neither mentioning 0 or 1): "
          f"{unmentioning}; valid: {len(unmentioning_valid)}")
    print(f"  valid dropped deltas: {len(valid_dropped)}; each has a valid one-item part: "
          f"{len(covered) == len(valid_dropped)}")
    if unmentioning_valid or len(unmentioning) != 1 or len(covered) != len(valid_dropped):
        failures.append("pruning")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
