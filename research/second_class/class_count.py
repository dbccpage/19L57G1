"""The finite cross-check for rung eight: the element count across the
isomorphism.

Classification (assumption discipline):

* Everything here is metatheory apparatus layered on the sealed kernel,
  the sealed genesis readings, the sealed isomorphism procedure, rung
  three's ``research/second_index/index.py`` and rung four's
  ``research/second_iso/iso_index.py``, all imported read-only through
  their public functions and pinned by blob in ``SOURCE_MANIFEST.json``.
  No sibling source is copied.
* The rectangle and its three bases are rung three's, consumed unchanged
  through rung four's population.  A class is the sealed key procedure's,
  through rung four's memoized keys, and the key partition is compared
  again here with the sealed brute-force minimum over every bijection
  pair.
* The FIVE COMPONENT COUNTS of a regime are its data, forms, instances,
  uniform rules and requirements, counted.  The Python regime keeps the
  last three as sets, so a Python count says nothing about a repeated
  entry in the Lean list presentation; that is the Lean's question.
* A CHANGING event is one after which the regime differs; a GROWTH is a
  changing event after which it has more data; a REST ROUND is any other
  changing event.  All three are counted here by stepping the sealed
  ``step``, never by a formula of this file.
* A sequence RECURS at position ``k`` when the regime after prefix ``k``
  has the class of the regime after an earlier prefix; the recurrence is
  a STUTTER when some earlier prefix of that class reached the very same
  regime, and a RETURN otherwise.
* The enumeration is a FINITE COMPUTATION over a declared rectangle, run
  without any sealed pruning lemma.
* Nothing here is a theorem.  The theorems of this rung are in ``lean/``;
  this file checks their content by exhaustion on a rectangle.
"""

from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass
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
# defect rung three found live, and rungs four to seven recorded again.
from iso_index import (  # noqa: E402
    ALPHABET,
    Keys,
    Population,
    build_population,
    partition_disagreements,
)
from index import BASE_NAMES, EMPTY_BASE, base_genesis  # noqa: E402
from nofirst import Alphabet  # noqa: E402
from derivation.iso import CanonKey  # noqa: E402
from derivation.model import (  # noqa: E402
    EMPTY,
    AdmissionError,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Regime,
    replay,
    step,
)

if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))

Components = tuple[int, int, int, int, int]
Counts = tuple[int, int, int]

# The four kinds of event the frozen prediction says reach a stutter, and
# the two it says never do, by the class names of the sealed event types.
STUTTER_KINDS = ("AdmitInst", "AdmitRuleAll", "Impose", "Supply")
GROWING_KINDS = ("AdmitDatum", "AdmitForm")


# ---------------------------------------------------------------------------
# Counts of a regime and of a history
# ---------------------------------------------------------------------------


def components(regime: Regime) -> Components:
    """The five component counts: data, forms, instances, uniform rules,
    requirements."""
    return (
        regime.n_data(),
        len(regime.forms),
        len(regime.insts),
        len(regime.rules),
        len(regime.reqs),
    )


def counts(base: Regime, history: Sequence[Event]) -> Counts:
    """The CHANGING count, the growths and the rest rounds of a history,
    by stepping the sealed step.  A history the sealed step refuses
    raises, as it does in the sealed replay."""
    changing = growths = rest = 0
    current = base
    for event in history:
        after = step(current, event)
        if after != current:
            changing += 1
            if after.n_data() > current.n_data():
                growths += 1
            else:
                rest += 1
        current = after
    return changing, growths, rest


def prefix_regimes(base: Regime, history: Sequence[Event]) -> list[Regime]:
    """The regime after every prefix of a history, the empty prefix
    first."""
    out = [base]
    for event in history:
        out.append(step(out[-1], event))
    return out


# ---------------------------------------------------------------------------
# Recurrence along one sequence
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Recurrence:
    """One position at which a sequence recurs."""

    position: int
    kind: str
    stutter: bool


def recurrences(
    base: Regime, history: Sequence[Event], keys: Keys
) -> list[Recurrence]:
    """Every position at which the sequence reaches the class of an
    earlier prefix, with the kind of the event taken there and whether
    some earlier prefix of that class reached the very same regime."""
    regimes = prefix_regimes(base, history)
    seen: dict[CanonKey, set[Regime]] = {}
    found: list[Recurrence] = []
    for position, regime in enumerate(regimes):
        key = keys.key(regime)
        earlier = seen.get(key)
        if earlier is not None and position > 0:
            found.append(
                Recurrence(
                    position,
                    type(history[position - 1]).__name__,
                    regime in earlier,
                )
            )
        seen.setdefault(key, set()).add(regime)
    return found


