"""Executable mirror of the local finite-alphabet G1 class.

Classification: deterministic computation and metatheory apparatus.  The
general exclusion is proved in ``Derivation.LocalStrategy``; computations in
this module are explicitly bounded checks and concrete witnesses.  A
``LocalStrategy`` is local by construction: its view is obtained by applying
one fixed factor function to one fixed-radius colour ball.  A finite alphabet
bound and the import discipline are separate data.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

from derivation.export import Json
from derivation.generator import Profile1, profile1

DEFAULT_MAX_CHAIN = 15

Colour = Callable[[int, int], int]
Factor = Callable[[tuple[int, ...]], int]
CandidateView = Callable[[int, int], int]


class ImportDiscipline(str, Enum):
    ONE_TIME = "one_time"
    RECURRING = "recurring"


def ball(i: int, radius: int) -> tuple[int, ...]:
    """Lean's fixed-length natural-number ball ``i - d + k``."""
    if i < 0 or radius < 0:
        raise ValueError("point and radius must be nonnegative")
    left = max(0, i - radius)
    return tuple(left + k for k in range(2 * radius + 1))


def encode(base: int, values: tuple[int, ...]) -> int:
    """The little-endian positional encoding from ``CapacityBound``."""
    if base < 0 or any(value < 0 for value in values):
        raise ValueError("base and values must be nonnegative")
    result = 0
    place = 1
    for value in values:
        result += place * value
        place *= base
    return result


def profile_code(value: Profile1) -> int:
    return int(value[0]) + 2 * int(value[1]) + 4 * int(value[2])


@dataclass(frozen=True)
class LocalStrategy:
    name: str
    radius: int
    import_discipline: ImportDiscipline
    alphabet_size: Optional[int]
    colour: Colour
    factor: Factor

    def __post_init__(self) -> None:
        if self.radius < 0:
            raise ValueError("radius must be nonnegative")
        if self.alphabet_size is not None and self.alphabet_size <= 0:
            raise ValueError("a declared alphabet must be nonempty")

    def colour_ball(self, n: int, i: int) -> tuple[int, ...]:
        return tuple(self.colour(n, point) for point in ball(i, self.radius))

    def view(self, n: int, i: int) -> int:
        return self.factor(self.colour_ball(n, i))


def _profile_colour(n: int, i: int) -> int:
    return profile_code(profile1(n, i))


def _identity_colour(_n: int, i: int) -> int:
    return i


def _head(values: tuple[int, ...]) -> int:
    return values[0]


def _depth_two_factor(values: tuple[int, ...]) -> int:
    return encode(8, values)


BARE = LocalStrategy(
    "none", 0, ImportDiscipline.ONE_TIME, 8, _profile_colour, _head
)
PRESENCE = LocalStrategy(
    "automark_presence",
    0,
    ImportDiscipline.ONE_TIME,
    8,
    _profile_colour,
    _head,
)
DEPTH_TWO = LocalStrategy(
    "depth2",
    1,
    ImportDiscipline.ONE_TIME,
    8,
    _profile_colour,
    _depth_two_factor,
)
PER_PAIR = LocalStrategy(
    "per_pair_fresh_mark",
    0,
    ImportDiscipline.RECURRING,
    None,
    _identity_colour,
    _head,
)
VALUED = LocalStrategy(
    "automark_valued",
    0,
    ImportDiscipline.ONE_TIME,
    None,
    _identity_colour,
    _head,
)

STRATEGIES = (BARE, PER_PAIR, PRESENCE, VALUED, DEPTH_TWO)


def base_obstructions(n: int) -> tuple[tuple[int, int], ...]:
    if n < 0:
        raise ValueError("chain length must be nonnegative")
    return tuple(
        (i, j)
        for i in range(n + 1)
        for j in range(i + 1, n + 1)
        if profile1(n, i) == profile1(n, j)
    )


def fires_within(strategy: LocalStrategy, max_chain: int) -> bool:
    """Whether the inherited pre-repair view fires in the stated bound."""
    if max_chain < 0:
        raise ValueError("bound must be nonnegative")
    _ = strategy
    return any(base_obstructions(n) for n in range(max_chain + 1))


def clears_within(strategy: LocalStrategy, max_chain: int) -> bool:
    """Bounded mirror of ``Clears``; never promoted to the general proof."""
    if max_chain < 0:
        raise ValueError("bound must be nonnegative")
    return all(
        strategy.view(n, i) != strategy.view(n, j)
        for n in range(max_chain + 1)
        for i, j in base_obstructions(n)
    )


def identity_grade_within(strategy: LocalStrategy, max_chain: int) -> bool:
    if max_chain < 0:
        raise ValueError("bound must be nonnegative")
    return all(
        strategy.view(n, i) != strategy.view(n, j)
        for n in range(max_chain + 1)
        for i in range(n + 1)
        for j in range(i + 1, n + 1)
    )


