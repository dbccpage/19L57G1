"""The declared extension on the sealed carrier, executed by the sealed kernel.

AuthorityEffect: None.  This module adds no primitive.  Every state it
produces is the sealed ``replay`` of a sealed event list; every demand it
reads is the sealed ``collapsed_pairs``; every response family it offers is
the sealed ``min_responses`` within the declared bounds, quotiented by the
sealed ``canonical`` key with every class retained.  What it declares, and
what the sealed derivation does not, are exactly two laws:

* **growth** -- one fresh datum is supplied and admitted (the sealed
  engine's external continuation policy, taken as a law of the history
  class);
* **firing** -- a collapsed pair of admitted data is the demand, and a
  minimum valid response answers it (the sealed closure policy plus the
  sealed response search, taken as a law of the history class).

Branch handling: a fire offers every retained isomorphism class.  A realized
history therefore needs a selection, and ``drive`` takes that selection as an
explicit input and records it; the family sizes are recorded alongside.

Also here, as executable negative controls for the tests: a demand generator
that reads presentation glyphs, a fire that drops tied classes, a scripted
driver that ignores its input, and a growth with no recorded event.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Optional, Sequence, cast

from derivation.candidates import (
    Bounds,
    Delta,
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    delta_events,
    min_responses,
    response_valid_naive,
)
from derivation.engine import READING_F, READING_L, Reading, closure_challenge_orbits, delta_label
from derivation.export import (
    Json,
    event_from_json,
    event_json,
    read_json_gz,
    regime_sha256,
    verify_full_export,
)
from derivation.iso import CanonKey, canonical
from derivation.model import (
    AdmitDatum,
    AdmitForm,
    AdmitRuleAll,
    Event,
    Impose,
    Pair,
    Regime,
    Supply,
    certify,
    replay,
)
from derivation.observe import collapsed_pairs, separable

BOUNDS = Bounds()
"""The declared candidate space: at most two items, form arity at most two."""

READINGS: Mapping[str, Reading] = {"L": READING_L, "F": READING_F}

JsonDict = dict[str, Json]


class IgnitionError(ValueError):
    """A refusal of the extension, named."""


# ---------------------------------------------------------------------------
# The invariant `Good`, and the demand read off the state
# ---------------------------------------------------------------------------


def mentioned(r: Regime, d: int) -> bool:
    """Some admitted instance names ``d`` (Lean ``Mentioned``)."""
    return any(d in args for (_, args) in r.insts)


def unmentioned_data(r: Regime) -> tuple[int, ...]:
    return tuple(d for d in range(r.n_data()) if not mentioned(r, d))


def rule_free(r: Regime) -> bool:
    return not r.rules


def well_formed(r: Regime) -> bool:
    """The sealed ``Regime.wf``, executed."""
    n = r.n_data()
    return (
        all(
            0 <= f < len(r.forms) and len(args) == r.forms[f] and all(a < n for a in args)
            for (f, args) in r.insts
        )
        and all(0 <= f < len(r.forms) for f in r.rules)
        and all(i < j < n for (i, j) in r.reqs)
        and all(a >= 1 for a in r.forms)
    )


def requirements_separated(r: Regime) -> bool:
    return all(separable(r, i, j) for (i, j) in sorted(r.reqs))


def good(r: Regime) -> bool:
    """Well-formed, rule-free, every standing requirement separated."""
    return well_formed(r) and rule_free(r) and requirements_separated(r)


def demands(r: Regime) -> tuple[Pair, ...]:
    """The demands a state carries under the total standing commitment:
    exactly the sealed collapsed pairs.  Read off the state; nothing emits
    them."""
    return collapsed_pairs(r)


def orbit_demands(r: Regime) -> tuple[Pair, ...]:
    """The sealed closure policy's representatives: one demand per
    automorphism orbit of the collapsed pairs."""
    return closure_challenge_orbits(r)


def verdicts(r: Regime) -> dict[Pair, bool]:
    """The observation interface: the separability verdict on every pair."""
    n = r.n_data()
    return {(i, j): separable(r, i, j) for i in range(n) for j in range(i + 1, n)}


def is_activity(r: Regime, t: Regime) -> bool:
    """A transition is activity when it changes a verdict on data both
    states hold.  Fresh names, longer histories and inert events do not."""
    n = min(r.n_data(), t.n_data())
    before, after = verdicts(r), verdicts(t)
    return any(before[(i, j)] != after[(i, j)] for i in range(n) for j in range(i + 1, n))


def is_inert(r: Regime, t: Regime) -> bool:
    return r == t


# ---------------------------------------------------------------------------
# The two laws
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Step:
    """One extension step, decoded to its sealed event block."""

    kind: str
    target: Optional[Pair]
    delta: Delta
    events: tuple[Event, ...]
    child: Regime
    tie_classes: int
    raw_minima: int
    cost: tuple[int, int]

    def label(self, base: Regime) -> str:
        return "grow" if self.kind == "grow" else delta_label(base, self.delta)


def fresh_token(r: Regime) -> str:
    """The sealed engine's fresh-name convention."""
    return f"g{r.n_data()}"


