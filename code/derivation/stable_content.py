"""Deterministic mirror of ``lean4/Derivation/StableContent.lean``.

Stable content is exactly protected separation: once a PROTECTED
pair is separated by the declared observation, every event of the
declared grammar preserves the separation — checked here
exhaustively over a deterministic event battery on sample states.
Protection is load-bearing: an accepted refinement destroys an
UNPROTECTED separation (the recorded countermodel).  Quiescence is
protected pairs inside the stable content: on a declared state, no
pair obstructs exactly when every retained protected pair is in the
stable content — checked exhaustively over all pairs on the sample
battery.
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


def stable_sep(s: PS, i: int, j: int) -> bool:
    """Membership in the stable content: protected and separated by
    the declared observation."""
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


def persistence_check(n: int) -> bool:
    """Every stable-content membership survives every battery
    event on every sample state."""
    for s in sample_states(n):
        members = [(i, j) for i in range(n) for j in range(n)
                   if stable_sep(s, i, j)]
        for e in event_battery(n):
            t = pstep(s, e)
            if not all(stable_sep(t, i, j) for (i, j) in members):
                return False
    return True


def unprotected_unstable() -> dict[str, Json]:
    """The countermodel: an accepted refinement — discharging a
    protected obstruction, preserving every protected separation —
    destroys the separation of an unprotected pair."""
    s = PS(occ=(0, 1, 2), asserted=((1, 2),), wit=((1, 2),),
           prot=((1, 2),), obs=((0,),), budget=1)
    t = pstep(s, ("refineCol", (0,), 1))
    assert s.obs is not None and t.obs is not None
    return {
        "before_separated_unprotected": sep_p(s.obs, 0, 1),
        "refinement_accepted": t != s,
        "after_broken_unprotected": not sep_p(t.obs, 0, 1),
        "protected_pair_now_separated": sep_p(t.obs, 1, 2),
        "protected_stable_content_intact": stable_sep(t, 1, 2),
    }


def quiescence_check(n: int) -> bool:
    """Quiescence coincides with protected-retained pairs being in
    the stable content, on every declared sample state and every
    battery successor."""
    states = []
    for s in sample_states(n):
        states.append(s)
        states.extend(pstep(s, e) for e in event_battery(n))
    for s in states:
        if s.obs is None:
            continue
        lhs = quiescent_p(s, n)
        rhs = all(stable_sep(s, i, j)
                  for (i, j) in s.prot if (i, j) in s.wit)
        if lhs != rhs:
            return False
    return True


def stable_content_report(n: int) -> dict[str, Json]:
    return {
        "carrier": n,
        "stable_content_persists_battery": persistence_check(n),
        "quiescence_iff_protected_in_stable_content":
            quiescence_check(n),
        "unprotected_separation_unstable": unprotected_unstable(),
    }
