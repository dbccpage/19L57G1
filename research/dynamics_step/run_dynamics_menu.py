"""
run_dynamics_menu.py — Generate dynamics menu and collapse receipt

<!-- AuthorityEffect: None -->
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from derivation.export import Json, write_json
from derivation.model import AdmitDatum, replay
from dynamics_menu import (
    inspect_response_menu,
    five_atom_collapse_exhibit,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--receipts",
        type=Path,
        default=Path("research/dynamics_step/receipts"),
    )
    args = parser.parse_args()

    # 1. Challenge 3 base menu inspection under mu1 & mu2
    base = replay([AdmitDatum("a"), AdmitDatum("ab")])
    pair = (0, 1)

    menu_mu1 = inspect_response_menu(base, pair, measure="mu1")
    menu_mu2 = inspect_response_menu(base, pair, measure="mu2")

    # 2. 5-atom collapse exhibit
    exhibit = five_atom_collapse_exhibit()

    payload: dict[str, Json] = {
        "challenge3_base_menu": {
            "mu1": {
                "attained_cost": list(menu_mu1.attained_cost) if menu_mu1.attained_cost else None,
                "is_tied": menu_mu1.is_tied,
                "candidate_count": len(menu_mu1.candidate_deltas),
            },
            "mu2": {
                "attained_cost": list(menu_mu2.attained_cost) if menu_mu2.attained_cost else None,
                "is_tied": menu_mu2.is_tied,
                "candidate_count": len(menu_mu2.candidate_deltas),
            },
        },
        "five_atom_collapse_exhibit": {
            "atom_cost": exhibit.atom_cost,
            "uncollapsed_holds": exhibit.uncollapsed_holds,
            "quotient_holds": exhibit.quotient_holds,
            "law_failed_in_quotient": exhibit.law_failed_in_quotient,
            "status": "EXHIBIT_ONLY_NOT_UNIQUENESS_SEARCH",
        },
    }

    out_path = args.receipts / "dynamics_menu_receipt.json"
    write_json(out_path, payload)
    print(f"Receipt written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
