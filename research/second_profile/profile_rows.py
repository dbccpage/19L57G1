"""The finite cross-check for rung nine: two-ness and the observational
classes.

Classification (assumption discipline):

* Everything here is metatheory apparatus layered on the sealed kernel,
  the sealed profiles, the sealed genesis readings, the sealed
  isomorphism procedure, rung three's ``research/second_index/index.py``
  and rung four's ``research/second_iso/iso_index.py``, all imported
  read-only through their public functions and pinned by blob in
  ``SOURCE_MANIFEST.json``.  No sibling source is copied.
* The rectangle and its three bases are rung three's, consumed unchanged
  through rung four's population.  A class of regimes is the sealed key
  procedure's, through rung four's memoized keys, and the key partition
  is compared again here with the sealed brute-force minimum over every
  bijection pair.
* A regime HOLDS TWO when the sealed ``separable`` tells some two of its
  admitted data apart.  Its CLASS COUNT is the number of distinct sealed
  ``profiles`` among its admitted data.  The two are read through two
  different sealed functions, so their agreement is a check and not an
  identity of this file.
* A TRANSITION is a sequence of length at least one with its prefix one
  event shorter; its KIND is the class name of its last event; its
  CHANGE is the class count after less the class count before.  It ENDS
  two-ness when the regime before holds two and the regime after does
  not.  A datum is NAMED when it is an argument of some held instance.
* The enumeration is a FINITE COMPUTATION over a declared rectangle, run
  without any sealed pruning lemma.
* Nothing here is a theorem.  The theorems of this rung are in ``lean/``;
  this file checks their content by exhaustion on a rectangle.
"""

from __future__ import annotations

import pathlib
import sys
from typing import Any, Sequence

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_ISO_TREE = str(REPO / "research" / "second_iso")
if _ISO_TREE not in sys.path:
    sys.path.insert(0, _ISO_TREE)

# Rung four's module puts rung three, the sealed kernel and the sibling
# trees on the path, and puts its OWN tree at the front.  Each of those
# trees carries modules named `verify_pins`, `check_coverage` and
# `test_*`, so this tree goes back to the front AFTER the import, or a
# sibling's module is silently loaded in place of this rung's -- the
# defect rung three found live, and rungs four to eight recorded again.
from iso_index import (  # noqa: E402
    ALPHABET,
    Keys,
    Population,
    build_population,
    partition_disagreements,
)
from index import BASE_NAMES, EMPTY_BASE  # noqa: E402
from nofirst import Alphabet  # noqa: E402
from derivation.iso import CanonKey  # noqa: E402
from derivation.model import (  # noqa: E402
    EMPTY,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Regime,
    replay,
    step,
)
from derivation.observe import profiles, separable  # noqa: E402

if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))

# The kinds the Lean of this rung proves keep holding two, and the two it
# shows can end it, by the class names of the sealed event types.
KEEPING_KINDS = ("AdmitDatum", "AdmitForm", "Impose", "Supply")
ENDING_KINDS = ("AdmitInst", "AdmitRuleAll")


# ---------------------------------------------------------------------------
# What one regime shows
# ---------------------------------------------------------------------------


def holds_two(regime: Regime) -> bool:
    """Some two admitted data are separable, by the sealed ``separable``."""
    n = regime.n_data()
    return any(separable(regime, i, j) for i in range(n) for j in range(i + 1, n))


def class_count(regime: Regime) -> int:
    """The number of distinct sealed profiles among the admitted data."""
    return len(set(profiles(regime)))


def named(regime: Regime) -> int:
    """The number of data that are an argument of some held instance."""
    return len({a for _, args in regime.insts for a in args})


class Readings:
    """Holding two and the class count, memoized by regime."""

    def __init__(self) -> None:
        self._two: dict[Regime, bool] = {}
        self._count: dict[Regime, int] = {}

    def two(self, regime: Regime) -> bool:
        found = self._two.get(regime)
        if found is None:
            found = holds_two(regime)
            self._two[regime] = found
        return found

    def count(self, regime: Regime) -> int:
        found = self._count.get(regime)
        if found is None:
            found = class_count(regime)
            self._count[regime] = found
        return found


# ---------------------------------------------------------------------------
# One base's rectangle
# ---------------------------------------------------------------------------


