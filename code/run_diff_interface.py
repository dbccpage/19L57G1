"""Produce the primitive-difference-interface artifact deterministically.

Usage: python code/run_diff_interface.py [--artifacts DIR] [--rounds N]

Writes ``diff_interface.json``: the reflective-tower pipeline rounds
(reflection -> zero-pair -> active obstruction -> orbit closure), the
fuel-driver outcomes, the bounded-grammar proposal check (exhaustive
over all eight Boolean views of three protected points), and the five
countermodels."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.diff_interface import (
    ROUNDS,
    bool_grammar_report,
    countermodel_report,
    fuel_report,
    tower_report,
)
from derivation.export import write_json


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    parser.add_argument("--rounds", type=int, default=ROUNDS)
    args = parser.parse_args(argv)
    tower = tower_report(args.rounds)
    fuel = fuel_report(args.rounds)
    grammar = bool_grammar_report()
    cms = countermodel_report()
    payload = {
        "bounds": {"rounds": args.rounds},
        "tower": tower,
        "fuel": fuel,
        "bool_grammar": grammar,
        "countermodels": cms,
    }
    out_path = args.artifacts / "diff_interface.json"
    write_json(out_path, payload)
    print(f"tower rounds: {args.rounds}")
    print(
        "strict decrease every closure: "
        f"{tower['all_strictly_decrease']}; "
        f"old distinctions preserved: {tower['all_preserve_old']}"
    )
    print(f"fuel outcomes all closed: {fuel['all_terminate_closed']}")
    print(
        f"grammar views checked: {grammar['views_checked']}; "
        f"proposal required: {grammar['proposal_required']}"
    )
    print(
        "countermodels zero-despite-feature: "
        f"{cms['all_zero_despite_feature']}"
    )
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