def has_unchanging_event(base: Regime, history: Sequence[Event]) -> bool:
    regimes = prefix_regimes(base, history)
    return any(regimes[i + 1] == regimes[i] for i in range(len(history)))


def recurrence_report(
    base: Regime, histories: Sequence[Sequence[Event]], keys: Keys
) -> dict[str, Any]:
    """At one base: how many sequences recur, how many recurrences are
    stutters and returns, which kinds reach a stutter, and whether a
    sequence recurs exactly when it holds an unchanging event."""
    recurring = 0
    with_unchanging = 0
    mismatches = 0
    stutters = 0
    returns = 0
    by_kind: dict[str, int] = {}
    for history in histories:
        found = recurrences(base, history, keys)
        unchanging = has_unchanging_event(base, history)
        if found:
            recurring += 1
        if unchanging:
            with_unchanging += 1
        if bool(found) != unchanging:
            mismatches += 1
        for item in found:
            if item.stutter:
                stutters += 1
                by_kind[item.kind] = by_kind.get(item.kind, 0) + 1
            else:
                returns += 1
    return {
        "sequences": len(histories),
        "recurring_sequences": recurring,
        "sequences_with_an_unchanging_event": with_unchanging,
        "recurs_iff_unchanging_mismatches": mismatches,
        "stutters": stutters,
        "returns": returns,
        "stutters_by_kind": dict(sorted(by_kind.items())),
    }


# ---------------------------------------------------------------------------
# Classes: component counts, and the counts of the histories reaching them
# ---------------------------------------------------------------------------


def class_report(population: Population) -> dict[str, Any]:
    """Classes within each base and over all three: those carrying two
    component tuples; those reached with two values of the three counts
    of a history within a base; those reached at more than one base, and
    at more than one base with two CHANGING counts."""
    keys = population.keys
    within: dict[str, dict[str, int]] = {}
    changing_by_class: dict[CanonKey, dict[str, set[int]]] = {}
    for rect in population.rects:
        tuples: dict[CanonKey, set[Components]] = {}
        histories: dict[CanonKey, set[Counts]] = {}
        for node in rect.nodes:
            key = keys.key(node.regime)
            tuples.setdefault(key, set()).add(components(node.regime))
            found = counts(rect.regime, node.history)
            histories.setdefault(key, set()).add(found)
            changing_by_class.setdefault(key, {}).setdefault(rect.base, set()).add(
                found[0]
            )
        within[rect.base] = {
            "classes": len(tuples),
            "classes_with_two_component_tuples": sum(
                1 for found in tuples.values() if len(found) > 1
            ),
            "classes_with_two_changing_counts": sum(
                1 for found in histories.values() if len({c[0] for c in found}) > 1
            ),
            "classes_with_two_growth_counts": sum(
                1 for found in histories.values() if len({c[1] for c in found}) > 1
            ),
            "classes_with_two_rest_counts": sum(
                1 for found in histories.values() if len({c[2] for c in found}) > 1
            ),
        }
    union: dict[CanonKey, set[Components]] = {}
    for regime in population.regimes:
        union.setdefault(keys.key(regime), set()).add(components(regime))
    multi = [bases for bases in changing_by_class.values() if len(bases) > 1]
    return {
        "within_base": within,
        "classes_over_all_bases": len(union),
        "classes_over_all_bases_with_two_component_tuples": sum(
            1 for found in union.values() if len(found) > 1
        ),
        "classes_at_more_than_one_base": len(multi),
        "classes_at_three_bases": sum(1 for bases in multi if len(bases) == 3),
        "classes_at_more_than_one_base_with_two_changing_counts": sum(
            1
            for bases in multi
            if len(set().union(*bases.values())) > 1
        ),
        "key_brute_disagreements": partition_disagreements(population.regimes, keys),
    }


# ---------------------------------------------------------------------------
# The Lean countermodels, written in the sealed Python grammar
# ---------------------------------------------------------------------------


def _tokens(n: int) -> tuple[str, ...]:
    return ALPHABET.fresh_tokens[:n]


