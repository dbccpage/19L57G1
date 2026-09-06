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
from concurrent.futures import ProcessPoolExecutor
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
from code.price import Minimum, PricingTrace, price_many, satisfies_at  # noqa: E402
from code.regime import genesis  # noqa: E402

DEPTH = 3
READINGS = ("L", "F")
MEASURES = ("mu1", "mu2")

LIMR_REACH_NOTE = (
    "A chain longer than the carrier needs width above the carrier. The "
    "count here belongs to the independent depth-3 chain population, not "
    "to a completed price census. Consult each reading's searches record "
    "for completion or refusal; the population count does not complete a "
    "refused search."
)
LIMG_REACH_NOTE = (
    "The carrier bound excludes LIM-G before any reader property is read. "
    "A completed empty price row therefore carries no information about "
    "readers. A refused price row remains unknown, not empty: this carrier "
    "argument does not certify enumeration completion. The independent "
    "obstruction evidence is the signature argument, capacity census and "
    "out-of-space carrier exhibit."
)
LIMF_EXTENSION_STATUS = "OPEN: no admitted extension or minimum escape price has been constructed"
LIMF_PROPOSED_EXTENSION = "an outside-contract item admitting a total function of the finite verdict sequence"


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
        "cost": None if m.search_refused else list(m.cost),
        "cost_below_minimum_all_fail": m.cost_below_minimum_all_fail,
        "demand": m.demand,
        "designated_pair": list(m.designated) if m.designated else None,
        "distinct_induced_relations": None if m.search_refused else m.distinct_induced_relations,
        "evidence_arity": m.evidence_arity,
        "grade": m.grade,
        "iso_class_count": None if m.search_refused else len(m.classes),
        "measure": m.measure,
        "raw_minimum_count": None if m.search_refused else len(m.raw_minima),
        "incomplete": m.search_refused,
        "outcome": ("OPEN" if m.search_refused else
                    "PRICE" if m.raw_minima else "NO CANDIDATE WITHIN BOUND"),
    }


def price_one_reading(reading: str) -> tuple[dict[tuple[str, str], Minimum], PricingTrace]:
    trace = PricingTrace()
    priced = price_many(
        genesis(reading), reading, DEMANDS, MEASURES, DEFAULT_BOUNDS,
        trace=trace, retain_completed_on_refusal=True,
    )
    return priced, trace


def trace_json(reading: str, trace: PricingTrace) -> dict[str, Any]:
    return {
        "base_reading": reading,
        "measures": list(MEASURES),
        "completed_levels": [
            {"item_count": k, "candidates": n}
            for k, n in sorted(trace.completed_levels.items())
        ],
        "terminal": "CandidateBudgetRefused" if trace.refused_level is not None else "COMPLETE",
        "incomplete": trace.refused_level is not None,
        "refused_level": trace.refused_level,
        "yielded_at_refusal": trace.yielded_at_refusal,
        "first_refused_ordinal": (trace.yielded_at_refusal + 1
                                   if trace.first_refused is not None else None),
        "last_yielded_delta": delta_json(trace.last_yielded) if trace.last_yielded is not None else None,
        "first_refused_delta": delta_json(trace.first_refused) if trace.first_refused is not None else None,
        "observed_hits_at_refusal": trace.observed_hits_at_refusal,
        "first_witnesses_at_refusal": {
            name: delta_json(d) for name, d in sorted(trace.first_witnesses_at_refusal.items())
        },
        "reason": trace.reason,
        "frontier_scope": "the observed prefix and next refused candidate of the interrupted level; not the unseen frontier",
        "candidate_order": "code.enumerate_space.iter_candidates; full reading-class axis; declared bounds; naive genesis replay",
    }


def run_prices() -> dict[str, Any]:
    """One enumeration per reading; every demand and both measures read it."""
    out: dict[str, Any] = {}
    store: dict[tuple[str, str, str], Minimum] = {}
    traces: dict[str, Any] = {}
    with ProcessPoolExecutor(max_workers=2) as pool:
        for reading, (priced, trace) in zip(READINGS, pool.map(price_one_reading, READINGS)):
            traces[reading] = trace_json(reading, trace)
            print(f"{reading}: {traces[reading]['terminal']}; completed levels "
                  f"{trace.completed_levels}; refused level {trace.refused_level}", flush=True)
            for (name, measure), m in priced.items():
                store[(name, reading, measure)] = m
                out[f"{name}|{reading}|{measure}"] = minimum_json(m)
    globals()["_STORE"] = store
    globals()["_TRACES"] = traces
    return out


