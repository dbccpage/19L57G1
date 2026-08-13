"""Deterministic mirror of ``lean4/Derivation/PrimitivePassage.lean``.

The passage dynamics: a minimal state carrying the separated stores
(occurrences, retained witnesses, protected demands, declared
observation, budget, license, refusals, terminal flag), the
four-condition active-obstruction predicate, the guarded step
function, the same-level repair family, the extension-proposal
family, and the represented next-event family.

Every function mirrors its Lean namesake exactly (same guards, same
order of stores, saturating ``Nat`` arithmetic at the budget field).
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional

Pair = tuple[int, int]
Col = tuple[int, ...]
Cols = tuple[Col, ...]
PEvent = tuple[object, ...]


@dataclass(frozen=True)
class PS:
    """The passage state (Lean ``PState``)."""

    occ: tuple[int, ...] = ()
    asserted: tuple[Pair, ...] = ()
    wit: tuple[Pair, ...] = ()
    prot: tuple[Pair, ...] = ()
    obs: Optional[Cols] = None
    budget: int = 0
    licensed: bool = True
    refusals: tuple[Pair, ...] = ()
    halted: bool = False


GENESIS_P = PS()


def sep_col(c: Col, i: int, j: int) -> bool:
    return (i in c) != (j in c)


def sep_p(cols: Cols, i: int, j: int) -> bool:
    return any(sep_col(c, i, j) for c in cols)


def zero_p(cols: Cols, i: int, j: int) -> bool:
    return not sep_p(cols, i, j)


def obst_p(s: PS, i: int, j: int) -> bool:
    """Active obstruction: retained, protected, observation DECLARED,
    observer-zero — the four-condition conjunction."""
    if s.obs is None:
        return False
    return ((i, j) in s.wit and (i, j) in s.prot
            and zero_p(s.obs, i, j))


def wf_pair(s: PS, i: int, j: int) -> bool:
    return i != j and i < len(s.occ) and j < len(s.occ)


def _refined(cols: Cols, v: Col, p: int) -> Cols:
    return tuple((p,) + c if c == v else c for c in cols)


def refine_ok(s: PS, v: Col, p: int) -> bool:
    if s.obs is None:
        return False
    cols = s.obs
    return (v in cols and p < len(s.occ) and p not in v
            and any(obst_p(s, r[0], r[1])
                    and sep_col((p,) + v, r[0], r[1])
                    for r in s.prot)
            and all((not sep_p(cols, r[0], r[1]))
                    or sep_p(_refined(cols, v, p), r[0], r[1])
                    for r in s.prot))


def col_ok(s: PS, c: Col) -> bool:
    if s.obs is None:
        return False
    return (all(p < len(s.occ) for p in c)
            and c not in s.obs
            and any(obst_p(s, r[0], r[1]) and sep_col(c, r[0], r[1])
                    for r in s.prot))


def pstep(s: PS, e: PEvent) -> PS:
    """The guarded step (Lean ``step``): dedup admission, wf guards,
    certificate-bearing refusal, budget/license gates on structure
    creation, absorbing terminal."""
    kind = e[0]
    if kind == "halt":
        return replace(s, halted=True)
    if s.halted:
        return s
    if kind == "admitOcc":
        t = e[1]
        assert isinstance(t, int)
        if t in s.occ:
            return s
        return replace(s, occ=s.occ + (t,))
    if kind == "assertWit":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        if wf_pair(s, i, j) and (i, j) not in s.asserted:
            return replace(s, asserted=s.asserted + ((i, j),))
        return s
    if kind == "admitWit":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        if (wf_pair(s, i, j) and (i, j) in s.asserted
                and (i, j) not in s.wit):
            return replace(s, wit=s.wit + ((i, j),))
        return s
    if kind == "protect":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        if (i, j) in s.wit and (i, j) not in s.prot:
            return replace(s, prot=s.prot + ((i, j),))
        return s
    if kind == "declareObs":
        if s.obs is None:
            return replace(s, obs=())
        return s
    if kind == "refineCol":
        v, p = e[1], e[2]
        assert isinstance(v, tuple) and isinstance(p, int)
        if refine_ok(s, v, p) and s.budget > 0 and s.obs is not None:
            return replace(s, obs=_refined(s.obs, v, p),
                           budget=max(0, s.budget - 1))
        return s
    if kind == "addCol":
        c = e[1]
        assert isinstance(c, tuple)
        if (col_ok(s, c) and s.licensed and s.budget > 0
                and s.obs is not None):
            return replace(s, obs=s.obs + (c,),
                           budget=max(0, s.budget - 1))
        return s
    if kind == "refuse":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        if obst_p(s, i, j) and (i, j) not in s.refusals:
            return replace(s, refusals=s.refusals + ((i, j),))
        return s
    if kind == "setBudget":
        n = e[1]
        assert isinstance(n, int) and n >= 0
        return replace(s, budget=n)
    if kind == "setLicense":
        b = e[1]
        assert isinstance(b, bool)
        return replace(s, licensed=b)
    raise ValueError(f"unknown event kind: {kind!r}")


def preplay(h: list[PEvent] | tuple[PEvent, ...], s: PS) -> PS:
    for e in h:
        s = pstep(s, e)
    return s


def response_menu(s: PS) -> list[tuple[Col, int]]:
    if s.obs is None:
        return []
    return [(v, p) for v in s.obs for p in range(len(s.occ))]


def repair_family_p(s: PS, i: int, j: int) -> list[tuple[Col, int]]:
    if s.obs is None:
        return []
    cols = s.obs
    return [m for m in response_menu(s)
            if refine_ok(s, m[0], m[1])
            and sep_p(_refined(cols, m[0], m[1]), i, j)]


def extension_proposals(s: PS, i: int, j: int) -> list[Col]:
    return [c for c in ((p,) for p in range(len(s.occ)))
            if col_ok(s, c) and sep_col(c, i, j)]


def obstructed_pairs(s: PS) -> list[Pair]:
    return [r for r in s.prot if obst_p(s, r[0], r[1])]


def next_family_p(s: PS) -> list[tuple[PEvent, ...]]:
    """The represented next-event family (Lean ``nextFamilyP``):
    repair blocks then funded extension blocks, per obstructed
    protected pair."""
    out: list[tuple[PEvent, ...]] = []
    for r in obstructed_pairs(s):
        for m in repair_family_p(s, r[0], r[1]):
            out.append((("refineCol", m[0], m[1]),))
        for c in extension_proposals(s, r[0], r[1]):
            out.append((("setBudget", 1), ("addCol", c)))
    return out


# ---------------------------------------------------------------------------
# The growth driver (Lean HigherStructure.growBlock / growHist / graphAt)


def grow_block(k: int) -> list[PEvent]:
    if k == 0:
        return [("admitOcc", 0)]
    if k == 1:
        return [("admitOcc", 1), ("assertWit", 0, 1),
                ("admitWit", 0, 1), ("protect", 0, 1),
                ("declareObs",), ("setBudget", 1), ("addCol", (0,))]
    return [("admitOcc", k), ("assertWit", k - 1, k),
            ("admitWit", k - 1, k), ("protect", k - 1, k),
            ("setBudget", 1), ("addCol", (k - 1,))]


def grow_hist(k: int) -> list[PEvent]:
    out: list[PEvent] = []
    for r in range(k + 1):
        out.extend(grow_block(r))
    return out


def graph_at(k: int) -> PS:
    return preplay(grow_hist(k), GENESIS_P)


def path_state(k: int) -> PS:
    """The characterized record (Lean ``pathState``): the grown state
    at stage ``k + 1``."""
    return PS(occ=tuple(range(k + 2)),
              asserted=tuple((i, i + 1) for i in range(k + 1)),
              wit=tuple((i, i + 1) for i in range(k + 1)),
              prot=tuple((i, i + 1) for i in range(k + 1)),
              obs=tuple((i,) for i in range(k + 1)),
              budget=0, licensed=True, refusals=(), halted=False)


def k4_passage_hist() -> list[PEvent]:
    """The passage history of the complete four-occurrence graph."""
    return grow_hist(3) + [
        ("assertWit", 0, 2), ("admitWit", 0, 2), ("protect", 0, 2),
        ("assertWit", 1, 3), ("admitWit", 1, 3), ("protect", 1, 3),
        ("assertWit", 0, 3), ("admitWit", 0, 3), ("protect", 0, 3)]


# ---------------------------------------------------------------------------
# Deterministic reports (artifact layer)

from derivation.export import Json  # noqa: E402


def growth_report(rounds: int) -> dict[str, Json]:
    """The growth of the first graph, checked round by round against
    the characterized record, with per-round obstruction, response,
    resolution, and creation records."""
    stages: list[dict[str, Json]] = []
    for k in range(rounds):
        g = graph_at(k + 1)
        spec = path_state(k)
        pre = preplay(grow_block(k + 2)[:5], spec)
        stages.append({
            "stage": k + 1,
            "occ": len(g.occ),
            "wit": len(g.wit),
            "cols": 0 if g.obs is None else len(g.obs),
            "spec_match": g == spec,
            "quiescent": all(not obst_p(g, r[0], r[1])
                              for r in g.prot),
            "connectivity_residue": len(g.occ) - len(g.wit),
            "round_obstruction": obst_p(pre, k + 1, k + 2),
            "round_extension_available":
                (k + 1,) in [tuple(c) for c in
                             extension_proposals(pre, k + 1, k + 2)],
            "round_resolution_lands_on_spec":
                pstep(pre, ("addCol", (k + 1,))) == path_state(k + 1),
            "creation_record": ["addCol", [k + 1]],
        })
    return {
        "rounds": rounds,
        "all_spec_match": all(bool(s["spec_match"]) for s in stages),
        "all_quiescent": all(bool(s["quiescent"]) for s in stages),
        "all_rounds_obstructed_then_resolved": all(
            bool(s["round_obstruction"])
            and bool(s["round_resolution_lands_on_spec"])
            for s in stages),
        "stages": stages,
    }


def arrow_report() -> dict[str, Json]:
    """Status of every passage arrow, with executable witnesses."""
    s0 = preplay([("admitOcc", 7), ("admitOcc", 8)], GENESIS_P)
    obst_state = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
                    prot=((0, 1),), obs=(), budget=0)
    pre_obs = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
                 prot=((0, 1),), obs=None)
    unlicensed = replace(obst_state, licensed=False, budget=5)
    funded = replace(obst_state, budget=5)
    refused = pstep(funded, ("refuse", 0, 1))
    halted = pstep(funded, ("halt",))
    pre_ret = preplay([("admitOcc", 7), ("admitOcc", 8),
                       ("assertWit", 0, 1)], GENESIS_P)
    return {
        "retention_is_declaration": s0.wit == (),
        "assertion_not_retained": (
            pre_ret.asserted == ((0, 1),) and pre_ret.wit == ()),
        "retention_requires_assertion": (
            pstep(replace(s0, obs=None), ("admitWit", 0, 1))
            == replace(s0, obs=None)),
        "retention_completes_from_assertion": (
            pstep(pre_ret, ("admitWit", 0, 1)).wit == ((0, 1),)),
        "obstruction_requires_observation":
            not obst_p(pre_obs, 0, 1),
        "obstruction_at_declared_blind": obst_p(obst_state, 0, 1),
        "proposal_not_execution":
            pstep(unlicensed, ("addCol", (0,))) == unlicensed,
        "budget_gates_execution":
            pstep(obst_state, ("addCol", (0,))) == obst_state,
        "extension_resolves":
            not obst_p(pstep(funded, ("addCol", (0,))), 0, 1),
        "refusal_is_record_not_action": (
            refused.refusals == ((0, 1),)
            and refused.occ == funded.occ
            and refused.wit == funded.wit
            and refused.prot == funded.prot
            and refused.obs == funded.obs
            and not refused.halted),
        "terminal_absorbing": all(
            pstep(halted, e) == halted
            for e in [("admitOcc", 9), ("admitWit", 0, 1),
                      ("protect", 0, 1), ("declareObs",),
                      ("refineCol", (), 0), ("addCol", (1,)),
                      ("refuse", 0, 1), ("setBudget", 3),
                      ("setLicense", False)]),
        "two_rule_at_obstruction": (
            repair_family_p(funded, 0, 1) != []
            or extension_proposals(funded, 0, 1) != []),
        "next_family_nonempty_at_obstruction":
            next_family_p(funded) != [],
        "next_family_stops_when_quiescent":
            next_family_p(path_state(3)) == [],
    }
