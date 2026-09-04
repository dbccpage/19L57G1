"""Observable functions for the frozen second-stake rule class.

The sealed regime is imported read-only.  Each function here is metatheory
apparatus: it computes a value from the current admitted state and a held pair.
"""

from __future__ import annotations

import pathlib
import sys
from functools import lru_cache
from itertools import permutations
from typing import Iterator, Sequence

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _path in (REPO / "code", REPO / "research" / "identification_dual"):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from derivation.iso import rename  # noqa: E402
from derivation.model import Pair, Regime  # noqa: E402
from derivation.observe import profiles  # noqa: E402
from dual import State, automorphisms  # noqa: E402

OBSERVABLE_IDS: tuple[str, ...] = ("O1", "O2", "O3", "O4", "O5", "O6")


class ObservableGuardError(RuntimeError):
    """The pinned exact observable exceeded its declared finite guard."""


def structural_regime(regime: Regime) -> Regime:
    """Erase presentation-token spelling, which no frozen observable reads."""

    return Regime(
        tuple(f"d{index}" for index in range(regime.n_data())),
        regime.forms,
        regime.insts,
        regime.rules,
        regime.reqs,
    )


@lru_cache(maxsize=None)
def _profile_table(regime: Regime) -> tuple[frozenset[tuple[int, tuple[int | None, ...]]], ...]:
    return profiles(regime)


def profile_table(regime: Regime) -> tuple[frozenset[tuple[int, tuple[int | None, ...]]], ...]:
    return _profile_table(structural_regime(regime))


def held_pairs(regime: Regime) -> tuple[Pair, ...]:
    """All unordered held pairs in deterministic order."""

    return tuple(
        (i, j)
        for i in range(regime.n_data())
        for j in range(i + 1, regime.n_data())
    )


def checked_pair(regime: Regime, i: int, j: int) -> Pair:
    """Return an ordered held pair, rejecting diagonals and absent data."""

    lo, hi = (i, j) if i < j else (j, i)
    if lo < 0 or lo == hi or hi >= regime.n_data():
        raise ValueError(f"not a held pair: ({i}, {j})")
    return (lo, hi)


def profile_equal(regime: Regime, i: int, j: int) -> bool:
    pair = checked_pair(regime, i, j)
    values = profile_table(regime)
    return values[pair[0]] == values[pair[1]]


def profile_empty(regime: Regime, datum: int) -> bool:
    if not 0 <= datum < regime.n_data():
        raise ValueError(f"datum is not held: {datum}")
    return not profile_table(regime)[datum]


def profile_size(regime: Regime, datum: int) -> int:
    if not 0 <= datum < regime.n_data():
        raise ValueError(f"datum is not held: {datum}")
    return len(profile_table(regime)[datum])


def class_count(regime: Regime) -> int:
    return len(set(profile_table(regime)))


def requirement_member(regime: Regime, i: int, j: int) -> bool:
    return checked_pair(regime, i, j) in regime.reqs


@lru_cache(maxsize=None)
def _regime_automorphisms(regime: Regime) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    """Every datum/form bijection fixing the full sealed regime."""

    state = State(regime, frozenset(), "stake")
    try:
        return tuple(automorphisms(state))
    except RuntimeError as exc:
        raise ObservableGuardError(str(exc)) from exc


def regime_automorphisms(regime: Regime) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    return _regime_automorphisms(structural_regime(regime))


def one_orbit(regime: Regime, i: int, j: int) -> bool:
    """Whether an automorphism carries either member of the pair to the other."""

    lo, hi = checked_pair(regime, i, j)
    return any(pi[lo] == hi for pi, _ in regime_automorphisms(regime))


def datum_permutations(regime: Regime) -> Iterator[tuple[int, ...]]:
    yield from permutations(range(regime.n_data()))


def form_permutations(regime: Regime) -> Iterator[tuple[int, ...]]:
    yield from permutations(range(len(regime.forms)))


def renamed(regime: Regime, pi: Sequence[int], phi: Sequence[int]) -> Regime:
    return rename(regime, pi, phi)


def observable_record(regime: Regime, pair: Pair) -> dict[str, object]:
    """Machine-readable values of every frozen observable for one pair."""

    i, j = checked_pair(regime, *pair)
    return {
        "O1": profile_equal(regime, i, j),
        "O2": [profile_empty(regime, i), profile_empty(regime, j)],
        "O3": [profile_size(regime, i), profile_size(regime, j)],
        "O4": one_orbit(regime, i, j),
        "O5": class_count(regime),
        "O6": requirement_member(regime, i, j),
    }
