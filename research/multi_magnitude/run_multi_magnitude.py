"""Runner for multi-magnitude carrier verification and receipt emission.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from separation_proof import generate_lp4_resolution_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-magnitude carrier runner.")
    parser.add_argument("--out", default=str(HERE / "receipts"))
    args = parser.parse_args()

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Generating LP4 resolution and channel separation report...")
    report = generate_lp4_resolution_report()

    out_file = out_dir / "carrier.json"
    content = json.dumps(report, indent=2, sort_keys=True) + "\n"
    out_file.write_text(content, encoding="utf-8")
    print(f"Receipt written to {out_file}")

    mm = report["multi_magnitude_resolution"]["channel_table"]
    print(f"Status: {report['status']}")
    print(f"Cells: {mm['cells']}")
    print(f"Terminal: {mm['terminal']}")
    print(f"Separated: {mm['separated']}")
    print(f"Operational magnitudes carried: {report['multi_magnitude_resolution']['operational_magnitudes_carried']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
