"""The frozen menu of state-reading stake rules and its controls."""

from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Literal, cast

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _path in (
    REPO / "code",
    REPO / "research" / "identification_dual",
    REPO / "research" / "two_sided_commitment",
):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from derivation.model import Pair, Regime  # noqa: E402
from two_sided import (  # noqa: E402
    APART,
    FREE,
    SAME,
    commitment_named,
    honoured,
)

from observables import (  # noqa: E402
    checked_pair,
    class_count,
    held_pairs,
    one_orbit,
    profile_empty,
    profile_equal,
    profile_size,
    requirement_member,
)

Label = Literal["apart", "same", "free"]
Labeler = Callable[[Regime, int, int], Label]


@dataclass(frozen=True)
class StakeRule:
    """One total rule in the frozen menu or control set."""

    name: str
    observables: tuple[str, ...]
    labeler: Labeler
    source: Literal["menu", "control"]
    index_reading: bool = False

    @property
    def capability_count(self) -> int:
        return len(set(self.observables))

    def label(self, regime: Regime, i: int, j: int) -> Label:
        lo, hi = checked_pair(regime, i, j)
        value = self.labeler(regime, lo, hi)
        if value not in (APART, SAME, FREE):
            raise ValueError(f"rule {self.name} returned {value!r}")
        return value


@lru_cache(maxsize=None)
def label_of(rule: StakeRule, regime: Regime, i: int, j: int) -> Label:
    return rule.label(regime, i, j)


def _e1(regime: Regime, i: int, j: int) -> Label:
    return cast(Label, SAME if profile_equal(regime, i, j) else APART)


def _e2(regime: Regime, i: int, j: int) -> Label:
    both_empty = profile_empty(regime, i) and profile_empty(regime, j)
    return cast(Label, SAME if both_empty else APART)


def _e3(regime: Regime, i: int, j: int) -> Label:
    return cast(Label, SAME if one_orbit(regime, i, j) else APART)


def _e4(regime: Regime, i: int, j: int) -> Label:
    return cast(Label, APART if one_orbit(regime, i, j) else SAME)


def _e5(regime: Regime, i: int, j: int) -> Label:
    return cast(Label, APART if profile_size(regime, i) != profile_size(regime, j) else SAME)


def _e6(regime: Regime, i: int, j: int) -> Label:
    selected = one_orbit(regime, i, j) and profile_size(regime, i) == profile_size(regime, j)
    return cast(Label, SAME if selected else FREE)


def _e7(regime: Regime, i: int, j: int) -> Label:
    exactly_one = profile_empty(regime, i) != profile_empty(regime, j)
    return cast(Label, APART if exactly_one else FREE)


def _e8(regime: Regime, i: int, j: int) -> Label:
    return cast(Label, APART if requirement_member(regime, i, j) else FREE)


def _e9(regime: Regime, i: int, j: int) -> Label:
    return cast(Label, SAME if class_count(regime) == 1 else APART)


MENU: tuple[StakeRule, ...] = (
    StakeRule("E1", ("O1",), _e1, "menu"),
    StakeRule("E2", ("O2",), _e2, "menu"),
    StakeRule("E3", ("O4",), _e3, "menu"),
    StakeRule("E4", ("O4",), _e4, "menu"),
    StakeRule("E5", ("O3",), _e5, "menu"),
    StakeRule("E6", ("O3", "O4"), _e6, "menu"),
    StakeRule("E7", ("O2",), _e7, "menu"),
    StakeRule("E8", ("O6",), _e8, "menu"),
    StakeRule("E9", ("O5",), _e9, "menu"),
)


def _control(name: str, index_reading: bool) -> StakeRule:
    commitment = commitment_named(name)

    def labeler(regime: Regime, i: int, j: int) -> Label:
        del regime
        return cast(Label, commitment.label(i, j))

    return StakeRule(name, (), labeler, "control", index_reading)


CONTROLS: tuple[StakeRule, ...] = (
    _control("total_apart", False),
    _control("total_same", False),
    _control("parity", True),
    _control("residue_three", True),
    _control("chain", True),
)

ALL_RULES: tuple[StakeRule, ...] = MENU + CONTROLS


def rule_named(name: str) -> StakeRule:
    for rule in ALL_RULES:
        if rule.name == name:
            return rule
    raise KeyError(name)


def labelled_pairs(regime: Regime, rule: StakeRule) -> tuple[tuple[Label, Pair], ...]:
    return tuple(
        (label, pair)
        for pair in held_pairs(regime)
        if (label := label_of(rule, regime, *pair)) != FREE
    )


def demands(regime: Regime, rule: StakeRule) -> tuple[tuple[Label, Pair], ...]:
    """Every currently labelled pair that the sealed honour relation rejects."""

    return tuple(
        (label, pair)
        for label, pair in labelled_pairs(regime, rule)
        if not honoured(regime, label, pair)
    )


def honoured_labelled_pairs(regime: Regime, rule: StakeRule) -> tuple[tuple[Label, Pair], ...]:
    return tuple(
        (label, pair)
        for label, pair in labelled_pairs(regime, rule)
        if honoured(regime, label, pair)
    )


def label_map(regime: Regime, rule: StakeRule) -> tuple[tuple[Pair, Label], ...]:
    return tuple((pair, label_of(rule, regime, *pair)) for pair in held_pairs(regime))
