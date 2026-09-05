"""The censuses, published before any finding.

Classification: deterministic computation.

A finding whose supporting count is zero is refused by name.  Both sealed
Challenge-3 bases carry zero contexts, so they can carry the calibration and
no observation finding whatever, and the census says so before anything else
is reported.
"""

from __future__ import annotations

import itertools
from typing import Iterator

from .enumerate_space import Bounds, iter_sealed_items
from .grammar import (
    admission_bit,
    collapsed_pairs,
    contexts,
    coverage_bit,
    data_pairs,
    sealed_relation,
)
from .items import StatedState, apply_delta
from .quotient import canonical_regime
from .readers import (
    ADMISSION_ONLY_READING,
    ALL_READINGS,
    BEHAVIOURS,
    BEHAVIOUR_NAMES,
    Reader,
    SEALED_READING,
    all_aggregations,
    all_reading_classes,
    behaviour,
    induced_blocks,
    induced_relation,
    lawful_aggregations,
    monotone_aggregations,
    non_constant_reading_classes,
    reads_at,
    sealed_as_reader,
    unlawful_aggregations,
)
from .regime import AdmissionRefused, Regime, genesis


class VacuousFindingRefused(RuntimeError):
    """Named terminal: a finding whose supporting count is zero."""


def refuse_if_vacuous(name: str, count: int) -> int:
    if count == 0:
        raise VacuousFindingRefused(
            f"{name} has a supporting count of zero and is refused as vacuous"
        )
    return count


def population(depth: int, bounds: Bounds) -> list[Regime]:
    """The quotiented population: states reachable from the two sealed bases
    by at most ``depth`` sealed one-item moves.  Recomputed, never trusted."""
    seen: dict[object, Regime] = {}
    for reading in ("L", "F"):
        r = genesis(reading)
        seen.setdefault(canonical_regime(r, bounds.bijection_budget), r)
    frontier = list(seen.values())
    for _ in range(depth):
        nxt: list[Regime] = []
        for r in frontier:
            for child in _children(r, bounds):
                k = canonical_regime(child, bounds.bijection_budget)
                if k not in seen:
                    seen[k] = child
                    nxt.append(child)
        frontier = nxt
    return list(seen.values())


def _children(r: Regime, bounds: Bounds) -> Iterator[Regime]:
    for it in iter_sealed_items(r, bounds):
        try:
            yield apply_delta(
                StatedState(r, ()), (it,), bounds.w_max, bounds.max_readers
            ).regime
        except AdmissionRefused:  # pragma: no cover - the alphabet is valid
            continue


def monotonicity_census(depth: int, bounds: Bounds) -> dict[str, int]:
    """Every item offered at every state of the population either enlarges
    the context set or leaves it unchanged, and never shrinks it.

    A single violation would invalidate evaluating an early context at a
    later stage, which both limit directions rely on."""
    moves = enlarge = unchanged = violations = 0
    for r in population(depth, bounds):
        before = set(contexts(r))
        for child in _children(r, bounds):
            moves += 1
            after = set(contexts(child))
            if not before <= after:
                violations += 1
            if len(after) > len(before):
                enlarge += 1
            else:
                unchanged += 1
    return {
        "moves": moves,
        "enlarge": enlarge,
        "unchanged": unchanged,
        "violations": violations,
    }


def column_kernel(r: Regime, c: object) -> frozenset[tuple[int, int]]:
    """The pairs one context's admission bit fails to tell apart."""
    return frozenset(
        (i, j)
        for (i, j) in data_pairs(r.n_data())
        if admission_bit(r, c, i) == admission_bit(r, c, j)  # type: ignore[arg-type]
    )


def admits_rival(r: Regime) -> bool:
    """Whether some sealed-collapsed pair is told apart by the admission bit
    at some context — the raw-bit rival, decided by computation."""
    ctx = contexts(r)
    for (i, j) in collapsed_pairs(r):
        for c in ctx:
            if admission_bit(r, c, i) != admission_bit(r, c, j):
                return True
    return False