def grow(r: Regime) -> Step:
    """Growth: supply and admit one fresh datum.  Refuses a colliding name,
    because an absorbed admission would be growth in the history and not in
    the state."""
    token = fresh_token(r)
    if token in r.data:
        raise IgnitionError(f"fresh token {token!r} collides with an admitted datum")
    events: tuple[Event, ...] = (Supply(token), AdmitDatum(token))
    child = replay(events, r)
    return Step("grow", None, (), events, child, 1, 1, (0, 0))


def _classes(r: Regime, target: Pair, deltas: Sequence[Delta]) -> list[tuple[Delta, int]]:
    """The sealed quotient: group minimum deltas by the canonical key of the
    resulting regime, representative first in enumeration order, classes in
    key order.  Every class is retained."""
    grouped: dict[CanonKey, list[Delta]] = {}
    for delta in deltas:
        child = replay((Impose(*target),) + delta_events(r, delta), r)
        grouped.setdefault(canonical(child), []).append(delta)
    return [(members[0], len(members)) for _, members in sorted(grouped.items())]


def fire_at(r: Regime, target: Pair, measure: str, bounds: Bounds = BOUNDS) -> tuple[Step, ...]:
    """Fire on one demand: every retained class of minimum valid response.

    Refuses a target that is not a demand (an already separated or repeated
    pair is not a demand), and refuses a base with a rule, as the sealed
    fast path does."""
    i, j = target
    if not (0 <= i < j < r.n_data()):
        raise IgnitionError(f"target {target} is not an ordered pair of admitted data")
    if target in r.reqs:
        raise IgnitionError(f"target {target} is already a standing requirement")
    if separable(r, i, j):
        raise IgnitionError(f"target {target} is separated already: not a demand")
    if r.rules:
        raise IgnitionError("fire needs a rule-free base")
    mr = min_responses(r, target, measure, bounds)
    if mr is None:
        raise IgnitionError(f"no valid response to {target} within {bounds}")
    out: list[Step] = []
    classes = _classes(r, target, mr.deltas)
    for rep, size in classes:
        if not response_valid_naive(r, target, rep):
            raise IgnitionError(f"the sealed enumeration offered an invalid response {rep}")
        events = (Impose(i, j),) + delta_events(r, rep)
        child = replay(events, r)
        cost = (mr.cost[0], mr.cost[1]) if measure == "mu2" else (mr.cost[0], -1)
        out.append(Step("fire", target, rep, events, child, len(classes), len(mr.deltas), cost))
    return tuple(out)


def fire(r: Regime, measure: str, bounds: Bounds = BOUNDS,
         targets: Optional[Sequence[Pair]] = None) -> tuple[Step, ...]:
    """Fire on every orbit demand of the state (or on the supplied targets:
    the sealed root round answers the reading's own target)."""
    chosen = tuple(targets) if targets is not None else orbit_demands(r)
    out: list[Step] = []
    for target in chosen:
        out.extend(fire_at(r, target, measure, bounds))
    return tuple(out)


