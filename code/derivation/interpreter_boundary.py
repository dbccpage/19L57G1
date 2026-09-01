"""Stage VIII mirror: the interpreter boundary (I0-I5).

Classification: metatheory apparatus; the theorem package lives in
``lean4/Derivation/InterpreterBoundary.lean``.  The sealed constitution
(``lean4/Derivation/Constitution.lean``) carries a 64-member
description family with one fixed family evaluator and a verified
self-description; the evaluator is a function over the codes and is
not itself a code.  This module mirrors that boundary finitely:

* the 64-member code family in the Lean enumeration order and the
  exact mirror of the family evaluator (``interp_step``);
* pairwise behavioral distinctness of all 64 evaluated codes on a
  declared world/event basis (the six probe pairs of the Initiality
  battery — one probe per toggle);
* the explicit diagonal construction of ``tower_persists``: a function
  of interpreter type that differs from every coded interpreter at its
  indexed world, verified exhaustively over all 64 indices;
* one typed-refusal evaluator ``eval_opt`` whose ``None`` input returns
  ``None``; this construction carries no necessity claim;
* the boundary as a primitive difference: the 65-occurrence carrier
  (64 codes plus the uncoded interpreter role), the witnessed pair
  (kernel description, interpreter role), and the exhaustively checked
  candidate verdicts A (pointed witnessed irreflexive) and F (retained
  and protected — both stores DECLARED data, priced as such).

Domain discipline: all numeric inputs are naturals, matching the Lean
carrier; the declared basis and histories below use only naturals.
Everything is deterministic and decided by implemented checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Callable, Optional, Sequence

from .export import Json
from .represented import (
    Event,
    World,
    aug_apply,
    aug_ok,
    mark_apply,
    mark_ok,
    obstructed,
    req_ok,
    step,
)

# ---------------------------------------------------------------------------
# The code family (mirror of Constitution.ConstitutionDesc / allDescs)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Desc:
    """A constitution description: six independent toggles, one per
    load-bearing guard of the sealed kernel.  Inert data (quotation);
    only ``interp_step`` gives it a semantics (interpretation)."""

    dedup_admit: bool
    guard_require: bool
    guard_accept: bool
    gate_budget: bool
    gate_license: bool
    cert_refusal: bool

    def json(self) -> dict[str, Json]:
        return {
            "dedup_admit": self.dedup_admit,
            "guard_require": self.guard_require,
            "guard_accept": self.guard_accept,
            "gate_budget": self.gate_budget,
            "gate_license": self.gate_license,
            "cert_refusal": self.cert_refusal,
        }


KERNEL_DESC = Desc(True, True, True, True, True, True)


def all_descs() -> tuple[Desc, ...]:
    """The complete 64-member family, in the Lean enumeration order of
    ``Constitution.allDescs`` (first field slowest, last fastest,
    ``False`` before ``True``)."""
    return tuple(
        Desc(a, b, c, e, f, g)
        for a, b, c, e, f, g in product((False, True), repeat=6)
    )


def interp_step(d: Desc, w: World, e: Event) -> World:
    """Exact mirror of ``Constitution.interpStep``: one small-step
    machine consuming a description and an event.  With every toggle
    on it is the sealed kernel (mirror of ``interp_describe``)."""
    kind = e[0]
    if kind == "admit":
        t = e[1]
        assert isinstance(t, int) and t >= 0
        if d.dedup_admit and t in w.data:
            return w
        return World(
            data=w.data + (t,), views=w.views, reqs=w.reqs,
            refusals=w.refusals, budget=w.budget,
            aug_licensed=w.aug_licensed, notes=w.notes,
        )
    if kind == "require":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        assert i >= 0 and j >= 0
        if (not d.guard_require) or req_ok(w, i, j):
            return World(
                data=w.data, views=w.views, reqs=w.reqs + ((i, j),),
                refusals=w.refusals, budget=w.budget,
                aug_licensed=w.aug_licensed, notes=w.notes,
            )
        return w
    if kind == "mark":
        v, p = e[1], e[2]
        assert isinstance(v, tuple) and isinstance(p, int) and p >= 0
        if ((not d.guard_accept) or mark_ok(w, v, p)) and (
            (not d.gate_budget) or w.budget > 0
        ):
            w2 = mark_apply(w, v, p)
            return World(
                data=w2.data, views=w2.views, reqs=w2.reqs,
                refusals=w2.refusals, budget=max(0, w.budget - 1),
                aug_licensed=w2.aug_licensed, notes=w2.notes,
            )
        return w
    if kind == "addView":
        c = e[1]
        assert isinstance(c, tuple)
        if (
            ((not d.guard_accept) or aug_ok(w, c))
            and ((not d.gate_license) or w.aug_licensed)
            and ((not d.gate_budget) or w.budget > 0)
        ):
            w2 = aug_apply(w, c)
            return World(
                data=w2.data, views=w2.views, reqs=w2.reqs,
                refusals=w2.refusals, budget=max(0, w.budget - 1),
                aug_licensed=w2.aug_licensed, notes=w2.notes,
            )
        return w
    if kind == "refuse":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        assert i >= 0 and j >= 0
        if ((not d.cert_refusal) or obstructed(w, (i, j))) and (
            (i, j) not in w.refusals
        ):
            return World(
                data=w.data, views=w.views, reqs=w.reqs,
                refusals=w.refusals + ((i, j),), budget=w.budget,
                aug_licensed=w.aug_licensed, notes=w.notes,
            )
        return w
    if kind == "note":
        n = e[1]
        assert isinstance(n, int) and n >= 0
        return World(
            data=w.data, views=w.views, reqs=w.reqs,
            refusals=w.refusals, budget=w.budget,
            aug_licensed=w.aug_licensed, notes=w.notes + (n,),
        )
    if kind == "setBudget":
        n = e[1]
        assert isinstance(n, int) and n >= 0
        return World(
            data=w.data, views=w.views, reqs=w.reqs,
            refusals=w.refusals, budget=n,
            aug_licensed=w.aug_licensed, notes=w.notes,
        )
    assert kind == "setAugLicense"
    b = e[1]
    assert isinstance(b, bool)
    return World(
        data=w.data, views=w.views, reqs=w.reqs,
        refusals=w.refusals, budget=w.budget,
        aug_licensed=b, notes=w.notes,
    )


# ---------------------------------------------------------------------------
# The declared world/event basis (the six Initiality probe pairs)
# ---------------------------------------------------------------------------

DUP_WORLD = World(data=(5,), budget=9)
SAT_WORLD = World(
    data=(10, 20), views=((0,),), reqs=((0, 1),), budget=9
)
BROKE_WORLD = World(
    data=(10, 20), views=((),), reqs=((0, 1),), budget=0
)
UNLICENSED_WORLD = World(
    data=(10, 20), views=((),), reqs=((0, 1),), budget=9,
    aug_licensed=False,
)

BASIS: tuple[tuple[str, World, Event], ...] = (
    ("dedup_admit", DUP_WORLD, ("admit", 5)),
    ("guard_require", DUP_WORLD, ("require", 0, 0)),
    ("guard_accept", SAT_WORLD, ("mark", (0,), 1)),
    ("gate_budget", BROKE_WORLD, ("mark", (), 0)),
    ("gate_license", UNLICENSED_WORLD, ("addView", (0,))),
    ("cert_refusal", SAT_WORLD, ("refuse", 0, 1)),
)


def behavior_vector(
    d: Desc, basis: Sequence[tuple[str, World, Event]] = BASIS
) -> tuple[World, ...]:
    """The evaluated code's outcomes on the declared basis."""
    return tuple(interp_step(d, w, e) for (_, w, e) in basis)


