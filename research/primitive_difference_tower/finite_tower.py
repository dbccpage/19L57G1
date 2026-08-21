"""A finite, replayable lift/descent test model.

This module intentionally has no dependency on the sealed derivation.  Its
standard trace is conditional: its initial anchor, fresh-label convention,
and one-edge lift grammar are explicit data, rather than claimed consequences
of the initial finite state.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence, Tuple


MAX_HORIZON = 15
Edge = Tuple[int, int]

# These are inputs to the positive fixture.  They are deliberately exported
# into every report so the resulting trace cannot be mistaken for an
# endogenous construction.
CONDITIONAL_ADMISSIONS = (
    "initial-carrier:labels-0-1",
    "seed-edge:0-1",
    "positive-edge-interpretation:declared",
    "named-anchor:0",
    "fresh-label:is-next-index",
    "one-edge-extension:anchor-to-fresh",
    "closure-rule:settle-active-edges",
    "replay-schedule:one-lift-then-closure",
)


class CandidateKind(str, Enum):
    """The declared one-step grammar for the finite assessment."""

    NO_OP = "no_op"
    SAME_CARRIER_CLOSURE = "same_carrier_closure"
    SINGLE_PAIR_LIFT = "single_pair_lift"
    ORBIT_AGGREGATE_LIFT = "orbit_aggregate_lift"
    OBSERVER_EXTENSION = "observer_extension"


class Disposition(str, Enum):
    """Assessment labels; none means an unqualified general theorem."""

    UNIQUE = "unique"
    TIED = "tied"
    CONDITIONAL = "conditional"
    REFUTED = "refuted"
    OPEN = "open"


def make_edge(left: int, right: int) -> Edge:
    """Return the canonical form of an undirected, irreflexive edge."""

    if left == right:
        raise ValueError("an edge must have distinct endpoints")
    return (left, right) if left < right else (right, left)


def normalize_edges(edges: Iterable[Edge]) -> Tuple[Edge, ...]:
    """Canonicalize a finite edge collection without preserving presentation."""

    return tuple(sorted({make_edge(left, right) for left, right in edges}))


def _canonical_bytes(payload: Any) -> bytes:
    return (
        json.dumps(
            payload,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )


def _digest(payload: Any) -> str:
    return sha256(_canonical_bytes(payload)).hexdigest()


@dataclass(frozen=True)
class Event:
    """One replay instruction and the state identity it expects to follow."""

    sequence: int
    action: str
    parent_key: str
    child_index: int
    fresh: Optional[int] = None
    edge: Optional[Edge] = None

    def to_data(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "child_index": self.child_index,
            "edge": list(self.edge) if self.edge is not None else None,
            "fresh": self.fresh,
            "parent_key": self.parent_key,
            "sequence": self.sequence,
        }


@dataclass(frozen=True)
class Stage:
    """A finite state plus a fully replayable history from the fixed genesis."""

    index: int
    carrier: Tuple[int, ...]
    edges: Tuple[Edge, ...]
    settled: Tuple[Edge, ...]
    anchor: int
    admissions: Tuple[str, ...]
    history: Tuple[Event, ...] = ()

    def __post_init__(self) -> None:
        if self.index < 0:
            raise ValueError("stage index must be nonnegative")
        if not self.carrier or self.carrier != tuple(sorted(set(self.carrier))):
            raise ValueError("carrier must be a nonempty sorted tuple of unique labels")
        if self.anchor not in self.carrier:
            raise ValueError("anchor must belong to the carrier")
        if self.edges != normalize_edges(self.edges):
            raise ValueError("edges must be canonical and duplicate-free")
        if self.settled != normalize_edges(self.settled):
            raise ValueError("settled edges must be canonical and duplicate-free")
        carrier_set = set(self.carrier)
        for left, right in self.edges:
            if left not in carrier_set or right not in carrier_set:
                raise ValueError("edge endpoint lies outside the carrier")
        if not set(self.settled).issubset(self.edges):
            raise ValueError("a settled edge must first be present")
        expected_sequences = tuple(range(1, len(self.history) + 1))
        if tuple(event.sequence for event in self.history) != expected_sequences:
            raise ValueError("event sequences must be contiguous from one")

    def structural_data(self) -> dict[str, Any]:
        """State data excluding replay provenance, for a structural snapshot."""

        return {
            "admissions": list(self.admissions),
            "anchor": self.anchor,
            "carrier": list(self.carrier),
            "edges": [list(edge) for edge in self.edges],
            "index": self.index,
            "settled": [list(edge) for edge in self.settled],
        }

    def state_data(self) -> dict[str, Any]:
        payload = self.structural_data()
        payload["history"] = [event.to_data() for event in self.history]
        return payload


@dataclass(frozen=True)
class Lift:
    """The restricted domain on which descent is total in this model."""

    source: Stage
    target: Stage
    fresh: int
    edge: Edge


@dataclass(frozen=True)
class ReplayInvariant:
    """Replay/provenance facts, deliberately separate from the active measure."""

    index: int
    admissions_preserved: bool
    genesis_edge_preserved: bool
    history_replays: bool
    retained_edge_count: int
    trace_key: str

    @property
    def holds(self) -> bool:
        return (
            self.admissions_preserved
            and self.genesis_edge_preserved
            and self.history_replays
        )

    def to_data(self) -> dict[str, Any]:
        return {
            "admissions_preserved": self.admissions_preserved,
            "genesis_edge_preserved": self.genesis_edge_preserved,
            "history_replays": self.history_replays,
            "index": self.index,
            "retained_edge_count": self.retained_edge_count,
            "trace_key": self.trace_key,
        }


@dataclass(frozen=True)
class Candidate:
    """A candidate and its scoped assessment under the declared grammar."""

    code: str
    kind: CandidateKind
    disposition: Disposition
    cost: Tuple[int, int]
    imports: Tuple[str, ...]
    reason: str
    alternatives: Tuple[str, ...] = ()

    def to_data(self) -> dict[str, Any]:
        return {
            "alternatives": list(self.alternatives),
            "code": self.code,
            "cost": list(self.cost),
            "disposition": self.disposition.value,
            "imports": list(self.imports),
            "kind": self.kind.value,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class SymmetryWitness:
    """A finite failure of a selector that chooses one pair from a two-pair orbit."""

    carrier: Tuple[int, ...]
    pair_orbit: Tuple[Edge, ...]
    permutation: Tuple[Tuple[int, int], ...]
    lexical_selection: Edge
    transported_selection: Edge
    selection_after_transport: Edge

    @property
    def is_transport_failure(self) -> bool:
        return self.transported_selection != self.selection_after_transport

    def to_data(self) -> dict[str, Any]:
        return {
            "carrier": list(self.carrier),
            "is_transport_failure": self.is_transport_failure,
            "lexical_selection": list(self.lexical_selection),
            "pair_orbit": [list(edge) for edge in self.pair_orbit],
            "permutation": [list(pair) for pair in self.permutation],
            "scope": (
                "The exhaustive two-choice fixture rules out a swap-stable "
                "one-pair selector for this orbit only. It does not refute "
                "aggregate lifts or explicitly admitted selection data."
            ),
            "selection_after_transport": list(self.selection_after_transport),
            "transported_selection": list(self.transported_selection),
        }


def genesis() -> Stage:
    """The explicitly admitted two-label seed of the conditional fixture."""

    seed = make_edge(0, 1)
    return Stage(
        index=0,
        carrier=(0, 1),
        edges=(seed,),
        settled=(seed,),
        anchor=0,
        admissions=CONDITIONAL_ADMISSIONS,
    )


def state_key(stage: Stage) -> str:
    """A stable identity for the exact replay state, including its history."""

    return _digest(stage.state_data())


def trace_key(stage: Stage) -> str:
    """A stable digest of provenance alone."""

    return _digest([event.to_data() for event in stage.history])


def active_measure(stage: Stage) -> int:
    """The number of present edges that have not yet passed same-carrier closure."""

    return len(set(stage.edges).difference(stage.settled))


def fresh_label(stage: Stage) -> int:
    """Use the admitted enumeration convention for one new carrier element."""

    expected = tuple(range(len(stage.carrier)))
    if stage.carrier != expected:
        raise ValueError("the conditional fresh-label convention is unavailable")
    return len(stage.carrier)


def up(stage: Stage) -> Lift:
    """Perform the conditional one-edge carrier lift from a closed state."""

    if active_measure(stage) != 0:
        raise ValueError("up requires a state with no active obstruction")
    fresh = fresh_label(stage)
    extension = make_edge(stage.anchor, fresh)
    event = Event(
        sequence=len(stage.history) + 1,
        action="lift",
        parent_key=state_key(stage),
        child_index=stage.index + 1,
        fresh=fresh,
        edge=extension,
    )
    target = Stage(
        index=stage.index + 1,
        carrier=stage.carrier + (fresh,),
        edges=normalize_edges(stage.edges + (extension,)),
        settled=stage.settled,
        anchor=stage.anchor,
        admissions=stage.admissions,
        history=stage.history + (event,),
    )
    return Lift(source=stage, target=target, fresh=fresh, edge=extension)


def down(record: Lift) -> Stage:
    """Forget exactly one certified lift; arbitrary larger stages are excluded.

    This returns the parent stored in the record, so ``down(up(stage))`` is
    ``stage`` by construction and is not a check of anything.  The checkable
    fact is that ``structural_descent`` agrees with it on every emitted lift.
    """

    expected = up(record.source)
    if record != expected:
        raise ValueError("descent requires a certified lift record")
    return record.source


def descent_rejects(record: Lift) -> bool:
    """Report whether ``down`` refuses a record, without raising."""

    try:
        down(record)
    except ValueError:
        return True
    return False


def structural_descent(stage: Stage) -> Stage:
    """Forget the most recent lift using only the target's own structure.

    No certificate is consulted: the fresh label and extension edge named by
    the last event are removed and the event is dropped.  Agreement with the
    certified ``down`` is therefore a fact about what ``up`` builds, not a
    consequence of how ``Lift`` stores its parent.  It is the Python analogue
    of the Lean fixture's ``clampedRestriction_certified``.
    """

    if not stage.history or stage.history[-1].action != "lift":
        raise ValueError("structural descent requires a stage whose last event is a lift")
    event = stage.history[-1]
    if event.fresh is None or event.edge is None:
        raise ValueError("a lift event must name its fresh label and extension edge")
    return Stage(
        index=stage.index - 1,
        carrier=tuple(label for label in stage.carrier if label != event.fresh),
        edges=tuple(edge for edge in stage.edges if edge != event.edge),
        settled=stage.settled,
        anchor=stage.anchor,
        admissions=stage.admissions,
        history=stage.history[:-1],
    )


def closure(stage: Stage) -> Stage:
    """Resolve every presently active edge without changing the carrier."""

    if active_measure(stage) == 0:
        return stage
    event = Event(
        sequence=len(stage.history) + 1,
        action="close",
        parent_key=state_key(stage),
        child_index=stage.index,
    )
    return Stage(
        index=stage.index,
        carrier=stage.carrier,
        edges=stage.edges,
        settled=stage.edges,
        anchor=stage.anchor,
        admissions=stage.admissions,
        history=stage.history + (event,),
    )


def replay(history: Iterable[Event]) -> Stage:
    """Rebuild a state from genesis and reject any nonmatching instruction."""

    current = genesis()
    for event in history:
        if event.sequence != len(current.history) + 1:
            raise ValueError("replay event sequence does not match the current state")
        if event.action == "lift":
            record = up(current)
            if event != record.target.history[-1]:
                raise ValueError("replay lift does not match the declared parent")
            current = record.target
        elif event.action == "close":
            next_state = closure(current)
            if next_state is current or event != next_state.history[-1]:
                raise ValueError("replay closure does not match the declared parent")
            current = next_state
        else:
            raise ValueError("replay action is not in the declared grammar")
    return current


def replay_invariant(stage: Stage) -> ReplayInvariant:
    """Check provenance and retention without consulting the active measure."""

    try:
        history_replays = replay(stage.history) == stage
    except ValueError:
        history_replays = False
    return ReplayInvariant(
        index=stage.index,
        admissions_preserved=stage.admissions == CONDITIONAL_ADMISSIONS,
        genesis_edge_preserved=make_edge(0, 1) in stage.edges,
        history_replays=history_replays,
        retained_edge_count=len(stage.edges),
        trace_key=trace_key(stage),
    )


def build_tower(horizon: int = MAX_HORIZON) -> Tuple[Stage, ...]:
    """Produce the completed conditional stages indexed from zero through horizon."""

    if horizon < 0 or horizon > MAX_HORIZON:
        raise ValueError("the finite fixture supports horizons from zero through 15")
    result = [genesis()]
    for _ in range(horizon):
        result.append(closure(up(result[-1]).target))
    return tuple(result)


def active_endpoints(stage: Stage) -> Tuple[int, ...]:
    """List endpoints involved in the currently active finite demand."""

    active = set(stage.edges).difference(stage.settled)
    return tuple(sorted({endpoint for edge in active for endpoint in edge}))


def aggregate_effect(stage: Stage, code: str) -> Tuple[Edge, ...]:
    """Materialize each retained aggregate tie for comparison, not progression."""

    fresh = fresh_label(stage)
    if code == "aggregate_all_carrier":
        endpoints = stage.carrier
    elif code == "aggregate_active_orbit":
        endpoints = active_endpoints(stage)
        if not endpoints:
            raise ValueError("active-orbit aggregation requires an active edge")
    else:
        raise ValueError("unknown aggregate candidate")
    return normalize_edges(stage.edges + tuple(make_edge(fresh, endpoint) for endpoint in endpoints))


def degree_profile(carrier: Sequence[int], edges: Iterable[Edge]) -> Tuple[int, ...]:
    """A presentation-free finite graph signature used only to retain a tie."""

    degree = {node: 0 for node in carrier}
    for left, right in edges:
        degree[left] += 1
        degree[right] += 1
    return tuple(sorted(degree.values()))


def candidate_grammar(stage: Stage) -> Tuple[Candidate, ...]:
    """Assess every declared candidate without promoting a label to a theorem."""

    closure_disposition = (
        Disposition.UNIQUE if active_measure(stage) > 0 else Disposition.REFUTED
    )
    closure_reason = (
        "Closure settles the exact active finite set deterministically."
        if closure_disposition is Disposition.UNIQUE
        else "There is no active finite set for same-carrier closure to resolve."
    )
    return (
        Candidate(
            code="no_op",
            kind=CandidateKind.NO_OP,
            disposition=Disposition.OPEN,
            cost=(0, 0),
            imports=(),
            reason="It preserves the present state but supplies no successor rule.",
        ),
        Candidate(
            code="same_carrier_closure",
            kind=CandidateKind.SAME_CARRIER_CLOSURE,
            disposition=closure_disposition,
            cost=(0, 1),
            imports=(),
            reason=closure_reason,
        ),
        Candidate(
            code="single_pair_lift",
            kind=CandidateKind.SINGLE_PAIR_LIFT,
            disposition=Disposition.CONDITIONAL,
            cost=(1, 2),
            imports=("named-anchor", "fresh-label convention"),
            reason=(
                "The standard lift is executable only after its anchor and "
                "fresh-label conventions are admitted."
            ),
        ),
        Candidate(
            code="aggregate_all_carrier",
            kind=CandidateKind.ORBIT_AGGREGATE_LIFT,
            disposition=Disposition.TIED,
            cost=(1, 1),
            imports=("fresh-label convention",),
            reason=(
                "This aggregate lift has the declared minimum aggregate cost; "
                "the grammar supplies no proof that it beats its retained peer."
            ),
            alternatives=("aggregate_active_orbit",),
        ),
        Candidate(
            code="aggregate_active_orbit",
            kind=CandidateKind.ORBIT_AGGREGATE_LIFT,
            disposition=Disposition.TIED,
            cost=(1, 1),
            imports=("fresh-label convention",),
            reason=(
                "This distinct aggregate lift has the same declared cost as "
                "aggregate_all_carrier and is retained rather than selected."
            ),
            alternatives=("aggregate_all_carrier",),
        ),
        Candidate(
            code="observer_extension",
            kind=CandidateKind.OBSERVER_EXTENSION,
            disposition=Disposition.OPEN,
            cost=(0, 1),
            imports=("observer grammar",),
            reason=(
                "No observer-extension grammar is supplied here that also "
                "yields a certified carrier lift and matching descent record; "
                "its absence from this grammar is not a refutation."
            ),
        ),
    )


def retained_ties(candidates: Iterable[Candidate]) -> Tuple[Candidate, ...]:
    """Keep every lowest-cost tied candidate; no selector resolves the tie."""

    tied = tuple(candidate for candidate in candidates if candidate.disposition is Disposition.TIED)
    if not tied:
        return ()
    minimum = min(candidate.cost for candidate in tied)
    return tuple(candidate for candidate in tied if candidate.cost == minimum)


def apply_permutation(edge: Edge, permutation: Sequence[Tuple[int, int]]) -> Edge:
    """Apply a finite carrier permutation to one canonical edge."""

    mapping = dict(permutation)
    return make_edge(mapping[edge[0]], mapping[edge[1]])


def symmetric_single_pair_failure() -> SymmetryWitness:
    """Exhaust the two possible one-pair outputs in a swapped pair orbit."""

    pair_orbit = (make_edge(0, 1), make_edge(2, 3))
    permutation = ((0, 2), (1, 3), (2, 0), (3, 1))
    lexical_selection = min(pair_orbit)
    transported_selection = apply_permutation(lexical_selection, permutation)
    transported_orbit = tuple(sorted(apply_permutation(edge, permutation) for edge in pair_orbit))
    selection_after_transport = min(transported_orbit)
    return SymmetryWitness(
        carrier=(0, 1, 2, 3),
        pair_orbit=pair_orbit,
        permutation=permutation,
        lexical_selection=lexical_selection,
        transported_selection=transported_selection,
        selection_after_transport=selection_after_transport,
    )


def no_swap_stable_single_pair_choice() -> bool:
    """Check both finite selectors: the swap moves either selected pair."""

    witness = symmetric_single_pair_failure()
    return all(
        apply_permutation(choice, witness.permutation) != choice
        for choice in witness.pair_orbit
    )


def negative_single_pair_candidate() -> Candidate:
    """The single-pair grammar's scoped negative classification."""

    return Candidate(
        code="single_pair_lift_on_swapped_pair_orbit",
        kind=CandidateKind.SINGLE_PAIR_LIFT,
        disposition=Disposition.REFUTED,
        cost=(1, 0),
        imports=(),
        reason=(
            "The two possible selected pairs are exchanged by the displayed "
            "swap, so neither remains stable in this finite fixture."
        ),
    )


