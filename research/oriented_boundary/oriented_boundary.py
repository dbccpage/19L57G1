"""Mechanization of the (B)-is-empty lemma that discharges SF-OPEN-A.

Classification: metatheory apparatus for an OPEN, ANALYTIC result. Touches
nothing under the seal. The result is ANALYTIC (author-reasoned, then reproduced
by a clean model run at VERDICT T7), not blind. See ``CLOSURE.md`` (this folder)
for the discharge and ``research/side_free/CLAIM_LEDGER.md`` (SF-OPEN-A, in the
19L57G1 repository) for the obstruction.

The question SF-OPEN-A left open was the *kind* classification: what kind of
thing is the admission order? The load-bearing lemma is that route (B) is empty.

Two routes to ``sigma not in Aut(M)`` were held distinct, where ``sigma`` is the
swap ``(x y)`` and ``Aut(M)`` is the permutations preserving every admitted
judgment:

  (A) admit a non-symmetric witness that distinguishes ``x`` from ``y``;
  (B) withdraw ``sigma`` from the automorphism family with **no** witness.

Claim: **(B) is empty.** If no admitted judgment distinguishes ``x, y`` then
every admitted judgment ``d`` has ``d(x,y) = d(y,x)``, so ``sigma`` preserves all
of them and ``sigma in Aut(M)``. Hence ``sigma not in Aut(M)`` forces some
admitted ``d`` with ``d(x,y) != d(y,x)`` -- exactly (A). A withdrawal with no
such ``d`` is either the forbidden observer-from-nowhere or a covert (A).

A judgment is modelled by its action on the tested ordered pair, the pair
``(d(x,y), d(y,x))`` -- CLOSURE.md's own formulation. The diagonal / reflexive
entries are not what the orientation question turns on.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any, Sequence

# A judgment read by its action on the tested ordered pair: (d(x,y), d(y,x)).
Judgment = tuple[bool, bool]

# The four distinct judgments on the pair. Two are symmetric, two asymmetric.
ALL_JUDGMENTS: tuple[Judgment, ...] = ((False, False), (True, True), (False, True), (True, False))


def distinguishes(d: Judgment) -> bool:
    """``d`` is a mechanism-(A) witness iff it is asymmetric on the pair."""
    return d[0] != d[1]


def swap_preserves(d: Judgment) -> bool:
    """The swap ``sigma = (x y)`` preserves ``d`` on the tested pair iff ``d`` is
    symmetric on it: ``d(x,y) = d(y,x)``."""
    return d[0] == d[1]


def swap_in_aut(admitted: Sequence[Judgment]) -> bool:
    """``sigma in Aut(M)`` iff ``sigma`` preserves every admitted judgment."""
    return all(swap_preserves(d) for d in admitted)


def has_A_witness(admitted: Sequence[Judgment]) -> bool:
    """Mechanism (A) is present: some admitted judgment distinguishes the pair."""
    return any(distinguishes(d) for d in admitted)


def b_is_empty(admitted: Sequence[Judgment]) -> bool:
    """The (B)-empty lemma on one admitted set: if ``sigma not in Aut`` then a
    mechanism-(A) witness is present. There is no witnessless route (B)."""
    if swap_in_aut(admitted):
        return True  # sigma in Aut: (B) does not even arise
    return has_A_witness(admitted)


def _all_admitted_sets() -> list[tuple[Judgment, ...]]:
    """Every finite admitted set over the four distinct judgments (2**4 = 16)."""
    out: list[tuple[Judgment, ...]] = []
    for k in range(len(ALL_JUDGMENTS) + 1):
        out.extend(combinations(ALL_JUDGMENTS, k))
    return out


# The two readings of AUTHOR_READING.md, in this model.
S2_U: tuple[Judgment, ...] = ((False, False),)  # unoriented: only a symmetric judgment
S2_O: tuple[Judgment, ...] = ((False, False), (True, False))  # oriented: one asymmetric witness


def breaking_witnesses(admitted: Sequence[Judgment]) -> tuple[Judgment, ...]:
    """The admitted judgments that break ``sigma``'s automorphism (the (A) witnesses)."""
    return tuple(d for d in admitted if distinguishes(d))


def receipt() -> dict[str, Any]:
    """Deterministic record of the mechanized discharge."""
    subsets = _all_admitted_sets()
    b_empty_all = all(b_is_empty(s) for s in subsets)
    # swap in Aut IFF no (A) witness -- exhaustively, over every admitted set.
    iff_all = all(swap_in_aut(s) == (not has_A_witness(s)) for s in subsets)
    # (B) unrepresentable: no admitted set gives sigma-not-in-Aut without an (A) witness.
    from_nowhere = any((not swap_in_aut(s)) and (not has_A_witness(s)) for s in subsets)
    return {
        "authority_effect": "None",
        "carrier": "two data x, y; judgment read as (d(x,y), d(y,x))",
        "n_admitted_sets_checked": len(subsets),
        "b_is_empty_over_all_admitted_sets": b_empty_all,
        "swap_in_aut_iff_no_A_witness": iff_all,
        "from_nowhere_withdrawal_representable": from_nowhere,  # must be False
        "S2_U_swap_is_automorphism": swap_in_aut(S2_U),  # AP1: True
        "S2_O_swap_is_automorphism": swap_in_aut(S2_O),  # AP2: False
        "S2_O_breaking_witness_count": len(breaking_witnesses(S2_O)),  # exactly one capability
        "discharges": "SF-OPEN-A (research/side_free/CLAIM_LEDGER.md): an order is a paid "
        "symmetry-breaking admitted witness (mechanism A, one capability), not a container.",
        "grade": "analytic discharge (not blind); object-language only, not physics",
    }


def main() -> None:
    import json

    print(json.dumps(receipt(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
