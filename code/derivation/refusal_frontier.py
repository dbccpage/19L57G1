"""Frontier Run 006: bounded search over refusal/reflection protocols.

Classification: metatheory apparatus for
``paper/refusal_as_difference.md``.  Instead of hand-selecting
disciplines, this enumerates a declared finite space of protocols and
computes, for every one, the reachable notions of two-ness, milestone
costs, declared imports, and dynamics.  No model judgment decides
equality, isomorphism, minimum cost, or reachability — everything is
exhaustive within declared bounds.

Protocol space (declared):

* ``algebra``    -- number of admission-result constructors (1 or 2);
* ``retention``  -- what happens to a refusal result:
                    ``none`` (discarded), ``judgment`` (admitted as a
                    judgment), ``occurrence`` (the token is re-appended;
                    position identity is a metatheoretic import),
                    ``datum`` (a receipt is reified into the carrier);
* ``tagging``    -- datum-mode receipts carry a built-in unary
                    observable;
* ``reflection`` -- datum-mode receipts may themselves be presented;
* ``autorel``    -- datum-mode reification also asserts a relation
                    instance from the refused subject to the receipt;
* ``tokens``     -- 1, or 2 (the distinct-token control R6).

Events: ``Present(token)`` and, where reflection is enabled and a
receipt exists, ``Reflect`` (present the newest receipt).
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import product
from typing import Iterator, Optional

Token = str


@dataclass(frozen=True)
class Proto:
    algebra: int
    retention: str
    tagging: bool
    reflection: bool
    autorel: bool
    tokens: int

    def valid(self) -> bool:
        if self.retention not in ("none", "judgment", "occurrence", "datum"):
            return False
        if self.retention != "datum" and (
            self.tagging or self.reflection or self.autorel
        ):
            return False
        return self.algebra in (1, 2) and self.tokens in (1, 2)

    def json(self) -> dict[str, object]:
        return {
            "algebra": self.algebra,
            "retention": self.retention,
            "tagging": self.tagging,
            "reflection": self.reflection,
            "autorel": self.autorel,
            "tokens": self.tokens,
        }

    def imports(self) -> list[str]:
        """The declared external purchases of this protocol."""
        out: list[str] = []
        if self.algebra >= 2:
            out.append("binary result algebra")
        if self.retention == "judgment":
            out.append("judgment retention rule")
        if self.retention == "occurrence":
            out.append("occurrence retention rule (position identity)")
        if self.retention == "datum":
            out.append("receipt reification rule (coproduct into carrier)")
        if self.tagging:
            out.append("built-in unary observable (tag)")
        if self.reflection:
            out.append("reflection rule (receipts presentable)")
        if self.autorel:
            out.append("relation symbol + witness rule")
        if self.tokens >= 2:
            out.append("second external token")
        return out


def enumerate_protocols() -> list[Proto]:
    out = []
    for algebra, retention, tagging, reflection, autorel, tokens in product(
        (1, 2),
        ("none", "judgment", "occurrence", "datum"),
        (False, True),
        (False, True),
        (False, True),
        (1, 2),
    ):
        p = Proto(algebra, retention, tagging, reflection, autorel, tokens)
        if p.valid():
            out.append(p)
    return out


@dataclass(frozen=True)
class FState:
    data: tuple[Token, ...]
    tags: frozenset[int]
    judgments: tuple[int, ...]
    rel: frozenset[tuple[int, int]]
    results_seen: frozenset[int]

    def json(self) -> dict[str, object]:
        return {
            "data": list(self.data),
            "tags": sorted(self.tags),
            "judgments": list(self.judgments),
            "rel": sorted(self.rel),
            "results_seen": sorted(self.results_seen),
        }


EMPTY_F = FState((), frozenset(), (), frozenset(), frozenset())

NEW, REFUSED = 0, 1


def _refuse(p: Proto, s: FState, subject_idx: int) -> FState:
    code = REFUSED if p.algebra >= 2 else NEW
    seen = s.results_seen | {code}
    if p.retention == "none":
        return FState(s.data, s.tags, s.judgments, s.rel, seen)
    if p.retention == "judgment":
        return FState(
            s.data, s.tags, s.judgments + (code,), s.rel, seen
        )
    if p.retention == "occurrence":
        return FState(
            s.data + (s.data[subject_idx],), s.tags, s.judgments, s.rel,
            seen,
        )
    # datum: reify a receipt
    idx = len(s.data)
    tags = s.tags | {idx} if p.tagging else s.tags
    rel = s.rel | {(subject_idx, idx)} if p.autorel else s.rel
    return FState(
        s.data + (f"r{idx}",), tags, s.judgments, rel, seen
    )


def step_f(p: Proto, s: FState, ev: tuple[str, object]) -> FState:
    kind, arg = ev
    if kind == "present":
        tok = arg
        assert isinstance(tok, str)
        if tok in s.data:
            return _refuse(p, s, s.data.index(tok))
        return FState(
            s.data + (tok,), s.tags, s.judgments, s.rel,
            s.results_seen | {NEW},
        )
    # reflect: present the newest receipt (datum-mode only)
    idx = len(s.data) - 1
    return _refuse(p, s, idx)


def events_of(p: Proto, s: FState) -> list[tuple[str, object]]:
    out: list[tuple[str, object]] = [("present", "<>")]
    if p.tokens >= 2:
        out.append(("present", "<a>"))
    if (
        p.reflection
        and s.data
        and s.data[-1].startswith("r")
    ):
        out.append(("reflect", None))
    return out


def reachable_f(
    p: Proto, max_events: int, carrier_cap: int = 4
) -> dict[FState, int]:
    seen: dict[FState, int] = {EMPTY_F: 0}
    queue: deque[FState] = deque([EMPTY_F])
    while queue:
        s = queue.popleft()
        depth = seen[s]
        if depth >= max_events:
            continue
        for ev in events_of(p, s):
            nxt = step_f(p, s, ev)
            if len(nxt.data) > carrier_cap:
                continue
            if nxt not in seen:
                seen[nxt] = depth + 1
                queue.append(nxt)
    return seen


# ---------------------------------------------------------------------------
# The notions of two-ness
# ---------------------------------------------------------------------------

ORIGINALS = ("<>", "<a>")


def notions(s: FState) -> dict[str, bool]:
    """The declared notions of two-ness, kept separate (n4, two
    histories, is a protocol-level metatheoretic notion computed in the
    report)."""
    originals = [t for t in s.data if t in ORIGINALS]
    profiles = [
        (i in s.tags, frozenset(
            (a == i, b == i) for (a, b) in s.rel if i in (a, b)
        ))
        for i in range(len(s.data))
    ]
    separable_pair = (
        len(s.data) >= 2
        and any(
            profiles[i] != profiles[j]
            for i in range(len(s.data))
            for j in range(i + 1, len(s.data))
        )
    )
    witnessed = any(a != b for (a, b) in s.rel)
    return {
        "two_carrier": len(s.data) >= 2,
        "two_tokens": len(set(originals)) >= 2,
        "two_occurrences": len(originals) - len(set(originals)) >= 1,
        "two_event_classes": False,  # filled per protocol below
        "two_result_constructors": len(s.results_seen) >= 2,
        "two_judgments": len(s.judgments) >= 2,
        "second_sort": any(t.startswith("r") for t in s.data),
        "witnessed_relation": witnessed,
        "witnessed_irreflexive": witnessed
        and all(a != b for (a, b) in s.rel),
        "separable_pair": separable_pair,
        "oriented": separable_pair,  # refined per state below
    }


def swap_first_two(s: FState) -> FState:
    """Index swap of positions 0 and 1 (only meaningful when the carrier
    has exactly two elements)."""
    assert len(s.data) == 2
    sw = {0: 1, 1: 0}
    return FState(
        (s.data[1], s.data[0]),
        frozenset(sw[t] for t in s.tags),
        s.judgments,
        frozenset((sw[a], sw[b]) for (a, b) in s.rel),
        s.results_seen,
    )


def oriented_two(s: FState) -> bool:
    if len(s.data) != 2:
        return False
    n = notions(s)
    return bool(n["separable_pair"]) and swap_first_two(s) != s


# ---------------------------------------------------------------------------
# Per-protocol report
# ---------------------------------------------------------------------------


def protocol_report(p: Proto, max_events: int) -> dict[str, object]:
    states = reachable_f(p, max_events)

    def first(pred_name: str) -> Optional[int]:
        depths = [
            d for s, d in states.items() if notions(s)[pred_name]
        ]
        return min(depths) if depths else None

    oriented_depths = [
        d for s, d in states.items()
        if len(s.data) == 2 and oriented_two(s)
    ]
    event_kinds = set()
    for s in states:
        for ev in events_of(p, s):
            event_kinds.add(ev[0])
    # dynamics: inert fixpoint (all events no-ops somewhere), or growth
    # to the carrier cap, or bounded activity
    has_fixpoint = any(
        all(step_f(p, s, ev) == s for ev in events_of(p, s))
        for s in states
    )
    max_carrier = max(len(s.data) for s in states)
    dynamics = (
        "fixpoint" if has_fixpoint
        else "growth_to_cap" if max_carrier >= 4
        else "bounded"
    )
    return {
        "protocol": p.json(),
        "imports": p.imports(),
        "states_reached": len(states),
        "max_carrier": max_carrier,
        "two_event_classes": len(event_kinds) >= 2,
        "dynamics": dynamics,
        "min_events_to": {
            "two_carrier": first("two_carrier"),
            "two_result_constructors": first("two_result_constructors"),
            "two_judgments": first("two_judgments"),
            "witnessed_relation": first("witnessed_relation"),
            "witnessed_irreflexive": first("witnessed_irreflexive"),
            "separable_pair": first("separable_pair"),
            "oriented_pair": (
                min(oriented_depths) if oriented_depths else None
            ),
        },
    }


# ---------------------------------------------------------------------------
# Cost orders, minimum protocols, ties; the normal form
# ---------------------------------------------------------------------------


def cost_a(p: Proto) -> int:
    """Cost order A: total declared imports."""
    return len(p.imports())


def cost_b(p: Proto) -> tuple[int, int, int]:
    """Cost order B: lexicographic (external token acts; sorts and
    constructors; rules and symbols)."""
    external = p.tokens - 1
    sorts_ctors = (1 if p.retention == "datum" else 0) + (p.algebra - 1)
    rules = (
        (1 if p.retention != "none" else 0)
        + (1 if p.tagging else 0)
        + (1 if p.reflection else 0)
        + (2 if p.autorel else 0)
    )
    return (external, sorts_ctors, rules)


def minimum_table(max_events: int) -> dict[str, object]:
    protos = enumerate_protocols()
    reports = {p: protocol_report(p, max_events) for p in protos}
    milestones = [
        "two_carrier",
        "witnessed_relation",
        "witnessed_irreflexive",
        "separable_pair",
        "oriented_pair",
    ]
    out: dict[str, object] = {}
    for name, cost in (("A_total_imports", cost_a), ("B_lex", cost_b)):
        per: dict[str, object] = {}
        for m in milestones:
            reaching = [
                p for p in protos
                if reports[p]["min_events_to"][m] is not None  # type: ignore[index]
            ]
            if not reaching:
                per[m] = None
                continue
            best = min(cost(p) for p in reaching)
            ties = [p.json() for p in reaching if cost(p) == best]
            per[m] = {"cost": best, "tied_minima": ties}
        out[name] = per
    return out


def normal_form_check(max_events: int) -> dict[str, object]:
    """T10: target-relative provenance dependencies, each checked
    exhaustively over the declared class — one check per claim made in
    the paper:

    * every ``witnessed_irreflexive`` reacher makes at least one
      declared purchase;
    * every ``witnessed_relation`` reacher has the relation rule;
    * every one-token ``two_carrier`` reacher has occurrence or datum
      retention;
    * every ``separable_pair`` reacher and every ``oriented_pair``
      reacher has a tag or a relation rule (the carrier-profile
      channels);
    * every ``two_result_constructors`` reacher has the binary result
      algebra (the result-outcome channel).

    The channels are target-relative: result-outcome distinction and
    carrier-pair separability have different channels, and no
    target-independent interchangeability of the three is claimed."""
    purchases = []
    violations = []
    dependency_rel = []
    dependency_two = []
    dependency_sep = []
    dependency_orient = []
    dependency_result = []
    for p in enumerate_protocols():
        rep = protocol_report(p, max_events)
        mins = rep["min_events_to"]
        assert isinstance(mins, dict)
        if mins["witnessed_irreflexive"] is not None:
            imp = p.imports()
            purchases.append({"protocol": p.json(), "imports": imp})
            if not imp:
                violations.append(p.json())
        if mins["witnessed_relation"] is not None and not p.autorel:
            dependency_rel.append(p.json())
        if mins["two_carrier"] is not None:
            if p.tokens == 1 and p.retention not in (
                "occurrence", "datum"
            ):
                dependency_two.append(p.json())
        if mins["separable_pair"] is not None and not (
            p.tagging or p.autorel
        ):
            dependency_sep.append(p.json())
        if mins["oriented_pair"] is not None and not (
            p.tagging or p.autorel
        ):
            dependency_orient.append(p.json())
        if (
            mins["two_result_constructors"] is not None
            and p.algebra < 2
        ):
            dependency_result.append(p.json())
    return {
        "witnessed_irreflexive_reachers": len(purchases),
        "all_made_a_purchase": not violations,
        "violations": violations,
        "witnessed_without_relation_rule": dependency_rel,
        "carrier2_without_reify_occurrence_or_second_token":
            dependency_two,
        "separable_without_tag_or_relation": dependency_sep,
        "oriented_without_tag_or_relation": dependency_orient,
        "result_distinction_without_binary_algebra": dependency_result,
        "normal_form_holds_in_class": not violations
        and not dependency_rel
        and not dependency_two
        and not dependency_sep
        and not dependency_orient
        and not dependency_result,
    }


def notion_matrix(max_events: int) -> dict[str, object]:
    """Implications among the nine *state-level* notions of two-ness,
    evaluated over every reachable state of every protocol;
    countermodels recorded per refuted implication.  The remaining
    declared notions are not state predicates and are reported
    separately: two histories and two states are metatheoretic
    (``histories_collapse``); two event classes is protocol-level (the
    report flag); orientation is a per-state refinement of separability
    (``oriented_two``)."""
    keys = [
        "two_carrier", "two_tokens", "two_occurrences",
        "two_result_constructors", "two_judgments", "second_sort",
        "witnessed_relation", "witnessed_irreflexive", "separable_pair",
    ]
    holds: dict[tuple[str, str], bool] = {
        (a, b): True for a in keys for b in keys
    }
    counter: dict[tuple[str, str], dict[str, object]] = {}
    for p in enumerate_protocols():
        for s in reachable_f(p, max_events):
            n = notions(s)
            for a in keys:
                if not n[a]:
                    continue
                for b in keys:
                    if not n[b] and holds[(a, b)]:
                        holds[(a, b)] = False
                        counter[(a, b)] = {
                            "protocol": p.json(),
                            "state": s.json(),
                        }
    return {
        "state_level_notions": keys,
        "separately_reported": [
            "two_histories (metatheoretic; histories_collapse)",
            "two_states (metatheoretic; dynamics rows)",
            "two_event_classes (protocol-level report flag)",
            "oriented (per-state refinement; oriented_two)",
        ],
        "implications": {
            f"{a}->{b}": holds[(a, b)] for a in keys for b in keys
        },
        "countermodels": {
            f"{a}->{b}": cm for (a, b), cm in sorted(counter.items())
        },
    }
