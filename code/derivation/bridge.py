"""The bridge: provenance of the primitive-difference ingredients.

Classification: metatheory apparatus for
``paper/bridge_provenance.md``.  Exhaustive, deterministic reachability
searches over bounded admission histories of the first development's
model (``derivation.model``), asking which ingredients of the witnessed
irreflexive datum are reachable from the opaque inscription and at what
external cost.

Scenarios:

* ``single_dedup``  -- one opaque token, presentation-identity dedup
                       (the declared admission discipline);
* ``two_dedup``     -- a second, externally supplied distinct token;
* ``occurrence``    -- one opaque token under a *declared*
                       occurrence-admission discipline (every admission
                       appends; occurrences are distinguished only by
                       metatheoretic position — a flagged import).
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterator, Optional

from .model import (
    AdmissionError,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    Event,
    Regime,
    Supply,
    step,
)


def event_alphabet(tokens: list[str], n_max: int) -> list[Event]:
    """The declared finite event alphabet: supplies and admissions of the
    given tokens, one binary form, and every binary instance over the
    first ``n_max`` datum indices."""
    events: list[Event] = []
    for t in tokens:
        events.append(Supply(t))
        events.append(AdmitDatum(t))
    events.append(AdmitForm(2))
    for a in range(n_max):
        for b in range(n_max):
            events.append(AdmitInst(0, (a, b)))
    return events


def occurrence_step(r: Regime, e: Event) -> Regime:
    """The occurrence-admission variant: datum admission always appends,
    occurrences distinguished only by metatheoretic position (the token
    is repeated verbatim)."""
    if isinstance(e, AdmitDatum):
        return Regime(
            r.data + (e.token,), r.forms, r.insts, r.rules, r.reqs
        )
    return step(r, e)


@dataclass(frozen=True)
class StateClass:
    carrier: int
    has_binary_form: bool
    oriented_witness: bool
    symmetric_witness: bool
    irreflexive_fact: bool
    self_edge: bool

    def json(self) -> dict[str, object]:
        return {
            "carrier": self.carrier,
            "has_binary_form": self.has_binary_form,
            "oriented_witness": self.oriented_witness,
            "symmetric_witness": self.symmetric_witness,
            "irreflexive_fact": self.irreflexive_fact,
            "self_edge": self.self_edge,
        }


def classify(r: Regime) -> StateClass:
    """Shape of a reached state relative to the target object."""
    off = {
        (a, b)
        for (_, args) in r.insts
        for (a, b) in [args]
        if a != b
    }
    diag = any(a == b for (_, args) in r.insts for (a, b) in [args])
    oriented = any(
        (a, b) in off and (b, a) not in off for (a, b) in off
    )
    symmetric = any((b, a) in off for (a, b) in off)
    return StateClass(
        carrier=r.n_data(),
        has_binary_form=len(r.forms) > 0,
        oriented_witness=oriented and not diag,
        symmetric_witness=symmetric and not diag,
        irreflexive_fact=not diag,
        self_edge=diag,
    )


def reachable_states(
    tokens: list[str],
    max_events: int,
    occurrence_mode: bool = False,
    n_max: int = 2,
) -> dict[Regime, int]:
    """Breadth-first reachability over the event alphabet: every regime
    reachable within ``max_events`` admissible events, with its minimal
    event count.  Deterministic order."""
    stepper = occurrence_step if occurrence_mode else step
    start = Regime((), (), frozenset(), frozenset(), frozenset())
    seen: dict[Regime, int] = {start: 0}
    queue: deque[Regime] = deque([start])
    alphabet = event_alphabet(tokens, n_max)
    while queue:
        r = queue.popleft()
        depth = seen[r]
        if depth >= max_events:
            continue
        usable: list[Event]
        if occurrence_mode and r.n_data() >= n_max:
            usable = [
                e for e in alphabet if not isinstance(e, AdmitDatum)
            ]
        else:
            usable = alphabet
        for e in usable:
            try:
                nxt = stepper(r, e)
            except AdmissionError:
                continue
            if nxt not in seen:
                seen[nxt] = depth + 1
                queue.append(nxt)
    return seen


def scenario_report(
    name: str,
    tokens: list[str],
    max_events: int,
    occurrence_mode: bool,
) -> dict[str, object]:
    states = reachable_states(tokens, max_events, occurrence_mode)
    classes: dict[StateClass, int] = {}
    for r, depth in states.items():
        c = classify(r)
        if c not in classes or depth < classes[c]:
            classes[c] = depth
    def first(pred_name: str) -> Optional[int]:
        depths = [
            d for c, d in classes.items()
            if getattr(c, pred_name)
        ]
        return min(depths) if depths else None
    max_carrier = max(c.carrier for c in classes)
    return {
        "scenario": name,
        "tokens": tokens,
        "max_events": max_events,
        "occurrence_mode": occurrence_mode,
        "states_reached": len(states),
        "max_carrier": max_carrier,
        "min_events_to": {
            "carrier_2": min(
                (d for c, d in classes.items() if c.carrier >= 2),
                default=None,
            ),
            "binary_form": first("has_binary_form"),
            "oriented_witness": first("oriented_witness"),
            "symmetric_witness": first("symmetric_witness"),
            "self_edge": first("self_edge"),
        },
    }


def equivariant_scan() -> dict[str, object]:
    """All 16 relations on the two-element carrier: the swap-invariant
    ones, and among those the irreflexive-as-fact inhabited ones —
    exactly the symmetric pair (echo of the Lean equivariance
    obstruction)."""
    pairs = [(x, y) for x in range(2) for y in range(2)]
    invariant = []
    winners = []
    for mask in range(16):
        rel = frozenset(p for k, p in enumerate(pairs) if mask >> k & 1)
        swapped = frozenset(((1 - a), (1 - b)) for (a, b) in rel)
        if rel != swapped:
            continue
        invariant.append(sorted(rel))
        irrefl = all(a != b for (a, b) in rel)
        inhabited = any(a != b for (a, b) in rel)
        if irrefl and inhabited:
            winners.append(sorted(rel))
    return {
        "swap_invariant_relations": invariant,
        "irreflexive_inhabited_invariant": winners,
        "unique_equivariant_witness_is_symmetric": winners
        == [[(0, 1), (1, 0)]],
    }


def provenance_table() -> list[dict[str, object]]:
    """The assembled per-ingredient provenance verdicts.  Statuses cite
    the Lean theorems (paper section references in
    ``paper/bridge_provenance.md``)."""
    return [
        {
            "ingredient": "carrier (size 1)",
            "verdict": "externally admitted",
            "mechanism": "retention/admission of the inscription; "
            "reading-dependent (L: never retained, F: at genesis)",
            "lean": None,
            "python": "single_dedup scenario: max_carrier",
        },
        {
            "ingredient": "carrier (size 2)",
            "verdict": "not derivable from one inscription",
            "mechanism": "requires a second distinct external token, or "
            "a declared occurrence-admission discipline whose occurrence "
            "identity is metatheoretic position (flagged import)",
            "lean": "single_token_carrier_bound, second_token_required",
            "python": "single_dedup vs two_dedup vs occurrence scenarios",
        },
        {
            "ingredient": "two designated occurrences",
            "verdict": "externally admitted / declared",
            "mechanism": "designation is an external act; no equivariant "
            "ordered designation exists on the symmetric state",
            "lean": "no_swap_fixed_offdiag_pair",
            "python": "equivariant_scan",
        },
        {
            "ingredient": "relation (form)",
            "verdict": "externally admitted",
            "mechanism": "no history without a form admission ever has "
            "a form; nothing derives a signature",
            "lean": "no_admitForm_no_forms",
            "python": "min_events_to.binary_form",
        },
        {
            "ingredient": "witness (instance)",
            "verdict": "externally admitted (oriented) / declared "
            "closure rule reaches only the symmetric form",
            "mechanism": "instances need a prior form; equivariant "
            "introduction reaches S2 only",
            "lean": "no_forms_no_witness, equivariant_witness_is_S2, "
            "equivariant_not_D2",
            "python": "equivariant_scan, min_events_to.*_witness",
        },
        {
            "ingredient": "irreflexivity",
            "verdict": "as-fact: constructible; as-law: declared only",
            "mechanism": "finite facts never entail the law "
            "(self-edge extension countermodel)",
            "lean": "irrefl_law_not_entailed",
            "python": "min_events_to.self_edge (self-edges stay "
            "reachable in every scenario)",
        },
        {
            "ingredient": "orientation",
            "verdict": "metatheoretically present (admission order), "
            "erased at object level; object-level orientation is "
            "externally admitted",
            "mechanism": "the token-aware state distinguishes admission "
            "orders; erasure identifies them; internalizing the order "
            "is the oriented witness itself",
            "lean": "order_visible_to_metatheory, "
            "order_erased_at_object_level, equivariant_not_D2",
            "python": "two_dedup scenario reaches oriented_witness only "
            "via an explicitly oriented instance event",
        },
    ]