def lean_witnesses() -> dict[str, Any]:
    """Each countermodel of `lean/SecondClass/Counter.lean` in the sealed
    Python grammar.  The `*_need_nodup` pairs, written as Python regimes,
    are one regime, because the Python regime keeps sets.  The event that
    would admit the ill-formed element of each `*_need_wf` pair, taken at
    the duplicate-free side, is refused by the sealed step.  The two sides
    of `counts_not_of_class` reach one class with CHANGING counts zero and
    three."""
    one = _tokens(1)
    two = _tokens(2)
    twice = {
        "insts_need_nodup": (
            Regime(one, (1,), frozenset([(0, (0,)), (0, (0,))]), frozenset(), frozenset()),
            Regime(one, (1,), frozenset([(0, (0,))]), frozenset(), frozenset()),
        ),
        "rules_need_nodup": (
            Regime((), (1,), frozenset(), frozenset([0, 0]), frozenset()),
            Regime((), (1,), frozenset(), frozenset([0]), frozenset()),
        ),
        "reqs_need_nodup": (
            Regime(two, (), frozenset(), frozenset(), frozenset([(0, 1), (0, 1)])),
            Regime(two, (), frozenset(), frozenset(), frozenset([(0, 1)])),
        ),
    }
    outside: dict[str, tuple[Regime, Event]] = {
        "insts_need_wf": (twice["insts_need_nodup"][1], AdmitInst(0, (5,))),
        "rules_need_wf": (twice["rules_need_nodup"][1], AdmitRuleAll(5)),
        "reqs_need_wf": (twice["reqs_need_nodup"][1], Impose(1, 0)),
    }
    out: dict[str, Any] = {}
    for name, (left, right) in sorted(twice.items()):
        same = left == right
        out[name] = {"one_python_regime": same, "claim_holds": same}
    for name, (regime, event) in sorted(outside.items()):
        refused = _refused(regime, event)
        out[name] = {"refused_by_the_sealed_step": refused, "claim_holds": refused}
    out["counts_not_of_class"] = _across_bases()
    return out


def python_reading_witness() -> dict[str, Any]:
    """RECORDED AFTER THE MISS OF P-13, and not scored.  The sealed Python
    reading regime L holds two data and NO requirement, where the sealed
    Lean reading regime `R2L` holds the requirement between them; so the
    Lean witness, written in the Python grammar, does not reach one class.
    Written for the Python readings instead: the empty history from L,
    and a datum and a datum from the empty regime, reach one class with
    CHANGING counts zero and two."""
    first, second = _tokens(2)
    reading_l = replay(base_genesis("L"), EMPTY)
    from_empty = (AdmitDatum(first), AdmitDatum(second))
    right = replay(from_empty, EMPTY)
    keys = Keys()
    return {
        "reading_l_requirements": len(reading_l.reqs),
        "one_class": keys.key(reading_l) == keys.key(right),
        "changing_counts": [counts(reading_l, ())[0], counts(EMPTY, from_empty)[0]],
    }


def _refused(regime: Regime, event: Event) -> bool:
    try:
        step(regime, event)
    except AdmissionError:
        return True
    return False


def across_bases_histories() -> tuple[tuple[Event, ...], tuple[Event, ...]]:
    """The empty history, from the reading regime L; and a datum, a datum
    and the requirement between them, from the empty regime."""
    first, second = _tokens(2)
    return (), (AdmitDatum(first), AdmitDatum(second), Impose(0, 1))


def _across_bases() -> dict[str, Any]:
    reading_l = replay(base_genesis("L"), EMPTY)
    from_l, from_empty = across_bases_histories()
    left = replay(from_l, reading_l)
    right = replay(from_empty, EMPTY)
    keys = Keys()
    one_class = keys.key(left) == keys.key(right)
    values = [counts(reading_l, from_l)[0], counts(EMPTY, from_empty)[0]]
    return {
        "one_class": one_class,
        "one_python_regime": left == right,
        "changing_counts": values,
        "claim_holds": one_class and values == [0, 3],
    }


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------


def all_reports(alphabet: Alphabet = ALPHABET) -> dict[str, Any]:
    """Everything this rung measures."""
    population = build_population(alphabet)
    replay_mismatches = 0
    bases: dict[str, Any] = {}
    for rect in population.rects:
        for node in rect.nodes:
            if replay(node.history, rect.regime) != node.regime:
                replay_mismatches += 1
        row = recurrence_report(
            rect.regime, [node.history for node in rect.nodes], population.keys
        )
        row["distinct_regimes"] = len({node.regime for node in rect.nodes})
        bases[rect.base] = row
    return {
        "base_order": list(BASE_NAMES),
        "bases": bases,
        "replay_mismatches": replay_mismatches,
        "distinct_regimes_over_all_bases": len(population.regimes),
        "classes": class_report(population),
        "lean_witnesses": lean_witnesses(),
        "python_reading_witness": python_reading_witness(),
    }


__all__ = [
    "ALPHABET",
    "EMPTY_BASE",
    "GROWING_KINDS",
    "Recurrence",
    "STUTTER_KINDS",
    "across_bases_histories",
    "all_reports",
    "build_population",
    "class_report",
    "components",
    "counts",
    "has_unchanging_event",
    "lean_witnesses",
    "prefix_regimes",
    "python_reading_witness",
    "recurrence_report",
    "recurrences",
]
