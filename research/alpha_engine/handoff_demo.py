"""Alpha handoff: four demonstrations on the sealed Challenge-3 fixtures.

AuthorityEffect: None.  No model provider: this module imports only the
sealed kernel's six pinned runtime modules and this tree.

Each demonstration runs the harness's public path (``evaluate`` ->
``make_license`` -> ``apply_licensed`` / ``explore``).  It is then checked
independently of the harness's own verdict: by sealed replay from genesis
(``derivation.model.replay``) and by a fresh recomputation from the sealed
kernel (``min_responses``, ``delta_events``, ``canonical``,
``observe.satisfies``, ``engine.challenge3_report``), never by the
harness's ``evaluate``.

1. an accepted transition (reading L, mu1, Bounds(2, 2));
2. retained ties (readings L and F, mu1, Bounds(2, 2));
3. invalid or unauthorized requests refused;
4. a bounded stop with its exported frontier (reading L, Bounds(1, 2)).

``--check`` recomputes the record and compares it with
``evidence/handoff_demo.json``; ``--write`` regenerates it deliberately,
never under a live injection.  Either mode fails if any independent check
is false.  The record carries no timestamps and no machine paths, and it is
a local receipt, not a proof.
"""

from __future__ import annotations

import argparse
from dataclasses import fields
import json
from pathlib import Path
from typing import Callable

from verify_sources import verify_sources

ROOT = Path(__file__).resolve().parent
RECORD = ROOT / "evidence" / "handoff_demo.json"


