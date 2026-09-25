"""The finite cross-check for rung seven: duration under the CHANGING
reading.

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
* A ROUND is an event after which the regime differs; a GROWTH is a round
  after which the regime has more data; a REST ROUND is any other round.
  The DURATION VECTOR of a history is its rest rounds counted by the
  number of growths taken before them.  All of it is counted here by
  stepping the sealed ``step``, never by a formula of this file.
* The LEVEL of a new element and the ENVELOPE of a base and a regime are
  the ones `PROMPT.md` declares.  The envelope is enumerated here by
  exhaustion over tuples, never by a closed form.
* The enumeration is a FINITE COMPUTATION over a declared rectangle, run
  without any sealed pruning lemma.
* Nothing here is a theorem.  The theorems of this rung are in ``lean/``;
  this file checks their content by exhaustion on a rectangle and records
  what the theorems do not state -- above all, that the vectors reached
  are exactly the envelope.
"""

from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass
from typing import Any, Callable, Optional, Sequence

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
# defect rung three found live, and rungs four to six recorded again.
from iso_index import ALPHABET, Population, build_population  # noqa: E402
from index import BASE_NAMES, history_descriptor  # noqa: E402
from nofirst import Alphabet  # noqa: E402
from derivation.iso import CanonKey  # noqa: E402
from derivation.model import (  # noqa: E402
    EMPTY,
    AdmitDatum,
    AdmitForm,
    Event,
    Impose,
    Regime,
    replay,
    step,
)

if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))

Vector = tuple[int, ...]


# ---------------------------------------------------------------------------
# The duration vector of a history
# ---------------------------------------------------------------------------


def vector(base: Regime, history: Sequence[Event]) -> Vector:
    """The rest rounds of a history, counted by the number of growths
    taken before them.  A history the sealed step refuses raises, as it
    does in the sealed replay."""
    segments = [0]
    current = base
    for event in history:
        after = step(current, event)
        if after != current:
            if after.n_data() > current.n_data():
                segments.append(0)
            else:
                segments[-1] += 1
        current = after
    return tuple(segments)


def gaps(vec: Vector) -> Vector:
    """The durations between growths: every segment but the lead and the
    tail."""
    return vec[1:-1]


# ---------------------------------------------------------------------------
# Levels and the envelope
# ---------------------------------------------------------------------------


def levels(base: Regime, regime: Regime) -> tuple[int, ...]:
    """The level of every new element of the regime other than a datum,
    sorted: zero for a form and a uniform rule; for an instance or a
    requirement, the largest datum index it names less the base's number
    of data plus one, and zero when that is negative."""
    held = base.n_data()
    out: list[int] = [0] * (len(regime.forms) - len(base.forms))
    out.extend(0 for _ in regime.rules - base.rules)
    for _, args in regime.insts - base.insts:
        out.append(max(0, max(args) - held + 1))
    for _, j in regime.reqs - base.reqs:
        out.append(max(0, j - held + 1))
    return tuple(sorted(out))


def envelope(base: Regime, regime: Regime) -> frozenset[Vector]:
    """Every tuple with one entry per segment position, summing to the
    number of new elements other than data, whose sum from each position
    on is at least the number of new elements of that level or above.
    Enumerated by exhaustion over all such tuples."""
    positions = regime.n_data() - base.n_data() + 1
    found = levels(base, regime)
    total = len(found)
    needed = [sum(1 for level in found if level >= i) for i in range(positions)]

    def compositions(remaining: int, parts: int) -> list[Vector]:
        if parts == 1:
            return [(remaining,)]
        return [
            (head,) + tail
            for head in range(remaining + 1)
            for tail in compositions(remaining - head, parts - 1)
        ]

    return frozenset(
        vec
        for vec in compositions(total, positions)
        if all(sum(vec[i:]) >= needed[i] for i in range(positions))
    )


# ---------------------------------------------------------------------------
# One base
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Sequenced:
    """One sequence of a base's rectangle, with its duration vector."""

    history: tuple[Event, ...]
    regime: Regime
    vector: Vector

    def order(self) -> tuple[int, tuple[str, ...]]:
        return (len(self.history), history_descriptor(self.history))