# ---------------------------------------------------------------------------
# A realized history under the fire-maximal law, with its selection recorded
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Realized:
    history: tuple[Event, ...]
    steps: tuple[Step, ...]
    selections: tuple[int, ...]
    final: Regime

    def certified(self) -> bool:
        return certify(self.history, self.final)


def drive(root_history: Sequence[Event], measure: str, n_steps: int,
          selections: Sequence[int] = (), *, closure: bool = True, growth: bool = True,
          bounds: Bounds = BOUNDS, root_targets: Optional[Sequence[Pair]] = None) -> Realized:
    """Realize one history of the extension's class from a recorded root.

    Fire-maximal: while a demand stands and ``closure`` holds, fire and take
    the branch named by the next selection (0 when the selection list is
    exhausted); otherwise, if ``growth`` holds, grow; otherwise stop.  The
    selection is an explicit input; the family it selects from is recorded
    in each step's ``tie_classes``.  ``root_targets`` answers the sealed
    reading's own target at the root, as the sealed engine does.
    """
    history = tuple(root_history)
    r = replay(history)
    steps: list[Step] = []
    used: list[int] = []
    first = True
    for _ in range(n_steps):
        targets: tuple[Pair, ...] = ()
        if closure:
            # Orbits are computed only under the closure law: the removal
            # test grows a symmetric carrier past the sealed permutation
            # budget, and reading a demand it would not act on is not its job.
            targets = tuple(root_targets) if (first and root_targets is not None) else orbit_demands(r)
        first = False
        if closure and targets:
            family = fire(r, measure, bounds, targets)
            index = selections[len(used)] if len(used) < len(selections) else 0
            if not (0 <= index < len(family)):
                raise IgnitionError(f"selection {index} outside the family of {len(family)}")
            used.append(index)
            chosen = family[index]
        elif growth:
            chosen = grow(r)
        else:
            break
        steps.append(chosen)
        history = history + chosen.events
        r = chosen.child
        assert certify(history, r)
    return Realized(history, tuple(steps), tuple(used), r)


# ---------------------------------------------------------------------------
# Exhibits
# ---------------------------------------------------------------------------


def growth_demand_record(r: Regime) -> JsonDict:
    """One growth step from ``r``: the Lean characterization, executed.
    The new demands are exactly the pairs of the fresh datum with the
    unmentioned data; at a good state there is at most one."""
    child = grow(r).child
    before = set(demands(r))
    after = set(demands(child))
    new = sorted(after - before)
    n = r.n_data()
    return {
        "data_before": n,
        "unmentioned_before": list(unmentioned_data(r)),
        "new_demands": [list(p) for p in new],
        "new_demand_count": len(new),
        "old_verdicts_unchanged": all(
            verdicts(r)[p] == verdicts(child)[p] for p in verdicts(r)
        ),
        "characterization_holds": new == [(a, n) for a in unmentioned_data(r)],
        "at_most_one": len(new) <= 1 if good(r) and not demands(r) else None,
    }


