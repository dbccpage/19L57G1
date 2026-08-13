"""Deterministic mirror of ``lean4/Derivation/TraceAlgebra.lean``.

Typed transition records, legal traces, and the laws the transition
monoid of the passage dynamics actually satisfies: the step normal
form, universal idempotence, the frame conditions under which two
events commute, the exact non-commutation countermodels, what an
internal trace cannot do, the non-erasability of a refusal record, the
scoping of replay equivalence, and a two-rule rewrite system on event
lists that is sound at every start state, terminating, confluent — and
deliberately incomplete.

Everything is checked exhaustively over declared finite batteries, and
every bound is recorded in the artifact.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterator, Optional, cast

from derivation.export import Json
from derivation.primitive_passage import (
    GENESIS_P,
    PS,
    Col,
    Cols,
    Pair,
    PEvent,
    preplay,
    pstep,
)
from derivation.transition_alphabet import (
    EVENT_BATTERY,
    accepted,
    budget_delta,
    class_of,
    profile_of,
    enumerate_states,
    event_json,
    guard_holds,
    state_json,
    state_size,
    wf_class,
)
from derivation.transition_alphabet import GUARD_OF, ENV_OWNED

# ---------------------------------------------------------------------------
# 1. The named post-state and the step normal form


def post_of(s: PS, e: PEvent) -> PS:
    """Lean ``postOf``: the state an event installs once its guard is
    discharged."""
    kind = e[0]
    if kind == "admitOcc":
        return replace(s, occ=s.occ + (cast(int, e[1]),))
    if kind == "assertWit":
        return replace(s, asserted=s.asserted
                       + ((cast(int, e[1]), cast(int, e[2])),))
    if kind == "admitWit":
        return replace(s, wit=s.wit + ((cast(int, e[1]), cast(int, e[2])),))
    if kind == "protect":
        return replace(s, prot=s.prot + ((cast(int, e[1]), cast(int, e[2])),))
    if kind == "declareObs":
        return replace(s, obs=())
    if kind == "refineCol":
        if s.obs is None:
            return s
        v, p = cast(Col, e[1]), cast(int, e[2])
        cols: Cols = tuple((p,) + c if c == v else c for c in s.obs)
        return replace(s, obs=cols, budget=s.budget - 1)
    if kind == "addCol":
        if s.obs is None:
            return s
        return replace(s, obs=s.obs + (cast(Col, e[1]),),
                       budget=s.budget - 1)
    if kind == "refuse":
        return replace(s, refusals=s.refusals
                       + ((cast(int, e[1]), cast(int, e[2])),))
    if kind == "setBudget":
        return replace(s, budget=cast(int, e[1]))
    if kind == "setLicense":
        return replace(s, licensed=cast(bool, e[1]))
    return replace(s, halted=True)


def step_by_normal_form(s: PS, e: PEvent) -> PS:
    """Lean ``step_eq_ite``: the step IS the guarded post-state."""
    return post_of(s, e) if guard_holds(s, e) else s


# ---------------------------------------------------------------------------
# 2. Typed transition records and legal traces


@dataclass(frozen=True)
class TRecord:
    """Lean ``TRecord``: pre-state, event, discharged guard, post-state,
    effect class, resource delta."""

    pre: PS
    ev: PEvent
    guard: str
    post: PS
    cls: str
    spend: str
    profile: tuple[tuple[bool, ...], str, str, str, str, str, bool]


def make_record(s: PS, e: PEvent) -> TRecord:
    t = pstep(s, e)
    return TRecord(pre=s, ev=e, guard=GUARD_OF[cast(str, e[0])], post=t,
                   cls=class_of(s, e), spend=budget_delta(s, t),
                   profile=profile_of(s, e))


def wf_record(r: TRecord) -> bool:
    """Lean ``WFRecord``: no field of a record is free data."""
    return (r.post == pstep(r.pre, r.ev)
            and r.guard == GUARD_OF[cast(str, r.ev[0])]
            and r.cls == class_of(r.pre, r.ev)
            and r.spend == budget_delta(r.pre, r.post)
            and r.profile == profile_of(r.pre, r.ev)
            and accepted(r.pre, r.ev)
            and wf_class(r.pre))


def aligned(s: PS, tr: tuple[TRecord, ...]) -> bool:
    """Lean ``Aligned``."""
    cur = s
    for r in tr:
        if r.pre != cur or r.post != pstep(r.pre, r.ev):
            return False
        cur = r.post
    return True


def end_state(s: PS, tr: tuple[TRecord, ...]) -> PS:
    """Lean ``endState``."""
    return tr[-1].post if tr else s


def erase_trace(tr: tuple[TRecord, ...]) -> list[PEvent]:
    """Lean ``eraseTrace``."""
    return [r.ev for r in tr]


def legal_trace(s: PS, tr: tuple[TRecord, ...]) -> bool:
    """Lean ``LegalTrace``."""
    return aligned(s, tr) and all(wf_record(r) for r in tr)


def build_trace(s: PS, events: tuple[PEvent, ...]) -> tuple[TRecord, ...]:
    """The typed trace of the accepted prefix-steps of a history: raw
    attempts that the guards refuse are not records."""
    out: list[TRecord] = []
    cur = s
    for e in events:
        if accepted(cur, e):
            r = make_record(cur, e)
            out.append(r)
            cur = r.post
    return tuple(out)


# ---------------------------------------------------------------------------
# 3. The declared batteries

LICENSE_INSENSITIVE: frozenset[str] = frozenset(
    {"admitOcc", "assertWit", "admitWit", "protect", "declareObs",
     "refineCol", "refuse", "setBudget"})

BUDGET_INSENSITIVE: frozenset[str] = frozenset(
    {"admitOcc", "assertWit", "admitWit", "protect", "declareObs",
     "refuse", "setLicense"})

OCC_INSENSITIVE: frozenset[str] = frozenset(
    {"protect", "declareObs", "refuse", "setBudget", "setLicense"})


def comm_states() -> Iterator[PS]:
    """The declared commutation battery: every state of the alphabet
    mirror's space with an empty refusal store, plus one halted state."""
    for s in enumerate_states():
        if s.refusals == ():
            yield s
    yield replace(GENESIS_P, halted=True)


