"""Dyadic twin threads, cylinder representations, and quotient canonicalization."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DyadicThread:
    """Represents an eventually periodic dyadic thread in Cantor space {0, 1}^N.

    An elementary boundary twin thread has:
    - a finite prefix of length n - 1
    - a discriminating bit at position n - 1 (0 for lower, 1 for upper)
    - a constant tail: 1^infty (tail_symbol = 1) or 0^infty (tail_symbol = 0)
    """

    prefix: Tuple[int, ...]
    discriminating_bit: int
    tail_symbol: int
    scale: int

    def __post_init__(self) -> None:
        if self.scale < 1:
            raise ValueError(f"scale must be >= 1, got {self.scale}")
        if len(self.prefix) != self.scale - 1:
            raise ValueError(
                f"prefix length {len(self.prefix)} != scale - 1 ({self.scale - 1})"
            )
        if self.discriminating_bit not in (0, 1):
            raise ValueError(f"discriminating_bit must be 0 or 1, got {self.discriminating_bit}")
        if self.tail_symbol not in (0, 1):
            raise ValueError(f"tail_symbol must be 0 or 1, got {self.tail_symbol}")

    def coordinate(self, i: int) -> int:
        """Evaluate the thread coordinate at 0-based position i."""
        if i < self.scale - 1:
            return self.prefix[i]
        elif i == self.scale - 1:
            return self.discriminating_bit
        else:
            return self.tail_symbol

    def prefix_at_depth(self, depth: int) -> Tuple[int, ...]:
        """Return the finite prefix of length `depth`."""
        return tuple(self.coordinate(i) for i in range(depth))


def generate_twin_pair(scale: int, prefix: Tuple[int, ...]) -> Tuple[DyadicThread, DyadicThread]:
    """Generate the lower and upper twin threads at given scale with common prefix."""
    if scale < 1:
        raise ValueError(f"scale must be >= 1, got {scale}")
    if len(prefix) != scale - 1:
        raise ValueError(f"prefix length must be {scale - 1}, got {len(prefix)}")
    t_lo = DyadicThread(
        prefix=prefix,
        discriminating_bit=0,
        tail_symbol=1,
        scale=scale,
    )
    t_hi = DyadicThread(
        prefix=prefix,
        discriminating_bit=1,
        tail_symbol=0,
        scale=scale,
    )
    return t_lo, t_hi


def generate_scale_twins(scale: int) -> list[Tuple[DyadicThread, DyadicThread]]:
    """Generate all 2^(scale - 1) dyadic twin pairs at scale n."""
    if scale < 1:
        raise ValueError(f"scale must be >= 1, got {scale}")
    num_pairs = 2 ** (scale - 1)
    twins: list[Tuple[DyadicThread, DyadicThread]] = []
    for idx in range(num_pairs):
        # Construct bit tuple for prefix of length scale - 1
        prefix_bits: list[int] = []
        val = idx
        for _ in range(scale - 1):
            prefix_bits.append(val & 1)
            val >>= 1
        prefix = tuple(reversed(prefix_bits))
        twins.append(generate_twin_pair(scale, prefix))
    return twins


def are_elementary_twins(t1: DyadicThread, t2: DyadicThread) -> bool:
    """Check whether t1 and t2 form an elementary dyadic twin pair."""
    if t1.scale != t2.scale:
        return False
    if t1.prefix != t2.prefix:
        return False
    # Case 1: t1 is lower, t2 is upper
    c1 = (
        t1.discriminating_bit == 0
        and t1.tail_symbol == 1
        and t2.discriminating_bit == 1
        and t2.tail_symbol == 0
    )
    # Case 2: t1 is upper, t2 is lower
    c2 = (
        t1.discriminating_bit == 1
        and t1.tail_symbol == 0
        and t2.discriminating_bit == 0
        and t2.tail_symbol == 1
    )
    return c1 or c2


def dyadic_valuation(thread: DyadicThread, depth: int = 50) -> float:
    """Compute the numerical real valuation in [0, 1] up to precision depth."""
    val = 0.0
    weight = 0.5
    for i in range(depth):
        val += thread.coordinate(i) * weight
        weight *= 0.5
    return val


def canonical_quotient_key(thread: DyadicThread) -> Tuple[int, int]:
    """Compute the canonical quotient key for an elementary twin thread.

    For an elementary twin pair at scale n with prefix w:
    The dyadic rational point is (2 * int(w) + 1) / 2^n.
    We return the canonical coprime pair (numerator, denominator) representing the point in [0, 1].
    """
    prefix_val = 0
    for b in thread.prefix:
        prefix_val = (prefix_val << 1) | b
    numerator = 2 * prefix_val + 1
    denominator = 2 ** thread.scale
    return numerator, denominator
