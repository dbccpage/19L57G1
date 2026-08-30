"""Write the P2 receipt: ``receipts/morphism_classes.json``.

Usage (from inside ``research/s9_obligations/``, with ``PYTHONPATH``
pointing at ``code/``):

    python run_morphism_classes.py --out receipts

The computation is ``morphism_classes.compute`` at the attempted object
carrier declared in PREFLIGHT.md (N = 4, which completed); the receipt
records the carrier actually reached under ``bounds_reached``.  The
receipt is timestamp-free and replays byte-identically (PROMPT.md step
33): run twice into two directories and compare bytes.  AuthorityEffect:
None.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

import common
import morphism_classes as mc

RECEIPT_NAME = "morphism_classes.json"


def key_lines(receipt: dict[str, object]) -> list[str]:
    """The headline numbers, each read back from the receipt it names."""

    lines = [
        f"menu_size: {receipt['menu_size']}",
        f"class_count: {receipt['class_count']}",
    ]
    bounds = receipt["bounds_reached"]
    assert isinstance(bounds, dict)
    shapes = receipt["shape"]
    assert isinstance(shapes, dict)
    ties = receipt["ties"]
    assert isinstance(ties, dict)
    summary = receipt["cell_summary"]
    assert isinstance(summary, dict)
    for key in ("primary", "secondary"):
        reached = bounds[key]
        sh = shapes[key]
        tr = ties[key]
        cs = summary[key]
        lines.append(
            f"{key}: carrier_reached {reached['carrier_reached']}, "
            f"objects_checked_total {reached['objects_checked_total']}, "
            f"candidate_iso_classes {reached['candidate_iso_classes']}, "
            f"cells {cs['cells']}, initial {cs['initial']}"
        )
        lines.append(
            f"{key}: admitting {sh['admitting_classes']}, minimal {sh['minimal']}, "
            f"maximal {sh['maximal']}, is_interval {sh['is_interval']}, "
            f"terminal {sh['terminal']}"
        )
        lines.append(f"{key}: classes_with_ties {tr['classes_with_ties']}, max_tie {tr['max_tie']}")
        lines.append(
            f"{key}: table_identical_at_required_carrier "
            f"{reached['table_identical_at_required_carrier']} (N = {reached['required_carrier']})"
        )
    groups = receipt["witness_groups"]
    assert isinstance(groups, dict)
    for key in ("primary", "secondary"):
        wg = groups[key]
        no_p = wg["no_P_classes"]
        lines.append(
            f"{key}: witness_groups partition {wg['partition_cell_counts']} = "
            f"{wg['partition_cell_total']} of {wg['table_cells']} cells, "
            f"disjoint_and_exhaustive {wg['partition_is_disjoint_and_exhaustive']}"
        )
        lines.append(
            f"{key}: no_P_classes cells {no_p['cells']}, initial {no_p['initial']}, "
            f"with_uniqueness_witness {no_p['with_uniqueness_witness']}, "
            f"without_uniqueness_witness {no_p['without_uniqueness_witness']}, "
            f"with_existence_witness {no_p['with_existence_witness']}"
        )
    d2 = receipt["d2_initial_pointed_cell"]
    assert isinstance(d2, dict)
    lines.append(
        f"d2_initial_pointed_cell: model_agrees_at_bound {d2['model_agrees_at_bound']}, "
        f"direct_check agrees {d2['direct_check']['agrees_with_theorem']} over "
        f"{d2['direct_check']['objects_checked']} objects at carrier "
        f"{d2['direct_check']['carrier_reached']}"
    )
    terminals = receipt["terminals"]
    assert isinstance(terminals, list)
    for item in terminals:
        lines.append(f"terminal {item['terminal']} -- {item['scope']}")
    return lines


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write the P2 (S9.2) receipt.")
    parser.add_argument("--out", default="receipts", help="output directory (inside the tree)")
    args = parser.parse_args(argv)
    receipt = mc.compute(mc.ATTEMPTED_N)
    target = common.write_receipt(Path(args.out) / RECEIPT_NAME, receipt)
    print(f"wrote {target.relative_to(common.TREE).as_posix()}")
    for line in key_lines(receipt):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