def linked_episodes(reading: Reading, measure: str, n_steps: int,
                    bounds: Bounds = BOUNDS) -> JsonDict:
    """Exhibit 2.  From the reading's Challenge 2 close: the sealed root round
    (every retained class), then for each class one realized fire-maximal
    history of ``n_steps`` further steps with selection 0 throughout, recording
    for every growth step the demand it creates and for every fire the family
    it was chosen from."""
    root_history = tuple(reading.genesis)
    root = replay(root_history)
    first_round = fire(root, measure, bounds, [reading.target])
    branches: list[Json] = []
    for index, opening in enumerate(first_round):
        history = root_history + opening.events
        assert certify(history, opening.child)
        realized = drive(history, measure, n_steps, [], bounds=bounds)
        kinds = [s.kind for s in realized.steps]
        grow_records: list[Json] = []
        state = opening.child
        for s in realized.steps:
            if s.kind == "grow":
                grow_records.append(cast(Json, growth_demand_record(state)))
            state = s.child
        fires = [s for s in realized.steps if s.kind == "fire"]
        branches.append({
            "opening_class": index,
            "opening_label": opening.label(root),
            "opening_events": [_event_json(e) for e in opening.events],
            "opening_regime_sha256": regime_sha256(opening.child),
            "steps": kinds,
            "fires": len(fires),
            "grows": kinds.count("grow"),
            "growth_records": grow_records,
            "fire_families": [s.tie_classes for s in fires],
            "fire_targets": [list(cast(Pair, s.target)) for s in fires],
            "every_fire_is_activity": all(
                is_activity(_before(realized, k), s.child)
                for k, s in enumerate(realized.steps) if s.kind == "fire"),
            "no_grow_is_activity": all(
                not is_activity(_before(realized, k), s.child)
                for k, s in enumerate(realized.steps) if s.kind == "grow"),
            "final_regime_sha256": regime_sha256(realized.final),
            "final_data": realized.final.n_data(),
            "final_reqs": len(realized.final.reqs),
            "final_good": good(realized.final),
            "history_length": len(realized.history),
            "certified": realized.certified(),
        })
    return {
        "reading": reading.name,
        "measure": measure,
        "root_target": list(reading.target),
        "root_classes": len(first_round),
        "root_raw_minima": first_round[0].raw_minima if first_round else 0,
        "root_cost": list(first_round[0].cost) if first_round else [],
        "branches": branches,
    }


def _before(realized: Realized, k: int) -> Regime:
    prefix = realized.history[: len(realized.history) - sum(len(s.events) for s in realized.steps[k:])]
    return replay(prefix)


def disabled_components(reading: Reading, measure: str, n_steps: int,
                        bounds: Bounds = BOUNDS) -> JsonDict:
    """Exhibit 2, the removal test.  With the closure law off the state only
    grows and no verdict ever changes; with the growth law off the run stops
    at the closure fixpoint."""
    root_history = tuple(reading.genesis)
    root = replay(root_history)
    opening = fire(root, measure, bounds, [reading.target])[0]
    history = root_history + opening.events
    no_closure = drive(history, measure, n_steps, [], closure=False, bounds=bounds)
    no_growth = drive(history, measure, n_steps, [], growth=False, bounds=bounds)
    full = drive(history, measure, n_steps, [], bounds=bounds)
    return {
        "reading": reading.name,
        "measure": measure,
        "requested_steps": n_steps,
        "no_closure": {
            "steps": len(no_closure.steps),
            "kinds": sorted(set(s.kind for s in no_closure.steps)),
            "any_activity": any(is_activity(_before(no_closure, k), s.child)
                                for k, s in enumerate(no_closure.steps)),
            "final_demands": len(demands(no_closure.final)),
            "final_data": no_closure.final.n_data(),
        },
        "no_growth": {
            "steps": len(no_growth.steps),
            "kinds": sorted(set(s.kind for s in no_growth.steps)),
            "stopped_at_fixpoint": not demands(no_growth.final),
            "final_data": no_growth.final.n_data(),
        },
        "both_laws": {
            "steps": len(full.steps),
            "kinds": sorted(set(s.kind for s in full.steps)),
            "fires": sum(1 for s in full.steps if s.kind == "fire"),
            "final_data": full.final.n_data(),
        },
    }


