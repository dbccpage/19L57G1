"""Deterministic mirror of ``lean4/Derivation/TransitionAlphabet.lean``.

This module checks a declared one-step codebook for the passage
dynamics.  It does not construct a quotient of histories: equal codes
can be separated by a common continuation, so raw events and states
remain necessary for replay.

The class table and projection are declarations whose coverage is
proved in Lean and checked here over a declared finite state space: every
accepted transition of every well-formed state of the space is shown
to realize exactly one class signature, and each class's minimum
witness is found by exhaustive search over the same space (the Lean
side only exhibits witnesses; minimality is this computation).

The cardinalities 13 and 12 are therefore presentation-relative code
image sizes, not a native alphabet, contextual congruence, DDA map, or
presentation-invariant theorem.

Every function mirrors its Lean namesake exactly.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Iterator, Optional, cast

from derivation.export import Json
from derivation.primitive_passage import (
    GENESIS_P,
    PS,
    Col,
    Cols,
    Pair,
    PEvent,
    col_ok,
    next_family_p,
    obst_p,
    pstep,
    refine_ok,
    wf_pair,
)

FIELDS: tuple[str, ...] = (
    "occ", "asserted", "wit", "prot", "obs", "budget", "licensed",
    "refusals", "halted",
)

# ---------------------------------------------------------------------------
# 0. Attempted events and accepted transitions


def accepted(s: PS, e: PEvent) -> bool:
    """Lean ``Accepted``: the transition moves the represented state."""
    return pstep(s, e) != s


def guard_holds(s: PS, e: PEvent) -> bool:
    """Lean ``guardHolds``: the exact acceptance condition, constructor
    by constructor.  ``accepted_eq_guardHolds`` is the theorem that this
    agrees with :func:`accepted`; the mirror re-checks it."""
    kind = e[0]
    if kind == "halt":
        return not s.halted
    if s.halted:
        return False
    if kind == "admitOcc":
        return cast(int, e[1]) not in s.occ
    if kind == "assertWit":
        i, j = cast(int, e[1]), cast(int, e[2])
        return wf_pair(s, i, j) and (i, j) not in s.asserted
    if kind == "admitWit":
        i, j = cast(int, e[1]), cast(int, e[2])
        return (wf_pair(s, i, j) and (i, j) in s.asserted
                and (i, j) not in s.wit)
    if kind == "protect":
        i, j = cast(int, e[1]), cast(int, e[2])
        return (i, j) in s.wit and (i, j) not in s.prot
    if kind == "declareObs":
        return s.obs is None
    if kind == "refineCol":
        return refine_ok(s, cast(Col, e[1]), cast(int, e[2])) and s.budget > 0
    if kind == "addCol":
        return col_ok(s, cast(Col, e[1])) and s.licensed and s.budget > 0
    if kind == "refuse":
        i, j = cast(int, e[1]), cast(int, e[2])
        return obst_p(s, i, j) and (i, j) not in s.refusals
    if kind == "setBudget":
        return cast(int, e[1]) != s.budget
    return cast(bool, e[1]) != s.licensed


# ---------------------------------------------------------------------------
# 1. The effect profile


def field_delta(s: PS, t: PS) -> tuple[bool, ...]:
    """Lean ``fieldDelta``: which of the nine fields changed."""
    return (t.occ != s.occ, t.asserted != s.asserted, t.wit != s.wit,
            t.prot != s.prot, t.obs != s.obs, t.budget != s.budget,
            t.licensed != s.licensed, t.refusals != s.refusals,
            t.halted != s.halted)


GUARD_OF: dict[str, str] = {
    "admitOcc": "occurrenceFresh",
    "assertWit": "assertionWellFormed",
    "admitWit": "retentionOfAssertion",
    "protect": "protectionOfRetained",
    "declareObs": "preObservational",
    "refineCol": "refinementAccepted",
    "addCol": "columnAccepted",
    "refuse": "obstructionCertified",
    "setBudget": "budgetWrite",
    "setLicense": "licenseWrite",
    "halt": "terminalDeclaration",
}

ORIGIN_OF: dict[str, str] = {
    "admitOcc": "environment",
    "assertWit": "internal",
    "admitWit": "internal",
    "protect": "internal",
    "declareObs": "internal",
    "refineCol": "internal",
    "addCol": "internal",
    "refuse": "internal",
    "setBudget": "environment",
    "setLicense": "environment",
    "halt": "environment",
}

ENV_OWNED: frozenset[str] = frozenset(
    k for k, v in ORIGIN_OF.items() if v == "environment")


def obstructed_pairs(s: PS) -> tuple[Pair, ...]:
    """Lean ``obstructedPairs``."""
    return tuple(r for r in s.prot if obst_p(s, r[0], r[1]))


def gained_pairs(s: PS, t: PS) -> tuple[Pair, ...]:
    before = obstructed_pairs(s)
    return tuple(r for r in obstructed_pairs(t) if r not in before)


def lost_pairs(s: PS, t: PS) -> tuple[Pair, ...]:
    after = obstructed_pairs(t)
    return tuple(r for r in obstructed_pairs(s) if r not in after)


def obst_effect(s: PS, t: PS) -> str:
    """Lean ``obstEffect``.  The classifier is ORDERED: a step that both
    loses and gains obstructed pairs is reported as ``removed``.  No
    accepted step of the declared class exercises that order, and the
    artifact records the check (``mixed_obstruction_steps``)."""
    if lost_pairs(s, t):
        return "removed"
    if gained_pairs(s, t):
        return "created"
    if not obstructed_pairs(s):
        return "untouched"
    return "preserved"


COARSE: dict[str, str] = {
    "created": "creates",
    "removed": "removes",
    "preserved": "inert",
    "untouched": "inert",
}


def budget_delta(s: PS, t: PS) -> str:
    """Lean ``budgetDeltaOf``."""
    if t.budget == s.budget:
        return "unchanged"
    if t.budget + 1 == s.budget:
        return "spentOne"
    return "rewritten"


def continuity_of(t: PS) -> str:
    """Lean ``continuityOf``."""
    return "absorption" if t.halted else "continuation"


Profile = tuple[tuple[bool, ...], str, str, str, str, str, bool]
Sig = tuple[tuple[bool, ...], str, str, str, str]
EffectSig = tuple[tuple[bool, ...], str, str, str]


def profile_of(s: PS, e: PEvent) -> Profile:
    """Lean ``profileOf``: the full seven-component effect profile."""
    t = pstep(s, e)
    kind = cast(str, e[0])
    return (field_delta(s, t), GUARD_OF[kind], obst_effect(s, t),
            budget_delta(s, t), continuity_of(t), ORIGIN_OF[kind],
            accepted(s, e))


def sig_of(s: PS, e: PEvent) -> Sig:
    """Lean ``sigOf``: the declared one-step profile projection."""
    t = pstep(s, e)
    kind = cast(str, e[0])
    return (field_delta(s, t), GUARD_OF[kind], COARSE[obst_effect(s, t)],
            continuity_of(t), ORIGIN_OF[kind])


def erase_guard(g: Sig) -> EffectSig:
    """Lean ``eraseGuard``."""
    return (g[0], g[2], g[3], g[4])


def effect_sig_of(s: PS, e: PEvent) -> EffectSig:
    return erase_guard(sig_of(s, e))


# ---------------------------------------------------------------------------
# 2. The declared well-formed state class


def wf_class(s: PS) -> bool:
    """Lean ``wfB`` / ``WFClass``: live, and protection contained in
    retention.  Both conditions are invariants of replay from genesis;
    the second is load-bearing (``retention_creates_outside_class``)."""
    return (not s.halted) and all(p in s.wit for p in s.prot)


# ---------------------------------------------------------------------------
# 3. The effect classes


def _fd(*changed: str) -> tuple[bool, ...]:
    return tuple(f in changed for f in FIELDS)


CLASS_SIGS: dict[str, Sig] = {
    "supplyOccurrence":
        (_fd("occ"), "occurrenceFresh", "inert", "continuation",
         "environment"),
    "assertDifference":
        (_fd("asserted"), "assertionWellFormed", "inert", "continuation",
         "internal"),
    "retainDifference":
        (_fd("wit"), "retentionOfAssertion", "inert", "continuation",
         "internal"),
    "protectQuiet":
        (_fd("prot"), "protectionOfRetained", "inert", "continuation",
         "internal"),
    "protectObstructing":
        (_fd("prot"), "protectionOfRetained", "creates", "continuation",
         "internal"),
    "declareQuiet":
        (_fd("obs"), "preObservational", "inert", "continuation",
         "internal"),
    "declareObstructing":
        (_fd("obs"), "preObservational", "creates", "continuation",
         "internal"),
    "refineObservation":
        (_fd("obs", "budget"), "refinementAccepted", "removes",
         "continuation", "internal"),
    "extendObservation":
        (_fd("obs", "budget"), "columnAccepted", "removes", "continuation",
         "internal"),
    "recordRefusal":
        (_fd("refusals"), "obstructionCertified", "inert", "continuation",
         "internal"),
    "writeBudget":
        (_fd("budget"), "budgetWrite", "inert", "continuation",
         "environment"),
    "writeLicense":
        (_fd("licensed"), "licenseWrite", "inert", "continuation",
         "environment"),
    "absorbTerminal":
        (_fd("halted"), "terminalDeclaration", "inert", "absorption",
         "environment"),
}

ALL_CLASSES: tuple[str, ...] = tuple(CLASS_SIGS)

_SIMPLE_CLASS: dict[str, str] = {
    "admitOcc": "supplyOccurrence",
    "assertWit": "assertDifference",
    "admitWit": "retainDifference",
    "refineCol": "refineObservation",
    "addCol": "extendObservation",
    "refuse": "recordRefusal",
    "setBudget": "writeBudget",
    "setLicense": "writeLicense",
    "halt": "absorbTerminal",
}


def prot_s(s: PS, i: int, j: int) -> PS:
    """Lean ``protS``: the post-state of an accepted protection."""
    return replace(s, prot=s.prot + ((i, j),))


def class_of(s: PS, e: PEvent) -> str:
    """Lean ``classOf``.  Protection and declaration split by what they
    do to the obstruction set; every other constructor contributes one
    class."""
    kind = cast(str, e[0])
    if kind == "protect":
        i, j = cast(int, e[1]), cast(int, e[2])
        if obst_p(prot_s(s, i, j), i, j):
            return "protectObstructing"
        return "protectQuiet"
    if kind == "declareObs":
        if s.prot:
            return "declareObstructing"
        return "declareQuiet"
    return _SIMPLE_CLASS[kind]


# ---------------------------------------------------------------------------
# 4. The declared finite state space and event battery

PAIR_POOL: tuple[Pair, ...] = ((0, 1), (1, 0))
OCC_POOL: tuple[tuple[int, ...], ...] = ((), (0,), (0, 1))
OBS_POOL: tuple[Optional[Cols], ...] = (None, (), ((),), ((0,),))
BUDGET_POOL: tuple[int, ...] = (0, 1)
REFUSAL_POOL: tuple[tuple[Pair, ...], ...] = ((), ((0, 1),))


def _pair_subsets() -> tuple[tuple[Pair, ...], ...]:
    return ((), ((0, 1),), ((1, 0),), ((0, 1), (1, 0)))


def enumerate_states(halted: bool = False) -> Iterator[PS]:
    """The declared finite state space: two occurrence positions, the
    two off-diagonal pairs in every store, four declared observations,
    unit budget, both licenses, both refusal records."""
    subsets = _pair_subsets()
    for occ in OCC_POOL:
        for asserted in subsets:
            for wit in subsets:
                for prot in subsets:
                    for obs in OBS_POOL:
                        for budget in BUDGET_POOL:
                            for licensed in (True, False):
                                for refusals in REFUSAL_POOL:
                                    yield PS(occ=occ, asserted=asserted,
                                             wit=wit, prot=prot, obs=obs,
                                             budget=budget,
                                             licensed=licensed,
                                             refusals=refusals,
                                             halted=halted)


EVENT_BATTERY: tuple[PEvent, ...] = (
    ("admitOcc", 0), ("admitOcc", 2),
    ("assertWit", 0, 1), ("assertWit", 1, 0),
    ("admitWit", 0, 1),
    ("protect", 0, 1),
    ("declareObs",),
    ("refineCol", (), 0), ("refineCol", (0,), 1),
    ("addCol", (0,)), ("addCol", (1,)),
    ("refuse", 0, 1),
    ("setBudget", 0), ("setBudget", 1), ("setBudget", 2),
    ("setLicense", True), ("setLicense", False),
    ("halt",),
)


def state_size(s: PS) -> int:
    """The declared size measure (Lean ``sizeP``)."""
    obs_size = 0 if s.obs is None else 1 + len(s.obs)
    return (len(s.occ) + len(s.asserted) + len(s.wit) + len(s.prot)
            + len(s.refusals) + s.budget + obs_size)


def state_json(s: PS) -> dict[str, Json]:
    return {
        "occ": list(s.occ),
        "asserted": [list(p) for p in s.asserted],
        "wit": [list(p) for p in s.wit],
        "prot": [list(p) for p in s.prot],
        "obs": None if s.obs is None else [list(c) for c in s.obs],
        "budget": s.budget,
        "licensed": s.licensed,
        "refusals": [list(p) for p in s.refusals],
        "halted": s.halted,
    }


def event_json(e: PEvent) -> list[Json]:
    out: list[Json] = [cast(str, e[0])]
    for arg in e[1:]:
        if isinstance(arg, tuple):
            out.append([cast(int, x) for x in arg])
        else:
            out.append(cast(Json, arg))
    return out


def sig_json(g: Sig) -> dict[str, Json]:
    return {
        "fields": [f for f, changed in zip(FIELDS, g[0]) if changed],
        "guard": g[1],
        "obstruction_move": g[2],
        "continuity": g[3],
        "declared_policy_class": g[4],
    }


# ---------------------------------------------------------------------------
# 5. Deterministic reports (artifact layer)


def partition_report() -> dict[str, Json]:
    """Exhaustive check over the declared space: guard agreement, the
    partition (every accepted transition of a well-formed state has the
    signature of exactly one class), and the absence of mixed
    obstruction steps."""
    checked = 0
    accepted_count = 0
    guard_mismatch = 0
    class_mismatch = 0
    ambiguous = 0
    mixed = 0
    full_profiles: set[Profile] = set()
    projected_signatures: set[Sig] = set()
    per_class: dict[str, int] = {k: 0 for k in ALL_CLASSES}
    for s in enumerate_states():
        wf = wf_class(s)
        for e in EVENT_BATTERY:
            checked += 1
            guard_mismatch += accepted(s, e) != guard_holds(s, e)
            if not (wf and accepted(s, e)):
                continue
            accepted_count += 1
            t = pstep(s, e)
            mixed += bool(gained_pairs(s, t)) and bool(lost_pairs(s, t))
            g = sig_of(s, e)
            full_profiles.add(profile_of(s, e))
            projected_signatures.add(g)
            k = class_of(s, e)
            class_mismatch += CLASS_SIGS[k] != g
            ambiguous += len(
                [n for n in ALL_CLASSES if CLASS_SIGS[n] == g]) != 1
            per_class[k] += 1
    halted_accepts = sum(
        1 for s in enumerate_states(halted=True) for e in EVENT_BATTERY
        if accepted(s, e))
    return {
        "pairs_checked": checked,
        "accepted_wellformed_transitions": accepted_count,
        "guard_agreement_failures": guard_mismatch,
        "class_signature_failures": class_mismatch,
        "ambiguous_classifications": ambiguous,
        "mixed_obstruction_steps": mixed,
        "halted_accepted_transitions": halted_accepts,
        "realized_per_class": cast(Json, per_class),
        "all_classes_realized": all(per_class[k] > 0 for k in ALL_CLASSES),
        "full_profile_image_size": len(full_profiles),
        "declared_signature_image_size": len(projected_signatures),
    }


def codebook_report() -> dict[str, Json]:
    """Sizes of the declared code image, with and without the guard.

    These counts are relative to ``CLASS_SIGS`` and are not a quotient
    or a presentation-invariant cardinality.
    """
    with_guard = {CLASS_SIGS[k] for k in ALL_CLASSES}
    erased = {erase_guard(CLASS_SIGS[k]) for k in ALL_CLASSES}
    merged: list[list[str]] = []
    for sig in sorted(erased, key=str):
        group = [k for k in ALL_CLASSES if erase_guard(CLASS_SIGS[k]) == sig]
        if len(group) > 1:
            merged.append(group)
    return {
        "classes": list(ALL_CLASSES),
        "declared_codebook_size": len(with_guard),
        "guard_erased_codebook_size": len(erased),
        "merged_under_guard_erasure": cast(Json, merged),
        "contextual_quotient": False,
        "dda_correspondence": False,
        "class_signatures": cast(
            Json, {k: sig_json(CLASS_SIGS[k]) for k in ALL_CLASSES}),
    }


def contextual_countermodel_report() -> dict[str, Json]:
    """Concrete failures of right congruence for the one-step code.

    A common suffix separates two equal signatures.  Therefore code
    equality cannot replace raw events in a compositional trace.
    """
    occurrence_left = ("admitOcc", 0)
    occurrence_right = ("admitOcc", 2)
    occurrence_suffix = ("admitOcc", 0)
    occurrence_equal = sig_of(GENESIS_P, occurrence_left) == sig_of(
        GENESIS_P, occurrence_right)
    occurrence_separated = pstep(
        pstep(GENESIS_P, occurrence_left), occurrence_suffix) != pstep(
            pstep(GENESIS_P, occurrence_right), occurrence_suffix)

    budget_start = replace(
        PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
           prot=((0, 1),), obs=(), licensed=True),
        budget=2,
    )
    budget_left = ("setBudget", 0)
    budget_right = ("setBudget", 1)
    budget_suffix = ("addCol", (0,))
    budget_equal = sig_of(budget_start, budget_left) == sig_of(
        budget_start, budget_right)
    budget_separated = pstep(
        pstep(budget_start, budget_left), budget_suffix) != pstep(
            pstep(budget_start, budget_right), budget_suffix)
    return {
        "occurrence_same_start_equal_code": occurrence_equal,
        "occurrence_common_suffix_separates": occurrence_separated,
        "budget_same_start_equal_code": budget_equal,
        "budget_common_suffix_separates": budget_separated,
        "safe_for_event_erasure": False,
    }


def witness_report() -> dict[str, Json]:
    """Exhaustive minimum witnesses: for every class, the smallest state
    of the declared space (by :func:`state_size`, ties broken by
    enumeration order) that accepts a battery event into that class."""
    candidates: list[tuple[int, int, PS, PEvent, str]] = [
        (state_size(s), i, s, e, class_of(s, e))
        for i, s in enumerate(enumerate_states()) if wf_class(s)
        for e in EVENT_BATTERY if accepted(s, e)]
    out: dict[str, Json] = {}
    for k in ALL_CLASSES:
        group = [c for c in candidates if c[4] == k]
        size, _, s, e, _ = min(group)
        out[k] = {
            "minimum_size": size,
            "state": cast(Json, state_json(s)),
            "event": cast(Json, event_json(e)),
            "signature": cast(Json, sig_json(sig_of(s, e))),
            "witnesses_at_minimum_size":
                sum(1 for c in group if c[0] == size),
        }
    return {
        "search_space_states": sum(1 for _ in enumerate_states()),
        "search_space_events": len(EVENT_BATTERY),
        "size_measure": ("occ + asserted + wit + prot + refusals + budget "
                         "+ (0 if pre-observational else 1 + columns)"),
        "witnesses": cast(Json, out),
    }


def invariance_report() -> dict[str, Json]:
    """The two profile components that are NOT invariants of the
    transition, with their witnesses, and the two facts that survive."""
    clear = GENESIS_P
    obstructed = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
                    prot=((0, 1),), obs=())
    two = replace(GENESIS_P, budget=2)
    outside = PS(occ=(0, 1), asserted=((0, 1),), wit=(), prot=((0, 1),),
                 obs=())
    funded = replace(obstructed, budget=1)
    refine_state = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
                      prot=((0, 1),), obs=((),), budget=1)
    return {
        "obstruction_split_untouched":
            obst_effect(clear, pstep(clear, ("admitOcc", 0))),
        "obstruction_split_preserved":
            obst_effect(obstructed, pstep(obstructed, ("admitOcc", 5))),
        "budget_delta_rewritten":
            budget_delta(clear, pstep(clear, ("setBudget", 3))),
        "budget_delta_spent_one_by_environment":
            budget_delta(two, pstep(two, ("setBudget", 1))),
        "funded_guards_always_spend_one": all(
            budget_delta(st, pstep(st, ev)) == "spentOne"
            for st, ev in ((refine_state, ("refineCol", (), 0)),
                           (funded, ("addCol", (0,))))),
        "refusal_always_preserved":
            obst_effect(obstructed, pstep(obstructed, ("refuse", 0, 1))),
        "outside_class_retention_creates": (
            not wf_class(outside)
            and accepted(outside, ("admitWit", 0, 1))
            and COARSE[obst_effect(
                outside, pstep(outside, ("admitWit", 0, 1)))] == "creates"),
        "licence_separates_refine_from_extend": (
            accepted(replace(refine_state, licensed=False),
                     ("refineCol", (), 0))
            and not accepted(replace(funded, licensed=False),
                             ("addCol", (0,)))
            and accepted(funded, ("addCol", (0,)))),
    }


def ownership_report() -> dict[str, Json]:
    """Declared constructor policy classes checked against the actual
    internal generator ``nextFamilyP`` over the declared space.

    The classification "no externally classified constructor is ever
    generated internally" is REFUTED: every extension block begins with
    a unit budget write.  The labels are not issuer provenance."""
    blocks: list[tuple[PEvent, ...]] = []
    for s in enumerate_states():
        blocks.extend(next_family_p(s))
    emitted = sorted({cast(str, ev[0]) for b in blocks for ev in b})
    env_emitted = sorted({cast(str, ev[0]) for b in blocks for ev in b
                          if cast(str, ev[0]) in ENV_OWNED})
    env_events = sorted({str(ev) for b in blocks for ev in b
                         if cast(str, ev[0]) in ENV_OWNED})
    witness = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
                 prot=((0, 1),), obs=())
    return {
        "externally_classified_constructors": sorted(ENV_OWNED),
        "blocks_generated": len(blocks),
        "constructors_emitted_internally": emitted,
        "externally_classified_emitted_internally": env_emitted,
        "externally_classified_events_emitted": env_events,
        "classification_is_provenance": False,
        "no_occurrence_supply_emitted": "admitOcc" not in emitted,
        "no_license_write_emitted": "setLicense" not in emitted,
        "no_terminal_emitted": "halt" not in emitted,
        "budget_write_claim_refuted": "setBudget" in env_emitted,
        "only_unit_funding_emitted": env_events == ["('setBudget', 1)"],
        "refutation_witness": {
            "state": cast(Json, state_json(witness)),
            "block": [cast(Json, event_json(ev))
                      for ev in (("setBudget", 1), ("addCol", (0,)))],
            "block_is_generated": (("setBudget", 1), ("addCol", (0,)))
                in next_family_p(witness),
        },
    }