def _stage_data(stage: Stage, invariant: ReplayInvariant) -> dict[str, Any]:
    return {
        "active_obstruction": active_measure(stage),
        "carrier": list(stage.carrier),
        "distinctions": [list(edge) for edge in stage.edges],
        "n": stage.index,
        "replay_invariant": invariant.to_data(),
        "settled": [list(edge) for edge in stage.settled],
        "state_key": state_key(stage),
    }


def model_report(horizon: int = MAX_HORIZON) -> dict[str, Any]:
    """Return a deterministic, scope-labelled report for stages zero through 15.

    Every entry of ``laws_checked`` can fail: each compares two independently
    computed objects or exercises a rejection path.  A check that held by
    construction, ``down(up(stage)) == stage``, was removed for that reason.
    """

    stages = build_tower(horizon)
    lifts = tuple(up(stage) for stage in stages)
    invariants = tuple(replay_invariant(stage) for stage in stages)
    provisional = lifts[0].target
    candidates = candidate_grammar(provisional)
    ties = retained_ties(candidates)
    all_carrier = aggregate_effect(provisional, "aggregate_all_carrier")
    active_orbit = aggregate_effect(provisional, "aggregate_active_orbit")
    witness = symmetric_single_pair_failure()
    return {
        "admissions": list(CONDITIONAL_ADMISSIONS),
        "candidate_grammar": [candidate.to_data() for candidate in candidates],
        "horizon": horizon,
        "laws_checked": {
            "each_emitted_round_closure_decreases_active_measure": all(
                active_measure(lift.target) > active_measure(closure(lift.target))
                for lift in lifts[:-1]
            ),
            "descent_rejects_an_uncertified_lift_record": all(
                descent_rejects(replace(lift, target=closure(lift.target))) for lift in lifts
            ),
            "old_distinctions_are_preserved": all(
                set(before.edges).issubset(after.edges)
                for before, after in zip(stages, stages[1:])
            ),
            "replay_invariant_holds": all(invariant.holds for invariant in invariants),
            "replay_reconstructs_every_completed_stage": all(
                replay(stage.history) == stage for stage in stages
            ),
            "structural_descent_inverts_each_certified_lift": all(
                structural_descent(lift.target) == down(lift) for lift in lifts
            ),
        },
        "negative_fixture": {
            "candidate": negative_single_pair_candidate().to_data(),
            "no_swap_stable_single_pair_choice": no_swap_stable_single_pair_choice(),
            "witness": witness.to_data(),
        },
        "retained_ties": {
            "candidates": [candidate.code for candidate in ties],
            "degree_profiles": {
                "aggregate_active_orbit": list(
                    degree_profile(provisional.carrier + (fresh_label(provisional),), active_orbit)
                ),
                "aggregate_all_carrier": list(
                    degree_profile(provisional.carrier + (fresh_label(provisional),), all_carrier)
                ),
            },
            "same_effect": all_carrier == active_orbit,
        },
        "schema": "finite-replay-lift-descent-v1",
        "scope": {
            "status": "conditional-finite-fixture",
            "terminal": [
                "The listed admissions are inputs, not derived structure.",
                "The report establishes a replayable finite trace only through the stated horizon.",
                "The symmetric fixture refutes one-pair swap-stable selection only in its displayed orbit.",
                "No unqualified endogenous or unbounded tower conclusion is issued.",
            ],
        },
        "stages": [
            _stage_data(stage, invariant) for stage, invariant in zip(stages, invariants)
        ],
    }


def render_report(horizon: int = MAX_HORIZON) -> bytes:
    """Serialize the report with byte-stable JSON formatting and a final LF."""

    return _canonical_bytes(model_report(horizon)) + b"\n"


def write_report(output: Path, horizon: int = MAX_HORIZON) -> None:
    """Write the deterministic report to a caller-selected path."""

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(render_report(horizon))
