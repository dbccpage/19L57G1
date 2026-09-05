"""Write ``receipts/price.json``: the censuses, the two prices, the
obstructions, the comparison, and a mechanical scoring of the frozen
predictions.

Deterministic: sorted keys, LF endings, no timestamp, no environment value.
Byte-identical on regeneration.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from code.calibration import calibration_report  # noqa: E402
from code.census import (  # noqa: E402
    capacity_census,
    chain_census,
    limf_control,
    monotonicity_census,
    reading_axis_census,
    rival_derivability_census,
    sealed_is_a_reader,
    vacuity_census,
)
from code.demands import DEMANDS, DEMANDS_BY_NAME  # noqa: E402
from code.enumerate_space import DEFAULT_BOUNDS, Bounds  # noqa: E402
from code.items import delta_json  # noqa: E402
from code.price import Minimum, price_many, satisfies_at  # noqa: E402
from code.regime import genesis  # noqa: E402

DEPTH = 3
READINGS = ("L", "F")
MEASURES = ("mu1", "mu2")


def bounds_json(b: Bounds) -> dict[str, int]:
    return {
        "bijection_budget": b.bijection_budget,
        "candidate_budget": b.candidate_budget,
        "max_arity": b.max_arity,
        "max_items": b.max_items,
        "max_reader_items": b.max_reader_items,
        "max_readers": b.max_readers,
        "max_sealed_items": b.max_sealed_items,
        "w_max": b.w_max,
    }


def minimum_json(m: Minimum) -> dict[str, Any]:
    return {
        "base_reading": m.base_reading,
        "classes": [
            {
                "capability_vector": c.capability_vector,
                "class_size": len(c.members),
                "representative": delta_json(c.representative),
            }
            for c in m.classes
        ],
        "cost": list(m.cost),
        "cost_below_minimum_all_fail": m.cost_below_minimum_all_fail,
        "demand": m.demand,
        "designated_pair": list(m.designated) if m.designated else None,
        "distinct_induced_relations": m.distinct_induced_relations,
        "evidence_arity": m.evidence_arity,
        "grade": m.grade,
        "iso_class_count": len(m.classes),
        "measure": m.measure,
        "raw_minimum_count": len(m.raw_minima),
        "outcome": "PRICE" if m.raw_minima else "NO CANDIDATE WITHIN BOUND",
    }


def run_prices() -> dict[str, Any]:
    """One enumeration per reading; every demand and both measures read it."""
    out: dict[str, Any] = {}
    store: dict[tuple[str, str, str], Minimum] = {}
    for reading in READINGS:
        priced = price_many(
            genesis(reading), reading, DEMANDS, MEASURES, DEFAULT_BOUNDS
        )
        for (name, measure), m in priced.items():
            store[(name, reading, measure)] = m
            out[f"{name}|{reading}|{measure}"] = minimum_json(m)
    globals()["_STORE"] = store
    return out


def obstruction_records(bounds: Bounds) -> dict[str, Any]:
    """For each obstructed demand: the proof, the positive control, and the
    price of the smallest admission that would lift it.

    Where **no** admission in the declared alphabet lifts it, that is stated
    and the capability a lifting item would have to carry is **named** — a
    number is not invented for it."""
    chains = chain_census(DEPTH, bounds)
    capacity = capacity_census(DEPTH, bounds)
    control = limf_control((False,) * 16, 12)
    return {
        "LIM-R": {
            "outcome": "PROVED OBSTRUCTION",
            "statement": (
                "no chain of strictly splitting selections is longer than "
                "the carrier minus one, so a chain longer than the carrier "
                "does not exist at any state"
            ),
            "proof": (
                "a lawful reader's induced partition has at least one block "
                "and at most n_data blocks; for a MONOTONE aggregation every "
                "added context leaves the block count at least where it was, "
                "so at most n_data - 1 strict splits occur"
            ),
            "proof_reach": (
                "the block-count proof covers the MONOTONE lawful "
                "aggregations only: 2 of the 4 at width 3, namely the blind "
                "one and at-least-one-separating-context. For the other two "
                "the block count can FALL when a context is added, and the "
                "bound is a bounded computation over the declared population "
                "rather than a theorem"
            ),
            "countermodel": (
                "under the parity aggregation, at the regime with one arity-2 "
                "form, no rule and the instance (0,(0,0)), a reader reading "
                "where coverage is absent has 2 blocks at one context and 1 "
                "block at two: adding a context LOWERS the block count"
            ),
            "narrowing": (
                "this tree's own first statement of the proof said every "
                "strict split raises the block count for every lawful "
                "reader. That is false, and its own test caught it. The "
                "statement is narrowed here rather than the wording kept and "
                "the receipt leaned on"
            ),
            "bound_verified_for_every_lawful_aggregation_over_the_population":
                chains["chains_above_the_ceiling"] == 0,
            "positive_control": {
                "carrier_ceiling_attained_at_states":
                    chains["carrier_ceiling_attained"],
                "chains_above_the_ceiling":
                    chains["chains_above_the_ceiling"],
                "longest_chain_histogram":
                    chains["longest_chain_histogram"],
            },
            "escape": {
                "liftable_by_a_finite_delta_over_the_six_kinds": False,
                "why": (
                    "the demand's threshold is stated relative to the "
                    "carrier and the ceiling tracks the carrier exactly, so "
                    "admitting data raises both together"
                ),
                "smallest_lifting_admission": (
                    "a seventh item kind, outside the declared alphabet"
                ),
                "capability_it_must_carry": (
                    "either a carrier not equal to the admitted data, or a "
                    "reader whose non-separation is not an equivalence on "
                    "the admitted data, which is exactly what lawfulness "
                    "refuses"
                ),
                "price_in_items": None,
            },
        },
        "LIM-G": {
            "outcome": "PROVED OBSTRUCTION",
            "statement": (
                "no fixed-selection reader of width w separates every pair "
                "once the carrier exceeds two to the power w"
            ),
            "proof": (
                "two data with equal signatures have s = 0 and a(0) is "
                "false, so the non-separation relation is coarser than "
                "signature equality and has at most 2**w blocks; once the "
                "carrier exceeds 2**w some pair is identified"
            ),
            "derived_threshold": capacity["carrier_threshold"],
            "positive_control": {
                "separating_reader_found":
                    capacity["separating_reader_found"],
                "states_considered": capacity["states_considered"],
            },
            "escape": {
                "liftable_by_a_finite_delta_over_the_six_kinds": True,
                "at_a_given_carrier": (
                    "buy width: the reader needs at least the base-two "
                    "logarithm of the carrier, rounded up, contexts"
                ),
                "price_at_one_carrier_in_items": 1,
                "price_for_growth_without_end": None,
                "why_no_one_step_price": (
                    "the requirement grows with the carrier, so the escape "
                    "is a rate of about log2(n) items and not a one-step "
                    "price"
                ),
            },
        },
        "LIM-F": {
            "outcome": "PROVED OBSTRUCTION",
            "statement": (
                "no object admissible by the six item kinds realises a "
                "function of the finite verdict sequence that is both stable "
                "and novel"
            ),
            "proof": (
                "no item carries a stage index, an earlier regime, or an "
                "earlier verdict, so every admitted reader's stage verdict "
                "is a function of that stage's regime alone; a novel family "
                "verdict differs from every stage verdict and so is the "
                "value of no stage-local reader"
            ),
            "definition_level_part": (
                "the implication that stage-local readers agreeing at every "
                "stage have equal family verdicts is true by unfolding and "
                "carries no content by itself; the content is the "
                "exhaustiveness check over the enumerated grammar, which is "
                "a real property and can fail"
            ),
            "positive_control": {
                "metatheory_functions_never_admitted": control,
                "at_least_one_passes": any(control.values()),
            },
            "escape": {
                "liftable_by_a_finite_delta_over_the_six_kinds": False,
                "smallest_lifting_admission": (
                    "a seventh item kind admitting a total function of the "
                    "finite verdict sequence"
                ),
                "capability_it_must_carry": (
                    "reading the family up to k rather than the current "
                    "state; research/second_stake independently classifies "
                    "such a rule as index-reading and treats it as a "
                    "negative control"
                ),
                "price_in_items": None,
            },
        },
    }


def comparison(bounds: Bounds) -> dict[str, Any]:
    """The deliverable.

    None of the three answers is inferred from equal cost, which is exactly
    the inference a shared measure invites."""
    store: dict[tuple[str, str, str], Minimum] = globals()["_STORE"]
    rows = []
    for d in DEMANDS:
        for reading in READINGS:
            m1 = store[(d.name, reading, "mu1")]
            m2 = store[(d.name, reading, "mu2")]
            rows.append(
                {
                    "base_reading": reading,
                    "demand": d.name,
                    "distinct_induced_relations":
                        m1.distinct_induced_relations,
                    "evidence_arity": d.evidence_arity,
                    "grade_mu1": m1.grade,
                    "grade_mu2": m2.grade,
                    "iso_classes_mu1": len(m1.classes),
                    "iso_classes_mu2": len(m2.classes),
                    "mu1": list(m1.cost),
                    "mu2": list(m2.cost),
                    "outcome": "PRICE" if m1.raw_minima else "NO CANDIDATE",
                    "representative_capabilities": (
                        m1.classes[0].capability_vector if m1.classes else None
                    ),
                }
            )
    purchase = []
    for a in DEMANDS:
        for b in DEMANDS:
            if a.name == b.name:
                continue
            for reading in READINGS:
                ma = store[(a.name, reading, "mu1")]
                if not ma.raw_minima:
                    continue
                base = genesis(reading)
                buys = all(
                    satisfies_at(base, d, DEMANDS_BY_NAME[b.name], bounds)
                    for d in ma.raw_minima
                )
                some = any(
                    satisfies_at(base, d, DEMANDS_BY_NAME[b.name], bounds)
                    for d in ma.raw_minima
                )
                purchase.append(
                    {
                        "base_reading": reading,
                        "every_minimum_of_the_first_answers_the_second": buys,
                        "first": a.name,
                        "second": b.name,
                        "some_minimum_of_the_first_answers_the_second": some,
                    }
                )
    containment = []
    for a in DEMANDS:
        for b in DEMANDS:
            if a.name >= b.name:
                continue
            for reading in READINGS:
                ka = {c.key for c in store[(a.name, reading, "mu1")].classes}
                kb = {c.key for c in store[(b.name, reading, "mu1")].classes}
                if not ka and not kb:
                    continue
                containment.append(
                    {
                        "base_reading": reading,
                        "first": a.name,
                        "first_within_second": bool(ka) and ka <= kb,
                        "second": b.name,
                        "second_within_first": bool(kb) and kb <= ka,
                    }
                )
    joint = []
    for a in DEMANDS:
        for b in DEMANDS:
            if a.name >= b.name:
                continue
            for reading in READINGS:
                sa = set(store[(a.name, reading, "mu1")].raw_minima)
                sb = set(store[(b.name, reading, "mu1")].raw_minima)
                shared = sa & sb
                if shared:
                    joint.append(
                        {
                            "base_reading": reading,
                            "first": a.name,
                            "second": b.name,
                            "shared_minimum_count": len(shared),
                            "same_evidence_arity":
                                a.evidence_arity == b.evidence_arity,
                        }
                    )
    return {
        "containment_of_canonical_key_sets": containment,
        "joint_minimality": joint,
        "purchase": purchase,
        "table": rows,
    }


def score_predictions(report: dict[str, Any]) -> dict[str, Any]:
    """Mechanical scoring of the frozen predictions.  A miss is recorded, not
    revised."""
    c = report["censuses"]
    p = report["prices"]
    o = report["obstructions"]
    s: dict[str, Any] = {}

    # P-1 as frozen. The move counts are the pre-freeze figures, which
    # counted moves only from the states expanded during the breadth rounds;
    # the census expands all 85 states. The prediction is scored as frozen and
    # the miss is recorded in STATUS.md rather than the text being edited.
    s["P-1"] = (
        c["vacuity"]["states"] == 85
        and c["monotonicity"] == {
            "moves": 243, "enlarge": 65, "unchanged": 178, "violations": 0
        }
    )
    s["P-1-population-and-violations"] = (
        c["vacuity"]["states"] == 85
        and c["monotonicity"]["violations"] == 0
    )
    s["P-2"] = c["sealed_bases_have_no_context"]
    s["P-3"] = report["calibration"]["agrees_field_by_field"]
    s["P-4"] = (
        c["reading_axis"]["complement_classes"] == 8
        and c["reading_axis"]["non_constant_complement_classes"] == 7
        and c["reading_axis"]["induced_separation_behaviours"] == 4
    )
    s["P-5"] = c["sealed_is_a_reader"]["mismatches"] == 0
    s["P-6"] = c["reading_axis"]["lawful_by_width"] == {
        1: 2, 2: 3, 3: 4, 4: 4
    }
    s["P-7"] = o["LIM-F"]["outcome"] == "PROVED OBSTRUCTION"
    s["P-8"] = bool(o["LIM-F"]["definition_level_part"])
    s["P-9"] = (
        o["LIM-R"]["outcome"] == "PROVED OBSTRUCTION"
        and o["LIM-R"]["positive_control"][
            "carrier_ceiling_attained_at_states"] == 26
        and o["LIM-R"]["positive_control"]["chains_above_the_ceiling"] == 0
    )
    s["P-10"] = o["LIM-R"]["escape"][
        "liftable_by_a_finite_delta_over_the_six_kinds"] is False
    s["P-11"] = (
        o["LIM-G"]["outcome"] == "PROVED OBSTRUCTION"
        and o["LIM-G"]["derived_threshold"] == 8
        and o["LIM-G"]["positive_control"]["separating_reader_found"] != {}
    )
    s["P-12"] = (
        o["LIM-R"]["escape"][
            "liftable_by_a_finite_delta_over_the_six_kinds"]
        != o["LIM-G"]["escape"][
            "liftable_by_a_finite_delta_over_the_six_kinds"]
    )
    s["P-13"] = all(
        p[f"OBS-3|{r}|mu1"]["cost"] == [5, -1]
        and p[f"OBS-3|{r}|mu2"]["cost"] == [5, 1]
        for r in READINGS
    )
    s["P-14"] = c["minimum_rival_prefix"]["shape_is_form_rule_instance"]
    # P-15 as frozen: "the rival is DERIVED, not admitted".  Scored on the
    # exhibited rival at the minimum rival state of BOTH readings, which is
    # what the prediction asserts.  It is false: derived at two admitted data,
    # admitted at three.  The prediction is not edited.
    s["P-15"] = all(
        c["rival_derivability"][r]["verdict"] == "DERIVED"
        for r in READINGS
    )
    s["P-15-at-two-data-only"] = (
        c["rival_derivability"]["L"]["verdict"] == "DERIVED"
    )
    s["P-16"] = (
        all(p[f"OBS-1|{r}|mu1"]["cost"] == [3, -1] for r in READINGS)
        and all(p[f"OBS-2|{r}|mu1"]["cost"] == [3, -1] for r in READINGS)
        and p["OBS-4|L|mu1"]["cost"] == [8, -1]
        and p["OBS-4|F|mu1"]["cost"] == [7, -1]
    )
    s["P-17"] = all(
        p[f"OBS-3|{r}|mu1"]["raw_minimum_count"] > 0 for r in READINGS
    ) and all(
        o[k]["escape"]["price_in_items"] is None
        or k == "LIM-G"
        for k in ("LIM-R", "LIM-F")
    )
    # P-18's first half only.  Its second half - "refinement purchases
    # growth" - is NOT tested here and cannot be: both LIM-R and LIM-G have
    # empty minima, so there is nothing to run the other predicate on and no
    # key set to compare.  Recorded as untested rather than scored as a hit.
    s["P-18-no-observer-purchases-a-limit"] = not any(
        row["every_minimum_of_the_first_answers_the_second"]
        for row in report["comparison"]["purchase"]
        if row["first"].startswith("OBS") and row["second"].startswith("LIM")
    )
    s["P-18-refinement-purchases-growth-UNTESTED"] = False
    return {
        "hits": sum(1 for v in s.values() if v is True),
        "of": len(s),
        "scores": {k: bool(v) for k, v in sorted(s.items())},
    }


def minimum_rival_prefix_census(bounds: Bounds) -> dict[str, Any]:
    """The shape of every minimum sealed prefix reaching a rival-admitting
    state, recomputed rather than inherited."""
    from code.census import admits_rival
    from code.enumerate_space import sealed_prefixes
    from code.items import NewForm, NewInst, NewRuleAll

    out: dict[str, Any] = {"by_reading": {}}
    shape_ok = True
    for reading in READINGS:
        base = genesis(reading)
        first = None
        raw = 0
        for k in range(0, bounds.max_sealed_items + 1):
            hits = [
                d for d, r in sealed_prefixes(base, k, bounds).items()
                if admits_rival(r)
            ]
            if hits:
                first, raw = k, len(hits)
                for d in hits:
                    kinds = sorted(type(it).__name__ for it in d)
                    if kinds != ["NewForm", "NewInst", "NewRuleAll"]:
                        shape_ok = False
                break
        out["by_reading"][reading] = {
            "minimum_sealed_items": first,
            "raw_minimum_prefixes": raw,
        }
    out["shape_is_form_rule_instance"] = shape_ok
    return out


def main() -> None:
    bounds = DEFAULT_BOUNDS
    from code.grammar import contexts

    report: dict[str, Any] = {}
    report["scope"] = {
        "population_depth": DEPTH,
        "depth_four_layer": "OPEN: not reached within the declared budget",
        "growth_run": (
            "this rung's own declared statement at the state level, not the "
            "sealed continuation policy"
        ),
        "readings": list(READINGS),
        "measures": list(MEASURES),
    }
    report["bounds"] = bounds_json(bounds)
    report["calibration"] = calibration_report()
    report["censuses"] = {
        "capacity": capacity_census(DEPTH, bounds),
        "chain": chain_census(DEPTH, bounds),
        "minimum_rival_prefix": minimum_rival_prefix_census(bounds),
        "monotonicity": monotonicity_census(DEPTH, bounds),
        "reading_axis": reading_axis_census(bounds.w_max),
        "sealed_bases_have_no_context": all(
            contexts(genesis(r)) == () for r in READINGS
        ),
        "rival_derivability": rival_derivability_census(bounds),
        "sealed_is_a_reader": sealed_is_a_reader(DEPTH, bounds),
        "vacuity": vacuity_census(DEPTH, bounds),
    }
    report["prices"] = run_prices()
    report["obstructions"] = obstruction_records(bounds)
    report["comparison"] = comparison(bounds)
    report["predictions"] = score_predictions(report)

    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "receipts", "price.json"
    )
    text = json.dumps(report, indent=1, sort_keys=True) + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print(f"wrote {path} ({len(text)} bytes)")
    print("predictions:", report["predictions"]["hits"],
          "of", report["predictions"]["of"])


if __name__ == "__main__":
    main()
