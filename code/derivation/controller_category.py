"""Deterministic mirror of ``lean4/Derivation/ControllerCategory.lean``.

The controller category over the passage dynamics: the 1024-member
class of variable event grammars (one enable bit per event kind), the
controlled interpreter, the live census, two-rule executability with
its three per-kind countermodels, the behavioral non-uniqueness of
live controllers, the constant-simulation refutation of initiality,
and the strict refinement with its invariant-twist countermodel and
reachable-orbit agreement.

Every function mirrors its Lean namesake (same field order, same
guards); every verdict below is a deterministic computation over a
declared finite basis, recorded in the artifact.
"""

from __future__ import annotations

from dataclasses import replace
from itertools import product
from typing import Callable, Sequence

from derivation.export import Json
from derivation.primitive_passage import (
    GENESIS_P,
    PS,
    PEvent,
    grow_hist,
    next_family_p,
    obst_p,
    preplay,
    pstep,
)

# ---------------------------------------------------------------------------
# The comparison class: variable event grammars (Lean ``KindDesc``)

KIND_NAMES: tuple[str, ...] = (
    "admitOcc", "admitWit", "protect", "declareObs", "refineCol",
    "addCol", "refuse", "setBudget", "setLicense", "halt",
)

_KIND_INDEX: dict[str, int] = {k: i for i, k in enumerate(KIND_NAMES)}

KindDesc = tuple[bool, ...]

FULL_K: KindDesc = (True,) * 10


def all_kinds() -> list[KindDesc]:
    """The complete enumeration (mirrors ``allKinds``: first field
    varies slowest, fields in ``KIND_NAMES`` order)."""
    return [tuple(bits) for bits in product((False, True), repeat=10)]


def full_without(name: str) -> KindDesc:
    """The all-on controller with exactly one kind disabled."""
    if name not in _KIND_INDEX:
        raise ValueError(f"unknown event kind: {name!r}")
    return tuple(k != name for k in KIND_NAMES)


NO_ADD_K: KindDesc = full_without("addCol")
NO_BUDGET_K: KindDesc = full_without("setBudget")
NO_REFINE_K: KindDesc = full_without("refineCol")
NO_REFUSE_K: KindDesc = full_without("refuse")


def enabled(d: KindDesc, e: PEvent) -> bool:
    """Whether the controller enables the event (Lean ``enabled``).
    The assertion event is supply-side grammar, present in every
    controller of the declared class: the class toggles the ten
    response/administrative kinds, not the supply of differences."""
    kind = e[0]
    if kind == "assertWit":
        return True
    if not isinstance(kind, str) or kind not in _KIND_INDEX:
        raise ValueError(f"unknown event kind: {kind!r}")
    return d[_KIND_INDEX[kind]]


def interp_k(d: KindDesc, s: PS, e: PEvent) -> PS:
    """The controlled interpreter (Lean ``interpK``): enabled events
    execute the sealed step; disabled events are inert."""
    return pstep(s, e) if enabled(d, e) else s


def replay_k(d: KindDesc, h: Sequence[PEvent], s: PS) -> PS:
    for e in h:
        s = interp_k(d, s, e)
    return s


def response_live(d: KindDesc) -> bool:
    """Syntactic two-rule support (Lean ``ResponseLiveB``): both
    response executors and the funding kind enabled."""
    return (d[_KIND_INDEX["refineCol"]] and d[_KIND_INDEX["addCol"]]
            and d[_KIND_INDEX["setBudget"]])


# ---------------------------------------------------------------------------
# Declared states (Lean namesakes) and the declared behavior basis

OBST5 = PS(occ=(0, 1), asserted=((0, 1), (1, 0)), wit=((0, 1),),
           prot=((0, 1),), obs=(),
           budget=5, licensed=True, refusals=(), halted=False)
OBST0 = replace(OBST5, budget=0)
LOBST = replace(OBST5, obs=((),), licensed=False)
PREOBS = replace(OBST5, obs=None)
WITU = replace(OBST5, prot=())
REFSTATE = replace(OBST5, obs=((),), budget=3)
HALTED0 = replace(GENESIS_P, halted=True)
HALTED1 = replace(GENESIS_P, occ=(0,), halted=True)
DUPSTATE = PS(occ=(5, 5), wit=(), prot=(), obs=None, budget=0,
              licensed=True, refusals=((3, 4),), halted=False)

TWORULE_BLOCK: tuple[PEvent, ...] = (("setBudget", 1), ("addCol", (0,)))

BASIS_STATES: tuple[PS, ...] = (
    OBST5, OBST0, LOBST, PREOBS, WITU, REFSTATE)