def obstructed_state() -> PS:
    return PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),), prot=((0, 1),),
              obs=())


def funded_state() -> PS:
    return replace(obstructed_state(), budget=1)


def refine_state() -> PS:
    return PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),), prot=((0, 1),),
              obs=((),), budget=1)


def one_occurrence_state() -> PS:
    return PS(occ=(5,), asserted=((0, 1),))


def named_states() -> list[PS]:
    """The declared small battery used for the rewrite-soundness spot
    check (soundness itself is proved universally in Lean)."""
    return [
        GENESIS_P,
        one_occurrence_state(),
        PS(occ=(0, 1)),
        PS(occ=(0, 1), asserted=((0, 1),)),
        PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),)),
        PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),), obs=()),
        PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),), prot=((0, 1),)),
        obstructed_state(),
        funded_state(),
        refine_state(),
        replace(funded_state(), licensed=False),
        replace(GENESIS_P, halted=True),
    ]


# ---------------------------------------------------------------------------
# 4. The rewrite system


def cons_nf(e: PEvent, r: list[PEvent]) -> list[PEvent]:
    """Lean ``consNF``."""
    if not r:
        return [e]
    if e == r[0]:
        return list(r)
    return [e] + list(r)


def nf(l: list[PEvent]) -> list[PEvent]:
    """Lean ``nf``: the computed normal form."""
    if not l:
        return []
    if l[0] == ("halt",):
        return [("halt",)]
    return cons_nf(l[0], nf(l[1:]))


def no_redex(l: list[PEvent]) -> bool:
    """Lean ``noRedex``."""
    if len(l) < 2:
        return True
    return l[0] != l[1] and l[0] != ("halt",) and no_redex(l[1:])


