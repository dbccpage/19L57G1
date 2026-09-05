"""Enumeration of the candidate space: sealed prefixes and reader suffixes.

Classification: admitted primitive of this rung (the widened item bound and
its enumerator); deterministic computation (everything else).

Following ``research/second_stream``, the widened space is **this rung's own
admitted primitive** and is never called the sealed candidate space at that
width.  The prefix enumerator is certified by set equality against an
independently written superset construction one coordinate wider in each
direction.

The sealed ``iter_cost2_deltas`` is never used: its four pruning lemmas are
justified against pair separation and none of this tree's demands is pair
separation.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Iterator

from .grammar import Context, admission_bit, contexts, coverage_bit
from .items import (
    AddContext,
    Delta,
    Item,
    NewDatum,
    NewForm,
    NewInst,
    NewReader,
    NewRuleAll,
    StatedState,
    apply_delta,
    canonical_delta,
)
from .readers import (
    Reading,
    all_reading_classes,
    behaviour,
    lawful_aggregations,
    reads_at,
)
from .regime import AdmissionRefused, Regime


class CandidateBudgetRefused(RuntimeError):
    """Named terminal: an enumeration exceeded its declared candidate budget.

    Refused rather than truncated."""


@dataclass(frozen=True)
class Bounds:
    """The declared finite bounds.  Each is refused rather than exceeded."""

    max_items: int = 8
    max_sealed_items: int = 4
    max_reader_items: int = 4
    max_arity: int = 2
    w_max: int = 3
    max_readers: int = 2
    bijection_budget: int = 100_000
    candidate_budget: int = 4_000_000


DEFAULT_BOUNDS = Bounds()


def iter_sealed_items(base: Regime, bounds: Bounds) -> Iterator[Item]:
    """The sealed one-item alphabet over a base, re-implemented."""
    yield NewDatum()
    for arity in range(1, bounds.max_arity + 1):
        yield NewForm(arity)
    for f in sorted(set(range(len(base.forms))) - set(base.rules)):
        yield NewRuleAll(f)
    for f, arity in enumerate(base.forms):
        for args in itertools.product(range(base.n_data()), repeat=arity):
            yield NewInst(f, tuple(args))


def _apply_sealed(base: Regime, delta: Delta, bounds: Bounds) -> Regime:
    return apply_delta(
        StatedState(base, ()), delta, bounds.w_max, bounds.max_readers
    ).regime


_PREFIX_CACHE: dict[tuple[object, int, object], dict[Delta, Regime]] = {}


def sealed_prefixes(
    base: Regime, k: int, bounds: Bounds
) -> dict[Delta, Regime]:
    """Every valid canonical delta of exactly ``k`` sealed items.

    Built by breadth over one-item moves.  Certified against
    ``superset_prefixes`` by set equality in the tests.

    Memoised on ``(base, k, bounds)``.  The function is pure and its result is
    never mutated by a caller, so the cache changes nothing about what is
    enumerated; it exists because the pricing routine asks for the same
    prefixes once per demand, measure and item count."""
    key = (base, k, bounds)
    hit = _PREFIX_CACHE.get(key)
    if hit is not None:
        return hit
    if k > bounds.max_sealed_items:
        raise CandidateBudgetRefused(
            f"sealed prefix of {k} items exceeds the declared bound "
            f"{bounds.max_sealed_items}"
        )
    current: dict[Delta, Regime] = {(): base}
    for _ in range(k):
        nxt: dict[Delta, Regime] = {}
        for path, r in current.items():
            for it in iter_sealed_items(r, bounds):
                try:
                    child = _apply_sealed(base, canonical_delta(path + (it,)),
                                          bounds)
                except AdmissionRefused:
                    continue
                nxt[canonical_delta(path + (it,))] = child
        current = nxt
        if len(current) > bounds.candidate_budget:
            raise CandidateBudgetRefused(
                f"{len(current)} prefixes exceed the declared budget"
            )
    _PREFIX_CACHE[key] = current
    return current


def superset_prefixes(
    base: Regime, k: int, bounds: Bounds
) -> dict[Delta, Regime]:
    """An independently written construction, one coordinate wider in each
    direction, filtered by validity.

    It does not descend through one-item moves: it builds a universe of items
    over form indices and datum indices each widened by ``k``, takes every
    multiset of size ``k``, and keeps the ones that replay.  Set equality with
    ``sealed_prefixes`` is what certifies the latter."""
    n0 = base.n_data()
    universe: list[Item] = [NewDatum()]
    for arity in range(1, bounds.max_arity + 1):
        universe.append(NewForm(arity))
    max_form = len(base.forms) + k
    arities = [bounds.max_arity, *base.forms]
    for f in range(max_form):
        universe.append(NewRuleAll(f))
        for arity in range(1, max(arities) + 1):
            for args in itertools.product(range(n0 + k), repeat=arity):
                universe.append(NewInst(f, tuple(args)))
    out: dict[Delta, Regime] = {}
    for combo in itertools.combinations_with_replacement(universe, k):
        delta = canonical_delta(tuple(combo))
        if delta in out:
            continue
        if not admissible_shape(base, delta):
            continue
        try:
            out[delta] = _apply_sealed(base, delta, bounds)
        except AdmissionRefused:
            continue
    return out


def admissible_shape(base: Regime, delta: Delta) -> bool:
    """An exact restatement of the sealed offer condition for rule items.

    The sealed ``iter_cost1_items`` offers ``NewRuleAll(f)`` only for a form
    ``f`` that is **not already ruled**, so no path applies the same rule
    twice and no path rules a form the base already rules.  Replay alone does
    not catch this, because admitting a rule is idempotent on the regime.

    This condition was not written in advance: the set-equality certification
    against ``superset_prefixes`` found the divergence, at three items, in
    reading L.  Restating the sealed condition exactly is the repair; silently
    widening the space to include a doubled rule item would have been the
    other one, and would have made every count in this tree wrong by the size
    of a redundancy class."""
    ruled: list[int] = []
    for it in delta:
        if isinstance(it, NewRuleAll):
            if it.form in base.rules or it.form in ruled:
                return False
            ruled.append(it.form)
    return True


def inert_context(r: Regime, b: Reading, c: Context) -> bool:
    """Whether a context contributes nothing to any reader with this reading.

    Two ways to be inert: the reading does not vary at the context's coverage
    bit, or the admission bit is constant across every datum there.  Adding an
    inert context leaves every separating count unchanged, so it leaves the
    induced relation identical while costing one item — hence no *minimum*
    candidate contains one.  The pruning is therefore sound for minima and for
    below-minimum exhaustion alike, and ``tests/test_enumeration.py`` checks
    it against the unpruned enumeration."""
    if not reads_at(b, coverage_bit(r, c)):
        return True
    vals = {admission_bit(r, c, d) for d in range(r.n_data())}
    return len(vals) <= 1


def reader_suffixes(
    r: Regime, s: int, bounds: Bounds, prune: bool = True
) -> Iterator[Delta]:
    """Every reader suffix of exactly ``s`` items over the regime.

    ``s`` items buy ``nr`` readers and ``s - nr`` contexts, each context its
    own item.  Readings are enumerated by behaviour representative, which is
    elimination by proof: the induced relation depends on the reading only
    through its behaviour."""
    if s == 0:
        yield ()
        return
    if s > bounds.max_reader_items:
        return
    ctx = contexts(r)
    aggs = lawful_aggregations(bounds.w_max)
    readings = _behaviour_representatives()
    # A canonical delta is the candidate, and two orderings of the same reader
    # specifications sort to one delta.  Deduping here is what keeps the raw
    # minima a set, which the harness invariants require.
    emitted: set[Delta] = set()
    for nr in range(1, min(bounds.max_readers, s) + 1):
        for widths in _compositions(s - nr, nr, bounds.w_max):
            for specs in itertools.product(
                *[list(itertools.product(readings, aggs))] * nr
            ):
                items: list[Item] = []
                ok = True
                for idx in range(nr):
                    b, a = specs[idx]
                    items.append(NewReader(b, a))
                    pool = [
                        c for c in ctx
                        if not (prune and inert_context(r, b, c))
                    ]
                    if len(pool) < widths[idx]:
                        ok = False
                        break
                if not ok:
                    continue
                pools = [
                    [
                        c for c in ctx
                        if not (prune and inert_context(r, specs[i][0], c))
                    ]
                    for i in range(nr)
                ]
                for chosen in itertools.product(
                    *[
                        list(itertools.combinations(pools[i], widths[i]))
                        for i in range(nr)
                    ]
                ):
                    add: list[Item] = []
                    for idx in range(nr):
                        for c in chosen[idx]:
                            add.append(AddContext(idx, c))
                    out = canonical_delta(tuple(items) + tuple(add))
                    if out in emitted:
                        continue
                    emitted.add(out)
                    yield out


def _behaviour_representatives() -> tuple[Reading, ...]:
    """One reading per induced-separation behaviour, deterministically."""
    seen: dict[tuple[bool, bool], Reading] = {}
    for b in all_reading_classes():
        seen.setdefault(behaviour(b), b)
    return tuple(seen[k] for k in sorted(seen))


def _compositions(total: int, parts: int, cap: int) -> Iterator[tuple[int, ...]]:
    """Every way to split ``total`` context items among ``parts`` readers,
    none exceeding the declared width."""
    if parts == 1:
        if 0 <= total <= cap:
            yield (total,)
        return
    for first in range(0, min(cap, total) + 1):
        for rest in _compositions(total - first, parts - 1, cap):
            yield (first,) + rest


def iter_candidates(
    base: Regime, total: int, bounds: Bounds, prune: bool = True
) -> Iterator[tuple[Delta, StatedState]]:
    """Every valid candidate of exactly ``total`` items at a base.

    Two stages: a sealed prefix, then reader suffixes over the *resulting*
    regime.  Cost is measured on the whole delta."""
    if total > bounds.max_items:
        raise CandidateBudgetRefused(
            f"{total} items exceeds the declared bound {bounds.max_items}"
        )
    seen = 0
    for p in range(0, min(bounds.max_sealed_items, total) + 1):
        s = total - p
        if s > bounds.max_reader_items:
            continue
        for prefix, regime in sealed_prefixes(base, p, bounds).items():
            for suffix in reader_suffixes(regime, s, bounds, prune):
                delta = canonical_delta(prefix + suffix)
                try:
                    state = apply_delta(
                        StatedState(base, ()), delta,
                        bounds.w_max, bounds.max_readers,
                    )
                except AdmissionRefused:  # pragma: no cover - shapes are valid
                    continue
                seen += 1
                if seen > bounds.candidate_budget:
                    raise CandidateBudgetRefused(
                        f"enumeration exceeded the declared candidate budget "
                        f"{bounds.candidate_budget}"
                    )
                yield delta, state
