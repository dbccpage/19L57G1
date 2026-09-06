"""One bounded continuation stage, with attempted and accepted rounds separate.

The boundary is an admitted primitive. State, validity, candidates, bookkeeping
and limits are declared metatheory; the exported census is computation. No
earlier result decides the validity of a new demand: it is recomputed on the
replayed configuration. In particular, null success is not lack of a response.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from functools import cache
from itertools import combinations
from typing import Any

from boundary import challenge2, challenge4, challenge5, continuation1 as prior, model
from boundary.challenge3 import one_step_minima
from boundary.presentation import read_nested_whole

Json = dict[str, Any]
PREDICTIONS_SHA256 = "f4b3ebf85ad0176352647a606e8dd856674fb153d89e10e17d48f4734cf26f06"
ATTEMPT_BOUND = 4
ACCEPTED_BOUND = 4
NODE_CEILING = 1000
BRANCHING_BOUND = 3
MARK_BOUND = 8
BOOL_COORDINATES = challenge4.COORDINATES[:-1]


@dataclass(frozen=True)
class State:
    origin: prior.Branch
    aug: challenge4.Augmentation
    policy: str | None
    events: tuple[model.Event, ...] = ()
    groups: tuple[int, ...] = ()


@dataclass(frozen=True)
class Challenge:
    inscription: str | None = None
    demand: tuple[int, int] | None = None


@dataclass(frozen=True)
class Response:
    kind: str = "null"
    value: str = ""
    cost: int = 0

    def name(self) -> str:
        return self.kind if not self.value else f"{self.kind}:{self.value}"


def initial(branch: prior.Branch) -> State:
    return State(branch, branch.aug, branch.policy)


@cache
def origin_configuration(reading: str, branch: prior.Branch) -> model.Configuration:
    if not prior.branch_certified(reading, branch):
        raise ValueError(f"uncertified origin: {reading}/{branch.label()}")
    return prior.branch_configuration(reading, branch)


def configuration(reading: str, state: State) -> model.Configuration:
    base = origin_configuration(reading, state.origin)
    regime = model.replay(full_history(state), model.genesis(reading))
    return model.Configuration(regime, base.groups + state.groups)


def full_history(state: State) -> tuple[model.Event, ...]:
    """Keep supplies in the genesis prefix: a regime alone does not retain them."""
    branch = state.origin
    if branch.policy is None:
        prefix = prior.inherited_history(branch)
    else:
        prefix = challenge5.flat_history(read_nested_whole(challenge5.INSCRIPTION), branch.policy)
    return tuple(prefix) + state.events


def renamings(reading: str, state: State) -> model.Renamings:
    return challenge4.renamings(reading, state.aug)


def requirement(reading: str, state: State, pair: tuple[int, int]) -> str:
    current = configuration(reading, state)
    if any(tag not in current.groups for tag in pair):
        return "disappeared"
    met = model.wholes_separable_in(current, *pair, renamings(reading, state))
    return "met" if met else "unresolved"


def requirements(reading: str, state: State, demands: tuple[tuple[int, int], ...]) -> Json:
    return {f"{a},{b}": requirement(reading, state, (a, b)) for a, b in demands}


def next_challenge(
    reading: str, state: State, generator: prior.Generator,
    presented: tuple[int, ...], demands: tuple[tuple[int, int], ...],
) -> Challenge | None:
    """Extend the frozen generator's search to the line's evolving records."""
    if generator == prior.ENUMERATION_GENERATOR:
        index = prior.first_missing(presented, len(prior.domain_texts()))
        return None if index is None else Challenge(prior.domain_texts()[index])
    if generator == prior.DEMAND_GENERATOR:
        tags = sorted(set(configuration(reading, state).groups))
        remaining = [pair for pair in combinations(tags, 2) if pair not in demands]
        return None if not remaining else Challenge(demand=remaining[0])
    raise ValueError(f"generator is outside the inherited minimum space: {generator}")


def candidates(reading: str, state: State, challenge: Challenge) -> list[Response]:
    """Every member of the declared atomic response space, plus a priced bundle.

