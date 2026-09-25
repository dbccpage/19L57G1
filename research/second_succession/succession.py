"""The finite cross-check for rung six: succession through the element
count.

Classification (assumption discipline):

* Everything here is metatheory apparatus layered on the sealed kernel,
  the sealed genesis readings, the sealed isomorphism procedure, rung
  three's ``research/second_index/index.py`` and rung four's
  ``research/second_iso/iso_index.py``, all imported read-only through
  their public functions and pinned by blob in ``SOURCE_MANIFEST.json``.
  No sibling source is copied.
* The rectangle and its three bases are rung three's, consumed unchanged
  through rung four's population.  A class is the sealed key procedure's,
  through rung four's memoized keys.
* The three READINGS of an accepted round are the ones `PROMPT.md`
  declares: EVERY (every event), ADMITTING (every event other than a
  supply) and CHANGING (every event after which the regime differs from
  the regime before).  They are counted here by stepping the sealed
  ``step``, never by a formula of this file.
* The enumeration is a FINITE COMPUTATION over a declared rectangle, run
  without any sealed pruning lemma.
* Nothing here is a theorem.  The theorems of this rung are in ``lean/``;
  this file checks their content by exhaustion on a rectangle and records
  the counts the theorems do not state.
"""

from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass
from typing import Any, Optional, Sequence

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
# defect rung three found live, and rungs four and five recorded again.
from iso_index import ALPHABET, Population, build_population  # noqa: E402
from index import BASE_NAMES, base_genesis, history_descriptor  # noqa: E402
from nofirst import Alphabet  # noqa: E402
from derivation.engine import GENESIS_L  # noqa: E402
from derivation.iso import CanonKey  # noqa: E402
from derivation.model import (  # noqa: E402
    EMPTY,
    AdmitForm,
    AdmitRuleAll,
    Event,
    Impose,
    Regime,
    Supply,
    replay,
    step,
)

if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))

READINGS: tuple[str, ...] = ("EVERY", "ADMITTING", "CHANGING")

Counts = dict[str, int]


# ---------------------------------------------------------------------------
# The element count and the three counts of a history
# ---------------------------------------------------------------------------


def element_count(regime: Regime) -> int:
    """Data, forms, instances, rules and requirements, counted."""
    return (
        regime.n_data()
        + len(regime.forms)
        + len(regime.insts)
        + len(regime.rules)
        + len(regime.reqs)
    )


def counts(base: Regime, history: Sequence[Event]) -> Counts:
    """The count of a history under each reading, stepping the sealed
    step from the base.  A history the sealed step refuses raises, as it
    does in the sealed replay."""
    every = admitting = changing = 0
    current = base
    for event in history:
        after = step(current, event)
        every += 1
        if not isinstance(event, Supply):
            admitting += 1
        if after != current:
            changing += 1
        current = after
    return {"EVERY": every, "ADMITTING": admitting, "CHANGING": changing}


# ---------------------------------------------------------------------------
# One base: split regimes and the shortest splitting sequence
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Sequenced:
    """One sequence of a base's rectangle, with its counts."""

    history: tuple[Event, ...]
    regime: Regime
    counts: Counts

    def order(self) -> tuple[int, tuple[str, ...]]:
        return (len(self.history), history_descriptor(self.history))


def splitting(
    groups: dict[Regime, list[Sequenced]], reading: str
) -> tuple[int, Optional[tuple[Sequenced, Sequenced]]]:
    """The number of regimes reached with two counts under a reading, and
    the shortest splitting sequence with the first sequence it splits
    from: the least sequence, in order of length and then descriptor,
    whose count differs from that of a sequence of no greater length
    reaching the same regime."""
    split = 0
    best: Optional[tuple[Sequenced, Sequenced]] = None
    for members in groups.values():
        if len({m.counts[reading] for m in members}) > 1:
            split += 1
        ordered = sorted(members, key=Sequenced.order)
        for later in ordered:
            earlier = next(
                (
                    m
                    for m in ordered
                    if len(m.history) <= len(later.history)
                    and m.counts[reading] != later.counts[reading]
                ),
                None,
            )
            if earlier is None:
                continue
            if best is None or later.order() < best[1].order():
                best = (earlier, later)
            break
    return split, best


def witness(pair: Optional[tuple[Sequenced, Sequenced]], reading: str) -> Optional[dict[str, Any]]:
    if pair is None:
        return None
    earlier, later = pair
    return {
        "length": len(later.history),
        "history": list(history_descriptor(later.history)),
        "count": later.counts[reading],
        "splits_from": list(history_descriptor(earlier.history)),
        "splits_from_count": earlier.counts[reading],
    }


def base_report(
    base: str, base_regime: Regime, sequences: Sequence[Sequenced]
) -> dict[str, Any]:
    """Every count at one base: split regimes and shortest splitting
    sequence under each reading; the CHANGING law against the element
    count; and the same law counted from the sealed empty regime through
    the base's sealed genesis history."""
    groups: dict[Regime, list[Sequenced]] = {}
    for item in sequences:
        groups.setdefault(item.regime, []).append(item)
    genesis = base_genesis(base)
    law_violations = 0
    genesis_violations = 0
    for item in sequences:
        if item.counts["CHANGING"] != element_count(item.regime) - element_count(base_regime):
            law_violations += 1
        through = counts(EMPTY, genesis + item.history)
        if through["CHANGING"] != element_count(item.regime):
            genesis_violations += 1
    readings: dict[str, Any] = {}
    for reading in READINGS:
        split, pair = splitting(groups, reading)
        readings[reading] = {
            "split_regimes": split,
            "shortest_splitting_sequence": witness(pair, reading),
        }
    return {
        "sequences": len(sequences),
        "distinct_regimes": len(groups),
        "base_element_count": element_count(base_regime),
        "genesis_counts": counts(EMPTY, genesis),
        "changing_law_violations": law_violations,
        "changing_from_empty_violations": genesis_violations,
        "readings": readings,
    }