def finite_declaration_within(
    strategy: LocalStrategy, max_chain: int
) -> bool:
    """Check the declared bound on carrier points through ``max_chain``."""
    if max_chain < 0:
        raise ValueError("bound must be nonnegative")
    if strategy.alphabet_size is None:
        return False
    return all(
        0 <= strategy.colour(n, i) < strategy.alphabet_size
        for n in range(max_chain + 1)
        for i in range(n + 1)
    )


def finite_factor_table(
    radius: int,
    colour: Colour,
    candidate_view: CandidateView,
    max_chain: int,
) -> Optional[dict[tuple[int, ...], int]]:
    """Find a bounded factor table, or reject a fiber-inconsistent view.

    This is the executable negative test for the unconstrained-view trap.
    It is a finite check only; class members instead carry the factor by
    construction.
    """
    if radius < 0 or max_chain < 0:
        raise ValueError("radius and bound must be nonnegative")
    table: dict[tuple[int, ...], int] = {}
    for n in range(max_chain + 1):
        for i in range(n + 1):
            key = tuple(colour(n, point) for point in ball(i, radius))
            value = candidate_view(n, i)
            previous = table.get(key)
            if previous is not None and previous != value:
                return None
            table[key] = value
    return table


def capacity_threshold(strategy: LocalStrategy) -> Optional[int]:
    if strategy.alphabet_size is None:
        return None
    k = strategy.alphabet_size
    d = strategy.radius
    return int(k ** (2 * d + 1) + 2 * d + 2)


def capacity_collision(strategy: LocalStrategy) -> Optional[tuple[int, int]]:
    """Concrete collision at the theorem's exact threshold, when finite."""
    threshold = capacity_threshold(strategy)
    if threshold is None:
        return None
    seen: dict[int, int] = {}
    for i in range(strategy.radius + 1, threshold - strategy.radius):
        value = strategy.view(threshold, i)
        if value in seen:
            return seen[value], i
        seen[value] = i
    return None


def classification(strategy: LocalStrategy, max_chain: int) -> str:
    clears = clears_within(strategy, max_chain)
    identity = identity_grade_within(strategy, max_chain)
    if strategy.import_discipline is ImportDiscipline.RECURRING and clears:
        return "repairs_by_recurring_imports"
    if strategy.import_discipline is ImportDiscipline.ONE_TIME and identity:
        return "generation_dead"
    if fires_within(strategy, max_chain) and not clears:
        return "fires_unrepaired"
    return "bounded_other"


def artifact_payload(max_chain: int = DEFAULT_MAX_CHAIN) -> dict[str, Json]:
    if max_chain < 5:
        raise ValueError("the declared check bound must include depth-two firing")
    rows: list[dict[str, Json]] = []
    capacity_rows: list[dict[str, Json]] = []
    for strategy in STRATEGIES:
        collision = capacity_collision(strategy)
        rows.append(
            {
                "name": strategy.name,
                "radius": strategy.radius,
                "alphabet_size": strategy.alphabet_size,
                "import_discipline": strategy.import_discipline.value,
                "finite_declaration_within_bound": finite_declaration_within(
                    strategy, max_chain
                ),
                "fires_within_bound": fires_within(strategy, max_chain),
                "clears_within_bound": clears_within(strategy, max_chain),
                "identity_grade_within_bound": identity_grade_within(
                    strategy, max_chain
                ),
                "classification": classification(strategy, max_chain),
            }
        )
        if strategy.alphabet_size is not None:
            capacity_rows.append(
                {
                    "name": strategy.name,
                    "threshold": capacity_threshold(strategy),
                    "collision": list(collision) if collision else None,
                }
            )
    rejected = finite_factor_table(
        0, lambda _n, _i: 0, lambda _n, i: i, max_chain
    )
    return {
        "bounds": {
            "finite_checks_max_chain": max_chain,
            "strategy_class_size": len(STRATEGIES),
        },
        "class": {
            "locality": "view factors through one fixed-radius colour ball",
            "finite_declaration": (
                "one fixed alphabet bound independent of chain length"
            ),
            "lean_theorems": [
                "LocalFiniteAlphabet.strategy_capacity_collision",
                "LocalFiniteAlphabet.finite_local_not_clears",
                "LocalFiniteAlphabet.g1_local_finite_alphabet_class",
            ],
        },
        "strategies": rows,
        "capacity_witnesses": capacity_rows,
        "negative_locality_probe": {
            "constant_colour_identity_view_accepted": rejected is not None,
            "reason": "same radius-zero colour ball receives two view values",
        },
        "terminals": {
            "g1": "G1_CLASS_EXCLUSION_PROVED",
            "object_language": "OBJECT_LANGUAGE_GENERATOR_NOT_IN_SCOPE",
            "closure_policy": "OB1_UNCHANGED",
        },
    }
