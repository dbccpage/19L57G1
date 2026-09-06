"""The calibration: this tree's machinery, run against the sealed answer.

Classification: metatheory apparatus.

It runs **first** and gates every other receipt.  Restricting this tree's
space to the four sealed item kinds with no readers, and running this tree's
own pricing routine with the sealed separation demand at the two sealed bases,
must reproduce ``artifacts/challenges.json`` ``challenge3`` field by field.

A failure voids the tree: this tree re-implements the sealed kernel rather
than importing it, so agreement here is the only thing standing between a
re-implementation and a lookalike.
"""

from __future__ import annotations

from .demands import Demand, Situation, SINGLE_STATE
from .enumerate_space import Bounds
from .grammar import profiles
from .items import Delta
from .price import Minimum, price
from .regime import Impose, Pair, Regime, genesis, step

CALIBRATION_BOUNDS = Bounds(
    max_items=2,
    max_sealed_items=2,
    max_reader_items=0,
    max_arity=2,
    w_max=3,
    max_readers=2,
)


def satisfies_requirements(r: Regime) -> bool:
    """Every imposed separation requirement holds."""
    profs = profiles(r)
    return all(profs[i] != profs[j] for (i, j) in sorted(r.reqs))


def separation_demand(target: Pair) -> Demand:
    """The sealed Challenge-3 demand: separate the imposed target."""

    def predicate(sit: Situation) -> bool:
        augmented = step(sit.state.regime, Impose(target[0], target[1]))
        return satisfies_requirements(augmented)

    return Demand(
        f"SEP{target}",
        predicate,
        SINGLE_STATE,
        "the externally imposed pair is internally separable",
        impose=target,
    )


def calibrate(reading: str, measure: str) -> Minimum:
    from .regime import READING_TARGET

    base = genesis(reading)
    return price(
        base,
        reading,
        separation_demand(READING_TARGET[reading]),
        measure,
        CALIBRATION_BOUNDS,
        prune=False,
    )


#: The committed sealed answer, transcribed from ``artifacts/challenges.json``
#: at the pinned snapshot.  This tree does not tune to it: the transcription
#: is pinned by sha256 in ``SOURCE_MANIFEST.json`` and CI regenerates the
#: sealed artifact independently.
SEALED_CHALLENGE3: dict[tuple[str, str], dict[str, object]] = {
    ("L", "mu1"): {
        "minimum_cost": (2, -1),
        "valid_deltas_at_minimum": 6,
        "iso_classes": 3,
        "cost_below_minimum_all_fail": True,
    },
    ("L", "mu2"): {
        "minimum_cost": (2, 1),
        "valid_deltas_at_minimum": 2,
        "iso_classes": 1,
        "cost_below_minimum_all_fail": True,
    },
    ("F", "mu1"): {
        "minimum_cost": (2, -1),
        "valid_deltas_at_minimum": 10,
        "iso_classes": 5,
        "cost_below_minimum_all_fail": True,
    },
    ("F", "mu2"): {
        "minimum_cost": (2, 1),
        "valid_deltas_at_minimum": 2,
        "iso_classes": 1,
        "cost_below_minimum_all_fail": True,
    },
}


def calibration_report() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    agree = True
    for reading in ("L", "F"):
        for measure in ("mu1", "mu2"):
            m = calibrate(reading, measure)
            want = SEALED_CHALLENGE3[(reading, measure)]
            got = {
                "minimum_cost": m.cost,
                "valid_deltas_at_minimum": len(m.raw_minima),
                "iso_classes": len(m.classes),
                "cost_below_minimum_all_fail":
                    m.cost_below_minimum_all_fail,
            }
            ok = got == want
            agree = agree and ok
            rows.append(
                {
                    "reading": reading,
                    "measure": measure,
                    "sealed": {k: list(v) if isinstance(v, tuple) else v
                               for k, v in want.items()},
                    "recomputed": {k: list(v) if isinstance(v, tuple) else v
                                   for k, v in got.items()},
                    "agrees": ok,
                }
            )
    return {"rows": rows, "agrees_field_by_field": agree}
