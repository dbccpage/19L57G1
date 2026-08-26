"""Finite G4 correspondence between chain obstructions and Challenge 3.

Classification: deterministic computation within the declared rounds,
candidate bounds, readings, and measures.  Each depth-one obstruction of
``reflState n`` for ``n = 3..15`` is sent by an order-preserving endpoint
adapter to the target pair of each sealed Challenge-3 reading.  The actual
minimum-response engine is then run under ``mu1`` and ``mu2`` and its results
are quotiented by the implemented regime isomorphism.

This check does not identify the historical engine with a generator.  It
only decides the stated finite correspondence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, cast

from derivation.candidates import (
    Bounds,
    Delta,
    MinResponses,
    NewForm,
    NewInst,
    delta_events,
    min_responses,
)
from derivation.engine import READINGS, Reading, delta_json_items
from derivation.export import Json
from derivation.generator import obstructions
from derivation.iso import CanonKey, canonical
from derivation.model import Impose, Pair, Regime, replay

FIRST_N = 3
LAST_N = 15
BOUNDS = Bounds(max_items=2, max_arity=2)
MEASURES = ("mu1", "mu2")


@dataclass(frozen=True)
class MinimumClass:
    representative: Delta
    class_size: int
    mark_class: str

    @property
    def accepted_pair_mark(self) -> bool:
        return self.mark_class in {
            "unary_endpoint_mark",
            "pair_only_fresh_mark",
        }


def classify_mark(base: Regime, target: Pair, delta: Delta) -> str:
    """Classify the response shape without using its presentation label."""
    forms = [item for item in delta if isinstance(item, NewForm)]
    instances = [item for item in delta if isinstance(item, NewInst)]
    if len(delta) != 2 or len(forms) != 1 or len(instances) != 1:
        return "not_fresh_form_instance"
    form = forms[0]
    instance = instances[0]
    if instance.form != len(base.forms) or len(instance.args) != form.arity:
        return "not_fresh_form_instance"
    if any(argument not in target for argument in instance.args):
        return "outside_target_argument"
    if form.arity == 1:
        return "unary_endpoint_mark"
    return "pair_only_fresh_mark"


def quotient_minima(
    base: Regime, target: Pair, responses: MinResponses
) -> tuple[MinimumClass, ...]:
    grouped: dict[CanonKey, list[Delta]] = {}
    for delta in responses.deltas:
        child = replay(
            (Impose(target[0], target[1]),) + delta_events(base, delta),
            base,
        )
        grouped.setdefault(canonical(child), []).append(delta)
    return tuple(
        MinimumClass(
            representative=members[0],
            class_size=len(members),
            mark_class=classify_mark(base, target, members[0]),
        )
        for _, members in sorted(grouped.items())
    )


def minimum_classes(reading: Reading, measure: str) -> tuple[MinimumClass, ...]:
    base = replay(reading.genesis)
    responses = min_responses(base, reading.target, measure, BOUNDS)
    if responses is None:
        raise AssertionError("sealed progress check returned no response")
    return quotient_minima(base, reading.target, responses)


def obstruction_stream(n: int) -> tuple[Pair, ...]:
    if n < FIRST_N or n > LAST_N:
        raise ValueError("G4 is declared only for n = 3..15")
    return tuple(obstructions("none", n, {}))


def _class_json(item: MinimumClass) -> dict[str, Json]:
    return {
        "representative": cast(Json, delta_json_items(item.representative)),
        "class_size": item.class_size,
        "mark_class": item.mark_class,
        "accepted_pair_mark": item.accepted_pair_mark,
    }


def _first_bad(classes: tuple[MinimumClass, ...]) -> Optional[MinimumClass]:
    return next((item for item in classes if not item.accepted_pair_mark), None)


def g4_report() -> dict[str, Json]:
    catalog: dict[tuple[str, str], tuple[MinimumClass, ...]] = {
        (reading.name, measure): minimum_classes(reading, measure)
        for reading in READINGS
        for measure in MEASURES
    }
    per_round: list[dict[str, Json]] = []
    first_failure: Optional[dict[str, Json]] = None
    totals: dict[str, bool] = {measure: True for measure in MEASURES}
    total_obstructions = 0

    for n in range(FIRST_N, LAST_N + 1):
        pairs = obstruction_stream(n)
        total_obstructions += len(pairs)
        checks: dict[str, Json] = {}
        for reading in READINGS:
            reading_checks: dict[str, Json] = {}
            for measure in MEASURES:
                all_hold = True
                bad: Optional[MinimumClass] = None
                bad_pair: Optional[Pair] = None
                for pair in pairs:
                    classes = minimum_classes(reading, measure)
                    current_bad = _first_bad(classes)
                    if current_bad is not None:
                        all_hold = False
                        if bad is None:
                            bad = current_bad
                            bad_pair = pair
                reading_checks[measure] = {
                    "pairs_checked": len(pairs),
                    "all_minimum_iso_classes_are_pair_marks": all_hold,
                }
                totals[measure] = totals[measure] and all_hold
                if first_failure is None and bad is not None:
                    assert bad_pair is not None
                    first_failure = {
                        "n": n,
                        "chain_pair": list(bad_pair),
                        "reading": reading.name,
                        "measure": measure,
                        "class": _class_json(bad),
                    }
            checks[reading.name] = reading_checks
        per_round.append(
            {
                "n": n,
                "obstruction_count": len(pairs),
                "first_obstruction": list(pairs[0]),
                "checks": checks,
            }
        )

    terminals: list[Json] = []
    for measure in MEASURES:
        if totals[measure]:
            terminals.append(f"G4_HOLDS_UNDER_{measure.upper()}")
    if first_failure is not None:
        terminals.append(
            "G4_FAILS_AT_<3,mu1,reading_F_outside_target_argument>"
        )

    class_catalog: dict[str, Json] = {}
    for reading in READINGS:
        class_catalog[reading.name] = {
            measure: [_class_json(item) for item in catalog[(reading.name, measure)]]
            for measure in MEASURES
        }

    return {
        "bounds": {
            "first_n": FIRST_N,
            "last_n": LAST_N,
            "max_items": BOUNDS.max_items,
            "max_arity": BOUNDS.max_arity,
            "readings": [reading.name for reading in READINGS],
            "measures": list(MEASURES),
        },
        "adapter": (
            "each ordered chain-pair endpoint is mapped to the corresponding "
            "Challenge-3 target endpoint"
        ),
        "total_obstructions_checked": total_obstructions,
        "minimum_iso_classes": class_catalog,
        "rounds": per_round,
        "measure_holds_in_every_reading": totals,
        "first_failure": first_failure,
        "terminals": terminals,
        "nonclaim": (
            "finite correspondence only; no identification of the sealed "
            "engine with an object-language generator"
        ),
    }