# ---------------------------------------------------------------------------
# Classes, within and across bases
# ---------------------------------------------------------------------------


def class_report(
    population: Population, by_base: dict[str, list[Sequenced]]
) -> dict[str, Any]:
    """Taken up to the implemented isomorphism: classes reached within a
    base with two CHANGING counts; classes reached from more than one
    base; among those, how many carry equal base-relative counts at two
    bases, and how many carry two counts from the sealed empty regime."""
    relative: dict[CanonKey, dict[str, set[int]]] = {}
    from_empty: dict[CanonKey, set[int]] = {}
    for base, sequences in by_base.items():
        offset = element_count(replay(base_genesis(base), EMPTY))
        for item in sequences:
            key = population.keys.key(item.regime)
            relative.setdefault(key, {}).setdefault(base, set()).add(
                item.counts["CHANGING"]
            )
            from_empty.setdefault(key, set()).add(item.counts["CHANGING"] + offset)
    within = {
        base: sum(1 for per in relative.values() if len(per.get(base, set())) > 1)
        for base in by_base
    }
    shared = [key for key, per in relative.items() if len(per) > 1]
    agreeing = 0
    for key in shared:
        values = [value for per in relative[key].values() for value in per]
        if len(values) != len(set(values)):
            agreeing += 1
    empty_disagreeing = sum(1 for key in shared if len(from_empty[key]) > 1)
    pairs: dict[str, int] = {}
    for key in shared:
        name = "+".join(b for b in by_base if b in relative[key])
        pairs[name] = pairs.get(name, 0) + 1
    return {
        "classes": len(relative),
        "classes_with_two_changing_counts_within_a_base": within,
        "classes_shared_by_bases": len(shared),
        "shared_classes_by_bases": dict(sorted(pairs.items())),
        "shared_classes_with_agreeing_relative_counts": agreeing,
        "shared_classes_with_two_counts_from_empty": empty_disagreeing,
    }


# ---------------------------------------------------------------------------
# The Lean countermodels, replayed in Python
# ---------------------------------------------------------------------------


def lean_witnesses() -> dict[str, tuple[Regime, tuple[Event, ...], Regime, tuple[Event, ...], str]]:
    """The three countermodels of `lean/SecondSuccession/Readings.lean`
    in the sealed Python grammar: two (base, history) pairs reaching one
    regime, and the reading under which their counts are claimed to
    differ.  The reading-L history is the sealed Python genesis followed
    by the requirement the sealed Lean reading-L regime carries."""
    history_l = tuple(GENESIS_L) + (Impose(0, 1),)
    reached_l = replay(history_l, EMPTY)
    rule_once: tuple[Event, ...] = (AdmitForm(1), AdmitRuleAll(0))
    return {
        "every_splits": (EMPTY, (), EMPTY, (Supply(ALPHABET.supply_token),), "EVERY"),
        "admitting_splits": (EMPTY, rule_once, EMPTY, rule_once + (AdmitRuleAll(0),), "ADMITTING"),
        "base_matters": (EMPTY, history_l, reached_l, (), "CHANGING"),
    }


def witness_report() -> dict[str, Any]:
    """Each countermodel replayed: both sides reach one regime, and the
    two counts under the claimed reading differ."""
    out: dict[str, Any] = {}
    for name, (base_a, hist_a, base_b, hist_b, reading) in sorted(lean_witnesses().items()):
        reached_a = replay(hist_a, base_a)
        reached_b = replay(hist_b, base_b)
        count_a = counts(base_a, hist_a)[reading]
        count_b = counts(base_b, hist_b)[reading]
        out[name] = {
            "reading": reading,
            "counts": [count_a, count_b],
            "same_regime": reached_a == reached_b,
            "claim_holds": reached_a == reached_b and count_a != count_b,
        }
    return out


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------


def sequenced(population: Population) -> dict[str, list[Sequenced]]:
    """Every sequence of every base, with its counts, in the enumerator's
    order."""
    out: dict[str, list[Sequenced]] = {}
    for rect in population.rects:
        out[rect.base] = [
            Sequenced(node.history, node.regime, counts(rect.regime, node.history))
            for node in rect.nodes
        ]
    return out


def all_reports(alphabet: Alphabet = ALPHABET) -> dict[str, Any]:
    """Everything this rung measures."""
    population = build_population(alphabet)
    replay_mismatches = 0
    for rect in population.rects:
        for node in rect.nodes:
            if replay(node.history, rect.regime) != node.regime:
                replay_mismatches += 1
    by_base = sequenced(population)
    bases = {
        rect.base: base_report(rect.base, rect.regime, by_base[rect.base])
        for rect in population.rects
    }
    return {
        "base_order": list(BASE_NAMES),
        "bases": bases,
        "replay_mismatches": replay_mismatches,
        "classes": class_report(population, by_base),
        "lean_witnesses": witness_report(),
    }


__all__ = [
    "ALPHABET",
    "READINGS",
    "Sequenced",
    "all_reports",
    "base_report",
    "build_population",
    "class_report",
    "counts",
    "element_count",
    "lean_witnesses",
    "sequenced",
    "splitting",
    "witness",
    "witness_report",
]