def route_pair() -> JsonDict:
    """Exhibit 1, on the sealed carrier.  Two histories with one endpoint:
    commit a rule before growing, or after.  The span total differs, the
    endpoint does not, and every continuation agrees."""
    base_history: tuple[Event, ...] = (AdmitDatum("a"), AdmitDatum("b"), AdmitForm(1))
    base = replay(base_history)
    early: tuple[Event, ...] = (AdmitRuleAll(0), AdmitDatum("c"))
    late: tuple[Event, ...] = (AdmitDatum("c"), AdmitRuleAll(0))
    end_early = replay(early, base)
    end_late = replay(late, base)
    continuation: tuple[Event, ...] = (AdmitForm(1), AdmitDatum("d"), Impose(0, 3))
    return {
        "base_regime_sha256": regime_sha256(base),
        "endpoints_equal": end_early == end_late,
        "endpoint_regime_sha256": regime_sha256(end_early),
        "span_total_early": span_total(early, base),
        "span_total_late": span_total(late, base),
        "continuations_agree": replay(continuation, end_early) == replay(continuation, end_late),
    }


def span_total(history: Sequence[Event], base: Regime) -> int:
    """The span weighting of the merged path-cost family, on the sealed
    events: a rule costs the carrier it ranges over when it is made."""
    total = 0
    r = base
    for e in history:
        if isinstance(e, AdmitRuleAll):
            total += r.n_data()
        r = replay((e,), r)
    return total


# ---------------------------------------------------------------------------
# The fixpoint census over the sealed closed exports
# ---------------------------------------------------------------------------


def reconstruct(payload: Mapping[str, Json]) -> tuple[dict[int, Regime], dict[int, str]]:
    """Regimes and statuses of every node, along creation edges."""
    if not verify_full_export(payload):
        raise IgnitionError("the sealed certification of the export failed")
    root_history = tuple(
        event_from_json(cast(Mapping[str, Json], e))
        for e in cast(Sequence[Json], payload["root_history"]))
    nodes = cast(Sequence[Mapping[str, Json]], payload["nodes"])
    edges = cast(Sequence[Mapping[str, Json]], payload["edges"])
    histories: dict[int, tuple[Event, ...]] = {0: root_history}
    creation = {cast(int, e["child"]): e for e in edges if e["kind"] == "creation"}
    for node in nodes:
        nid = cast(int, node["id"])
        if nid == 0:
            continue
        edge = creation[nid]
        parent = cast(int, edge["parent"])
        events = tuple(event_from_json(cast(Mapping[str, Json], e))
                       for e in cast(Sequence[Json], edge["events"]))
        histories[nid] = histories[parent] + events
    regimes = {nid: replay(h) for nid, h in histories.items()}
    statuses = {cast(int, node["id"]): cast(str, node["status"]) for node in nodes}
    for node in nodes:
        nid = cast(int, node["id"])
        if regime_sha256(regimes[nid]) != node["regime_sha256"]:
            raise IgnitionError(f"node {nid}: replayed regime hash differs from the record")
    return regimes, statuses


def fixpoint_census(root: Path) -> JsonDict:
    """At every closure fixpoint of the two closed exports: the state is
    good, one growth step creates as many demands as there are unmentioned
    data (at most one), and two growth steps create the fresh pair."""
    out: JsonDict = {}
    for name in ("closed_L", "closed_F"):
        payload = cast(Mapping[str, Json], read_json_gz(root / "artifacts" / "full" / f"{name}.json.gz"))
        regimes, statuses = reconstruct(payload)
        fixpoints = sorted(nid for nid, status in statuses.items() if status == "terminal_all_separated")
        rows: list[Json] = []
        for nid in fixpoints:
            r = regimes[nid]
            record = growth_demand_record(r)
            twice = grow(grow(r).child).child
            n = r.n_data()
            rows.append({
                "node": nid,
                "good": good(r),
                "data": n,
                "unmentioned": record["unmentioned_before"],
                "one_growth_new_demands": record["new_demand_count"],
                "characterization_holds": record["characterization_holds"],
                "two_growths_fresh_pair_demanded": (n, n + 1) in demands(twice),
            })
        out[name] = {
            "nodes": len(regimes),
            "fixpoints": len(fixpoints),
            "all_good": all(cast(bool, cast(Mapping[str, Json], row)["good"]) for row in rows),
            "all_characterizations_hold": all(
                cast(bool, cast(Mapping[str, Json], row)["characterization_holds"]) for row in rows),
            "all_two_growths_demand": all(
                cast(bool, cast(Mapping[str, Json], row)["two_growths_fresh_pair_demanded"])
                for row in rows),
            "one_growth_demand_histogram": _histogram(
                cast(int, cast(Mapping[str, Json], row)["one_growth_new_demands"]) for row in rows),
            "rows": rows,
        }
    return out