def rw_reducts(l: list[PEvent]) -> list[list[PEvent]]:
    """Every one-step reduct of ``l`` under the two rules, in the
    context closure (Lean ``Rw``)."""
    out: list[list[PEvent]] = []
    if len(l) >= 2 and l[0] == l[1]:
        out.append(l[1:])
    if len(l) >= 2 and l[0] == ("halt",):
        out.append([("halt",)])
    if l:
        for r in rw_reducts(l[1:]):
            out.append([l[0]] + r)
    return out


def normal_forms(l: list[PEvent]) -> list[list[PEvent]]:
    """Every irreducible list reachable from ``l``."""
    seen: set[tuple[PEvent, ...]] = set()
    stack: list[list[PEvent]] = [l]
    out: list[list[PEvent]] = []
    while stack:
        cur = stack.pop()
        key = tuple(cur)
        if key in seen:
            continue
        seen.add(key)
        reducts = rw_reducts(cur)
        if not reducts:
            out.append(cur)
        stack.extend(reducts)
    return out


REWRITE_ALPHABET: tuple[PEvent, ...] = (
    ("admitOcc", 0), ("setBudget", 1), ("refuse", 0, 1), ("halt",),
)


def list_battery(max_len: int) -> list[list[PEvent]]:
    """Every event list of length at most ``max_len`` over the declared
    rewrite alphabet."""
    out: list[list[PEvent]] = [[]]
    frontier: list[list[PEvent]] = [[]]
    for _ in range(max_len):
        nxt: list[list[PEvent]] = []
        for l in frontier:
            for e in REWRITE_ALPHABET:
                nxt.append(l + [e])
        out.extend(nxt)
        frontier = nxt
    return out


# ---------------------------------------------------------------------------
# 5. Deterministic reports (artifact layer)


def identity_report() -> dict[str, Json]:
    """Inertness, absorption and idempotence, checked exhaustively over
    the alphabet mirror's state space and event battery."""
    checked = 0
    nf_failures = 0
    idem_failures = 0
    absorb_failures = 0
    inert_failures = 0
    for s in enumerate_states():
        halted = pstep(s, ("halt",))
        for e in EVENT_BATTERY:
            checked += 1
            t = pstep(s, e)
            nf_failures += step_by_normal_form(s, e) != t
            idem_failures += pstep(t, e) != t
            inert_failures += (t == s) != (not guard_holds(s, e))
            absorb_failures += pstep(halted, e) != halted
    return {
        "pairs_checked": checked,
        "step_normal_form_failures": nf_failures,
        "idempotence_failures": idem_failures,
        "inertness_criterion_failures": inert_failures,
        "terminal_absorption_failures": absorb_failures,
        "every_event_idempotent": idem_failures == 0,
    }


def trace_report() -> dict[str, Json]:
    """Typed traces: a declared history from genesis, its typed record
    chain, and the erasure/replay agreement."""
    history: tuple[PEvent, ...] = (
        ("admitOcc", 0), ("admitOcc", 1), ("assertWit", 0, 1),
        ("admitWit", 0, 1), ("protect", 0, 1), ("declareObs",),
        ("admitWit", 0, 1), ("refuse", 0, 1), ("setBudget", 1),
        ("addCol", (0,)), ("refuse", 0, 1), ("halt",),
    )
    tr = build_trace(GENESIS_P, history)
    erased = erase_trace(tr)
    return {
        "history_length": len(history),
        "records": len(tr),
        "refused_attempts": len(history) - len(tr),
        "legal_trace": legal_trace(GENESIS_P, tr),
        "replay_erases": preplay(erased, GENESIS_P) == end_state(GENESIS_P, tr),
        "raw_history_same_end_state":
            preplay(list(history), GENESIS_P) == end_state(GENESIS_P, tr),
        "classes": [r.cls for r in tr],
        "guards": [r.guard for r in tr],
        "spends": [r.spend for r in tr],
        "erased": [cast(Json, event_json(e)) for e in erased],
    }


def _smallest_witness(e1: PEvent, e2: PEvent,
                      states: list[PS]) -> Optional[PS]:
    best: Optional[PS] = None
    for s in states:
        if pstep(pstep(s, e1), e2) != pstep(pstep(s, e2), e1):
            if best is None or state_size(s) < state_size(best):
                best = s
    return best