def distinct_on_basis(
    basis: Sequence[tuple[str, World, Event]] = BASIS,
) -> int:
    """The number of pairwise behaviorally distinct evaluated codes on
    the declared basis (64 = the whole family is separated)."""
    return len({behavior_vector(d, basis) for d in all_descs()})


def self_description_on_basis() -> bool:
    """Mirror of ``Constitution.interp_describe`` on the declared
    basis: the kernel's code, executed by the family evaluator, is the
    sealed step."""
    return all(
        interp_step(KERNEL_DESC, w, e) == step(w, e)
        for (_, w, e) in BASIS
    )


# ---------------------------------------------------------------------------
# The diagonal construction (mirror of tower_persists at the 64-family)
# ---------------------------------------------------------------------------

NOTE_EVENT: Event = ("note", 0)


def index_world(i: int) -> World:
    """The world whose carrier length encodes the index ``i``."""
    return World(data=tuple(range(i)))


def diag(cs: Sequence[Desc], w: World, e: Event) -> World:
    """The diagonal interpreter against the code list ``cs``: at a
    world whose carrier length indexes into ``cs``, run the code at
    that index and extend the transition-inert notes by one element;
    elsewhere, do nothing (mirror of ``InterpreterBoundary.diag``)."""
    idx = len(w.data)
    if idx < len(cs):
        w2 = interp_step(cs[idx], w, e)
        return World(
            data=w2.data, views=w2.views, reqs=w2.reqs,
            refusals=w2.refusals, budget=w2.budget,
            aug_licensed=w2.aug_licensed, notes=w2.notes + (999,),
        )
    return w


