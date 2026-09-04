"""Run both sides and write the receipt deterministically (``--out DIR``).

The receipt records computations; it proves no theorem.  Keys are sorted
and no timestamp or environment value is written.  AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import dual_side
import sealed_side

ADVERSARIAL: dict[str, str] = {
    "A1": "reach is not a better measure; it is a different one, and the sealed measures keep their meaning",
    "A2": "reach never widens the valid set; the sealed and dual enumerators remain the authority on validity",
    "A3": "the sealed side shows no local-versus-global choice because a rule item is not even well formed at the sealed Challenge-3 base, which has no forms",
    "A4": "a rule is not global by syntax; a rule whose form has one plugging left has reach one, and reach says so",
    "A5": "the partition of demands into locally repairable and not is a property of the pinned rectangle, not of all demands",
    "A6": "the blindness theorem is about the FORM of a base-free measure, not about mu1 and mu2 in particular",
    "A7": "Lean proves the blindness; the receipt records the computation",
}


def build() -> dict[str, object]:
    return {
        "adversarial": ADVERSARIAL,
        "authority_effect": "None",
        "dual_side": dual_side.report(),
        "measure": {
            "name": "reach",
            "definition": "the number of pluggings that become derivable: the growth in total profile size",
            "mu3": "(reach, item count), lexicographic, reach leading",
            "base_relative": True,
            "refines_mu1": False,
        },
        "sealed_side": sealed_side.report(),
        "snapshot": "7fcd72f6",
        "write_root": "research/reach_measure/",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=Path("receipts"))
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    report = build()
    (args.out / "reach_measure.json").write_bytes(
        (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    d = report["dual_side"]
    assert isinstance(d, dict)
    print(f"dual side: {d['answered']} demands answered, "
          f"{d['demands_where_only_rules_are_valid']} admit only rules, "
          f"{d['demands_where_reach_picks_the_instance_over_the_rule']} re-selected")
    print(f"cross-kind ties: mu1 {d['mu1_ties_spanning_two_item_kinds']} "
          f"-> mu3 {d['mu3_ties_spanning_two_item_kinds']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
