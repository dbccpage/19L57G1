"""Produce the attachment/ladder artifact deterministically.

Usage: python code/run_attachment_ladder.py [--artifacts DIR]
       [--rounds N] [--max-dim D]

Writes ``attachment_ladder.json``: tree growth under path, star, and
zigzag policies checked against the characterized record (every
policy yields a tree, V - E = 1 throughout, pre-observational); the
non-forcing of global shape (path vs star non-isomorphic at four
occurrences); the complete Up family with presentation invariance
and orbit-valued parent choices; and the generalized ladder replayed
at dimensions 2 through the bound with guard load-bearing and
boundary-composite checks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.attachment_ladder import (
    ladder_report,
    shape_report,
    tree_report,
    up_report,
)
from derivation.export import Json, write_json


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    parser.add_argument("--rounds", type=int, default=15)
    parser.add_argument("--max-dim", type=int, default=5)
    args = parser.parse_args(argv)
    payload: dict[str, Json] = {
        "bounds": {"rounds": args.rounds, "max_dim": args.max_dim,
                   "shape_carrier": 4, "orbit_carrier": 3},
        "imported_inputs": [
            "fresh occurrence supply (canonical next numeral)",
            "protection", "observer transport (unused: attachment "
            "is pre-observational)", "budget/activation",
            "cell encoding and boundary signs",
            "metatheoretic driver iteration",
        ],
        "trees": tree_report(args.rounds),
        "shape": shape_report(),
        "up": up_report(),
        "ladder": ladder_report(args.max_dim),
    }
    out_path = args.artifacts / "attachment_ladder.json"
    write_json(out_path, payload)
    trees = payload["trees"]
    assert isinstance(trees, dict)
    print("trees: " + ", ".join(
        f"{k}:spec={v['all_spec_match']},tree={v['all_trees']}"
        for k, v in trees.items() if isinstance(v, dict)))
    shape = payload["shape"]
    assert isinstance(shape, dict)
    print(f"shape not forced: "
          f"{shape['trees_but_shapes_differ']}")
    ladder = payload["ladder"]
    assert isinstance(ladder, dict)
    print(f"ladder dims {ladder['dims_checked']}: "
          f"fire={ladder['all_ladders_fire']} "
          f"guards={ladder['all_guards_load_bearing']} "
          f"d2zero={ladder['all_d2_zero']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