def compute() -> dict[str, object]:
    """Run the four demonstrations; import after the custody scan."""
    from derivation.candidates import Bounds, Delta, delta_events, min_responses
    from derivation.engine import (
        READING_F,
        READING_L,
        Reading,
        challenge3_report,
        delta_json_items,
    )
    from derivation.iso import CanonKey, canonical
    from derivation.model import Event, Impose, Pair, Regime, replay
    from derivation.observe import satisfies

    from driver_a import apply_licensed, explore
    from evaluate import evaluate
    from harness import (
        EvalResult,
        HarnessError,
        Node,
        RetainedClass,
        history_digest,
        jsonable,
        make_license,
    )
    from search_policy import declared_explore_first, record_census

    checks: dict[str, bool] = {}
    bounds = Bounds(max_items=2, max_arity=2)

    def fresh_classes(
        regime: Regime, target: Pair, measure: str, declared: Bounds
    ) -> dict[CanonKey, tuple[Delta, ...]]:
        """Independent recomputation: sealed minima grouped by canonical key."""
        minima = min_responses(regime, target, measure, declared)
        grouped: dict[CanonKey, list[Delta]] = {}
        if minima is None:
            return {}
        for delta in minima.deltas:
            child = replay(
                (Impose(target[0], target[1]),) + delta_events(regime, delta),
                regime,
            )
            grouped.setdefault(canonical(child), []).append(delta)
        return {key: tuple(members) for key, members in grouped.items()}

    def events_json(events: tuple[Event, ...]) -> list[object]:
        return [
            [type(event).__name__, *(jsonable(getattr(event, item.name)) for item in fields(event))]
            for event in events
        ]

    def root(reading: Reading) -> Node:
        return Node(history=reading.genesis, regime=replay(reading.genesis), license=None)

    def refusal(call: Callable[[], object]) -> dict[str, object]:
        try:
            out = call()
        except HarnessError as exc:
            return {"outcome": "refused", "error": type(exc).__name__, "message": str(exc)}
        if out is None:
            return {"outcome": "not_authorized", "error": None, "message": "apply_licensed returned None"}
        return {"outcome": "admitted", "error": None, "message": repr(out)}

    # 1. An accepted transition.
    node = root(READING_L)
    target = READING_L.target
    result = evaluate(node.regime, target, "mu1", bounds)
    keys = tuple(item.key for item in result.retained)
    policy = declared_explore_first(keys)
    license = make_license(
        granter=policy.policy_id,
        scope="handoff-C3-L-mu1",
        authorized=policy.subset(),
        source=node,
        target=target,
        measure="mu1",
        bounds=bounds,
    )
    explored = explore(node, result, license, policy.census(), target)
    child = explored.children[0]
    key = license.authorized[0]
    tail = child.history[len(node.history):]
    classes = fresh_classes(node.regime, target, "mu1", bounds)
    executed = [
        member for member in classes.get(key, ())
        if (Impose(target[0], target[1]),) + delta_events(node.regime, member) == tail
    ]
    checks["accepted.child_replays_from_genesis"] = replay(child.history) == child.regime
    checks["accepted.child_history_extends_parent"] = (
        child.history[: len(node.history)] == node.history
    )
    checks["accepted.child_key_is_the_authorized_key"] = canonical(child.regime) == key
    checks["accepted.child_satisfies_every_imposed_requirement"] = satisfies(child.regime)
    checks["accepted.executed_delta_is_a_fresh_class_member"] = len(executed) == 1
    checks["accepted.parent_unchanged"] = node.regime == replay(READING_L.genesis)
    checks["accepted.one_child_per_explored_class"] = (
        len(explored.children) == len(explored.census.explored)
    )
    accepted = {
        "reading": READING_L.name,
        "declaration": {
            "source_history_sha256": license.source,
            "target": list(target),
            "measure": license.measure,
            "bounds": [bounds.max_items, bounds.max_arity],
        },
        "authorized_key": jsonable(key),
        "executed_events": events_json(tail),
        "executed_delta": delta_json_items(executed[0]) if executed else None,
        "child_history_sha256": history_digest(child.history),
        "child_history_length": len(child.history),
        "parent_history_length": len(node.history),
        "open_alternatives": [jsonable(item) for item in explored.census.open_keys],
        "leftover_pairs_are_observations": explored.leftover_are_observations,
    }

    # 2. Retained ties.
    ties: dict[str, object] = {}
    for reading in (READING_L, READING_F):
        start = root(reading)
        evaluated = evaluate(start.regime, reading.target, "mu1", bounds)
        independent = fresh_classes(start.regime, reading.target, "mu1", bounds)
        engine = challenge3_report(reading, bounds)["mu1"]
        assert isinstance(engine, dict)
        engine_classes = engine["iso_classes"]
        assert isinstance(engine_classes, list)
        harness_classes = {item.key: item.members for item in evaluated.retained}
        tie_keys = tuple(item.key for item in evaluated.retained)
        census = declared_explore_first(tie_keys).census()
        disposed = census.explored + census.pruned + census.open_keys
        name = reading.name
        checks[f"ties.{name}.keys_and_members_match_fresh_recomputation"] = (
            harness_classes == independent
        )
        checks[f"ties.{name}.class_sizes_match_sealed_engine_quotient"] = [
            len(members) for members in harness_classes.values()
        ] == [item["class_size"] for item in engine_classes if isinstance(item, dict)]
        checks[f"ties.{name}.every_class_has_one_disposition"] = (
            sorted(disposed) == sorted(independent) and len(set(disposed)) == len(disposed)
        )
        ties[name] = {
            "retained_class_count": len(evaluated.retained),
            "class_sizes": [len(item.members) for item in evaluated.retained],
            "class_keys": [jsonable(item.key) for item in evaluated.retained],
            "explored_count": len(census.explored),
            "pruned_count": len(census.pruned),
            "open_count": len(census.open_keys),
        }

    # 3. Invalid or unauthorized requests refused.
    forged_classes = list(result.retained)
    forged_classes[0] = RetainedClass(forged_classes[0].key, ((),))
    forged = EvalResult(
        measure=result.measure,
        cost=result.cost,
        raw_minima=result.raw_minima,
        retained=tuple(forged_classes),
        found=True,
        max_items=result.max_items,
        max_arity=result.max_arity,
    )
    mu2 = evaluate(node.regime, target, "mu2", bounds)
    unlicensed = keys[1]
    bad = Node(history=READING_F.genesis, regime=node.regime, license=None)
    bad_license = make_license(
        granter="host",
        scope="handoff-bad-parent",
        authorized=(key,),
        source=bad,
        target=target,
        measure="mu1",
        bounds=bounds,
    )
    refused = {
        "substituted_empty_member": refusal(
            lambda: apply_licensed(node, forged, license, key, target)
        ),
        "license_reused_for_another_measure": refusal(
            lambda: apply_licensed(node, mu2, license, key, target)
        ),
        "key_not_named_by_the_license": refusal(
            lambda: apply_licensed(node, result, license, unlicensed, target)
        ),
        "parent_that_does_not_replay": refusal(
            lambda: apply_licensed(bad, result, bad_license, key, target)
        ),
    }
    empty_child = replay((Impose(target[0], target[1]),), node.regime)
    checks["refused.none_admitted"] = all(
        item["outcome"] != "admitted" for item in refused.values()
    )
    checks["refused.forged_member_is_not_a_fresh_class_member"] = (
        () not in classes.get(key, ())
    )
    checks["refused.forged_member_would_not_satisfy"] = not satisfies(empty_child)
    checks["refused.other_measure_has_other_classes"] = (
        fresh_classes(node.regime, target, "mu2", bounds) != classes
    )
    checks["refused.unlicensed_key_is_retained_but_not_authorized"] = (
        unlicensed in classes and unlicensed not in license.authorized
    )
    checks["refused.bad_parent_does_not_replay"] = replay(bad.history) != bad.regime
    checks["refused.parent_unchanged"] = replay(node.history) == node.regime

    # 4. A bounded stop with its exported frontier.
    tight = Bounds(max_items=1, max_arity=2)
    stopped = evaluate(node.regime, target, "mu1", tight)
    stop_license = make_license(
        granter="host",
        scope="handoff-bounded-stop",
        authorized=(),
        source=node,
        target=target,
        measure="mu1",
        bounds=tight,
    )
    stop = explore(node, stopped, stop_license, record_census((), (), (), ()), target)
    checks["bounded.no_valid_response_within_the_bound"] = (
        min_responses(node.regime, target, "mu1", tight) is None
    )
    checks["bounded.the_bound_not_absence_stops_it"] = (
        min_responses(node.regime, target, "mu1", bounds) is not None
    )
    checks["bounded.typed_unfound_evaluation"] = (
        not stopped.found and stopped.cost is None and stopped.retained == ()
    )
    checks["bounded.nothing_admitted"] = stop.children == () and stop.census.tie_set_size == 0
    checks["bounded.parent_unchanged"] = replay(node.history) == node.regime
    bounded = {
        "outcome": "no_response_within_bounds",
        "frontier": [
            {
                "source_history_sha256": history_digest(node.history),
                "target": list(target),
                "measure": "mu1",
                "bounds": [tight.max_items, tight.max_arity],
                "status": "open_beyond_declared_bounds",
            }
        ],
        "children": len(stop.children),
    }

    return {
        "authority_effect": "None",
        "schema": "alpha-handoff-demo-v1",
        "model_provider": "none",
        "receipt_is_not_proof": True,
        "demand_policy": (
            "host-supplied: each reading's Challenge-3 target; endogenous "
            "demand generation is OPEN"
        ),
        "demonstrations": {
            "accepted_transition": accepted,
            "retained_ties": ties,
            "refused": refused,
            "bounded_stop": bounded,
        },
        "independent_checks": checks,
    }


def record_bytes() -> tuple[bytes, list[str]]:
    """The deterministic record and the names of any failed independent check."""
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed: " + "; ".join(failures))
    record = compute()
    checks = record["independent_checks"]
    assert isinstance(checks, dict)
    failed = sorted(name for name, ok in checks.items() if ok is not True)
    raw = (json.dumps(record, sort_keys=True, indent=1) + "\n").encode("utf-8")
    return raw, failed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true",
                      help="deliberately regenerate the record")
    args = parser.parse_args()
    fresh, failed = record_bytes()
    for name in failed:
        print(f"FAIL: independent check {name}")
    if failed:
        return 1
    if args.write:
        RECORD.parent.mkdir(parents=True, exist_ok=True)
        RECORD.write_bytes(fresh)
        print("WROTE: deterministic handoff demonstration record")
        return 0
    if not RECORD.is_file():
        print("FAIL: evidence/handoff_demo.json is missing")
        return 1
    on_disk = RECORD.read_bytes().replace(b"\r\n", b"\n")
    if on_disk != fresh:
        print("FAIL: evidence/handoff_demo.json differs from fresh computation")
        return 1
    print("PASS: four handoff demonstrations, each independently checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