def commutation_report() -> dict[str, Json]:
    """The full ordered commutation matrix over the declared battery,
    with the smallest witness for every non-commuting pair."""
    states = list(comm_states())
    commuting: list[list[Json]] = []
    failing: list[dict[str, Json]] = []
    for a in range(len(EVENT_BATTERY)):
        for b in range(a + 1, len(EVENT_BATTERY)):
            e1, e2 = EVENT_BATTERY[a], EVENT_BATTERY[b]
            w = _smallest_witness(e1, e2, states)
            if w is None:
                commuting.append([cast(Json, event_json(e1)),
                                  cast(Json, event_json(e2))])
            else:
                failing.append({
                    "left": cast(Json, event_json(e1)),
                    "right": cast(Json, event_json(e2)),
                    "witness": cast(Json, state_json(w)),
                    "witness_size": state_size(w),
                    "left_then_right":
                        cast(Json, state_json(pstep(pstep(w, e1), e2))),
                    "right_then_left":
                        cast(Json, state_json(pstep(pstep(w, e2), e1))),
                })
    return {
        "battery_states": len(states),
        "battery_events": len(EVENT_BATTERY),
        "unordered_pairs": len(commuting) + len(failing),
        "commuting_pairs": cast(Json, commuting),
        "non_commuting_pairs": cast(Json, failing),
    }


def frame_report() -> dict[str, Json]:
    """The frame conditions: the declared insensitivity predicates are
    sound (the frame law holds for every insensitive event over the
    battery) and tight (it fails for every excluded event)."""
    states = list(comm_states())
    holds_by_kind: dict[str, dict[str, bool]] = {}
    for e in EVENT_BATTERY:
        kind = cast(str, e[0])
        ok_lic = all(
            pstep(replace(s, licensed=b), e)
            == replace(pstep(s, e), licensed=b)
            for s in states for b in (True, False))
        ok_bud = all(
            pstep(replace(s, budget=n), e) == replace(pstep(s, e), budget=n)
            for s in states for n in (0, 1))
        ok_occ = all(
            pstep(replace(s, occ=s.occ + (7,)), e)
            == replace(pstep(s, e), occ=pstep(s, e).occ + (7,))
            for s in states)
        prev = holds_by_kind.get(kind, {"license": True, "budget": True,
                                        "occurrence": True})
        holds_by_kind[kind] = {
            "license": prev["license"] and ok_lic,
            "budget": prev["budget"] and ok_bud,
            "occurrence": prev["occurrence"] and ok_occ,
        }
    rows = [(name, kind, declared, holds[name])
            for kind, holds in sorted(holds_by_kind.items())
            for name, declared in
            (("license", kind in LICENSE_INSENSITIVE),
             ("budget", kind in BUDGET_INSENSITIVE),
             ("occurrence", kind in OCC_INSENSITIVE))]
    sound = sum(1 for _, _, d, h in rows if d and h)
    unsound = sum(1 for _, _, d, h in rows if d and not h)
    tight = [f"{n}:{k}" for n, k, d, h in rows if not d and not h]
    not_tight = [f"{n}:{k}" for n, k, d, h in rows if not d and h]
    return {
        "license_insensitive": sorted(LICENSE_INSENSITIVE),
        "budget_insensitive": sorted(BUDGET_INSENSITIVE),
        "occurrence_insensitive": sorted(OCC_INSENSITIVE),
        "frames_verified": sound,
        "frames_violated": unsound,
        "excluded_and_really_failing": sorted(set(tight)),
        "excluded_but_actually_framing": sorted(set(not_tight)),
        "why_the_terminal_is_excluded": (
            "the terminal satisfies the one-sided frame law but is "
            "excluded from every insensitivity predicate because "
            "commutation needs the frame in both directions and the "
            "post-terminal state accepts nothing: see the terminal "
            "countermodel in the commutation report"),
    }


