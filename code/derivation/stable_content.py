"""Deterministic mirror of ``lean4/Derivation/StableContent.lean``
(audit repair).

Protected separation is SUFFICIENT for trace stability, and that is
all that is claimed: once a PROTECTED pair is separated by the
declared observation, every event of the declared grammar preserves
the separation — checked here exhaustively over a deterministic
event battery on sample states.  The CONVERSE IS FALSE, with one
full-trace countermodel: an absorbed (halted) state, where every
replay is inert so an unprotected separation is trace stable; and a
separate restricted-fragment example is a live but unfunded state,
where no event in an explicitly restricted
fragment can change the observation.  The restriction is syntactic,
not an event-ownership claim.  Instability is witness-borne: an accepted,
funded refinement routed through the separating column destroys an
unprotected separation (the third countermodel).  The exact
characterization of trace stability on the live funded class is OPEN
and is recorded as such.

Quiescence is a statement about protected separation, not about
trace stability: on a declared state, no pair obstructs exactly when
every retained protected pair is protected-separated.
"""

from __future__ import annotations

from derivation.export import Json
from derivation.primitive_passage import (
    GENESIS_P,
    PS,
    PEvent,
    obst_p,
    preplay,
    pstep,
    sep_p,
)


def prot_sep(s: PS, i: int, j: int) -> bool:
    """Protected separation: protected AND separated by the declared
    observation.  A property of the state — not yet a stability
    claim."""
    if s.obs is None:
        return False
    return (i, j) in s.prot and sep_p(s.obs, i, j)


def quiescent_p(s: PS, n: int) -> bool:
    """No pair below ``n`` is actively obstructed."""
    return all(not obst_p(s, i, j)
               for i in range(n) for j in range(n))


def event_battery(n: int) -> list[PEvent]:
    """A deterministic battery covering every event kind."""
    out: list[PEvent] = [("declareObs",), ("setBudget", 2),
                         ("setLicense", True), ("setLicense", False)]
    for t in range(n + 2):
        out.append(("admitOcc", t))
    for i in range(n):
        for j in range(n):
            out.extend([("assertWit", i, j), ("admitWit", i, j),
                        ("protect", i, j), ("refuse", i, j)])
    out.extend([("addCol", (0,)), ("addCol", (1,)),
                ("addCol", (0, 2)), ("refineCol", (0,), 1),
                ("refineCol", (0,), 2), ("refineCol", (1,), 2),
                ("halt",)])
    return out


def sample_states(n: int) -> list[PS]:
    """Deterministic sample states: grown, declared, budgeted, in
    several observation stages."""
    base: list[PEvent] = [("admitOcc", t) for t in range(n)]
    wire: list[PEvent] = [
        ("assertWit", 0, 1), ("admitWit", 0, 1), ("protect", 0, 1),
        ("assertWit", 1, 2), ("admitWit", 1, 2), ("protect", 1, 2),
        ("declareObs",), ("setBudget", 3),
    ]
    s0 = preplay(base + wire, GENESIS_P)
    s1 = pstep(s0, ("addCol", (0,)))
    s2 = pstep(s1, ("addCol", (1,)))
    s3 = pstep(s1, ("refineCol", (0,), 2))
    return [s0, s1, s2, s3]


def is_trace_excluded_event(e: PEvent) -> bool:
    """Event forms omitted by the restricted trace fragment.

    This is a syntactic classification only.  It does not assert who
    owns or emits an event; generated blocks may themselves contain a
    ``setBudget`` event.
    """
    return e[0] in ("admitOcc", "setBudget", "setLicense")


def persistence_check(n: int) -> bool:
    """Every protected separation survives every battery event on
    every sample state (the SUFFICIENCY direction)."""
    for s in sample_states(n):
        members = [(i, j) for i in range(n) for j in range(n)
                   if prot_sep(s, i, j)]
        for e in event_battery(n):
            t = pstep(s, e)
            if not all(prot_sep(t, i, j) for (i, j) in members):
                return False
    return True


def replay_persistence_check(n: int, depth: int) -> bool:
    """Sufficiency along multi-event traces: every protected
    separation survives every battery trace up to the declared depth
    and breadth bound."""
    battery = event_battery(n)
    for s in sample_states(n):
        members = [(i, j) for i in range(n) for j in range(n)
                   if prot_sep(s, i, j)]
        frontier = [s]
        for _ in range(depth):
            nxt: list[PS] = []
            for cur in frontier:
                for e in battery:
                    t = pstep(cur, e)
                    if not all(prot_sep(t, i, j)
                               for (i, j) in members):
                        return False
                    nxt.append(t)
            frontier = nxt[:24]
    return True


