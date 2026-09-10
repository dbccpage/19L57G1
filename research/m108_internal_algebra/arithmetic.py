"""Exact integer and rational carriers for M108."""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Union

# ==============================================================================
# 1. Exact Internal Arithmetic (Z and Q)
# ==============================================================================

@dataclass(frozen=True)
class InternalInt:
    """Exact constructive integer with zero floating-point logic."""
    val: int

    def __init__(self, val: Union[int, InternalInt]) -> None:
        if isinstance(val, InternalInt):
            object.__setattr__(self, "val", val.val)
        elif isinstance(val, int):
            object.__setattr__(self, "val", val)
        else:
            raise TypeError(f"InternalInt expects int, got {type(val).__name__}")

    def __add__(self, other: Union[InternalInt, int]) -> InternalInt:
        o = other.val if isinstance(other, InternalInt) else int(other)
        return InternalInt(self.val + o)

    def __radd__(self, other: int) -> InternalInt:
        return self.__add__(other)

    def __sub__(self, other: Union[InternalInt, int]) -> InternalInt:
        o = other.val if isinstance(other, InternalInt) else int(other)
        return InternalInt(self.val - o)

    def __rsub__(self, other: int) -> InternalInt:
        return InternalInt(int(other) - self.val)

    def __mul__(self, other: Union[InternalInt, int]) -> InternalInt:
        o = other.val if isinstance(other, InternalInt) else int(other)
        return InternalInt(self.val * o)

    def __rmul__(self, other: int) -> InternalInt:
        return self.__mul__(other)

    def __neg__(self) -> InternalInt:
        return InternalInt(-self.val)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, InternalInt):
            return self.val == other.val
        if isinstance(other, int):
            return self.val == other
        return False

    def __lt__(self, other: Union[InternalInt, int]) -> bool:
        o = other.val if isinstance(other, InternalInt) else int(other)
        return self.val < o

    def __le__(self, other: Union[InternalInt, int]) -> bool:
        o = other.val if isinstance(other, InternalInt) else int(other)
        return self.val <= o

    def __hash__(self) -> int:
        return hash(self.val)

    def __repr__(self) -> str:
        return f"InternalInt({self.val})"


@dataclass(frozen=True)
class InternalRat:
    """Exact constructive rational pair (num, den) with den > 0 and gcd(num, den) = 1."""
    num: int
    den: int

    def __init__(self, num: Union[int, InternalInt, InternalRat], den: Union[int, InternalInt] = 1) -> None:
        if isinstance(num, InternalRat):
            if den != 1:
                raise ValueError("Cannot specify second denominator when numerator is InternalRat")
            object.__setattr__(self, "num", num.num)
            object.__setattr__(self, "den", num.den)
            return

        n = num.val if isinstance(num, InternalInt) else int(num)
        d = den.val if isinstance(den, InternalInt) else int(den)
        if d == 0:
            raise ZeroDivisionError("Rational denominator cannot be zero")
        if d < 0:
            n = -n
            d = -d
        g = math.gcd(abs(n), d)
        object.__setattr__(self, "num", n // g)
        object.__setattr__(self, "den", d // g)

    @classmethod
    def zero(cls) -> InternalRat:
        return cls(0, 1)

    @classmethod
    def one(cls) -> InternalRat:
        return cls(1, 1)

    def is_zero(self) -> bool:
        return self.num == 0

    def __add__(self, other: Union[InternalRat, InternalInt, int]) -> InternalRat:
        o = self._to_rat(other)
        return InternalRat(self.num * o.den + o.num * self.den, self.den * o.den)

    def __radd__(self, other: Union[InternalInt, int]) -> InternalRat:
        return self.__add__(other)

    def __sub__(self, other: Union[InternalRat, InternalInt, int]) -> InternalRat:
        o = self._to_rat(other)
        return InternalRat(self.num * o.den - o.num * self.den, self.den * o.den)

    def __rsub__(self, other: Union[InternalInt, int]) -> InternalRat:
        o = self._to_rat(other)
        return o.__sub__(self)

    def __mul__(self, other: Union[InternalRat, InternalInt, int]) -> InternalRat:
        o = self._to_rat(other)
        return InternalRat(self.num * o.num, self.den * o.den)

    def __rmul__(self, other: Union[InternalInt, int]) -> InternalRat:
        return self.__mul__(other)

    def __truediv__(self, other: Union[InternalRat, InternalInt, int]) -> InternalRat:
        o = self._to_rat(other)
        if o.num == 0:
            raise ZeroDivisionError("Division by zero rational")
        return InternalRat(self.num * o.den, self.den * o.num)

    def __neg__(self) -> InternalRat:
        return InternalRat(-self.num, self.den)

    def inv(self) -> InternalRat:
        if self.num == 0:
            raise ZeroDivisionError("Cannot invert zero rational")
        return InternalRat(self.den, self.num)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, InternalRat):
            return self.num == other.num and self.den == other.den
        if isinstance(other, (InternalInt, int)):
            o = other.val if isinstance(other, InternalInt) else other
            return self.den == 1 and self.num == o
        return False

    def __lt__(self, other: Union[InternalRat, InternalInt, int]) -> bool:
        o = self._to_rat(other)
        return self.num * o.den < o.num * self.den

    def __le__(self, other: Union[InternalRat, InternalInt, int]) -> bool:
        o = self._to_rat(other)
        return self.num * o.den <= o.num * self.den

    def __hash__(self) -> int:
        return hash((self.num, self.den))

    def __repr__(self) -> str:
        return f"InternalRat({self.num}/{self.den})"

    @staticmethod
    def _to_rat(x: Union[InternalRat, InternalInt, int]) -> InternalRat:
        if isinstance(x, InternalRat):
            return x
        if isinstance(x, InternalInt):
            return InternalRat(x.val, 1)
        if isinstance(x, int):
            return InternalRat(x, 1)
        raise TypeError(f"Cannot convert {type(x).__name__} to InternalRat")