def _histogram(values: Iterable[int]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        counts[str(value)] = counts.get(str(value), 0) + 1
    return dict(sorted(counts.items()))


# ---------------------------------------------------------------------------
# Negative controls (exercised by the tests; never used by the exhibits)
# ---------------------------------------------------------------------------


def glyph_demands(r: Regime) -> tuple[Pair, ...]:
    """A demand generator that reads presentation glyphs: it keeps a
    collapsed pair only when the tokens sort the same way as the indices.
    The comparison it hides is the glyph order, a supplied ``q``."""
    return tuple((i, j) for (i, j) in collapsed_pairs(r) if r.data[i] < r.data[j])


def represent(r: Regime, tokens: Sequence[str]) -> Regime:
    """The same structure under other presentation tokens."""
    if len(tokens) != r.n_data() or len(set(tokens)) != len(tokens):
        raise IgnitionError("a presentation needs one distinct token per datum")
    return Regime(tuple(tokens), r.forms, r.insts, r.rules, r.reqs)


def fire_first_class_only(r: Regime, target: Pair, measure: str,
                          bounds: Bounds = BOUNDS) -> tuple[Step, ...]:
    """A fire that drops every tied class but the first."""
    return fire_at(r, target, measure, bounds)[:1]


def retains_all_classes(steps: Sequence[Step], r: Regime, target: Pair, measure: str,
                        bounds: Bounds = BOUNDS) -> bool:
    """The retention check: the offered classes are all the classes of the
    sealed minimum family."""
    mr = min_responses(r, target, measure, bounds)
    if mr is None:
        return not steps
    expected = {canonical(replay((Impose(*target),) + delta_events(r, d), r)) for d in mr.deltas}
    offered = {canonical(s.child) for s in steps}
    return offered == expected


def scripted_events(script: Sequence[Event]) -> tuple[Event, ...]:
    """A precomputed future: the same events whatever the state."""
    return tuple(script)


def input_dependent(step_of: Sequence[tuple[Regime, tuple[Event, ...]]]) -> bool:
    """A conditional machine answers different states with different event
    blocks somewhere; a script does not."""
    blocks = {events for (_, events) in step_of}
    return len(blocks) > 1


def phantom_grow(r: Regime) -> Regime:
    """Growth with no recorded event: the state grows, the history does not."""
    return Regime(r.data + (fresh_token(r),), r.forms, r.insts, r.rules, r.reqs)


def regressing_response_example() -> tuple[Regime, Pair, Delta]:
    """A response that separates its target and collapses a standing
    requirement: marking datum 1 with the form that already marks datum 0."""
    base = Regime(("a", "b", "c"), (1,), frozenset({(0, (0,))}), frozenset(), frozenset({(0, 1)}))
    delta: Delta = (NewInst(0, (1,)),)
    return base, (1, 2), delta


def _event_json(e: Event) -> Json:
    return cast(Json, event_json(e))


__all__ = [
    "BOUNDS", "READINGS", "IgnitionError", "Step", "Realized",
    "mentioned", "unmentioned_data", "rule_free", "well_formed", "requirements_separated", "good",
    "demands", "orbit_demands", "verdicts", "is_activity", "is_inert",
    "fresh_token", "grow", "fire_at", "fire", "drive",
    "growth_demand_record", "linked_episodes", "disabled_components", "route_pair", "span_total",
    "reconstruct", "fixpoint_census",
    "glyph_demands", "represent", "fire_first_class_only", "retains_all_classes",
    "scripted_events", "input_dependent", "phantom_grow", "regressing_response_example",
    "NewDatum", "NewForm", "NewInst", "NewRuleAll",
]
