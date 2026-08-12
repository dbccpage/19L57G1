"""Produce the passage and higher-structure artifacts deterministically.

Usage: python code/run_primitive_passage.py [--artifacts DIR] [--rounds N]

Writes ``primitive_passage.json``: the per-arrow status of the
passage chain (executable side), the growth of the first graph with
per-round obstruction/response/resolution/creation records, and the
declared cell calculus: the 0-, 1-, 2-, 3-simplex demonstration with
creation logs, the named invariants (connectivity residue,
occurrence alternation number, cut census), the vanishing composite
boundary under the declared calculus, and the boundary non-forcing
countermodel."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import Json, write_json
from derivation.higher_structure import (
    EMPTY_COMPLEX,
    Complex,
    alt_num,
    boundary_not_forced,
    creplay,
    cstep,
    cut_census,
    d2_zero_tet,
    d2_zero_triangles,
    horn3,
    k4,
    k4_boundary,
    k4_events,
)
from derivation.primitive_passage import (
    GENESIS_P,
    arrow_report,
    growth_report,
    k4_passage_hist,
    obst_p,
    preplay,
)


def cells_report() -> dict[str, Json]:
    """The declared cell calculus on the four-occurrence complex."""
    passage_state = preplay(k4_passage_hist(), GENESIS_P)
    full = k4()
    shell = k4_boundary()
    stage_v = creplay(k4_events()[:4], EMPTY_COMPLEX)
    stage_e = creplay(k4_events()[:10], EMPTY_COMPLEX)
    guard_state = Complex(c0=(0, 1, 2), c1=((0, 1),))
    return {
        "skeleton_from_passage": {
            "wit": [list(r) for r in passage_state.wit],
            "prot": [list(r) for r in passage_state.prot],
            "quiescent": all(
                not obst_p(passage_state, r[0], r[1])
                for r in passage_state.prot),
            "matches_complex_c1":
                tuple(passage_state.wit) == full.c1,
        },
        "creation_log": [list(map(str, e)) for e in k4_events()],
        "cells": {
            "c0": list(full.c0),
            "c1": [list(e) for e in full.c1],
            "c2": [list(t) for t in full.c2],
            "c3": [list(q) for q in full.c3],
        },
        "ladder": {
            "horn_guard_load_bearing":
                cstep(guard_state, ("addT", 0, 1, 2)) == guard_state,
            "filling_not_forced": (
                horn3(shell, 0, 1, 2, 3) and shell.c3 == ()),
        },
        "invariants": {
            "alt_num_stages": {
                "vertices": alt_num(stage_v),
                "edges": alt_num(stage_e),
                "shell": alt_num(shell),
                "solid": alt_num(full),
            },
            "cut_census": {
                str(n): cut_census(n, 0, 1) for n in (2, 3, 4, 5)
            },
        },
        "boundary_calculus": {
            "d2_zero_triangles": d2_zero_triangles(full),
            "d2_zero_tet": d2_zero_tet(full, (0, 1, 2, 3)),
            "boundary_not_forced": boundary_not_forced((0, 1, 2)),
        },
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    parser.add_argument("--rounds", type=int, default=15)
    args = parser.parse_args(argv)
    payload: dict[str, Json] = {
        "bounds": {"rounds": args.rounds,
                   "cell_carrier": 4,
                   "cut_census_carriers": [2, 3, 4, 5]},
        "arrows": arrow_report(),
        "growth": growth_report(args.rounds),
        "cells": cells_report(),
    }
    out_path = args.artifacts / "primitive_passage.json"
    write_json(out_path, payload)
    growth = payload["growth"]
    assert isinstance(growth, dict)
    print(f"growth: spec_match={growth['all_spec_match']} "
          f"quiescent={growth['all_quiescent']} "
          f"obstructed_then_resolved="
          f"{growth['all_rounds_obstructed_then_resolved']}")
    arrows = payload["arrows"]
    assert isinstance(arrows, dict)
    print(f"arrows: all "
          f"{sum(1 for v in arrows.values() if v is True)}"
          f"/{len(arrows)} checks pass")
    cells = payload["cells"]
    assert isinstance(cells, dict)
    bc = cells["boundary_calculus"]
    assert isinstance(bc, dict)
    print(f"cells: d2_zero={bc['d2_zero_triangles']} "
          f"and {bc['d2_zero_tet']}, "
          f"not_forced={bc['boundary_not_forced']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
