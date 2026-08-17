"""Evaluation returns a set. Reporting one element is a selection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Report:
    chosen: object
    declared: bool
    pool_size: int

    @property
    def unauthorized(self) -> bool:
        return self.pool_size > 1 and not self.declared


def evaluate_set(options: FrozenSet[T]) -> FrozenSet[T]:
    if not options:
        raise ValueError("evaluation of the empty set is undefined")
    return frozenset(options)


def report_one(options: FrozenSet[T], pick: T, *, declare: bool) -> Report:
    pool = evaluate_set(options)
    if pick not in pool:
        raise ValueError("pick is not in the evaluated set")
    return Report(chosen=pick, declared=declare, pool_size=len(pool))