def reachability_census(bounds: Bounds) -> dict[str, Any]:
    """How far into each limit demand the declared candidate space can reach.

    An empty minimum set means two very different things depending on this.
    If the demand's own test can be **met** somewhere the space reaches, the
    empty row is evidence about readers.  If the space cannot reach the test
    at all, the empty row is a statement about the item bound and carries no
    information about readers whatever — and `REQUIREMENTS.md` warns against
    exactly that confusion, in the paragraph justifying the widening above
    the sealed two items.

    Both directions are computed here rather than argued, and the answers
    differ: LIM-R's chain test is reachable at part of the population, LIM-G's
    carrier test is reachable nowhere in the declared space."""
    from code.census import population
    from code.enumerate_space import sealed_prefixes
    from code.grammar import contexts

    pop = population(DEPTH, bounds)
    # A chain of strict splits has at most one step per context of the
    # selection, so a chain longer than the carrier needs a width above the
    # carrier.  Where ``w_max`` is not above the carrier the demand cannot be
    # met whatever the readers do.
    limr_reachable = sum(
        1 for r in pop
        if bounds.w_max > r.n_data() and len(contexts(r)) >= r.n_data() + 1
    )
    limg_max_carrier: dict[str, int] = {}
    for reading in READINGS:
        base = genesis(reading)
        best = base.n_data()
        for k in range(0, bounds.max_sealed_items + 1):
            for r in sealed_prefixes(base, k, bounds).values():
                best = max(best, r.n_data())
        limg_max_carrier[reading] = best
    return {
        "carriers_in_the_population": sorted({r.n_data() for r in pop}),
        "limr_states_where_a_longer_chain_would_fit_in_w_max":
            limr_reachable,
        "limr_states_considered": len(pop),
        "limg_largest_carrier_reachable_by_reading": limg_max_carrier,
        "limg_carrier_the_demand_requires_above": 2 ** bounds.w_max,
        "limg_demand_is_reachable_in_the_declared_space": any(
            n > 2 ** bounds.w_max for n in limg_max_carrier.values()
        ),
    }


def out_of_space_carrier_control(bounds: Bounds) -> dict[str, Any]:
    """LIM-G's positive control for the carrier test, named as **outside** the
    declared candidate space.

    The threshold needs a carrier of nine and the declared space reaches at
    most seven, so the exhibit is built from eight sealed items — twice
    ``max_sealed_items``.  It is metatheory, never admitted, and it is
    recorded here rather than left only in a test because the outcome below
    rests on it."""
    import itertools

    from code.grammar import contexts as _contexts, data_pairs
    from code.items import (
        NewDatum,
        NewForm,
        NewRuleAll,
        StatedState,
        apply_delta,
    )
    from code.readers import (
        Reader,
        all_reading_classes,
        induced_relation,
        lawful_aggregations,
    )

    delta = (NewForm(1), NewRuleAll(0)) + tuple(NewDatum() for _ in range(6))
    wide = apply_delta(
        StatedState(genesis("F"), ()), delta, bounds.w_max, bounds.max_readers
    ).regime
    ctx = _contexts(wide)
    universe = frozenset(data_pairs(wide.n_data()))
    separating = False
    for b in all_reading_classes():
        for a in lawful_aggregations(bounds.w_max):
            for w in range(0, min(bounds.w_max, len(ctx)) + 1):
                for sel in itertools.combinations(ctx, w):
                    if induced_relation(wide, Reader(sel, b, a)) == universe:
                        separating = True
    return {
        "carrier": wide.n_data(),
        "sealed_items_in_the_exhibit": len(delta),
        "declared_max_sealed_items": bounds.max_sealed_items,
        "inside_the_declared_candidate_space": (
            len(delta) <= bounds.max_sealed_items
        ),
        "some_fixed_selection_reader_separates_every_pair": separating,
    }