def internal_report() -> dict[str, Json]:
    """What a trace of non-environment events cannot do, and the
    non-erasability of a refusal record."""
    internal_events = [e for e in EVENT_BATTERY
                       if cast(str, e[0]) not in ENV_OWNED]
    occ_ok = True
    lic_ok = True
    for s in enumerate_states():
        t = preplay(internal_events, s)
        occ_ok = occ_ok and t.occ == s.occ
        lic_ok = lic_ok and t.licensed == s.licensed
    obstructed = obstructed_state()
    refused = pstep(obstructed, ("refuse", 0, 1))
    persists = all(
        (0, 1) in preplay([e], refused).refusals for e in EVENT_BATTERY)
    return {
        "internal_events": [cast(Json, event_json(e))
                            for e in internal_events],
        "internal_trace_preserves_occurrences": occ_ok,
        "internal_trace_preserves_license": lic_ok,
        "budget_claim_not_made": (
            "the internal generator emits setBudget 1; no internal-trace "
            "budget-preservation claim is made"),
        "refusal_is_accepted": accepted(obstructed, ("refuse", 0, 1)),
        "refusal_recorded": [list(p) for p in refused.refusals],
        "refusal_survives_every_event": persists,
        "refusal_survives_terminal":
            (0, 1) in pstep(refused, ("halt",)).refusals,
    }


def scoping_report() -> dict[str, Json]:
    """Replay equivalence is scoped to a declared start class."""
    left: list[PEvent] = [("admitOcc", 0)]
    right: list[PEvent] = []
    scoped = all(preplay(left, s) == preplay(right, s)
                 for s in enumerate_states() if 0 in s.occ)
    return {
        "left": [cast(Json, event_json(e)) for e in left],
        "right": [cast(Json, event_json(e)) for e in right],
        "scope": "states already representing occurrence 0",
        "equivalent_on_scope": scoped,
        "equivalent_at_genesis":
            preplay(left, GENESIS_P) == preplay(right, GENESIS_P),
        "unscoped_countermodel": cast(Json, state_json(GENESIS_P)),
    }


def rewrite_report(max_len: int = 3) -> dict[str, Json]:
    """The two-rule rewrite system: soundness at every battery state,
    termination, confluence with a unique normal form — and the
    incompleteness witness."""
    lists = list_battery(max_len)
    states = named_states()
    sound_failures = 0
    termination_failures = 0
    confluence_failures = 0
    fixpoint_failures = 0
    for l in lists:
        n = nf(l)
        fixpoint_failures += (not no_redex(n)) + (nf(n) != n)
        termination_failures += sum(
            1 for r in rw_reducts(l) if len(r) >= len(l))
        confluence_failures += sum(1 for m in normal_forms(l) if m != n)
        sound_failures += sum(
            1 for s in states if preplay(n, s) != preplay(l, s))
    incomplete_left: list[PEvent] = [("setBudget", 1), ("setBudget", 2)]
    incomplete_right: list[PEvent] = [("setBudget", 2)]
    same_everywhere = all(
        preplay(incomplete_left, s) == preplay(incomplete_right, s)
        for s in enumerate_states())
    return {
        "rules": ["adjacent idempotence: e :: e :: l  ->  e :: l",
                  "terminal absorption: halt :: r :: l  ->  [halt]"],
        "rewrite_alphabet": [cast(Json, event_json(e))
                             for e in REWRITE_ALPHABET],
        "max_list_length": max_len,
        "lists_checked": len(lists),
        "states_checked": len(states),
        "soundness_failures": sound_failures,
        "termination_failures": termination_failures,
        "confluence_failures": confluence_failures,
        "normal_form_fixpoint_failures": fixpoint_failures,
        "incompleteness_witness": {
            "left": [cast(Json, event_json(e)) for e in incomplete_left],
            "right": [cast(Json, event_json(e)) for e in incomplete_right],
            "same_replay_everywhere": same_everywhere,
            "identified_by_rewriting":
                nf(incomplete_left) == nf(incomplete_right),
        },
        "normal_form_claim_ceiling": (
            "the witness refutes completeness of this two-rule normalizer; "
            "it does not rule out a richer universal or start-scoped "
            "canonicalizer"),
    }
