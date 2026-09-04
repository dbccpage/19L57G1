"""Run the rung-two track-one cross-check and write the receipt.

Deterministic: no timestamp, no environment value, keys sorted, LF only.
The receipt regenerates byte-identically.  Predictions are scored
mechanically from the computed values; a miss is recorded next to its
value and never edited.

Usage: python research/second_nofirst/run_nofirst.py [--receipts DIR]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from typing import Any, Optional

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

# `nofirst` puts the sealed kernel and the sibling tree on the path, so it
# is imported before anything drawn from either.
from nofirst import (  # noqa: E402
    ALPHABET,
    Alphabet,
    APART,
    FREE,
    FREE_STAKE,
    Node,
    Stake,
    all_apart_stake,
    declared_stakes,
    demands,
    dishonoured_labelled_pairs,
    empty_profile_data,
    enumerate_by_levels,
    enumerate_rectangle,
    event_kind,
    first_demand,
    grow_once,
    honour,
    inert_event_kinds,
    kind_occurrences,
)
from derivation.engine import READINGS  # noqa: E402
from derivation.model import replay  # noqa: E402

CROSSCHECK_DEPTH = 3


def measure_reading(
    reading_name: str,
    genesis: tuple[Any, ...],
    stakes: tuple[Stake, ...],
    alphabet: Alphabet = ALPHABET,
    crosscheck_depth: int = CROSSCHECK_DEPTH,
) -> dict[str, Any]:
    base = replay(genesis)
    nodes, bound_stops, grammar_refusals = enumerate_rectangle(genesis, alphabet)

    free_nonempty = 0
    unlabelled_demands = 0
    total_demands = 0
    totality_mismatches = 0
    for node in nodes:
        for s in stakes:
            ds = demands(s, node.regime)
            total_demands += len(ds)
            if s.name == FREE_STAKE.name and ds:
                free_nonempty += 1
            for label, pair in ds:
                if s.label(pair[0], pair[1]) == FREE:
                    unlabelled_demands += 1
            # Totality: the classifier's demand pairs must equal the
            # population computed independently by `honour`.
            if tuple(p for _, p in ds) != dishonoured_labelled_pairs(s, node.regime):
                totality_mismatches += 1

    # First demand, per stake, over every sequence of the rectangle.
    first: dict[str, dict[str, Any]] = {}
    for s in stakes:
        indices: dict[str, int] = {}
        disagreements = 0
        with_demand = 0
        for node in nodes:
            fd = first_demand(genesis, node.history, s)
            if fd.index is None:
                continue
            with_demand += 1
            key = fd.kind if fd.kind is not None else "genesis"
            indices[key] = indices.get(key, 0) + 1
            if fd.dishonoured_index != fd.index:
                disagreements += 1
        earliest = min(
            (
                fd.index
                for fd in (first_demand(genesis, n.history, s) for n in nodes)
                if fd.index is not None
            ),
            default=None,
        )
        first[s.name] = {
            "earliest_index": earliest,
            "index_agrees_with_first_dishonoured": disagreements == 0,
            "sequences_with_a_demand": with_demand,
            "first_event_kinds": dict(sorted(indices.items())),
        }

    inert, exercised = inert_event_kinds(base, nodes, stakes)

    # The at-most-one measurements, under the stake labelling every
    # distinct pair apart.
    apart = all_apart_stake()
    demand_free = 0
    max_empty_profiles = 0
    max_new_demands = 0
    max_total_demands_after = 0
    growth_steps = 0
    generating_one = 0
    generating_none = 0
    for node in nodes:
        if demands(apart, node.regime):
            continue
        demand_free += 1
        max_empty_profiles = max(
            max_empty_profiles, len(empty_profile_data(node.regime))
        )
        if node.regime.n_data() >= alphabet.max_data:
            continue
        grown = grow_once(node.regime, "<grow>")
        growth_steps += 1
        fresh = grown.n_data() - 1
        after = demands(apart, grown)
        new = [p for _, p in after if p[1] == fresh or p[0] == fresh]
        max_new_demands = max(max_new_demands, len(new))
        # The TOTAL bound the Lean theorem states: the grown regime carries
        # at most one demand altogether, old pairs included.
        max_total_demands_after = max(max_total_demands_after, len(after))
        if len(new) == 1:
            generating_one += 1
        elif not new:
            generating_none += 1

    # The one-sided total commitment against the sibling's all-apart stake.
    # Reported as null, never as zero, when the caller's stake list does not
    # carry it: a comparison that was not made must not read as a comparison
    # that found no difference.
    one_sided = next((s for s in stakes if s.name == "one_sided_total"), None)
    one_sided_diffs: Optional[int] = None
    if one_sided is not None:
        one_sided_diffs = sum(
            1
            for node in nodes
            if demands(one_sided, node.regime) != demands(apart, node.regime)
        )

    # Cross-check: the second enumerator's reach on the declared family.
    small = enumerate_rectangle(
        genesis,
        Alphabet(
            alphabet.supply_token,
            alphabet.fresh_tokens,
            alphabet.arities,
            alphabet.max_data,
            alphabet.max_forms,
            crosscheck_depth,
        ),
    )
    reach_a = frozenset(n.regime for n in small[0])
    reach_b, visits_b = enumerate_by_levels(genesis, alphabet, crosscheck_depth)

    return {
        "reading": reading_name,
        "genesis_data": base.n_data(),
        "nodes": len(nodes),
        "bound_stops": bound_stops,
        "grammar_refusals": grammar_refusals,
        "distinct_regimes": len(frozenset(n.regime for n in nodes)),
        "max_data_reached": max(n.regime.n_data() for n in nodes),
        "max_forms_reached": max(len(n.regime.forms) for n in nodes),
        "event_kind_occurrences": dict(sorted(kind_occurrences(nodes).items())),
        "demands": {
            "total_recorded": total_demands,
            "free_stake_nodes_with_a_demand": free_nonempty,
            "demands_at_an_unlabelled_pair": unlabelled_demands,
            "totality_mismatches": totality_mismatches,
        },
        "first_demand": first,
        "inert_event_kinds": list(inert),
        "exercised_event_kinds": list(exercised),
        "all_apart": {
            "demand_free_nodes": demand_free,
            "growth_steps_generating_no_demand": generating_none,
            "growth_steps_generating_one_demand": generating_one,
            "growth_steps_taken": growth_steps,
            "max_empty_profiles_at_a_demand_free_node": max_empty_profiles,
            "max_new_demands_per_growth_step": max_new_demands,
            "max_total_demands_after_one_growth_step": max_total_demands_after,
        },
        "one_sided_total_differs_from_all_apart_at": one_sided_diffs,
        "crosscheck": {
            "depth": crosscheck_depth,
            "first_enumerator_regimes": len(reach_a),
            "second_enumerator_regimes": len(reach_b),
            "reach_agrees": reach_a == reach_b,
            "second_enumerator_visits": visits_b,
        },
    }


def score(readings: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Score every prediction mechanically from the computed values."""
    out: dict[str, dict[str, Any]] = {}

    def verdict(pid: str, hit: bool, value: Any) -> None:
        out[pid] = {"verdict": "HIT" if hit else "MISSED", "value": value}

    free_bad = sum(r["demands"]["free_stake_nodes_with_a_demand"] for r in readings)
    verdict("N-13", free_bad == 0, free_bad)

    unlabelled = sum(r["demands"]["demands_at_an_unlabelled_pair"] for r in readings)
    mismatch = sum(r["demands"]["totality_mismatches"] for r in readings)
    verdict("N-14", unlabelled == 0 and mismatch == 0,
            {"at_free_pairs": unlabelled, "totality_mismatches": mismatch})

    agree = all(
        s["index_agrees_with_first_dishonoured"]
        for r in readings
        for s in r["first_demand"].values()
    )
    verdict("N-15", agree, {
        r["reading"]: {
            n: s["index_agrees_with_first_dishonoured"]
            for n, s in r["first_demand"].items()
        }
        for r in readings
    })

    inert = sorted(set.intersection(*[set(r["inert_event_kinds"]) for r in readings]))
    verdict("N-16", len(inert) == 2, {"count": len(inert), "kinds": inert})

    empties = max(r["all_apart"]["max_empty_profiles_at_a_demand_free_node"]
                  for r in readings)
    new = max(r["all_apart"]["max_new_demands_per_growth_step"] for r in readings)
    total_after = max(
        r["all_apart"]["max_total_demands_after_one_growth_step"] for r in readings
    )
    witnesses = sum(
        r["all_apart"]["growth_steps_generating_one_demand"] for r in readings
    )
    verdict("N-17", empties <= 1 and new <= 1,
            {"max_empty_profiles": empties, "max_new_demands": new,
             "max_total_demands_after_one_growth_step": total_after,
             "growth_steps_generating_exactly_one": witnesses})

    values = [r["one_sided_total_differs_from_all_apart_at"] for r in readings]
    verdict("N-18", all(v == 0 for v in values), values)

    agrees = all(r["crosscheck"]["reach_agrees"] for r in readings)
    verdict("N-19", agrees, {
        r["reading"]: {
            "first": r["crosscheck"]["first_enumerator_regimes"],
            "second": r["crosscheck"]["second_enumerator_regimes"],
            "agrees": r["crosscheck"]["reach_agrees"],
        }
        for r in readings
    })
    out["N-X"] = {
        "verdict": "PENDING",
        "value": "scored by the operator packet's rung four, the removal grammar",
    }
    return out


