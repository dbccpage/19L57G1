"""Produce the Frontier Run 006 artifact deterministically.

Usage: python code/run_refusal_frontier.py [--artifacts DIR]
       [--max-events N]

Writes ``refusal_frontier.json``: per-protocol reports over the declared
protocol space, the notion implication matrix with countermodels, the
minimum-price table under two cost orders with all ties, and the
provenance normal-form check."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import write_json
from derivation.refusal_frontier import (
    enumerate_protocols,
    minimum_table,
    normal_form_check,
    notion_matrix,
    protocol_report,
)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    parser.add_argument("--max-events", type=int, default=6)
    args = parser.parse_args(argv)
    protos = enumerate_protocols()
    payload = {
        "protocol_space_size": len(protos),
        "protocols": [
            protocol_report(p, args.max_events) for p in protos
        ],
        "notion_matrix": notion_matrix(args.max_events),
        "minimum_table": minimum_table(args.max_events),
        "normal_form": normal_form_check(args.max_events),
    }
    out_path = args.artifacts / "refusal_frontier.json"
    write_json(out_path, payload)  # type: ignore[arg-type]
    nf = payload["normal_form"]
    assert isinstance(nf, dict)
    print(f"protocols: {len(protos)}")
    print(
        f"witnessed-irreflexive reachers: "
        f"{nf['witnessed_irreflexive_reachers']}; "
        f"normal form holds in class: {nf['normal_form_holds_in_class']}"
    )
    matrix = payload["notion_matrix"]
    assert isinstance(matrix, dict)
    imps = matrix["implications"]
    assert isinstance(imps, dict)
    live = sum(
        1 for k, v in imps.items()
        if v and k.split("->")[0] != k.split("->")[1]
    )
    print(f"notion implications holding: {live} of {len(imps)}")
    print(
        f"artifact written to "
        f"{args.artifacts / 'refusal_frontier.json'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