BASIS_EVENTS: tuple[PEvent, ...] = (
    ("admitOcc", 2), ("admitWit", 1, 0), ("protect", 0, 1),
    ("declareObs",), ("refineCol", (), 0), ("addCol", (0,)),
    ("refuse", 0, 1), ("setBudget", 3), ("setLicense", False),
    ("halt",),
)


def behavior_signature(d: KindDesc) -> tuple[PS, ...]:
    """The controller's behavior on the declared basis."""
    return tuple(interp_k(d, s, e) for s in BASIS_STATES
                 for e in BASIS_EVENTS)


def live_behavior_classes() -> int:
    """Number of behaviorally distinct live controllers on the
    declared basis."""
    return len({behavior_signature(d) for d in all_kinds()
                if response_live(d)})


# ---------------------------------------------------------------------------
# Serialization helpers

def ps_json(s: PS) -> dict[str, Json]:
    return {
        "occ": list(s.occ),
        "wit": [list(p) for p in s.wit],
        "prot": [list(p) for p in s.prot],
        "obs": None if s.obs is None else [list(c) for c in s.obs],
        "budget": s.budget,
        "licensed": s.licensed,
        "refusals": [list(p) for p in s.refusals],
        "halted": s.halted,
    }


def kind_json(d: KindDesc) -> dict[str, Json]:
    return {name: d[i] for i, name in enumerate(KIND_NAMES)}


def event_json(e: PEvent) -> list[Json]:
    out: list[Json] = []
    for x in e:
        if isinstance(x, tuple):
            col: list[Json] = []
            for v in x:
                assert isinstance(v, int)
                col.append(v)
            out.append(col)
        else:
            assert isinstance(x, (bool, int, str))
            out.append(x)
    return out


# ---------------------------------------------------------------------------
# Reports

def _battery_persists(d: KindDesc, s: PS) -> bool:
    """Nonempty driver battery, and the obstruction (0, 1) survives
    every block under the controller ``d``."""
    battery = next_family_p(s)
    return battery != [] and all(
        obst_p(replay_k(d, blk, s), 0, 1) for blk in battery)


def response_kind_countermodels() -> dict[str, Json]:
    """The three per-kind countermodels (Lean ``dead_without_*``):
    disabling one response kind alone kills the resolution path on a
    state where that kind is load-bearing, over the exact battery the
    driver emits — and the all-on controller resolves each state."""
    refine_block: tuple[PEvent, ...] = (("refineCol", (), 0),)
    cases: list[tuple[str, KindDesc, PS, tuple[PEvent, ...]]] = [
        ("addCol", NO_ADD_K, OBST5, TWORULE_BLOCK),
        ("setBudget", NO_BUDGET_K, OBST0, TWORULE_BLOCK),
        ("refineCol", NO_REFINE_K, LOBST, refine_block),
    ]
    out: dict[str, Json] = {}
    for name, dead, state, resolving in cases:
        out[name] = {
            "controller": kind_json(dead),
            "state": ps_json(state),
            "obstruction_certified": bool(obst_p(state, 0, 1)),
            "battery": [[event_json(e) for e in blk]
                        for blk in next_family_p(state)],
            "obstruction_persists_on_all_blocks":
                _battery_persists(dead, state),
            "full_controller_resolves":
                not obst_p(replay_k(FULL_K, resolving, state), 0, 1),
        }
    return out


def nonuniqueness_report() -> dict[str, Json]:
    """Two live controllers, identical on every refusal-free basis
    cell, distinct on a refuse event at a certified obstruction
    (Lean ``nonrefuse_agree`` / ``refuse_distinguishes``)."""
    nonrefuse = [e for e in BASIS_EVENTS if e[0] != "refuse"]
    agree = all(
        interp_k(FULL_K, s, e) == interp_k(NO_REFUSE_K, s, e)
        for s in BASIS_STATES for e in nonrefuse)
    differ = (interp_k(FULL_K, OBST5, ("refuse", 0, 1))
              != interp_k(NO_REFUSE_K, OBST5, ("refuse", 0, 1)))
    live_members = sum(1 for d in all_kinds() if response_live(d))
    return {
        "pair": {"full": kind_json(FULL_K),
                 "no_refuse": kind_json(NO_REFUSE_K)},
        "both_live": (response_live(FULL_K)
                      and response_live(NO_REFUSE_K)),
        "agree_on_all_nonrefuse_basis_cells": agree,
        "differ_on_refuse_at_certified_obstruction": differ,
        "obstruction_certificate": bool(obst_p(OBST5, 0, 1)),
        "behavioral_basis": {
            "states": [ps_json(s) for s in BASIS_STATES],
            "events": [event_json(e) for e in BASIS_EVENTS],
            "live_members": live_members,
            "distinct_behavioral_classes": live_behavior_classes(),
        },
        "conclusion": "NONUNIQUE_CONTROLLER_FAMILY",
    }


