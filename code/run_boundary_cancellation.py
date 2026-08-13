"""Produce the boundary-cancellation artifact deterministically.

Usage: python code/run_boundary_cancellation.py [--artifacts DIR]
       [--max-vertices N] [--min-dim D] [--max-dim D]

Writes ``boundary_cancellation.json``: the exhaustive re-check, over
the declared finite bounds, of the general boundary-cancellation
theorem proved in ``lean4/Derivation/BoundaryCancellation.lean`` — the
composite boundary has coefficient zero at every presentation, for
every strictly ascending cell whose vertices come from the first
``--max-vertices`` numerals, in dimensions ``--min-dim`` through
``--max-dim``; the deletion-order involution on the index rectangle
(fixed-point-free, face-preserving, sign-reversing); the identity
between the collected coefficient and the rectangle double sum; the
distinctness statements that strict ascent actually buys; renaming
independence with its exact scope; and the two required countermodels
(signless composite nonzero, repeated-vertex pseudo-cell)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.boundary_cancellation import (
    cancellation_report,
    illformed_countermodel,
    renaming_report,
    signless_countermodel,
)
from derivation.export import Json, write_json


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    parser.add_argument("--max-vertices", type=int, default=8)
    parser.add_argument("--min-dim", type=int, default=2)
    parser.add_argument("--max-dim", type=int, default=6)
    args = parser.parse_args(argv)
    cancellation = cancellation_report(
        args.max_vertices, args.min_dim, args.max_dim)
    payload: dict[str, Json] = {
        "declared_inputs": [
            "the ascending-list cell encoding",
            "integer coefficients",
            "the alternating sign convention (-1)^i",
        ],
        "scope": (
            "the vanishing is proved in Lean for EVERY list and every "
            "presentation (d2_zero_unrestricted); the ascent and "
            "dimension hypotheses of d2_zero_general are recorded, not "
            "used.  Strict ascent is load-bearing only for the "
            "distinctness statements.  Nothing here is a homology "
            "claim: the coefficients and signs are declared inputs, "
            "not consequences of the filler rule."),
        "cancellation": cancellation,
        "renaming": renaming_report(
            args.max_vertices, args.min_dim, args.max_dim),
        "countermodels": {
            "signless": signless_countermodel(),
            "illformed": illformed_countermodel(),
        },
    }
    out_path = args.artifacts / "boundary_cancellation.json"
    write_json(out_path, payload)
    bounds = cancellation["bounds"]
    assert isinstance(bounds, dict)
    print(f"bounds: vertices<={bounds['max_vertices']} "
          f"dims {bounds['min_dim']}..{bounds['max_dim']} "
          f"cells={bounds['cells_checked']} "
          f"coefficient_checks={bounds['coefficient_checks']}")
    print(f"cancellation: all_cancel={cancellation['all_cancel']} "
          f"all_distinct={cancellation['all_distinct']} "
          f"sgn_cancel_pairs={cancellation['sgn_cancel_pairs']}")
    ren = payload["renaming"]
    assert isinstance(ren, dict)
    print(f"renaming: ascent={ren['monotone_preserves_ascent']} "
          f"faces={ren['faces_transport']} "
          f"cancels={ren['monotone_cancels']}")
    cms = payload["countermodels"]
    assert isinstance(cms, dict)
    signless = cms["signless"]
    assert isinstance(signless, dict)
    illformed = cms["illformed"]
    assert isinstance(illformed, dict)
    print(f"countermodels: signless_nonzero="
          f"{signless['all_signless_nonzero']} "
          f"illformed_distinctness_fails="
          f"{not illformed['erase_injective']} "
          f"illformed_still_cancels="
          f"{illformed['composite_still_vanishes']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