def diagonal_misses_all(
    f: Callable[[World, Event], World], cs: Sequence[Desc]
) -> bool:
    """Exhaustive check that ``f`` differs from every coded
    interpreter at its indexed world (the tower_persists witness
    property).  A fake diagonal that copies a member fails at that
    member's index."""
    return all(
        f(index_world(i), NOTE_EVENT)
        != interp_step(cs[i], index_world(i), NOTE_EVENT)
        for i in range(len(cs))
    )


# ---------------------------------------------------------------------------
# The typed-refusal evaluator (mirror of evalOpt)
# ---------------------------------------------------------------------------


def eval_opt(
    c: Optional[Desc], w: World, e: Event
) -> Optional[World]:
    """Mirror of ``InterpreterBoundary.evalOpt``: coded members
    evaluate as before; the uncoded top ``None`` REFUSES — a typed
    verdict in the codomain, never a hidden failure."""
    if c is None:
        return None
    return interp_step(c, w, e)


# ---------------------------------------------------------------------------
# The boundary as a primitive difference (mirror of boundarySetting)
# ---------------------------------------------------------------------------


def carrier() -> tuple[Optional[Desc], ...]:
    """The 65-occurrence carrier: the 64 codes plus the uncoded
    interpreter role (``None``)."""
    return all_descs() + (None,)


def boundary_rel(x: Optional[Desc], y: Optional[Desc]) -> bool:
    """The asserted difference (= retention store = protected-demand
    store): exactly the pair (kernel description, interpreter role)."""
    return x == KERNEL_DESC and y is None


def irrefl(
    rel: Callable[[Optional[Desc], Optional[Desc]], bool],
    xs: Sequence[Optional[Desc]],
) -> bool:
    """Exhaustive irreflexivity over a finite carrier."""
    return all(not rel(x, x) for x in xs)


def candidate_a() -> bool:
    """Candidate A on the boundary setting: the witnessed pair is
    asserted and the relation is irreflexive (exhaustive over the 65
    occurrences)."""
    return boundary_rel(KERNEL_DESC, None) and irrefl(
        boundary_rel, carrier()
    )