def build(alphabet: Alphabet = ALPHABET, crosscheck_depth: int = CROSSCHECK_DEPTH
          ) -> dict[str, Any]:
    stakes = declared_stakes()
    readings = [
        measure_reading(rd.name, rd.genesis, stakes, alphabet, crosscheck_depth)
        for rd in READINGS
    ]
    scored = score(readings)
    payload: dict[str, Any] = {
        "authority_effect": "None",
        "rung": "two, track one",
        "write_root": "research/second_nofirst",
        "prompt_sha256": hashlib.sha256(
            (HERE / "PROMPT.md").read_bytes()
        ).hexdigest(),
        "predictions_sha256": hashlib.sha256(
            (HERE / "PREDICTIONS.md").read_bytes()
        ).hexdigest(),
        "alphabet": {
            "arities": list(alphabet.arities),
            "crosscheck_depth": crosscheck_depth,
            "fresh_tokens": list(alphabet.fresh_tokens),
            "max_data": alphabet.max_data,
            "max_forms": alphabet.max_forms,
            "max_sequence_length": alphabet.max_length,
            "supply_token": alphabet.supply_token,
        },
        "stakes": [s.name for s in stakes],
        "readings": readings,
        "predictions_scored": scored,
        "input_count_claim": "none",
    }
    return payload


def write(payload: dict[str, Any], receipts: pathlib.Path) -> pathlib.Path:
    receipts.mkdir(parents=True, exist_ok=True)
    target = receipts / "nofirst.json"
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    target.write_bytes(text.encode("utf-8"))
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the rung-two cross-check.")
    parser.add_argument(
        "--receipts", default=str(HERE / "receipts"), help="output directory"
    )
    args = parser.parse_args()
    receipts = pathlib.Path(args.receipts)
    payload = build()
    target = write(payload, receipts)
    size = target.stat().st_size
    print(f"wrote {target} ({size} bytes)")
    if size > 1_000_000:
        print("NOTE: the receipt exceeds one megabyte and must be split")
    for pid, res in sorted(payload["predictions_scored"].items()):
        print(f"  {pid}: {res['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
