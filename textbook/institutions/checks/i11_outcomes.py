"""Unit 11 check: same and apart outcomes.

Checks:
  1. outcome_check(3): 243 subset/extension pairs times nine ordered input
     pairs = 2187 counted comparisons. One ordering per partition subset;
     no repeated members. Additionally, 192 distinct-pair extension searches.
     `same` is never `supported`,
     `apart` is never `refuted`, `supported`/`refuted` persist under extension,
     and for `x != y` some extension refutes `same`;
  2. `scoped_identity_not_absolute`: `sameRel([], 0, 1)` is True while
     `sameRel([(0, 1)], 0, 1)` is False.
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i11_outcomes.py
"""
from __future__ import annotations

import _tree  # noqa: F401
from model import outcome_check, sig  # noqa: E402


def main() -> int:
    oc = outcome_check(3)
    print(f"outcome_check(3): {oc}")

    scoped_empty = sig((), 0) == sig((), 1)
    scoped_id = sig(((0, 1),), 0) == sig(((0, 1),), 1)
    print(f"scoped_identity_not_absolute (empty, [id] on 0, 1): {[scoped_empty, scoped_id]}")

    ok = (
        oc["checked"] == 2187
        and oc["violations"] == 0
        and scoped_empty is True
        and scoped_id is False
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
