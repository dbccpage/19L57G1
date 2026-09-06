"""Write or check the deterministic receipt and its rendered prose."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "code"))

from typed_translation.report import build_receipt, canonical_json, rendered_prose  # noqa: E402


RECEIPT = HERE / "receipts" / "typed_translation.json"


def expected_outputs() -> dict[Path, bytes]:
    receipt = build_receipt()
    outputs = {RECEIPT: canonical_json(receipt)}
    outputs.update(
        {HERE / name: text.encode("utf-8") for name, text in rendered_prose(receipt).items()}
    )
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    outputs = expected_outputs()
    problems: list[str] = []
    if args.check:
        for path, expected in outputs.items():
            if not path.is_file():
                problems.append(f"missing {path.relative_to(HERE)}")
            elif path.read_bytes() != expected:
                problems.append(f"drift in {path.relative_to(HERE)}")
    else:
        for path, expected in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected)
    for problem in problems:
        print(f"FAIL: {problem}")
    if problems:
        return 1
    receipt_bytes = outputs[RECEIPT]
    receipt = build_receipt()
    map_data = receipt["map"]
    removal = receipt["removal"]
    assert isinstance(map_data, dict) and isinstance(removal, dict)
    action = "checked" if args.check else "wrote"
    print(
        f"{action} typed translation: {map_data['candidate_count']} candidates, "
        f"{map_data['valid_count']} valid, removal {removal['hit_count']}/"
        f"{removal['population']}, {len(receipt_bytes)} bytes, "
        f"sha256 {hashlib.sha256(receipt_bytes).hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