Offer every not-yet-declared Boolean capability of Challenge 4; occurrence
admission on either side; all different admitting Challenge 5 policies; and
retention of the generated whole under the currently declared policy. A policy
declaration changes future retention only, never the past. No simultaneous
multi-coordinate adoption is a one-step response. The two-capability recording
policy is present and refused as a bundle. There is no new depth or glyph rule.
    """
    out = [Response()]
    for coordinate in BOOL_COORDINATES:
        if not getattr(state.aug, coordinate):
            out.append(Response("declare", coordinate, 1))
    out.extend(Response("occurrence", str(side), 1) for side in (0, 1))
    for policy in challenge5.POLICY_SPACE[1:]:
        if policy != state.policy:
            out.append(Response("policy", policy, len(challenge5.POLICY_CAPABILITIES[policy])))
    if challenge.inscription is not None:
        out.append(Response("retain", cost=1))
    return out


def apply_response(reading: str, state: State, challenge: Challenge, response: Response) -> State:
    """One explicit declaration/admission, applied only after candidate selection."""
    if response.kind == "null":
        return state
    if response.kind == "declare":
        return replace(state, aug=replace(state.aug, **{response.value: True}))
    if response.kind == "policy":
        return replace(state, policy=response.value)
    current = configuration(reading, state)
    tag = max(current.groups, default=-1) + 1
    if response.kind == "occurrence":
        supplied = next(event.token for event in full_history(state) if isinstance(event, model.Supply))
        event = model.AdmitOccurrence(supplied, int(response.value))
        return replace(state, events=state.events + (event,), groups=state.groups + (tag,))
    if response.kind != "retain" or challenge.inscription is None:
        raise ValueError(f"unknown or inapplicable response: {response.name()}")
    policy = state.policy or challenge5.POLICY_REFUSE
    retained = challenge5.retain(
        reading, read_nested_whole(challenge.inscription), policy, challenge.inscription
    )
    if retained.regime is None:
        raise ValueError(f"retention refused: {retained.refusal}")
    if retained.deep is not None and any(len(address) > 1 for address in retained.deep.addresses):
        raise ValueError("depth exceeds this continuation's flat admission grammar")
    events = tuple(challenge5.flat_history(read_nested_whole(challenge.inscription), policy))
    return replace(state, events=state.events + events, groups=state.groups + (tag,) * retained.regime.n_marks())


def valid(reading: str, before: State, after: State, challenge: Challenge) -> bool:
    """A supply imposes no admission obligation. A demand must actually be met.

Already met carried requirements may not be lost; unresolved old requirements
persist and are not silently promoted into new challenges. The executor checks
those preservation clauses with its actual requirement record separately.
    """
    current = configuration(reading, after)
    if current.regime.n_marks() > MARK_BOUND:
        return False
    if challenge.demand is not None:
        return requirement(reading, after, challenge.demand) == "met"
    return challenge.inscription is not None and configuration(reading, before).regime.reading == reading


@cache
def policy_key(reading: str, policy: str | None) -> str:
    if policy is None:
        return "no policy"
    return json.dumps(challenge5.domain_behaviour(reading, challenge5.Point(policy)), sort_keys=True)


def state_key(reading: str, state: State, demands: tuple[tuple[int, int], ...]) -> str:
    """Joint configuration/requirement key; the U action includes reflection.

