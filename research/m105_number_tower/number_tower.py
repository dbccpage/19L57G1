"""Internal Constructive Number Tower: NNO, IntZ, RatQ.

Constructs:
1. Natural Number Object (NNO) with universal pointed recursion.
2. Integers (IntZ) as Grothendieck group of difference pairs over ordinals.
3. Rationals (RatQ) as localization / field of fractions over IntZ.

Enforces:
- Exact arithmetic (zero floating-point operations).
- Equivalence relation semantics (cross-addition for Z, cross-multiplication for Q).
- Complete representative independence under non-canonical forms.
- Parity with fractions.Fraction.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
import fractions
import math
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


# =============================================================================
# 1. Natural Number Object (NNO) & Universal Property
# =============================================================================

@dataclass(frozen=True)
class PointedSystem(Generic[T]):
    """A pointed endosystem (X, pt, step)."""
    pt: T
    step: Callable[[T], T]


def nno_rec(system: PointedSystem[T], n: int) -> T:
    """Universal initial homomorphism out of NNO into any pointed endosystem.
    
    rec(pt, step, 0) = pt
    rec(pt, step, succ(n)) = step(rec(pt, step, n))
    """
    if n < 0:
        raise ValueError(f"NNO input must be non-negative, got {n}")
    curr = system.pt
    for _ in range(n):
        curr = system.step(curr)
    return curr


class NNO:
    """Categorical Natural Number Object witness."""

    @staticmethod
    def zero() -> int:
        return 0

    @staticmethod
    def succ(n: int) -> int:
        if n < 0:
            raise ValueError(f"Expected non-negative integer, got {n}")
        return n + 1

    @staticmethod
    def rec(system: PointedSystem[T], n: int) -> T:
        return nno_rec(system, n)

    @staticmethod
    def check_uniqueness(
        system: PointedSystem[T],
        candidate_hom: Callable[[int], T],
        max_n: int = 50,
    ) -> bool:
        """Verify candidate_hom matches universal rec up to max_n."""
        # 1. Base step: h(0) == pt
        if candidate_hom(0) != system.pt:
            return False
        # 2. Inductive step: h(succ(n)) == step(h(n))
        for i in range(max_n):
            if candidate_hom(i + 1) != system.step(candidate_hom(i)):
                return False
        return True


# =============================================================================
# 2. Grothendieck Integers (IntZ)
# =============================================================================

@dataclass(frozen=True)
class IntZ:
    """Integer represented as a constructive difference pair (pos, neg).
    
    Represents the mathematical integer pos - neg.
    Equivalence relation: (p1, n1) ~ (p2, n2) iff p1 + n2 == p2 + n1.
    """
    pos: int
    neg: int

    def __post_init__(self) -> None:
        if not isinstance(self.pos, int) or not isinstance(self.neg, int):
            raise TypeError("IntZ components must be integers")
        if self.pos < 0 or self.neg < 0:
            raise ValueError(f"IntZ difference components must be non-negative: ({self.pos}, {self.neg})")

    @classmethod
    def from_int(cls, val: int) -> IntZ:
        """Embed Python integer into canonical IntZ."""
        if val >= 0:
            return cls(val, 0)
        return cls(0, -val)

    @classmethod
    def from_nat(cls, n: int) -> IntZ:
        """Embed natural number into IntZ."""
        if n < 0:
            raise ValueError(f"Natural number must be non-negative: {n}")
        return cls(n, 0)

    @classmethod
    def zero(cls) -> IntZ:
        return cls(0, 0)

    @classmethod
    def one(cls) -> IntZ:
        return cls(1, 0)

    def to_int(self) -> int:
        """Evaluate constructive difference to integer."""
        return self.pos - self.neg

    def canonical(self) -> tuple[int, int]:
        """Return reduced canonical representative: (x, 0) or (0, y)."""
        if self.pos >= self.neg:
            return (self.pos - self.neg, 0)
        return (0, self.neg - self.pos)

    def is_canonical(self) -> bool:
        return self.pos == 0 or self.neg == 0

    def is_zero(self) -> bool:
        return self.pos == self.neg

    def is_nonneg(self) -> bool:
        return self.pos >= self.neg

    def __eq__(self, other: object) -> bool:
        """Cross-addition equivalence relation."""
        if not isinstance(other, IntZ):
            if isinstance(other, int):
                other = IntZ.from_int(other)
            else:
                return NotImplemented
        return (self.pos + other.neg) == (other.pos + self.neg)

    def __hash__(self) -> int:
        """Hash based on the unique canonical difference pair."""
        return hash(self.canonical())

    def __lt__(self, other: IntZ | int) -> bool:
        if isinstance(other, int):
            other = IntZ.from_int(other)
        elif not isinstance(other, IntZ):
            return NotImplemented
        return (self.pos + other.neg) < (other.pos + self.neg)

    def __le__(self, other: IntZ | int) -> bool:
        if isinstance(other, int):
            other = IntZ.from_int(other)
        elif not isinstance(other, IntZ):
            return NotImplemented
        return (self.pos + other.neg) <= (other.pos + self.neg)

    def __gt__(self, other: IntZ | int) -> bool:
        if isinstance(other, int):
            other = IntZ.from_int(other)
        elif not isinstance(other, IntZ):
            return NotImplemented
        return (self.pos + other.neg) > (other.pos + self.neg)

    def __ge__(self, other: IntZ | int) -> bool:
        if isinstance(other, int):
            other = IntZ.from_int(other)
        elif not isinstance(other, IntZ):
            return NotImplemented
        return (self.pos + other.neg) >= (other.pos + self.neg)

    def __neg__(self) -> IntZ:
        return IntZ(self.neg, self.pos)

    def __add__(self, other: IntZ | int) -> IntZ:
        if isinstance(other, int):
            other = IntZ.from_int(other)
        elif not isinstance(other, IntZ):
            return NotImplemented
        return IntZ(self.pos + other.pos, self.neg + other.neg)

    def __radd__(self, other: int) -> IntZ:
        return IntZ.from_int(other) + self

    def __sub__(self, other: IntZ | int) -> IntZ:
        if isinstance(other, int):
            other = IntZ.from_int(other)
        elif not isinstance(other, IntZ):
            return NotImplemented
        return self + (-other)

    def __rsub__(self, other: int) -> IntZ:
        return IntZ.from_int(other) - self

    def __mul__(self, other: IntZ | int) -> IntZ:
        if isinstance(other, int):
            other = IntZ.from_int(other)
        elif not isinstance(other, IntZ):
            return NotImplemented
        # (p1 - n1) * (p2 - n2) = (p1*p2 + n1*n2) - (p1*n2 + n1*p2)
        pos_part = self.pos * other.pos + self.neg * other.neg
        neg_part = self.pos * other.neg + self.neg * other.pos
        return IntZ(pos_part, neg_part)

    def __rmul__(self, other: int) -> IntZ:
        return IntZ.from_int(other) * self

    def __repr__(self) -> str:
        if self.is_canonical():
            return f"IntZ({self.to_int()})"
        return f"IntZ({self.pos}, {self.neg})[={self.to_int()}]"


# =============================================================================
# 3. Rational Numbers (RatQ)
# =============================================================================

@dataclass(frozen=True)
class RatQ:
    """Constructive rational represented as fraction pair (num, den).
    
    num: IntZ (numerator)
    den: int strictly > 0 (denominator)
    
    Equivalence relation: (p1, q1) ~ (p2, q2) iff p1 * q2 == p2 * q1 in IntZ.
    """
    num: IntZ
    den: int

    def __post_init__(self) -> None:
        if not isinstance(self.num, IntZ):
            if isinstance(self.num, int):
                object.__setattr__(self, "num", IntZ.from_int(self.num))
            else:
                raise TypeError(f"Numerator must be IntZ or int, got {type(self.num)}")
        if not isinstance(self.den, int):
            raise TypeError(f"Denominator must be integer, got {type(self.den)}")
        if self.den <= 0:
            raise ValueError(f"Denominator must be strictly positive natural number, got {self.den}")

    @classmethod
    def from_int(cls, val: int) -> RatQ:
        return cls(IntZ.from_int(val), 1)

    @classmethod
    def from_int_z(cls, z: IntZ) -> RatQ:
        return cls(z, 1)

    @classmethod
    def from_nat(cls, n: int) -> RatQ:
        return cls(IntZ.from_nat(n), 1)

    @classmethod
    def from_fraction(cls, frac: fractions.Fraction) -> RatQ:
        return cls(IntZ.from_int(frac.numerator), frac.denominator)

    @classmethod
    def zero(cls) -> RatQ:
        return cls(IntZ.zero(), 1)

    @classmethod
    def one(cls) -> RatQ:
        return cls(IntZ.one(), 1)

    def to_fraction(self) -> fractions.Fraction:
        """Convert to Python fractions.Fraction with exact parity."""
        return fractions.Fraction(self.num.to_int(), self.den)

    def canonical(self) -> tuple[int, int]:
        """Return reduced canonical coprime pair: (n, d) with d > 0, gcd(|n|, d) == 1."""
        n = self.num.to_int()
        g = math.gcd(abs(n), self.den)
        return (n // g, self.den // g)

    def is_canonical(self) -> bool:
        n = self.num.to_int()
        return self.num.is_canonical() and math.gcd(abs(n), self.den) == 1

    def is_zero(self) -> bool:
        return self.num.is_zero()

    def is_nonneg(self) -> bool:
        return self.num.is_nonneg()

    def __eq__(self, other: object) -> bool:
        """Cross-multiplication equivalence relation."""
        if not isinstance(other, RatQ):
            if isinstance(other, (int, fractions.Fraction)):
                other = RatQ.from_fraction(fractions.Fraction(other))
            elif isinstance(other, IntZ):
                other = RatQ.from_int_z(other)
            else:
                return NotImplemented
        # p1 * q2 == p2 * q1
        return (self.num * other.den) == (other.num * self.den)

    def __hash__(self) -> int:
        """Hash based on unique canonical coprime pair."""
        return hash(self.canonical())

    def __lt__(self, other: RatQ | int | fractions.Fraction) -> bool:
        if not isinstance(other, RatQ):
            other = RatQ.from_fraction(fractions.Fraction(other))
        return (self.num * other.den) < (other.num * self.den)

    def __le__(self, other: RatQ | int | fractions.Fraction) -> bool:
        if not isinstance(other, RatQ):
            other = RatQ.from_fraction(fractions.Fraction(other))
        return (self.num * other.den) <= (other.num * self.den)

    def __gt__(self, other: RatQ | int | fractions.Fraction) -> bool:
        if not isinstance(other, RatQ):
            other = RatQ.from_fraction(fractions.Fraction(other))
        return (self.num * other.den) > (other.num * self.den)

    def __ge__(self, other: RatQ | int | fractions.Fraction) -> bool:
        if not isinstance(other, RatQ):
            other = RatQ.from_fraction(fractions.Fraction(other))
        return (self.num * other.den) >= (other.num * self.den)

    def __neg__(self) -> RatQ:
        return RatQ(-self.num, self.den)

    def __add__(self, other: RatQ | int | fractions.Fraction) -> RatQ:
        if not isinstance(other, RatQ):
            other = RatQ.from_fraction(fractions.Fraction(other))
        # (p1 * q2 + p2 * q1) / (q1 * q2)
        new_num = (self.num * other.den) + (other.num * self.den)
        new_den = self.den * other.den
        return RatQ(new_num, new_den)

    def __radd__(self, other: int | fractions.Fraction) -> RatQ:
        return RatQ.from_fraction(fractions.Fraction(other)) + self

    def __sub__(self, other: RatQ | int | fractions.Fraction) -> RatQ:
        if not isinstance(other, RatQ):
            other = RatQ.from_fraction(fractions.Fraction(other))
        return self + (-other)

    def __rsub__(self, other: int | fractions.Fraction) -> RatQ:
        return RatQ.from_fraction(fractions.Fraction(other)) - self

    def __mul__(self, other: RatQ | int | fractions.Fraction) -> RatQ:
        if not isinstance(other, RatQ):
            other = RatQ.from_fraction(fractions.Fraction(other))
        # (p1 * p2) / (q1 * q2)
        return RatQ(self.num * other.num, self.den * other.den)

    def __rmul__(self, other: int | fractions.Fraction) -> RatQ:
        return RatQ.from_fraction(fractions.Fraction(other)) * self

    def inv(self) -> RatQ:
        """Multiplicative inverse: (p / q)^(-1) = q / p.
        
        Requires numerator != 0.
        Maintains positive denominator constraint.
        """
        if self.is_zero():
            raise ZeroDivisionError("Cannot invert zero rational")
        n_val = self.num.to_int()
        if n_val > 0:
            return RatQ(IntZ.from_nat(self.den), n_val)
        return RatQ(IntZ.from_int(-self.den), -n_val)

    def __truediv__(self, other: RatQ | int | fractions.Fraction) -> RatQ:
        if not isinstance(other, RatQ):
            other = RatQ.from_fraction(fractions.Fraction(other))
        return self * other.inv()

    def __rtruediv__(self, other: int | fractions.Fraction) -> RatQ:
        return RatQ.from_fraction(fractions.Fraction(other)) / self

    def __repr__(self) -> str:
        cn, cd = self.canonical()
        if self.is_canonical():
            return f"RatQ({cn}/{cd})"
        return f"RatQ({self.num!r}/{self.den})[={cn}/{cd}]"