def vacuity_census(depth: int, bounds: Bounds) -> dict[str, int]:
    """Published **before** any finding."""
    pop = population(depth, bounds)
    out = {
        "states": len(pop),
        "with_a_context": 0,
        "two_distinct_kernels": 0,
        "two_incomparable_kernels": 0,
        "collapsed_pair_and_a_context": 0,
        "carrier_ceiling_attained": 0,
        "admits_a_rival": 0,
    }
    for r in pop:
        ctx = contexts(r)
        if ctx:
            out["with_a_context"] += 1
        kernels = {column_kernel(r, c) for c in ctx}
        if len(kernels) >= 2:
            out["two_distinct_kernels"] += 1
        if any(
            not a <= b and not b <= a for a in kernels for b in kernels
        ):
            out["two_incomparable_kernels"] += 1
        if collapsed_pairs(r) and ctx:
            out["collapsed_pair_and_a_context"] += 1
        if r.n_data() and len(sealed_relation(r)) == len(
            data_pairs(r.n_data())
        ):
            out["carrier_ceiling_attained"] += 1
        if admits_rival(r):
            out["admits_a_rival"] += 1
    return out


def reading_axis_census(w_max: int) -> dict[str, object]:
    """The reading and aggregation axes, enumerated once, before pricing."""
    behaviours: dict[tuple[bool, bool], int] = {}
    for b in ALL_READINGS:
        behaviours[behaviour(b)] = behaviours.get(behaviour(b), 0) + 1
    return {
        "readings": 16,
        "complement_classes": len(all_reading_classes()),
        "non_constant_complement_classes": len(
            non_constant_reading_classes()
        ),
        "induced_separation_behaviours": len(behaviours),
        "behaviour_names": [BEHAVIOUR_NAMES[b] for b in BEHAVIOURS],
        "sealed_behaviour": BEHAVIOUR_NAMES[behaviour(SEALED_READING)],
        "admission_only_behaviour": BEHAVIOUR_NAMES[
            behaviour(ADMISSION_ONLY_READING)
        ],
        "aggregations": len(all_aggregations(w_max)),
        "lawful": len(lawful_aggregations(w_max)),
        "monotone": len(monotone_aggregations(w_max)),
        "monotone_by_width": {
            w: len(monotone_aggregations(w)) for w in range(1, w_max + 2)
        },
        "unlawful_refused": len(unlawful_aggregations(w_max)),
        "lawful_by_width": {
            w: len(lawful_aggregations(w)) for w in range(1, w_max + 2)
        },
        "aggregations_by_width": {
            w: len(all_aggregations(w)) for w in range(1, w_max + 2)
        },
    }


def sealed_is_a_reader(depth: int, bounds: Bounds) -> dict[str, int]:
    """The sealed observation relation is the full-selection reader that
    reads the admission bit only where coverage is absent, with ``s >= 1``.

    Checked at every state of the population, not merely at the bases."""
    checked = mismatches = 0
    for r in population(depth, bounds):
        checked += 1
        if induced_relation(r, sealed_as_reader(r)) != sealed_relation(r):
            mismatches += 1
    return {"checked": checked, "mismatches": mismatches}


def chain_census(depth: int, bounds: Bounds) -> dict[str, object]:
    """The longest chain of strictly splitting selections at each state.

    The positive control for LIM-R: the obstruction is void unless the
    carrier ceiling is **attained** somewhere."""
    hist: dict[int, int] = {}
    attained = over_ceiling = 0
    for r in population(depth, bounds):
        ctx = contexts(r)
        if not ctx:
            continue
        best = 0
        for b in all_reading_classes():
            for a in lawful_aggregations(bounds.w_max):
                for w in range(0, min(bounds.w_max, len(ctx)) + 1):
                    for sel in itertools.combinations(ctx, w):
                        for order in itertools.permutations(sel):
                            blocks = induced_blocks(r, Reader((), b, a))
                            steps = 0
                            for k in range(len(order)):
                                nxt = induced_blocks(
                                    r, Reader(order[: k + 1], b, a)
                                )
                                if nxt > blocks:
                                    steps += 1
                                    blocks = nxt
                            best = max(best, steps)
        hist[best] = hist.get(best, 0) + 1
        if best == r.n_data() - 1:
            attained += 1
        if best > r.n_data() - 1:
            over_ceiling += 1
    return {
        "longest_chain_histogram": dict(sorted(hist.items())),
        "carrier_ceiling_attained": attained,
        "chains_above_the_ceiling": over_ceiling,
    }


