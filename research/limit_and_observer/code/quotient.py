"""The isomorphism quotient on stated states, and the equivariant pair policy.

Classification: metatheory apparatus.

The canonical key is the minimum serialization over **all** bijection pairs on
data and forms — the brute-force minimum.  It is used rather than the sealed
colour-refined key because this tree's regimes are small enough that the
factorial minimum is cheap, and because a brute-force minimum has no
refinement to get wrong.  A test asserts that its equality relation agrees
with the sealed refined ``canonical`` over the whole population.

Presentation tokens are deliberately forgotten, exactly as in the seal.
"""

from __future__ import annotations

from itertools import permutations
from math import factorial
from typing import Iterable, Sequence, TypeVar

from .grammar import Context
from .items import StatedState
from .readers import Reader, reading_class
from .regime import Pair, Regime

T = TypeVar("T")

CanonKey = tuple[object, ...]


class BijectionBudgetRefused(RuntimeError):
    """Named terminal: the bijection count exceeds the declared budget.

    Refused rather than truncated."""


def _budget_check(r: Regime, budget: int) -> None:
    total = factorial(r.n_data()) * factorial(len(r.forms))
    if total > budget:
        raise BijectionBudgetRefused(
            f"{total} candidate bijections exceed the declared budget {budget}"
        )


def transport_context(
    c: Context, pi: Sequence[int], phi: Sequence[int]
) -> Context:
    f, slots = c
    return (phi[f], tuple(None if s is None else pi[s] for s in slots))


def serialize_regime(
    r: Regime, pi: Sequence[int], phi: Sequence[int]
) -> CanonKey:
    """A regime under a bijection pair, with presentation tokens forgotten."""
    forms = [0] * len(r.forms)
    for f, arity in enumerate(r.forms):
        forms[phi[f]] = arity
    insts = sorted(
        (phi[f], tuple(pi[a] for a in args)) for (f, args) in r.insts
    )
    rules = sorted(phi[f] for f in r.rules)
    reqs = sorted(
        (min(pi[i], pi[j]), max(pi[i], pi[j])) for (i, j) in r.reqs
    )
    return (r.n_data(), tuple(forms), tuple(insts), tuple(rules), tuple(reqs))


def serialize_reader(
    rho: Reader, pi: Sequence[int], phi: Sequence[int]
) -> CanonKey:
    """A reader under a bijection pair.

    The reading enters through its complement class, as frozen in section 7.
    Equal separation behaviours need not be the same transported reader;
    relation agreement does not erase this field from OBS-4."""
    sel = sorted(
        flatten_context(transport_context(c, pi, phi))
        for c in rho.selection
    )
    return (reading_class(rho.reading), tuple(rho.aggregation), tuple(sel))


def flatten_context(c: Context) -> tuple[int, tuple[int, ...]]:
    """A context with its holes written as -1, so that every serialized key
    is totally ordered by the built-in comparison.  A hole and a datum index
    are never confused: -1 is not a datum index."""
    return (c[0], tuple(-1 if s is None else s for s in c[1]))


def serialize_state(
    s: StatedState, pi: Sequence[int], phi: Sequence[int]
) -> CanonKey:
    return (
        serialize_regime(s.regime, pi, phi),
        tuple(sorted(serialize_reader(rho, pi, phi) for rho in s.readers)),
    )


def canonical_state(s: StatedState, budget: int = 100_000) -> CanonKey:
    """The canonical key of a stated state."""
    _budget_check(s.regime, budget)
    n, nf = s.regime.n_data(), len(s.regime.forms)
    return min(
        serialize_state(s, pi, phi)
        for pi in permutations(range(n))
        for phi in permutations(range(nf))
    )


def canonical_regime(r: Regime, budget: int = 100_000) -> CanonKey:
    _budget_check(r, budget)
    n, nf = r.n_data(), len(r.forms)
    return min(
        serialize_regime(r, pi, phi)
        for pi in permutations(range(n))
        for phi in permutations(range(nf))
    )


_AUTO_CACHE: dict[object, list[tuple[tuple[int, ...], tuple[int, ...]]]] = {}


def automorphisms(
    r: Regime, budget: int = 100_000
) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """Every bijection pair under which the renamed regime equals itself.

    Memoised on the regime.  The function is pure and its result is never
    mutated by a caller, so the cache changes nothing about what is computed;
    it exists because the anti-renaming guard asks for the automorphisms of
    the same regime once per candidate."""
    hit = _AUTO_CACHE.get((r, budget))
    if hit is not None:
        return hit
    _budget_check(r, budget)
    n, nf = r.n_data(), len(r.forms)
    identity = serialize_regime(r, tuple(range(n)), tuple(range(nf)))
    out = [
        (pi, phi)
        for pi in permutations(range(n))
        for phi in permutations(range(nf))
        if serialize_regime(r, pi, phi) == identity
    ]
    _AUTO_CACHE[(r, budget)] = out
    return out


def pair_orbits(
    r: Regime, pairs: Sequence[Pair], budget: int = 100_000
) -> tuple[tuple[Pair, ...], ...]:
    """Orbits of unordered data pairs under the automorphism group.

    Selecting one representative per orbit is the equivariant policy that
    replaced least-pair selection in the seal, because least-pair depends on
    the representative labelling."""
    autos = automorphisms(r, budget)
    remaining = set(pairs)
    out: list[tuple[Pair, ...]] = []
    for p in sorted(pairs):
        if p not in remaining:
            continue
        orbit = set()
        for pi, _ in autos:
            q = (min(pi[p[0]], pi[p[1]]), max(pi[p[0]], pi[p[1]]))
            if q in remaining:
                orbit.add(q)
        orbit.add(p)
        remaining -= orbit
        out.append(tuple(sorted(orbit)))
    return tuple(out)


def designated_pair(r: Regime, pairs: Sequence[Pair]) -> Pair | None:
    """One representative per automorphism orbit, least orbit first.

    Fixed **before** any enumeration; never chosen after seeing one."""
    orbits = pair_orbits(r, pairs)
    return orbits[0][0] if orbits else None


def group_by_key(
    items: Iterable[tuple[StatedState, T]], budget: int = 100_000
) -> dict[CanonKey, list[T]]:
    out: dict[CanonKey, list[T]] = {}
    for state, payload in items:
        out.setdefault(canonical_state(state, budget), []).append(payload)
    return out