def halted_countermodel() -> dict[str, Json]:
    """Countermodel 1 to the converse: on an absorbed state every
    replay is inert, so an UNPROTECTED separation is trace stable."""
    s = PS(occ=(0, 1), obs=((0,),), halted=True)
    inert = all(pstep(s, e) == s for e in event_battery(2))
    assert s.obs is not None
    return {
        "separated": sep_p(s.obs, 0, 1),
        "not_protected": not prot_sep(s, 0, 1),
        "every_event_inert": inert,
        "trace_stable_but_unprotected": (
            inert and sep_p(s.obs, 0, 1) and not prot_sep(s, 0, 1)),
    }


def unfunded_countermodel() -> dict[str, Json]:
    """Countermodel 2 to the converse: on a live but UNFUNDED state
    no event in the restricted fragment changes the observation, so
    an UNPROTECTED separation is restricted-stable.  This does not
    establish stability under the full grammar."""
    s = PS(occ=(0, 1), obs=((0,),), budget=0, halted=False)
    restricted = [e for e in event_battery(2)
                  if not is_trace_excluded_event(e)]
    obs_fixed = all(pstep(s, e).obs == s.obs for e in restricted)
    budget_fixed = all(pstep(s, e).budget == 0 for e in restricted)
    assert s.obs is not None
    return {
        "live": not s.halted,
        "separated": sep_p(s.obs, 0, 1),
        "not_protected": not prot_sep(s, 0, 1),
        "restricted_events_leave_obs_fixed": obs_fixed,
        "restricted_events_leave_budget_zero": budget_fixed,
        "restricted_stable_but_unprotected": (
            obs_fixed and sep_p(s.obs, 0, 1)
            and not prot_sep(s, 0, 1)),
    }


def unprotected_unstable() -> dict[str, Json]:
    """Countermodel 3 (witness-borne instability): an accepted,
    funded refinement — discharging a protected obstruction,
    preserving every protected separation — destroys the separation
    of an unprotected pair."""
    s = PS(occ=(0, 1, 2), asserted=((1, 2),), wit=((1, 2),),
           prot=((1, 2),), obs=((0,),), budget=1)
    t = pstep(s, ("refineCol", (0,), 1))
    assert s.obs is not None and t.obs is not None
    return {
        "before_separated_unprotected": sep_p(s.obs, 0, 1),
        "refinement_accepted": t != s,
        "after_broken_unprotected": not sep_p(t.obs, 0, 1),
        "protected_pair_now_separated": sep_p(t.obs, 1, 2),
        "protected_separation_intact": prot_sep(t, 1, 2),
    }


def quiescence_check(n: int) -> bool:
    """Quiescence coincides with every retained protected pair being
    protected-separated, on every declared sample state and every
    battery successor.  A statement about protected separation, NOT
    about trace stability."""
    states = []
    for s in sample_states(n):
        states.append(s)
        states.extend(pstep(s, e) for e in event_battery(n))
    for s in states:
        if s.obs is None:
            continue
        lhs = quiescent_p(s, n)
        rhs = all(prot_sep(s, i, j)
                  for (i, j) in s.prot if (i, j) in s.wit)
        if lhs != rhs:
            return False
    return True


def stable_content_report(n: int) -> dict[str, Json]:
    return {
        "carrier": n,
        "trace_depth_bound": 2,
        "trace_breadth_bound": 24,
        "claim":
            "protected separation is SUFFICIENT for trace stability; "
            "the converse is FALSE (absorbed-state countermodel); "
            "a separate unfunded example is restricted-fragment only; the exact "
            "characterization on the live funded class is OPEN",
        "sufficiency_single_step": persistence_check(n),
        "sufficiency_along_traces": replay_persistence_check(n, 2),
        "converse_false_absorbed": halted_countermodel(),
        "converse_false_unfunded": unfunded_countermodel(),
        "instability_needs_witness": unprotected_unstable(),
        "quiescence_iff_protected_separated": quiescence_check(n),
        "open_exact_characterization":
            "whether trace stability implies protected separation on "
            "live funded states is OPEN; not claimed",
    }
