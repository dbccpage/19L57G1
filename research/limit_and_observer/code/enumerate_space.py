"""Enumeration of the candidate space: sealed prefixes and reader suffixes.

Classification: admitted primitive of this rung (the widened item bound and
its enumerator); deterministic computation (everything else).

Following ``research/second_stream``, the widened space is **this rung's own
admitted primitive** and is never called the sealed candidate space at that
width. At both genesis bases the prefix enumerator is certified by exact
delta-to-child equality through four items against an independent grouped
construction with widened coordinate pools (tests/test_prefix_certificate.py).
The shared replay semantics remain a separate correspondence obligation.

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
    lawful_aggregations,
    reads_at,
)
from .regime import AdmissionRefused, Regime


class CandidateBudgetRefused(RuntimeError):
    """Named terminal: an enumeration exceeded its declared candidate budget.

    Refused rather than truncated."""

    def __init__(self, message: str, candidate: Delta | None = None) -> None:
        super().__init__(message)
        self.candidate = candidate


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
    induced relation identical while costing one item.

    **How far that argument reaches, stated exactly.**  It settles the
    pruning for a predicate whose value depends on the candidate only through
    the induced relations and the resulting regime: OBS-1, OBS-2, OBS-3, OBS-5
    and LIM-G are of that form.  It settles **nothing by itself** for the
    other three, and each is a different case:

    * **OBS-4** reads the two readers' **selections**, through
      ``renaming_of_each_other``, so an inert context could move its verdict
      without moving any relation.
    * **LIM-R** reads a reader's **width**, in the short-circuit that skips
      the chain search below the carrier; an inert context raises the width
      while adding no strict split.
    * **LIM-F** reads the **item kinds** of the delta and no relation at all.

    An earlier version of this docstring claimed soundness for minima and
    below-minimum exhaustion with no qualification whatever.  That claim is
    **WITHDRAWN** as stated.

    What covers the three.  OBS-4 has an argument at the declared bounds:
    ``max_reader_items`` is 4 and ``max_readers`` is 2, so two readers leave
    at most two context items between them, and OBS-4 refuses a reader that
    separates nothing — a width-1 reader whose only context is inert separates
    nothing, and a width-0 reader separates nothing either — so no candidate
    answering OBS-4 within these bounds holds an inert context.
    ``tests/test_enumeration.py``
    ``test_a_width_one_inert_reader_separates_nothing`` carries that step and
    ``test_pruning_does_not_move_obs4_where_obs4_is_answered`` compares pruned
    against unpruned where OBS-4 is answered.  LIM-R and LIM-F have no such
    argument written here; for them the evidence is the cross-check itself,
    ``test_pruned_and_unpruned_minima_agree``, which runs **every** demand at a
    tightened bound where OBS-3 is answered inside it."""
    if not reads_at(b, coverage_bit(r, c)):
        return True
    vals = {admission_bit(r, c, d) for d in range(r.n_data())}
    return len(vals) <= 1


def reader_suffixes(
    r: Regime, s: int, bounds: Bounds, prune: bool = True
) -> Iterator[Delta]:
    """Every reader suffix of exactly ``s`` items over the regime.

    ``s`` items buy ``nr`` readers and ``s - nr`` contexts, each context its
    own item. All eight complement classes are retained. Equal separation
    behaviours do not establish full reader identity for OBS-4."""
    if s == 0:
        yield ()
        return
    if s > bounds.max_reader_items:
        return
    ctx = contexts(r)
    aggs = lawful_aggregations(bounds.w_max)
    readings = all_reading_classes()
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
                        f"{bounds.candidate_budget} at item count {total}; "
                        f"{seen - 1} candidates yielded; next candidate refused",
                        candidate=delta,
                    )
                yield delta, state
