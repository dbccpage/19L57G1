"""Exact finite mirror of the represented-progress kernel.

Classification: metatheory apparatus for
``paper/represented_progress.md``; the theorem package lives in
``lean4/Derivation/Represented.lean``.  Every load-bearing input of a
transition — evaluator, requirement, scheduler, tie-break, fresh-name
source, fuel, authorization, stopping condition — occurs in the
represented state or the represented history; the step function takes
nothing else.  The eight countermodels are minimal non-kernel
semantics, each consuming exactly one unrepresented input.

The kernel constitution is fixed metatheory, not represented runtime
input: the event grammar, the separation/satisfaction laws, the
response menu, the acceptance predicates, and the history producer
that supplies event streams.  The theorems and checks say: relative to
this fixed constitution, no hidden runtime input reaches a transition.
Refusal records verified same-level exhaustion and is non-absorbing;
it certifies, it never terminalizes a run.  All domains are the
naturals: negative tokens, endpoints, points, view members, budgets,
and notes are rejected, matching the Lean carrier exactly.

Everything below is deterministic and decided by the implemented
checks; no model judgment selects, orders, or certifies anything.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Optional

View = tuple[int, ...]
Req = tuple[int, int]
Event = tuple[object, ...]


@dataclass(frozen=True)
class World:
    data: tuple[int, ...] = ()
    views: tuple[View, ...] = ()
    reqs: tuple[Req, ...] = ()
    refusals: tuple[Req, ...] = ()
    budget: int = 0
    aug_licensed: bool = True
    notes: tuple[int, ...] = ()

    def json(self) -> dict[str, object]:
        return {
            "data": list(self.data),
            "views": [list(v) for v in self.views],
            "reqs": [list(r) for r in self.reqs],
            "refusals": [list(r) for r in self.refusals],
            "budget": self.budget,
            "aug_licensed": self.aug_licensed,
            "notes": list(self.notes),
        }


GENESIS = World()


def sep(c: View, i: int, j: int) -> bool:
    return (i in c) != (j in c)


def sat(w: World, r: Req) -> bool:
    return any(sep(c, r[0], r[1]) for c in w.views)


def viol(w: World, r: Req) -> bool:
    return r in w.reqs and not sat(w, r)


def quiescent(w: World) -> bool:
    return all(sat(w, r) for r in w.reqs)


def mark_apply(w: World, v: View, p: int) -> World:
    return replace(
        w,
        views=tuple((p,) + c if c == v else c for c in w.views),
    )


def preserves(w: World, w2: World) -> bool:
    return all(sat(w2, r) for r in w.reqs if sat(w, r))


def discharges_some(w: World, w2: World) -> bool:
    return any(viol(w, r) and sat(w2, r) for r in w.reqs)


def mark_ok(w: World, v: View, p: int) -> bool:
    if p < 0 or v not in w.views or p >= len(w.data) or p in v:
        return False
    w2 = mark_apply(w, v, p)
    return discharges_some(w, w2) and preserves(w, w2)


def aug_apply(w: World, c: View) -> World:
    return replace(w, views=w.views + (c,))


def increase(w: World, c: View) -> bool:
    n = len(w.data)
    return any(
        i != j and sep(c, i, j) and not sat(w, (i, j))
        for i in range(n)
        for j in range(n)
    )


def aug_ok(w: World, c: View) -> bool:
    return (
        all(0 <= p < len(w.data) for p in c)
        and c not in w.views
        and increase(w, c)
    )


def response_menu(w: World) -> list[tuple[View, int]]:
    return [(v, p) for v in w.views for p in range(len(w.data))]


def repairs(w: World, m: tuple[View, int], r: Req) -> bool:
    return mark_ok(w, m[0], m[1]) and sat(mark_apply(w, m[0], m[1]), r)


def repair_family(w: World, r: Req) -> list[tuple[View, int]]:
    """The internally determined successor family: every accepted tied
    response, retained; no least representative is chosen anywhere."""
    return [m for m in response_menu(w) if repairs(w, m, r)]


def obstructed(w: World, r: Req) -> bool:
    """A recorded requirement plus the exhaustive failure of the
    declared finite response menu — never mere lookalikeness."""
    return viol(w, r) and all(
        not repairs(w, m, r) for m in response_menu(w)
    )


def req_ok(w: World, i: int, j: int) -> bool:
    return (
        0 <= i
        and 0 <= j
        and i != j
        and i < len(w.data)
        and j < len(w.data)
        and (i, j) not in w.reqs
    )


def step(w: World, e: Event) -> World:
    kind = e[0]
    if kind == "admit":
        t = e[1]
        assert isinstance(t, int)
        if t < 0 or t in w.data:
            return w
        return replace(w, data=w.data + (t,))
    if kind == "require":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        if req_ok(w, i, j):
            return replace(w, reqs=w.reqs + ((i, j),))
        return w
    if kind == "mark":
        v, p = e[1], e[2]
        assert isinstance(v, tuple) and isinstance(p, int)
        if mark_ok(w, v, p) and w.budget > 0:
            return replace(mark_apply(w, v, p), budget=w.budget - 1)
        return w
    if kind == "addView":
        c = e[1]
        assert isinstance(c, tuple)
        if aug_ok(w, c) and w.aug_licensed and w.budget > 0:
            return replace(aug_apply(w, c), budget=w.budget - 1)
        return w
    if kind == "refuse":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        if obstructed(w, (i, j)) and (i, j) not in w.refusals:
            return replace(w, refusals=w.refusals + ((i, j),))
        return w
    if kind == "note":
        n = e[1]
        assert isinstance(n, int)
        if n < 0:
            return w
        return replace(w, notes=w.notes + (n,))
    if kind == "setBudget":
        n = e[1]
        assert isinstance(n, int)
        if n < 0:
            return w
        return replace(w, budget=n)
    assert kind == "setAugLicense"
    b = e[1]
    assert isinstance(b, bool)
    return replace(w, aug_licensed=b)


def replay(hist: list[Event], w: World = GENESIS) -> World:
    for e in hist:
        w = step(w, e)
    return w


def wf(w: World) -> bool:
    return all(
        r[0] != r[1] and r[0] < len(w.data) and r[1] < len(w.data)
        for r in w.reqs
    )


# ---------------------------------------------------------------------------
# The pigeonhole progress story (violation -> family -> obstruction
# certificate -> augmentation -> discharge), mirrored from Lean
# ---------------------------------------------------------------------------

PIGEON_HISTORY: list[Event] = [
    ("setBudget", 9), ("admit", 10), ("admit", 20), ("admit", 30),
    ("require", 0, 1), ("require", 0, 2), ("require", 1, 2),
    ("addView", (0,)),
]


def progress_story() -> dict[str, object]:
    w = replay(PIGEON_HISTORY)
    fam12 = repair_family(w, (1, 2))
    obs12 = obstructed(w, (1, 2))
    w2 = step(w, ("addView", (1,)))
    return {
        "world": w.json(),
        "wf": wf(w),
        "violated_1_2": viol(w, (1, 2)),
        "repair_family_1_2": [
            [list(v), p] for (v, p) in fam12
        ],
        "obstructed_1_2": obs12,
        "augmentation_accepted": w2 != w,
        "discharged_after_augmentation": sat(w2, (1, 2)),
        "old_reqs_preserved": all(
            sat(w2, r) for r in w.reqs if sat(w, r)
        ),
        "quiescent_after": quiescent(w2),
    }


# ---------------------------------------------------------------------------
# The productive unbounded run (prefix-compatible, ever-growing)
# ---------------------------------------------------------------------------

def block_events(k: int) -> list[Event]:
    return [
        ("setBudget", 1), ("admit", k), ("require", 0, k),
        ("addView", (k,)),
    ]


def hist_up_to(k: int) -> list[Event]:
    h: list[Event] = [("admit", 0)]
    for i in range(1, k + 1):
        h.extend(block_events(i))
    return h


def events_all_accepted(h: list[Event]) -> bool:
    """Every event on the supplied stream changes the state: nothing is
    silently rejected."""
    w = GENESIS
    for e in h:
        w2 = step(w, e)
        if w2 == w:
            return False
        w = w2
    return True


def productivity_report(rounds: int = 15) -> dict[str, object]:
    rows = []
    segments = []
    accepted = []
    prev_hist: list[Event] = hist_up_to(0)
    for k in range(rounds + 1):
        h = hist_up_to(k)
        w = replay(h)
        segments.append(list(w.data) == list(range(k + 1)))
        accepted.append(events_all_accepted(h))
        rows.append(
            {
                "k": k,
                "history_length": len(h),
                "carrier": list(w.data),
                "quiescent": quiescent(w),
                "wf": wf(w),
                "prefix_of_next": h == hist_up_to(k + 1)[: len(h)],
                "extends_previous": h[: len(prev_hist)] == prev_hist,
            }
        )
        prev_hist = h
    return {
        "rows": rows,
        "all_prefix_compatible": all(
            bool(r["prefix_of_next"]) and bool(r["extends_previous"])
            for r in rows
        ),
        "carriers_are_initial_segments": all(segments),
        "all_events_accepted": all(accepted),
        "all_quiescent": all(bool(r["quiescent"]) for r in rows),
    }


# ---------------------------------------------------------------------------
# Countermodel 8: witnesses at every length, no compatible infinite
# history
# ---------------------------------------------------------------------------

def wit_valid(l: list[int]) -> bool:
    return all(len(l) <= x for x in l)


def koenig_report(max_n: int = 15) -> dict[str, object]:
    witnesses = all(
        wit_valid([n] * n) for n in range(max_n + 1)
    )
    # any infinite source g is refuted at prefix length g(0) + 1;
    # exhaustively check every constant source below the bound and the
    # identity source as concrete refutations
    refuted = all(
        not wit_valid([c] * (c + 1)) for c in range(max_n + 1)
    ) and not wit_valid(list(range(max_n + 1)))
    return {
        "witness_at_every_length": witnesses,
        "sampled_infinite_sources_refuted": refuted,
    }


# ---------------------------------------------------------------------------
# Internal certification (represented evaluators)
# ---------------------------------------------------------------------------

def verdict(evaluator: tuple[View, ...], i: int, j: int) -> bool:
    return any(sep(c, i, j) for c in evaluator)


def cert_pos(panel: list[tuple[View, ...]], i: int, j: int) -> bool:
    return bool(panel) and all(verdict(E, i, j) for E in panel)


def cert_neg(panel: list[tuple[View, ...]], i: int, j: int) -> bool:
    return bool(panel) and all(not verdict(E, i, j) for E in panel)


def certification_report() -> dict[str, object]:
    blind_panel: list[tuple[View, ...]] = [((0, 1),), ((0, 1),)]
    return {
        "panel_certifies_equivalent": cert_neg(blind_panel, 0, 1),
        "outside_column_separates": sep((0,), 0, 1),
        "certification_is_panel_relative": (
            cert_pos([((0,),)], 0, 1)
            and not cert_pos([((0,),), ((0, 1),)], 0, 1)
        ),
    }


# ---------------------------------------------------------------------------
# Countermodels 1-7: one unrepresented input each
# ---------------------------------------------------------------------------

SCHED_WORLD = World(
    data=(10, 20), views=((),), reqs=((0, 1),), budget=9
)
ORACLE_WORLD = World(
    data=(10, 20), views=((0,),), reqs=((0, 1),), budget=9
)
TRUNC_WORLD = World(
    data=(10, 20, 30), views=((0,),), reqs=((1, 2),), budget=9
)
OW_WORLD = ORACLE_WORLD
HEAD_A = World(
    data=(10, 20), views=((), (0,)), reqs=((0, 1),), budget=9
)
HEAD_B = World(
    data=(10, 20), views=((0,), ()), reqs=((0, 1),), budget=9
)


def step_sched(ext: bool, w: World, e: Event) -> World:
    if e[0] == "mark":
        return step(w, e) if ext else w
    return step(w, e)


def step_gensym(seed: int, w: World, e: Event) -> World:
    if e[0] == "admit":
        return step(w, ("admit", seed))
    return step(w, e)


def step_oracle(oracle: bool, w: World, e: Event) -> World:
    if e[0] == "mark":
        v, p = e[1], e[2]
        assert isinstance(v, tuple) and isinstance(p, int)
        if (mark_ok(w, v, p) or oracle) and w.budget > 0:
            return replace(mark_apply(w, v, p), budget=w.budget - 1)
        return w
    return step(w, e)


def obstructed_trunc(k: int, w: World, r: Req) -> bool:
    return viol(w, r) and all(
        not repairs(w, m, r) for m in response_menu(w)[:k]
    )


def overwrite_first(w: World, c: View) -> World:
    return replace(w, views=(c,) + w.views[1:])


def step_head(w: World, e: Event) -> World:
    if e[0] == "mark":
        p = e[2]
        assert isinstance(p, int)
        if not w.views:
            return w
        return replace(
            w, views=((p,) + w.views[0],) + w.views[1:]
        )
    return step(w, e)


def countermodel_report() -> dict[str, object]:
    base = replay([("admit", 0)] + block_events(1))
    rows: list[dict[str, object]] = [
        {
            "name": "unrecorded_scheduler",
            "kind": "hidden_runtime_input",
            "differs": step_sched(True, SCHED_WORLD, ("mark", (), 0))
            != step_sched(False, SCHED_WORLD, ("mark", (), 0)),
        },
        {
            "name": "unrecorded_fresh_name_source",
            "kind": "hidden_runtime_input",
            "differs": step_gensym(0, base, ("admit", 99)).data
            != step_gensym(99, base, ("admit", 99)).data,
        },
        {
            "name": "hidden_evaluator",
            "kind": "hidden_runtime_input",
            "differs": step_oracle(True, ORACLE_WORLD, ("mark", (0,), 1))
            != step_oracle(False, ORACLE_WORLD, ("mark", (0,), 1)),
        },
        {
            "name": "incomplete_search_false_obstruction",
            "kind": "semantic_inference_failure",
            "differs": obstructed_trunc(1, TRUNC_WORLD, (1, 2))
            and not obstructed(TRUNC_WORLD, (1, 2))
            and bool(repair_family(TRUNC_WORLD, (1, 2))),
        },
        {
            "name": "destructive_rewrite_not_augmentation",
            "kind": "semantic_inference_failure",
            "differs": sat(OW_WORLD, (0, 1))
            and not sat(overwrite_first(OW_WORLD, ()), (0, 1)),
        },
        {
            "name": "repetition_mislabeled_as_progress",
            "kind": "semantic_inference_failure",
            "differs": replay([("admit", 5)] * 3)
            == replay([("admit", 5)])
            and len([("admit", 5)] * 3) != len([("admit", 5)]),
        },
        {
            "name": "order_sensitive_semantics_splits_equivalents",
            "kind": "hidden_runtime_input",
            "differs": sat(step_head(HEAD_A, ("mark", (), 1)), (0, 1))
            != sat(step_head(HEAD_B, ("mark", (), 1)), (0, 1)),
        },
    ]
    return {
        "rows": rows,
        "all_exhibited": all(bool(r["differs"]) for r in rows),
    }


# ---------------------------------------------------------------------------
# Replay and mutation checks
# ---------------------------------------------------------------------------

def mutation_report() -> dict[str, object]:
    h = PIGEON_HISTORY
    w = replay(h)
    mutations = []
    for idx in range(len(h)):
        mutated = list(h)
        mutated[idx] = ("note", 999)
        mutations.append(replay(mutated) != w)
    return {
        "replay_deterministic": replay(h) == replay(h),
        "every_single_event_mutation_detected": all(mutations),
        "mutations_checked": len(mutations),
    }