The grouping stays in this metatheoretic key even when it is unavailable to
object-language observation, since it fixes future generated demands. Thus this
is deliberately finer than the observational key. Policy behaviour is compared
over the entire inherited domain; no hash decides its equality.
    """
    rn = renamings(reading, state)
    images = []
    for _reflection, _pi, sigma, image in model.permitted_configuration_images(configuration(reading, state), rn):
        moved = sorted(tuple(sorted(model.relabel_groups(pair, sigma))) for pair in demands)
        images.append(repr((model.configuration_key(image, rn), image.groups, moved)))
    return repr((challenge4.effective_structure(reading, state.aug), policy_key(reading, state.policy), min(images)))


def response_rows(
    reading: str, state: State, challenge: Challenge, demands: tuple[tuple[int, int], ...],
) -> tuple[list[Json], list[list[Response]]]:
    rows: list[Json] = []
    valid_points: list[tuple[Response, str]] = []
    before = requirements(reading, state, demands)
    for response in candidates(reading, state, challenge):
        row: Json = {"name": response.name(), "cost": response.cost, "one_step_or_null": response.cost <= 1}
        try:
            if response.cost > 1:
                raise ValueError("bundles undeclared capabilities")
            after = apply_response(reading, state, challenge, response)
            row["valid"] = valid(reading, state, after, challenge) and all(
                status != "met" or requirement(reading, after, pair) == "met"
                for pair, status in zip(demands, before.values())
            )
            row["refusal"] = None if row["valid"] else "challenge or carried-requirement predicate fails"
            if row["valid"]:
                carried = demands if challenge.demand is None or challenge.demand in demands else demands + (challenge.demand,)
                valid_points.append((response, state_key(reading, after, carried)))
        except ValueError as exc:
            row.update(valid=False, refusal=str(exc))
        rows.append(row)
    if not valid_points:
        return rows, []
    minimum = min(response.cost for response, _key in valid_points)
    grouped: dict[str, list[Response]] = {}
    for response, key in valid_points:
        if response.cost == minimum:
            grouped.setdefault(key, []).append(response)
    return rows, list(grouped.values())


def initial_lines(reading: str) -> list[tuple[prior.Branch, prior.Generator]]:
    """Recompute eligibility and preserve every minimum generator class."""
    out = []
    for branch in prior.declared_branches(reading):
        rows = [prior.generator_row(reading, branch, generator) for generator in prior.generator_space()]
        minimum = one_step_minima(rows, "mu1", "emits")
        by_name = {prior.generator_name(generator): generator for generator in prior.generator_space()}
        for group in minimum["classes"]:
            out.append((branch, by_name[group["members"][0]]))
    return out


def challenge_json(challenge: Challenge | None) -> Json | None:
    if challenge is None:
        return None
    return {"inscription": challenge.inscription, "demand": None if challenge.demand is None else list(challenge.demand)}


def state_json(reading: str, state: State) -> Json:
    current = configuration(reading, state)
    return {
        "declarations": list(state.aug.values()), "policy": state.policy,
        "marks": list(current.regime.marks), "placement": list(current.regime.placement),
        "groups": list(current.groups), "initial_datum": current.regime.initial_datum.internal_id,
        "origin_history": prior.branch_history(reading, state.origin),
        "full_flat_replay_history": challenge2.history_json(list(full_history(state))),
        "continuation_events": challenge2.history_json(list(state.events)),
        "continuation_groups": list(state.groups),
        "certified": model.certify(full_history(state), model.genesis(reading), current.regime),
    }


def execute(reading: str, attempt_bound: int = ATTEMPT_BOUND, node_ceiling: int = NODE_CEILING) -> Json:
    if attempt_bound < 0 or node_ceiling < 1:
        raise ValueError("invalid finite resource bound")
    roots = initial_lines(reading)
    if len(roots) > node_ceiling:
        raise ValueError("node ceiling cannot contain every inherited generator root")
    nodes: list[Json] = []
    pending: list[tuple[State, prior.Generator, tuple[int, ...], tuple[tuple[int, int], ...], int, int, str | None, list[str]]] = []
    for branch, generator in roots:
        pending.append((initial(branch), generator, tuple(prior.presented_indices()), prior.IMPOSED_DEMANDS, 0, 0, None, []))
    frontier: list[str] = []
    terminals: list[str] = []
    while pending:
        state, generator, presented, demands, attempted, accepted, parent, response_members = pending.pop(0)
        node_id = f"{reading}{len(nodes)}"
        challenge = next_challenge(reading, state, generator, presented, demands)
        node: Json = {
            "id": node_id, "parent": parent, "origin": state.origin.label(),
            "generator": prior.generator_name(generator), "attempted": attempted, "accepted": accepted,
            "generator_adoption": {"capabilities": prior.capabilities(generator), "cost": prior.mu1(generator), "classification": "metatheory apparatus"},
            "presented": list(presented), "demands": [list(pair) for pair in demands],
            "state": state_json(reading, state), "requirements": requirements(reading, state, demands),
            "incoming_minimum_class": response_members, "challenge": challenge_json(challenge),
            "candidate_rows": [], "minimum_classes": [], "status": "expanded",
        }
        nodes.append(node)
        if challenge is None:
            node["status"] = "no_next_challenge"
            terminals.append(node_id)
            continue
        if attempted >= attempt_bound or accepted >= ACCEPTED_BOUND:
            node["status"] = "attempt_bound" if attempted >= attempt_bound else "accepted_bound"
            frontier.append(node_id)
            continue
        rows, groups = response_rows(reading, state, challenge, demands)
        node["candidate_rows"] = rows
        node["minimum_classes"] = [[point.name() for point in group] for group in groups]
        if not groups:
            node["status"] = "no_valid_response"
            terminals.append(node_id)
            continue
        if len(groups) > BRANCHING_BOUND or len(nodes) + len(pending) + len(groups) > node_ceiling:
            node["status"] = "branching_bound" if len(groups) > BRANCHING_BOUND else "node_ceiling"
            frontier.append(node_id)
            continue
        for group in groups:
            response = group[0]
            after = apply_response(reading, state, challenge, response)
            new_presented, new_demands = presented, demands
            if challenge.inscription is not None:
                new_presented += (prior.domain_texts().index(challenge.inscription),)
                after = replace(after, events=state.events + (model.Supply(challenge.inscription),) + after.events[len(state.events):])
            if challenge.demand is not None:
                new_demands += (challenge.demand,)
            pending.append((after, generator, new_presented, new_demands, attempted + 1,
                            accepted + int(response.kind != "null"), node_id, [point.name() for point in group]))
    return {
        "reading": reading, "root_count": len(roots), "node_count": len(nodes),
        "attempt_bound": attempt_bound, "accepted_bound": ACCEPTED_BOUND,
        "node_ceiling": node_ceiling, "branching_bound": BRANCHING_BOUND,
        "seed_accepted_target": prior.SEED_ROUND_BOUND, "nodes": nodes,
        "frontier": frontier, "terminals": terminals,
        "accepted_total": sum(node["accepted"] for node in nodes if node["id"] in frontier + terminals),
    }


def score(readings: Json) -> Json:
    u, o = readings["U"], readings["O"]
    forests = [u, o]
    nodes = [node for forest in forests for node in forest["nodes"]]
    roots = [node for node in nodes if node["parent"] is None]
    supply = [node for node in roots if node["challenge"]["inscription"] is not None]
    demand = [node for node in roots if node["challenge"]["demand"] is not None]
    checks = {
        "S2-1": u["root_count"] == 7 and o["root_count"] == 5,
        "S2-2": bool(supply) and all(node["minimum_classes"] == [["null"]] and any(row["cost"] > 0 and row["valid"] for row in node["candidate_rows"]) for node in supply),
        "S2-3": bool(demand) and all(node["minimum_classes"] == [["null"]] for node in demand),
        "S2-4": all(node["accepted"] == 0 and len(node["minimum_classes"]) <= 1 for node in nodes),
        "S2-5": any(forest["frontier"] for forest in forests),
        "S2-6": all(any("unresolved" in node["requirements"].values() for node in forest["nodes"] if node["id"] in forest["frontier"] + forest["terminals"]) for forest in forests),
    }
    scores: Json = {name: {"status": "HIT" if hit else "MISSED", "basis": "deterministic computation in the declared finite space"} for name, hit in checks.items()}
    scores["S2-X"] = {"status": "PENDING", "basis": "beyond the executed prefix; not computed"}
    s1_clauses = {
        "every_first_challenge_supplies_the_predicted_text": all(node["challenge"]["inscription"] == "<|b>" for node in roots),
        "no_first_accepted_augmentation": all(child["accepted"] == 0 for child in nodes if child["attempted"] == 1),
        "first_response_is_null": all(node["minimum_classes"] == [["null"]] for node in roots),
        "no_first_split": all(len(node["minimum_classes"]) == 1 for node in roots),
        "every_branch_stops_for_want_of_a_response_before_the_bound": all(node["status"] == "no_valid_response" and node["accepted"] < ACCEPTED_BOUND for node in nodes if node["id"] in u["frontier"] + u["terminals"] + o["frontier"] + o["terminals"]),
    }
    scores["S1-X"] = {"status": "HIT" if all(s1_clauses.values()) else "PARTIAL" if any(s1_clauses.values()) else "MISSED", "clauses": s1_clauses}
    scores["C5-X"] = {"status": "HIT" if all(forest["frontier"] and all(node["accepted"] < 15 for node in forest["nodes"]) for forest in forests) else "MISSED", "scope": "the four prior clauses retain their stage-1 scope; exact frontier is exported here; completeness is a computed bounded census, not an unbounded theorem"}
    return scores


def build() -> Json:
    readings = {reading: execute(reading) for reading in model.READINGS}
    return {
        "stage": 2, "authority_effect": "None", "seed_sha256": prior.SEED_SHA256,
        "predictions_sha256": PREDICTIONS_SHA256, "provenance": "SOURCE_ISOLATED_WITH_DECLARED_PRIOR_EXPOSURE",
        "capabilities": {"admitted boundary": {"classification": "admitted primitive", "declarations": 1}},
        "bounds": {"attempts": ATTEMPT_BOUND, "accepted": ACCEPTED_BOUND, "marks": MARK_BOUND,
                   "nodes_per_reading": NODE_CEILING, "minimum_classes_per_attempt": BRANCHING_BOUND},
        "validity": "recompute the generated demand; supply has no retention demand; preserve carried met requirements; mark bound applies",
        "boundary_dependence": "The supplied inscriptions, placement and renaming action use the paid boundary. Attempt accounting, enumeration, replay checks and finite resource limits are metatheory.",
        "readings": readings, "scores": score(readings),
        "completeness_status": "COMPUTED: every retained generator root and every enumerated minimum response class is expanded or named on the exact frontier within the declared bounds",
        "open": ["unbounded continuation", "universal minimality", "outside of the outermost boundary", "depth convergence", "unbounded renaming correspondence", "Python and Lean semantic correspondence"],
    }


def render(receipt: Json) -> bytes:
    return (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8")


def verify_export(receipt: Json) -> list[str]:
    """Independent fresh execution checks roots, edges, states and the frontier.

It is algorithmic replay, not an independent mathematical implementation.
The first unequal named path identifies a deleted tie or corrupted history.
    """
    def difference(actual: Any, expected: Any, path: str) -> list[str]:
        if type(actual) is not type(expected):
            return [f"{path}: value type differs"]
        if isinstance(expected, dict):
            if set(actual) != set(expected):
                return [f"{path}: field census differs"]
            return [problem for key in expected for problem in difference(actual[key], expected[key], f"{path}.{key}")]
        if isinstance(expected, list):
            if len(actual) != len(expected):
                return [f"{path}: member census differs"]
            return [problem for i, (a, e) in enumerate(zip(actual, expected)) for problem in difference(a, e, f"{path}[{i}]")]
        return [] if actual == expected else [f"{path}: replayed value differs"]
    return difference(receipt, build(), "continuation2")
