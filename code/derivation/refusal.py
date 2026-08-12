"""Refusal as a difference source: discipline comparison.

Classification: metatheory apparatus for
``paper/refusal_difference.md``.  Deterministic BFS reachability over a
reduced admission signature, comparing five re-admission disciplines
plus the occurrence and second-token baselines, without assuming that
refusal, repetition, occurrence, and state difference are equivalent.

State: admitted tokens in order, discipline-tagged indices, a refusal
counter, one optional unary form with its instances.  Observables: the
unary instances and (where the discipline declares it) the tag.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Callable, Optional, Union

Token = str


@dataclass(frozen=True)
class Sup:
    tok: Token


@dataclass(frozen=True)
class Adm:
    tok: Token


@dataclass(frozen=True)
class Form:
    pass


@dataclass(frozen=True)
class Inst:
    idx: int


REv = Union[Sup, Adm, Form, Inst]


@dataclass(frozen=True)
class RSt:
    data: tuple[Token, ...]
    tags: frozenset[int]
    refusals: int
    has_form: bool
    insts: frozenset[int]

    def json(self) -> dict[str, object]:
        return {
            "data": list(self.data),
            "tags": sorted(self.tags),
            "refusals": self.refusals,
            "has_form": self.has_form,
            "insts": sorted(self.insts),
        }


EMPTY = RSt((), frozenset(), 0, False, frozenset())

Discipline = Callable[[RSt, Token], RSt]


def _append(s: RSt, tok: Token, tag: bool) -> RSt:
    new_tags = s.tags | {len(s.data)} if tag else s.tags
    return RSt(
        s.data + (tok,), new_tags, s.refusals, s.has_form, s.insts
    )


def readmit_silent(s: RSt, tok: Token) -> RSt:
    return s


def readmit_meta(s: RSt, tok: Token) -> RSt:
    # State-identical to silent; the refusal marker lives in the history
    # only (theorem `silent_eq_meta`).  The runner counts markers.
    return s


def readmit_fact(s: RSt, tok: Token) -> RSt:
    return RSt(s.data, s.tags, s.refusals + 1, s.has_form, s.insts)


def readmit_reify_untagged(s: RSt, tok: Token) -> RSt:
    return _append(s, tok, tag=False)


def readmit_reify_tagged(s: RSt, tok: Token) -> RSt:
    return _append(s, tok, tag=True)


DISCIPLINES: dict[str, Discipline] = {
    "silent": readmit_silent,
    "meta": readmit_meta,
    "fact": readmit_fact,
    "reify_untagged": readmit_reify_untagged,
    "reify_tagged": readmit_reify_tagged,
}


def step(
    s: RSt, e: REv, readmit: Discipline, occurrence: bool = False
) -> RSt:
    if isinstance(e, Sup):
        return s
    if isinstance(e, Adm):
        if occurrence or e.tok not in s.data:
            return _append(s, e.tok, tag=False)
        return readmit(s, e.tok)
    if isinstance(e, Form):
        if s.has_form:
            return s
        return RSt(s.data, s.tags, s.refusals, True, s.insts)
    if not s.has_form or e.idx >= len(s.data):
        return s  # inadmissible instance: no-op in the reduced signature
    return RSt(s.data, s.tags, s.refusals, s.has_form, s.insts | {e.idx})


def observable_profile(s: RSt, i: int) -> tuple[bool, bool]:
    """Object-level observables of datum ``i``: the unary instance and,
    where declared, the tag."""
    return (i in s.insts, i in s.tags)


def separable(s: RSt, i: int, j: int) -> bool:
    return observable_profile(s, i) != observable_profile(s, j)


def swap_two(s: RSt) -> RSt:
    """Index swap on a two-datum state (tokens travel with indices)."""
    assert len(s.data) == 2
    sw = {0: 1, 1: 0}
    return RSt(
        (s.data[1], s.data[0]),
        frozenset(sw[t] for t in s.tags),
        s.refusals,
        s.has_form,
        frozenset(sw[t] for t in s.insts),
    )


def alphabet(tokens: list[Token]) -> list[REv]:
    out: list[REv] = []
    for t in tokens:
        out.append(Sup(t))
        out.append(Adm(t))
    out.append(Form())
    out.append(Inst(0))
    out.append(Inst(1))
    return out


def reachable(
    tokens: list[Token],
    readmit: Discipline,
    max_events: int,
    occurrence: bool = False,
    carrier_cap: int = 2,
) -> dict[RSt, int]:
    seen: dict[RSt, int] = {EMPTY: 0}
    queue: deque[RSt] = deque([EMPTY])
    alpha = alphabet(tokens)
    while queue:
        s = queue.popleft()
        depth = seen[s]
        if depth >= max_events:
            continue
        for e in alpha:
            nxt = step(s, e, readmit, occurrence)
            if len(nxt.data) > carrier_cap:
                continue  # declared carrier cap for the finite search
            if nxt not in seen:
                seen[nxt] = depth + 1
                queue.append(nxt)
    return seen


def _min_depth(
    states: dict[RSt, int], pred: Callable[[RSt], bool]
) -> Optional[int]:
    depths = [d for s, d in states.items() if pred(s)]
    return min(depths) if depths else None


def discipline_report(
    name: str,
    tokens: list[Token],
    max_events: int,
) -> dict[str, object]:
    occurrence = name == "occurrence"
    readmit = DISCIPLINES.get(name, readmit_silent)
    states = reachable(tokens, readmit, max_events, occurrence)
    two_carrier = _min_depth(states, lambda s: len(s.data) >= 2)
    state_diff = _min_depth(
        states,
        lambda s: len(s.data) <= 1
        and (s.refusals > 0 or len(s.tags) > 0),
    )
    witnessed = _min_depth(
        states, lambda s: len(s.data) == 2 and separable(s, 0, 1)
    )
    oriented = _min_depth(
        states,
        lambda s: len(s.data) == 2
        and separable(s, 0, 1)
        and swap_two(s) != s,
    )
    tag_only_witness = _min_depth(
        states,
        lambda s: len(s.data) == 2
        and separable(s, 0, 1)
        and not s.insts,
    )
    # The four-way determination of the research question.
    if two_carrier is not None:
        outcome = "two carrier objects"
    elif state_diff is not None:
        outcome = "two states only"
    elif name == "meta":
        outcome = "one object plus one (metatheoretic) event"
    else:
        outcome = "no new object-level difference"
    return {
        "discipline": name,
        "tokens": tokens,
        "max_events": max_events,
        "states_reached": len(states),
        "outcome": outcome,
        "min_events_to": {
            "carrier_2": two_carrier,
            "readmission_state_difference": state_diff,
            "witnessed_pair": witnessed,
            "oriented_witnessed_pair": oriented,
            "witness_without_instances": tag_only_witness,
        },
    }


def equivalence_check(max_events: int) -> dict[str, object]:
    """reify_untagged and occurrence admission reach exactly the same
    states from one token (theorem `reifyUntagged_eq_occurrence`,
    checked exhaustively here)."""
    a = reachable(["<>"], readmit_reify_untagged, max_events, False)
    b = reachable(["<>"], readmit_silent, max_events, True)
    return {
        "scope": f"single token, {max_events} events",
        "reify_untagged_states": len(a),
        "occurrence_states": len(b),
        "state_sets_equal": set(a) == set(b),
    }


def orientation_check() -> dict[str, object]:
    """The tagged discipline's two-occurrence state is not
    swap-invariant (canonical orientation); the untagged one is
    (per-act choice required)."""
    tagged = step(
        step(EMPTY, Adm("<>"), readmit_reify_tagged),
        Adm("<>"),
        readmit_reify_tagged,
    )
    untagged = step(
        step(EMPTY, Adm("<>"), readmit_reify_untagged),
        Adm("<>"),
        readmit_reify_untagged,
    )
    return {
        "tagged_state": tagged.json(),
        "untagged_state": untagged.json(),
        "tagged_swap_invariant": swap_two(tagged) == tagged,
        "untagged_swap_invariant": swap_two(untagged) == untagged,
        "tagged_separable_without_instances": separable(tagged, 0, 1)
        and not tagged.insts,
        "untagged_separable": separable(untagged, 0, 1),
    }


def capability_prices() -> list[dict[str, object]]:
    """Imported capabilities per discipline (the declared bill)."""
    return [
        {
            "discipline": "silent",
            "imports": [],
            "note": "the first development's dedup; no refusal record "
            "anywhere",
        },
        {
            "discipline": "meta",
            "imports": ["history-only refusal marker"],
            "note": "state-identical to silent (silent_eq_meta); the "
            "marker is erased below the history level "
            "(markers_invisible)",
        },
        {
            "discipline": "fact",
            "imports": ["admitted refusal counter"],
            "note": "state difference without carrier growth; the "
            "counter attaches to no datum and separates no pair",
        },
        {
            "discipline": "reify_untagged",
            "imports": ["reification (metatheoretic position identity)"],
            "note": "provably identical to occurrence admission "
            "(reifyUntagged_eq_occurrence): repetition-refusal reified "
            "without a tag is occurrence admission under another name",
        },
        {
            "discipline": "reify_tagged",
            "imports": [
                "reification (metatheoretic position identity)",
                "built-in unary observable (= one form + one instance, "
                "tagged_translation_separable)",
                "canonical orientation (per-declaration, not per-act)",
            ],
            "note": "witnessed oriented difference at two admissions "
            "from one token; the declaration bundles exactly the "
            "capabilities the explicit route admits one by one",
        },
        {
            "discipline": "occurrence",
            "imports": ["metatheoretic position identity"],
            "note": "carrier 2, collapsed; designation is a per-act "
            "choice (swap-invariant state)",
        },
        {
            "discipline": "second_token",
            "imports": ["second external presentation"],
            "note": "carrier 2, collapsed; witness and orientation "
            "priced as in the bridge investigation",
        },
    ]