def capacity_census(depth: int, bounds: Bounds) -> dict[str, object]:
    """The positive control for LIM-G, and the derived threshold.

    A fixed-selection reader of width ``w`` has at most ``2 ** w`` blocks,
    because equal signatures force ``s = 0`` and ``a(0) = false``.  The census
    records where a reader separating **every** pair exists."""
    found: dict[str, int] = {}
    states = 0
    for r in population(depth, bounds):
        n = r.n_data()
        if n < 2:
            continue
        states += 1
        ctx = contexts(r)
        universe = frozenset(data_pairs(n))
        for w in range(0, min(bounds.w_max, len(ctx)) + 1):
            hit = False
            for b in all_reading_classes():
                for a in lawful_aggregations(bounds.w_max):
                    for sel in itertools.combinations(ctx, w):
                        if induced_relation(r, Reader(sel, b, a)) == universe:
                            hit = True
                            break
                    if hit:
                        break
                if hit:
                    break
            if hit:
                key = f"n={n},width={w}"
                found[key] = found.get(key, 0) + 1
                break
    return {
        "states_considered": states,
        "separating_reader_found": dict(sorted(found.items())),
        "block_ceiling_by_width": {
            w: 2 ** w for w in range(1, bounds.w_max + 1)
        },
        "carrier_threshold": 2 ** bounds.w_max,
    }


# --------------------------------------------------------------------------
# The LIM-F positive control: metatheory functions, never admitted
# --------------------------------------------------------------------------


def family_stable(values: tuple[bool, ...], window_start: int,
                  f: object) -> bool:
    fn = f  # a total function of a finite prefix
    full = fn(values)  # type: ignore[operator]
    return all(
        fn(values[: k + 1]) == full  # type: ignore[operator]
        for k in range(window_start, len(values))
    )


def family_novel(values: tuple[bool, ...], f: object) -> bool:
    full = f(values)  # type: ignore[operator]
    return all(full != v for v in values)


def control_family_functions() -> dict[str, object]:
    """Hand-supplied functions **outside** the admitted grammar.

    They are metatheory apparatus and are never admitted by any item.  They
    exist so that an empty LIM-F minimum set is an obstruction rather than a
    demand nothing finite could ever meet."""
    return {
        "not the first verdict": lambda v: (not v[0]) if v else False,
        "not the last verdict": lambda v: (not v[-1]) if v else False,
        "no verdict was true": lambda v: not any(v),
    }


def limf_control(values: tuple[bool, ...], window_start: int
                 ) -> dict[str, bool]:
    """Whether the stability and novelty tests can be passed at all."""
    return {
        name: family_stable(values, window_start, f)
        and family_novel(values, f)
        for name, f in control_family_functions().items()
    }


def rival_derivability_census(bounds: Bounds) -> dict[str, object]:
    """Is the exhibited rival a value of the declared combination set applied
    to the sealed relation, or is it genuinely admitted?

    Decided at the minimum rival state of each reading.  The answer is not
    uniform, and that is the finding: at two admitted data the sealed relation
    is empty and the rival is its complement, so the rival is DERIVED; at
    three the rival separates one datum from the other two, which is neither
    the sealed relation, nor its complement, nor anything else the declared
    one-application set reaches, so the rival is ADMITTED."""
    from .demands import combination_values
    from .items import NewForm, NewInst, NewRuleAll
    from .readers import ADMISSION_ONLY_READING

    out: dict[str, object] = {}
    for reading in ("L", "F"):
        r = apply_delta(
            StatedState(genesis(reading), ()),
            (NewForm(1), NewRuleAll(0), NewInst(0, (0,))),
            bounds.w_max, bounds.max_readers,
        ).regime
        ctx = contexts(r)
        universe = frozenset(data_pairs(r.n_data()))
        sealed = sealed_relation(r)
        rho = Reader(
            ctx[:1], ADMISSION_ONLY_READING, (False, True, True, True)
        )
        rel = induced_relation(r, rho)
        inside = sorted(
            k for k, v in combination_values(universe, sealed, None).items()
            if v == rel
        )
        out[reading] = {
            "n_data": r.n_data(),
            "sealed_separates": sorted(sealed),
            "rival_separates": sorted(rel),
            "verdict": "DERIVED" if inside else "ADMITTED",
            "combinations_matching": inside,
        }
    return out
