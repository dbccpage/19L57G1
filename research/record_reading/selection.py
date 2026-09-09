"""A class of laws and a discriminating input.

AuthorityEffect: None.  Mirrors ``lean/Select.lean``.

The protocol is declared here, before any readout is seen: the two classes
of laws, the inputs an experimenter may choose (a start datum and a scale),
the fuel, and which observation is taken as "seen" (the artifact's recorded
``forever`` run, read at the declared scale).  Every law of a class is
retained that replays the seen observation — by running it, not by
reasoning — and the retained laws are then separated by the declared inputs
only.  What no declared input separates is the residual: the tape
identifies a law up to its next-value function on the pairs the runs reach
(``Select.obs_bisim``), and never the index of the operation that carried
the datum (``Select.forever_indistinguishable``).  The class is not narrowed
after the readout; the constants below are the whole protocol.

Each retained law is run once per start datum at the finest scale; the
readout of a coarser scale is the prefix of that run (``Select.obs_take``,
``Record.robs_prefix_add``), so the separation is computed from those runs
without running the law again.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import product
from typing import Sequence, Union

import control as ct
from execution import Graph, lookup
import limits as lm
import record as rc
import translation as tr

Word = tuple[int, ...]
JsonObj = dict[str, object]
Law = Union[ct.Controlled, rc.Recorded]
Input = tuple[int, int]
Signature = tuple[Word, ...]

# --- the protocol, declared before any readout ------------------------------
STARTS: tuple[int, ...] = (0, 1, 2)
MAX_SCALE = 8
SCALES: tuple[int, ...] = tuple(range(1, MAX_SCALE + 1))
FUEL = MAX_SCALE
INPUTS: tuple[Input, ...] = tuple((start, scale) for start in STARTS for scale in SCALES)
OBSERVED_START = 0
OBSERVED_SCALE = 3
OBSERVED_PROGRAM = "forever"
READOUT = "the tape after the scale's number of steps of the deterministic runner"
CLASSES = {
    "memoryless": "every program on the identified setting with at most one operation enabled per datum",
    "record": "every record-reading program on the identified setting with at most one operation enabled "
              "per (previous, active) pair",
}


class SelectError(ValueError):
    """A named refusal."""


# ---------------------------------------------------------------------------
# The classes, the observation, the next-value function
# ---------------------------------------------------------------------------


def memoryless_class(F: tr.FiniteSetting) -> list[ct.Controlled]:
    return lm.deterministic_programs(F)


def record_class(F: tr.FiniteSetting) -> list[rc.Recorded]:
    """Every record-reading program with at most one operation enabled at
    each (previous, active) pair."""
    count = len(F.ops)
    pairs = [(p, x) for p in range(F.n) for x in range(F.n)]
    out: list[rc.Recorded] = []
    for choice in product(range(-1, count), repeat=len(pairs)):
        out.append(rc.Recorded(F, frozenset((p, x, k) for (p, x), k in zip(pairs, choice) if k >= 0)))
    return out


def observe(law: Law, start: int, scale: int) -> Word:
    """The readout of one experiment: run the law from the start datum with
    the declared fuel and read the tape at the scale."""
    if isinstance(law, ct.Controlled):
        return lm.obs(scale, ct.init(law, start, FUEL))
    return rc.robs(scale, rc.rinit(law, start, FUEL))


def survivors(laws: Sequence[Law], observation: Word, start: int = OBSERVED_START,
              scale: int = OBSERVED_SCALE) -> list[Law]:
    """Retain every law whose run replays the seen observation."""
    return [law for law in laws if observe(law, start, scale) == observation]


@lru_cache(maxsize=None)
def _loaded(law: Law) -> tuple[Graph, int]:
    if isinstance(law, ct.Controlled):
        return ct.program(law), ct.nops(law)
    return rc.rprogram(law), len(law.F.ops)


def next_value(law: Law, p: int, x: int) -> int | None:
    """The Lean ``nextValue``, read from the program: the value of the one
    enabled operation at ``x`` (after ``p`` for a record law), or ``None``."""
    g, count = _loaded(law)
    en = ct.enabled_at(g, count, x) if isinstance(law, ct.Controlled) else rc.renabled_at(g, count, p, x)
    return lookup(3 + en[0], x, g) if len(en) == 1 else None


def signature(law: Law) -> Signature:
    """One run per declared start at the finest scale."""
    return tuple(observe(law, start, MAX_SCALE) for start in STARTS)


def signatures(laws: Sequence[Law]) -> list[Signature]:
    return [signature(law) for law in laws]


def readout_of(sig: Signature, inp: Input) -> Word:
    """The readout of a declared input, as the prefix of the finest run."""
    start, scale = inp
    return sig[STARTS.index(start)][: scale + 1]


def reached_pairs(sig: Signature) -> frozenset[tuple[int, int]]:
    """The (previous, active) pairs at which the runs read the law's next
    value: every position followed by another entry, and the last position
    when the run stopped before the finest scale."""
    out: set[tuple[int, int]] = set()
    for tape in sig:
        for i in range(len(tape)):
            if i + 1 < len(tape) or len(tape) - 1 < MAX_SCALE:
                out.add((tape[i - 1] if i >= 1 else tape[i], tape[i]))
    return frozenset(out)


# ---------------------------------------------------------------------------
# Separation by the declared inputs
# ---------------------------------------------------------------------------


def partition(sigs: Sequence[Signature], inputs: Sequence[Input]) -> dict[tuple[Word, ...], list[int]]:
    classes: dict[tuple[Word, ...], list[int]] = {}
    for i, sig in enumerate(sigs):
        classes.setdefault(tuple(readout_of(sig, inp) for inp in inputs), []).append(i)
    return classes


def burden(laws: Sequence[Law], sigs: Sequence[Signature] | None = None) -> tuple[list[JsonObj], int]:
    """The greedy experiment sequence: at each step the declared input that
    refines the partition of the retained laws most (ties to the earlier
    declared input); stop when no input refines it.  Returns the sequence
    with the class counts, and the residual class count."""
    sigs = signatures(laws) if sigs is None else sigs
    chosen: list[Input] = []
    count = len(partition(sigs, chosen))
    sequence: list[JsonObj] = []
    while True:
        best: tuple[int, Input] | None = None
        for inp in INPUTS:
            if inp in chosen:
                continue
            n = len(partition(sigs, [*chosen, inp]))
            if best is None or n > best[0]:
                best = (n, inp)
        if best is None or best[0] <= count:
            return sequence, count
        chosen.append(best[1])
        count = best[0]
        sequence.append({"start": best[1][0], "scale": best[1][1], "classes_after": count})


def residual_reason(laws: Sequence[Law], sigs: Sequence[Signature] | None = None) -> JsonObj:
    """Check the reason for the residual against the programs themselves:
    within a class of laws no declared input separates, the next-value
    function read from the program agrees on every pair the runs reach
    (the computed counterpart of ``Select.stepDet_spec``); between two
    classes it differs on some reached pair (the localized converse of
    ``Select.obs_bisim``)."""
    sigs = signatures(laws) if sigs is None else sigs
    classes = list(partition(sigs, list(INPUTS)).values())
    within = True
    for members in classes:
        pairs = sorted(reached_pairs(sigs[members[0]]))
        values = {tuple(next_value(laws[i], p, x) for p, x in pairs) for i in members}
        if len(values) != 1:
            within = False
    between = True
    for i, a in enumerate(classes):
        for b in classes[i + 1:]:
            union = reached_pairs(sigs[a[0]]) | reached_pairs(sigs[b[0]])
            if all(next_value(laws[a[0]], p, x) == next_value(laws[b[0]], p, x) for p, x in union):
                between = False
    return {
        "residual_classes": len(classes),
        "largest_class": max(len(m) for m in classes),
        "within_a_class_the_next_value_function_agrees_on_reached_pairs": within,
        "between_classes_it_differs_on_a_reached_pair": between,
    }


# ---------------------------------------------------------------------------
# The experiment
# ---------------------------------------------------------------------------


def enablements(law: Law) -> list[list[int]]:
    if isinstance(law, ct.Controlled):
        return sorted(list(pair) for pair in law.ctrl)
    return sorted(list(triple) for triple in law.hctrl)


def contains(laws: Sequence[Law], law: Law) -> bool:
    return any(other == law for other in laws)


def experiment(F: tr.FiniteSetting, observation: Word, forever: ct.Controlled) -> JsonObj:
    """The whole protocol on the identified setting: both classes, the
    survivors of the seen observation, the greedy burden, the residual and
    its reason, the exhibited ambiguity and the exhibited discrimination."""
    if len(observation) != OBSERVED_SCALE + 1:
        raise SelectError(f"the seen observation has {len(observation)} entries, not scale {OBSERVED_SCALE} + 1")
    climb_first = ct.Controlled(F, frozenset({(0, 2), (1, 0), (2, 0)}))
    turncoat = rc.turncoat(F)
    lifted = rc.lift(forever)
    results: JsonObj = {}
    kept_by_class: dict[str, list[Law]] = {}
    for name, laws in (("memoryless", memoryless_class(F)), ("record", record_class(F))):
        kept = survivors(laws, observation)
        if not kept:
            raise SelectError(f"no law of the {name} class replays the seen observation")
        kept_by_class[name] = kept
        sigs = signatures(kept)
        sequence, residual = burden(kept, sigs)
        results[name] = {
            "class": CLASSES[name],
            "class_size": len(laws),
            "survivors": len(kept),
            "experiments": sequence,
            "burden": len(sequence),
            "residual": residual_reason(kept, sigs),
            "unique_within_class": residual == 1 and len(kept) == 1,
        }
    if not (contains(kept_by_class["memoryless"], forever) and contains(kept_by_class["memoryless"], climb_first)):
        raise SelectError("the exhibited ambiguous pair does not survive the seen observation")
    if not (contains(kept_by_class["record"], turncoat) and contains(kept_by_class["record"], lifted)):
        raise SelectError("the exhibited discriminated pair does not survive the seen observation")
    return {
        "declared_before_readout": {
            "classes": CLASSES, "starts": list(STARTS), "scales": list(SCALES), "fuel": FUEL,
            "observed_program": OBSERVED_PROGRAM, "observed_start": OBSERVED_START,
            "observed_scale": OBSERVED_SCALE, "readout": READOUT,
            "survivor_rule": "a law is retained when its own run from the observed start at the observed "
                             "scale reads the seen observation; no law is removed afterwards",
            "separation_rule": "the retained laws are separated by the readouts of the declared inputs only, "
                               "each read as the prefix of one run per start at the finest scale",
        },
        "observation": list(observation),
        "classes": results,
        "ambiguity_exhibited": {
            "forever": enablements(forever),
            "climbFirst": enablements(climb_first),
            "programs_differ": ct.program(forever) != ct.program(climb_first),
            "both_survive": True,
            "separated_by_a_declared_input": signature(forever) != signature(climb_first),
            "why": "both carry 0 to 1: the tape does not say which operation carried the datum "
                   "(Select.forever_indistinguishable, from Select.obs_bisim)",
        },
        "discrimination_exhibited": {
            "turncoat": enablements(turncoat),
            "lift_forever": enablements(lifted),
            "agree_at_the_seen_observation": observe(turncoat, 0, 3) == observe(lifted, 0, 3),
            "separated_by_scale": {"start": 0, "scale": 4,
                                   "readouts": [list(observe(turncoat, 0, 4)), list(observe(lifted, 0, 4))]},
            "separated_by_start": {"start": 2, "scale": 2,
                                   "readouts": [list(observe(turncoat, 2, 2)), list(observe(lifted, 2, 2))]},
        },
        "missing_axiom": "an observable that reads which operation fired, not only where the datum went: the "
                         "tape identifies a law up to its next-value function on the pairs the runs reach "
                         "(Select.obs_bisim) and the residual classes are exactly those (checked above)",
    }
