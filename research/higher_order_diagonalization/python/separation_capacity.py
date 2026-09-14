"""Separation capacity bounds and scale depth gap.

AuthorityEffect: None.
"""

from __future__ import annotations

from itertools import product
from typing import Iterator

from .observer_hierarchy import ScaleRegime, canon_seq


def nat_to_bits(length: int, n: int) -> tuple[int, ...]:
    """Convert natural number to little-endian binary bit tuple of fixed length."""
    if n < 0:
        raise ValueError("n must be non-negative")
    bits: list[int] = []
    val = n
    for _ in range(length):
        bits.append(val % 2)
        val //= 2
    return tuple(bits)


def bits_to_nat(bits: tuple[int, ...]) -> int:
    """Decode little-endian binary bit tuple back to natural number."""
    val = 0
    multiplier = 1
    for b in bits:
        val += b * multiplier
        multiplier *= 2
    return val


def capacity(k: int) -> int:
    """Maximum separation capacity of observer of resolution depth k: 2^k."""
    if k < 0:
        raise ValueError("k must be non-negative")
    return 2**k


def canonical_family_size(k: int) -> int:
    """Size of canonical test regime family at scale depth k+2: 2^(k+1)."""
    return 2 ** (k + 1)


def canonical_test_regime(k: int, i: int) -> ScaleRegime:
    """Canonical test regime i at scale depth k+2. Starts with 0 followed by nat_to_bits(k+1, i)."""
    bound = canonical_family_size(k)
    if not (0 <= i < bound):
        raise ValueError(f"index i={i} must be in [0, {bound})")
    tokens = (0,) + nat_to_bits(k + 1, i)
    return ScaleRegime(depth=k + 2, tokens=tokens)


def capacity_gap(k: int, d: int) -> int:
    """Exact gap between isomorphism classes at scale depth d and capacity at depth k."""
    if d > k + 1:
        return (2 ** (d - 1)) - capacity(k)
    return 0


def enumerate_canonical_regimes(depth: int) -> Iterator[ScaleRegime]:
    """Enumerate canonical regimes of given depth without duplicates."""
    seen: set[tuple[int, ...]] = set()
    for seq in product((0, 1), repeat=depth):
        c = tuple(canon_seq(seq))
        if c not in seen:
            seen.add(c)
            yield ScaleRegime(depth=depth, tokens=c)
