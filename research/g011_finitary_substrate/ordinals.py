"""Pure Inductive Finitary Ordinals.

Provides endogenous finite ordinals, identity, order, and arithmetic
without reliance on host Nat, host pointers, or host memory order.

AuthorityEffect: None.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterator


class Ordinal(ABC):
    """Abstract base class for pure finitary inductive ordinals."""

    @abstractmethod
    def is_zero(self) -> bool:
        """Return True iff this ordinal is zero."""

    @abstractmethod
    def pred(self) -> Ordinal:
        """Return the predecessor of this ordinal, or zero if zero."""

    def succ(self) -> Ordinal:
        """Return the successor of this ordinal."""
        return Succ(self)

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Endogenous structural equality."""

    @abstractmethod
    def __hash__(self) -> int:
        """Endogenous hash consistent with structural equality."""

    def __lt__(self, other: Ordinal) -> bool:
        """Endogenous strict order: a < b iff succ(a) <= b."""
        if not isinstance(other, Ordinal):
            return NotImplemented
        return self.succ().le(other)

    def __le__(self, other: Ordinal) -> bool:
        """Endogenous non-strict order."""
        if not isinstance(other, Ordinal):
            return NotImplemented
        return self.le(other)

    def __gt__(self, other: Ordinal) -> bool:
        if not isinstance(other, Ordinal):
            return NotImplemented
        return other < self

    def __ge__(self, other: Ordinal) -> bool:
        if not isinstance(other, Ordinal):
            return NotImplemented
        return other <= self

    def le(self, other: Ordinal) -> bool:
        """Endogenous less-or-equal relation evaluated iteratively without stack recursion."""
        if not isinstance(other, Ordinal):
            raise TypeError(f"expected Ordinal, got {type(other)}")
        curr_self: Ordinal = self
        curr_other: Ordinal = other
        while not curr_self.is_zero():
            if curr_other.is_zero():
                return False
            curr_self = curr_self.pred()
            curr_other = curr_other.pred()
        return True

    def add(self, other: Ordinal) -> Ordinal:
        """Endogenous inductive addition: 0 + b = b, succ(a) + b = succ(a + b)."""
        if not isinstance(other, Ordinal):
            raise TypeError(f"expected Ordinal, got {type(other)}")
        if self.is_zero():
            return other
        return self.pred().add(other).succ()

    def mul(self, other: Ordinal) -> Ordinal:
        """Endogenous inductive multiplication: 0 * b = 0, succ(a) * b = b + (a * b)."""
        if not isinstance(other, Ordinal):
            raise TypeError(f"expected Ordinal, got {type(other)}")
        if self.is_zero():
            return Zero()
        return other.add(self.pred().mul(other))

    def sub(self, other: Ordinal) -> Ordinal:
        """Endogenous truncated subtraction: a - 0 = a, 0 - succ(b) = 0, succ(a) - succ(b) = a - b."""
        if not isinstance(other, Ordinal):
            raise TypeError(f"expected Ordinal, got {type(other)}")
        if other.is_zero():
            return self
        if self.is_zero():
            return Zero()
        return self.pred().sub(other.pred())

    def compare(self, other: Ordinal) -> int:
        """Endogenous trichotomy comparison returning -1, 0, or 1."""
        if self == other:
            return 0
        if self.le(other):
            return -1
        return 1

    @classmethod
    def zero(cls) -> Ordinal:
        """Factory for zero ordinal."""
        return Zero()

    @classmethod
    def from_nat(cls, n: int) -> Ordinal:
        """Reify an ordinal from a host integer (for external test boundaries only)."""
        if not isinstance(n, int) or n < 0:
            raise ValueError(f"expected non-negative int, got {n}")
        res: Ordinal = Zero()
        for _ in range(n):
            res = res.succ()
        return res

    def to_nat(self) -> int:
        """Convert to host integer (for external boundary inspection only)."""
        curr = self
        count = 0
        while not curr.is_zero():
            count += 1
            curr = curr.pred()
        return count


class Zero(Ordinal):
    """The zero ordinal."""

    _instance: Zero | None = None

    def __new__(cls) -> Zero:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def is_zero(self) -> bool:
        return True

    def pred(self) -> Ordinal:
        return self

    def le(self, other: Ordinal) -> bool:
        # Zero is <= any ordinal
        return True

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Zero)

    def __hash__(self) -> int:
        return hash((Zero, 0))

    def __repr__(self) -> str:
        return "Ordinal.zero()"


class Succ(Ordinal):
    """The successor ordinal succ(o)."""

    __slots__ = ("_pred",)

    def __init__(self, pred: Ordinal) -> None:
        if not isinstance(pred, Ordinal):
            raise TypeError(f"expected Ordinal predecessor, got {type(pred)}")
        self._pred = pred

    def is_zero(self) -> bool:
        return False

    def pred(self) -> Ordinal:
        return self._pred

    def le(self, other: Ordinal) -> bool:
        return super().le(other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ordinal):
            return False
        curr_self: Ordinal = self
        curr_other: Ordinal = other
        while not curr_self.is_zero() and not curr_other.is_zero():
            curr_self = curr_self.pred()
            curr_other = curr_other.pred()
        return curr_self.is_zero() and curr_other.is_zero()

    def __hash__(self) -> int:
        return hash((Ordinal, self.to_nat()))

    def __repr__(self) -> str:
        return f"Ordinal.from_nat({self.to_nat()})"
