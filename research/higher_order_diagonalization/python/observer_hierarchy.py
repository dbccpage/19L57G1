"""Finite observer hierarchy and canonical isomorphism coarsening.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence


def flip_token(b: int) -> int:
    """Bit-swap involution on Fin 2."""
    if b not in (0, 1):
        raise ValueError(f"token must be 0 or 1, got {b}")
    return 1 - b


def flip_seq(s: Sequence[int]) -> list[int]:
    """Involutive bit-swap across sequence."""
    return [flip_token(b) for b in s]


def le_seq(s1: Sequence[int], s2: Sequence[int]) -> bool:
    """Lexicographic comparison of token sequences."""
    return list(s1) <= list(s2)


def canon_seq(s: Sequence[int]) -> list[int]:
    """Canonical representative under Presentation bit-swap."""
    flipped = flip_seq(s)
    return list(s) if le_seq(s, flipped) else flipped


@dataclass(frozen=True)
class ScaleRegime:
    """A finite regime at scale depth with presentation tokens."""

    depth: int
    tokens: tuple[int, ...]

    def __post_init__(self) -> None:
        if len(self.tokens) != self.depth:
            raise ValueError(
                f"tokens length ({len(self.tokens)}) must equal depth ({self.depth})"
            )
        for t in self.tokens:
            if t not in (0, 1):
                raise ValueError(f"token {t} not in {{0, 1}}")

    @property
    def canonical_tokens(self) -> tuple[int, ...]:
        return tuple(canon_seq(self.tokens))


def is_isomorphic(r1: ScaleRegime, r2: ScaleRegime) -> bool:
    """Canonical isomorphism: identical scale depth and identical canonical keys."""
    return r1.depth == r2.depth and r1.canonical_tokens == r2.canonical_tokens


def prefix_k(k: int, s: Sequence[int]) -> tuple[int, ...]:
    """Prefix truncation at resolution depth k."""
    return tuple(s[:k])


@dataclass(frozen=True)
class Observer:
    """A finite observer at resolution depth k."""

    resolution_depth: int
    signature_map: Callable[[tuple[int, ...]], int]

    def __call__(self, r: ScaleRegime) -> int:
        return eval_observer(self, r)


def eval_observer(observer: Observer, regime: ScaleRegime) -> int:
    """Evaluate observer on scale regime through canonical prefix truncation."""
    canonical_trunc = prefix_k(
        observer.resolution_depth, regime.canonical_tokens
    )
    sig = observer.signature_map(canonical_trunc)
    bound = 2**observer.resolution_depth
    if not (0 <= sig < bound):
        raise ValueError(
            f"observer signature {sig} out of bound [0, {bound})"
        )
    return sig


def observer_equiv(observer: Observer, r1: ScaleRegime, r2: ScaleRegime) -> bool:
    """Observer equivalence: indistinguishability under evaluation."""
    return eval_observer(observer, r1) == eval_observer(observer, r2)


def compose_higher_order(
    observers: Sequence[Observer],
    aggregator: Callable[[Sequence[int]], int],
    resolution_depth: int,
) -> Observer:
    """Compose higher-order observer from lower-order evaluation traces."""

    def composite_signature(trunc: tuple[int, ...]) -> int:
        traces = [obs.signature_map(trunc[: obs.resolution_depth]) for obs in observers]
        return aggregator(traces)

    return Observer(
        resolution_depth=resolution_depth,
        signature_map=composite_signature,
    )
