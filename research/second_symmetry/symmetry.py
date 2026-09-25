"""The finite cross-check for rung five: the automorphisms of a regime
along a history.

Classification (assumption discipline):

* Everything here is metatheory apparatus layered on the sealed kernel,
  the sealed isomorphism procedure, and rung four's
  ``research/second_iso/iso_index.py`` (which consumes rung three's
  rectangle), all imported read-only through their public functions and
  pinned by blob in ``SOURCE_MANIFEST.json``.  No sibling source is
  copied.
* The rectangle and its three bases are rung three's, consumed unchanged
  through rung four's population.
* An AUTOMORPHISM is a bijection pair the sealed ``automorphisms``
  returns.  The set is checked here, at every regime reached, against a
  brute-force set over every bijection pair written in this file, and its
  size against rung four's brute-force count.
* An EDGE is a sequence other than the empty one, read as its last event
  applied to the regime its prefix reaches.  Every event of every
  sequence is the last event of exactly one edge.
* The enumeration is a FINITE COMPUTATION over a declared rectangle, run
  without any sealed pruning lemma.
* Nothing here is a theorem.  The theorems of this rung are in ``lean/``;
  this file checks their content by exhaustion on a rectangle and records
  the SIZES the theorems do not state.
"""

from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations
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
# defect rung three found live, and rung four recorded again.
from iso_index import (  # noqa: E402
    ALPHABET,
    ORBIT_BOUND,
    Population,
    brute_automorphism_count,
    build_population,
)
from index import history_descriptor, regime_shape  # noqa: E402
from nofirst import Alphabet  # noqa: E402
from derivation.iso import automorphisms, serialize  # noqa: E402
from derivation.model import (  # noqa: E402
    EMPTY,
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

Pair = tuple[tuple[int, ...], tuple[int, ...]]

KINDS: tuple[str, ...] = (
    "Supply",
    "AdmitDatum",
    "AdmitForm",
    "AdmitInst",
    "AdmitRuleAll",
    "Impose",
)
ADDING_KINDS: tuple[str, ...] = ("AdmitInst", "AdmitRuleAll", "Impose")
DIRECTIONS: tuple[str, ...] = ("up", "equal", "down")
SEQUENCE_CLASSES: tuple[str, ...] = ("CONSTANT", "RISING", "FALLING", "MIXED")


# ---------------------------------------------------------------------------
# Automorphism sets, two ways
# ---------------------------------------------------------------------------


class Automorphisms:
    """Automorphism sets of regimes, memoized.  Two procedures are kept
    apart: the sealed ``automorphisms``, which refines colours and
    searches only colour-preserving bijections, and ``brute`` below, which
    tries every bijection pair.  Neither is derived from the other."""

    def __init__(self) -> None:
        self._sealed: dict[Regime, frozenset[Pair]] = {}

    def of(self, regime: Regime) -> frozenset[Pair]:
        found = self._sealed.get(regime)
        if found is None:
            found = frozenset(automorphisms(regime, ORBIT_BOUND))
            self._sealed[regime] = found
        return found

    def size(self, regime: Regime) -> int:
        return len(self.of(regime))


def brute_automorphisms(regime: Regime) -> frozenset[Pair]:
    """Every bijection pair whose serialization equals the identity's,
    written independently of the sealed ``automorphisms``."""
    n, m = regime.n_data(), len(regime.forms)
    identity = serialize(regime, tuple(range(n)), tuple(range(m)))
    return frozenset(
        (pi, phi)
        for pi in permutations(range(n))
        for phi in permutations(range(m))
        if serialize(regime, pi, phi) == identity
    )


# ---------------------------------------------------------------------------
# Untouched indices, added elements, images
# ---------------------------------------------------------------------------


def untouched_data(regime: Regime) -> int:
    """Data named by no admitted instance and no admitted requirement."""
    touched: set[int] = set()
    for _form, args in regime.insts:
        touched.update(args)
    for i, j in regime.reqs:
        touched.update((i, j))
    return sum(1 for d in range(regime.n_data()) if d not in touched)


def untouched_forms(regime: Regime, arity: int) -> int:
    """Forms of the given arity used by no admitted instance and named by
    no admitted rule."""
    used = {form for form, _args in regime.insts} | set(regime.rules)
    return sum(
        1
        for f, a in enumerate(regime.forms)
        if a == arity and f not in used
    )


Element = tuple[str, Any]


def added_element(before: Regime, event: Event, after: Regime) -> Optional[Element]:
    """The one element a changing adding event admits, or ``None`` for any
    other edge."""
    if after == before:
        return None
    if isinstance(event, AdmitInst):
        return ("inst", (event.form, tuple(event.args)))
    if isinstance(event, AdmitRuleAll):
        return ("rule", event.form)
    if isinstance(event, Impose):
        return ("req", (event.i, event.j))
    return None


def image(pair: Pair, element: Element) -> object:
    """Where a bijection pair carries an added element.  A requirement is
    re-ordered, as the sealed serialization orders it."""
    pi, phi = pair
    kind, value = element
    if kind == "inst":
        form, args = value
        return (phi[form], tuple(pi[a] for a in args))
    if kind == "rule":
        return phi[value]
    i, j = value
    return (min(pi[i], pi[j]), max(pi[i], pi[j]))


def element_count(regime: Regime) -> int:
    """Data, forms, instances, rules and requirements, counted."""
    return (
        regime.n_data()
        + len(regime.forms)
        + len(regime.insts)
        + len(regime.rules)
        + len(regime.reqs)
    )


def direction(before: int, after: int) -> str:
    if after > before:
        return "up"
    if after < before:
        return "down"
    return "equal"


def event_kind(event: Event) -> str:
    return type(event).__name__


# ---------------------------------------------------------------------------
# The edges
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Edge:
    base: str
    history: tuple[Event, ...]
    before: Regime
    after: Regime

    @property
    def event(self) -> Event:
        return self.history[-1]

    @property
    def kind(self) -> str:
        return event_kind(self.event)

    @property
    def changing(self) -> bool:
        return self.after != self.before


def edges(population: Population) -> list[Edge]:
    """Every edge of every base's rectangle, in the enumerator's order."""
    out: list[Edge] = []
    for rect in population.rects:
        regimes = rect.by_history()
        for node in rect.nodes:
            if not node.history:
                continue
            out.append(
                Edge(rect.base, node.history, regimes[node.history[:-1]], node.regime)
            )
    return out


def automorphism_crosscheck(
    population: Population, auts: Automorphisms
) -> dict[str, Any]:
    """At every distinct regime reached: the sealed set against the brute
    set, and its size against rung four's brute-force count."""
    set_disagreements = 0
    count_disagreements = 0
    sizes: dict[int, int] = {}
    for regime in population.regimes:
        sealed = auts.of(regime)
        if sealed != brute_automorphisms(regime):
            set_disagreements += 1
        if len(sealed) != brute_automorphism_count(regime):
            count_disagreements += 1
        sizes[len(sealed)] = sizes.get(len(sealed), 0) + 1
    return {
        "regimes": len(population.regimes),
        "set_disagreements": set_disagreements,
        "count_disagreements": count_disagreements,
        "smallest": min(sizes),
        "largest": max(sizes),
        "size_distribution": {str(k): sizes[k] for k in sorted(sizes)},
    }


def empty_tally() -> dict[str, dict[str, dict[str, int]]]:
    return {
        kind: {
            status: {d: 0 for d in DIRECTIONS} for status in ("changing", "unchanging")
        }
        for kind in KINDS
    }


def edge_report(all_edges: Sequence[Edge], auts: Automorphisms) -> dict[str, Any]:
    """Direction by kind; the datum, form and meet laws; the extreme
    ratios; the element count."""
    tally = empty_tally()
    datum_violations = 0
    datum_checked = 0
    form_violations = 0
    form_checked = 0
    meet_violations = 0
    ratio_violations = 0
    meet_checked = 0
    count_violations = 0
    up_max = Fraction(1)
    up_kinds: set[str] = set()
    down_max = Fraction(1)
    down_kinds: set[str] = set()
    for edge in all_edges:
        before_set = auts.of(edge.before)
        after_set = auts.of(edge.after)
        size_before, size_after = len(before_set), len(after_set)
        way = direction(size_before, size_after)
        status = "changing" if edge.changing else "unchanging"
        tally[edge.kind][status][way] += 1

        grown = element_count(edge.after) - element_count(edge.before)
        if grown != (1 if edge.changing else 0):
            count_violations += 1

        if way == "up":
            ratio = Fraction(size_after, size_before)
            if ratio > up_max:
                up_max, up_kinds = ratio, {edge.kind}
            elif ratio == up_max:
                up_kinds.add(edge.kind)
        elif way == "down":
            ratio = Fraction(size_before, size_after)
            if ratio > down_max:
                down_max, down_kinds = ratio, {edge.kind}
            elif ratio == down_max:
                down_kinds.add(edge.kind)

        if not edge.changing:
            continue
        if isinstance(edge.event, AdmitDatum):
            datum_checked += 1
            if size_after != size_before * (untouched_data(edge.before) + 1):
                datum_violations += 1
        elif isinstance(edge.event, AdmitForm):
            form_checked += 1
            factor = untouched_forms(edge.before, edge.event.arity) + 1
            if size_after != size_before * factor:
                form_violations += 1
        element = added_element(edge.before, edge.event, edge.after)
        if element is None:
            continue
        meet_checked += 1
        common = before_set & after_set
        fix_before = frozenset(p for p in before_set if image(p, element) == element[1])
        fix_after = frozenset(p for p in after_set if image(p, element) == element[1])
        if not (common == fix_before == fix_after):
            meet_violations += 1
        images_before = {image(p, element) for p in before_set}
        images_after = {image(p, element) for p in after_set}
        if size_before * len(images_after) != size_after * len(images_before):
            ratio_violations += 1
    return {
        "edges": len(all_edges),
        "by_kind": tally,
        "datum_law": {"checked": datum_checked, "violations": datum_violations},
        "form_law": {"checked": form_checked, "violations": form_violations},
        "meet_law": {
            "checked": meet_checked,
            "set_violations": meet_violations,
            "ratio_violations": ratio_violations,
        },
        "element_count_violations": count_violations,
        "largest_rise": {"ratio": str(up_max), "kinds": sorted(up_kinds)},
        "largest_fall": {"ratio": str(down_max), "kinds": sorted(down_kinds)},
    }


# ---------------------------------------------------------------------------
# Sequences
# ---------------------------------------------------------------------------


def sequence_class(sizes: Sequence[int]) -> str:
    """CONSTANT, RISING (never lower, not constant), FALLING (never higher,
    not constant) or MIXED, read off the sizes along the prefixes."""
    rises = any(b > a for a, b in zip(sizes, sizes[1:]))
    falls = any(b < a for a, b in zip(sizes, sizes[1:]))
    if rises and falls:
        return "MIXED"
    if rises:
        return "RISING"
    if falls:
        return "FALLING"
    return "CONSTANT"


def sequence_report(population: Population, auts: Automorphisms) -> dict[str, Any]:
    """Every sequence classed by its sizes; the shortest MIXED one; and
    whether any sequence reaches, by a changing event, a class an earlier
    prefix reached."""
    counts: dict[str, dict[str, int]] = {}
    shortest: Optional[tuple[int, str, tuple[str, ...]]] = None
    revisit_edges = 0
    for rect in population.rects:
        regimes = rect.by_history()
        per = {name: 0 for name in SEQUENCE_CLASSES}
        for node in rect.nodes:
            prefixes = [regimes[node.history[:k]] for k in range(len(node.history) + 1)]
            sizes = [auts.size(r) for r in prefixes]
            cls = sequence_class(sizes)
            per[cls] += 1
            if cls == "MIXED":
                candidate = (len(node.history), rect.base, history_descriptor(node.history))
                if shortest is None or candidate < shortest:
                    shortest = candidate
            if node.history and prefixes[-1] != prefixes[-2]:
                key = population.keys.key(prefixes[-1])
                if any(population.keys.key(r) == key for r in prefixes[:-1]):
                    revisit_edges += 1
        counts[rect.base] = per
    witness: Optional[dict[str, Any]] = None
    if shortest is not None:
        witness = {
            "length": shortest[0],
            "base": shortest[1],
            "history": list(shortest[2]),
        }
    return {
        "classes_by_base": counts,
        "shortest_mixed": witness,
        "class_revisits_after_a_changing_event": revisit_edges,
    }


# ---------------------------------------------------------------------------
# The Lean witnesses, replayed in Python
# ---------------------------------------------------------------------------

_FRESH = ALPHABET.fresh_tokens


def lean_witnesses() -> dict[str, tuple[tuple[Event, ...], Event, Pair, str]]:
    """The six regimes of `lean/SecondSymmetry/Witness.lean`, reached from
    the empty regime by declared events, with the added event, the
    exhibited bijection pair, and which side the pair is claimed on:
    LOSS (an automorphism before, not after) or GAIN (after, not before)."""
    two_unary: tuple[Event, ...] = (
        AdmitDatum(_FRESH[0]),
        AdmitDatum(_FRESH[1]),
        AdmitForm(1),
    )
    two_forms: tuple[Event, ...] = (AdmitForm(1), AdmitForm(1))
    three: tuple[Event, ...] = (
        AdmitDatum(_FRESH[0]),
        AdmitDatum(_FRESH[1]),
        AdmitDatum(_FRESH[2]),
    )
    return {
        "inst_loss": (two_unary, AdmitInst(0, (0,)), ((1, 0), (0,)), "LOSS"),
        "inst_gain": (
            two_unary + (AdmitInst(0, (0,)),),
            AdmitInst(0, (1,)),
            ((1, 0), (0,)),
            "GAIN",
        ),
        "rule_loss": (two_forms, AdmitRuleAll(0), ((), (1, 0)), "LOSS"),
        "rule_gain": (two_forms + (AdmitRuleAll(0),), AdmitRuleAll(1), ((), (1, 0)), "GAIN"),
        "req_loss": (three, Impose(0, 1), ((0, 2, 1), ()), "LOSS"),
        "req_gain": (three + (Impose(0, 1),), Impose(1, 2), ((2, 1, 0), ()), "GAIN"),
    }


def witness_report(auts: Automorphisms) -> dict[str, Any]:
    """Each Lean witness replayed: its regime's shape, both sizes, and
    whether the exhibited pair sits on the claimed side only."""
    out: dict[str, Any] = {}
    for name, (prefix, event, pair, side) in sorted(lean_witnesses().items()):
        before = replay(prefix, EMPTY)
        after = step(before, event)
        in_before = pair in auts.of(before)
        in_after = pair in auts.of(after)
        holds = (in_before and not in_after) if side == "LOSS" else (
            in_after and not in_before
        )
        out[name] = {
            "side": side,
            "regime_before": regime_shape(before),
            "sizes": [auts.size(before), auts.size(after)],
            "claim_holds": holds,
        }
    return out


def all_reports(alphabet: Alphabet = ALPHABET) -> dict[str, Any]:
    """Everything this rung measures."""
    population = build_population(alphabet)
    auts = Automorphisms()
    replay_mismatches = 0
    for rect in population.rects:
        for node in rect.nodes:
            if replay(node.history, rect.regime) != node.regime:
                replay_mismatches += 1
    all_edges = edges(population)
    return {
        "bases": {
            rect.base: {"sequences": len(rect.nodes), "edges": len(rect.nodes) - 1}
            for rect in population.rects
        },
        "replay_mismatches": replay_mismatches,
        "automorphisms": automorphism_crosscheck(population, auts),
        "edges": edge_report(all_edges, auts),
        "sequences": sequence_report(population, auts),
        "lean_witnesses": witness_report(auts),
    }


__all__ = [
    "ADDING_KINDS",
    "ALPHABET",
    "Automorphisms",
    "DIRECTIONS",
    "Edge",
    "KINDS",
    "SEQUENCE_CLASSES",
    "added_element",
    "all_reports",
    "automorphism_crosscheck",
    "brute_automorphisms",
    "build_population",
    "direction",
    "edge_report",
    "edges",
    "element_count",
    "event_kind",
    "image",
    "lean_witnesses",
    "sequence_class",
    "sequence_report",
    "untouched_data",
    "untouched_forms",
    "witness_report",
]