def base_report(
    root: Regime,
    nodes: Sequence[tuple[tuple[Event, ...], Regime]],
    keys: Keys,
    seen: Readings,
) -> dict[str, Any]:
    """Everything one base's rectangle shows about holding two and the
    class count.  ``nodes`` pairs each sequence with the regime it
    reaches; every prefix of a sequence is itself a node."""
    by_history = dict(nodes)
    replay_mismatches = sum(
        1 for history, regime in nodes if replay(history, root) != regime
    )
    regimes = {regime for _, regime in nodes}
    least: int | None = None
    sequences_two = 0
    for history, regime in nodes:
        if seen.two(regime):
            sequences_two += 1
            if least is None or len(history) < least:
                least = len(history)
    regimes_two = [r for r in regimes if seen.two(r)]
    two_count_mismatches = sum(
        1 for r in regimes if seen.two(r) != (seen.count(r) >= 2)
    )
    over_data = sum(1 for r in regimes if seen.count(r) > r.n_data())
    over_named = sum(1 for r in regimes if seen.count(r) > named(r) + 1)
    histogram: dict[int, int] = {}
    for r in regimes:
        histogram[seen.count(r)] = histogram.get(seen.count(r), 0) + 1
    ending: dict[str, int] = {}
    changes: dict[str, set[int]] = {}
    for history, regime in nodes:
        if not history:
            continue
        before = by_history[history[:-1]]
        kind = type(history[-1]).__name__
        changes.setdefault(kind, set()).add(seen.count(regime) - seen.count(before))
        if seen.two(before) and not seen.two(regime):
            ending[kind] = ending.get(kind, 0) + 1
    return {
        "sequences": len(nodes),
        "distinct_regimes": len(regimes),
        "replay_mismatches": replay_mismatches,
        "least_length_holding_two": least,
        "sequences_holding_two": sequences_two,
        "regimes_holding_two": len(regimes_two),
        "classes_holding_two": len({keys.key(r) for r in regimes_two}),
        "two_count_mismatches": two_count_mismatches,
        "class_count_histogram": {str(k): histogram[k] for k in sorted(histogram)},
        "largest_class_count": max(histogram),
        "count_above_data": over_data,
        "count_above_named_plus_one": over_named,
        "ending_transitions_by_kind": dict(sorted(ending.items())),
        "changes_by_kind": {k: sorted(v) for k, v in sorted(changes.items())},
    }


# ---------------------------------------------------------------------------
# Classes of regimes
# ---------------------------------------------------------------------------


def lumping(
    groups: Sequence[Sequence[Regime]], keys: Keys, seen: Readings
) -> dict[str, int]:
    """For each group of regimes, the classes of the key procedure that
    carry two values of holding two, and two values of the class count."""
    two: dict[CanonKey, set[bool]] = {}
    count: dict[CanonKey, set[int]] = {}
    for group in groups:
        for regime in group:
            key = keys.key(regime)
            two.setdefault(key, set()).add(seen.two(regime))
            count.setdefault(key, set()).add(seen.count(regime))
    return {
        "classes": len(two),
        "classes_with_two_values_of_holding_two": sum(1 for v in two.values() if len(v) > 1),
        "classes_with_two_class_counts": sum(1 for v in count.values() if len(v) > 1),
    }


def class_report(population: Population, seen: Readings) -> dict[str, Any]:
    keys = population.keys
    within = {
        rect.base: lumping([[node.regime for node in rect.nodes]], keys, seen)
        for rect in population.rects
    }
    return {
        "within_base": within,
        "over_all_bases": lumping([population.regimes], keys, seen),
        "distinct_regimes_over_all_bases": len(population.regimes),
        "key_brute_disagreements": partition_disagreements(population.regimes, keys),
    }


# ---------------------------------------------------------------------------
# The Lean witnesses, written in the sealed Python grammar
# ---------------------------------------------------------------------------


def lean_witnesses() -> dict[str, Any]:
    """RECORDED, not scored.  The histories of `twoness_at_four` and of
    the two ending countermodels of `lean/SecondProfile/`, replayed by the
    sealed Python step from the sealed empty regime."""
    first, second = ALPHABET.fresh_tokens[:2]
    four: tuple[Event, ...] = (
        AdmitDatum(first),
        AdmitDatum(second),
        AdmitForm(1),
        AdmitInst(0, (0,)),
    )
    reached = replay(four, EMPTY)
    by_inst = step(reached, AdmitInst(0, (1,)))
    by_rule = step(reached, AdmitRuleAll(0))
    return {
        "twoness_at_four": {"holds_two": holds_two(reached), "class_count": class_count(reached)},
        "twoness_lost_by_inst": {"holds_two": holds_two(by_inst), "class_count": class_count(by_inst)},
        "twoness_lost_by_rule": {"holds_two": holds_two(by_rule), "class_count": class_count(by_rule)},
    }


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------


def all_reports(alphabet: Alphabet = ALPHABET) -> dict[str, Any]:
    """Everything this rung measures."""
    population = build_population(alphabet)
    seen = Readings()
    bases: dict[str, Any] = {}
    changes: dict[str, set[int]] = {}
    for rect in population.rects:
        row = base_report(
            rect.regime,
            [(node.history, node.regime) for node in rect.nodes],
            population.keys,
            seen,
        )
        bases[rect.base] = row
        for kind, values in row["changes_by_kind"].items():
            changes.setdefault(kind, set()).update(values)
    return {
        "base_order": list(BASE_NAMES),
        "bases": bases,
        "changes_by_kind_over_all_bases": {k: sorted(v) for k, v in sorted(changes.items())},
        "classes": class_report(population, seen),
        "lean_witnesses": lean_witnesses(),
    }


__all__ = [
    "ALPHABET",
    "EMPTY_BASE",
    "ENDING_KINDS",
    "KEEPING_KINDS",
    "Readings",
    "all_reports",
    "base_report",
    "build_population",
    "class_count",
    "class_report",
    "holds_two",
    "lean_witnesses",
    "lumping",
    "named",
]
