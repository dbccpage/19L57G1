"""Write the side-free control's receipt.

Sorted keys, LF only and no timestamp. The frozen conditional source-check
field can vary without the required source; validated runs require that
source and byte-identical regeneration. ``--check`` never writes.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "code"))

from sidefree.control import decide, render  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
RECEIPT = HERE / "receipts" / "side_free.json"
LIMIT = 1_000_000


def gate_problems(record: dict[str, object]) -> list[str]:
    """Every problem the gates named, so a VOID record says WHY by name."""
    gates = record["gates"]
    if not isinstance(gates, dict):
        return ["the record carries no gate block"]
    problems: list[str] = []
    for name, gate in sorted(gates.items()):
        if not isinstance(gate, dict):
            continue
        for problem in gate.get("problems", []) or []:
            problems.append(f"{name}: {problem}")
    return problems


def main(argv: list[str]) -> int:
    record = decide()
    if record["void"]:
        print("FAIL: the record is VOID and NO difference is reported")
        for problem in gate_problems(record):
            print(f"FAIL: {problem}")
        return 1
    payload = render(record)
    if len(payload) > LIMIT:
        print(
            f"FAIL: the receipt is {len(payload)} bytes, over the {LIMIT} byte "
            f"bound; split it into a summary plus a hashed archive"
        )
        return 1
    if "--check" in argv:
        if not RECEIPT.exists():
            print("FAIL: receipts/side_free.json is missing")
            return 1
        if RECEIPT.read_bytes() != payload:
            print("FAIL: receipts/side_free.json differs from a fresh computation")
            return 1
        print(f"receipt ok: {len(payload)} bytes, byte-identical")
        return 0
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_bytes(payload)
    print(f"wrote {RECEIPT.relative_to(HERE).as_posix()}: {len(payload)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
