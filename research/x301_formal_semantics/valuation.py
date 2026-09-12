"""Exact rational Heyting valuations in [0, 1] cap Q.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Union

@dataclass(frozen=True)
class RationalValuation:
    """Exact rational truth valuation in [0, 1] cap Q.

    Operates over an exact rational Heyting truth structure (poset):
    - Top element (True): 1
    - Bottom element (False): 0
    - Intermediate values: partial / constructive evidence weights
    - Meet: min(a, b)
    - Join: max(a, b)
    - Heyting Implication: 1 if a <= b else b
    - Pseudo-complement / Operational Negation: 1 if a == 0 else 0
    """

    val: Fraction

    def __init__(self, val: Union[Fraction, int, str] = 0):
        if isinstance(val, float):
            raise TypeError("float is not exact Q; pass Fraction, int, or rational str")
        if isinstance(val, RationalValuation):
            frac = val.val
        elif isinstance(val, Fraction):
            frac = val
        elif isinstance(val, int):
            frac = Fraction(val, 1)
        elif isinstance(val, str):
            frac = Fraction(val)
        else:
            raise TypeError(f"Unsupported exact-Q conversion: {type(val)}")

        if not (Fraction(0, 1) <= frac <= Fraction(1, 1)):
            raise ValueError(f"Valuation must be in [0, 1], got {frac}")
        object.__setattr__(self, "val", frac)

    @property
    def is_true(self) -> bool:
        return self.val == Fraction(1, 1)

    @property
    def is_false(self) -> bool:
        return self.val == Fraction(0, 1)

    def __bool__(self) -> bool:
        return self.is_true

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RationalValuation):
            return self.val == other.val
        if isinstance(other, (Fraction, int)):
            return self.val == other
        return False

    def __lt__(self, other: RationalValuation) -> bool:
        return self.val < other.val

    def __le__(self, other: RationalValuation) -> bool:
        return self.val <= other.val

    def __gt__(self, other: RationalValuation) -> bool:
        return self.val > other.val

    def __ge__(self, other: RationalValuation) -> bool:
        return self.val >= other.val

    def __hash__(self) -> int:
        return hash(self.val)

    def __repr__(self) -> str:
        return f"RationalValuation({self.val})"

    def __str__(self) -> str:
        return str(self.val)

    def __and__(self, other: RationalValuation) -> RationalValuation:
        return meet(self, other)

    def __or__(self, other: RationalValuation) -> RationalValuation:
        return join(self, other)

    def __invert__(self) -> RationalValuation:
        return pseudo_complement(self)


TRUE = RationalValuation(Fraction(1, 1))
FALSE = RationalValuation(Fraction(0, 1))
HALF = RationalValuation(Fraction(1, 2))


def meet(a: RationalValuation, b: RationalValuation) -> RationalValuation:
    """Greatest lower bound in the valuation poset: min(a, b)."""
    return a if a.val <= b.val else b


def join(a: RationalValuation, b: RationalValuation) -> RationalValuation:
    """Least upper bound in the valuation poset: max(a, b)."""
    return b if a.val <= b.val else a


def implies(a: RationalValuation, b: RationalValuation) -> RationalValuation:
    """Heyting implication in the linearly ordered valuation poset.

    a -> b = 1 if a <= b else b.
    Satisfies the adjunction: meet(c, a) <= b iff c <= implies(a, b).
    """
    if a.val <= b.val:
        return TRUE
    return b


def pseudo_complement(a: RationalValuation) -> RationalValuation:
    """Operational negation / pseudo-complement: a -> 0."""
    return implies(a, FALSE)