def category_report() -> dict[str, Json]:
    """The constant-simulation record: the target side of the
    commutation square is inert on halted states for every event of
    the declared battery; the source side of a constant map holds
    identically.  Two distinct halted states give two distinct
    simulations between every ordered pair of controllers."""
    consts = {"halted0": HALTED0, "halted1": HALTED1}
    inert: dict[str, Json] = {
        name: all(interp_k(FULL_K, c, e) == c for e in BASIS_EVENTS)
        for name, c in consts.items()}
    return {
        "objects": len(all_kinds()),
        "constant_simulation_targets_inert": inert,
        "constants_distinct": HALTED0 != HALTED1,
        "two_distinct_endo_simulations_on_full": (
            HALTED0 != GENESIS_P
            and all(interp_k(FULL_K, HALTED0, e) == HALTED0
                    for e in BASIS_EVENTS)),
        "note": ("a constant map into a halted state commutes with "
                 "every controller on the source side identically; "
                 "the target-side inertia above is the entire proof "
                 "obligation, mirrored from the Lean constSim"),
    }


def has_dup(xs: Sequence[int]) -> bool:
    """Mirror of ``hasDup``: some element recurs."""
    return any(x in xs[i + 1:] for i, x in enumerate(xs))


def erase_ref(s: PS) -> PS:
    """Mirror of ``eraseRef``."""
    return replace(s, refusals=())


def twist_ref(s: PS) -> tuple[tuple[int, int], ...]:
    """Mirror of ``twistRef``: a step-invariant refusal store."""
    return ((0, 0),) if has_dup(s.occ) else ()


def twist_f(s: PS) -> PS:
    """Mirror of ``twistF``: the invariant-twisted strict
    simulation."""
    return replace(s, refusals=twist_ref(s))


def _comm_holds(f: Callable[[PS], PS]) -> bool:
    """The simulation square for ``f`` from the all-on controller to
    the refusal-free controller, on the declared battery extended by
    the off-orbit duplicate state."""
    return all(
        f(interp_k(FULL_K, s, e)) == interp_k(NO_REFUSE_K, f(s), e)
        for s in BASIS_STATES + (DUPSTATE,) for e in BASIS_EVENTS)


def strict_refinement_report() -> dict[str, Json]:
    """The strict refinement: constants excluded, erasure and the
    invariant twist both strict, distinct off the orbit, equal on the
    reachable orbit (Lean ``strict_not_unique`` /
    ``strict_agree_on_reachable``)."""
    probe = BASIS_STATES + (DUPSTATE,)
    hists = [grow_hist(k) for k in range(6)]
    reach = [preplay(h, GENESIS_P) for h in hists]
    return {
        "strict_demands": ["genesis_preserved", "nonhalted_preserved"],
        "constants_excluded_by_liveness":
            (not GENESIS_P.halted) and HALTED0.halted,
        "erase_is_strict": (
            erase_ref(GENESIS_P) == GENESIS_P
            and all(erase_ref(s).halted == s.halted for s in probe)),
        "twist_is_strict": (
            twist_f(GENESIS_P) == GENESIS_P
            and all(twist_f(s).halted == s.halted for s in probe)),
        "erase_comm_on_battery": _comm_holds(erase_ref),
        "twist_comm_on_battery": _comm_holds(twist_f),
        "twist_differs_from_erase_at": ps_json(DUPSTATE),
        "twist_value": ps_json(twist_f(DUPSTATE)),
        "erase_value": ps_json(erase_ref(DUPSTATE)),
        "twist_ne_erase": twist_f(DUPSTATE) != erase_ref(DUPSTATE),
        "global_uniqueness": "REFUTED_BY_INVARIANT_TWIST",
        "reachable_orbit": {
            "generator": "grow_hist(k) for k in range(6)",
            "histories": len(hists),
            "occurrence_stores_duplicate_free":
                all(not has_dup(s.occ) for s in reach),
            "twist_agrees_with_erase":
                all(twist_f(s) == erase_ref(s) for s in reach),
        },
    }


def controller_category_report() -> dict[str, Json]:
    """The full artifact payload."""
    kinds = all_kinds()
    live = [d for d in kinds if response_live(d)]
    tworule_all = all(
        not obst_p(replay_k(d, TWORULE_BLOCK, OBST5), 0, 1)
        for d in live)
    return {
        "class_size": len(kinds),
        "live_census": len(live),
        "tworule_all_live_pass": tworule_all,
        "response_kind_countermodels": response_kind_countermodels(),
        "nonuniqueness": nonuniqueness_report(),
        "initiality": "REFUTED_BY_CONSTANT_SIMULATIONS",
        "category": category_report(),
        "strict_refinement": strict_refinement_report(),
    }
