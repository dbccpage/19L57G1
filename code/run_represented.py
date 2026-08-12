"""Produce the represented-progress artifact deterministically.

Usage: python code/run_represented.py [--artifacts DIR] [--rounds N]

Writes ``represented.json``: the pigeonhole progress story (violation
-> tied repair family -> exhaustive obstruction certificate ->
accepted augmentation -> discharge), the prefix-compatible unbounded
run, the internal-certification scope checks, the seven
unrepresented-input countermodels, the finite-witness/no-infinite
countermodel, and the replay/mutation checks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import write_json
from derivation.represented import (
    certification_report,
    countermodel_report,
    koenig_report,
    mutation_report,
    productivity_report,
    progress_story,
)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    parser.add_argument("--rounds", type=int, default=15)
    args = parser.parse_args(argv)
    payload = {
        "bounds": {"rounds": args.rounds},
        "progress_story": progress_story(),
        "productivity": productivity_report(args.rounds),
        "certification": certification_report(),
        "countermodels": countermodel_report(),
        "koenig": koenig_report(args.rounds),
        "mutation": mutation_report(),
    }
    out_path = args.artifacts / "represented.json"
    write_json(out_path, payload)
    story = payload["progress_story"]
    assert isinstance(story, dict)
    print(
        f"pigeonhole: violated={story['violated_1_2']} "
        f"obstructed={story['obstructed_1_2']} "
        f"aug_discharges={story['discharged_after_augmentation']}"
    )
    prod = payload["productivity"]
    assert isinstance(prod, dict)
    print(
        f"productive run: prefix_compatible="
        f"{prod['all_prefix_compatible']} "
        f"carriers_initial_segments="
        f"{prod['carriers_are_initial_segments']}"
    )
    cms = payload["countermodels"]
    assert isinstance(cms, dict)
    print(f"countermodels exhibited: {cms['all_exhibited']}")
    mut = payload["mutation"]
    assert isinstance(mut, dict)
    print(
        f"mutations detected: "
        f"{mut['every_single_event_mutation_detected']} "
        f"({mut['mutations_checked']} checked)"
    )
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