def candidate_f() -> bool:
    """Candidate F: A plus retention plus protection on the witnessed
    pair.  Retention and protection are DECLARED (the stores are the
    same relation data), priced as declarations."""
    return (
        candidate_a()
        and boundary_rel(KERNEL_DESC, None)  # ret store
        and boundary_rel(KERNEL_DESC, None)  # prot store
    )


def collapse_obstructed(
    q: Callable[[Optional[Desc]], int],
) -> bool:
    """Mirror of ``i5_collapse_obstructed``: if ``q`` identifies the
    endpoints, the pushforward relation carries a self-pair, so its
    irreflexivity is lost (obstruction relative to the protected
    law)."""
    if q(KERNEL_DESC) != q(None):
        return False
    xs = carrier()
    return any(
        boundary_rel(u, v) and q(u) == q(v) for u in xs for v in xs
    )


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------


def event_json(e: Event) -> list[Json]:
    out: list[Json] = []
    for x in e:
        if isinstance(x, tuple):
            vals: list[Json] = []
            for p in x:
                assert isinstance(p, int)
                vals.append(p)
            out.append(vals)
        else:
            assert isinstance(x, (bool, int, str))
            out.append(x)
    return out


def world_json(w: World) -> dict[str, Json]:
    return {
        "data": list(w.data),
        "views": [list(v) for v in w.views],
        "reqs": [list(r) for r in w.reqs],
        "refusals": [list(r) for r in w.refusals],
        "budget": w.budget,
        "aug_licensed": w.aug_licensed,
        "notes": list(w.notes),
    }


def basis_report() -> list[dict[str, Json]]:
    return [
        {"name": name, "world": world_json(w), "event": event_json(e)}
        for (name, w, e) in BASIS
    ]


TERMINALS: tuple[str, ...] = (
    "FINITE_CODE_FAMILY_NOT_EXTENSIONALLY_COMPLETE",
    "DECLARED_BOUNDARY_MODEL_SATISFIES_A_AND_F",
)

TERMINAL_EVIDENCE: dict[str, list[str]] = {
    "FINITE_CODE_FAMILY_NOT_EXTENSIONALLY_COMPLETE": [
        "InterpreterBoundary.tower_persists",
        "InterpreterBoundary.family_missed",
        "diagonal_misses_all (exhaustive over the 64 indices)",
    ],
    "DECLARED_BOUNDARY_MODEL_SATISFIES_A_AND_F": [
        "InterpreterBoundary.i5_boundary_is_A",
        "InterpreterBoundary.i5_boundary_is_F",
        "InterpreterBoundary.i5_collapse_obstructed",
        "InterpreterBoundary.i5_family_not_extensionally_complete",
    ],
}


def boundary_report() -> dict[str, Json]:
    return {
        "carrier": "Option ConstitutionDesc (65 occurrences)",
        "occurrences": len(carrier()),
        "witness": ["kernelDesc", "interpreter-role"],
        "candidates": {"A": candidate_a(), "F": candidate_f()},
        "retention_protection": "DECLARED",
        "collapse_obstructed": collapse_obstructed(lambda _x: 0),
    }


def interpreter_report() -> dict[str, Json]:
    """The full artifact payload.  ``partial_top`` records the typed
    verdict of the uncoded top; absolute no-outside is NOT claimed
    anywhere in this payload."""
    descs = all_descs()
    return {
        "family_size": len(descs),
        "behaviorally_distinct_on_basis": distinct_on_basis(),
        "basis": basis_report(),
        "self_description_on_basis": self_description_on_basis(),
        "diagonal_misses_all": diagonal_misses_all(
            lambda w, e: diag(descs, w, e), descs
        ),
        "partial_top": (
            "REFUSES" if eval_opt(None, DUP_WORLD, NOTE_EVENT) is None
            else "EVALUATES"
        ),
        "boundary_setting": boundary_report(),
        "terminals": list(TERMINALS),
        "terminal_evidence": {
            k: list(v) for k, v in sorted(TERMINAL_EVIDENCE.items())
        },
    }