def splitting(
    groups: dict[Regime, list[Sequenced]], read: Callable[[Sequenced], Vector]
) -> tuple[int, Optional[tuple[Sequenced, Sequenced]]]:
    """The number of regimes reached with two values of ``read``, and the
    shortest splitting sequence with the first sequence it splits from:
    the least sequence, in order of length and then descriptor, whose
    value differs from that of a sequence of no greater length reaching
    the same regime."""
    split = 0
    best: Optional[tuple[Sequenced, Sequenced]] = None
    for members in groups.values():
        if len({read(m) for m in members}) > 1:
            split += 1
        ordered = sorted(members, key=Sequenced.order)
        for later in ordered:
            earlier = next(
                (
                    m
                    for m in ordered
                    if len(m.history) <= len(later.history) and read(m) != read(later)
                ),
                None,
            )
            if earlier is None:
                continue
            if best is None or later.order() < best[1].order():
                best = (earlier, later)
            break
    return split, best


def witness(
    pair: Optional[tuple[Sequenced, Sequenced]], read: Callable[[Sequenced], Vector]
) -> Optional[dict[str, Any]]:
    if pair is None:
        return None
    earlier, later = pair
    return {
        "length": len(later.history),
        "history": list(history_descriptor(later.history)),
        "value": list(read(later)),
        "splits_from": list(history_descriptor(earlier.history)),
        "splits_from_value": list(read(earlier)),
    }


def _whole(item: Sequenced) -> Vector:
    return item.vector


def _between(item: Sequenced) -> Vector:
    return gaps(item.vector)


def base_report(base_regime: Regime, sequences: Sequence[Sequenced]) -> dict[str, Any]:
    """Every measurement at one base: the shape laws of the vector, the
    envelope in both directions, the split regimes and the shortest
    splitting sequences, and the regimes whose envelope has one tuple."""
    groups: dict[Regime, list[Sequenced]] = {}
    for item in sequences:
        groups.setdefault(item.regime, []).append(item)
    held = base_regime.n_data()
    length_violations = 0
    sum_violations = 0
    outside = 0
    for item in sequences:
        new_data = item.regime.n_data() - held
        if len(item.vector) != new_data + 1:
            length_violations += 1
        if sum(item.vector) != len(levels(base_regime, item.regime)):
            sum_violations += 1
        if item.vector not in envelope(base_regime, item.regime):
            outside += 1
    unreached = 0
    one_tuple = 0
    one_vector = 0
    one_iff_violations = 0
    tail_only = 0
    for regime, members in groups.items():
        allowed = envelope(base_regime, regime)
        reached = {m.vector for m in members}
        if reached != allowed:
            unreached += 1
        if len(allowed) == 1:
            one_tuple += 1
            only = next(iter(allowed))
            if len(only) > 1 and only[-1] >= 1:
                tail_only += 1
        if len(reached) == 1:
            one_vector += 1
        if (len(allowed) == 1) != (len(reached) == 1):
            one_iff_violations += 1
    vector_split, vector_pair = splitting(groups, _whole)
    gap_split, gap_pair = splitting(groups, _between)
    return {
        "sequences": len(sequences),
        "distinct_regimes": len(groups),
        "base_data": held,
        "length_violations": length_violations,
        "sum_violations": sum_violations,
        "vectors_outside_envelope": outside,
        "regimes_with_unreached_or_extra_tuples": unreached,
        "regimes_with_one_tuple_envelope": one_tuple,
        "regimes_reached_with_one_vector": one_vector,
        "one_tuple_iff_one_vector_violations": one_iff_violations,
        "tail_only_regimes": tail_only,
        "vector_split_regimes": vector_split,
        "gap_split_regimes": gap_split,
        "shortest_vector_splitting_sequence": witness(vector_pair, _whole),
        "shortest_gap_splitting_sequence": witness(gap_pair, _between),
    }


# ---------------------------------------------------------------------------
# Classes, within a base
# ---------------------------------------------------------------------------