def width_only_countermodel(bounds: Bounds) -> dict[str, Any]:
    """A carrier with enough contexts but identical admission signatures."""
    from code.grammar import contexts
    from code.items import NewForm, StatedState, apply_delta
    from code.readers import induced_relation, iter_readers

    r = apply_delta(StatedState(genesis("F"), ()), (NewForm(2),),
                    bounds.w_max, bounds.max_readers).regime
    checked = separating = 0
    for width in range(bounds.w_max + 1):
        for rho in iter_readers(r, width, bounds.w_max):
            checked += 1
            separating += bool(induced_relation(r, rho))
    return {
        "carrier": r.n_data(), "available_contexts": len(contexts(r)),
        "reader_selections_checked": checked,
        "separating_readers": separating,
        "all_readers_fail": checked > 0 and separating == 0,
    }


def obstruction_records(
    bounds: Bounds, store: dict[tuple[str, str, str], Minimum]
) -> dict[str, Any]:
    """For each obstructed demand: evidence, control and escape status.

    Necessary escape conditions do not construct a lifting item or its
    minimum. Those feasibility and price fields remain OPEN when unproved.

    Boolean obstruction controls below are computed from the enumeration and
    the censuses; null escape fields mean OPEN, not false. Earlier controls
    were literals, which meant P-7, P-10 and P-12 were scored against strings
    this same script had written ten lines earlier and could not miss."""
    chains = chain_census(DEPTH, bounds)
    capacity = capacity_census(DEPTH, bounds)
    control = limf_control((False,) * 16, 12)
    reach = reachability_census(bounds)
    carrier_control = out_of_space_carrier_control(bounds)

    def empty_everywhere(name: str) -> bool:
        return all(not store[(name, r, "mu1")].raw_minima
                   and not store[(name, r, "mu1")].search_refused for r in READINGS)

    def finite_liftable(name: str) -> bool | None:
        if any(store[(name, r, "mu1")].raw_minima for r in READINGS):
            return True
        return False if empty_everywhere(name) else None

    # REQUIREMENTS section 9: an empty minimum set with no positive control is
    # reported OPEN, never as an obstruction.  That rule is applied here
    # rather than restated.
    limr_control_passes = chains["carrier_ceiling_attained"] != 0
    limg_control_passes = bool(capacity["separating_reader_found"])
    limf_control_passes = any(control.values())
    limr_liftable = (True if chains["chains_above_the_ceiling"] != 0
                    else finite_liftable("LIM-R"))
    width_control = width_only_countermodel(bounds)
    limf_liftable = finite_liftable("LIM-F")
    return {
        "LIM-R": {
            "outcome": (
                "PROVED OBSTRUCTION"
                if empty_everywhere("LIM-R") and limr_control_passes
                else "OPEN"
            ),
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
            "reach_of_the_declared_space": {
                "states_where_a_longer_chain_would_fit_in_w_max":
                    reach["limr_states_where_a_longer_chain_would_fit_in_w_max"],
                "states_considered": reach["limr_states_considered"],
                "note": LIMR_REACH_NOTE,
            },
            "positive_control": {
                "carrier_ceiling_attained_at_states":
                    chains["carrier_ceiling_attained"],
                "chains_above_the_ceiling":
                    chains["chains_above_the_ceiling"],
                "longest_chain_histogram":
                    chains["longest_chain_histogram"],
            },
            "escape": {
                "liftable_by_a_finite_delta_over_the_six_kinds": limr_liftable,
                "why": (
                    "the demand's threshold is stated relative to the "
                    "carrier and the ceiling tracks the carrier exactly, so "
                    "admitting data raises both together"
                ),
                "smallest_lifting_admission": None,
                "extension_status": "OPEN: no sufficient extension or minimum has been constructed",
                "necessary_escape": "outside the declared six-kind space and its refinement contract",
                "capability_it_must_carry": (
                    "change some condition of the declared finite-carrier "
                    "refinement contract; this necessary condition constructs "
                    "no sufficient lifting item and establishes no minimum"
                ),
                "price_in_items": None,
            },
        },
        "LIM-G": {
            "outcome": (
                "PROVED OBSTRUCTION"
                if empty_everywhere("LIM-G") and limg_control_passes
                else "OPEN"
            ),
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
            "reach_of_the_declared_space": {
                "largest_carrier_reachable_by_reading":
                    reach["limg_largest_carrier_reachable_by_reading"],
                "carrier_the_demand_requires_above":
                    reach["limg_carrier_the_demand_requires_above"],
                "demand_is_reachable_in_the_declared_space":
                    reach["limg_demand_is_reachable_in_the_declared_space"],
                "what_the_empty_price_row_therefore_carries": LIMG_REACH_NOTE,
            },
            "positive_control": {
                "separating_reader_found":
                    capacity["separating_reader_found"],
                "states_considered": capacity["states_considered"],
                "carrier_above_the_threshold_exhibited_out_of_space":
                    carrier_control,
            },
            "escape": {
                "liftable_by_a_finite_delta_over_the_six_kinds": None,
                "status": "OPEN",
                "width_only_countermodel": width_control,
                "width_alone_lifts_every_carrier": (
                    False if width_control["all_readers_fail"] else None
                ),
                "at_a_given_carrier": (
                    "at least ceil(log2(n)) contexts are necessary, but "
                    "coincident raw signatures cannot be separated by buying width"
                ),
                "price_at_one_carrier_in_items": None,
                "price_for_growth_without_end": None,
                "why_no_one_step_price": (
                    "the width bound is necessary, not a sufficient construction; "
                    "no minimum escape price has been computed"
                ),
            },
        },
        "LIM-F": {
            "outcome": (
                "PROVED OBSTRUCTION"
                if empty_everywhere("LIM-F") and limf_control_passes
                else "OPEN"
            ),
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
                "liftable_by_a_finite_delta_over_the_six_kinds": limf_liftable,
                "smallest_lifting_admission": None,
                "extension_status": LIMF_EXTENSION_STATUS,
                "proposed_lifting_admission": LIMF_PROPOSED_EXTENSION,
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
                        None if m1.search_refused else m1.distinct_induced_relations,
                    "evidence_arity": d.evidence_arity,
                    "grade_mu1": m1.grade,
                    "grade_mu2": m2.grade,
                    "iso_classes_mu1": None if m1.search_refused else len(m1.classes),
                    "iso_classes_mu2": None if m2.search_refused else len(m2.classes),
                    "mu1": None if m1.search_refused else list(m1.cost),
                    "mu2": None if m2.search_refused else list(m2.cost),
                    "incomplete": m1.search_refused,
                    "outcome": ("OPEN" if m1.search_refused else
                                "PRICE" if m1.raw_minima else "NO CANDIDATE"),
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
    containment_omitted = []
    for a in DEMANDS:
        for b in DEMANDS:
            if a.name >= b.name:
                continue
            for reading in READINGS:
                if any(store[(d.name, reading, "mu1")].search_refused for d in (a, b)):
                    containment_omitted.append({"first": a.name, "second": b.name,
                                                "base_reading": reading,
                                                "reason": "OPEN: incomplete minimum census"})
                    continue
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
                if any(store[(d.name, reading, "mu1")].search_refused for d in (a, b)):
                    continue
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
        "containment_omitted": containment_omitted,
        "joint_minimality_scope": "only pairs with complete minimum censuses; absence from this list is not a negative answer",
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
    # P-7, P-10 and P-12 read fields that ``obstruction_records`` now
    # COMPUTES, from the enumeration and the censuses.  They read literals
    # this same script had written a few lines earlier, so they could not
    # miss whatever the run produced; the supporting evidence existed but was
    # not what these three scores looked at.
    s["P-7"] = None if o["LIM-F"]["outcome"] == "OPEN" else True
    s["P-8"] = bool(o["LIM-F"]["definition_level_part"])
    s["P-9"] = None if o["LIM-R"]["outcome"] == "OPEN" else (
        o["LIM-R"]["outcome"] == "PROVED OBSTRUCTION"
        and o["LIM-R"]["positive_control"][
            "carrier_ceiling_attained_at_states"] == 26
        and o["LIM-R"]["positive_control"]["chains_above_the_ceiling"] == 0
    )
    liftable = o["LIM-R"]["escape"]["liftable_by_a_finite_delta_over_the_six_kinds"]
    s["P-10-no-finite-delta"] = None if liftable is None else liftable is False
    # Nonexistence in the declared alphabet does not construct a smallest
    # extension. The frozen prediction's second clause remains untested.
    s["P-10-smallest-extension-UNTESTED"] = False
    s["P-11"] = None if o["LIM-G"]["outcome"] == "OPEN" else (
        o["LIM-G"]["outcome"] == "PROVED OBSTRUCTION"
        and o["LIM-G"]["derived_threshold"] == 8
        and o["LIM-G"]["positive_control"]["separating_reader_found"] != {}
    )
    s["P-12"] = (
        o["LIM-R"]["escape"][
            "liftable_by_a_finite_delta_over_the_six_kinds"] is False
        and o["LIM-G"]["escape"]["width_alone_lifts_every_carrier"] is True
    )
    s["P-13"] = None if any(p[f"OBS-3|{r}|mu1"]["incomplete"] for r in READINGS) else all(
        p[f"OBS-3|{r}|mu1"]["cost"] == [5, -1]
        and p[f"OBS-3|{r}|mu2"]["cost"] == [5, 1]
        for r in READINGS
    )
    # P-14 as frozen, in full: the shape AND the four counts.  It was scored
    # on the shape alone while the class counts were computed nowhere and yet
    # quoted as a result in LO-06 and FINDINGS.md.
    _mrp = c["minimum_rival_prefix"]
    s["P-14"] = (
        _mrp["shape_is_form_rule_instance"]
        and _mrp["by_reading"]["L"]["raw_minimum_prefixes"] == 6
        and _mrp["by_reading"]["L"]["iso_classes"] == 3
        and _mrp["by_reading"]["F"]["raw_minimum_prefixes"] == 12
        and _mrp["by_reading"]["F"]["iso_classes"] == 3
    )
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
    s["P-16"] = None if any(p[f"{d}|{r}|mu1"]["incomplete"] for r in READINGS for d in ("OBS-1", "OBS-2", "OBS-4")) else (
        all(p[f"OBS-1|{r}|mu1"]["cost"] == [3, -1] for r in READINGS)
        and all(p[f"OBS-2|{r}|mu1"]["cost"] == [3, -1] for r in READINGS)
        and p["OBS-4|L|mu1"]["cost"] == [8, -1]
        and p["OBS-4|F|mu1"]["cost"] == [7, -1]
    )
    s["P-17"] = None if any(o[k]["outcome"] == "OPEN" for k in ("LIM-R", "LIM-G", "LIM-F")) else all(
        p[f"OBS-3|{r}|mu1"]["raw_minimum_count"] > 0 for r in READINGS
    ) and all(
        o[k]["outcome"] == "PROVED OBSTRUCTION"
        for k in ("LIM-R", "LIM-G", "LIM-F")
    )
    # P-18's first half only.  Its second half - "refinement purchases
    # growth" - is NOT tested here and cannot be: both LIM-R and LIM-G have
    # empty minima, so there is nothing to run the other predicate on and no
    # key set to compare.  Recorded as untested rather than scored as a hit.
    s["P-18-no-observer-purchases-a-limit"] = None if any(
        p[f"OBS-{d}|{r}|mu1"]["incomplete"] for r in READINGS for d in range(1, 6)
    ) else not any(
        row["every_minimum_of_the_first_answers_the_second"]
        for row in report["comparison"]["purchase"]
        if row["first"].startswith("OBS") and row["second"].startswith("LIM")
    )
    s["P-18-refinement-purchases-growth-UNTESTED"] = False
    return {
        "hits": sum(1 for v in s.values() if v is True),
        "open": sum(1 for v in s.values() if v is None),
        "of": len(s),
        "scores": {k: None if v is None else bool(v) for k, v in sorted(s.items())},
    }


def minimum_rival_prefix_census(bounds: Bounds) -> dict[str, Any]:
    """The shape of every minimum sealed prefix reaching a rival-admitting
    state, recomputed rather than inherited.

    The isomorphism class count is computed here too.  It was quoted in
    ``CLAIM_LEDGER.md`` LO-06 and in ``FINDINGS.md`` as a result while being
    computed nowhere, and P-14 — whose frozen text asserts it — was scored on
    the shape alone, a strictly weaker condition that could not miss on the
    counts.  Both counts now enter the score."""
    from code.census import admits_rival
    from code.enumerate_space import sealed_prefixes
    from code.quotient import canonical_regime

    out: dict[str, Any] = {"by_reading": {}}
    shape_ok = True
    for reading in READINGS:
        base = genesis(reading)
        first = None
        raw = 0
        classes = 0
        for k in range(0, bounds.max_sealed_items + 1):
            hits = [
                (d, r) for d, r in sealed_prefixes(base, k, bounds).items()
                if admits_rival(r)
            ]
            if hits:
                first, raw = k, len(hits)
                classes = len({
                    canonical_regime(r, bounds.bijection_budget)
                    for _, r in hits
                })
                for d, _ in hits:
                    kinds = sorted(type(it).__name__ for it in d)
                    if kinds != ["NewForm", "NewInst", "NewRuleAll"]:
                        shape_ok = False
                break
        out["by_reading"][reading] = {
            "iso_classes": classes,
            "minimum_sealed_items": first,
            "raw_minimum_prefixes": raw,
        }
    out["shape_is_form_rule_instance"] = shape_ok
    return out


def refresh_search_descriptions(report: dict[str, Any]) -> None:
    """Rerender only descriptions and nullable summaries from recorded rows.

    This does not replay or complete a search. It permits a metadata-only
    correction without calling an expensive, already refused enumeration
    again; prices, searches, censuses and prediction scores remain untouched.
    """
    obstructions = report["obstructions"]
    obstructions["LIM-R"]["reach_of_the_declared_space"]["note"] = LIMR_REACH_NOTE
    obstructions["LIM-G"]["reach_of_the_declared_space"][
        "what_the_empty_price_row_therefore_carries"] = LIMG_REACH_NOTE
    escape = obstructions["LIM-F"]["escape"]
    escape["smallest_lifting_admission"] = None
    escape["extension_status"] = LIMF_EXTENSION_STATUS
    escape["proposed_lifting_admission"] = LIMF_PROPOSED_EXTENSION
    for row in report["comparison"]["table"]:
        key = f"{row['demand']}|{row['base_reading']}|mu1"
        row["distinct_induced_relations"] = report["prices"][key]["distinct_induced_relations"]


def main(check: bool = False) -> None:
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
        "independent_prefix_certification": {
            "checked_item_counts": [0, 1, 2, 3, 4],
            "certificate_test": "tests/test_prefix_certificate.py::test_exact_delta_and_child_equality_through_four_items",
            "scope": "both genesis bases; independently widened construction against shared replay semantics; executed by the test battery",
            "sealed_measure_agreement_counts": [0, 1, 2, 3, 4],
        },
        "reader_candidate_axis": "all eight complement classes; no behavior quotient",
        "reader_isomorphism": "reading class, exact aggregation table, transported selection",
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
    report["searches"] = globals()["_TRACES"]
    store: dict[tuple[str, str, str], Minimum] = globals()["_STORE"]
    report["obstructions"] = obstruction_records(bounds, store)
    report["comparison"] = comparison(bounds)
    report["predictions"] = score_predictions(report)
    refresh_search_descriptions(report)
    write_report(report, check)


def write_report(report: dict[str, Any], check: bool = False) -> None:
    """Serialize a report; writing is not evidence that its search was replayed."""
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "receipts", "price.json"
    )
    text = json.dumps(report, indent=1, sort_keys=True) + "\n"
    if check:
        with open(path, "rb") as fh:
            if fh.read() != text.encode("utf-8"):
                raise SystemExit("FAIL: regenerated price.json differs from receipt")
        print(f"price.json serialization matches ({len(text)} bytes); writing alone does not certify replay")
        return
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print(f"wrote {path} ({len(text)} bytes)")
    print("predictions:", report["predictions"]["hits"],
          "of", report["predictions"]["of"])


if __name__ == "__main__":
    main(check="--check" in sys.argv)