def class_report(
    population: Population,
    base_regimes: dict[str, Regime],
    by_base: dict[str, list[Sequenced]],
) -> dict[str, Any]:
    """Taken up to the implemented isomorphism, within each base: classes
    reached with two vectors, with two vector sums, and carrying regimes
    with two envelopes."""
    two_vectors: dict[str, int] = {}
    two_sums: dict[str, int] = {}
    two_envelopes: dict[str, int] = {}
    classes: dict[str, int] = {}
    for base, sequences in by_base.items():
        vectors: dict[CanonKey, set[Vector]] = {}
        envelopes: dict[CanonKey, set[frozenset[Vector]]] = {}
        for item in sequences:
            key = population.keys.key(item.regime)
            vectors.setdefault(key, set()).add(item.vector)
            envelopes.setdefault(key, set()).add(envelope(base_regimes[base], item.regime))
        classes[base] = len(vectors)
        two_vectors[base] = sum(1 for found in vectors.values() if len(found) > 1)
        two_sums[base] = sum(
            1 for found in vectors.values() if len({sum(v) for v in found}) > 1
        )
        two_envelopes[base] = sum(1 for found in envelopes.values() if len(found) > 1)
    return {
        "classes": classes,
        "classes_with_two_vectors": two_vectors,
        "classes_with_two_sums": two_sums,
        "classes_with_two_envelopes": two_envelopes,
    }


# ---------------------------------------------------------------------------
# The Lean countermodels, replayed in Python
# ---------------------------------------------------------------------------


def lean_witnesses() -> dict[str, tuple[tuple[Event, ...], tuple[Event, ...], int]]:
    """The two countermodels of `lean/SecondDuration/Gaps.lean` in the
    sealed Python grammar, from the sealed empty regime: two histories
    reaching one regime, and the segment position at which their vectors
    are claimed to differ."""
    first, second = ALPHABET.fresh_tokens[0], ALPHABET.fresh_tokens[1]
    return {
        "lead_splits": (
            (AdmitForm(1), AdmitDatum(first)),
            (AdmitDatum(first), AdmitForm(1)),
            0,
        ),
        "gap_splits": (
            (AdmitDatum(first), AdmitForm(1), AdmitDatum(second)),
            (AdmitDatum(first), AdmitDatum(second), AdmitForm(1)),
            1,
        ),
    }


def pinned_history() -> tuple[Event, ...]:
    """A history reaching the regime of `pinned_by_requirement`: two data
    and the one requirement between them."""
    first, second = ALPHABET.fresh_tokens[0], ALPHABET.fresh_tokens[1]
    return (AdmitDatum(first), AdmitDatum(second), Impose(0, 1))


def witness_report() -> dict[str, Any]:
    """Each countermodel replayed: both sides reach one regime, and the
    claimed segments differ, one against zero.  The pinned regime has an
    envelope of one tuple, whose one rest round is in the tail."""
    out: dict[str, Any] = {}
    for name, (left, right, position) in sorted(lean_witnesses().items()):
        values = [vector(EMPTY, left)[position], vector(EMPTY, right)[position]]
        same = replay(left, EMPTY) == replay(right, EMPTY)
        out[name] = {
            "position": position,
            "segments": values,
            "same_regime": same,
            "claim_holds": same and values == [1, 0],
        }
    pinned = replay(pinned_history(), EMPTY)
    allowed = sorted(envelope(EMPTY, pinned))
    out["pinned_by_requirement"] = {
        "envelope": [list(v) for v in allowed],
        "vector": list(vector(EMPTY, pinned_history())),
        "claim_holds": allowed == [(0, 0, 1)],
    }
    return out


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------


def sequenced(population: Population) -> dict[str, list[Sequenced]]:
    """Every sequence of every base, with its vector, in the enumerator's
    order."""
    out: dict[str, list[Sequenced]] = {}
    for rect in population.rects:
        out[rect.base] = [
            Sequenced(node.history, node.regime, vector(rect.regime, node.history))
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
    base_regimes = {rect.base: rect.regime for rect in population.rects}
    bases = {
        rect.base: base_report(rect.regime, by_base[rect.base])
        for rect in population.rects
    }
    return {
        "base_order": list(BASE_NAMES),
        "bases": bases,
        "replay_mismatches": replay_mismatches,
        "classes": class_report(population, base_regimes, by_base),
        "lean_witnesses": witness_report(),
    }


__all__ = [
    "ALPHABET",
    "Sequenced",
    "all_reports",
    "base_report",
    "build_population",
    "class_report",
    "envelope",
    "gaps",
    "lean_witnesses",
    "levels",
    "pinned_history",
    "sequenced",
    "splitting",
    "vector",
    "witness",
    "witness_report",
]
